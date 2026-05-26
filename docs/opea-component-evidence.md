# OPEA Component Evidence

This document translates WearEdge Pro into the OPEA architecture expected by the challenge judges. The goal is to make the OPEA connection concrete while avoiding unsupported claims.

## Official OPEA References

| Reference | URL | How this submission uses it |
| --- | --- | --- |
| OPEA overview | https://opea-project.github.io/latest/introduction/index.html | Gateway, microservice, and megaservice architecture alignment |
| GenAI microservices | https://opea-project.github.io/latest/microservices/index.html | Microservice categories for LLM, RAG, guardrails, and orchestration |
| GenAIComps | https://github.com/opea-project/GenAIComps | Composable component reference |
| GenAIExamples | https://github.com/opea-project/GenAIExamples | Example application and deployment reference |

## Architecture

```mermaid
flowchart LR
    M400["Vuzix M400<br/>first-person evidence"] --> GW["Gateway"]
    GW --> MEGA["Manufacturing Megaservice"]
    MEGA --> DATA["Dataprep"]
    MEGA --> RET["Retriever / RAG"]
    MEGA --> PROMPT["Prompt Contract"]
    MEGA --> LLM["LLM Service"]
    MEGA --> EVAL["Deterministic Evaluator"]
    MEGA --> GUARD["Guardrails"]
    MEGA --> AUDIT["Audit / Runtime Stream"]
    GUARD --> ACTION["CMMS-ready Action Card"]
```

## Evidence Table

| OPEA layer | Status | WearEdge evidence | Claim |
| --- | --- | --- | --- |
| Gateway | Implemented in source | `jetson/app.py`, `scripts/run_fastapi.sh`, `docs/m400-inference-contract.md` | M400/Web/audit/session entry point |
| Megaservice | Implemented in source | `jetson/agently_orchestrator.py`, `jetson/agent_loop.py` | Manufacturing orchestration |
| Dataprep | Adapter-ready | `industrial-rag-agent/src/wear_edge_rag/documents.py` | SOP/log/quality-plan prep |
| Retriever / RAG | Implemented in source | `jetson/maintenance_kb.py`, `industrial-rag-agent/src/wear_edge_rag/retriever.py` | Machine-specific maintenance retrieval |
| LLM Service | Adapter-ready | `jetson/llama_client.py`, `scripts/run_llama_server.sh` | OpenAI-compatible edge LLM service |
| Prompt Contract | Implemented in source | `jetson/output_contract.py` | Bounded Manufacturing fields and action starters |
| Guardrails | Implemented in source | `jetson/agent_loop.py`, `jetson/released_source.py` | Source guard, uncertainty guard, human gate |
| Evaluation | Adapter-ready | `docs/edge-runtime-benchmark.md`, `docs/test-log-history.md` | Add GenAIEval-style scorecard next |
| Embeddings | Planned | Not committed | Do not claim yet |
| Vector DB | Planned | Not committed | Do not claim yet |

## Required OPEA Hardening

The current source project already contains an OPEA-shaped Manufacturing application. To make the challenge claim stronger, this standalone repository should add:

- `deploy.sh` or Docker Compose challenge profile.
- OPEA-compatible wrappers around gateway, retrieval, LLM service, and evaluator.
- Qdrant/Chroma/Milvus/Redis vector-store profile.
- GenAIEval-style scorecard with latency, throughput, RAG quality, and action-card correctness.
- OPEA blueprint feedback issue or PR link.

