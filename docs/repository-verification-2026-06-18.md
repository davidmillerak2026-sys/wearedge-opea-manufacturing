# Repository Verification: WearEdge OPEA Manufacturing

Date: 2026-06-18

## Scope

This review covers the public repository's product positioning, core Python runtime, Docker/OPEA profiles, route contracts, guardrails, evaluation artifacts, benchmark summaries, data-provenance statements, and existing publication records. The review is a static source-and-evidence audit of the public repository; it is not an independent factory acceptance test, penetration test, safety certification, or re-run of every benchmark.

Reviewed representative paths include:

- `README.md`, `PROJECT_OVERVIEW.md`, `TECHNICAL_REPORT.md`;
- `src/wear_edge_opea/gateway.py`, `agents.py`, `megaservice.py`, `retriever.py`, `vector_store.py`, `embedding.py`, `evaluator.py`, `guardrails.py`, `llm_adapter.py`, and `scorecard.py`;
- `docker-compose.yml`, `docker-compose.opea.yml`, and `docker-compose.opea-tei.yml`;
- `evidence/genaieval/summary.md`, `benchmark_results.json`, and `official_benchmark_summary.json`;
- `docs/product-risk-burn-down.md`, `docs/production-llm-benchmark-path.md`, `docs/publication-record.md`, and `docs/public-platform-publishing-handoff.md`.

## Verified Product Shape

WearEdge Pro is presented as a Docker-runnable, OPEA-aligned manufacturing agent suite rather than an Android-only demo. The public package exposes a FastAPI browser console and API on port `8088`, with Qdrant as the Docker vector-store profile and a dependency-light in-memory fallback.

The runtime implements five bounded routes:

| Route | Operational decision | Integration target |
| --- | --- | --- |
| `maintenance` | Convert equipment-condition evidence into a maintenance proposal | `maintenance_work_order` |
| `iqc` | Convert defect evidence into a quality hold/review event | `qms_quality_event` |
| `changeover` | Gate changeover evidence before human sign-off | `changeover_checklist` |
| `wi` | Retrieve released work-instruction guidance | `wi_reference` |
| `hazard` | Convert visible hazards into an EHS action | `ehs_case` |

The common flow is:

```text
M400/API evidence
  -> FastAPI Gateway
  -> Manufacturing Megaservice
  -> route-specific knowledge source
  -> Retriever/RAG
  -> in-memory or Qdrant vector store
  -> optional embedding service
  -> LLM explanation adapter or deterministic template
  -> deterministic route evaluator
  -> guardrails
  -> bounded action card
```

## What Is Implemented Well

1. **Route isolation is explicit.** Each route has a different business owner, target system, human gate, knowledge source, and blocked claims.
2. **Safety authority is bounded.** The system blocks claims such as restart permission, quality release, safety clearance, final root cause, remaining useful life, and maintenance release.
3. **The model is not the control plane.** Deterministic checks and action-card contracts remain outside the LLM boundary.
4. **Reproducibility is prioritized.** The default path runs without model credentials, while optional Qdrant, OPEA embedding, TEI, reranker, and external LLM profiles can be added.
5. **Evidence is separated from claims.** The documentation repeatedly distinguishes public sanitized fixtures, private production-data lineage, local-model evidence, external endpoint evidence, and unmerged upstream work.

## Evaluation Evidence Verified

The committed lightweight route-evaluation summary reports `15/15` cases passing across contract, action-target, channel, risk, human-gate, guardrail, RAG-source, and route-isolation checks.

The committed deterministic benchmark reports:

- 300 total route calls;
- about `249.6` calls/second in that local run;
- mean latency about `3.99 ms`;
- p95 latency about `6.14 ms`;
- all cases passing.

These numbers measure the local deterministic route runner and its small fixtures. They must not be represented as OpenAI model latency, production plant throughput, or an independent safety score.

The repository also records a small official OPEA GenAIEval `chatqnafixed` endpoint run with 1, 5, and 10 requests and zero failures. This is useful compatibility evidence, but it is not a large-scale load test.

## OpenAI Status: Accurate Claim Boundary

The repository is **OpenAI-compatible**, but it is not yet an OpenAI-native implementation.

Verified current state:

- `llm_adapter.py` can call an OpenAI-compatible `/v1/chat/completions` endpoint.
- The default backend is a deterministic in-process template.
- The runtime uses Python `urllib` rather than the official OpenAI SDK.
- `requirements.txt` does not include the `openai` package.
- The committed documentation includes strict local Gemma and DeepSeek-compatible endpoint evidence.
- No committed artifact reviewed in this audit proves a production benchmark against an actual OpenAI model endpoint.

Therefore, safe wording is:

> WearEdge Pro has an OpenAI-compatible LLM boundary and a clear path to an OpenAI-centered manufacturing architecture.

Unsafe wording is:

> WearEdge Pro is already running its production manufacturing workflow on OpenAI.

The accompanying technology article deliberately presents OpenAI Responses, vision, strict function calling, structured outputs, and evaluation as the **next native integration layer**, while preserving the repository's current deterministic evaluator and guardrail boundaries.

## Priority Gaps Before Production

### P0: Security and plant governance

- Add authentication, RBAC, tenant/plant isolation, and service-to-service identity.
- Replace untyped `dict` request bodies with strict Pydantic schemas and size limits.
- Add rate limits, request timeouts, retries, circuit breakers, and idempotency keys.
- Protect Qdrant and internal embedding endpoints from direct public exposure.
- Add immutable audit events for input evidence, retrieved sources, model/tool calls, approvals, and downstream actions.
- Define redaction, retention, regional processing, and data-classification policies for plant images and identifiers.

### P0: Operational safety

- Keep restart, release, safety clearance, and final disposition outside model authority.
- Require signed human approvals for high-risk action cards.
- Add fail-closed behavior for missing identity, stale knowledge revisions, tool errors, and source mismatches.
- Validate downstream CMMS/QMS/MES/EHS actions in a sandbox before production write access.

### P1: OpenAI-native engineering

- Add a Responses API adapter instead of relying only on Chat Completions compatibility.
- Use image inputs for M400 evidence where plant policy permits.
- Represent CMMS/QMS/MES/EHS actions as strict function tools with `additionalProperties: false` and all fields required.
- Return action cards through Structured Outputs rather than free-form parsing.
- Add model-specific eval sets for false escalation, missed escalation, unsupported authority claims, source citation, tool selection, and abstention.
- Record cost, latency, fallback, and quality metrics separately for every route and model version.

### P1: Reproducibility and dependency hygiene

- Pin Python dependencies and avoid floating `latest` container tags in production.
- Add software-bill-of-materials, image signing, vulnerability scanning, and dependency update policy.
- Make silent vector-store and LLM fallback behavior visible as degraded status; production should not quietly mask an outage.

## Publication Guidance

The strongest public story is not “a chatbot for factories.” It is:

> A bounded manufacturing decision-support system that combines wearable evidence, route-specific retrieval, deterministic industrial checks, human gates, and an OpenAI-centered reasoning/tool layer without delegating safety or release authority to the model.

## Final Verification Position

The repository is technically credible as a reproducible industrial-agent prototype with unusually clear route boundaries and claim controls. Its strongest differentiation is the combination of wearable/edge evidence lineage, five plant workflows, OPEA modularity, and bounded action cards.

For an OpenAI-centered release, the honest next step is an additive native integration—not a rewrite: use OpenAI for multimodal understanding, grounded explanation, and strict tool selection, while retaining deterministic evaluators, source revision checks, guardrails, and human approvals as the manufacturing control boundary.
