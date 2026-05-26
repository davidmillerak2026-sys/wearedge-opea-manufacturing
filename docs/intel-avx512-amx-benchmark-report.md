# Intel AVX-512 / AMX Benchmark Report

Status: benchmark harness implemented; local smoke test captured; Xeon AVX-512/AMX run pending.

## Objective

The OPEA challenge gives bonus credit for demonstrating Intel AVX-512/AMX optimization. WearEdge OPEA Manufacturing now includes a repeatable benchmark harness that measures the five-agent route pipeline and records CPU feature detection.

## Benchmark Command

```bash
python scripts/intel_cpu_benchmark.py --iterations 200 --output evidence/benchmarks/intel_cpu_benchmark.local-smoke.json
```

The script is dependency-free and defaults to the in-memory vector profile so it can run on a fresh clone. It records:

- Host CPU model and detected ISA flags.
- Per-route latency for `maintenance`, `iqc`, `changeover`, `wi`, and `hazard`.
- Overall calls/second.
- Scorecard status for contract, guardrail, RAG/source match, action target correctness, and route isolation.

## Local Smoke Test

Local machine:

```text
Intel(R) Core(TM) Ultra 9 185H
16 physical cores / 22 logical processors
```

Current local result file:

```text
evidence/benchmarks/intel_cpu_benchmark.local-smoke.json
```

This local machine is useful for smoke testing the benchmark and proving repeatability, but it is not sufficient for an AVX-512/AMX bonus claim unless the feature detector reports the relevant flags.

## Required Xeon Bonus Run

Run the same command on an Intel Xeon system that exposes AVX-512 and AMX, preferably Linux so `/proc/cpuinfo` exposes ISA flags:

```bash
git clone https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
cd wearedge-opea-manufacturing
python scripts/intel_cpu_benchmark.py --iterations 1000 --output evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json
```

For a strong bonus submission, attach:

- CPU model and core count.
- `avx512f=true`.
- At least one AMX flag such as `amx_tile`, `amx_int8`, or `amx_bf16`.
- Route-level p50 and p95 latency.
- Scorecard `ok=true`.
- A short note describing whether the run used OPEA Qdrant profile or dependency-free memory profile.

## Claim Language

Use this language after a Xeon run is captured:

```text
WearEdge OPEA Manufacturing includes an Intel CPU benchmark harness and was profiled on an Intel Xeon host with AVX-512/AMX feature flags detected. The five-agent route suite passed the scorecard while reporting per-route latency and throughput.
```

Do not claim production LLM acceleration unless a real embedding/LLM service path is benchmarked on the same host.
