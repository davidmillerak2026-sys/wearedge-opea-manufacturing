# Building an OPEA Manufacturing Five-Agent Suite: TEI, Qdrant, Guardrails, and What We Would Feed Back to OPEA

WearEdge Pro is a real industrial AI agent system for frontline manufacturing.
For the OPEA ecosystem, we packaged the product into a reproducible
OPEA-aligned manufacturing suite that evaluators can run without private factory
data, M400 hardware, or large local VLM model weights.

The important design choice was separation of concerns:

- WearEdge-Pro remains the broader product repository for M400, Jetson, real
  edge VLM evidence, Android client work, and field workflow history.
- `wearedge-opea-manufacturing` is the public OPEA package:
  one-click Docker, Gateway, Megaservice, official TEI embeddings, Qdrant RAG,
  five manufacturing routes, guardrails, scorecard, and evaluation evidence.

## Architecture

```text
M400/API evidence
  -> Gateway
  -> Manufacturing Megaservice
  -> route registry: maintenance / iqc / changeover / wi / hazard
  -> Dataprep
  -> official OPEA TEI embedding microservice
  -> Qdrant vector store
  -> Retriever/RAG
  -> LLM adapter boundary
  -> deterministic evaluator
  -> route-specific guardrails
  -> action card for CMMS/QMS/MES/WI/EHS
  -> scorecard and GenAIEval-compatible metrics
```

The default path is intentionally reproducible. An evaluator can run it on a normal
CPU machine and inspect every route without secrets. The production product
path is deeper: WearEdge-Pro has already run a Jetson edge VLM flow with
Gemma 4 E2B + `mmproj-F16` through a FastAPI gateway and M400-style image
evidence.

That is the OPEA value point we want to make explicit: Gateway, Megaservice,
Retriever/RAG, Vector DB, LLM adapter, Evaluator, and Guardrails are modular
parts of the system. The model is only the replaceable component behind the
adapter. Local Gemma, Gemini, or an enterprise OpenAI-compatible endpoint can
change, but route isolation, source grounding, deterministic checks, blocked
claims, human-confirmation gates, and action-card contracts remain stable.

## Why TEI + Qdrant

OPEA is strongest when the system is visibly composable. We therefore avoided
burying retrieval inside one application process. The official TEI profile has
four distinct services:

```text
manufacturing-gateway
qdrant
opea/embedding:latest
ghcr.io/huggingface/text-embeddings-inference:cpu-latest
```

That makes the retrieval path auditable:

- TEI serves `BAAI/bge-base-en-v1.5`;
- the OPEA embedding microservice exposes `/v1/embeddings`;
- the gateway indexes route-specific knowledge into Qdrant;
- each action card preserves source IDs from retrieved evidence.

For a manufacturing workflow, source IDs are not decoration. They are how a
technician, quality engineer, operator, or EHS owner can tell whether the model
was grounded in an approved maintenance KB, quality plan, released work
instruction, changeover checklist, or safety policy.

## Five Routes, One OPEA Pattern

| Route | Industrial decision | Integration target |
| --- | --- | --- |
| `maintenance` | High-risk gearbox condition and work-order proposal | `maintenance_work_order` |
| `iqc` | Defect evidence and QMS hold event | `qms_quality_event` |
| `changeover` | SKU changeover checklist gating | `changeover_checklist` |
| `wi` | Released work-instruction guidance | `wi_reference` |
| `hazard` | Stop-and-make-safe EHS observation | `ehs_case` |

The platform value is not that we wrote five prompts. The platform value is
that the same OPEA-style chain handles five different plant decisions while
keeping each route isolated.

Route isolation matters. A maintenance request must not issue EHS clearance. A
hazard route must not invent a root cause. An IQC route must not release
quality. The route boundary is part of the architecture, not just wording in a
prompt.

## Guardrails We Actually Needed

| Route | Blocked claims |
| --- | --- |
| `maintenance` | final root cause, remaining useful life, restart permission, maintenance release |
| `iqc` | quality release, final disposition, customer acceptance, measurement certification |
| `changeover` | restart permission, quality release, recipe release, first-piece release |
| `wi` | unreleased instruction, bypass interlock, quality release, restart permission |
| `hazard` | area safe, restart permission, safety clearance, incident root cause |

These guardrails changed the product shape. The system does not try to sound
like a supervisor. It creates bounded action cards with source IDs, owners,
priorities, integration targets, and human confirmation flags.

That is the difference between a manufacturing assistant and an unsafe chatbot.

## Real VLM Evidence vs Reproducible OPEA Package

The source WearEdge-Pro system has a real edge VLM path:

```text
M400/browser image
  -> WearEdge-Pro /v1/infer
  -> llama.cpp /v1/chat/completions
  -> Gemma 4 E2B Q4_K_S + mmproj-F16
  -> output contract
  -> agent loop
  -> action card and audit log
```

Archived source evidence includes:

- a 3.17 MB industrial JPEG running through Gemma 4 E2B in 5.824 s;
- an autostart browser run in 8.734 s;
- a full five-agent real gateway summary with 6/6 cases passed;
- a lao-shi-fu maintenance evidence loop where oil leakage, burnt-oil smell,
  visible shaking, and gearbox noise routed to a critical maintenance action.

For the OPEA repository, we did not dump private images or large GGUF model
files. Instead, we mapped the real VLM evidence and made the public OPEA path
fully runnable. We also added a strict public oil-leak LMM benchmark harness:
it calls a real image-capable endpoint, parses maintenance evidence, and feeds
that into the OPEA action-card pipeline with no fallback.

The model story is deliberately not locked to one provider. The local
Jetson/Gemma 4 E2B path proves WearEdge is not a cloud-wrapper. The
external LMM benchmark path proves the same five-agent OPEA pipeline can also
attach to Gemini or any OpenAI/OPEA-compatible image endpoint through a strict
adapter boundary. Edge models serve privacy-sensitive or offline factory
deployments; external model APIs serve cloud-augmented reasoning and enterprise
model-service replacement.

## Evaluation

The scorecard checks every route for:

- latency;
- contract pass;
- guardrail pass;
- RAG/source match;
- action target correctness;
- route isolation.

We also added a lightweight GenAIEval-compatible pack with a JSONL dataset,
route evaluator, benchmark runner, and generated summary. It does not pretend
to be the official GenAIEval/RAGAS/AutoRAG stack, but it makes the
evaluation method visible and repeatable.

## Hardware Evidence

The OPEA TEI profile passed on Google Cloud C3 `c3-standard-4`:

```text
4 vCPU
16 GiB RAM
no GPU
Intel Xeon Platinum 8481C
AVX-512 and AMX flags detected
```

The profile ran official TEI embeddings, OPEA embedding wrapper, Qdrant, the
gateway, five sample routes, and scorecard. We also added a follow-up Cloud Shell
script that enables `ONEDNN_VERBOSE`, `DNNL_VERBOSE`, and `MKLDNN_VERBOSE`,
then captures TEI/OPEA logs and searches for oneDNN/ISA markers. If the logs
do not emit dispatch details, the artifact says so instead of over-claiming.

## What We Would Suggest to OPEA

After building this, our feedback to OPEA is concrete:

1. Add a Manufacturing Agent Suite blueprint.
2. Include route-isolation and action-card guardrail examples in GenAIExamples.
3. Provide an official TEI + Qdrant Compose reference for CPU-only enterprise
   deployments.
4. Add GenAIEval-compatible examples for action-card correctness, guardrail
   pass/fail, and source-ID preservation.
5. Publish a hardware evidence template that distinguishes CPU feature flags,
   application-level performance, and actual oneDNN/AMX kernel dispatch logs.

OPEA is a strong fit for enterprise manufacturing because it encourages
component boundaries: embedding service, vector DB, gateway, megaservice,
evaluation, and deployment profile. The next useful step is more domain
blueprints with real operational guardrails, not only generic chat examples.

## Closing

The system we released is not an Android-only sample and not a single
maintenance prompt. It is a manufacturing agent suite: five bounded industrial
routes, official OPEA TEI embeddings, Qdrant RAG, route-specific guardrails,
action-card contracts, scorecard evidence, and a mapped real VLM product path
from WearEdge-Pro.

That combination is what makes it enterprise-shaped: reproducible enough for
evaluators, grounded enough for operators, and honest enough for industrial use.
