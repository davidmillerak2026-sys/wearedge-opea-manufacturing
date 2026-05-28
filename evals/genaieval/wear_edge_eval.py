from __future__ import annotations

import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = ROOT / "evals" / "genaieval" / "manufacturing_route_eval.dataset.jsonl"
CONTRACT_FIELDS = {
    "mode",
    "channel",
    "priority",
    "owner",
    "requires_human_confirmation",
    "integration_target",
    "action",
    "source_ids",
    "blocked_claims",
}

if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from wear_edge_opea.agents import ROUTES  # noqa: E402
from wear_edge_opea.megaservice import run_pipeline  # noqa: E402


def load_dataset(path: Path = DEFAULT_DATASET) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        case = json.loads(stripped)
        case.setdefault("case_id", f"line-{line_number}")
        cases.append(case)
    return cases


def evaluate_dataset(cases: list[dict[str, Any]], dataset_path: Path = DEFAULT_DATASET) -> dict[str, Any]:
    case_results = [evaluate_case(case) for case in cases]
    return build_report(case_results, dataset_path)


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    mode = case["mode"]
    expected = case["expected"]
    start = time.perf_counter()
    result = run_pipeline(case["request"], mode=mode)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 4)

    action_card = result["action_card"]
    evaluation = result["agent_evaluation"]
    source_ids = list(action_card.get("source_ids", []))
    blocked_claims = list(action_card.get("blocked_claims", []))

    checks = {
        "contract_pass": CONTRACT_FIELDS.issubset(action_card),
        "action_target_correctness": action_card.get("integration_target") == expected["integration_target"],
        "channel_correctness": action_card.get("channel") == expected["channel"],
        "risk_level_correctness": evaluation.get("risk_level") == expected["risk_level"],
        "human_gate_correctness": action_card.get("requires_human_confirmation")
        is expected["requires_human_confirmation"],
        "guardrail_pass": _includes_all(blocked_claims, expected.get("blocked_claims_include", []))
        and _excludes_all(blocked_claims, expected.get("blocked_claims_absent", [])),
        "rag_source_match": _rag_source_match(result, expected),
        "route_isolation_pass": _route_isolation_pass(result, expected),
    }

    return {
        "case_id": case["case_id"],
        "mode": mode,
        "ok": all(checks.values()),
        "metrics": checks,
        "actual": {
            "channel": action_card.get("channel"),
            "integration_target": action_card.get("integration_target"),
            "risk_level": evaluation.get("risk_level"),
            "priority": action_card.get("priority"),
            "requires_human_confirmation": action_card.get("requires_human_confirmation"),
            "source_ids": source_ids,
            "blocked_claims": blocked_claims,
            "latency_ms": result["timing"]["pipeline_latency_ms"],
            "eval_latency_ms": elapsed_ms,
            "rag_vector_store": result["rag"].get("vector_store"),
            "llm_runtime": result.get("llm_runtime", {}),
        },
    }


def build_report(case_results: list[dict[str, Any]], dataset_path: Path = DEFAULT_DATASET) -> dict[str, Any]:
    metric_names = list(case_results[0]["metrics"]) if case_results else []
    metric_summary = {
        name: {
            "passed": sum(1 for case in case_results if case["metrics"][name]),
            "total": len(case_results),
        }
        for name in metric_names
    }
    for metric in metric_summary.values():
        metric["pass_rate"] = _ratio(metric["passed"], metric["total"])

    per_route = {}
    for mode in ROUTES:
        route_cases = [case for case in case_results if case["mode"] == mode]
        route_latencies = [case["actual"]["eval_latency_ms"] for case in route_cases]
        per_route[mode] = {
            "cases": len(route_cases),
            "passed": sum(1 for case in route_cases if case["ok"]),
            "pass_rate": _ratio(sum(1 for case in route_cases if case["ok"]), len(route_cases)),
            "mean_eval_latency_ms": _mean(route_latencies),
            "p95_eval_latency_ms": _percentile(route_latencies, 95),
            "status": "pass" if route_cases and all(case["ok"] for case in route_cases) else "review",
        }

    passed_cases = sum(1 for case in case_results if case["ok"])
    return {
        "suite": "WearEdge GenAIEval-compatible manufacturing route evaluation",
        "schema_version": "2026-05-28",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "compatibility": {
            "official_genaieval_runner_used": False,
            "claim_boundary": (
                "This is a lightweight GenAIEval-compatible artifact: JSONL dataset, "
                "benchmark config, deterministic runner, metrics, and evidence JSON. "
                "It does not claim full official GenAIEval/RAGAS/AutoRAG/LLM-as-judge execution."
            ),
            "maps_to_genaieval_concepts": [
                "dataset",
                "task runner",
                "metric outputs",
                "latency benchmark",
                "pass/fail summary",
                "reproducible evidence artifact",
            ],
        },
        "dataset": {
            "path": dataset_path.relative_to(ROOT).as_posix(),
            "cases": len(case_results),
            "routes": list(ROUTES),
        },
        "metrics": metric_names,
        "summary": {
            "ok": passed_cases == len(case_results),
            "total_cases": len(case_results),
            "passed_cases": passed_cases,
            "pass_rate": _ratio(passed_cases, len(case_results)),
            "per_metric": metric_summary,
            "per_route": per_route,
        },
        "cases": case_results,
    }


def write_json_report(report: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown_summary(report: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary = report["summary"]
    per_route = summary["per_route"]
    lines = [
        "# WearEdge GenAIEval-Compatible Evaluation Summary",
        "",
        f"Generated UTC: `{report['generated_at_utc']}`",
        "",
        "Claim boundary: lightweight GenAIEval-compatible evidence package; not a full official GenAIEval/RAGAS/AutoRAG/LLM-as-judge run.",
        "",
        f"Overall: `ok={str(summary['ok']).lower()}`, `{summary['passed_cases']}/{summary['total_cases']}` cases passed, pass rate `{summary['pass_rate']}`.",
        "",
        "| Route | Cases | Passed | Pass rate | Mean eval latency ms | P95 eval latency ms | Status |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for mode, route in per_route.items():
        lines.append(
            f"| `{mode}` | {route['cases']} | {route['passed']} | {route['pass_rate']} | "
            f"{route['mean_eval_latency_ms']} | {route['p95_eval_latency_ms']} | `{route['status']}` |"
        )
    lines.extend(
        [
            "",
            "Metrics:",
            "",
        ]
    )
    for metric, values in summary["per_metric"].items():
        lines.append(f"- `{metric}`: `{values['passed']}/{values['total']}` passed, pass rate `{values['pass_rate']}`")
    lines.extend(
        [
            "",
            "Artifacts:",
            "",
            "- `evals/genaieval/manufacturing_route_eval.dataset.jsonl`",
            "- `evals/genaieval/manufacturing_route_benchmark.yaml`",
            "- `evals/genaieval/run_wear_edge_eval.py`",
            "- `evals/genaieval/run_wear_edge_benchmark.py`",
            "- `evidence/genaieval/route_eval_results.json`",
            "- `evidence/genaieval/benchmark_results.json`",
            "- `evidence/genaieval/summary.md`",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _rag_source_match(result: dict[str, Any], expected: dict[str, Any]) -> bool:
    source_ids = set(result["action_card"].get("source_ids", []))
    allowed = set(expected.get("source_ids_all_within", []))
    min_hits = int(expected.get("source_ids_min", 1))
    payload_modes = {
        hit.get("payload", {}).get("mode")
        for hit in result.get("rag", {}).get("hits", [])
        if hit.get("payload")
    }
    if len(source_ids) < min_hits:
        return False
    if allowed and not source_ids.issubset(allowed):
        return False
    if expected.get("source_ids_include_any") and not source_ids.intersection(expected["source_ids_include_any"]):
        return False
    return payload_modes == {result["mode"]}


def _route_isolation_pass(result: dict[str, Any], expected: dict[str, Any]) -> bool:
    action_card = result["action_card"]
    forbidden_targets = set(expected.get("forbidden_integration_targets", []))
    return (
        result["mode"] == action_card.get("mode")
        and action_card.get("integration_target") not in forbidden_targets
        and _excludes_all(action_card.get("blocked_claims", []), expected.get("blocked_claims_absent", []))
    )


def _includes_all(actual: list[str], expected: list[str]) -> bool:
    return set(expected).issubset(set(actual))


def _excludes_all(actual: list[str], blocked: list[str]) -> bool:
    return set(actual).isdisjoint(set(blocked))


def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(statistics.fmean(values), 4)


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, round((percentile / 100) * (len(ordered) - 1)))
    return round(ordered[index], 4)
