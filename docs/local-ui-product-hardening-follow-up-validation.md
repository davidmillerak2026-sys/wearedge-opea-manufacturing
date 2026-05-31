# Local UI And Product Hardening Follow-Up Validation

Date: 2026-05-28

Purpose: validate the follow-up changes requested after the product evidence areas
audit:

- stronger "real industrial AI agent system" framing;
- private enterprise production-data boundary, including toothbrush workshop
  IQC/OQC lineage;
- upgraded five-agent Web Console UI;
- OPEA/LLM/hardware/evidence gap closure documentation.

## Docker Compose Run

Command:

```powershell
docker compose up --build -d
```

Result:

```text
manufacturing-gateway image rebuilt
qdrant container running
manufacturing-gateway container recreated and started
```

Note: Docker reported existing orphan containers from a previous OPEA TEI run.
They do not affect the base Compose profile validation.

## Endpoint Checks

| Endpoint | Result |
| --- | --- |
| `GET /healthz` | `ok=true`, vector backend `qdrant`, LLM backend `deterministic`, agents `maintenance, iqc, changeover, wi, hazard` |
| `GET /demo` | HTML returned with upgraded WearEdge Pro OPEA Manufacturing Console |
| `GET /v1/agents` | Returned all five agent modes and route metadata |
| `GET /v1/scorecard` | `ok=true`, all five routes pass |

Scorecard route status:

| Route | Status | Integration target |
| --- | --- | --- |
| `maintenance` | pass | `maintenance_work_order` |
| `iqc` | pass | `qms_quality_event` |
| `changeover` | pass | `changeover_checklist` |
| `wi` | pass | `wi_reference` |
| `hazard` | pass | `ehs_case` |

## UI Changes Validated By Returned HTML

The returned `/demo` HTML includes:

- "Real industrial AI agent system" positioning;
- five agent route selector;
- OPEA pipeline rail: Gateway, Megaservice, Dataprep, Retriever, TEI Embedding,
  LLM Adapter, Evaluator, Guardrails;
- RAG source evidence panel;
- action-card panel with source IDs, LLM runtime, entity, blocked claims, and
  human confirmation state;
- scorecard panel;
- enterprise data boundary panel stating private production lineage and public
  sanitized fixtures.

## Browser Screenshot Note

An attempt to inspect the UI through the browser automation tool failed
because the browser automation kernel exited unexpectedly. The live application
itself was still verified through Docker and HTTP endpoint checks. A visual
browser screenshot can be retried through Chrome/Browser plugin separately if
needed.

## Supporting Checks

```text
project-profile.json: valid JSON
evidence/component-evidence.json: valid JSON
scripts/evidence_check.py: passed
python -m unittest discover -s tests: 15 tests passed
git diff --check: no whitespace errors, Windows LF/CRLF warnings only
```
