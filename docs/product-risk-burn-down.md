# Product Risk Burn-Down

Date: 2026-05-28

This document converts each known "why we might not win" concern into a
project action, evidence artifact, and claim boundary. The target is not to
pretend every risk is gone; it is to make the project strong enough that a
evaluator can see a complete OPEA Manufacturing product instead of a single
scenario walkthrough.

## Executive Position

WearEdge should be released as:

```text
An OPEA-aligned, Docker-runnable Manufacturing Agent Suite that demonstrates
how one Gateway + Megaservice + RAG + Qdrant + official OPEA TEI embedding path
can support five front-line manufacturing agents with guardrails and a
machine-verifiable scorecard plus GenAIEval-compatible route evidence and an
official GenAIEval benchmark run.
```

Do not publish it as an Android app only, an M400-only artifact, or a generic
RAG chatbot.

## Risk Status

| Risk | Current mitigation | Evidence | Residual claim boundary |
| --- | --- | --- | --- |
| OPEA-native depth could be beaten by teams with more official microservices, Helm/GMC, or merged PRs | Official TEI profile is implemented and C3-validated; OPEA component matrix maps Gateway, Megaservice, Dataprep, Retriever/RAG, Embeddings, Vector DB, LLM adapter, Guardrails, and Evaluation; GenAIEval-compatible route evidence and an official GenAIEval `chatqnafixed` benchmark run are included; upstream PR #2462 is open with key check-run evidence | `docker-compose.opea-tei.yml`, `docs/official-opea-tei-profile.md`, `docs/opea-native-depth-matrix.md`, `docs/genaieval-compatible-evaluation.md`, `docs/official-genaieval-benchmark.md`, `evidence/genaieval/official_benchmark_summary.json`, `docs/opea-upstream/pr-ready/`, `docs/upstream-pr-attempt-2026-05-28.md`, `https://github.com/opea-project/GenAIExamples/pull/2462` | We can claim official OPEA TEI embedding path, lightweight GenAIEval-compatible evidence, an official local GenAIEval benchmark run, and a real upstream PR opened with key checks passing; do not claim Helm/GMC production deployment, RAGAS/AutoRAG/LLM-as-evaluator execution, merged upstream PR, or official acceptance |
| Production LLM path had no complete benchmark | OpenAI/OPEA-compatible LLM adapter now exists in the runtime path; benchmark harness records endpoint usage, latency, fallback, and contract pass/fail | `src/wear_edge_opea/llm_adapter.py`, `scripts/llm_adapter_benchmark.py`, `evidence/benchmarks/llm_adapter_contract.local-smoke.json`, `docs/production-llm-benchmark-path.md` | Current committed JSON is an adapter contract smoke test unless a real endpoint is configured and `production_llm_endpoint_benchmarked` is recorded |
| Product walkthrough may not catch a fast-skimming evaluator | README, form guide, and manufacturing console now put "five agents + OPEA TEI + Qdrant + scorecard" first; manufacturing console shows LLM runtime and route evidence | `README.md`, `/demo`, `docs/project-profile-fill-guide.md`, `public/product-walkthrough-script.md` | The strongest proof is engineering evidence; the video remains short and focused rather than cinematic |
| Knowledge-sharing evidence may be discounted if GitHub-only | Burned down: external Dev.to article and YouTube product walkthrough video are published; OPEA docs Publications PR #395 is open and mergeable to add the article to the official OPEA Publications / Blogs list | Dev.to article, YouTube walkthrough, `docs/publication-record.md`, `https://github.com/opea-project/docs/pull/395` | Do not claim official OPEA publication until PR #395 is merged |
| Hardware evidence may be discounted if only CPU flags are shown | Intel effective-use summary now ties C3 AVX-512/AMX feature detection to deterministic route benchmark, Docker/Qdrant E2E, OPEA-compatible embedding E2E, and official OPEA TEI E2E | `docs/intel-effective-use-evidence.md`, `evidence/benchmarks/intel_effective_use.summary.json`, `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json` | Claim application-level effective use on a C3 Xeon host; do not claim oneDNN/TEI microkernel dispatch proof |
| Manufacturing data may be perceived as evaluation-fixture-only rather than broad enterprise dataset | Data provenance separates real M400/Jetson maintenance evidence from transparent public-scale route fixtures; each route has released-source style KB and guardrails | `docs/data-provenance-and-field-validation.md`, `docs/source-project-map.md`, `data/maintenance_kb/`, `data/agent_kb/` | Do not claim customer deployment or large-scale proprietary plant data; claim a runnable industrial AI agent package with field-evidence lineage and route-specific controls |
| Upstream OPEA PR has key checks passing but is not merged | Public RFC and comments are posted; direct push was blocked by GitHub 403; fork push succeeded; upstream PR #2462 is open; DCO, dependency-review, get-test-matrix, get-test-case, and compose-test check runs pass on the current PR head; contribution patch is smoke-tested; minimal first-PR scope is documented for maintainers; docs PR #395 is open and mergeable | `docs/opea-upstream/rfc-issue-working-copy.md`, `docs/opea-upstream/implementation-feedback-comment.md`, `docs/opea-upstream/tei-update-comment.md`, `docs/upstream-pr-attempt-2026-05-28.md`, `docs/opea-upstream/pr-ready/`, `https://github.com/opea-project/GenAIExamples/pull/2462`, `https://github.com/opea-project/docs/pull/395` | This is stronger than prepared-package evidence but still weaker than reviewed or merged upstream contributions; legacy status contexts should be rechecked before saying the PR is fully green |
| Program reviewers might favor telecom/network entries | Manufacturing is kept as the official vertical, but the story is positioned around enterprise edge operations, route isolation, and industrial reliability rather than narrow maintenance | `docs/telecom-scope-and-manufacturing-positioning.md`, `docs/product-package.md`, `docs/technical-report-working-copy.md` | Do not switch verticals; emphasize that manufacturing is a named enterprise scenario and the platform pattern is reusable for telecom operations |

## Product-Ready Project Lead

Use this in any short notes field:

```text
WearEdge Pro is not a single maintenance chatbot. It is a five-agent OPEA
Manufacturing suite with official OPEA TEI embeddings, Qdrant RAG, a unified
Gateway/Megaservice, guardrails, a scorecard, GenAIEval-compatible route
evaluation, an official GenAIEval benchmark run, C3 Xeon validation, upstream
OPEA RFC/comment/open-PR evidence, and an evaluation-facing Docker/Web/API
product.
```

## Remaining Human Action

The one action that cannot be completed from this local environment is pressing
the authenticated public release button. Use
`docs/project-profile-fill-guide.md` for the final paste values.
