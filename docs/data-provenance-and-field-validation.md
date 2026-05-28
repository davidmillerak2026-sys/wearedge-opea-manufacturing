# Data Provenance And Field Validation Boundary

Date: 2026-05-28

## What Is Real

The broader WearEdge-Pro project contains the real deployment lineage:

```text
Vuzix M400 / Android front end
  -> Jetson / FastAPI gateway
  -> local edge LLM path
  -> M400 result return
  -> maintenance-focused lao-shi-fu evidence workflow
```

The maintenance route is the hero because it has the strongest archived
wearable/edge evidence and maps directly to CMMS work-order drafting.

## What Is Packaged For Judges

This OPEA repository is the self-contained challenge package. It includes:

- deterministic sample requests for five manufacturing agents;
- released-source style KB files for each route;
- route-specific thresholds, confirmations, source IDs, and blocked claims;
- Docker/Qdrant/OPEA TEI runtime evidence;
- a browser console and API scorecard so judges do not need M400 hardware.

## What Is Prototype Data

The IQC, changeover, WI, and hazard data are demo-scale manufacturing scenarios.
They are intentionally transparent and committed as JSON so judges can inspect
every source and reproduce every action card.

The submission should claim:

```text
runnable prototype + field-evidence lineage + route-specific released-source
controls + guardrails
```

The submission should not claim:

```text
large proprietary factory dataset, certified safety controller, autonomous
release authority, customer production rollout, or final root-cause authority
```

## How This Still Competes

Many enterprise GenAI demos stop at one chatbot. WearEdge shows a platform
pattern across five plant workflows:

| Route | Value pool | Human-safe boundary |
| --- | --- | --- |
| Maintenance | Downtime and expert know-how | Draft work order, no final root cause |
| IQC | Scrap, rework, customer escapes | Quality hold, no final disposition |
| Changeover | Restart loss and SKU mix-up | Checklist hold, no restart permission |
| WI | Training and procedure drift | Released guidance, no bypass/interlock instruction |
| Hazard | Near-miss capture and corrective action | EHS observation, no safety clearance |

This is a stronger business story than a single dataset demo because it proves
route isolation, integration targets, and guardrails across multiple factory
systems.
