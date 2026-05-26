# WearEdge Pro: Five Manufacturing Agents On One OPEA-Aligned Architecture

WearEdge Pro started from a simple manufacturing question: what if the most useful AI assistant on a factory floor is not a generic chatbot, but a governed action-card system that understands which workflow it is helping?

In a real plant, the same first-person evidence can mean very different things. A gearbox vibration observation belongs to maintenance. A scratch on an aluminum housing belongs to quality. A label-roll mismatch during SKU changeover belongs to MES or a changeover checklist. A question about a cartoner guide rail belongs to a released work instruction. A blocked walkway or exposed moving part belongs to EHS.

That is why the OPEA Manufacturing version of WearEdge Pro is built as a five-agent suite:

| Agent route | Workflow | Output |
| --- | --- | --- |
| `maintenance` | Lao-shi-fu predictive maintenance | CMMS work-order draft |
| `iqc` | Incoming and in-process quality control | QMS quality event |
| `changeover` | SKU changeover verification | MES/checklist hold |
| `wi` | Released work-instruction guidance | Work-instruction reference |
| `hazard` | EHS hazard observation | EHS action card |

The key idea is route isolation. Every route has its own source evidence, retrieval scope, evaluator, blocked claims, owner, and integration target. A maintenance route should not issue safety clearance. A hazard route should not write a final root cause. A quality route should not release product without human disposition.

## Architecture

WearEdge OPEA Manufacturing uses one platform architecture:

```text
M400 or API request
  -> Gateway
  -> Manufacturing Megaservice
  -> route registry
  -> Dataprep
  -> Retriever/RAG
  -> Qdrant vector DB profile
  -> LLM adapter
  -> deterministic evaluator
  -> Guardrails
  -> bounded action card
```

This maps naturally to OPEA concepts: Gateway, Megaservice, Dataprep, Retriever/RAG, Vector DB, LLM service, Guardrails, and Evaluation. The submitted repository keeps a deterministic no-model path so judges and maintainers can run the full suite without pulling a large model, while the architecture remains compatible with a production LLM service.

## Why Five Agents Matter

Manufacturing AI value does not come from one isolated demo. The enterprise value comes from covering several loss pools with the same governed platform:

- Downtime through maintenance triage.
- Scrap and rework through quality holds.
- Changeover loss through checklist verification.
- Training and procedure drift through released work instructions.
- Safety risk through EHS observations.

The same API shape supports all five:

```bash
GET  /v1/agents
GET  /v1/agents/{mode}/demo
POST /v1/agents/{mode}/infer
GET  /v1/scorecard
```

The scorecard reports route-level latency, action-card contract pass, guardrail pass, source match, action target correctness, and route isolation.

## Guardrails Are The Product

In manufacturing, a confident wrong answer is worse than no answer. WearEdge Pro does not claim final root cause, restart permission, quality release, safety clearance, or maintenance release. Instead it creates auditable action cards with source IDs and human-confirmation gates.

That design choice is practical. It lets an AI assistant help technicians, operators, quality engineers, and supervisors move faster without pretending to be a certified release controller.

## Open Source Package

The OPEA submission package is public:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

It includes Docker Compose, Qdrant, five sample requests, route-specific knowledge sources, a FastAPI gateway, a scorecard endpoint, tests, OPEA component mapping, and a draft upstream blueprint proposal for the OPEA community.

## What Comes Next

The next hardening steps are:

- Publish an OPEA RFC issue proposing a `ManufacturingAgentSuite` blueprint.
- Add a production embedding microservice profile.
- Run the benchmark harness on Intel Xeon hardware with AVX-512 and AMX.
- Add a short demo video showing all five agents in less than three minutes.

WearEdge Pro's position is simple: the best plant-floor AI systems will be source-grounded, route-aware, human-confirmed, and measured. That is the shape this OPEA Manufacturing suite is trying to make concrete.
