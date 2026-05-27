# OPEA TEI Update Comment

Target issue:

```text
https://github.com/opea-project/GenAIExamples/issues/2461
```

Status: posted to the upstream OPEA issue on 2026-05-27:

```text
https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017
```

A GitHub App attempt on 2026-05-27 returned
`403 Resource not accessible by integration`, so the comment was posted through
a user-authenticated GitHub browser session. The same update was also posted to
the project tracker:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2#issuecomment-4553776627
```

## Comment Body

Implementation update: the reference package now includes an official OPEA TEI
embedding profile in addition to the deterministic and OPEA-compatible profiles.

New profile:

```bash
docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml up -d
```

What changed:

- `docker-compose.opea-tei.yml` wires Hugging Face TEI, `opea/embedding:latest`,
  Qdrant, and the Manufacturing Gateway.
- The profile uses the OPEA TEI pattern with `TEI_EMBEDDING_ENDPOINT`,
  `EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`, and `/v1/embeddings`.
- Local E2E passed with `BAAI/bge-base-en-v1.5`, 768-dimensional embeddings,
  all five manufacturing demo routes, and `/v1/scorecard` passing.
- Google Cloud C3 fresh-clone E2E passed on `c3-standard-4` in
  `us-central1-a`; the temporary VM `wearedge-opea-tei-0527103938` was deleted
  after the run.
- All five route demos report `qdrant-opea-tei-vector-store` in the RAG
  evidence when this profile is used.
- A Google Cloud C3 fresh-clone rerun script is included for the same profile:
  `scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh`.

Evidence:

- Official TEI profile docs:
  https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-tei-profile.md
- Local TEI E2E report:
  https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-opea-tei-profile-e2e-report.md
- Local TEI JSON summary:
  https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/local_opea_tei_profile_e2e.summary.json
- GCP C3 TEI E2E report:
  https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-tei-profile-e2e-report.md
- GCP C3 TEI JSON summary:
  https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json
- Commit:
  https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/commit/e7126c63d0e4dc7d7cee6784550a3f3dd8a8131d

This makes the proposed `ManufacturingAgentSuite` blueprint closer to an
OPEA-native example rather than only an API-compatible wrapper: it now has
Gateway/Megaservice, route-isolated RAG/Qdrant, guardrails, scorecard, and an
official TEI embedding component path.
