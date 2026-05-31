# GCP C3 OPEA TEI Profile E2E Report

Captured: 2026-05-27 10:41 UTC

## Summary

The official OPEA TEI profile passed from a fresh clone on Google Cloud C3.

```text
docker-compose.yml + docker-compose.opea-tei.yml
```

Overall result:

```text
all_checks_pass=true
```

The runner created a temporary C3 VM, fresh-cloned the repository, started
Qdrant, Hugging Face TEI, the OPEA embedding microservice, and the WearEdge
Manufacturing Gateway, validated all five manufacturing routes, printed the JSON
artifact, and deleted the VM.

## Host

| Field | Value |
| --- | --- |
| Project | `gen-lang-client-0555254036` |
| Zone | `us-central1-a` |
| Machine type | `c3-standard-4` |
| Temporary VM | `wearedge-opea-tei-0527103938` |
| Cleanup | deleted |

## Component Path

```text
Manufacturing Gateway
  -> OPEA embedding microservice
  -> Hugging Face Text Embeddings Inference
  -> Qdrant
  -> five WearEdge manufacturing agents
  -> scorecard
```

| Component | Evidence |
| --- | --- |
| OPEA embedding service | `opea/embedding:latest` |
| TEI service | `ghcr.io/huggingface/text-embeddings-inference:cpu-latest` |
| Vector DB | `qdrant/qdrant:v1.12.6` |
| Embedding model | `BAAI/bge-base-en-v1.5` |
| Embedding dimensions | `768` |
| Compose project | `wearedge-opea-tei-fresh` |

## Validation

The Cloud Shell transcript reported:

```text
gateway_ok=true
qdrant_backend=true
gateway_embedding_backend_opea=true
gateway_embedding_url_is_opea_tei=true
embedding_health_endpoint_responds=true
embedding_endpoint_openai_shape=true
embedding_dimensions_768=true
all_samples_ok=true
all_rag_uses_opea_tei_marker=true
scorecard_ok=true
scorecard_routes_pass=true
```

All five routes reported the official TEI-backed Qdrant marker:

| Route | RAG vector store |
| --- | --- |
| `maintenance` | `qdrant-opea-tei-vector-store` |
| `iqc` | `qdrant-opea-tei-vector-store` |
| `changeover` | `qdrant-opea-tei-vector-store` |
| `wi` | `qdrant-opea-tei-vector-store` |
| `hazard` | `qdrant-opea-tei-vector-store` |

Visible route examples in the transcript:

| Route | Target | Latency |
| --- | --- | --- |
| `wi` | `wi_reference` | 184.06 ms |
| `hazard` | `ehs_case` | 212.98 ms |

## Resource Snapshot

| Container | CPU | Memory |
| --- | --- | --- |
| Manufacturing Gateway | 0.05% | 36.37 MiB / 15.61 GiB |
| OPEA embedding wrapper | 0.05% | 93.68 MiB / 15.61 GiB |
| Qdrant | 0.05% | 56.07 MiB / 15.61 GiB |
| TEI | 0.07% | 855.6 MiB / 15.61 GiB |

## Evidence

```text
scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh
evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json
```

## Claim Boundary

This run validates the official OPEA TEI embedding component path on Google
Cloud C3. It does not claim production LLM acceleration. The evidence was
recorded from the user-provided Cloud Shell transcript, which showed
`all_checks_pass=true` and successful deletion of the temporary VM.
