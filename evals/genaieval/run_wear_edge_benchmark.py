# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import json
import statistics
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path

from wear_edge_eval import DEFAULT_DATASET, evaluate_case, load_dataset


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark the WearEdge GenAIEval-compatible route suite.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "genaieval" / "benchmark_results.json")
    args = parser.parse_args()

    cases = load_dataset(args.dataset)
    if args.iterations < 1:
        raise SystemExit("--iterations must be >= 1")
    if args.warmup < 0:
        raise SystemExit("--warmup must be >= 0")

    for _ in range(args.warmup):
        for case in cases:
            evaluate_case(case)

    latencies: list[float] = []
    route_latencies: dict[str, list[float]] = {}
    failures: list[dict] = []
    tracemalloc.start()
    start = time.perf_counter()
    total_calls = 0
    for _ in range(args.iterations):
        for case in cases:
            total_calls += 1
            case_start = time.perf_counter()
            result = evaluate_case(case)
            elapsed_ms = (time.perf_counter() - case_start) * 1000
            latencies.append(elapsed_ms)
            route_latencies.setdefault(case["mode"], []).append(elapsed_ms)
            if not result["ok"]:
                failures.append({"case_id": case["case_id"], "mode": case["mode"], "metrics": result["metrics"]})
    total_seconds = time.perf_counter() - start
    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    report = {
        "suite": "WearEdge GenAIEval-compatible manufacturing route benchmark",
        "schema_version": "2026-05-28",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "compatibility": {
            "official_genaieval_runner_used": False,
            "claim_boundary": (
                "Benchmark uses the local deterministic WearEdge route runner and GenAIEval-compatible "
                "metric schema. It is not a full official GenAIEval/RAGAS/AutoRAG/LLM-as-judge run."
            ),
        },
        "benchmark_config": {
            "dataset": args.dataset.relative_to(ROOT).as_posix(),
            "cases_per_iteration": len(cases),
            "iterations": args.iterations,
            "warmup": args.warmup,
            "total_calls": total_calls,
        },
        "summary": {
            "ok": not failures,
            "total_seconds": round(total_seconds, 4),
            "calls_per_second": round(total_calls / total_seconds, 4) if total_seconds else 0.0,
            "latency_ms": _summarize(latencies),
            "python_tracemalloc": {
                "current_mb": round(current_bytes / 1024 / 1024, 4),
                "peak_mb": round(peak_bytes / 1024 / 1024, 4),
            },
        },
        "routes": {mode: _summarize(values) for mode, values in route_latencies.items()},
        "validation": {
            "all_cases_pass": not failures,
            "routes_covered": sorted(route_latencies) == ["changeover", "hazard", "iqc", "maintenance", "wi"],
            "failures": failures[:10],
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    status = "passed" if report["summary"]["ok"] else "requires review"
    print(f"WearEdge GenAIEval-compatible benchmark {status}: {total_calls} calls")
    print(args.output)
    return 0 if report["summary"]["ok"] else 1


def _summarize(values: list[float]) -> dict:
    if not values:
        return {"count": 0, "min_ms": 0.0, "mean_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "max_ms": 0.0}
    ordered = sorted(values)
    return {
        "count": len(values),
        "min_ms": round(ordered[0], 4),
        "mean_ms": round(statistics.fmean(ordered), 4),
        "p50_ms": _percentile(ordered, 50),
        "p95_ms": _percentile(ordered, 95),
        "max_ms": round(ordered[-1], 4),
    }


def _percentile(ordered_values: list[float], percentile: int) -> float:
    index = min(len(ordered_values) - 1, round((percentile / 100) * (len(ordered_values) - 1)))
    return round(ordered_values[index], 4)


if __name__ == "__main__":
    raise SystemExit(main())
