# WearEdge OPEA Manufacturing

Dedicated ITU AI for Good / OPEA Manufacturing submission package for WearEdge Pro.

Project URL:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

WearEdge OPEA Manufacturing is a five-agent, OPEA-aligned manufacturing suite. A single Gateway and Manufacturing Megaservice route first-person M400 evidence through Dataprep, RAG, Vector DB, LLM adapter, deterministic evaluators, and guardrails before producing bounded action cards for plant systems.

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
curl http://127.0.0.1:8088/healthz
curl http://127.0.0.1:8088/v1/agents
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/agents/iqc/demo
curl http://127.0.0.1:8088/v1/agents/changeover/demo
curl http://127.0.0.1:8088/v1/agents/wi/demo
curl http://127.0.0.1:8088/v1/agents/hazard/demo
curl http://127.0.0.1:8088/v1/scorecard
```

The legacy maintenance endpoints remain available:

```bash
curl http://127.0.0.1:8088/v1/manufacturing/demo
curl http://127.0.0.1:8088/v1/manufacturing/suite
```

## API Surface

| Endpoint | Purpose |
| --- | --- |
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
| [`data/sample_requests/`](data/sample_requests/) | Five agent demo inputs |
| [`data/agent_kb/`](data/agent_kb/) | IQC, changeover, WI, and hazard knowledge sources |
| [`data/maintenance_kb/`](data/maintenance_kb/) | Lao-shi-fu maintenance KB |
| [`src/wear_edge_opea/agents.py`](src/wear_edge_opea/agents.py) | Unified route registry |
| [`src/wear_edge_opea/scorecard.py`](src/wear_edge_opea/scorecard.py) | Five-agent evaluation scorecard |
| [`docker-compose.yml`](docker-compose.yml) | Qdrant + Manufacturing Gateway runnable profile |
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

## Source Provenance

This repository is the self-contained OPEA competition package. The full engineering project remains available at:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

The submitted system is an assistive industrial decision-support prototype, not a certified safety or maintenance-release controller. High-risk outputs remain human-confirmed, and guardrails block unsupported claims such as final root cause, restart permission, quality release, safety clearance, and maintenance release.
