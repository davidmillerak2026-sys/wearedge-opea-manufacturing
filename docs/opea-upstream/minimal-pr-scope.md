# Minimal OPEA PR Scope

This is the proposed first PR shape for `opea-project/GenAIExamples` once
maintainers confirm the preferred location and naming from RFC issue #2461.

Status: PR-ready package prepared and locally smoke-tested in
`docs/opea-upstream/pr-ready/ManufacturingAgentSuite/`.

## Proposed Path

```text
ManufacturingAgentSuite/
  README.md
  manufacturing_agent_suite.py
  docker_compose/intel/cpu/xeon/compose.yaml
  docker_compose/intel/cpu/xeon/compose.opea-tei.yaml
  benchmark/README.md
  tests/test_compose_on_xeon.sh
  assets/flow.md
```

## First PR Boundary

The first PR should remain deliberately small:

- Route registry for `maintenance`, `iqc`, `changeover`, `wi`, and `hazard`.
- Deterministic demo path that does not require downloading an LLM.
- Qdrant vector DB profile, with clear environment variables.
- Optional official OPEA TEI embedding profile using `TEI_EMBEDDING_ENDPOINT` and `EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`.
- `/v1/agents`, `/v1/agents/{mode}/demo`, `/v1/agents/{mode}/infer`, and `/v1/scorecard`.
- Guardrails that block final root cause, restart permission, maintenance release, quality release, area safe, and safety clearance claims.
- A runnable Docker Compose profile and a smoke/E2E test.

## Follow-Up PRs

After maintainers accept the example shape:

- Add production LLM service profile.
- Add Helm/GMC deployment.
- Decide whether reusable route registry, action-card contract, and guardrail checks belong in `GenAIComps`.
- Add Intel Xeon AVX-512/AMX benchmark results from a cloud host.

## Prepared Artifact

The current repository includes a copyable upstream artifact at:

```text
docs/opea-upstream/pr-ready/ManufacturingAgentSuite/
```

It has been validated locally with:

```text
Python syntax parse: pass
HTTP smoke: /healthz, five agents, five demos, five infers, scorecard pass
docker-compose base config: pass
docker-compose official TEI config: pass
```

The package is intentionally smaller than the competition repository so OPEA
maintainers can review the example shape first, then decide whether production
LLM, Helm/GMC, or reusable GenAIComps pieces should move into later PRs.
