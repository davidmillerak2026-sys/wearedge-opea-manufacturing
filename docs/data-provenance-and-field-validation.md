# Data Provenance And Field Validation Boundary

Date: 2026-05-28

## What Is Real

WearEdge Pro is a real industrial AI agent system, not a toy demo. The broader
WearEdge-Pro project contains the deployment lineage:

```text
Vuzix M400 / Android front end
  -> Jetson / FastAPI gateway
  -> local edge LLM or configured model service
  -> industrial agent loop
  -> M400 result return
  -> plant action-card workflow
```

Archived WearEdge-Pro records include real M400 / Jetson runs for maintenance,
IQC, WI, changeover, and hazard flows. The maintenance route remains the hero
because it has the strongest archived wearable/edge evidence and maps directly
to CMMS work-order drafting.

## Private Enterprise Production Data

The product also has private enterprise production-data lineage. This includes
customer manufacturing quality-inspection work such as toothbrush workshop
visual inspection for IQC/OQC-style defect detection and quality hold workflows.

Those raw customer files, plant images, labels, lot identifiers, and production
records are not committed to this public challenge repository. The submission
keeps the claim boundary clear:

- real enterprise production-data lineage exists in the WearEdge program;
- public repo data is sanitized, small, and reproducible;
- private customer data is represented through redacted route behavior,
  anonymized quality-plan patterns, detector confidence fields, source IDs, and
  QMS-style action-card contracts;
- no confidential production image, customer identity, or lot-level record is
  leaked.

## What Is Packaged For Judges

This OPEA repository is the self-contained challenge package. It includes:

- deterministic sample requests for five manufacturing agents;
- sanitized knowledge-base files for each route;
- route-specific thresholds, confirmations, source IDs, and blocked claims;
- Docker/Qdrant/OPEA TEI runtime evidence;
- a browser console and API scorecard so judges do not need M400 hardware or
  customer plant data.

## What Is Competition-Scale Evaluation Data

The committed route records are competition-scale evaluation fixtures for the
real WearEdge industrial agent system. They are intentionally transparent and
committed as JSON so judges can inspect every source and reproduce every action
card. They are not the full proprietary customer dataset.

The submission should claim:

```text
real industrial AI agent system + private production-data lineage +
sanitized public evaluation package + field-evidence lineage +
route-specific released-source controls + guardrails
```

The submission should not claim:

```text
public release of proprietary customer data, certified safety controller,
autonomous release authority, customer identity disclosure, or final root-cause
authority
```

## How This Competes

Many enterprise GenAI submissions stop at one chatbot. WearEdge shows a
platform pattern across five plant workflows:

| Route | Value pool | Enterprise evidence boundary | Human-safe boundary |
| --- | --- | --- | --- |
| Maintenance | Downtime and expert know-how | M400 / Jetson lao-shi-fu evidence | Draft work order, no final root cause |
| IQC/OQC | Scrap, rework, customer escapes | Private quality-inspection lineage, including toothbrush workshop visual inspection | Quality hold, no final disposition |
| Changeover | Restart loss and SKU mix-up | Released setup/checklist evidence | Checklist hold, no restart permission |
| WI | Training and procedure drift | Released work-instruction evidence | Released guidance, no bypass/interlock instruction |
| Hazard | Near-miss capture and corrective action | M400 / plant-scene safety evidence | EHS observation, no safety clearance |

This is a stronger business story than a single dataset submission because it
proves route isolation, integration targets, and guardrails across multiple
factory systems while respecting customer confidentiality.
