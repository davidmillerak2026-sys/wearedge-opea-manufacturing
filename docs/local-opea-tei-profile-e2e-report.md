# Local OPEA TEI Profile E2E Report

Captured: 2026-05-28 16:45 +08:00

## Summary

The official OPEA TEI profile passed locally through Docker Desktop after a
fresh Gateway rebuild/recreate:

```text
docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml up -d --build
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
| Browser console | `/demo` returned HTTP 200, 16246 bytes |

## Route Results

| Route | Demo status | RAG vector store | Integration target | Demo latency |
| --- | --- | --- | --- | --- |
| `maintenance` | pass | `qdrant-opea-tei-vector-store` | `maintenance_work_order` | 706.66 ms |
| `iqc` | pass | `qdrant-opea-tei-vector-store` | `qms_quality_event` | 423.15 ms |
| `changeover` | pass | `qdrant-opea-tei-vector-store` | `changeover_checklist` | 287.71 ms |
| `wi` | pass | `qdrant-opea-tei-vector-store` | `wi_reference` | 387.12 ms |
| `hazard` | pass | `qdrant-opea-tei-vector-store` | `ehs_case` | 441.92 ms |

Scorecard: pass for all five routes.

## Infer Results

All five `POST /v1/agents/{mode}/infer` routes passed with the expected action
targets and `qdrant-opea-tei-vector-store` RAG marker.

| Route | Infer status | Integration target | Infer latency |
| --- | --- | --- | --- |
| `maintenance` | pass | `maintenance_work_order` | 537.12 ms |
| `iqc` | pass | `qms_quality_event` | 342.89 ms |
| `changeover` | pass | `changeover_checklist` | 279.86 ms |
| `wi` | pass | `wi_reference` | 237.74 ms |
| `hazard` | pass | `ehs_case` | 285.99 ms |

## HTTP Concurrency

The local Docker Gateway also passed an HTTP-level concurrency smoke test
against `GET /v1/agents/{mode}/demo`:

| Metric | Value |
| --- | --- |
| Workers | 8 |
| Total requests | 50 |
| Route coverage | 10 requests each for maintenance, IQC, changeover, WI, hazard |
| Result | all requests OK; all used `qdrant-opea-tei-vector-store` |
| Throughput | 4.4 requests/second |
| Latency mean / p50 / p95 | 1713.01 ms / 1590.57 ms / 2774.17 ms |

## Resource Snapshot

| Container | CPU | Memory |
| --- | --- | --- |
| Manufacturing Gateway | 0.15% | 36.14 MiB / 27.4 GiB |
| OPEA embedding wrapper | 0.17% | 92.09 MiB / 27.4 GiB |
| Qdrant | 1.63% | 215.2 MiB / 27.4 GiB |
| TEI | 0.39% | 967.9 MiB / 27.4 GiB |

## Claim Boundary

This is local Docker Desktop evidence for the official OPEA TEI component path.
It validates the evaluation-facing Gateway, Qdrant, OPEA embedding wrapper, TEI
embedding service, `/demo`, sample routes, infer routes, scorecard, and HTTP
concurrency. It does not claim certified plant control, oneDNN/TEI microkernel
dispatch proof, or production LLM acceleration.
