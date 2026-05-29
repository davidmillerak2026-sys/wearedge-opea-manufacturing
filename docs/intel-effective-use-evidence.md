# Intel Effective-Use Evidence

Status: application-level effective-use evidence captured; supplemental
TEI/oneDNN run captured; same-host oneDNN BF16/AMX probe dispatch markers were
captured. The TEI container logs themselves did not emit oneDNN dispatch
markers.

## What We Can Claim

WearEdge OPEA Manufacturing was run on Google Cloud C3 `c3-standard-4`, a
single-node Intel Xeon profile with 4 vCPU, 16 GiB RAM, and no GPU. The host
reported AVX-512 and AMX feature flags, and the same project package passed:

- deterministic five-agent route benchmark;
- Docker/Qdrant fresh-clone E2E;
- OPEA-compatible `/v1/embeddings` profile E2E;
- official OPEA TEI embedding profile E2E with Hugging Face TEI,
  `opea/embedding:latest`, Qdrant, and five route demos.
- supplemental TEI/oneDNN verbose capture on the same C3 profile, with Gateway,
  five demos, scorecard, Docker stats, CPU flags, and TEI logs captured.
- same-host oneDNN BF16/AMX probe on that C3 VM, with probe dispatch markers
  captured.

This is the right claim boundary for the competition bonus:

```text
WearEdge demonstrates effective application-level use of Intel Xeon hardware by
running its OPEA TEI embedding/RAG profile and five-agent Manufacturing route
suite on a single-node Google Cloud C3 Xeon host exposing AVX-512 and AMX
features, with route, embedding, Qdrant, scorecard, latency, memory, cleanup,
and same-host oneDNN BF16/AMX probe dispatch evidence recorded.
```

Do not claim that the TEI model server itself emitted AMX/AVX-512 oneDNN
dispatch markers. Do not claim production LLM acceleration. It is now valid to
claim same-host oneDNN BF16/AMX probe dispatch evidence, because the r23
artifact reports `probe_dispatch_markers_captured=true`.

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
| TEI/oneDNN verbose + probe capture | `evidence/benchmarks/gcp_c3_tei_onednn_verbose.summary.json` | Re-ran official TEI profile with verbose env enabled; Gateway, scorecard, five demos, Docker stats, AVX-512/AMX CPU flag checks, and TEI logs passed; TEI container dispatch marker grep returned zero lines; same-host oneDNN BF16/AMX probe executed and captured dispatch markers |

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
plus the supplemental TEI/oneDNN run and same-host probe into one competition-facing
artifact.

## Supplemental TEI/oneDNN Verbose Result

The supplemental run is recorded in:

```text
docs/gcp-c3-tei-onednn-verbose-report.md
evidence/benchmarks/gcp_c3_tei_onednn_verbose.summary.json
```

Result:

```text
all_checks_pass=true
c3_cpu_flags_include_avx512=true
c3_cpu_flags_include_amx=true
dispatch_markers_captured=false
onednn_probe_executed=true
probe_dispatch_markers_captured=true
```

This strengthens the hardware bonus by proving the official OPEA TEI + Qdrant
+ five-agent scorecard workload ran on the C3 profile while verbose capture was
enabled, and by proving same-host oneDNN BF16/AMX dispatch evidence. It still
must not be described as TEI-internal AMX dispatch proof, because the TEI logs
did not emit matching dispatch marker lines.

## Remaining Optional Upgrade

The current record is strong enough to defend full hardware bonus under the
rubric wording. To make the hardware story even harder to dispute, add one of
the following only if time and platform access allow:

- collect lower-level `perf` counters or a TEI build that emits oneDNN/DNNL
  dispatch lines;
- side-by-side latency comparison against a non-AMX CPU instance;
- production LLM endpoint benchmark on the same C3 host with strict fallback
  disabled.

## Resource Audit

| Resource | Current status | Best next use |
| --- | --- | --- |
| Google Cloud C3 `c3-standard-4` | Available and validated, including supplemental TEI/oneDNN verbose attempt plus same-host BF16/AMX probe dispatch evidence | Optional perf or non-AMX comparison only if more hardening is worth the cloud time |
| Local Docker Desktop | Available, but Docker Engine access may require local permission from Codex sandbox | Rerun official OPEA TEI profile and UI validation locally |
| GPU | Not required by challenge and not used in current proof | Do not introduce unless it clearly improves LMM benchmarking |
| Production LLM endpoint | Not currently configured in the public repo | Only benchmark if a real endpoint is available with strict fallback disabled |

Decision: the existing hardware package is full-mark defendable for the rubric
wording "effective use of Intel hardware features (AMX, AVX-512)." The only
remaining optional upgrade is TEI-specific instruction/backend dispatch
evidence or a non-AMX comparison, not another ordinary route benchmark.
