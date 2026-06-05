# Final Evidence Update Comment Draft

This is a concise update that can be posted to the OPEA RFC issue or related PR
thread when reviewer-facing evidence needs to be consolidated.

Project tracker copy posted:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2#issuecomment-4631635695
```

Direct posting to `opea-project/GenAIExamples#2462` was attempted from the
current GitHub integration, but GitHub returned `403 Resource not accessible by
integration`. Keep the draft below for reposting when write permission is
available.

```markdown
Final WearEdge OPEA Manufacturing evidence update:

This PR/RFC package now has a runnable five-agent Manufacturing sample with
clear OPEA claim boundaries.

What is implemented and evidenced:

- Official OPEA TEI embedding profile:
  - `docker-compose.opea-tei.yml`
  - local Docker Desktop E2E evidence
  - Google Cloud C3 fresh-clone E2E evidence
- Five-route Manufacturing RAG:
  - maintenance, IQC, changeover, WI, hazard
  - Qdrant-backed route collections with deterministic local fallback
- Optional reranker profile:
  - in-process reranking boundary
  - `/v1/rerank` microservice profile
  - `docker-compose.reranker.yml`
- LLM endpoint evidence:
  - deterministic default remains available for fast local evaluation
  - strict local Ollama `gemma4:31b` benchmark with `fallback_count=0`
  - strict DeepSeek `deepseek-chat` OpenAI-compatible benchmark with `fallback_count=0`
  - API key values are not stored in committed evidence
- Evaluation:
  - 15-case GenAIEval-compatible route dataset
  - 300-call local route benchmark
  - official OPEA GenAIEval `chatqnafixed` local benchmark summary with zero failures
- Deployment:
  - Docker Compose default profile
  - official OPEA TEI profile
  - optional Kubernetes manifest for Qdrant, reranker, and gateway
- Public evidence:
  - technical article and walkthrough assets
  - Intel/GCP C3 application-level evidence

Boundaries:

- This should not be described as an official OPEA-published example until the
  upstream PR is merged.
- The current release path intentionally does not include GraphRAG or
  fine-tuning/SFT/DPO/PPO.
- Kubernetes is provided as an optional manifest; Helm/GMC is future work.
- The reranker profile proves the component boundary, but it is not a heavy
  production reranking model service yet.
```
