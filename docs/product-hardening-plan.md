# Product Hardening Plan

Date: 2026-05-28

This plan turns the product evidence map into concrete follow-up actions. It assumes
the goal is to maintain strong product evidence across the expected criteria.

## 1. Framing: Real Industrial Agent System

Required position across all materials:

```text
WearEdge Pro is a real industrial AI agent system. This repository is the
OPEA public runnable package for that system.
```

Actions already taken:

- README, project docs, technical report, and manufacturing console describe the
  product as a real industrial AI agent system.
- The manufacturing console now shows five plant agents, OPEA pipeline stages, RAG source
  evidence, action-card guardrails, and private production-data boundary.

Remaining follow-up:

- In the project profile, avoid "sample project" wording.
- Use "evaluation-facing manufacturing console" only to describe the Web UI, not the whole
  product.

## 2. Enterprise Customer Production Data

Current defendable claim:

```text
WearEdge has private enterprise production-data lineage, including
quality-inspection work such as toothbrush workshop visual inspection for
IQC/OQC-style defect detection. The public repo uses sanitized, reproducible
fixtures instead of leaking customer files.
```

Why this matters:

- It protects business relevance evidence.
- It answers the likely evaluator question: "Is this just synthetic data?"
- It keeps confidentiality clean.

Do not publish:

- raw customer plant images;
- lot IDs, order IDs, operator IDs, customer names, or factory identifiers;
- proprietary defect labels unless cleared for public release.

If we want to strengthen this further, add a redacted evidence manifest with:

- dataset name such as `private_toothbrush_iqc_visual_inspection_redacted`;
- date range or collection period;
- number of images/frames if permitted;
- defect classes if permitted;
- statement that raw data is private and not included.

## 3. Use Of OPEA: What Else Can We Do?

Current strong evidence:

- OPEA-style Gateway and Manufacturing Megaservice;
- Dataprep, Retriever/RAG, Qdrant, guardrails, scorecard;
- OPEA-compatible `/v1/embeddings` profile;
- official OPEA TEI profile using `opea/embedding:latest`, Hugging Face TEI,
  `TEI_EMBEDDING_ENDPOINT`, and 768-dimensional embeddings;
- GenAIEval-compatible dataset, runner, metrics, and benchmark outputs;
- OPEA RFC issue, upstream PR #2462, and OPEA docs Publications PR #395.

Highest-value remaining upgrades:

| Upgrade | Value | Feasibility | Recommendation |
| --- | --- | --- | --- |
| Keep PR #2462 and docs PR #395 green/responded | Directly protects OPEA use, open-source evidence, and knowledge-sharing evidence | High | Do daily through the review window |
| Add final upstream comment linking TEI, GCP C3, article, and video | Shows feedback loop, not just code dump | High | Do before release |
| Optional Helm/GMC/Kubernetes note or manifest | Helps if evaluators expect cloud-native OPEA | Medium | Nice-to-have, not P0 |
| More official GenAIComps services | Could deepen OPEA-native implementation | Medium/low under time limit | Only if it does not destabilize the runnable package |
| Official GenAIEval integration | Stronger than compatible pack | Medium/low if dependency setup is heavy | Do only if quick; current compatible pack is honest and runnable |

Best product posture:

```text
We use official OPEA TEI where it matters most for the reproducible workload,
and we keep the rest of the pipeline OPEA-aligned, inspectable, and upstreamed.
```

## 4. Production LLM/LMM Full-Chain Benchmark

Current state:

- The repository includes a real OpenAI/OPEA-compatible LLM adapter.
- `scripts/llm_adapter_benchmark.py` can benchmark a real chat-completions
  endpoint when configured.
- The committed default path is deterministic so evaluators can run the package
  without secrets or large model downloads.

Can we run a production end-to-end benchmark now?

| Requirement | Status | Decision |
| --- | --- | --- |
| Real OpenAI/OPEA-compatible LLM endpoint | Not currently configured in repo | Needed for honest production LLM claim |
| Multimodal LMM endpoint for image evidence | Not currently configured in OPEA package | Needed for honest production LMM/VLM claim |
| Local Docker Desktop | Available, but Docker Engine access needs local Docker permission | Can rerun Compose/TEI if approved |
| GCP C3 CPU host | Available and validated, including supplemental TEI/oneDNN verbose attempt | Additional perf/non-AMX comparison is possible but optional |

Recommendation:

- Do not claim production LLM/LMM end-to-end benchmark unless a real endpoint is
  configured and `fallback_count=0`.
- If credentials or a local model service become available, run the existing
  strict benchmark path and commit `evidence/benchmarks/llm_adapter.production.json`.
- For true LMM/VLM evidence, add a separate multimodal benchmark only after the
  endpoint accepts image inputs. Otherwise keep the IQC detector evidence as
  structured visual evidence, not LMM benchmark evidence.

## 5. Code Quality: Why We Should Still Defend Strong Product Quality

We should not say "code is elsewhere." The correct framing is:

```text
This repository contains the complete runnable OPEA public product package.
WearEdge-Pro is the broader engineering source tree for M400 Android, Jetson,
edge gateway, and archived field evidence.
```

Current code-quality evidence:

- source code under `src/wear_edge_opea/`;
- tests under `tests/`;
- Dockerfiles and Compose profiles;
- route registry and data-driven five-agent architecture;
- evidence checker;
- LLM adapter and benchmark harness;
- GenAIEval-compatible evaluation package;
- upstream PR package.

Remaining optional upgrade:

- Add a `docs/source-release-snapshot.md` or mirror selected WearEdge-Pro source
  directories only if the repo must be self-contained for M400/Jetson review.
  This is not required for the OPEA public product, but it can remove any
  doubt that code quality is real.

## 6. Functional Completeness And UI

Functional completeness is now a product-hardening position:

- `/demo` Web Console;
- `/healthz`;
- `/v1/agents`;
- five `GET /v1/agents/{mode}/demo` routes;
- five `POST /v1/agents/{mode}/infer` routes;
- `/v1/scorecard`;
- Qdrant RAG and official OPEA TEI profile;
- action-card contracts and guardrails;
- local and GCP evidence.

UI follow-up completed:

- The Web Console now opens as a five-agent industrial command console.
- It shows the OPEA pipeline rail, route selector, scorecard, RAG sources,
  blocked claims, LLM runtime, and enterprise data boundary.

## 7. Evidence Plan

### Open-Source Evidence

Current state: strong but still vulnerable until maintainers engage.

Follow-up:

- monitor OPEA PR #2462 and OPEA docs PR #395;
- respond to any maintainer review quickly;
- add a final comment with GCP C3 TEI evidence and the public article/video;
- if maintainers ask for a smaller scope, split the PR.

### Knowledge-Sharing Evidence

Current state: defendable because Dev.to and YouTube are public, and OPEA docs
PR #395 is open and mergeable to add the article to the official OPEA
Publications / Blogs list.

Is the article technical enough?

Yes, it covers route registry, OPEA architecture, Qdrant RAG, TEI embeddings,
guardrails, evaluation, and Intel evidence. To strengthen beyond "one article
and one video", optional follow-up articles could cover:

- "What we learned integrating OPEA TEI with Qdrant for manufacturing RAG";
- "How we designed guardrails for five industrial agent routes";
- "Running WearEdge on Google Cloud C3 Xeon with AVX-512/AMX evidence";
- "Blueprint feedback for OPEA Manufacturing examples".

Recommendation: keep PR #395 monitored and do not claim official OPEA
publication until it merges. The existing Dev.to + YouTube evidence already
satisfies the evaluation criteria; PR #395 makes the knowledge-sharing evidence stronger.

### Hardware Optimization Evidence

Current state: strong application-level evidence; supplemental TEI/oneDNN
verbose attempt captured; still vulnerable only on instruction-level dispatch
proof.

What we already have:

- GCP C3 `c3-standard-4`;
- 4 vCPU, 16 GiB RAM, no GPU;
- Intel Xeon Platinum 8481C;
- AVX-512 and AMX flags detected;
- Docker/Qdrant E2E;
- OPEA-compatible embedding E2E;
- official OPEA TEI E2E;
- supplemental TEI/oneDNN verbose attempt with Gateway, scorecard, five samples,
  Docker stats, CPU flags, and TEI logs captured;
- route, scorecard, memory, and cleanup evidence.

What would make it harder to dispute:

- TEI or oneDNN verbose logs showing CPU backend/kernel dispatch. The r20
  attempt enabled verbose capture but returned `dispatch_markers_captured=false`;
- side-by-side comparison against a non-AMX CPU instance;
- production LLM endpoint benchmark on the same C3 host with strict fallback
  disabled.

Recommendation: keep the current claim as "effective use of Intel hardware
features", which is exactly the wording of the evidence category. Only add more
hardware work if we can collect perf counters, a non-AMX comparison, or a TEI
build that emits oneDNN/DNNL dispatch marker lines.
