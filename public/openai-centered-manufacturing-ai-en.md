# Do Not Let the Model Run the Factory: An OpenAI-Centered Architecture for Wearable Manufacturing AI

> Industrial glasses can capture the evidence. OpenAI can understand and orchestrate it. Deterministic controls and accountable people must still authorize the decision.

## Executive summary

Manufacturing does not need another general-purpose chatbot. It needs a dependable way to turn frontline evidence into traceable, reviewable actions that enter the right enterprise workflow.

WearEdge Pro is built around that problem. A Vuzix M400 or API client captures first-person observations. A unified manufacturing agent platform then identifies one of five routes, retrieves released plant knowledge, applies deterministic checks, enforces route-specific guardrails, and produces a bounded action card for maintenance, quality, changeover, work instructions, or EHS.

The public repository already implements an OPEA-aligned five-agent suite, Qdrant RAG, TEI embedding profiles, deterministic evaluators, guardrails, and an OpenAI-compatible model boundary. The next step should not be a rewrite. It should be a native OpenAI layer placed inside the existing control architecture:

- image and text understanding for M400 evidence;
- the Responses API for reasoning and orchestration;
- strict function calling for approved plant-system tools;
- Structured Outputs for machine-verifiable action cards;
- continuous evaluations for route accuracy, evidence grounding, abstention, and authority boundaries.

The governing principle is simple:

> OpenAI interprets and orchestrates. Industrial rules adjudicate. Humans authorize.

---

## 1. The “last ten meters” of manufacturing information

Operators and experienced technicians often notice a problem before CMMS, MES, QMS, or ERP does:

- a gearbox sounds or vibrates differently;
- a label, part, or surface defect is visible;
- a changeover confirmation is incomplete;
- the active work instruction is unclear;
- PPE is missing, a walkway is blocked, or moving parts are exposed.

The hard problem is not merely recognizing an image. It is linking the observation to the correct asset, released knowledge revision, risk rule, responsible owner, and enterprise workflow.

WearEdge Pro therefore models five isolated routes rather than one universal assistant:

| Route | Operational question | Integration target |
| --- | --- | --- |
| `maintenance` | Does the equipment condition require maintenance escalation? | `maintenance_work_order` |
| `iqc` | Does defect evidence require quality containment or review? | `qms_quality_event` |
| `changeover` | Is the changeover evidence ready for human sign-off? | `changeover_checklist` |
| `wi` | Which released work instruction applies? | `wi_reference` |
| `hazard` | Does the visible condition require stop, correction, or EHS reporting? | `ehs_case` |

Each route has a different owner, data contract, source, human gate, and list of prohibited claims. A maintenance route cannot grant safety clearance. A quality route cannot release a lot. A changeover route cannot authorize restart. A hazard route cannot invent the final incident root cause.

## 2. Where OpenAI belongs in the architecture

A fragile design sends an image, sensor values, and a broad prompt directly to a model and accepts whatever recommendation comes back. That is fast to demonstrate but difficult to govern: formats drift, source revisions disappear, permissions become ambiguous, and outputs are hard to audit.

A stronger OpenAI-centered architecture looks like this:

```text
M400 image / operator speech or text / equipment signals
  -> edge redaction, compression, and asset identity check
  -> WearEdge Gateway
  -> five-route registry and request contracts
  -> TEI / Qdrant route-specific retrieval
  -> OpenAI Responses API
       - image and language understanding
       - evidence-grounded explanation
       - strict tool selection
       - structured action proposal
  -> deterministic industrial evaluator
  -> guardrails and prohibited claims
  -> human approval
  -> CMMS / QMS / MES / WI / EHS
  -> audit and evaluation records
```

OpenAI becomes the reasoning and orchestration core, not the factory authority core.

### Multimodal evidence understanding

An image-capable model can combine first-person images with operator language to identify visible labels, gauges, PPE, obstructions, defects, or equipment context. The result should be structured evidence—not an unbounded final decision.

### Grounded explanations

The model should explain the condition only from retrieved equipment thresholds, quality plans, changeover checklists, released work instructions, or EHS policies. Source IDs and revision identifiers must survive into the output.

### Strict tool calling

Approved actions—draft a maintenance work order, draft a quality event, request first-piece sign-off, open a released work instruction, or create an EHS observation—should be exposed as narrowly scoped functions. Each tool should use a strict JSON Schema, require every field, and reject additional properties.

### Structured action cards

The model should return a contract, not prose alone: route, asset, evidence, source IDs, risk, proposed action, owner, human-confirmation requirement, prohibited claims, and target system. Deterministic code validates the object again before any downstream write.

## 3. Why deterministic evaluators must remain

Large models are useful for interpreting ambiguous evidence. They should not replace industrial thresholds or workflow gates.

The current WearEdge implementation explicitly checks:

- vibration, gearbox temperature, bearing temperature, lubrication interval, and PLC alarms for maintenance;
- detector confidence against a released quality-plan threshold for IQC;
- line clearance, label-roll match, recipe match, and first-piece verification for changeover;
- equipment identity, released revision, guard state, and active alarms for work instructions;
- moving-parts exposure, blocked walkways, and missing PPE for hazards.

Those checks are testable code. OpenAI can explain why a combination of signals is concerning, but it must not silently alter a threshold or waive a missing confirmation.

A production decision should therefore use two layers:

1. **Model layer:** recognize evidence, select a candidate route, extract fields, explain the reasoning, and propose an allowed tool.
2. **Industrial control layer:** verify asset identity, knowledge revision, thresholds, permissions, required evidence, and approval status.

Any disagreement should fail closed into human review.

## 4. Five business views of the same platform

### Maintenance: preserve expertise without fabricating root cause

Experienced technicians recognize weak signals such as unusual noise, visible shaking, or a burnt-oil smell. Multimodal reasoning can combine those observations with sensor values and maintenance knowledge to prepare an escalation.

The system may say “high-risk condition; prepare a human-confirmed work-order proposal.” It must not declare final root cause, remaining useful life, restart permission, or maintenance release.

### Quality: turn visual evidence into a traceable QMS event

The product value is not only drawing a defect box. It is preserving product identity, lot window, defect type, confidence, quality-plan revision, image source, and disposition owner. OpenAI can organize mixed visual and textual evidence; deterministic quality rules decide when to expand inspection or create a hold proposal.

Final release remains with authorized quality personnel.

### Changeover: reduce mix-ups and unsafe restart

Changeover failure is often a missing confirmation rather than a single recognition error. AI can gather evidence from images, scans, checklists, and operator dialogue and assemble a sign-off package. A missing first-piece confirmation must continue to block restart authorization.

### Work instructions: bring released knowledge to the operator

The goal is not to let the model invent a procedure. It is to locate the currently released instruction for the identified machine and product and explain it clearly. The system should stop when identity is uncertain, the revision is not confirmed, a guard is open, or an alarm is active.

### Safety: improve observation and reporting without granting clearance

Vision models can help detect visible PPE, walkway, and moving-parts risks and package the evidence into an EHS observation. They cannot declare an area safe or replace lockout/tagout, formal risk assessment, or accountable sign-off.

## 5. What is already real—and what is not

The public repository is technically credible as a reproducible industrial-agent prototype:

- a FastAPI browser/API gateway;
- five isolated route contracts;
- in-memory and Qdrant vector-store paths;
- optional OPEA-compatible and official OPEA TEI embedding profiles;
- an OpenAI-compatible Chat Completions adapter plus deterministic default;
- route-specific deterministic evaluators and guardrails;
- scorecards and committed evaluation evidence.

It is important to describe the current OpenAI status precisely. The runtime is OpenAI-compatible, but the reviewed repository is not yet OpenAI-native. It uses a Chat Completions-shaped HTTP adapter, defaults to a deterministic template, does not depend on the official OpenAI SDK, and does not contain reviewed evidence of a benchmark against an actual OpenAI model endpoint.

The native OpenAI design in this article is therefore a concrete upgrade path, not a claim that the current public package already runs production workflows on OpenAI.

## 6. Reading the benchmark evidence honestly

The committed lightweight route evaluation reports 15 of 15 cases passing across contract, target, channel, risk, human gate, guardrail, RAG-source, and route-isolation checks.

A committed deterministic benchmark records 300 calls at approximately 249.6 calls per second, with about 3.99 ms mean latency and 6.14 ms p95 latency. A small official OPEA GenAIEval `chatqnafixed` compatibility run also records zero failures for runs of 1, 5, and 10 requests.

These figures demonstrate fast, repeatable execution of small public fixtures and deterministic code paths. They are not OpenAI model latency, full image-inference throughput, an independent safety score, or a production-factory SLA.

After an OpenAI integration, measurements should be separated into:

- edge capture and upload time;
- retrieval and reranking time;
- model first-token and full-response latency;
- tool-execution time;
- deterministic validation and human approval time;
- quality, cost, and failure rate per route;
- recovery behavior under low bandwidth, no network, or model outage.

## 7. Production gaps that matter more than a better prompt

### Identity and access

Add authentication, RBAC, plant and tenant isolation, service identities, and least-privilege credentials. A model tool must never hold a universal token that can act across every plant and asset.

### Data governance

Plant images may contain people, proprietary process details, customer labels, or trade secrets. Redact and classify evidence at the edge, define retention and regional-processing rules, and log every access. OpenAI offers enterprise/API data controls, including default non-training of business data, but each manufacturer still owns the governance of collection, transfer, storage, and downstream use.

### Reliability

Use strict request schemas, size limits, timeouts, retries, circuit breakers, idempotency keys, and explicit degraded states. Silent vector-store or model fallbacks may be convenient for a demo; a production workflow should report “degraded” or “unable to determine” instead of masking an outage.

### Auditability

Every action card should trace back to an evidence hash, asset identity, source revision, model and prompt version, tool calls, deterministic checks, human approval, and downstream write result.

### Evaluation

Test more than format compliance: missed escalation, false escalation, wrong route, wrong tool, unsupported authority, missing sources, abstention, multilingual operation, poor image quality, stale knowledge, and prompt injection. Results should be segmented by plant, equipment family, route, and model version.

## 8. What customers actually pay for

Manufacturers do not sustain a product because it “can chat.” They pay for measurable workflow outcomes:

- shorter time from anomaly discovery to a work-order proposal;
- shorter time from defect evidence to lot containment;
- fewer missed changeover confirmations and incorrect restarts;
- faster access to the correct released instruction;
- a higher percentage of near misses recorded and closed;
- broader reuse of expert troubleshooting knowledge.

OpenAI is the capability engine. WearEdge’s durable product assets are the device integration, route contracts, plant knowledge, deterministic checks, guardrails, approvals, audit trail, and enterprise-system connectors.

## 9. A practical OpenAI-native roadmap

### Phase 1: replace only the explanation layer

- Add a Responses API adapter.
- Preserve the current RAG, evaluators, guardrails, and action-card contract.
- Run strict no-fallback tests across all five routes.
- Track model quality, latency, and cost separately.

### Phase 2: introduce multimodal evidence

- Build a cleared and redacted image benchmark.
- Extract structured evidence from image inputs.
- Test low light, blur, occlusion, varied viewpoints, and multiple languages.
- Route low-confidence or unidentified scenes to human review.

### Phase 3: use strict tools and Structured Outputs

- Define least-privilege CMMS, QMS, MES, WI, and EHS tools.
- Enable strict function schemas.
- Require a fixed action-card JSON contract.
- Validate in a sandbox before allowing production writes.
- Require signed human approval for high-risk actions.

### Phase 4: operate with continuous evaluation and governance

- Run regression evals for every model, prompt, knowledge, or rule change.
- Red-team missed hazards, false holds, wrong tools, and authority violations.
- Maintain quality dashboards by plant and route.
- Keep an operational kill switch for model-initiated writes.

## Conclusion

The right question for OpenAI in manufacturing is not whether a model can sound like an engineer. It is whether the system can transform frontline evidence into an action that has a source, a contract, a boundary, and an accountable owner—and then stop at the exact point where human authority is required.

WearEdge Pro offers a strong foundation for that pattern: wearable devices observe the plant; OPEA and RAG organize knowledge; OpenAI provides multimodal understanding, reasoning, and tool orchestration; deterministic code enforces industrial gates; guardrails prevent authority overreach; and humans approve the consequential action.

That is not a model running the factory. It is a factory seeing problems sooner, preserving evidence more completely, and executing workflows more consistently.

---

## Project and references

- Repository: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing`
- Repository verification: `docs/repository-verification-2026-06-18.md`
- OpenAI Responses API: `https://platform.openai.com/docs/api-reference/responses`
- OpenAI Function Calling: `https://platform.openai.com/docs/guides/function-calling`
- OpenAI Images and Vision: `https://platform.openai.com/docs/guides/images-vision`
- OpenAI Evaluation best practices: `https://platform.openai.com/docs/guides/evaluation-best-practices`
- OpenAI Enterprise Privacy: `https://openai.com/enterprise-privacy/`

## Suggested metadata

- **Subtitle:** From M400 frontline evidence and TEI/Qdrant RAG to OpenAI Responses, strict tools, deterministic industrial controls, and human approval
- **Tags:** OpenAI, Manufacturing AI, Industrial Agents, Edge AI, OPEA, RAG, Qdrant, AI Safety, Digital Transformation
- **Canonical recommendation:** Use the merged GitHub English article as canonical and retain the canonical/project links on syndicated platforms
