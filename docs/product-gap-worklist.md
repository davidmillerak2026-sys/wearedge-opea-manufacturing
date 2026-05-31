# Product Gap Worklist

The current WearEdge Pro source is strong, but product readiness requires making the OPEA evidence executable and evaluator-friendly across all five Manufacturing agents.

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
| Add production LLM adapter benchmark path | Prevents the LLM component claim from looking like a pure stub | OpenAI/OPEA-compatible adapter, benchmark script, local contract smoke JSON, and strict production endpoint claim boundary are included |
| Add deeper GenAIEval-style benchmark report | Strengthens System Efficiency | Done: `evals/genaieval/` and `evidence/genaieval/` include a 15-case route dataset, metrics runner, summary, and 300-call throughput/latency benchmark |
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
