# Official OPEA Profile

Status: lightweight profile validated; official TEI profile added separately.

## Why This Exists

The default `docker-compose.yml` profile is optimized for evaluator
reproducibility: Qdrant plus the Manufacturing Gateway, no model downloads, and
a deterministic embedding path.

For the OPEA ecosystem, the stronger story is not just that WearEdge has RAG.
It is that WearEdge can be assembled as OPEA-style microservices behind a
Gateway and Megaservice. OPEA's embedding service documentation exposes
`/v1/embeddings` and describes the API as OpenAI-compatible. This profile moves
WearEdge's embedding boundary out of the Gateway process and into a separate
OPEA-compatible embedding microservice.

For the production-model OPEA component path, see
[`docs/official-opea-tei-profile.md`](official-opea-tei-profile.md). That
profile wires the Gateway to OPEA's TEI embedding pattern through
`TEI_EMBEDDING_ENDPOINT`, `EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`, and
`/v1/embeddings`.

## Run

```bash
docker compose -f docker-compose.yml -f docker-compose.opea.yml up --build -d
curl http://127.0.0.1:6000/healthz
curl http://127.0.0.1:8088/healthz
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/scorecard
```

Google Cloud C3 rerun:

```bash
export PROJECT_ID=gen-lang-client-0555254036
export ZONE=us-central1-a
curl -fsSL https://raw.githubusercontent.com/davidmillerak2026-sys/wearedge-opea-manufacturing/main/scripts/gcp_c3_opea_profile_e2e_cloudshell.sh \
  -o gcp_c3_opea_profile_e2e_cloudshell.sh
bash gcp_c3_opea_profile_e2e_cloudshell.sh
```

Expected `/healthz` differences:

```json
{
  "vector_backend": "qdrant",
  "embedding_backend": "opea",
  "embedding_url": "http://opea-embedding:6000/v1/embeddings"
}
```

Expected RAG vector-store marker:

```text
qdrant-opea-compatible-embedding-vector-store
```

## Local Validation

Local Docker Desktop validation passed with:

| Check | Result |
| --- | --- |
| `opea-embedding` service | pass |
| `/v1/embeddings` vector length | 64 |
| Gateway `embedding_backend` | `opea` |
| Gateway `vector_backend` | `qdrant` |
| Five `/demo` routes | pass |
| Five `/infer` routes | pass |
| `/v1/scorecard` | pass |
| RAG vector store marker | `qdrant-opea-compatible-embedding-vector-store` |

Evidence:

```text
evidence/benchmarks/local_opea_profile_e2e.summary.json
```

## GCP C3 Validation

Google Cloud C3 fresh-clone validation also passed:

| Check | Result |
| --- | --- |
| `docker-compose.yml + docker-compose.opea.yml` | pass |
| `embedding_backend=opea` | pass |
| Embedding response compatibility | `OPEA/OpenAI-compatible /v1/embeddings` |
| Five `/demo` routes | pass |
| `/v1/scorecard` | pass |
| RAG vector store marker | `qdrant-opea-compatible-embedding-vector-store` |
| Temporary VM cleanup | pass |

Evidence:

```text
docs/gcp-c3-opea-profile-e2e-report.md
evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json
```

## Service Topology

```text
M400 / API evidence
  -> Manufacturing Gateway
  -> Manufacturing Megaservice
  -> Dataprep
  -> Retriever / RAG
  -> OPEA-compatible Embedding Microservice /v1/embeddings
  -> Qdrant Vector DB
  -> LLM adapter / deterministic explanation path
  -> Evaluator
  -> Guardrails
  -> Action Card
```

## What Changed

| Layer | Default profile | Official OPEA profile |
| --- | --- | --- |
| Embeddings | In-process deterministic hashing | Separate `/v1/embeddings` microservice |
| Vector DB | Qdrant | Qdrant |
| Gateway | FastAPI | FastAPI with `WEAREDGE_EMBEDDING_BACKEND=opea` |
| RAG evidence | Five route KBs | Same five route KBs, embedded through service boundary |
| LLM | Adapter-ready deterministic path | Same, pending production OPEA LLM profile |

## Claim Boundary

This is an OPEA-compatible embedding microservice profile. It uses the
OpenAI-compatible `/v1/embeddings` payload shape used by OPEA embedding
services while preserving deterministic local behavior for reproducibility. If
`opea-comps` is installed, the service also exposes an optional
`register_microservice` hook with `ServiceType.EMBEDDING`, `TextDoc`, and
`EmbedDoc`, matching the GenAIComps embedding microservice decorator pattern.

Optional local install for that hook:

```bash
pip install -e ".[opea]"
```

Do not claim that this profile runs a production embedding model. The next
hardening profile is now in `docker-compose.opea-tei.yml` and the matching
Google Cloud C3 runner is
`scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh`. Claim production TEI
evidence only after that fresh-clone runner passes.
