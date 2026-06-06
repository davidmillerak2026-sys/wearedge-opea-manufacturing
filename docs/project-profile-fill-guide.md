# Release Form Fill Guide

Date: 2026-05-29

Source of truth: `project-profile.json`

Platform page:

```text
https://competition.aiforgood.itu.int/web/challenges/challenge-page/492/project
```

## Required Identity Fields

| Form concept | Value |
| --- | --- |
| Application name | `WearEdge Pro` |
| Industry vertical | `Manufacturing` |
| Method name / project title | `WearEdge Pro: OPEA Manufacturing Five-Agent Suite` |
| Project URL | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing` |
| Frozen project tag | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/final-submission-2026-06-06-r31` |
| Source engineering URL | `https://github.com/davidmillerak2026-sys/WearEdge-Pro` |
| Technical report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/TECHNICAL_REPORT.md` |
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
Embeddings
Evaluation
Retriever
Reranker
```

## Method Description

Paste this text if the form provides a project description field:

```text
WearEdge Pro is a real wearable edge industrial AI agent system packaged for the OPEA ecosystem as a Docker-runnable Manufacturing Agent Suite. The public repository starts an OPEA-style Gateway, Manufacturing Megaservice, Retriever/RAG layer, Qdrant Vector DB profile, OPEA-compatible embedding microservice profile, official OPEA TEI embedding profile, OpenAI/OPEA-compatible LLM adapter, deterministic evaluators, guardrails, browser manufacturing console, five route scenarios, a scorecard, and a lightweight GenAIEval-compatible evaluation pack. The key OPEA value is modularity: Gateway, Megaservice, Retriever/RAG, Vector DB, LLM adapter, Evaluator, and Guardrails are composable platform boundaries, while the model is a pluggable component behind the adapter. WearEdge can therefore run with local Jetson/Gemma 4 E2B, Gemini, or another OpenAI/OPEA-compatible model endpoint without rewriting route isolation, source grounding, deterministic checks, human-confirmation gates, or action-card contracts. The Vuzix M400 / Android client is the real deployment front end and field-evidence source; the Browser Manufacturing Console at /demo is the reproducible product experience. The broader WearEdge program has private enterprise production-data lineage, including quality-inspection work such as toothbrush workshop visual inspection for IQC/OQC-style defect detection; raw customer plant images, labels, lot identifiers, and production records are intentionally not published. The five runnable agents cover maintenance / CMMS work order, IQC-OQC / QMS quality event, changeover / checklist verification, WI / released instruction guidance, and hazard / EHS observation. The official TEI profile has both local Docker Desktop and Google Cloud C3 c3-standard-4 fresh-clone evidence on a single-node 4-vCPU / 16-GiB-RAM / no-GPU configuration, which is inside the target runtime limit of single node, <=64GB RAM, and 4-core CPU. The current main package and frozen tag include 15/15 GenAIEval-compatible route evaluation cases passing, a captured official OPEA GenAIEval chatqnafixed local benchmark, an 8-worker route concurrency benchmark, local Gemma/Ollama LLM endpoint evidence, optional OPEA-compatible reranker and Kubernetes profiles, a product risk burn-down, OPEA native depth matrix, an open upstream OPEA PR with key check-run evidence, OPEA docs Publications PR #395, contribution patch, public article, and product walkthrough video evidence.
```

## Data Sources

Paste this text if the form asks for data sources:

```text
WearEdge uses OPEA workloads and GitHub resources from opea.dev and github.com/opea-project for architecture alignment, upstream contribution, and the official OPEA TEI embedding profile. The public repository uses sanitized manufacturing knowledge sources and deterministic/synthetic benchmark fixtures committed under data/, evals/genaieval/, and evidence/ so evaluators can reproduce the five-agent routes without private plant access. The broader WearEdge program has private enterprise production-data lineage, including toothbrush workshop IQC/OQC visual-inspection work, but raw customer images, labels, lot IDs, and production records are not published. Public/open resources are used only where relevant to the runnable stack, including GitHub-hosted OPEA components, Hugging Face TEI images/models, Qdrant, Docker images, and public documentation. We do not claim use of unrelated public NLP datasets such as THUCTC, CLUE, CSDB, DRCD, Common Crawl, DBpedia, Kaggle, or other public corpora unless they are explicitly added in a future benchmark.
```

## Evidence URLs

Paste these into any optional links, supporting materials, or notes fields:

| Evidence | URL |
| --- | --- |
| OPEA RFC issue | `https://github.com/opea-project/GenAIExamples/issues/2461` |
| OPEA upstream PR | `https://github.com/opea-project/GenAIExamples/pull/2462` |
| OPEA docs Publications PR | `https://github.com/opea-project/docs/pull/395` |
| OPEA TEI update comment | `https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017` |
| OPEA project tracker | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2` |
| OPEA contribution package | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/docs/opea-upstream/pr-ready` |
| Direct upstream PR attempt | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/upstream-pr-attempt-2026-05-28.md` |
| Product risk burn-down | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/product-risk-burn-down.md` |
| Product evidence map | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/product-evaluation-map.md` |
| Product hardening plan | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/product-hardening-plan.md` |
| OPEA architecture alignment | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/opea-architecture-alignment.md` |
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
| YouTube product walkthrough video | `https://www.youtube.com/watch?v=dd9k8m6PDco` |
| Public product walkthrough video backup | `https://www.youtube.com/watch?v=dd9k8m6PDco` |
| Public video platform metadata | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/video-platform-description.md` |
| Product walkthrough video source | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/public/product-walkthrough` |
| Product walkthrough render report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/product-walkthrough-render-report.md` |
| Public URL availability check | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/public-url-check.md` |
| Project guidelines final audit | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/release-guidelines-audit.md` |
| Local Docker Desktop final validation | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-docker-desktop-final-validation.md` |
| Local UI/product hardening follow-up validation | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-ui-product-hardening-follow-up-validation.md` |
| Hardware constraints and clean-run boundary | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/hardware-constraints-and-clean-run.md` |
| License and third-party attribution | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/license-and-attribution.md` |
| Xeon AVX-512/AMX benchmark JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json` |
| Intel effective-use evidence | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/intel-effective-use-evidence.md` |
| Intel effective-use summary JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/intel_effective_use.summary.json` |
| GCP C3 Docker/Qdrant E2E report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-docker-qdrant-e2e-report.md` |
| GCP C3 Docker/Qdrant E2E JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json` |
| GCP C3 Docker/Qdrant timed clean-run JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_docker_qdrant_e2e_timed.summary.json` |
| Official OPEA profile | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-profile.md` |
| Official OPEA TEI profile | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-tei-profile.md` |
| GCP C3 OPEA profile E2E report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-profile-e2e-report.md` |
| GCP C3 OPEA profile E2E JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json` |
| Local OPEA TEI E2E report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-opea-tei-profile-e2e-report.md` |
| Local OPEA TEI E2E JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/local_opea_tei_profile_e2e.summary.json` |
| GCP C3 OPEA TEI E2E report | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-tei-profile-e2e-report.md` |
| GCP C3 OPEA TEI E2E JSON | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json` |

## Final Visual Review

Before publishing, verify:

- The vertical is `Manufacturing`.
- The project URL is the OPEA public repository, not the broader
  WearEdge-Pro source repository.
- The description says the evaluation-facing product is Docker/Web/API, not an
  Android-only APK.
- The description says OPEA's value is modular composition: Gateway,
  Megaservice, Retriever/RAG, Vector DB, LLM adapter, Evaluator, and
  Guardrails are stable; the model is pluggable.
- The selected components include LLM, RAG, Vector DB, Orchestration,
  Guardrails, Embeddings, Evaluation, Retriever, and Reranker if the form
  exposes those categories.
- GenAIEval wording says lightweight compatible evidence plus an official
  GenAIEval benchmark run; it does not claim RAGAS/AutoRAG/LLM-as-evaluator
  execution.
- The product walkthrough video URL opens on YouTube.
- The external article URL is published on Dev.to, and the external product walkthrough video
  URL is published on YouTube.
- OPEA docs Publications PR #395 is listed as open, not as merged or
  official OPEA publication yet.
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
