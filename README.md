# WearEdge OPEA Manufacturing

Dedicated ITU AI for Good / OPEA Manufacturing submission package for WearEdge Pro.

Project URL:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

WearEdge OPEA Manufacturing is the OPEA-aligned delivery package for WearEdge Pro, a real industrial AI agent system for frontline manufacturing operations. A single Gateway and Manufacturing Megaservice route first-person M400 evidence, sanitized customer-production-derived quality evidence, and route-specific plant context through Dataprep, RAG, Vector DB, an optional OpenAI/OPEA-compatible LLM adapter, deterministic evaluators, and guardrails before producing bounded action cards for plant systems.

This is not a demo-only repository. The Web Console is the judge-facing demo surface; the product being submitted is a real five-agent industrial system packaged so reviewers can run and inspect it without private plant data or M400 hardware.

Champion submission headline:

```text
Five manufacturing agents + official OPEA TEI embeddings + Qdrant RAG +
Gateway/Megaservice orchestration + guardrails + GenAIEval-compatible evidence +
GCP C3 evidence.
```

Single-node challenge compliance:

```text
Google Cloud C3 c3-standard-4
4 vCPU, 16 GiB RAM, no GPU
Intel Xeon Platinum 8481C with AVX-512 and AMX flags detected
Within the challenge limit: single node, <=64GB RAM, 4-core CPU profile, GPU optional
```

## Submission Product Shape

This repository is the challenge-facing product package. It is not submitted as an Android-only app. The submitted deliverable is a Docker-runnable OPEA Manufacturing Agent Suite with a browser demo console, public API, five route demos, and scorecard.

Product front ends:

| Front end | Role |
| --- | --- |
| Web Demo Console at `/demo` | Judge-facing experience for reproducible evaluation |
| API endpoints under `/v1` | Machine-verifiable OPEA route and scorecard surface |
| Vuzix M400 / Android client | Real deployment front end and field-evidence source from the full WearEdge-Pro project |

The M400 evidence is a product differentiator, but judges do not need M400 hardware to evaluate the submission.

## Challenge Task Fit

WearEdge Pro maps directly to the four official challenge tasks:

| Challenge task | WearEdge answer |
| --- | --- |
| Domain-specific GenAI application | Manufacturing AI agent suite using OPEA-style Gateway, Megaservice, LLM adapter, TEI embeddings, Qdrant RAG, guardrails, and evaluation |
| Concrete industry scenario | Manufacturing, with maintenance, IQC, changeover, work-instruction, and hazard workflows |
| Working prototype with documentation | Docker-runnable OPEA package, README, technical report, `deploy.sh`, Compose profiles, and one-command smoke path |
| Performance and usability | GCP C3 4-vCPU / 16-GiB / no-GPU evidence, latency JSON, Docker memory stats, 8-worker route concurrency benchmark, 300-call GenAIEval-compatible benchmark, and `/demo` browser console |

See [`docs/challenge-task-compliance.md`](docs/challenge-task-compliance.md).

## Five Manufacturing Agents

| Mode | Scenario | Integration target | Business value |
| --- | --- | --- | --- |
| `maintenance` | Lao-shi-fu predictive maintenance for `PKG-L3-GBX-03` | `maintenance_work_order` | Reduce downtime and preserve expert troubleshooting patterns |
| `iqc` | IQC/OQC quality inspection, with private customer lineage including toothbrush workshop visual inspection | `qms_quality_event` | Reduce scrap, rework, and customer escape risk |
| `changeover` | Labeler SKU-C500 changeover verification | `changeover_checklist` | Reduce restart errors, mix-up risk, and changeover loss |
| `wi` | Released work-instruction guidance for `CARTONER-ST2` | `wi_reference` | Reduce training time and procedure drift |
| `hazard` | PPE, moving-parts, and blocked-walkway EHS observation | `ehs_case` | Improve near-miss capture and corrective action routing |

The maintenance route remains the hero route because it has the strongest archived M400/Jetson field evidence, but all five agents are runnable through the same OPEA-style API.

## OPEA Architecture

```text
Vuzix M400 / API request
  -> Gateway
  -> Manufacturing Megaservice
  -> route registry: maintenance / iqc / changeover / wi / hazard
  -> Dataprep + route-specific knowledge source
  -> Retriever / RAG
  -> Qdrant Vector DB profile, with in-memory fallback
  -> optional OPEA-compatible Embedding Microservice /v1/embeddings
  -> LLM service adapter, deterministic no-model evaluation path or OpenAI/OPEA-compatible endpoint
  -> route-specific evaluator
  -> Guardrails and blocked claims
  -> CMMS / QMS / MES / WI / EHS action card
  -> scorecard and GenAIEval-compatible evidence artifacts
```

Official component evidence is in [`evidence/component-evidence.json`](evidence/component-evidence.json) and [`docs/opea-component-evidence.md`](docs/opea-component-evidence.md).

## Run Locally

Dependency-free local runtime:

```powershell
.\scripts\run_demo.ps1
```

Code validation:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

Docker Compose profile with Qdrant:

```bash
docker compose up --build -d
# Open in browser: http://127.0.0.1:8088/demo
curl http://127.0.0.1:8088/healthz
curl http://127.0.0.1:8088/v1/agents
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/agents/iqc/demo
curl http://127.0.0.1:8088/v1/agents/changeover/demo
curl http://127.0.0.1:8088/v1/agents/wi/demo
curl http://127.0.0.1:8088/v1/agents/hazard/demo
curl http://127.0.0.1:8088/v1/scorecard
```

Official OPEA-compatible embedding microservice profile:

```bash
docker compose -f docker-compose.yml -f docker-compose.opea.yml up --build -d
curl http://127.0.0.1:6000/healthz
curl http://127.0.0.1:8088/healthz
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/scorecard
```

This profile routes Qdrant embeddings through a separate `/v1/embeddings`
microservice and reports `qdrant-opea-compatible-embedding-vector-store` in
RAG results.

Official OPEA TEI embedding profile:

```bash
docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml up -d
curl http://127.0.0.1:6000/v1/health_check
curl http://127.0.0.1:8088/healthz
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/scorecard
```

This profile follows the OPEA GenAIComps TEI pattern: Hugging Face TEI serves
the embedding model, the OPEA embedding microservice connects through
`TEI_EMBEDDING_ENDPOINT` and
`EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`, and the Manufacturing Gateway
uses `/v1/embeddings` for Qdrant indexing and retrieval.

LLM adapter contract benchmark:

```powershell
$env:PYTHONPATH="src"
python scripts\llm_adapter_benchmark.py --iterations 1 `
  --output evidence\benchmarks\llm_adapter_contract.local-smoke.json
```

To benchmark a real OpenAI/OPEA-compatible LLM endpoint, set
`WEAREDGE_LLM_BACKEND=openai-compatible`, `WEAREDGE_LLM_URL` or
`WEAREDGE_LLM_BASE_URL`, `WEAREDGE_LLM_MODEL`, and
`WEAREDGE_LLM_STRICT=true`. See
[`docs/production-llm-benchmark-path.md`](docs/production-llm-benchmark-path.md).

Strict LMM oil-leak image benchmark:

```powershell
$env:PYTHONPATH="src"
$env:WEAREDGE_LMM_PROVIDER="gemini"
$env:GEMINI_MODEL="gemini-2.5-flash"
python scripts\lmm_image_benchmark.py --image evidence\images\machine_oil_leak.png `
  --output evidence\benchmarks\lmm_machine_oil_leak.strict.json --strict
```

Only cite this as production LMM evidence when the output reports
`claim_status=strict_production_lmm_endpoint_benchmarked` and
`all_checks_pass=true`. See
[`docs/lmm-machine-oil-leak-benchmark-report.md`](docs/lmm-machine-oil-leak-benchmark-report.md).

GenAIEval-compatible route evaluation:

```powershell
$env:PYTHONPATH="src"
python evals\genaieval\run_wear_edge_eval.py --output evidence\genaieval\route_eval_results.json --summary-output evidence\genaieval\summary.md
python evals\genaieval\run_wear_edge_benchmark.py --iterations 20 --output evidence\genaieval\benchmark_results.json
```

This lightweight package provides a JSONL dataset, benchmark metadata, runner,
metrics, and committed evidence outputs. It does not claim full official
GenAIEval/RAGAS/AutoRAG/LLM-as-judge execution.

The legacy maintenance endpoints remain available:

```bash
curl http://127.0.0.1:8088/v1/manufacturing/demo
curl http://127.0.0.1:8088/v1/manufacturing/suite
```

## API Surface

| Endpoint | Purpose |
| --- | --- |
| `GET /` and `GET /demo` | Browser Manufacturing Demo Console |
| `GET /healthz` | Service, vector backend, and supported agents |
| `GET /v1/agents` | Route registry and knowledge/sample paths |
| `GET /v1/agents/{mode}/demo` | Fixed sample request for one agent |
| `POST /v1/agents/{mode}/infer` | Route-specific inference with caller-provided evidence |
| `GET /v1/scorecard` | Five-route scorecard: latency, contract, guardrail, RAG/source match, action target correctness |

## Included Materials

| Path | Purpose |
| --- | --- |
| [`SUBMISSION.md`](SUBMISSION.md) | Challenge-facing summary |
| [`docs/technical-report.draft.md`](docs/technical-report.draft.md) | <=2 page technical report draft |
| [`docs/submission-product-shape.md`](docs/submission-product-shape.md) | Final product/deliverable definition |
| [`docs/final-submission-readiness-audit.md`](docs/final-submission-readiness-audit.md) | Evaluation criteria mapping, evidence links, and remaining final tasks |
| [`docs/final-submission-form-fill-guide.md`](docs/final-submission-form-fill-guide.md) | Copy/paste guide for the challenge submission form |
| [`docs/evaluation-criteria-scorecard.md`](docs/evaluation-criteria-scorecard.md) | 100 base + 40 bonus official rubric full-mark audit |
| [`docs/full-mark-gap-closure-plan.md`](docs/full-mark-gap-closure-plan.md) | Point-by-point follow-up plan for OPEA, LLM, code quality, UI, and bonus gaps |
| [`docs/local-ui-full-mark-follow-up-validation.md`](docs/local-ui-full-mark-follow-up-validation.md) | Local Docker/UI validation after the full-mark follow-up changes |
| [`docs/challenge-task-compliance.md`](docs/challenge-task-compliance.md) | Direct mapping to the official Challenge Task requirements |
| [`docs/source-vlm-e2e-evidence-map.md`](docs/source-vlm-e2e-evidence-map.md) | WearEdge-Pro real Jetson/Gemma 4 E2B VLM E2E evidence map and OPEA repo boundary |
| [`docs/lmm-machine-oil-leak-benchmark-report.md`](docs/lmm-machine-oil-leak-benchmark-report.md) | Strict public oil-leak image benchmark protocol for real LMM endpoints |
| [`docs/final-pre-submit-audit-2026-05-28.md`](docs/final-pre-submit-audit-2026-05-28.md) | Final pre-submit evidence audit |
| [`docs/champion-risk-burn-down.md`](docs/champion-risk-burn-down.md) | One-by-one mitigation for the six known champion risks |
| [`docs/opea-native-depth-matrix.md`](docs/opea-native-depth-matrix.md) | OPEA component depth matrix and claim boundaries |
| [`docs/production-llm-benchmark-path.md`](docs/production-llm-benchmark-path.md) | Optional production LLM endpoint benchmark path |
| [`docs/genaieval-compatible-evaluation.md`](docs/genaieval-compatible-evaluation.md) | Lightweight GenAIEval-compatible dataset, runner, metrics, and evidence |
| [`docs/data-provenance-and-field-validation.md`](docs/data-provenance-and-field-validation.md) | Real system lineage, competition data scope, and field validation boundary |
| [`docs/telecom-scope-and-manufacturing-positioning.md`](docs/telecom-scope-and-manufacturing-positioning.md) | Manufacturing positioning if judges compare telecom/network projects |
| [`docs/submission-url-dry-run.md`](docs/submission-url-dry-run.md) | Public URL dry run for challenge form fields |
| [`docs/local-docker-desktop-final-validation.md`](docs/local-docker-desktop-final-validation.md) | Final local Docker Desktop runtime validation |
| [`docs/official-opea-profile.md`](docs/official-opea-profile.md) | OPEA-compatible embedding microservice profile |
| [`docs/official-opea-tei-profile.md`](docs/official-opea-tei-profile.md) | Official OPEA TEI embedding profile and C3 rerun instructions |
| [`docs/publication-record.md`](docs/publication-record.md) | Public OPEA/article publication URLs |
| [`docs/opea-upstream/`](docs/opea-upstream/) | OPEA RFC issue draft, blueprint feedback, and PR plan |
| [`docs/opea-upstream/pr-ready/`](docs/opea-upstream/pr-ready/) | Copyable OPEA `GenAIExamples` contribution package |
| [`docs/upstream-pr-attempt-2026-05-28.md`](docs/upstream-pr-attempt-2026-05-28.md) | Direct upstream PR attempt, fork push, opened PR record, and CI-green status |
| [`docs/intel-avx512-amx-benchmark-report.md`](docs/intel-avx512-amx-benchmark-report.md) | Intel CPU benchmark report with Google Cloud C3 Xeon AVX-512/AMX evidence |
| [`docs/intel-effective-use-evidence.md`](docs/intel-effective-use-evidence.md) | Intel effective-use evidence across route, Qdrant, embedding, and official OPEA TEI workloads |
| [`docs/gcp-c3-docker-qdrant-e2e-report.md`](docs/gcp-c3-docker-qdrant-e2e-report.md) | Google Cloud C3 fresh-clone Docker/Qdrant E2E evidence |
| [`docs/gcp-c3-opea-profile-e2e-report.md`](docs/gcp-c3-opea-profile-e2e-report.md) | Google Cloud C3 OPEA-compatible embedding profile E2E evidence |
| [`docs/local-opea-tei-profile-e2e-report.md`](docs/local-opea-tei-profile-e2e-report.md) | Local official OPEA TEI embedding profile E2E evidence |
| [`docs/gcp-c3-opea-tei-profile-e2e-report.md`](docs/gcp-c3-opea-tei-profile-e2e-report.md) | Google Cloud C3 official OPEA TEI embedding profile E2E evidence |
| [`docs/gcp-c3-tei-onednn-verbose-runbook.md`](docs/gcp-c3-tei-onednn-verbose-runbook.md) | GCP C3 TEI oneDNN/ISA verbose capture runbook |
| [Dev.to external article](https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh) | Published public knowledge-sharing article |
| [`public/article-wear-edge-opea-manufacturing.md`](public/article-wear-edge-opea-manufacturing.md) | Public GitHub article backup |
| [`public/article-opea-tei-qdrant-guardrails-lessons.md`](public/article-opea-tei-qdrant-guardrails-lessons.md) | OPEA practical technical article: TEI, Qdrant, guardrails, hardware, and feedback |
| [`public/external-platform-article.md`](public/external-platform-article.md) | Source article package published via Dev.to |
| [`docs/public-platform-publishing-handoff.md`](docs/public-platform-publishing-handoff.md) | Remaining public video publication steps and claim boundary |
| [`public/demo-video-script.md`](public/demo-video-script.md) | 1-3 minute demo video shot list and narration |
| [`public/video-platform-description.md`](public/video-platform-description.md) | Copy-ready public video platform title, description, and tags |
| [YouTube demo video](https://www.youtube.com/watch?v=dd9k8m6PDco) | Published public demo video |
| [`public/demo-video/`](public/demo-video/) | Renderable HyperFrames demo video source package |
| [`docs/demo-video-render-report.md`](docs/demo-video-render-report.md) | Local demo video render and validation evidence |
| [`evals/genaieval/`](evals/genaieval/) | GenAIEval-compatible evaluation pack |
| [`evidence/genaieval/`](evidence/genaieval/) | Generated route evaluation, benchmark JSON, and summary |
| [`evidence/source-wearedge-vlm/e2e-summary.json`](evidence/source-wearedge-vlm/e2e-summary.json) | Machine-readable source-project VLM evidence summary |
| [`evidence/images/machine_oil_leak.png`](evidence/images/machine_oil_leak.png) | Public redacted maintenance image fixture for strict LMM benchmark |
| [`data/sample_requests/`](data/sample_requests/) | Five agent demo inputs |
| [`data/agent_kb/`](data/agent_kb/) | IQC, changeover, WI, and hazard knowledge sources |
| [`data/maintenance_kb/`](data/maintenance_kb/) | Lao-shi-fu maintenance KB |
| [`src/wear_edge_opea/agents.py`](src/wear_edge_opea/agents.py) | Unified route registry |
| [`src/wear_edge_opea/demo_console.py`](src/wear_edge_opea/demo_console.py) | Judge-facing browser product console |
| [`src/wear_edge_opea/llm_adapter.py`](src/wear_edge_opea/llm_adapter.py) | Deterministic and OpenAI/OPEA-compatible LLM adapter |
| [`src/wear_edge_opea/scorecard.py`](src/wear_edge_opea/scorecard.py) | Five-agent evaluation scorecard |
| [`docker-compose.yml`](docker-compose.yml) | Qdrant + Manufacturing Gateway runnable profile |
| [`docker-compose.opea.yml`](docker-compose.opea.yml) | Optional OPEA-compatible embedding microservice override |
| [`docker-compose.opea-tei.yml`](docker-compose.opea-tei.yml) | Optional official OPEA TEI embedding profile |
| [`tests/`](tests/) | Route, guardrail, scorecard, and Qdrant validation |

## Submission Fields

Draft challenge fields are in [`submission-fields.draft.json`](submission-fields.draft.json).

Recommended component selection:

```text
LLM, RAG, Vector DB, Orchestration, Guardrails
```

## Evidence Check

```powershell
python scripts\evidence_check.py
```

Expected:

```text
OPEA submission evidence check passed
```

## Bonus Evidence

OPEA open-source contribution package:

```text
https://github.com/opea-project/GenAIExamples/issues/2461
https://github.com/opea-project/GenAIExamples/pull/2462
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2
https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017
docs/upstream-pr-attempt-2026-05-28.md
docs/opea-upstream/rfc-issue-draft.md
docs/opea-upstream/blueprint-feedback.md
docs/opea-upstream/implementation-feedback-comment.md
docs/opea-upstream/minimal-pr-scope.md
docs/opea-upstream/pr-ready-update-comment.md
docs/opea-upstream/pr-ready/
docs/opea-upstream/pr-ready/0001-add-manufacturing-agent-suite.patch
```

Knowledge-sharing package:

```text
https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh
https://www.youtube.com/watch?v=dd9k8m6PDco
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1
public/article-wear-edge-opea-manufacturing.md
public/external-platform-article.md
docs/public-platform-publishing-handoff.md
public/demo-video-script.md
public/demo-video-captions.srt
public/video-platform-description.md
public/demo-video/
docs/demo-video-render-report.md
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4
```

Intel CPU benchmark evidence:

```powershell
$env:PYTHONPATH="src"
python scripts\intel_cpu_benchmark.py --iterations 200
```

The committed benchmark evidence includes:

```text
evidence/benchmarks/intel_cpu_benchmark.local-smoke.json
evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json
evidence/benchmarks/intel_effective_use.summary.json
evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json
evidence/benchmarks/local_opea_profile_e2e.summary.json
evidence/benchmarks/local_opea_tei_profile_e2e.summary.json
evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json
evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json
evidence/benchmarks/llm_adapter_contract.local-smoke.json
evidence/benchmarks/route_concurrency.local-smoke.json
```

Official OPEA TEI rerun script:

```text
scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh
```

GenAIEval-compatible evidence:

```text
evals/genaieval/manufacturing_route_eval.dataset.jsonl
evals/genaieval/manufacturing_route_benchmark.yaml
evidence/genaieval/route_eval_results.json
evidence/genaieval/benchmark_results.json
evidence/genaieval/summary.md
```

The committed route evaluation reports 15/15 cases passing across maintenance,
IQC, changeover, WI, and hazard. The benchmark records 300 route evaluations
with all cases passing and all five routes covered.

The Xeon run was captured on Google Cloud C3 `c3-standard-4`, a single-node
4-vCPU / 16-GiB-RAM / no-GPU profile that is inside the challenge limit of
single node, <=64GB RAM, and 4-core CPU. The CPU was Intel Xeon Platinum 8481C
with `avx512f=true`, `amx_tile=true`, `amx_int8=true`, `amx_bf16=true`,
scorecard `ok=true`, and 4,581.4536 calls/second across 5,000 deterministic
route calls.

The Intel effective-use summary combines that CPU feature run with C3
Docker/Qdrant E2E, OPEA-compatible embedding E2E, and official OPEA TEI E2E.
It shows the WearEdge OPEA TEI embedding/RAG profile and five-agent suite
running inside the single-node 4-vCPU / 16-GiB-RAM / no-GPU challenge envelope.
It does not claim oneDNN/TEI microkernel dispatch proof or production LLM
acceleration.

The Docker/Qdrant E2E run was captured on Google Cloud C3 `c3-standard-4` in `us-central1-a`. It fresh-cloned this repository, started Docker Compose, verified Qdrant plus the Manufacturing Gateway, passed all five demo and infer routes, passed `/v1/scorecard`, and deleted the temporary VM `wearedge-docker-e2e-0527082214` after the run.

The official OPEA TEI E2E run was captured on Google Cloud C3 `c3-standard-4` in `us-central1-a`. It fresh-cloned this repository, started Qdrant, `opea/embedding:latest`, Hugging Face TEI, and the Manufacturing Gateway, verified 768-dimensional TEI embeddings, passed all five route demos with `qdrant-opea-tei-vector-store`, passed `/v1/scorecard`, and deleted the temporary VM `wearedge-opea-tei-0527103938` after the run.

Xeon AMX runbook:

```text
docs/xeon-amx-benchmark-runbook.md
scripts/xeon_amx_benchmark_remote.sh
```

## Source Provenance

This repository is the self-contained OPEA competition package. The full engineering project remains available at:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

The submitted system is an assistive industrial AI decision-support system, not a certified safety or maintenance-release controller. High-risk outputs remain human-confirmed, and guardrails block unsupported claims such as final root cause, restart permission, quality release, safety clearance, and maintenance release.
