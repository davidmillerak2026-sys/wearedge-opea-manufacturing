# Intel Effective-Use Evidence

Status: application-level effective-use evidence captured; low-level kernel
dispatch evidence remains optional.

## What We Can Claim

WearEdge OPEA Manufacturing was run on Google Cloud C3 `c3-standard-4`, a
single-node Intel Xeon profile with 4 vCPU, 16 GiB RAM, and no GPU. The host
reported AVX-512 and AMX feature flags, and the same project package passed:

- deterministic five-agent route benchmark;
- Docker/Qdrant fresh-clone E2E;
- OPEA-compatible `/v1/embeddings` profile E2E;
- official OPEA TEI embedding profile E2E with Hugging Face TEI,
  `opea/embedding:latest`, Qdrant, and five route demos.

This is the right claim boundary for the competition bonus:

```text
WearEdge demonstrates effective application-level use of Intel Xeon hardware by
running its OPEA TEI embedding/RAG profile and five-agent Manufacturing route
suite on a single-node Google Cloud C3 Xeon host exposing AVX-512 and AMX
features, with route, embedding, Qdrant, scorecard, latency, memory, and cleanup
evidence recorded.
```

Do not claim that the benchmark proves TEI or oneDNN microkernels dispatched
AMX/AVX-512 instructions internally. Do not claim production LLM acceleration.

## Hardware

| Item | Value |
| --- | --- |
| Cloud | Google Cloud |
| Machine type | `c3-standard-4` |
| Zone | `us-central1-a` |
| CPU | Intel Xeon Platinum 8481C |
| vCPU | 4 |
| RAM | 16 GiB |
| GPU | none |
| Challenge fit | single node, <=64GB RAM, 4-core CPU profile |

Detected feature flags from `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json`:

| Feature | Detected |
| --- | --- |
| `avx512f` | true |
| `avx512_bf16` | true |
| `avx512_vnni` | true |
| `amx_tile` | true |
| `amx_int8` | true |
| `amx_bf16` | true |

## Workloads Validated

| Workload | Evidence | What passed |
| --- | --- | --- |
| Deterministic five-agent route benchmark | `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json` | 5,000 route calls, 4,581.4536 calls/sec, p50 0.2111 ms, p95 0.2748 ms, scorecard ok |
| Docker/Qdrant fresh-clone E2E | `evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json` | `/demo`, `/healthz`, five demo routes, five infer routes, Qdrant, `/v1/scorecard`, Docker stats |
| OPEA-compatible embedding profile | `evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json` | `/v1/embeddings`, Qdrant route collections, all five demos, scorecard routes pass |
| Official OPEA TEI profile | `evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json` | Hugging Face TEI, `opea/embedding:latest`, 768-dimensional embeddings, Qdrant TEI vector-store markers, five routes, scorecard pass |

## Official OPEA TEI Profile Runtime

The official TEI run used:

| Component | Value |
| --- | --- |
| OPEA embedding image | `opea/embedding:latest` |
| TEI image | `ghcr.io/huggingface/text-embeddings-inference:cpu-latest` |
| Qdrant image | `qdrant/qdrant:v1.12.6` |
| Embedding model | `BAAI/bge-base-en-v1.5` |
| Embedding dimensions | 768 |
| Compose profile | `docker-compose.yml + docker-compose.opea-tei.yml` |

Route markers showed all five routes using:

```text
qdrant-opea-tei-vector-store
```

Visible TEI route examples from the captured Cloud Shell transcript:

| Route | Integration target | Pipeline latency |
| --- | --- | ---: |
| `wi` | `wi_reference` | 184.06 ms |
| `hazard` | `ehs_case` | 212.98 ms |

Docker stats snapshot:

| Service | Memory |
| --- | ---: |
| Manufacturing Gateway | 36.37 MiB / 15.61 GiB |
| OPEA embedding TEI wrapper | 93.68 MiB / 15.61 GiB |
| Qdrant | 56.07 MiB / 15.61 GiB |
| Hugging Face TEI | 855.6 MiB / 15.61 GiB |

## Generated Summary

Run:

```powershell
python scripts\build_intel_effective_use_summary.py
```

Output:

```text
evidence/benchmarks/intel_effective_use.summary.json
```

The summary combines the CPU feature evidence, deterministic route benchmark,
Docker/Qdrant E2E, OPEA-compatible embedding E2E, and official OPEA TEI E2E
into one competition-facing artifact.

## Remaining Optional Upgrade

The current record is strong enough to show application-level effective use of
Intel Xeon hardware. To make the hardware bonus even harder to dispute, add one
of the following if time and platform access allow:

- TEI/oneDNN verbose log showing the backend kernel dispatch path;
- side-by-side latency comparison against a non-AMX CPU instance;
- production LLM endpoint benchmark on the same C3 host with strict fallback
  disabled.
