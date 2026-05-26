# Champion Gap Worklist

The current WearEdge Pro source is strong, but first-prize positioning requires making the OPEA evidence executable and judge-friendly.

## P0

| Work item | Reason | Done when |
| --- | --- | --- |
| Make this repository self-contained or explicitly dual-link source | The official project URL should not feel like a wrapper-only repo | Judges can access source code, docs, demo, and evidence from one clear landing page |
| Harden OPEA runtime wrapper into final challenge profile | Protects the 20-point "Use of OPEA" subscore | `docker compose up` or `./deploy.sh` starts the Manufacturing demo path and records expected output |
| Polish one-click challenge deployment | Official submission requirement | Fresh clone can run sample Manufacturing flow with documented logs |
| Finalize <=2 page technical report | Official submission requirement | PDF/Markdown report has no `TBD` or planned claims |
| Produce 1-3 minute prototype demo video | Optional officially, essential for champion-level clarity | Video shows actual M400/edge workflow, not only cinematic branding |

## P1

| Work item | Reason | Done when |
| --- | --- | --- |
| Replace hashing embeddings with production embedding service | Improves RAG quality and technical credibility | OPEA embedding service or selected embedding model is documented and benchmarked |
| Add GenAIEval-style scorecard | Strengthens System Efficiency | Scorecard covers latency, throughput, RAG quality, and action-card correctness |
| Add Intel hardware optimization path | Up to 15 bonus points | OpenVINO/AVX-512/AMX or Intel CPU benchmark is documented |
| Publish OPEA issue/PR/blueprint feedback | Up to 15 open-source bonus points | Public link recorded in `submission-fields.draft.json` |
| Publish technical article/video walkthrough | Up to 10 knowledge-sharing bonus points | Public link recorded as `publication_url` |

## P2

| Work item | Reason | Done when |
| --- | --- | --- |
| Add challenge-specific screenshots | Judges skim quickly | README includes architecture + real prototype image |
| Add public dataset/source statement | Compliance and reproducibility | Data sources and generated sample evidence are listed |
| Add short FAQ | Reduces judge confusion | README answers "Why OPEA?", "Why Manufacturing?", "What is real?" |
