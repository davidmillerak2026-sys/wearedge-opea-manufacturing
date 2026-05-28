# OPEA Native Depth Matrix

Date: 2026-05-28

This matrix records how WearEdge follows the spirit of OPEA rather than merely
adding OPEA names to a demo. It is based on the public OPEA/GenAIExamples
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

| OPEA pattern | WearEdge implementation | Runtime proof | Submission stance |
| --- | --- | --- | --- |
| Example application built from microservice boundaries | Gateway, Manufacturing Megaservice, OPEA embedding service, Qdrant, TEI, route evaluators | `docker-compose.yml`, `docker-compose.opea.yml`, `docker-compose.opea-tei.yml` | Strong |
| Gateway / user-facing API | FastAPI gateway with `/demo`, `/healthz`, `/v1/agents`, `/v1/scorecard` | `src/wear_edge_opea/gateway.py` | Strong |
| Megaservice orchestration | Single megaservice routes five agent modes through the same pipeline | `src/wear_edge_opea/megaservice.py` | Strong |
| Dataprep | Route KB loaders normalize maintenance, IQC, changeover, WI, and EHS sources | `src/wear_edge_opea/dataprep.py`, `data/` | Strong |
| Retriever/RAG | Route-isolated RAG over per-agent KB collections | `src/wear_edge_opea/retriever.py`, `src/wear_edge_opea/vector_store.py` | Strong |
| Vector DB | Qdrant profile with idempotent collection creation and in-memory fallback | `docker-compose.yml`, tests | Strong |
| Official TEI embedding path | Hugging Face TEI -> `opea/embedding:latest` -> `/v1/embeddings` -> Gateway -> Qdrant | `docker-compose.opea-tei.yml`, local and GCP C3 reports | Very strong |
| LLM service | Deterministic default plus OpenAI/OPEA-compatible LLM adapter and benchmark harness | `src/wear_edge_opea/llm_adapter.py`, `scripts/llm_adapter_benchmark.py` | Adapter-ready; production endpoint evidence optional |
| Guardrails | Route-specific blocked claims, human confirmation, and integration target controls | `src/wear_edge_opea/guardrails.py` | Strong |
| Evaluation | Five-route scorecard plus lightweight GenAIEval-compatible dataset, runner, metrics, benchmark JSON, and summary | `src/wear_edge_opea/scorecard.py`, `/v1/scorecard`, `evals/genaieval/`, `evidence/genaieval/` | Strong |
| Docker Compose | One-command base profile plus official OPEA TEI profile | README run commands, C3 fresh-clone evidence | Strong |
| Helm/GMC | Not implemented in this submission package | Documented as follow-up in upstream blueprint | Do not claim |
| Upstream example | GenAIExamples first PR opened from the prepared `docs/opea-upstream/pr-ready/` package | Smoke-tested local package, public RFC issue, and upstream PR #2462 | Strong, but weaker than merged PR |

## Why This Is OPEA-Native Enough For The Challenge

The project adopts OPEA's enterprise application shape:

- microservice boundaries instead of one monolithic script;
- official OPEA TEI embedding component path;
- a vector database-backed RAG profile;
- a megaservice that composes route-specific services;
- a GenAIEval-compatible evaluation artifact set for 15 route cases;
- an API and Docker Compose profile that can be evaluated from a fresh clone;
- an opened GenAIExamples PR for upstream discussion.

The deliberately conservative boundary is LLM serving. The default submission
does not download or require a large model, so judges can evaluate it quickly.
The production LLM adapter and benchmark harness are included so the same
pipeline can be rerun against a real OpenAI/OPEA-compatible endpoint without
changing the route logic.

## Remaining OPEA Depth Options

The current implementation is strong because it includes the official OPEA TEI
embedding profile and a real upstream PR. If additional hardening time is
available, prioritize:

| Option | Why it helps | Risk |
| --- | --- | --- |
| Keep PR #2462 green and answer maintainer review | Converts OPEA alignment into public OPEA collaboration | Depends on upstream timing |
| Add a final PR/issue comment linking official TEI, GCP C3, article, and video evidence | Makes bonus evidence easy for OPEA reviewers to see | Low |
| Add optional Kubernetes/Helm/GMC notes | Supports OPEA cloud-native deployment narrative | Medium; may distract from Docker one-click path |
| Add more official GenAIComps services | Deepens OPEA-native component count | Medium; could destabilize a working submission if rushed |
| Run a real production LLM endpoint benchmark | Strengthens the LLM service claim | Requires model endpoint and strict no-fallback proof |

Champion recommendation: protect the current runnable official TEI profile first.
Do not add a heavier OPEA integration unless it can pass fresh-clone validation
without weakening the one-click judge experience.
