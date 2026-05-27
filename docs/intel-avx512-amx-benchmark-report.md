# Intel AVX-512 / AMX Benchmark Report

Status: benchmark harness implemented; local smoke test captured; Google Cloud C3 Xeon AVX-512/AMX run captured.

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

## Captured Xeon Bonus Run

Cloud machine:

```text
Google Cloud C3 `c3-standard-4`, us-central1-a, 4 vCPU, 16 GiB RAM
Intel(R) Xeon(R) Platinum 8481C CPU @ 2.70GHz
Linux 6.17.0-1016-gcp, Python 3.12.3
```

Result file:

```text
evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json
```

Detected ISA evidence:

| Feature | Detected |
| --- | --- |
| `avx512f` | `true` |
| `avx512_bf16` | `true` |
| `avx512_vnni` | `true` |
| `amx_tile` | `true` |
| `amx_int8` | `true` |
| `amx_bf16` | `true` |

Five-agent deterministic route benchmark:

| Metric | Result |
| --- | --- |
| Total calls | 5,000 |
| Iterations per route | 1,000 |
| Calls/second | 4,581.4536 |
| Overall mean latency | 0.2179 ms |
| Overall p50 latency | 0.2111 ms |
| Overall p95 latency | 0.2748 ms |
| Scorecard | `ok=true` |

Route-level p95 latency:

| Route | p95 latency |
| --- | --- |
| `maintenance` | 0.2813 ms |
| `iqc` | 0.2232 ms |
| `changeover` | 0.1998 ms |
| `wi` | 0.2068 ms |
| `hazard` | 0.2306 ms |

The temporary VM was deleted after the run:

```text
wearedge-amx-bench-0527072816 in us-central1-a
```

## Reproducibility Command

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

```text
WearEdge OPEA Manufacturing includes an Intel CPU benchmark harness and was profiled on a Google Cloud C3 Intel Xeon Platinum 8481C host with AVX-512 and Intel AMX feature flags detected. The five-agent deterministic route suite passed the scorecard while reporting 4,581.4536 calls/second, 0.2111 ms p50 latency, and 0.2748 ms p95 latency across 5,000 route calls.
```

Do not claim production LLM acceleration unless a real embedding/LLM service path is benchmarked on the same host.

## Current Machine Search Result

The accepted cloud path used Google Cloud `c3-standard-4`. Azure `Standard_D4s_v6` and AWS `c7i.xlarge` remain valid rerun options if an additional provider comparison is needed.
