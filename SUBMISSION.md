# ITU AI for Good OPEA Manufacturing Submission

Challenge: Innovation Challenge on Generative AI Applications for Enterprise Scenarios Using OPEA

Vertical: Manufacturing

Application name: WearEdge Pro

## One-Sentence Summary

WearEdge Pro is an OPEA-aligned wearable edge AI suite for Manufacturing that routes first-person M400 evidence into five bounded agents: maintenance, IQC, changeover, work instruction, and hazard observation.

## Why This Fits Manufacturing

Manufacturing losses rarely live in one silo. A frontline operator may see a gearbox vibration issue, a machined-part defect, a changeover mismatch, a work-instruction question, or an unsafe walkway. WearEdge Pro uses one OPEA-style Gateway and Manufacturing Megaservice to convert those observations into auditable action cards for plant systems.

| Agent | Manufacturing decision | Integration target |
| --- | --- | --- |
| `maintenance` | Is this machine condition ready for CMMS escalation? | `maintenance_work_order` |
| `iqc` | Should this part or lot be held for quality review? | `qms_quality_event` |
| `changeover` | Is the SKU changeover evidence ready for first-piece sign-off? | `changeover_checklist` |
| `wi` | What released work instruction should guide the operator? | `wi_reference` |
| `hazard` | Does the scene require stop, report, or EHS correction? | `ehs_case` |

The hero scenario remains the lao-shi-fu predictive-maintenance loop for packaging-line gearbox `PKG-L3-GBX-03`, because it has the strongest archived M400/Jetson evidence. The submitted repository now also includes runnable samples and route-specific guardrails for IQC, changeover, WI, and hazard.

## OPEA Claim

Current submission components:

```text
LLM, RAG, Vector DB, Orchestration, Guardrails
```

Implemented OPEA-style path:

```text
Gateway -> Manufacturing Megaservice -> Dataprep -> Retriever/RAG -> Vector DB -> LLM adapter -> Evaluator -> Guardrails -> Action Card
```

The Docker Compose profile uses Qdrant as the Vector DB. The local no-dependency demo keeps an in-memory vector fallback so reviewers can run the same route contracts without Docker.

## Runnable Evidence

```bash
docker compose up --build -d
curl http://127.0.0.1:8088/v1/agents
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/agents/iqc/demo
curl http://127.0.0.1:8088/v1/agents/changeover/demo
curl http://127.0.0.1:8088/v1/agents/wi/demo
curl http://127.0.0.1:8088/v1/agents/hazard/demo
curl http://127.0.0.1:8088/v1/scorecard
```

The scorecard reports route latency, contract pass, guardrail pass, RAG/source match, action-target correctness, and route-isolation pass/fail for all five agents.

## Source Evidence

Full engineering source:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

Key archived evidence already mapped into this submission package:

- M400 real-device full chain
- Jetson local multimodal inference
- five-agent deterministic validation
- lao-shi-fu maintenance evidence loop
- manufacturing RAG / maintenance KB
- IQC quality plan and released-source checks
- guardrailed action cards
- runtime stream and audit logs
- automated tests

## Remaining Champion Bonus Work

- Publish OPEA issue/PR/blueprint feedback link.
- Publish technical article or public walkthrough.
- Add 1-3 minute demo video link.
- Add Intel AVX-512/AMX benchmark evidence.
