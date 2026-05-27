# Local OPEA TEI Profile E2E Report

Captured: 2026-05-27 18:16 +08:00

## Summary

The official OPEA TEI profile passed locally through Docker Desktop:

```text
docker-compose.yml + docker-compose.opea-tei.yml
```

Validated path:

```text
Manufacturing Gateway
  -> OPEA embedding microservice
  -> Hugging Face Text Embeddings Inference
  -> Qdrant
  -> five WearEdge manufacturing agents
  -> scorecard
```

## Components

| Component | Evidence |
| --- | --- |
| OPEA embedding microservice | `opea/embedding:latest` |
| OPEA health endpoint | `/v1/health_check` returned `opea_service@embedding`, version `1.5` |
| TEI service | `ghcr.io/huggingface/text-embeddings-inference:cpu-latest` |
| Embedding model | `BAAI/bge-base-en-v1.5` |
| Embedding response | OpenAI-compatible `data[0].embedding` |
| Embedding dimensions | `768` |
| Vector DB | `qdrant/qdrant:v1.12.6` |
| Gateway embedding backend | `opea` |
| Gateway embedding URL | `http://opea-embedding-tei:6000/v1/embeddings` |

## Route Results

| Route | Demo status | RAG vector store | Integration target | Demo latency |
| --- | --- | --- | --- | --- |
| `maintenance` | pass | `qdrant-opea-tei-vector-store` | `maintenance_work_order` | 727.29 ms |
| `iqc` | pass | `qdrant-opea-tei-vector-store` | `qms_quality_event` | 489.71 ms |
| `changeover` | pass | `qdrant-opea-tei-vector-store` | `changeover_checklist` | 427.15 ms |
| `wi` | pass | `qdrant-opea-tei-vector-store` | `wi_reference` | 413.43 ms |
| `hazard` | pass | `qdrant-opea-tei-vector-store` | `ehs_case` | 562.94 ms |

Scorecard: pass for all five routes.

## Resource Snapshot

| Container | CPU | Memory |
| --- | --- | --- |
| Manufacturing Gateway | 0.15% | 36.54 MiB / 27.4 GiB |
| OPEA embedding wrapper | 0.18% | 94.66 MiB / 27.4 GiB |
| Qdrant | 0.53% | 200.9 MiB / 27.4 GiB |
| TEI | 0.37% | 966.1 MiB / 27.4 GiB |

## Claim Boundary

This is local evidence for the official OPEA TEI component path. The next
competition-grade evidence step is a Google Cloud C3 fresh-clone rerun using:

```text
scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh
```

After that C3 run passes and its JSON artifact is committed, we can claim
official OPEA TEI embedding evidence on the same Xeon-class cloud family used
for the AVX-512/AMX benchmark.
