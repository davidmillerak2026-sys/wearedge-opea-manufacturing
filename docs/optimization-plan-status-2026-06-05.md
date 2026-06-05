# Optimization Plan Status - 2026-06-05

This note records the current optimization state after the OPEA photo audit and
the decision to skip GraphRAG and fine-tuning for this release path.

## Confirmed Evidence

| Optimization area | Status | Evidence | Claim boundary |
| --- | --- | --- | --- |
| Official OPEA TEI embedding | Done | `docker-compose.opea-tei.yml`, `evidence/benchmarks/local_opea_tei_profile_e2e.summary.json`, `evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json` | Validates the official TEI embedding path, not production LLM acceleration |
| Local model endpoint | Done | `evidence/benchmarks/llm_adapter.local-gemma.json` | Ollama `gemma4:31b`, strict mode, five route calls, `fallback_count=0`, `all_contracts_pass=true`; local endpoint only |
| Cloud model endpoint | Done | `evidence/benchmarks/llm_adapter.deepseek.json` | DeepSeek `deepseek-chat`, strict mode, five route calls, `fallback_count=0`, `all_contracts_pass=true`; API key value is not stored |
| Official GenAIEval run | Done | `evidence/genaieval/official_benchmark_summary.json` | Official GenAIEval `chatqnafixed` benchmark ran locally with 1/5/10 request stages and zero failures |
| GenAIEval-compatible route eval | Done | `evals/genaieval/`, `evidence/genaieval/route_eval_results.json`, `evidence/genaieval/benchmark_results.json` | Local route dataset and 300-call benchmark; compatible pack is separate from official GenAIEval |
| Re-ranker | Done as optional profile | `src/wear_edge_opea/reranker.py`, `src/wear_edge_opea/reranker_service.py`, `docker-compose.reranker.yml` | Provides lexical and remote-compatible reranking boundary; not yet a heavy production reranking model |
| Kubernetes | Done as optional profile | `deploy/kubernetes/wearedge-opea-manufacturing.yaml`, `docs/kubernetes-optional-profile.md` | Kubernetes manifest exists; Helm/GMC are not implemented |
| Final evidence tracker update | Done in project tracker | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2#issuecomment-4631635695` | Upstream PR direct comment was attempted but blocked by GitHub integration permissions |
| Upstream OPEA collaboration | Evidence exists | OPEA RFC issue, GenAIExamples PR #2462, OPEA docs PR #395, local comment drafts | Do not claim official acceptance or official publication until the PRs are merged |

## Priority Decision

| Priority | Action | Decision |
| --- | --- | --- |
| P1 | Publish or attach a final evidence update | Project tracker copy is done; upstream PR/issue copy remains permission-gated |
| P2 | Production reranking model service | Defer unless reviewers ask or a stable model endpoint is chosen |
| P2 | Helm/GMC packaging | Defer; Kubernetes manifest already gives cloud-native evidence without adding chart maintenance |
| Maintenance | Re-run local/cloud LLM benchmarks before final demo/submission | Keep; model endpoints can drift |
| Excluded | GraphRAG | Do not do in this release |
| Excluded | Fine-tuning/SFT/DPO/PPO | Do not do in this release |

## Practical Remaining Gap

The remaining gap is not core functionality. The core OPEA evidence path now
covers official TEI, RAG, reranker, LLM local/cloud endpoints, official
GenAIEval, Docker Compose, and optional Kubernetes. The practical gap is
reviewer communication and maintenance:

1. Keep upstream PR/RFC threads updated with a concise evidence comment when
   write permission is available; the project tracker copy is already public.
2. Keep strict LLM endpoint benchmark JSON fresh before the final submission.
3. Avoid expanding scope into GraphRAG, fine-tuning, Helm/GMC, or heavy reranker
   work unless the review process explicitly demands it.
