# OpenAI-Native Integration Blueprint for WearEdge Pro

Date: 2026-06-18

## Purpose

This blueprint translates the accompanying technology article into an implementation plan. It is additive: the existing route registry, RAG layer, deterministic evaluators, guardrails, and human gates remain the manufacturing control plane.

## Current Verified Boundary

The public runtime currently supports:

- deterministic explanation output by default;
- an OpenAI-compatible Chat Completions HTTP adapter;
- five route-specific evaluators and action-card contracts;
- in-memory or Qdrant vector storage;
- optional OPEA-compatible and TEI embedding profiles;
- scorecard and evaluation artifacts.

The repository should not claim an OpenAI model production benchmark until a strict no-fallback artifact against an actual OpenAI endpoint is recorded.

## Target Architecture

```text
M400 / browser / sensor evidence
  -> edge evidence processor
       - asset and station identity
       - image crop/redaction
       - size and MIME validation
       - evidence hash
  -> WearEdge Gateway
       - authentication and RBAC
       - tenant/plant isolation
       - request schema validation
       - idempotency and audit ID
  -> route registry
       - maintenance / iqc / changeover / wi / hazard
  -> route-specific retrieval
       - released-source filtering
       - revision checks
       - TEI embeddings
       - Qdrant
  -> OpenAI Responses adapter
       - text and image inputs
       - grounded explanation
       - strict tool selection
       - structured action proposal
  -> deterministic evaluator
       - thresholds
       - required confirmations
       - asset identity
       - stale-source rejection
  -> guardrails
       - prohibited claims
       - authority boundary
       - fail-closed checks
  -> human approval
  -> least-privilege CMMS/QMS/MES/WI/EHS connector
  -> immutable audit event and eval telemetry
```

## Responses Adapter Contract

Proposed module:

```text
src/wear_edge_opea/openai_responses_adapter.py
```

Configuration:

```text
WEAREDGE_LLM_BACKEND=openai-responses
OPENAI_API_KEY=<secret-manager-reference>
WEAREDGE_OPENAI_MODEL=<approved-model-id>
WEAREDGE_OPENAI_TIMEOUT_SECONDS=30
WEAREDGE_OPENAI_MAX_OUTPUT_TOKENS=500
WEAREDGE_OPENAI_STORE=false
WEAREDGE_OPENAI_STRICT=true
```

Do not log API keys, bearer headers, raw private images, or unrestricted model response bodies.

## Proposed Structured Action Card

```json
{
  "schema_version": "1.0",
  "route": "maintenance",
  "entity_id": "PKG-L3-GBX-03",
  "evidence_ids": ["evidence-sha256-..."],
  "source_ids": ["maintenance-policy-rev-7"],
  "source_revision": "7",
  "observations": [
    {
      "type": "visible_shaking",
      "value": true,
      "confidence": 0.91
    }
  ],
  "proposed_tool": "draft_maintenance_work_order",
  "risk_level": "high",
  "reason": "Multiple accepted evidence flags exceed the released maintenance thresholds.",
  "requires_human_confirmation": true,
  "prohibited_authority": [
    "final_root_cause",
    "remaining_useful_life",
    "restart_permission",
    "maintenance_release"
  ]
}
```

The production schema should use strict structured output rules:

- `additionalProperties: false` at every object level;
- all properties required;
- optional semantics represented with nullable types where necessary;
- enums for route, risk, tool, and authority fields;
- bounded string and array lengths;
- server-side revalidation before tool execution.

## Least-Privilege Tools

### Maintenance

```text
draft_maintenance_work_order
get_asset_history
request_vibration_recheck
```

The model cannot close a work order, grant restart, or release maintenance.

### IQC

```text
draft_qms_quality_event
request_expanded_inspection
attach_redacted_defect_evidence
```

The model cannot release the lot or determine final disposition.

### Changeover

```text
prepare_changeover_signoff_package
request_missing_confirmation
```

The model cannot authorize restart or first-piece release.

### Work instruction

```text
open_released_work_instruction
request_identity_confirmation
escalate_active_alarm
```

The model cannot invent an instruction or bypass an interlock.

### Hazard

```text
draft_ehs_observation
request_stop_and_make_safe_confirmation
attach_redacted_hazard_evidence
```

The model cannot declare an area safe or determine final incident root cause.

## Required Server-Side Validation

Before any tool call is executed:

1. Verify authenticated user, role, tenant, plant, and shift context.
2. Verify entity identity and route match.
3. Verify retrieved source is released and current.
4. Re-run the deterministic route evaluator.
5. Verify the proposed tool belongs to the route allow-list.
6. Verify prohibited-authority fields are absent.
7. Verify human approval for high or critical actions.
8. Apply idempotency key and duplicate-action protection.
9. Write a pre-execution audit event.
10. Execute in sandbox or read-only mode before production enablement.

## Multimodal Evidence Policy

- Accept only approved MIME types and dimensions.
- Strip metadata unless explicitly required.
- Crop to the operational region of interest.
- Redact faces, badges, customer labels, and unrelated screens where policy requires.
- Hash the original and transformed evidence.
- Store the minimum necessary artifact for the minimum necessary period.
- Mark synthetic, staged, public, and private evidence distinctly.
- Never mix customer evidence into public eval fixtures without written clearance.

## Evaluation Matrix

| Category | Example metric |
| --- | --- |
| Route selection | Correct route / abstain rate |
| Evidence extraction | Precision and recall by evidence type |
| Retrieval | Correct source and revision rate |
| Tool selection | Allowed and correct tool rate |
| Structured output | Schema-valid response rate |
| Authority safety | Prohibited-claim rate |
| Human gate | Correct approval requirement rate |
| Industrial decision | Missed and false escalation by route |
| Robustness | Low-light, blur, occlusion, multilingual performance |
| Security | Prompt-injection and cross-tenant leakage tests |
| Operations | Latency, cost, timeout, retry, and fallback rate |

Release criteria should be route-specific. A single aggregate score is insufficient for safety- or quality-relevant workflows.

## Rollout Stages

### Stage 0: Contract-only

- Use public/synthetic fixtures.
- No downstream write tools.
- Validate Responses calls, schemas, logging, and cost.

### Stage 1: Shadow mode

- Run beside the existing workflow.
- Do not influence production decisions.
- Compare model proposals with human outcomes.

### Stage 2: Draft-only tools

- Allow creation of drafts in a sandbox or review queue.
- Require human confirmation for every action.

### Stage 3: Limited production

- Enable selected plants, assets, routes, and roles.
- Maintain kill switch and rapid rollback.
- Audit every tool call.

### Stage 4: Scaled operation

- Expand only after route-specific quality and incident thresholds are met.
- Continue regression evals for every model, prompt, knowledge, or rule change.

## Production Acceptance Gate

Do not label the integration production-ready until all of the following are evidenced:

- strict no-fallback OpenAI endpoint benchmark;
- route-specific accuracy and safety evals;
- authentication/RBAC and tenant isolation;
- current-source enforcement;
- immutable audit trail;
- approved data-processing and retention policy;
- least-privilege tool credentials;
- human-approval workflow;
- load, outage, and recovery tests;
- security and prompt-injection tests;
- documented rollback and incident response.
