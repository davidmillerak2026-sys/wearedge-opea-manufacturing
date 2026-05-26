# OPEA RFC Issue Draft

Target repository: `opea-project/GenAIExamples`

Posted issue:

```text
https://github.com/opea-project/GenAIExamples/issues/2461
```

Suggested title:

```text
RFC: ManufacturingAgentSuite blueprint for route-isolated industrial action-card agents
```

Suggested labels:

```text
enhancement, example, rfc
```

## Issue Body

### Summary

I would like to propose a new OPEA GenAIExamples blueprint named `ManufacturingAgentSuite`.

The blueprint demonstrates a route-isolated manufacturing agent suite that uses one OPEA-style Gateway and Megaservice to coordinate route-specific Dataprep, Retriever/RAG, Vector DB, LLM, deterministic evaluation, guardrails, and action-card outputs.

The first reference implementation is WearEdge OPEA Manufacturing:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

### Why This Belongs In OPEA

Manufacturing deployments often need more than a single chatbot. A plant-floor assistant must route the same evidence stream to different governed workflows:

| Route | Manufacturing workflow | Output target |
| --- | --- | --- |
| `maintenance` | Predictive maintenance / lao-shi-fu troubleshooting | CMMS work-order draft |
| `iqc` | Incoming and in-process quality control | QMS quality event |
| `changeover` | SKU changeover verification | MES/checklist hold |
| `wi` | Released work-instruction guidance | Work-instruction reference |
| `hazard` | EHS hazard observation | EHS observation/case |

This pattern can help OPEA users understand how to build enterprise agent suites where every route has its own retrieval source, output contract, guardrails, and integration target.

### Proposed Blueprint Shape

```text
ManufacturingAgentSuite/
  README.md
  manufacturing_agent_suite.py
  docker_compose/intel/cpu/xeon/compose.yaml
  benchmark/README.md
  tests/test_compose_on_xeon.sh
  assets/flow.md
```

The blueprint should show:

- Gateway endpoint for `/v1/agents`.
- Route-specific `/v1/agents/{mode}/demo` and `/v1/agents/{mode}/infer`.
- Route registry with fixed input examples and output action-card contracts.
- Dataprep + Retriever/RAG + Vector DB collections isolated by route.
- Guardrails blocking unsupported release, restart, root-cause, and safety-clearance claims.
- A scorecard endpoint that reports latency, contract pass, guardrail pass, RAG/source match, action target correctness, and route isolation.

### OPEA Component Mapping

The reference implementation maps to existing OPEA concepts:

| OPEA concept | Blueprint use |
| --- | --- |
| Gateway | Plant evidence/API entry point |
| Megaservice | Route orchestration and service composition |
| Dataprep | Route-specific manuals, quality plans, policies, and checklists |
| Retriever/RAG | Source-grounded action-card generation |
| Vector DB | Qdrant route collections, with local fallback in the reference package |
| LLM service | Pluggable LLM adapter, deterministic no-model path for CI |
| Guardrails | Blocked claims and human confirmation gates |
| Evaluation | Deterministic route scorecard |

### Reference Validation

The reference repository currently supports:

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

Expected route registry:

```text
maintenance, iqc, changeover, wi, hazard
```

### Requested Feedback

I would appreciate maintainer feedback on:

- Whether this should be contributed as a new `GenAIExamples/ManufacturingAgentSuite` example.
- Whether route-isolated guardrails and action-card contracts belong in GenAIExamples or GenAIComps.
- Whether OPEA would prefer a minimal Docker Compose-only blueprint first, with Helm/GMC support added in a follow-up PR.
- Naming guidance for the example and route registry endpoints.

### Follow-Up PR Plan

If maintainers agree, I can prepare a PR with:

- Minimal Docker Compose deployment.
- README and architecture diagram.
- Five sample manufacturing routes.
- Deterministic CI-friendly demo mode.
- Qdrant vector DB profile.
- Scorecard endpoint and E2E test.
