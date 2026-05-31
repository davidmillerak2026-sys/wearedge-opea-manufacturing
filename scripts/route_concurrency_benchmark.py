# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
import tracemalloc
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wear_edge_opea.agents import ROUTES, load_sample_request  # noqa: E402
from wear_edge_opea.megaservice import run_pipeline  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark concurrent WearEdge route requests.")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--requests-per-route", type=int, default=20)
    parser.add_argument("--warmup-per-route", type=int, default=1)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "evidence" / "benchmarks" / "route_concurrency.local-smoke.json",
    )
    args = parser.parse_args()

    if args.concurrency < 1:
        raise SystemExit("--concurrency must be >= 1")
    if args.requests_per_route < 1:
        raise SystemExit("--requests-per-route must be >= 1")
    if args.warmup_per_route < 0:
        raise SystemExit("--warmup-per-route must be >= 0")

    modes = list(ROUTES)
    samples = {mode: load_sample_request(mode) for mode in modes}
    for _ in range(args.warmup_per_route):
        for mode in modes:
            run_pipeline(dict(samples[mode]), mode=mode)

    jobs = [
        {"mode": mode, "request": dict(samples[mode])}
        for mode in modes
        for _ in range(args.requests_per_route)
    ]

    tracemalloc.start()
    start = time.perf_counter()
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(_run_one, job["mode"], job["request"]) for job in jobs]
        for future in as_completed(futures):
            results.append(future.result())
    wall_seconds = time.perf_counter() - start
    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    failures = [item for item in results if not item["ok"]]
    by_route: dict[str, list[float]] = {mode: [] for mode in modes}
    for item in results:
        by_route.setdefault(item["mode"], []).append(item["latency_ms"])

    report = {
        "suite": "WearEdge OPEA Manufacturing concurrent route benchmark",
        "schema_version": "2026-05-28",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "claim_boundary": (
            "This is a local deterministic route-concurrency benchmark for the WearEdge "
            "Manufacturing megaservice. It validates concurrent request handling for the "
            "released route pipeline, not production LLM serving or certified plant control."
        ),
        "config": {
            "concurrency": args.concurrency,
            "requests_per_route": args.requests_per_route,
            "warmup_per_route": args.warmup_per_route,
            "total_requests": len(jobs),
            "routes": modes,
        },
        "summary": {
            "ok": not failures,
            "wall_seconds": round(wall_seconds, 4),
            "requests_per_second": round(len(jobs) / wall_seconds, 4) if wall_seconds else 0.0,
            "latency_ms": _summarize([item["latency_ms"] for item in results]),
            "python_tracemalloc": {
                "current_mb": round(current_bytes / 1024 / 1024, 4),
                "peak_mb": round(peak_bytes / 1024 / 1024, 4),
            },
        },
        "routes": {mode: _summarize(values) for mode, values in by_route.items()},
        "validation": {
            "all_requests_ok": not failures,
            "all_routes_covered": sorted(by_route) == sorted(modes),
            "all_action_targets_correct": all(item["action_target_correct"] for item in results),
            "failures": failures[:10],
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"WearEdge concurrent route benchmark {'passed' if report['summary']['ok'] else 'failed'}")
    print(args.output)
    return 0 if report["summary"]["ok"] else 1


def _run_one(mode: str, request: dict) -> dict:
    start = time.perf_counter()
    try:
        result = run_pipeline(request, mode=mode)
        action_card = result.get("action_card", {})
        expected_target = ROUTES[mode].integration_target
        return {
            "ok": bool(result.get("ok")) and action_card.get("integration_target") == expected_target,
            "mode": result.get("mode", mode),
            "latency_ms": round((time.perf_counter() - start) * 1000, 4),
            "action_target_correct": action_card.get("integration_target") == expected_target,
            "integration_target": action_card.get("integration_target"),
        }
    except Exception as exc:  # pragma: no cover - included in JSON evidence if hit
        return {
            "ok": False,
            "mode": mode,
            "latency_ms": round((time.perf_counter() - start) * 1000, 4),
            "action_target_correct": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


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
