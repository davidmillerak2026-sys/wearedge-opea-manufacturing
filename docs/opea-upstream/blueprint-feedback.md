# OPEA Blueprint Feedback Package

This document records the upstream contribution plan for OPEA bonus evidence. It is based on OPEA's public contribution guidance: substantial workflow or user-facing interface changes should start as an RFC issue, and GenAIExamples contributions should include at least a Docker Compose deployment plus an end-to-end test.

## Target Repositories

| Repository | Purpose | WearEdge action |
| --- | --- | --- |
| `opea-project/GenAIExamples` | New example applications and blueprints | Propose `ManufacturingAgentSuite` as a new example |
| `opea-project/GenAIComps` | Reusable microservices and component APIs | Later propose reusable action-card / route registry component if maintainers want it |
| `opea-project/docs` | RFCs, contribution docs, design discussion | Use only if maintainers prefer docs-first RFC |

## Proposed OPEA Example

Name: `ManufacturingAgentSuite`

Purpose: show how enterprise manufacturing teams can build several route-isolated agents behind one Gateway and Megaservice.

Recommended first PR scope:

```text
ManufacturingAgentSuite/
  README.md
  manufacturing_agent_suite.py
  docker_compose/intel/cpu/xeon/compose.yaml
  benchmark/README.md
  tests/test_compose_on_xeon.sh
  assets/flow.md
```

The first PR should stay intentionally small: route registry, Docker Compose, Qdrant profile, deterministic demo path, scorecard, and docs. Helm/GMC can be a follow-up once maintainers accept the blueprint.

## Maintainer Feedback Questions

1. Should route-specific action-card contracts be represented as an example-level pattern or a reusable GenAIComps component?
2. Does OPEA prefer `/v1/agents/{mode}/infer` or a single `/v1/manufacturing/infer` endpoint with `mode` in the body?
3. Should the scorecard map into GenAIEval, or remain an example-local evaluation endpoint?
4. Should plant-system targets such as CMMS/QMS/MES/EHS remain stubbed, or should the blueprint include mock integration services?
5. Is `ManufacturingAgentSuite` an acceptable example name, or should it align to existing OPEA example naming such as `ManufacturingQnA`?

## PR Readiness Checklist

| Item | Status |
| --- | --- |
| RFC issue body prepared | Ready in `docs/opea-upstream/rfc-issue-draft.md` |
| Reference implementation public | Ready at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing` |
| Docker Compose demo | Ready |
| Five route demos | Ready |
| Scorecard endpoint | Ready |
| Qdrant vector DB profile | Ready |
| Intel CPU benchmark harness | Ready in `scripts/intel_cpu_benchmark.py` |
| Upstream issue URL | Posted at `https://github.com/opea-project/GenAIExamples/issues/2461` |
| Upstream PR URL | Pending maintainer feedback |

## Posted Issue Link

The RFC issue has been posted to OPEA GenAIExamples:

```text
https://github.com/opea-project/GenAIExamples/issues/2461
```
