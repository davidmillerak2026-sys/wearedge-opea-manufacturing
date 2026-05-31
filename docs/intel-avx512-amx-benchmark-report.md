# Intel AVX-512 / AMX Benchmark Report

Status: benchmark harness implemented; local smoke test captured; Google Cloud C3 Xeon AVX-512/AMX run captured.

See also `docs/intel-effective-use-evidence.md` and
`evidence/benchmarks/intel_effective_use.summary.json`, which connect this CPU
feature benchmark to the Docker/Qdrant, OPEA-compatible embedding, and official
OPEA TEI workloads that ran on the C3 Xeon profile.

## Objective

The OPEA ecosystem gives evidence credit for demonstrating Intel AVX-512/AMX optimization. WearEdge OPEA Manufacturing now includes a repeatable benchmark harness that measures the five-agent route pipeline and records CPU feature detection.

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

This local machine is useful for smoke testing the benchmark and proving repeatability, but it is not sufficient for an AVX-512/AMX evidence claim unless the feature detector reports the relevant flags.

## Captured Xeon Evidence Run

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

## Complementary Docker / Qdrant E2E Run

A second Google Cloud C3 run validates the public Docker package
rather than only the dependency-free benchmark harness.

Result files:

```text
docs/gcp-c3-docker-qdrant-e2e-report.md
evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json
```

Captured run:

```text
Google Cloud C3 c3-standard-4, us-central1-a
Temporary VM: wearedge-docker-e2e-0527082214
Runtime: fresh clone -> docker compose -> Qdrant -> Manufacturing Gateway
Cleanup: VM deleted after run
```

All E2E checks passed: `/demo` HTTP 200, `/healthz` ok, Qdrant backend reported,
five agents registered, five sample endpoints ok, five infer endpoints ok, action
targets correct, `/v1/scorecard` ok, scorecard routes pass, and Docker stats
captured.

Endpoint p95 latency from the deterministic Qdrant profile:

| Endpoint group | p95 latency |
| --- | ---: |
| `GET /v1/scorecard` | 23.0418 ms |
| `POST /v1/agents/maintenance/infer` | 6.4216 ms |
| `POST /v1/agents/iqc/infer` | 6.2449 ms |
| `POST /v1/agents/changeover/infer` | 5.7111 ms |
| `POST /v1/agents/wi/infer` | 5.9895 ms |
| `POST /v1/agents/hazard/infer` | 5.7732 ms |

## Reproducibility Command

Run the same command on an Intel Xeon system that exposes AVX-512 and AMX, preferably Linux so `/proc/cpuinfo` exposes ISA flags:

```bash
git clone https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
cd wearedge-opea-manufacturing
python scripts/intel_cpu_benchmark.py --iterations 1000 --output evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json
```

For a strong evidence project, attach:

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

Also do not claim low-level TEI/oneDNN AMX or AVX-512 microkernel dispatch from
this artifact alone. The current evidence is application-level effective use of
an Intel Xeon C3 host exposing AVX-512 and AMX while running the WearEdge OPEA
route, Qdrant, embedding, and TEI workloads.

## Current Machine Search Result

The accepted cloud path used Google Cloud `c3-standard-4`. Azure `Standard_D4s_v6` and AWS `c7i.xlarge` remain valid rerun options if an additional provider comparison is needed.
