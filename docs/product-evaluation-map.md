# Product Evidence Map

Date: 2026-05-28

This document audits the product evidence areas one by one. It is not a guaranteed outcome statement. It is a product-hardening defense plan: what WearEdge Pro can
defend now, where evaluators could still raise questions, and what follow-up evidence
should be used to close each gap before release.

Status language:

- `Strong evidence`: current evidence is strong enough to argue for full
  coverage under the stated evidence areas.
- `Evidence gap to watch`: current evidence is strong, but a strict evaluator could
  still raise concerns unless the listed follow-up is emphasized or completed.
- `Not product-hardening safe`: this area needs additional work before we should claim a
  product-hardening position.

## Executive Evidence Position

| Product evidence area | Evidence scope | Current product-readiness status | Main reason |
| --- | ---: | --- | --- |
| Originality | Base readiness | Strong evidence | Wearable frontline evidence is routed into five manufacturing agents, not a generic chatbot. |
| Business Relevance | Base readiness | Strong evidence | Each agent closes into a real enterprise target: CMMS, QMS, changeover checklist, WI reference, or EHS case, with private production-data lineage behind the public package. |
| Use of OPEA | Architecture evidence | Evidence gap to watch | Official OPEA TEI and OPEA-style components are implemented, but no Helm/GMC deployment or merged upstream PR should be claimed. |
| System Efficiency | Runtime evidence | Strong evidence, with one LLM caveat | Single-node 4-vCPU / 16-GiB / no-GPU local and GCP C3 evidence is strong; production LLM serving latency is intentionally not over-claimed. |
| Code Quality | Engineering evidence | Strong evidence | Self-contained source, tests, Docker profiles, evidence checker, and signed commits are present. |
| Functional Completeness | Product evidence | Strong evidence | Web UI, API, five samples, five infer routes, Qdrant RAG, TEI profile, scorecard, and GenAIEval-compatible pack all run. |
| Open-source evidence | Public contribution evidence | Evidence gap to watch | Public RFC, comments, GenAIExamples PR #2462 with key check-run evidence, and open but unmerged OPEA docs Publications PR #395 exist; product evidence is stronger if maintainers engage, merge, or request changes that we address. |
| Knowledge-sharing evidence | Public knowledge evidence | Strong evidence | Public Dev.to article and YouTube walkthrough are live and linked; OPEA docs Publications PR #395 proposes adding the article to the official OPEA Publications / Blogs list. |
| Hardware optimization evidence | Runtime/hardware evidence | Strong evidence, with TEI-specific boundary | AVX-512/AMX C3 evidence is connected to WearEdge workloads; the r23 run passed the OPEA TEI/Qdrant/five-agent scorecard path and captured same-host oneDNN BF16/AMX probe dispatch markers. |

Target position: keep the base product evidence complete and keep the public evidence package coherent. The main remaining exposure is not missing product function; it is evaluator
interpretation around OPEA-native depth, upstream contribution maturity, and
low-level Intel optimization proof.

## Base Readiness Review

### Originality: Evidence Area

| Question | Audit |
| --- | --- |
| Is the product evidence strong now? | Yes. `Strong evidence`. |
| Why the evidence is strong | WearEdge Pro is a real wearable edge industrial AI agent system packaged for the target environment as a five-agent OPEA Manufacturing suite. The five routes cover predictive maintenance, IQC, SKU changeover, released work instruction guidance, and EHS hazard observation from one shared architecture. |
| What could cause weaker evidence | If the project is perceived as a collection of small samples instead of one industrial agent system, or if the M400 / frontline evidence lineage is not visible in the first minute. |
| Follow-up to protect product quality | In the project profile and video, lead with "real industrial AI agent system" and "five manufacturing value pools"; avoid calling the product a sample except for the evaluation-facing manufacturing console. |
| Evidence | `README.md`, `PROJECT_OVERVIEW.md`, `docs/product-package.md`, `docs/source-project-map.md`, `docs/data-provenance-and-field-validation.md`. |

### Business Relevance: Evidence Area

| Question | Audit |
| --- | --- |
| Is the product evidence strong now? | Yes. `Strong evidence`. |
| Why the evidence is strong | Every route maps to a concrete manufacturing workflow and system of record: maintenance work order, QMS quality event, changeover checklist, WI reference, or EHS case. This covers downtime, scrap, changeover loss, training drift, and safety risk. The broader WearEdge program also has private enterprise production-data lineage, including quality-inspection work such as toothbrush workshop visual inspection for IQC/OQC-style defect detection. |
| What could cause weaker evidence | Evaluators may ask why raw customer production data is not committed. |
| Follow-up to protect product quality | Emphasize integration targets, guarded action cards, and privacy-safe customer-data boundary. Keep claim boundaries clear: real product plus private production-data lineage, public sanitized package, not certified automatic plant release. |
| Evidence | `docs/opea-architecture-alignment.md`, `docs/data-provenance-and-field-validation.md`, `docs/product-hardening-plan.md`, `data/sample_requests/`, `data/agent_kb/`. |

### Use of OPEA: Evidence Area

| Question | Audit |
| --- | --- |
| Is the product evidence strong now? | Mostly yes, but `Evidence gap to watch`. |
| Why the evidence is strong | The package implements an OPEA-aligned modular chain: Gateway, Manufacturing Megaservice, Dataprep, Retriever/RAG, Qdrant Vector DB, LLM adapter, Evaluator, and Guardrails. These are composable platform boundaries; the model is only a pluggable component behind the adapter. It includes Qdrant, an OPEA-compatible embedding service, and an official OPEA TEI profile using `opea/embedding:latest` plus Hugging Face TEI. It also includes GenAIEval-compatible evaluation artifacts. |
| What could cause weaker evidence | A strict OPEA evaluator could reward teams that use more official GenAIComps microservices, Helm/GMC/Kubernetes deployment, production LLM serving, or merged upstream OPEA code. We must not overstate "OPEA native" beyond what is implemented. |
| Follow-up to close the gap | First: make PR #2462 and OPEA RFC/comment evidence prominent. Second: keep the official TEI profile and modular component map as the default product proof. Third: repeat that local Gemma, Gemini, or another endpoint can be swapped through the LLM adapter while Gateway/Megaservice/RAG/Evaluator/Guardrails remain unchanged. Stretch: add optional Kubernetes/Helm or GMC notes if time allows, and respond quickly to any upstream review. |
| Evidence | `docker-compose.opea-tei.yml`, `docs/official-opea-tei-profile.md`, `docs/opea-native-depth-matrix.md`, `docs/opea-component-evidence.md`, `evals/genaieval/`, OPEA issue #2461, OPEA PR #2462. |

### System Efficiency: Evidence Area

| Question | Audit |
| --- | --- |
| Is the product evidence strong now? | Yes, with one clear boundary. `Strong evidence, with production LLM caveat`. |
| Why the evidence is strong | The target hardware profile calls out typical enterprise hardware such as 64GB RAM, 4-core CPU, GPU optional. WearEdge has GCP C3 `c3-standard-4` single-node evidence with 4 vCPU, 16 GiB RAM, no GPU, Intel Xeon Platinum 8481C, AVX-512 and AMX flags. It also has local Docker Desktop TEI evidence, Docker memory stats, route latency, 8-worker route concurrency, and all five routes passing. |
| What could cause weaker evidence | Production LLM latency/quality is not benchmarked end to end. Current latency numbers are route/evaluator/RAG/embedding-focused, with deterministic LLM-adapter behavior unless an external LLM is configured. |
| Follow-up to protect product quality | In release, state the boundary exactly. Do not claim production LLM acceleration. If extra time/cloud budget exists, run one optional external LLM adapter benchmark and attach it as supplemental evidence, but the current no-GPU 4-core TEI/Qdrant evidence already fits the official hardware requirement. |
| Evidence | `docs/gcp-c3-opea-tei-profile-e2e-report.md`, `docs/local-opea-tei-profile-e2e-report.md`, `evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json`, `evidence/benchmarks/local_opea_tei_profile_e2e.summary.json`, `evidence/benchmarks/route_concurrency.local-smoke.json`. |

### Code Quality: Evidence Area

| Question | Audit |
| --- | --- |
| Is the product evidence strong now? | Yes. `Strong evidence`. |
| Why the evidence is strong | The repo is self-contained, Docker-runnable, dependency-light for the core app, test-covered, signed, and organized around clear route registry, megaservice, embedding, LLM adapter, evaluator, guardrail, scorecard, and UI boundaries. |
| What could cause weaker evidence | The public package is intentionally smaller than the broader WearEdge-Pro engineering repo, so evaluators could miss the source-system lineage if they only inspect this repo. |
| Follow-up to protect product quality | Keep `source-project-map` visible and make the public package read as a clean productization layer, not a stripped toy repo. Before release, run fresh-clone validation and avoid any unpushed evidence commits. |
| Evidence | `src/wear_edge_opea/`, `tests/`, `scripts/evidence_check.py`, `pyproject.toml`, `docs/source-project-map.md`. |

### Functional Completeness: Evidence Area

| Question | Audit |
| --- | --- |
| Is the product evidence strong now? | Yes. `Strong evidence`. |
| Why the evidence is strong | The package exposes `/demo`, `/healthz`, `/v1/agents`, five `GET /v1/agents/{mode}/demo` routes, five `POST /v1/agents/{mode}/infer` routes, `/v1/scorecard`, Qdrant-backed RAG, official TEI embeddings, action-card contracts, and guardrails. |
| What could cause weaker evidence | Only if evaluators do not run the Web Console or miss the five-route system shape. |
| Follow-up to protect product quality | The Web Console has been upgraded into a five-agent industrial command console. Use the YouTube walkthrough and final README opening to show the console quickly, then immediately show five agents, RAG source IDs, blocked claims, and scorecard pass state. |
| Evidence | `src/wear_edge_opea/demo_console.py`, `README.md`, `PROJECT_OVERVIEW.md`, `docs/local-docker-desktop-final-validation.md`, `public/product-walkthrough/`, `evidence/benchmarks/`. |

## Public Evidence Review

### Open-Source Evidence

| Question | Audit |
| --- | --- |
| Is the extended evidence strong now? | Strong, but `Evidence gap to watch`. |
| Why the evidence is strong | We have a public OPEA RFC issue, blueprint/implementation/TEI feedback, an upstream PR from the fork, signed commits, a local PR-ready package, and OPEA docs Publications PR #395. This directly matches "bug reports, PRs, or blueprint feedback". |
| What could cause weaker evidence | PR #2462 or PR #395 may remain unmerged, or maintainers may not review them before review. Some reviewers may value merged code more than open PRs and comments. |
| Follow-up to close the gap | Monitor PR #2462 and docs PR #395 daily, respond to review within hours, keep CI green, and add final comments linking the official TEI evidence and product-hardening audit. If maintainers request a smaller scope, split the PR rather than arguing scope. |
| Evidence | `https://github.com/opea-project/GenAIExamples/issues/2461`, `https://github.com/opea-project/GenAIExamples/pull/2462`, `https://github.com/opea-project/docs/pull/395`, `docs/upstream-pr-attempt-2026-05-28.md`, `docs/opea-upstream/`. |

### Knowledge Sharing: Public Evidence

| Question | Audit |
| --- | --- |
| Is the extended evidence strong now? | Yes. `Strong evidence`. |
| Why the evidence is strong | A public technical article, complete OPEA demo video, and product walkthrough video are published on external platforms, the repo includes publication records and backup copies, and OPEA docs PR #395 proposes adding the article to the official OPEA Publications / Blogs list. |
| What could cause weaker evidence | If evaluators do not click external links, if the article/video framing sounds like a sample instead of a real industrial AI agent system, or if they expect OPEA official publication and PR #395 remains unmerged. |
| Follow-up to protect product quality | In the project profile, include the Dev.to, YouTube, and OPEA docs PR #395 links near the top and use language that says WearEdge Pro is a real industrial AI agent system, with this repo as the OPEA public package. Do not claim official OPEA publication until PR #395 is merged. |
| Evidence | Dev.to article: `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh`; complete OPEA demo video: `https://youtu.be/ID8QPYhhhtk`; YouTube walkthrough: `https://www.youtube.com/watch?v=dd9k8m6PDco`; OPEA docs Publications PR: `https://github.com/opea-project/docs/pull/395`; `docs/publication-record.md`; `public/external-platform-article.md`; `public/video-platform-description.md`. |

### Hardware Optimization Evidence

| Question | Audit |
| --- | --- |
| Is the extended evidence strong now? | Yes. `Strong evidence, with TEI-specific boundary`. |
| Why the evidence is strong | GCP C3 `c3-standard-4` runs on Intel Xeon Platinum 8481C and detects `avx512f`, `avx512_bf16`, `avx512_vnni`, `amx_tile`, `amx_int8`, and `amx_bf16`. WearEdge validates five-agent scorecards, Docker/Qdrant, OPEA-compatible embeddings, official OPEA TEI, and the r23 TEI/oneDNN run on that hardware profile. The r23 run also reports `onednn_probe_executed=true` and `probe_dispatch_markers_captured=true` for a same-host oneDNN BF16/AMX probe. |
| What could cause weaker evidence | A strict evaluator could ask whether the TEI model server itself emitted AMX/AVX-512 oneDNN dispatch logs. It did not: `dispatch_markers_captured=false` applies to TEI/OPEA container logs. |
| Follow-up to protect product quality | Use the exact boundary: "OPEA TEI + Qdrant + five-agent scorecard passed on C3, and same-host oneDNN BF16/AMX probe captured dispatch markers; TEI-internal dispatch is not claimed." Optional hardening would be `perf` counters, a non-AMX CPU comparison, or a TEI build that emits oneDNN/DNNL dispatch lines. |
| Evidence | `docs/intel-effective-use-evidence.md`, `docs/intel-avx512-amx-benchmark-report.md`, `docs/gcp-c3-tei-onednn-verbose-report.md`, `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json`, `evidence/benchmarks/intel_effective_use.summary.json`, `evidence/benchmarks/gcp_c3_tei_onednn_verbose.summary.json`, `docs/gcp-c3-opea-tei-profile-e2e-report.md`. |

## Highest-Impact Follow-Up List

| Priority | Action | Evidence area protected | Why it matters |
| --- | --- | --- | --- |
| P0 | Push the latest local commit/tag so GitHub reflects this product-hardening audit. | All categories | Evaluators should see the final evidence map, not the older r14 package only. |
| P0 | In the project narrative, lead with "real industrial AI agent system" and "OPEA public package", not "sample project". | Originality, Business Relevance, Functional Completeness | This prevents the biggest framing error. |
| P0 | State the private customer production-data boundary, including toothbrush workshop IQC/OQC lineage, without leaking raw data. | Business Relevance, Code Quality | This proves enterprise relevance while respecting confidentiality. |
| P0 | Make the official TEI profile the primary technical proof. | Use of OPEA, System Efficiency | `opea/embedding:latest` plus TEI plus Qdrant is the strongest OPEA-native evidence. |
| P1 | Monitor and respond to OPEA PR #2462, docs PR #395, and issue #2461. | Open-source evidence, Use of OPEA, Knowledge Sharing | Merge is not required by the wording, but maintainers' engagement makes the evidence much harder to discount. |
| P1 | Add a short final PR/issue comment linking the GCP C3 official OPEA TEI evidence and Dev.to/YouTube materials. | Open-source, Knowledge Sharing, Hardware Optimization | It ties all public evidence into the upstream OPEA conversation. |
| P1 | Optional: collect perf counters, non-AMX comparison, or TEI build logs that emit oneDNN/DNNL dispatch lines. | Hardware Optimization | The r23 same-host oneDNN probe closes the main hardware gap; these are only extra hardening paths if evaluators ask for TEI-internal dispatch proof. |
| P2 | Optional Kubernetes/Helm/GMC deployment note or manifest. | Use of OPEA | Helpful if reviewers strongly favor cloud-native OPEA deployment, but not necessary for the required Docker one-click path. |
| P2 | Optional external LLM adapter benchmark. | System Efficiency | Useful only if we can run it cleanly without over-claiming production LLM quality. |

## Claim Boundaries To Keep Us Safe

Use these boundaries in the project profile and any evaluator Q&A:

- WearEdge Pro is a real industrial AI agent system; this repository is the
  OPEA public runnable package.
- The Vuzix M400 / Android path is the frontline evidence source and real
  deployment context; the released evaluation experience is Docker + Web UI + API.
- High-risk decisions remain human-confirmed. The system generates bounded action cards
  and blocks unsupported claims such as restart permission, quality release,
  final root cause, and safety clearance.
- The official TEI profile proves OPEA embedding integration and Qdrant RAG on
  4-vCPU / 16-GiB / no-GPU hardware; production LLM endpoint performance is not
  claimed unless separately configured and benchmarked.
- AVX-512/AMX evidence is effective-use evidence on Intel C3 hardware. The r23
  TEI/oneDNN run passed application checks and captured same-host oneDNN
  BF16/AMX probe dispatch markers. The TEI container logs still did not emit
  dispatch markers, so TEI-internal AMX dispatch is not claimed.

## One-Paragraph Project Summary

```text
WearEdge Pro is a real wearable edge industrial AI agent system packaged for
this OPEA ecosystem as a Docker-runnable Manufacturing Agent Suite. It targets
Manufacturing with five executable agents for maintenance, IQC, changeover,
released work instructions, and EHS hazard observation. Its OPEA value is the
modular chain: Gateway, Manufacturing Megaservice, Retriever/RAG, Qdrant Vector
DB, LLM adapter, Evaluator, and Guardrails are composable boundaries, while the
model is pluggable through the adapter. The package includes official OPEA TEI,
scorecards, GenAIEval-compatible artifacts, local Docker Desktop and Google
Cloud C3 single-node 4-vCPU / 16-GiB / no-GPU evidence, public OPEA
RFC/PR/feedback, a public technical article, a public product walkthrough video, and Intel
AVX-512/AMX effective-use evidence.
```
