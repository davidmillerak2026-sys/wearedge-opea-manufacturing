# OPEA Native Depth Matrix

Date: 2026-06-05

This matrix records how WearEdge follows the spirit of OPEA rather than merely
adding OPEA names to a thin prototype. It is based on the public OPEA/GenAIExamples
patterns for microservice-based applications, Docker Compose deployment,
Kubernetes Helm/GMC deployment options, and GenAIComps services such as
embedding, retriever, reranking, and LLM.

Relevant references:

```text
https://github.com/opea-project/GenAIExamples
https://github.com/opea-project/GenAIComps
https://github.com/opea-project/GenAIEval
https://opea-project.github.io/latest/GenAIComps/comps/embeddings/src/README_tei.html
https://github.com/opea-project/GenAIInfra/tree/main/microservices-connector
```

## Component Alignment

| OPEA pattern | WearEdge implementation | Runtime proof | Project stance |
| --- | --- | --- | --- |
| Example application built from microservice boundaries | Gateway, Manufacturing Megaservice, OPEA embedding service, Qdrant, TEI, optional reranker, route evaluators | `docker-compose.yml`, `docker-compose.opea.yml`, `docker-compose.opea-tei.yml`, `docker-compose.reranker.yml` | Strong |
| Gateway / user-facing API | FastAPI gateway with `/demo`, `/healthz`, `/v1/agents`, `/v1/scorecard` | `src/wear_edge_opea/gateway.py` | Strong |
| Megaservice orchestration | Single megaservice routes five agent modes through the same pipeline | `src/wear_edge_opea/megaservice.py` | Strong |
| Dataprep | Route KB loaders normalize maintenance, IQC, changeover, WI, and EHS sources | `src/wear_edge_opea/dataprep.py`, `data/` | Strong |
| Retriever/RAG | Route-isolated RAG over per-agent KB collections | `src/wear_edge_opea/retriever.py`, `src/wear_edge_opea/vector_store.py` | Strong |
| Re-ranker | Optional in-process reranker plus `/v1/rerank` microservice profile after vector retrieval | `src/wear_edge_opea/reranker.py`, `src/wear_edge_opea/reranker_service.py`, `docker-compose.reranker.yml`, `docs/opea-reranker-profile.md` | Strong optional profile |
| Vector DB | Qdrant profile with idempotent collection creation and in-memory fallback | `docker-compose.yml`, tests | Strong |
| Official TEI embedding path | Hugging Face TEI -> `opea/embedding:latest` -> `/v1/embeddings` -> Gateway -> Qdrant | `docker-compose.opea-tei.yml`, local and GCP C3 reports | Very strong |
| LLM service | Deterministic default plus OpenAI/OPEA-compatible and Ollama local LLM adapter, with strict local Gemma and DeepSeek endpoint evidence | `src/wear_edge_opea/llm_adapter.py`, `scripts/llm_adapter_benchmark.py`, `docs/local-gemma-llm-benchmark.md`, `docs/production-llm-benchmark-path.md`, `evidence/benchmarks/llm_adapter.local-gemma.json`, `evidence/benchmarks/llm_adapter.deepseek.json` | Strong; local and cloud endpoint evidence captured |
| Guardrails | Route-specific blocked claims, human confirmation, and integration target controls | `src/wear_edge_opea/guardrails.py` | Strong |
| Evaluation | Five-route scorecard plus GenAIEval-compatible dataset, local route benchmark, official GenAIEval chatqnafixed benchmark path, and captured official run summary | `src/wear_edge_opea/scorecard.py`, `/v1/scorecard`, `/v1/chatqna`, `evals/genaieval/`, `evidence/genaieval/`, `docs/official-genaieval-benchmark.md`, `evidence/genaieval/official_benchmark_summary.json` | Strong; official local GenAIEval run captured |
| Docker Compose | One-command base profile plus official OPEA TEI profile | README run commands, C3 fresh-clone evidence | Strong |
| Kubernetes optional profile | Minimal manifest for Qdrant, reranker, and Manufacturing Gateway | `deploy/kubernetes/wearedge-opea-manufacturing.yaml`, `docs/kubernetes-optional-profile.md` | Optional; do not claim Helm/GMC production deployment |
| Upstream example | GenAIExamples first PR opened from the prepared `docs/opea-upstream/pr-ready/` package | Smoke-tested local package, public RFC issue, and upstream PR #2462 | Strong, but weaker than merged PR |
| OPEA docs contribution | Publications PR #395 proposes adding the WearEdge technical article to OPEA Publications / Blogs | `https://github.com/opea-project/docs/pull/395` | Strong, but not official publication until merged |

## Why This Is OPEA-Native Enough For Enterprise Use

The project adopts OPEA's enterprise application shape:

- microservice boundaries instead of one monolithic script;
- Gateway, Manufacturing Megaservice, Retriever/RAG, Vector DB, LLM adapter,
  Evaluator, and Guardrails are treated as modular product boundaries, not
  labels wrapped around one prompt;
- official OPEA TEI embedding component path;
- optional reranking stage and microservice profile;
- a vector database-backed RAG profile;
- a megaservice that composes route-specific services;
- a GenAIEval-compatible evaluation artifact set for 15 route cases, a
  300-call local benchmark, and an official GenAIEval chatqnafixed local run;
- strict local Gemma4:31B and cloud DeepSeek LLM endpoint benchmark evidence;
- an API and Docker Compose profile that can be evaluated from a fresh clone;
- an opened GenAIExamples PR for upstream discussion;
- an opened OPEA docs Publications PR for public knowledge sharing.

The deliberately conservative boundary is still the default model path. The
default project does not download or require a large model, so evaluators can
run it quickly. The LLM/LMM adapter and benchmark harnesses now also include
strict no-fallback evidence for local Ollama `gemma4:31b` and the remote
DeepSeek `deepseek-chat` OpenAI-compatible endpoint. This proves the same
pipeline can run with local or cloud model endpoints without changing route
logic, RAG source grounding, evaluators, guardrails, or action-card contracts.

## Remaining OPEA Depth Options

The current implementation is strong because it includes the official OPEA TEI
embedding profile, a real upstream GenAIExamples PR, and an OPEA docs
Publications PR. If additional hardening time is available, prioritize:

| Option | Why it helps | Risk |
| --- | --- | --- |
| Keep PR #2462 and docs PR #395 green/responded | Converts OPEA alignment into public OPEA collaboration | Depends on upstream timing |
| Add a final PR/issue comment linking official TEI, GCP C3, article, video, reranker, official GenAIEval, local Gemma, DeepSeek, and Kubernetes evidence | Makes public evidence easy for OPEA reviewers to see | Low |
| Add Helm/GMC on top of the Kubernetes manifest | Supports deeper OPEA cloud-native deployment narrative | Medium; may distract from Docker one-click path |
| Replace lightweight reranker with production reranking model service | Deepens OPEA-native component quality | Medium; could destabilize a working project if rushed |
| Keep local and cloud LLM endpoint benchmark evidence fresh | Strengthens the LLM service claim over time | Requires endpoint availability and strict no-fallback proof |

Out of current scope by decision: GraphRAG and fine-tuning/SFT/DPO/PPO. They
remain valid OPEA architecture concepts, but they are not required for this
Manufacturing RAG release path and would add cost and destabilization risk.

Product recommendation: protect the current runnable official TEI profile first.
Do not add a heavier OPEA integration unless it can pass fresh-clone validation
without weakening the one-click evaluation experience.
