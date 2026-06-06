# WearEdge OPEA Manufacturing Project Overview

Program: OPEA-aligned enterprise GenAI manufacturing application

Vertical: Manufacturing

Application name: WearEdge Pro

## One-Sentence Summary

WearEdge Pro is a real OPEA-aligned wearable edge industrial AI agent system for Manufacturing that routes first-person M400 evidence into five bounded agents: maintenance, IQC, changeover, work instruction, and hazard observation.

## Final Product Shape

The public release package is not an Android-only APK and not an ephemeral contest artifact. It is the Docker-runnable OPEA Manufacturing Agent Suite package for the WearEdge Pro industrial AI agent system, with a browser evaluation console and API surface.

The public repository contains sanitized, reproducible route fixtures. The broader WearEdge program has private enterprise production-data lineage, including quality-inspection work such as toothbrush workshop visual inspection for IQC/OQC-style defect detection. Raw customer plant images, labels, lot identifiers, and customer-specific production records are intentionally not published.

Evaluation entry point:

```text
http://127.0.0.1:8088/demo
```

The Vuzix M400 / Android client is the real deployment front end and field-evidence source from the full WearEdge-Pro product. The Browser Manufacturing Console is the reproducible evaluation surface for evaluators who do not have M400 hardware.

Data-source boundary:

```text
OPEA workloads and GitHub resources from opea.dev and github.com/opea-project;
sanitized manufacturing knowledge sources and deterministic/synthetic benchmark
fixtures committed in this repository; private enterprise production-data
lineage for WearEdge, including toothbrush workshop IQC/OQC visual-inspection
work, with raw customer data excluded from the public package; and public/open
stack resources such as Hugging Face TEI, Qdrant, Docker images, and public
documentation. Do not claim unrelated THUCTC, CLUE, CSDB, DRCD, Kaggle, Common
Crawl, or DBpedia usage unless those datasets are explicitly added later.
```

Single-node hardware proof:

```text
Google Cloud C3 c3-standard-4, us-central1-a
4 vCPU, 16 GiB RAM, no GPU
Intel Xeon Platinum 8481C
AVX-512 and AMX flags detected
Runtime fit: single node, <=64GB RAM, 4-core CPU profile, GPU optional
10-minute clean-run: default Docker/Qdrant C3 timed run passed clean_initial_run_under_10_min=true and all_checks_pass=true
Measured clean install + initial run: 45 seconds
```

## Why This Fits Manufacturing

Manufacturing losses rarely live in one silo. A frontline operator may see a gearbox vibration issue, a machined-part defect, a changeover mismatch, a work-instruction question, or an unsafe walkway. WearEdge Pro uses one OPEA-style Gateway and Manufacturing Megaservice to convert those observations into auditable action cards for plant systems.

| Agent | Manufacturing decision | Integration target |
| --- | --- | --- |
| `maintenance` | Is this machine condition ready for CMMS escalation? | `maintenance_work_order` |
| `iqc` | Should this part or lot be held for quality review, including IQC/OQC visual-inspection patterns from private production lineage? | `qms_quality_event` |
| `changeover` | Is the SKU changeover evidence ready for first-piece sign-off? | `changeover_checklist` |
| `wi` | What released work instruction should guide the operator? | `wi_reference` |
| `hazard` | Does the scene require stop, report, or EHS correction? | `ehs_case` |

The hero scenario remains the lao-shi-fu predictive-maintenance loop for packaging-line gearbox `PKG-L3-GBX-03`, because it has the strongest archived M400/Jetson evidence. The public repository now also includes runnable samples and route-specific guardrails for IQC, changeover, WI, and hazard.

## OPEA Claim

Current project components:

```text
LLM, RAG, Vector DB, Orchestration, Guardrails
```

Implemented OPEA-style path:

```text
Gateway -> Manufacturing Megaservice -> Dataprep -> Retriever/RAG -> Vector DB -> LLM adapter -> Evaluator -> Guardrails -> Action Card
```

The OPEA value point is that these boundaries are modular and composable.
Gateway, Megaservice, Retriever/RAG, Vector DB, LLM adapter, Evaluator, and
Guardrails are stable platform components; the model is only the pluggable
service behind the adapter. WearEdge can therefore run with local Jetson/Gemma
4 E2B, Gemini, or another OpenAI/OPEA-compatible model endpoint without
rewriting route isolation, source grounding, deterministic checks, or action
card contracts.

Evaluation path:

```text
/v1/scorecard + GenAIEval-compatible JSONL dataset, runner, metrics, benchmark JSON, and summary.md
```

The Docker Compose profile uses Qdrant as the Vector DB. The local no-dependency sample keeps an in-memory vector fallback so operators and evaluators can run the same route contracts without Docker.

The repository also includes an official OPEA-compatible embedding microservice profile:

```bash
docker compose -f docker-compose.yml -f docker-compose.opea.yml up --build -d
```

That profile adds a separate `/v1/embeddings` microservice and configures the Gateway with `WEAREDGE_EMBEDDING_BACKEND=opea`, so Qdrant indexing and search use a microservice boundary instead of only in-process embeddings.

The repository also includes a stronger official TEI component profile:

```bash
docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml up -d
```

That profile follows OPEA's TEI embedding pattern with Hugging Face TEI,
`TEI_EMBEDDING_ENDPOINT`, `EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`, the
OPEA embedding microservice, Qdrant, and the same five WearEdge manufacturing
routes. It is the right profile to rerun on Google Cloud C3 for official
production embedding evidence.

The FastAPI gateway also serves a browser Manufacturing Console at `/demo`, so operators and evaluators can inspect requests, RAG evidence, action cards, guardrails, and scorecard results without writing curl commands.

The LLM adapter now supports both the deterministic no-secret path and an
OpenAI/OPEA-compatible chat-completions endpoint. The recorded evidence
includes a local adapter contract benchmark; production LLM wording should only
be used after a configured endpoint benchmark reports
`production_llm_endpoint_benchmarked`.

## OPEA Architecture Alignment

| OPEA requirement | WearEdge Pro implementation |
| --- | --- |
| Design and build a domain-specific GenAI application | OPEA-style Manufacturing suite with Gateway, Megaservice, LLM adapter, official TEI embedding profile, Qdrant RAG, route evaluators, guardrails, and scorecard |
| Select a concrete industry scenario | Manufacturing, covering maintenance, IQC, changeover, work instruction, and EHS hazard observation |
| Deliver a working prototype with documentation | Docker-runnable WearEdge Pro OPEA package with `README.md`, `TECHNICAL_REPORT.md`, `deploy.sh`, Compose profiles, and Web/API evaluation surface |
| Demonstrate performance and usability | GCP C3 4-vCPU / 16-GiB / no-GPU runs, latency JSON, Docker memory stats, 8-worker route concurrency benchmark, GenAIEval-compatible 300-call benchmark, and browser console at `/demo` |

Detailed mapping: `docs/opea-architecture-alignment.md`.

## Product Evidence Defense

WearEdge Pro is organized around the official product evaluation criteria:

| Product evidence area | Project evidence |
| --- | --- |
| Creativity and Business Value | Five real manufacturing workflows and integration targets, private production-data lineage, and field evidence, not a single chatbot |
| Technical Implementation | OPEA-style modular Gateway/Megaservice/Retriever-RAG/Qdrant Vector DB/LLM-adapter/Evaluator/Guardrails architecture with local and GCP evidence; model choice is pluggable |
| Product Quality | Docker-runnable Web/API product, `/demo`, five sample routes, five infer routes, scorecard, tests, and documentation |
| Open-source evidence | OPEA RFC/comments plus upstream PR #2462 with key check-run evidence, and OPEA docs Publications PR #395 |
| Knowledge-sharing evidence | Public Dev.to technical article, YouTube product walkthrough video, and OPEA Publications blog-listing PR #395 |
| Hardware optimization evidence | Intel Xeon AVX-512/AMX C3 evidence, application-level OPEA TEI/Qdrant workload records, and same-host oneDNN BF16/AMX probe dispatch evidence |

Detailed evidence map: `docs/product-evaluation-map.md`. Product hardening plan: `docs/product-hardening-plan.md`.

## Runnable Evidence

```bash
docker compose up --build -d
# Open in browser: http://127.0.0.1:8088/demo
curl http://127.0.0.1:8088/v1/agents
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/agents/iqc/demo
curl http://127.0.0.1:8088/v1/agents/changeover/demo
curl http://127.0.0.1:8088/v1/agents/wi/demo
curl http://127.0.0.1:8088/v1/agents/hazard/demo
curl http://127.0.0.1:8088/v1/scorecard
```

The scorecard reports route latency, contract pass, guardrail pass, RAG/source match, action-target correctness, and route-isolation pass/fail for all five agents.

The lightweight GenAIEval-compatible evaluation pack in `evals/genaieval/`
adds 15 committed route cases and records 15/15 pass across contract, target,
channel, risk, human gate, guardrail, RAG source, and route-isolation metrics.

## Source Evidence

Full engineering source:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

Key archived evidence already mapped into this product package:

- M400 real-device full chain
- Jetson local multimodal inference
- five-agent deterministic validation
- lao-shi-fu maintenance evidence loop
- manufacturing RAG / maintenance KB
- IQC quality plan and released-source checks
- guardrailed action cards
- runtime stream and audit logs
- automated tests

## Product Hardening And Public Evidence

- OPEA issue/PR/blueprint feedback: public RFC issue posted at `https://github.com/opea-project/GenAIExamples/issues/2461`; implementation and official TEI update comments posted upstream; real upstream PR opened at `https://github.com/opea-project/GenAIExamples/pull/2462`; DCO, dependency-review, get-test-matrix, get-test-case, and compose-test check runs pass on the current PR head, while legacy `pre-commit.ci - pr` reports failure; OPEA docs Publications PR #395 opened at `https://github.com/opea-project/docs/pull/395` and remains unmerged; public tracker posted at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`. The prepared contribution package and `git format-patch` artifact remain under `docs/opea-upstream/pr-ready/`.
- Product risk burn-down: each known product risk has a mitigation and claim boundary in `docs/product-risk-burn-down.md`, including OPEA-native depth, production LLM benchmark path, skim-friendly sample positioning, data provenance, upstream PR status, and telecom-vs-manufacturing positioning.
- LLM adapter benchmark path: `src/wear_edge_opea/llm_adapter.py` and `scripts/llm_adapter_benchmark.py` provide a production endpoint benchmark path while keeping the default reproducible run deterministic and reproducible.
- GenAIEval-compatible evaluation: `evals/genaieval/` and `evidence/genaieval/` provide a dataset, benchmark config, runner, 15-case route evaluation JSON, throughput/latency benchmark JSON, and summary.
- OPEA-compatible embedding profile: `docker-compose.opea.yml` adds a separate `/v1/embeddings` microservice and routes Qdrant RAG embeddings through it.
- Official OPEA TEI profile: `docker-compose.opea-tei.yml` wires Hugging Face TEI, the OPEA embedding microservice, Qdrant, and the five agent routes for production embedding evidence; local E2E and Google Cloud C3 fresh-clone E2E both passed.
- Knowledge sharing: the external technical article is published on Dev.to at `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh`; the product walkthrough video is published on YouTube at `https://www.youtube.com/watch?v=dd9k8m6PDco`; OPEA docs Publications PR #395 proposes adding the article to the official OPEA Publications / Blogs list, but is not merged yet; the GitHub article/video backups remain public evidence.
- Intel AVX-512/AMX: Google Cloud C3 `c3-standard-4` single-node run captured in `us-central1-a` with 4 vCPU, 16 GiB RAM, no GPU, Intel Xeon Platinum 8481C, `avx512f`, `amx_tile`, `amx_int8`, and `amx_bf16` detected; scorecard passed; `docs/intel-effective-use-evidence.md` and `evidence/benchmarks/intel_effective_use.summary.json` connect the C3 CPU feature run to Docker/Qdrant, OPEA-compatible embedding, official OPEA TEI, and supplemental TEI/oneDNN verbose-attempt workloads.
- Docker/Qdrant E2E: Google Cloud C3 `c3-standard-4` single-node 4-vCPU / 16-GiB-RAM / no-GPU fresh-clone run captured in `us-central1-a`; Docker Compose started Qdrant plus the Manufacturing Gateway, `/demo` returned HTTP 200, five sample routes and five infer routes returned correct action cards, `/v1/scorecard` passed, and the VM was deleted after the run.
- 10-minute clean-run requirement: the default Docker/Qdrant timed C3 run on temporary VM `wearedge-docker-e2e-0529041313` reached `setup_seconds=23`, `clean_initial_run_seconds=45`, `validation.clean_initial_run_under_10_min=true`, and `all_checks_pass=true`.
- OPEA profile E2E: Google Cloud C3 `c3-standard-4` single-node 4-vCPU / 16-GiB-RAM / no-GPU fresh-clone run captured in `us-central1-a`; Docker Compose started Qdrant, the OPEA-compatible `/v1/embeddings` service, and the Manufacturing Gateway; five routes reported `qdrant-opea-compatible-embedding-vector-store`, `/v1/scorecard` passed, and the VM was deleted after the run.
- Local official OPEA TEI E2E: Docker Desktop started `opea/embedding:latest`, Hugging Face TEI, Qdrant, and the Manufacturing Gateway; `/v1/embeddings` returned 768-dimensional embeddings; all five samples reported `qdrant-opea-tei-vector-store`; `/v1/scorecard` passed.
- GCP C3 official OPEA TEI E2E: Google Cloud C3 `c3-standard-4` single-node 4-vCPU / 16-GiB-RAM / no-GPU fresh-clone run captured in `us-central1-a`; Docker Compose started Qdrant, `opea/embedding:latest`, Hugging Face TEI, and the Manufacturing Gateway; 768-dimensional embeddings, five `qdrant-opea-tei-vector-store` route samples, and `/v1/scorecard` passed; temporary VM `wearedge-opea-tei-0527103938` was deleted after the run.
- Supplemental C3 TEI/oneDNN run: Google Cloud C3 `c3-standard-4` single-node run from the historical May 29 submission series, now represented by valid tag `final-submission-2026-05-29-r23`, passed Gateway health, `/v1/scorecard`, five sample routes, Docker stats capture, AVX-512 flag check, AMX flag check, TEI log capture, and same-host oneDNN BF16/AMX probe dispatch capture; temporary VM `wearedge-tei-onednn-0529024359` was deleted after the run. The captured TEI build did not emit dispatch marker lines, so this is application-level Intel effective-use evidence plus host-level oneDNN dispatch evidence, not TEI-internal AMX dispatch proof.

## Public Evidence URLs And Artifacts

- `publication_url`: `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh`
- `publication_record_url`: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1`
- OPEA RFC issue: `https://github.com/opea-project/GenAIExamples/issues/2461`
- OPEA upstream PR: `https://github.com/opea-project/GenAIExamples/pull/2462`
- OPEA docs Publications PR: `https://github.com/opea-project/docs/pull/395`
- OPEA TEI update comment: `https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017`
- OPEA tracker: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`
- Upstream PR record: `docs/upstream-pr-attempt-2026-05-28.md`
- OPEA RFC issue working copy: `docs/opea-upstream/rfc-issue-working-copy.md`
- OPEA blueprint feedback: `docs/opea-upstream/blueprint-feedback.md`
- OPEA contribution package used for PR #2462: `docs/opea-upstream/pr-ready/`
- OPEA PR patch artifact: `docs/opea-upstream/pr-ready/0001-add-manufacturing-agent-suite.patch`
- Product risk burn-down: `docs/product-risk-burn-down.md`
- OPEA native depth matrix: `docs/opea-native-depth-matrix.md`
- Production LLM benchmark path: `docs/production-llm-benchmark-path.md`
- GenAIEval-compatible evaluation: `docs/genaieval-compatible-evaluation.md`
- GenAIEval-compatible route eval JSON: `evidence/genaieval/route_eval_results.json`
- GenAIEval-compatible benchmark JSON: `evidence/genaieval/benchmark_results.json`
- Official OPEA profile: `docs/official-opea-profile.md`
- Official OPEA TEI profile: `docs/official-opea-tei-profile.md`
- Local OPEA TEI report: `docs/local-opea-tei-profile-e2e-report.md`
- GCP C3 OPEA TEI report: `docs/gcp-c3-opea-tei-profile-e2e-report.md`
- GCP C3 TEI/oneDNN verbose report: `docs/gcp-c3-tei-onednn-verbose-report.md`
- Public URL availability check report: `docs/public-url-check.md`
- Local Docker Desktop final validation: `docs/local-docker-desktop-final-validation.md`
- GCP OPEA profile report: `docs/gcp-c3-opea-profile-e2e-report.md`
- Intel benchmark report: `docs/intel-avx512-amx-benchmark-report.md`
- Intel effective-use evidence: `docs/intel-effective-use-evidence.md`
- Intel effective-use summary JSON: `evidence/benchmarks/intel_effective_use.summary.json`
- GCP C3 TEI/oneDNN verbose summary JSON: `evidence/benchmarks/gcp_c3_tei_onednn_verbose.summary.json`
- GCP Docker/Qdrant E2E report: `docs/gcp-c3-docker-qdrant-e2e-report.md`
- Product walkthrough video source package: `public/product-walkthrough/`
- Product walkthrough render report: `docs/product-walkthrough-render-report.md`
- Product walkthrough video URL: `https://www.youtube.com/watch?v=dd9k8m6PDco`
- Final form fill guide: `docs/project-profile-fill-guide.md`
- Local benchmark JSON: `evidence/benchmarks/intel_cpu_benchmark.local-smoke.json`
- Xeon AVX-512/AMX benchmark JSON: `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json`
- GCP Docker/Qdrant E2E summary JSON: `evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json`
- GCP OPEA profile E2E summary JSON: `evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json`
