# Champion Gap Worklist

The current WearEdge Pro source is strong, but first-prize positioning requires making the OPEA evidence executable and judge-friendly across all five Manufacturing agents.

## P0

| Work item | Reason | Done when |
| --- | --- | --- |
| Make this repository self-contained for five agents | The official project URL should not feel like a wrapper-only repo | Judges can access five route samples, KBs, docs, demo, and evidence from one clear landing page |
| Harden OPEA runtime wrapper into final challenge profile | Protects the 20-point "Use of OPEA" subscore | `docker compose up` or `./deploy.sh` starts the five-agent Manufacturing demo path and records expected output |
| Polish one-click challenge deployment | Official submission requirement | Fresh clone can run sample Manufacturing flow with documented logs |
| Finalize <=2 page technical report | Official submission requirement | PDF/Markdown report has no placeholder or planned claims |
| Productize judge-facing demo console | Converts API evidence into an evaluable product | `/demo` lets judges switch routes, run demos, inspect RAG evidence, action cards, guardrails, and scorecard |
| Produce 1-3 minute prototype demo video | Optional officially, useful after product console exists | HyperFrames source, MP4 render, render report, and public GitHub video asset page are ready |

## P1

| Work item | Reason | Done when |
| --- | --- | --- |
| Replace hashing embeddings with production embedding service | Improves RAG quality and technical credibility | Official TEI/GenAIComps profile is implemented and passed both local Docker Desktop and Google Cloud C3 fresh-clone E2E |
| Add production LLM adapter benchmark path | Prevents the LLM component claim from looking like a pure stub | OpenAI/OPEA-compatible adapter, benchmark script, local contract smoke JSON, and strict production endpoint claim boundary are included |
| Add deeper GenAIEval-style benchmark report | Strengthens System Efficiency | Done: `evals/genaieval/` and `evidence/genaieval/` include a 15-case route dataset, metrics runner, summary, and 300-call throughput/latency benchmark |
| Add Intel hardware optimization path | Up to 15 bonus points | Harness and local smoke test are ready; Xeon AVX-512/AMX JSON captured |
| Publish OPEA issue/PR/blueprint feedback | Up to 15 open-source bonus points | RFC issue, implementation update, and TEI update are posted at `https://github.com/opea-project/GenAIExamples/issues/2461`; tracker posted at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`; upstream PR #2462 is open at `https://github.com/opea-project/GenAIExamples/pull/2462`; contribution package and `git format-patch` artifact are prepared under `docs/opea-upstream/pr-ready/` |
| Publish technical article/video walkthrough | Up to 10 knowledge-sharing bonus points | Article is public and recorded at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1`; video source, local render, render report, and public GitHub video asset page are ready |

## P2

| Work item | Reason | Done when |
| --- | --- | --- |
| Add challenge-specific screenshots | Judges skim quickly | README includes architecture + real prototype image |
| Add public dataset/source statement | Compliance and reproducibility | Data sources and generated sample evidence are listed |
| Add short FAQ | Reduces judge confusion | README answers "Why OPEA?", "Why Manufacturing?", "What is real?" |
| Add champion risk burn-down | Makes final review explicit | Six non-winning risks are tracked in `docs/champion-risk-burn-down.md` with artifacts and claim boundaries |
