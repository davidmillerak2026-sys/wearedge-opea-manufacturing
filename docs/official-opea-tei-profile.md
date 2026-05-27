# Official OPEA TEI Profile

Status: profile and benchmark runner added; local Docker Desktop E2E passed;
Google Cloud C3 fresh-clone E2E passed.

## Why This Exists

The lightweight `docker-compose.opea.yml` profile proves the microservice
boundary without model downloads. The stronger OPEA championship evidence is an
official TEI path:

```text
Manufacturing Gateway
  -> OPEA Embedding Microservice
  -> Hugging Face Text Embeddings Inference
  -> Qdrant
  -> five manufacturing agents and scorecard
```

This matches the OPEA GenAIComps TEI embedding pattern: run TEI, set
`TEI_EMBEDDING_ENDPOINT`, set
`EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`, and consume the embedding service
through `/v1/embeddings`.

Official references:

```text
https://opea-project.github.io/latest/GenAIComps/comps/embeddings/src/README_tei.html
https://github.com/opea-project/GenAIComps
https://github.com/opea-project/GenAIExamples
https://huggingface.co/docs/text-embeddings-inference/index
```

## Run

This profile downloads a production embedding model and is slower than the
deterministic profile. Use it when the goal is OPEA component proof, not the
fastest judge smoke test.

```bash
docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml up -d
curl http://127.0.0.1:6000/v1/health_check
curl http://127.0.0.1:8088/healthz
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/scorecard
```

Default model:

```text
BAAI/bge-base-en-v1.5
```

Override it if the host needs a smaller model:

```bash
EMBEDDING_MODEL_ID=BAAI/bge-small-en-v1.5 \
docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml up -d
```

## Expected Markers

Gateway health:

```json
{
  "vector_backend": "qdrant",
  "embedding_backend": "opea",
  "embedding_url": "http://opea-embedding-tei:6000/v1/embeddings"
}
```

RAG vector-store marker:

```text
qdrant-opea-tei-vector-store
```

The profile also sets:

```text
WEAREDGE_EMBEDDING_DIMENSIONS=768
WEAREDGE_EMBEDDING_STRICT_DIMENSIONS=true
WEAREDGE_EMBEDDING_SEND_DIMENSIONS=false
```

That means the run fails if the OPEA/TEI service does not return the expected
production embedding dimension. This is intentional; it prevents us from
silently padding or truncating official benchmark evidence.

## Google Cloud C3 Rerun

```bash
export PROJECT_ID=gen-lang-client-0555254036
export ZONE=us-central1-a
curl -fsSL https://raw.githubusercontent.com/davidmillerak2026-sys/wearedge-opea-manufacturing/main/scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh \
  -o gcp_c3_opea_tei_profile_e2e_cloudshell.sh
bash gcp_c3_opea_tei_profile_e2e_cloudshell.sh
```

The runner creates a temporary billable C3 VM, fresh-clones this repository,
starts `docker-compose.yml + docker-compose.opea-tei.yml`, validates the OPEA
embedding service, verifies all five agent routes and `/v1/scorecard`, records
Docker stats, prints JSON evidence, and deletes the VM unless `KEEP_VM=1`.

After the run, copy the printed JSON artifact into a local file and generate the
submission summary/report with:

```bash
python scripts/record_gcp_opea_tei_evidence.py gcp_c3_opea_tei_profile_e2e.json
```

## Local Validation

Local Docker Desktop validation passed:

| Check | Result |
| --- | --- |
| OPEA embedding image | `opea/embedding:latest` |
| TEI image | `ghcr.io/huggingface/text-embeddings-inference:cpu-latest` |
| OPEA health endpoint | pass |
| `/v1/embeddings` response | OpenAI-compatible shape |
| Embedding dimensions | `768` |
| Gateway embedding backend | `opea` |
| Five `/demo` routes | pass |
| `/v1/scorecard` | pass |
| RAG vector store marker | `qdrant-opea-tei-vector-store` |

Evidence:

```text
docs/local-opea-tei-profile-e2e-report.md
evidence/benchmarks/local_opea_tei_profile_e2e.summary.json
docs/gcp-c3-opea-tei-profile-e2e-report.md
evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json
```

## Claim Boundary

The C3 rerun passed, so we can claim:

```text
WearEdge OPEA Manufacturing was fresh-clone validated on Google Cloud C3 with
Qdrant, the OPEA TEI embedding microservice path, five route demos, and the
five-agent scorecard.
```

Do not claim production LLM acceleration from this profile. It validates the
embedding/RAG component path; the LLM service remains adapter-ready and
deterministic in the submitted demo unless a separate production LLM profile is
added and benchmarked.
