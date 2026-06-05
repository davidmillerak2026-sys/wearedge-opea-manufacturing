# Product Gap Worklist

The current WearEdge Pro source is strong, but product readiness requires making the OPEA evidence executable and evaluator-friendly across all five Manufacturing agents.

Status date: 2026-06-05

Current decision: continue the OPEA optimization plan except GraphRAG and
fine-tuning/SFT/DPO/PPO. The immediate focus is evidence quality, official
evaluation proof, model endpoint proof, optional OPEA reranking, and deployment
depth without weakening the one-command demo path.

## Current Status Snapshot

| Area | Status | Evidence |
| --- | --- | --- |
| Local model endpoint | Done | `evidence/benchmarks/llm_adapter.local-gemma.json` records Ollama `gemma4:31b`, strict mode, five route calls, `fallback_count=0`, `all_contracts_pass=true` |
| Cloud model endpoint | Done | `evidence/benchmarks/llm_adapter.deepseek.json` records DeepSeek `deepseek-chat`, strict mode, five route calls, `fallback_count=0`, `all_contracts_pass=true`; API key value is not stored |
| Official GenAIEval | Done | `evidence/genaieval/official_benchmark_summary.json` records official GenAIEval `chatqnafixed` local run with 1/5/10 request stages and zero failures |
| Re-ranker | Done as optional profile | `src/wear_edge_opea/reranker.py`, `src/wear_edge_opea/reranker_service.py`, and `docker-compose.reranker.yml` add a reranking stage and service profile |
| Kubernetes | Done as optional manifest | `deploy/kubernetes/wearedge-opea-manufacturing.yaml` documents a minimal Qdrant, reranker, and gateway deployment profile; Helm/GMC is still optional future depth |
| Final evidence update | Done in project tracker | Consolidated public evidence update posted at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2#issuecomment-4631635695`; direct upstream PR comment was blocked by GitHub integration permissions |
| Upstream OPEA status | External dependency | GenAIExamples PR #2462 and OPEA docs PR #395 are opened evidence, but they are not merged, so the project must not claim official OPEA acceptance/publication yet |

## P0

| Work item | Reason | Done when |
| --- | --- | --- |
| Make this repository self-contained for five agents | The official project URL should not feel like a wrapper-only repo | Evaluators can access five route samples, KBs, docs, sample, and evidence from one clear landing page |
| Harden OPEA runtime wrapper into final release profile | Protects OPEA use evidence | `docker compose up` or `./deploy.sh` starts the five-agent Manufacturing sample path and records expected output |
| Polish one-click release deployment | Official release requirement | Fresh clone can run sample Manufacturing flow with documented logs |
| Finalize <=2 page technical report | Official release requirement | PDF/Markdown report has no placeholder or planned claims |
| Productize evaluation-facing manufacturing console | Converts API evidence into an evaluable product | `/demo` lets evaluators switch routes, run samples, inspect RAG evidence, action cards, guardrails, and scorecard |
| Produce 1-3 minute product walkthrough video | Optional officially, useful after product console exists | HyperFrames source, MP4 render, render report, YouTube walkthrough, and public GitHub video asset page are ready |

## P1

| Work item | Reason | Done when |
| --- | --- | --- |
| Replace hashing embeddings with production embedding service | Improves RAG quality and technical credibility | Official TEI/GenAIComps profile is implemented and passed both local Docker Desktop and Google Cloud C3 fresh-clone E2E |
| Add production LLM adapter benchmark path | Prevents the LLM component claim from looking like a pure stub | Done: OpenAI/OPEA-compatible and Ollama adapter, benchmark script, local contract smoke JSON, strict local Gemma4:31B endpoint evidence, strict DeepSeek cloud endpoint evidence, and no-fallback claim boundaries are included |
| Add deeper GenAIEval-style benchmark report | Strengthens System Efficiency | Done: `evals/genaieval/` and `evidence/genaieval/` include a 15-case route dataset, metrics runner, summary, 300-call throughput/latency benchmark, and official OPEA GenAIEval `chatqnafixed` local benchmark summary |
| Add OPEA-style reranker stage | Aligns with the OPEA architecture slide's retriever/reranker pattern | Done as optional profile: vector retrieval can pass through lexical or remote-compatible reranking, and `/v1/rerank` is available as a service profile |
| Add Intel hardware optimization path | Public evidence | Done: Xeon AVX-512/AMX JSON, C3 Docker/Qdrant E2E, OPEA-compatible embedding E2E, official OPEA TEI E2E, and `docs/intel-effective-use-evidence.md` are captured with application-level claim boundaries |
| Publish OPEA issue/PR/blueprint feedback | Public open-source evidence | RFC issue, implementation update, and TEI update are posted at `https://github.com/opea-project/GenAIExamples/issues/2461`; tracker posted at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`; upstream PR #2462 is open at `https://github.com/opea-project/GenAIExamples/pull/2462`; OPEA docs Publications PR #395 is open at `https://github.com/opea-project/docs/pull/395`; contribution package and `git format-patch` artifact are prepared under `docs/opea-upstream/pr-ready/` |
| Publish technical article/video walkthrough | Public knowledge-sharing evidence | Done: external Dev.to article and YouTube product walkthrough video are published; OPEA docs Publications PR #395 proposes adding the article to the official OPEA Publications / Blogs list; GitHub article/video backups remain public and are tracked in `docs/publication-record.md` |

## P2

| Work item | Reason | Done when |
| --- | --- | --- |
| Add project-specific screenshots | Evaluators skim quickly | README includes architecture and real system imagery |
| Add public dataset/source statement | Compliance and reproducibility | Data sources and generated sample evidence are listed |
| Add short FAQ | Reduces evaluator confusion | README answers "Why OPEA?", "Why Manufacturing?", "What is real?" |
| Add product risk burn-down | Makes final review explicit | Six product risks are tracked in `docs/product-risk-burn-down.md` with artifacts and claim boundaries |
| Add optional Kubernetes deployment depth | Supports OPEA cloud-native narrative without blocking Docker evaluation | Done: minimal Kubernetes manifest and validation notes are tracked in `deploy/kubernetes/wearedge-opea-manufacturing.yaml` and `docs/kubernetes-optional-profile.md`; Helm/GMC remains future work |

## Remaining Decision List

| Priority | Item | Recommendation | Reason |
| --- | --- | --- | --- |
| P1 | Post or attach final upstream evidence update | Project tracker copy is done; post upstream when write permission is available | Low implementation cost and improves reviewer visibility across TEI, C3, reranker, GenAIEval, local Gemma, DeepSeek, article/video, and Kubernetes evidence |
| P2 | Production reranking model service | Defer until endpoint or model choice is stable | Current optional reranker proves the architecture; a heavier model service adds quality but can destabilize local evaluation |
| P2 | Helm/GMC packaging | Defer unless reviewers ask for deeper cloud-native proof | Kubernetes manifest already supports the narrative; Helm/GMC adds maintenance and test cost |
| Maintenance | Refresh local/cloud LLM benchmarks | Run before final submission or major demo | Endpoint and local model performance can drift; strict no-fallback evidence should stay fresh |
| Excluded | GraphRAG | Do not do in this release | Current dataset and product framing are conventional route-isolated RAG; GraphRAG would require graph extraction, schema, query planning, and new evals |
| Excluded | Fine-tuning/SFT/DPO/PPO | Do not do in this release | Fine-tuning needs curated training data, GPU training cost, model governance, and safety evaluation beyond this release's evidence needs |
