# OPEA Implementation Feedback Comment

Target issue:

```text
https://github.com/opea-project/GenAIExamples/issues/2461
```

Status: posted to the upstream OPEA issue on 2026-05-27:

```text
https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4551375202
```

GitHub App write permission to the upstream OPEA repository is not available in
this environment; the authoritative upstream comment was posted through a
user-authenticated GitHub browser session.

## Comment Body

Implementation update for the proposed `ManufacturingAgentSuite` blueprint:

The reference package is now more judge- and maintainer-friendly. It includes a browser demo console in addition to the API endpoints, so reviewers can inspect route selection, sample requests, RAG evidence, bounded action cards, blocked claims, and the five-route scorecard without writing curl commands.

Reference implementation:
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing

Runnable entry point after `docker compose up --build -d`:

```text
http://127.0.0.1:8088/demo
```

Current validation status:

- `GET /v1/agents` returns `maintenance`, `iqc`, `changeover`, `wi`, and `hazard`.
- `GET /v1/agents/{mode}/demo` returns a route-specific action card for every mode.
- `GET /v1/scorecard` reports five passing route checks covering contract, guardrail, RAG/source match, action target correctness, and route isolation.
- The Docker profile starts a Qdrant-backed gateway, with a deterministic no-model evaluation path for CI/reviewer reproducibility.
- `docker-compose.opea.yml` adds an OPEA-compatible `/v1/embeddings` microservice boundary for Qdrant RAG.
- `docker-compose.opea-tei.yml` adds the official OPEA TEI embedding pattern with Hugging Face TEI, `TEI_EMBEDDING_ENDPOINT`, and `EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`; local E2E passed with 768-dimensional embeddings and all five demos using `qdrant-opea-tei-vector-store`.

PR-ready minimal scope I can prepare if this direction is useful:

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

A short technical article describing the route-isolated manufacturing action-card pattern is also public here:
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-wear-edge-opea-manufacturing.md

The main feedback I am looking for before opening the first PR is whether OPEA would prefer this as a new `GenAIExamples/ManufacturingAgentSuite` example, a docs-first blueprint proposal, or a split where reusable action-card/route-registry pieces move toward `GenAIComps` later.
