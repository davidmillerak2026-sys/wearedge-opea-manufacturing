# Champion Risk Burn-Down

Date: 2026-05-28

This document converts each known "why we might not win" concern into a
submission action, evidence artifact, and claim boundary. The target is not to
pretend every risk is gone; it is to make the project strong enough that a
judge can see a complete OPEA Manufacturing product instead of a single demo.

## Executive Position

WearEdge should be submitted as:

```text
An OPEA-aligned, Docker-runnable Manufacturing Agent Suite that demonstrates
how one Gateway + Megaservice + RAG + Qdrant + official OPEA TEI embedding path
can support five front-line manufacturing agents with guardrails and a
machine-verifiable scorecard plus GenAIEval-compatible route evidence.
```

Do not submit it as an Android app only, an M400-only prototype, or a generic
RAG chatbot.

## Risk Status

| Risk | Current mitigation | Evidence | Residual claim boundary |
| --- | --- | --- | --- |
| OPEA-native depth could be beaten by teams with more official microservices, Helm/GMC, or merged PRs | Official TEI profile is implemented and C3-validated; OPEA component matrix maps Gateway, Megaservice, Dataprep, Retriever/RAG, Embeddings, Vector DB, LLM adapter, Guardrails, and Evaluation; GenAIEval-compatible route evidence is included; upstream PR #2462 is open and CI-green | `docker-compose.opea-tei.yml`, `docs/official-opea-tei-profile.md`, `docs/opea-native-depth-matrix.md`, `docs/genaieval-compatible-evaluation.md`, `docs/opea-upstream/pr-ready/`, `docs/upstream-pr-attempt-2026-05-28.md`, `https://github.com/opea-project/GenAIExamples/pull/2462` | We can claim official OPEA TEI embedding path, lightweight GenAIEval-compatible evidence, and real CI-green upstream PR opened; do not claim Helm/GMC production deployment, full official GenAIEval/RAGAS/AutoRAG/LLM-as-judge execution, or merged upstream PR |
| Production LLM path had no complete benchmark | OpenAI/OPEA-compatible LLM adapter now exists in the runtime path; benchmark harness records endpoint usage, latency, fallback, and contract pass/fail | `src/wear_edge_opea/llm_adapter.py`, `scripts/llm_adapter_benchmark.py`, `evidence/benchmarks/llm_adapter_contract.local-smoke.json`, `docs/production-llm-benchmark-path.md` | Current committed JSON is an adapter contract smoke test unless a real endpoint is configured and `production_llm_endpoint_benchmarked` is recorded |
| Demo/video may not catch a fast-skimming judge | README, form guide, and demo console now put "five agents + OPEA TEI + Qdrant + scorecard" first; demo console shows LLM runtime and route evidence | `README.md`, `/demo`, `docs/final-submission-form-fill-guide.md`, `public/demo-video-script.md` | The strongest proof is engineering evidence; the video remains short and focused rather than cinematic |
| Manufacturing data is prototype/demo rather than broad enterprise dataset | Data provenance separates real M400/Jetson maintenance evidence from synthetic-but-realistic route samples; each route has released-source style KB and guardrails | `docs/data-provenance-and-field-validation.md`, `docs/source-project-map.md`, `data/maintenance_kb/`, `data/agent_kb/` | Do not claim customer deployment or large-scale proprietary plant data; claim runnable prototype with field-evidence lineage and route-specific controls |
| Upstream OPEA PR is CI-green but not merged | Public RFC and comments are posted; direct push was blocked by GitHub 403; fork push succeeded; upstream PR #2462 is open; DCO, pre-commit.ci, dependency-review, get-test-matrix, get-test-case, and compose-test passed; contribution patch is smoke-tested; minimal first-PR scope is documented for maintainers | `docs/opea-upstream/rfc-issue-draft.md`, `docs/opea-upstream/implementation-feedback-comment.md`, `docs/opea-upstream/tei-update-comment.md`, `docs/upstream-pr-attempt-2026-05-28.md`, `docs/opea-upstream/pr-ready/`, `https://github.com/opea-project/GenAIExamples/pull/2462` | This is stronger than prepared-package evidence but still weaker than a reviewed or merged upstream contribution |
| Challenge might favor telecom/network entries | Manufacturing is kept as the official vertical, but the story is positioned around enterprise edge operations, route isolation, and industrial reliability rather than narrow maintenance | `docs/telecom-scope-and-manufacturing-positioning.md`, `docs/submission-product-shape.md`, `docs/technical-report.draft.md` | Do not switch verticals; emphasize that manufacturing is a named enterprise scenario and the platform pattern is reusable for telecom operations |

## Champion-Ready Submission Lead

Use this in any short notes field:

```text
WearEdge Pro is not a single maintenance chatbot. It is a five-agent OPEA
Manufacturing suite with official OPEA TEI embeddings, Qdrant RAG, a unified
Gateway/Megaservice, guardrails, a scorecard, GenAIEval-compatible route
evaluation, C3 Xeon validation, upstream OPEA RFC/comment/open-PR evidence,
and a judge-facing Docker/Web/API product.
```

## Remaining Human Action

The one action that cannot be completed from this local environment is pressing
the authenticated challenge submission button. Use
`docs/final-submission-form-fill-guide.md` for the final paste values.
