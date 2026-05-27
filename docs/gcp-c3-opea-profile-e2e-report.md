# GCP C3 OPEA-Compatible Profile E2E Report

Status: passed on Google Cloud C3.

## Objective

This run validates the OPEA-compatible profile, not only the default
Docker/Qdrant demo. It fresh-clones the public repository, starts:

```text
docker-compose.yml + docker-compose.opea.yml
```

and verifies the service topology:

```text
Manufacturing Gateway
  -> Manufacturing Megaservice
  -> Retriever / RAG
  -> OPEA-compatible Embedding Microservice /v1/embeddings
  -> Qdrant Vector DB
  -> Evaluator + Guardrails
  -> Five Manufacturing action cards
```

## Run Identity

| Field | Value |
| --- | --- |
| Project | `gen-lang-client-0555254036` |
| Machine type | `c3-standard-4` |
| Zone | `us-central1-a` |
| VM name | `wearedge-opea-profile-0527085558` |
| Cleanup | VM deleted after run |
| Summary artifact | `evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json` |
| Runner | `scripts/gcp_c3_opea_profile_e2e_cloudshell.sh` |

## Validation Result

All checks passed:

| Check | Result |
| --- | --- |
| Gateway ok | pass |
| Qdrant backend reported | pass |
| Gateway `embedding_backend=opea` | pass |
| Embedding service ok | pass |
| Embedding endpoint returns OpenAI-compatible shape | pass |
| Five demo routes ok | pass |
| Five routes use OPEA-compatible embedding marker | pass |
| `/v1/scorecard` ok | pass |
| Scorecard routes pass | pass |
| Temporary VM cleanup | pass |

The embedding response reported:

```text
opea_component = Embedding Microservice
compatibility = OPEA/OpenAI-compatible /v1/embeddings
```

## Scorecard

| Route | Status | Latency | Integration target |
| --- | --- | ---: | --- |
| `maintenance` | pass | 90.96 ms | `maintenance_work_order` |
| `iqc` | pass | 83.13 ms | `qms_quality_event` |
| `changeover` | pass | 95.67 ms | `changeover_checklist` |
| `wi` | pass | 85.08 ms | `wi_reference` |
| `hazard` | pass | 79.96 ms | `ehs_case` |

All five RAG paths reported:

```text
qdrant-opea-compatible-embedding-vector-store
```

## Resource Snapshot

| Service | CPU | Memory |
| --- | ---: | ---: |
| `manufacturing-gateway` | 0.04% | 35.95MiB / 15.61GiB |
| `qdrant` | 0.03% | 55.33MiB / 15.61GiB |
| `opea-embedding` | 0.06% | 35.47MiB / 15.61GiB |

## What This Proves

- The public repo can be fresh-cloned on cloud hardware.
- The optional OPEA-compatible profile starts as three services.
- The Gateway actually calls an embedding microservice boundary instead of
  only using in-process embeddings.
- Qdrant RAG runs with the `qdrant-opea-compatible-embedding-vector-store`
  marker across all five Manufacturing agents.
- The scorecard passes after the OPEA-compatible profile is enabled.

## Claim Boundary

This proves an OPEA-compatible `/v1/embeddings` service boundary and a
fresh-clone C3 E2E run. It does not claim production TEI embedding quality or
production LLM acceleration. The next hardening step is to swap the deterministic
embedding service for official TEI/GenAIComps and rerun the same benchmark.
