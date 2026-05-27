# GCP C3 Docker / Qdrant Fresh-Clone E2E Report

Status: passed on Google Cloud C3.

## Objective

This run validates the challenge-facing product package rather than only the
dependency-free benchmark harness. The test creates a temporary GCP C3 VM,
fresh-clones the public GitHub repository, starts Docker Compose, brings up
Qdrant plus the Manufacturing Gateway, and verifies the five-agent API surface.

This is the strongest current hardware/runtime evidence for the submitted
product shape:

```text
fresh clone -> docker compose -> Qdrant -> Gateway -> Megaservice -> RAG -> evaluator -> guardrails -> action cards
```

## Run Identity

| Field | Value |
| --- | --- |
| Project | `gen-lang-client-0555254036` |
| Machine type | `c3-standard-4` |
| Zone | `us-central1-a` |
| VM name | `wearedge-docker-e2e-0527082214` |
| Cleanup | VM deleted after run |
| Summary artifact | `evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json` |
| Runner | `scripts/gcp_c3_docker_qdrant_e2e_cloudshell.sh` |

## Validation Result

All checks passed:

| Check | Result |
| --- | --- |
| `/demo` HTTP 200 | pass |
| `/healthz` ok | pass |
| Qdrant backend reported | pass |
| Qdrant endpoint responded | pass |
| Five agents registered | pass |
| All five demo endpoints ok | pass |
| All five infer endpoints ok | pass |
| Demo action targets correct | pass |
| Infer action targets correct | pass |
| Scorecard ok | pass |
| Scorecard has five routes | pass |
| Scorecard routes pass | pass |
| Docker stats captured | pass |

## Endpoint Latency

Each endpoint was sampled 30 times from inside the VM against
`http://127.0.0.1:8088`.

| Endpoint | p50 | p95 | Mean |
| --- | ---: | ---: | ---: |
| `GET /healthz` | 0.9072 ms | 1.6402 ms | 1.7362 ms |
| `GET /v1/agents` | 1.1411 ms | 1.2557 ms | 1.1499 ms |
| `GET /v1/scorecard` | 21.5195 ms | 23.0418 ms | 21.4063 ms |
| `GET /v1/agents/maintenance/demo` | 4.9185 ms | 5.8133 ms | 5.2314 ms |
| `GET /v1/agents/iqc/demo` | 4.8850 ms | 5.6839 ms | 5.2031 ms |
| `GET /v1/agents/changeover/demo` | 4.7706 ms | 5.7552 ms | 5.0532 ms |
| `GET /v1/agents/wi/demo` | 4.8481 ms | 5.9601 ms | 5.1655 ms |
| `GET /v1/agents/hazard/demo` | 4.8374 ms | 5.8232 ms | 5.1855 ms |
| `POST /v1/agents/maintenance/infer` | 5.0734 ms | 6.4216 ms | 5.3537 ms |
| `POST /v1/agents/iqc/infer` | 4.9159 ms | 6.2449 ms | 5.0849 ms |
| `POST /v1/agents/changeover/infer` | 4.8640 ms | 5.7111 ms | 5.0675 ms |
| `POST /v1/agents/wi/infer` | 4.9049 ms | 5.9895 ms | 5.1316 ms |
| `POST /v1/agents/hazard/infer` | 4.9588 ms | 5.7732 ms | 5.0523 ms |

## What This Proves

- The public submission repository can be cloned fresh on cloud hardware.
- `docker compose up --build -d` starts the judge-facing package.
- The running profile uses Qdrant as the vector backend.
- All five Manufacturing agents run through the same Gateway and Megaservice.
- RAG source evidence, action-card contracts, guardrails, and integration
  targets are returned by both demo and infer endpoints.
- The scorecard passes across all five routes.

## Claim Boundary

This run measures the deterministic WearEdge OPEA demo path with Qdrant. It is
valid evidence for Docker/Qdrant reproducibility and endpoint latency. It should
not be described as production LLM acceleration or production embedding
acceleration. The API-reported vector store is `qdrant-hashing-vector-store`,
so the next OPEA hardening step is to add an official OPEA/GenAIComps-compatible
embedding or LLM microservice profile.

## Recommended Submission Language

```text
WearEdge OPEA Manufacturing was fresh-cloned and run on Google Cloud C3
`c3-standard-4` with Docker Compose. The run started Qdrant plus the
Manufacturing Gateway, verified `/demo`, `/healthz`, `/v1/agents`,
five `/demo` routes, five `/infer` routes, and `/v1/scorecard`, and all
validation checks passed. The five agent infer endpoints reported p95 latency
between 5.7111 ms and 6.4216 ms in the deterministic Qdrant demo profile.
```
