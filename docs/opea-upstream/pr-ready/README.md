# PR-Ready OPEA Contribution Package

This directory contains a minimal, docs-first contribution package prepared for
`opea-project/GenAIExamples`.

It is not a replacement for the full WearEdge competition repository. It is a
small first-PR candidate that maintainers can review quickly:

```text
ManufacturingAgentSuite/
  README.md
  manufacturing_agent_suite.py
  docker_compose/intel/cpu/xeon/README.md
  docker_compose/intel/cpu/xeon/compose.yaml
  docker_compose/intel/cpu/xeon/compose.opea-tei.yaml
  benchmark/README.md
  tests/test_compose_on_xeon.sh
  assets/flow.md
```

## Intended Upstream Use

Copy `ManufacturingAgentSuite/` to the root of a fork of
`opea-project/GenAIExamples`, then open a PR that references:

- RFC issue: https://github.com/opea-project/GenAIExamples/issues/2461
- TEI update comment: https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017
- Reference implementation: https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing

## Boundary

The package deliberately avoids production LLM claims. It proves the example
shape, route contracts, guardrails, scorecard, Docker Compose entry point, and
official OPEA TEI wiring pattern. Production LLM/Helm/GMC can be follow-up PRs.

## Local Validation

Validated on 2026-05-27 from this repository root:

- Python syntax parse passed for `ManufacturingAgentSuite/manufacturing_agent_suite.py`.
- Local service smoke passed for `/healthz`, `/v1/agents`, five
  `/v1/agents/{mode}/demo` routes, five `/v1/agents/{mode}/infer` routes, and
  `/v1/scorecard`.
- `docker-compose -f ManufacturingAgentSuite/docker_compose/intel/cpu/xeon/compose.yaml config`
  passed.
- `docker-compose -f ManufacturingAgentSuite/docker_compose/intel/cpu/xeon/compose.yaml -f ManufacturingAgentSuite/docker_compose/intel/cpu/xeon/compose.opea-tei.yaml config`
  passed.
