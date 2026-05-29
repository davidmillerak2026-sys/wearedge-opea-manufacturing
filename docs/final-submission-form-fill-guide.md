# Final Submission Form Fill Guide

Date: 2026-05-29

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
| Frozen submission tag | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/final-submission-2026-05-29-r25` |
| Source engineering URL | `https://github.com/davidmillerak2026-sys/WearEdge-Pro` |
| Publication URL | `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh` |
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
WearEdge Pro is a real wearable edge industrial AI agent system packaged for the OPEA challenge as a Docker-runnable Manufacturing Agent Suite. The submitted repository starts an OPEA-style Gateway, Manufacturing Megaservice, Retriever/RAG layer, Qdrant Vector DB profile, OPEA-compatible embedding microservice profile, official OPEA TEI embedding profile, OpenAI/OPEA-compatible LLM adapter, deterministic evaluators, guardrails, browser demo console, five route scenarios, a scorecard, and a lightweight GenAIEval-compatible evaluation pack. The key OPEA value is modularity: Gateway, Megaservice, Retriever/RAG, Vector DB, LLM adapter, Evaluator, and Guardrails are composable platform boundaries, while the model is a pluggable component behind the adapter. WearEdge can therefore run with local Jetson/Gemma 4 E2B, Gemini, or another OpenAI/OPEA-compatible model endpoint without rewriting route isolation, source grounding, deterministic checks, human-confirmation gates, or action-card contracts. The Vuzix M400 / Android client is the real deployment front end and field-evidence source; the Web Demo Console at /demo is the judge-facing experience for reproducible evaluation. The broader WearEdge program has private enterprise production-data lineage, including quality-inspection work such as toothbrush workshop visual inspection for IQC/OQC-style defect detection; raw customer plant images, labels, lot identifiers, and production records are intentionally not published. The five runnable agents cover maintenance / CMMS work order, IQC-OQC / QMS quality event, changeover / checklist verification, WI / released instruction guidance, and hazard / EHS observation. The official TEI profile has both local Docker Desktop and Google Cloud C3 c3-standard-4 fresh-clone evidence on a single-node 4-vCPU / 16-GiB-RAM / no-GPU configuration, which is inside the challenge limit of single node, <=64GB RAM, and 4-core CPU. The final package includes 15/15 GenAIEval-compatible route evaluation cases passing, an 8-worker route concurrency benchmark, a champion risk burn-down, OPEA native depth matrix, CI-green upstream OPEA PR, contribution patch, public article, and demo video evidence.
```

## Data Sources

Paste this text if the form asks for data sources:

```text
WearEdge uses OPEA workloads and GitHub resources from opea.dev and github.com/opea-project for architecture alignment, upstream contribution, and the official OPEA TEI embedding profile. The public challenge repository uses sanitized manufacturing knowledge sources and deterministic/synthetic benchmark fixtures committed under data/, evals/genaieval/, and evidence/ so judges can reproduce the five-agent routes without private plant access. The broader WearEdge program has private enterprise production-data lineage, including toothbrush workshop IQC/OQC visual-inspection work, but raw customer images, labels, lot IDs, and production records are not published. Public/open resources are used only where relevant to the runnable stack, including GitHub-hosted OPEA components, Hugging Face TEI images/models, Qdrant, Docker images, and public documentation. We do not claim use of unrelated public NLP datasets such as THUCTC, CLUE, CSDB, DRCD, Common Crawl, DBpedia, Kaggle, or other public corpora unless they are explicitly added in a future benchmark.
```

## Bonus Evidence URLs

Paste these into any optional links, supporting materials, or notes fields:

| Evidence | URL |
| --- | --- |
| OPEA RFC issue | `https://github.com/opea-project/GenAIExamples/issues/2461` |
| OPEA upstream PR | `https://github.com/opea-project/GenAIExamples/pull/2462` |
| OPEA TEI update comment | `https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017` |
| OPEA project tracker | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2` |
| OPEA contribution package | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/docs/opea-upstream/pr-ready` |
| Direct upstream PR attempt | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/upstream-pr-attempt-2026-05-28.md` |
| Champion risk burn-down | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/champion-risk-burn-down.md` |
| Evaluation criteria scorecard | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/evaluation-criteria-scorecard.md` |
| Full-mark gap closure plan | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/full-mark-gap-closure-plan.md` |
| Challenge task compliance | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/challenge-task-compliance.md` |
| OPEA native depth matrix | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/opea-native-depth-matrix.md` |
| Production LLM benchmark path | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/production-llm-benchmark-path.md` |
| GenAIEval-compatible evaluation | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/genaieval-compatible-evaluation.md` |
| GenAIEval-compatible route eval JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/genaieval/route_eval_results.json` |
| GenAIEval-compatible benchmark JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/genaieval/benchmark_results.json` |
| Route concurrency benchmark JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/route_concurrency.local-smoke.json` |
| Data provenance and field validation | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/data-provenance-and-field-validation.md` |
| Telecom/manufacturing positioning | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/telecom-scope-and-manufacturing-positioning.md` |
| External technical article | `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh` |
| GitHub article backup | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-wear-edge-opea-manufacturing.md` |
| External-platform article package | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/external-platform-article.md` |
| External-platform publishing handoff | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/public-platform-publishing-handoff.md` |
| YouTube demo video | `https://www.youtube.com/watch?v=dd9k8m6PDco` |
| GitHub demo video backup | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4` |
| Public video platform metadata | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/video-platform-description.md` |
| Demo video source | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/public/demo-video` |
| Demo video render report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/demo-video-render-report.md` |
| Submission URL dry run | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/submission-url-dry-run.md` |
| Local Docker Desktop final validation | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-docker-desktop-final-validation.md` |
| Local UI/full-mark follow-up validation | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-ui-full-mark-follow-up-validation.md` |
| Xeon AVX-512/AMX benchmark JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json` |
| Intel effective-use evidence | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/intel-effective-use-evidence.md` |
| Intel effective-use summary JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/intel_effective_use.summary.json` |
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
- The description says OPEA's value is modular composition: Gateway,
  Megaservice, Retriever/RAG, Vector DB, LLM adapter, Evaluator, and
  Guardrails are stable; the model is pluggable.
- The selected components include RAG, Vector DB, Orchestration, Guardrails,
  and LLM.
- GenAIEval wording says compatible/lightweight evidence, not full official
  GenAIEval/RAGAS/AutoRAG/LLM-as-judge execution.
- The demo video URL opens as a GitHub asset page.
- The external article URL is published on Dev.to, and the external demo video
  URL is published on YouTube.
- Data-source wording maps to OPEA/GitHub resources, sanitized manufacturing
  fixtures, synthetic benchmark cases, and private production-data lineage; it
  does not falsely claim unrelated THUCTC/CLUE/CSDB/DRCD/Common Crawl/DBpedia
  usage.
- Hardware wording says application-level Intel effective-use evidence plus
  same-host oneDNN BF16/AMX probe dispatch evidence, not TEI-internal AMX
  dispatch proof.
- The safety wording does not claim autonomous restart, quality release,
  maintenance release, safety clearance, final root cause, or production LLM
  acceleration.
