# Final Submission Form Fill Guide

Date: 2026-05-28

Source of truth: `submission-fields.draft.json`

Submission page:

```text
https://competition.aiforgood.itu.int/web/challenges/challenge-page/492/submission
```

## Required Identity Fields

| Form concept | Value |
| --- | --- |
| Application name | `WearEdge Pro` |
| Industry vertical | `Manufacturing` |
| Method name / project title | `WearEdge Pro: OPEA Manufacturing Five-Agent Suite` |
| Project URL | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing` |
| Frozen submission tag | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/final-submission-2026-05-28-r3` |
| Source engineering URL | `https://github.com/davidmillerak2026-sys/WearEdge-Pro` |
| Publication URL | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-wear-edge-opea-manufacturing.md` |
| Publication record URL | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1` |

## Component Selection

Select these OPEA component categories:

```text
LLM
RAG
Vector DB
Orchestration
Guardrails
```

## Method Description

Paste this text if the form provides a project description field:

```text
WearEdge Pro is a wearable edge AI product packaged for the OPEA challenge as a Docker-runnable Manufacturing Agent Suite. The submitted repository starts an OPEA-style Gateway, Manufacturing Megaservice, Qdrant RAG profile, OPEA-compatible embedding microservice profile, official OPEA TEI embedding profile, OpenAI/OPEA-compatible LLM adapter, deterministic evaluators, guardrails, browser demo console, five route demos, and a scorecard. The Vuzix M400 / Android client is the real deployment front end and field-evidence source; the Web Demo Console at /demo is the judge-facing experience for reproducible evaluation. The five runnable agents cover maintenance / CMMS work order, IQC / QMS quality event, changeover / checklist verification, WI / released instruction guidance, and hazard / EHS observation. The official TEI profile has both local Docker Desktop and Google Cloud C3 fresh-clone evidence, and the final package includes a champion risk burn-down, OPEA native depth matrix, PR-ready upstream patch, and LLM adapter benchmark path.
```

## Bonus Evidence URLs

Paste these into any optional links, supporting materials, or notes fields:

| Evidence | URL |
| --- | --- |
| OPEA RFC issue | `https://github.com/opea-project/GenAIExamples/issues/2461` |
| OPEA TEI update comment | `https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017` |
| OPEA project tracker | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2` |
| OPEA PR-ready package | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/docs/opea-upstream/pr-ready` |
| Champion risk burn-down | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/champion-risk-burn-down.md` |
| OPEA native depth matrix | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/opea-native-depth-matrix.md` |
| Production LLM benchmark path | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/production-llm-benchmark-path.md` |
| Data provenance and field validation | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/data-provenance-and-field-validation.md` |
| Telecom/manufacturing positioning | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/telecom-scope-and-manufacturing-positioning.md` |
| Technical article | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-wear-edge-opea-manufacturing.md` |
| Demo video | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4` |
| Demo video source | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/public/demo-video` |
| Demo video render report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/demo-video-render-report.md` |
| Submission URL dry run | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/submission-url-dry-run.md` |
| Local Docker Desktop final validation | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-docker-desktop-final-validation.md` |
| Xeon AVX-512/AMX benchmark JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json` |
| GCP C3 Docker/Qdrant E2E report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-docker-qdrant-e2e-report.md` |
| GCP C3 Docker/Qdrant E2E JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json` |
| Official OPEA profile | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-profile.md` |
| Official OPEA TEI profile | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-tei-profile.md` |
| GCP C3 OPEA profile E2E report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-profile-e2e-report.md` |
| GCP C3 OPEA profile E2E JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json` |
| Local OPEA TEI E2E report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-opea-tei-profile-e2e-report.md` |
| Local OPEA TEI E2E JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/local_opea_tei_profile_e2e.summary.json` |
| GCP C3 OPEA TEI E2E report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-tei-profile-e2e-report.md` |
| GCP C3 OPEA TEI E2E JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json` |

## Final Visual Review

Before pressing submit, verify:

- The vertical is `Manufacturing`.
- The project URL is the OPEA competition repository, not the broader
  WearEdge-Pro source repository.
- The description says the judge-facing product is Docker/Web/API, not an
  Android-only APK.
- The selected components include RAG, Vector DB, Orchestration, Guardrails,
  and LLM.
- The demo video URL opens as a GitHub asset page.
- The safety wording does not claim autonomous restart, quality release,
  maintenance release, safety clearance, final root cause, or production LLM
  acceleration.
