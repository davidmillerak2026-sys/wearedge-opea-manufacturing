# WearEdge OPEA Manufacturing

Dedicated ITU AI for Good / OPEA Manufacturing submission package for WearEdge Pro.

Project URL:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

WearEdge OPEA Manufacturing is a five-agent, OPEA-aligned manufacturing suite. A single Gateway and Manufacturing Megaservice route first-person M400 evidence through Dataprep, RAG, Vector DB, LLM adapter, deterministic evaluators, and guardrails before producing bounded action cards for plant systems.

## Submission Product Shape

This repository is the challenge-facing product package. It is not submitted as an Android-only app. The submitted deliverable is a Docker-runnable OPEA Manufacturing Agent Suite with a browser demo console, public API, five route demos, and scorecard.

Product front ends:

| Front end | Role |
| --- | --- |
| Web Demo Console at `/demo` | Judge-facing experience for reproducible evaluation |
| API endpoints under `/v1` | Machine-verifiable OPEA route and scorecard surface |
| Vuzix M400 / Android client | Real deployment front end and field-evidence source from the full WearEdge-Pro project |

The M400 evidence is a product differentiator, but judges do not need M400 hardware to evaluate the submission.

## Five Manufacturing Agents

| Mode | Scenario | Integration target | Business value |
| --- | --- | --- | --- |
| `maintenance` | Lao-shi-fu predictive maintenance for `PKG-L3-GBX-03` | `maintenance_work_order` | Reduce downtime and preserve expert troubleshooting patterns |
| `iqc` | Machined aluminum housing quality inspection | `qms_quality_event` | Reduce scrap, rework, and customer escape risk |
| `changeover` | Labeler SKU-C500 changeover verification | `changeover_checklist` | Reduce restart errors, mix-up risk, and changeover loss |
| `wi` | Released work-instruction guidance for `CARTONER-ST2` | `wi_reference` | Reduce training time and procedure drift |
| `hazard` | PPE, moving-parts, and blocked-walkway EHS observation | `ehs_case` | Improve near-miss capture and corrective action routing |

The maintenance route remains the hero demo because it has the strongest archived M400/Jetson field evidence, but all five agents are runnable through the same OPEA-style API.

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
  -> LLM service adapter, deterministic no-model demo path
  -> route-specific evaluator
  -> Guardrails and blocked claims
  -> CMMS / QMS / MES / WI / EHS action card
```

Official component evidence is in [`evidence/component-evidence.json`](evidence/component-evidence.json) and [`docs/opea-component-evidence.md`](docs/opea-component-evidence.md).

## Run Locally

Dependency-free local demo:

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
| [`docs/official-opea-profile.md`](docs/official-opea-profile.md) | OPEA-compatible embedding microservice profile |
| [`docs/official-opea-tei-profile.md`](docs/official-opea-tei-profile.md) | Official OPEA TEI embedding profile and C3 rerun instructions |
| [`docs/publication-record.md`](docs/publication-record.md) | Public OPEA/article publication URLs |
| [`docs/opea-upstream/`](docs/opea-upstream/) | OPEA RFC issue draft, blueprint feedback, and PR plan |
| [`docs/intel-avx512-amx-benchmark-report.md`](docs/intel-avx512-amx-benchmark-report.md) | Intel CPU benchmark report with Google Cloud C3 Xeon AVX-512/AMX evidence |
| [`docs/gcp-c3-docker-qdrant-e2e-report.md`](docs/gcp-c3-docker-qdrant-e2e-report.md) | Google Cloud C3 fresh-clone Docker/Qdrant E2E evidence |
| [`docs/gcp-c3-opea-profile-e2e-report.md`](docs/gcp-c3-opea-profile-e2e-report.md) | Google Cloud C3 OPEA-compatible embedding profile E2E evidence |
| [`docs/local-opea-tei-profile-e2e-report.md`](docs/local-opea-tei-profile-e2e-report.md) | Local official OPEA TEI embedding profile E2E evidence |
| [`docs/gcp-c3-opea-tei-profile-e2e-report.md`](docs/gcp-c3-opea-tei-profile-e2e-report.md) | Google Cloud C3 official OPEA TEI embedding profile E2E evidence |
| [`public/article-wear-edge-opea-manufacturing.md`](public/article-wear-edge-opea-manufacturing.md) | Public knowledge-sharing article draft |
| [`public/demo-video-script.md`](public/demo-video-script.md) | 1-3 minute demo video shot list and narration |
| [`data/sample_requests/`](data/sample_requests/) | Five agent demo inputs |
| [`data/agent_kb/`](data/agent_kb/) | IQC, changeover, WI, and hazard knowledge sources |
| [`data/maintenance_kb/`](data/maintenance_kb/) | Lao-shi-fu maintenance KB |
| [`src/wear_edge_opea/agents.py`](src/wear_edge_opea/agents.py) | Unified route registry |
| [`src/wear_edge_opea/demo_console.py`](src/wear_edge_opea/demo_console.py) | Judge-facing browser product console |
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
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2
docs/opea-upstream/rfc-issue-draft.md
docs/opea-upstream/blueprint-feedback.md
docs/opea-upstream/implementation-feedback-comment.md
docs/opea-upstream/minimal-pr-scope.md
```

Knowledge-sharing package:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1
public/article-wear-edge-opea-manufacturing.md
public/demo-video-script.md
public/demo-video-captions.srt
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
evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json
evidence/benchmarks/local_opea_profile_e2e.summary.json
evidence/benchmarks/local_opea_tei_profile_e2e.summary.json
evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json
evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json
```

Official OPEA TEI rerun script:

```text
scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh
```

The Xeon run was captured on Google Cloud C3 `c3-standard-4` with Intel Xeon Platinum 8481C, `avx512f=true`, `amx_tile=true`, `amx_int8=true`, `amx_bf16=true`, scorecard `ok=true`, and 4,581.4536 calls/second across 5,000 deterministic route calls.

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

The submitted system is an assistive industrial decision-support prototype, not a certified safety or maintenance-release controller. High-risk outputs remain human-confirmed, and guardrails block unsupported claims such as final root cause, restart permission, quality release, safety clearance, and maintenance release.
