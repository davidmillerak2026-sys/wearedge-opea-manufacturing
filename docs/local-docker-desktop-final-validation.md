# Local Docker Desktop Final Validation

Date: 2026-05-28 Asia/Shanghai

Purpose: final local validation of the judge-facing Docker runtime before
challenge submission.

Result: pass.

## Running Profile

Docker Desktop was already running the WearEdge OPEA TEI profile on the standard
judge-facing ports:

| Container | Image | Port evidence |
| --- | --- | --- |
| `wearedge-opea-manufacturing-manufacturing-gateway-1` | `wearedge-opea-manufacturing-manufacturing-gateway` | `0.0.0.0:8088->8088/tcp` |
| `wearedge-opea-manufacturing-qdrant-1` | `qdrant/qdrant:v1.12.6` | `0.0.0.0:6333-6334->6333-6334/tcp` |
| `wearedge-opea-manufacturing-opea-embedding-tei-1` | `opea/embedding:latest` | `0.0.0.0:6000->6000/tcp` |
| `wearedge-opea-manufacturing-tei-embedding-serving-1` | `ghcr.io/huggingface/text-embeddings-inference:cpu-latest` | `0.0.0.0:8090->80/tcp` |

The containers were left running because they were already active before this
validation pass.

## API Validation

Base URL:

```text
http://127.0.0.1:8088
```

Embedding URL:

```text
http://127.0.0.1:6000
```

| Check | Result |
| --- | --- |
| `GET /healthz` | `ok=true`, `vector_backend=qdrant`, `embedding_backend=opea` |
| `GET /demo` | HTTP 200, HTML length 16042 |
| `GET /v1/agents` | `maintenance`, `iqc`, `changeover`, `wi`, `hazard` |
| Five `GET /v1/agents/{mode}/demo` routes | Pass |
| Five `POST /v1/agents/{mode}/infer` routes | Pass |
| `GET /v1/scorecard` | `ok=true`, five routes, all `status=pass` |
| `GET /v1/health_check` on OPEA embedding service | Pass |
| `POST /v1/embeddings` on OPEA embedding service | OpenAI-compatible shape, 768 dimensions |

## Route Results

| Route | Demo target | Infer target | Vector store marker |
| --- | --- | --- | --- |
| `maintenance` | `maintenance_work_order` | `maintenance_work_order` | `qdrant-opea-tei-vector-store` |
| `iqc` | `qms_quality_event` | `qms_quality_event` | `qdrant-opea-tei-vector-store` |
| `changeover` | `changeover_checklist` | `changeover_checklist` | `qdrant-opea-tei-vector-store` |
| `wi` | `wi_reference` | `wi_reference` | `qdrant-opea-tei-vector-store` |
| `hazard` | `ehs_case` | `ehs_case` | `qdrant-opea-tei-vector-store` |

## OPEA Embedding Check

Request:

```text
POST http://127.0.0.1:6000/v1/embeddings
```

Result:

```json
{
  "object": "list",
  "data_count": 1,
  "first_object": "embedding",
  "dimensions": 768
}
```

## Docker Resource Snapshot

| Container | CPU | Memory | PIDs |
| --- | --- | --- | --- |
| `manufacturing-gateway` | `0.14%` | `36.01MiB / 27.4GiB` | `6` |
| `opea-embedding-tei` | `0.19%` | `92.08MiB / 27.4GiB` | `25` |
| `qdrant` | `0.59%` | `210.2MiB / 27.4GiB` | `109` |
| `tei-embedding-serving` | `0.39%` | `967MiB / 27.4GiB` | `67` |

## Verdict

The local Docker Desktop profile validates the final submission product shape:
browser demo console, API route registry, five route demos, five infer routes,
Qdrant-backed RAG, official OPEA TEI embedding path, and five-route scorecard.
