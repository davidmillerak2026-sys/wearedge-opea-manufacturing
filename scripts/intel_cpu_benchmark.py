"""Run a dependency-free Intel CPU benchmark for the WearEdge OPEA suite.

The script is intentionally CI-friendly. It measures the deterministic
five-agent pipeline and records whether the host advertises AVX-512 or AMX
features. Run it again on an Intel Xeon host to produce the competition
bonus evidence for AVX-512/AMX.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wear_edge_opea.agents import ROUTES, load_sample_request  # noqa: E402
from wear_edge_opea.megaservice import run_pipeline  # noqa: E402
from wear_edge_opea.scorecard import build_scorecard  # noqa: E402


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, round((len(ordered) - 1) * percentile))
    return ordered[index]


def _read_linux_cpuinfo() -> tuple[str | None, set[str]]:
    cpuinfo = Path("/proc/cpuinfo")
    if not cpuinfo.exists():
        return None, set()
    text = cpuinfo.read_text(encoding="utf-8", errors="ignore")
    model = None
    flags: set[str] = set()
    for line in text.splitlines():
        if line.startswith("model name") and model is None:
            model = line.split(":", 1)[1].strip()
        if line.startswith("flags") or line.startswith("Features"):
            flags.update(line.split(":", 1)[1].strip().lower().split())
    return model, flags


def _read_windows_cpu_name() -> str | None:
    if platform.system().lower() != "windows":
        return None
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-CimInstance Win32_Processor | Select-Object -First 1 -ExpandProperty Name)",
    ]
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=5)
    except OSError:
        return None
    return result.stdout.strip() or None


def _optional_py_cpuinfo() -> tuple[str | None, set[str]]:
    try:
        import cpuinfo  # type: ignore
    except Exception:
        return None, set()
    try:
        info = cpuinfo.get_cpu_info()
    except Exception:
        return None, set()
    return info.get("brand_raw"), {str(flag).lower() for flag in info.get("flags", [])}


def detect_cpu() -> dict:
    linux_model, linux_flags = _read_linux_cpuinfo()
    cpuinfo_model, cpuinfo_flags = _optional_py_cpuinfo()
    flags = linux_flags | cpuinfo_flags
    model = cpuinfo_model or linux_model or _read_windows_cpu_name() or platform.processor() or "unknown"
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": model,
        "python": platform.python_version(),
        "flags_detected_count": len(flags),
        "feature_detection": {
            "avx2": "avx2" in flags,
            "avx512f": "avx512f" in flags,
            "avx512_bf16": "avx512_bf16" in flags or "avx512bf16" in flags,
            "avx512_vnni": "avx512_vnni" in flags or "avx512vnni" in flags,
            "amx_tile": "amx_tile" in flags or "amx-tile" in flags,
            "amx_int8": "amx_int8" in flags or "amx-int8" in flags,
            "amx_bf16": "amx_bf16" in flags or "amx-bf16" in flags,
        },
        "feature_notes": (
            "Windows often hides ISA flags from standard APIs. Install py-cpuinfo "
            "or rerun on Linux for richer AVX-512/AMX detection."
        ),
    }


def summarize(values: list[float]) -> dict:
    return {
        "count": len(values),
        "min_ms": round(min(values), 4) if values else 0.0,
        "mean_ms": round(statistics.fmean(values), 4) if values else 0.0,
        "p50_ms": round(_percentile(values, 0.50), 4),
        "p95_ms": round(_percentile(values, 0.95), 4),
        "max_ms": round(max(values), 4) if values else 0.0,
    }


def run_iterations(modes: Iterable[str], iterations: int, warmup: int) -> dict:
    os.environ.setdefault("WEAREDGE_VECTOR_BACKEND", "memory")
    samples = {mode: load_sample_request(mode) for mode in modes}

    for _ in range(warmup):
        for mode in modes:
            run_pipeline(samples[mode], mode=mode)

    all_latencies: list[float] = []
    route_latencies: dict[str, list[float]] = {mode: [] for mode in modes}
    started = time.perf_counter()
    for _ in range(iterations):
        for mode in modes:
            before = time.perf_counter()
            result = run_pipeline(samples[mode], mode=mode)
            elapsed_ms = (time.perf_counter() - before) * 1000
            route_latencies[mode].append(elapsed_ms)
            all_latencies.append(elapsed_ms)
            if not result.get("ok"):
                raise RuntimeError(f"pipeline failed for route {mode}")
    total_seconds = time.perf_counter() - started

    return {
        "iterations_per_route": iterations,
        "warmup_per_route": warmup,
        "total_calls": len(all_latencies),
        "total_seconds": round(total_seconds, 4),
        "calls_per_second": round(len(all_latencies) / total_seconds, 4) if total_seconds else 0.0,
        "overall": summarize(all_latencies),
        "routes": {mode: summarize(values) for mode, values in route_latencies.items()},
        "scorecard": build_scorecard(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=200)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument(
        "--output",
        default="evidence/benchmarks/intel_cpu_benchmark.local-smoke.json",
        help="Path for benchmark JSON output.",
    )
    args = parser.parse_args()

    modes = list(ROUTES)
    report = {
        "benchmark": "WearEdge OPEA Manufacturing five-agent CPU benchmark",
        "schema_version": "2026-05-26",
        "claim_status": "local_smoke_test_not_avx512_amx_claim",
        "cpu": detect_cpu(),
        "pipeline": run_iterations(modes, args.iterations, args.warmup),
        "competition_note": (
            "For Intel AVX-512/AMX bonus evidence, rerun this script on a Xeon host "
            "that advertises avx512f plus AMX flags, then attach the JSON and report."
        ),
    }

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
