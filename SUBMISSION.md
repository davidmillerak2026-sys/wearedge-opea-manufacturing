# ITU AI for Good OPEA Manufacturing Submission

Challenge: Innovation Challenge on Generative AI Applications for Enterprise Scenarios Using OPEA

Vertical: Manufacturing

Application name: WearEdge Pro

## One-Sentence Summary

WearEdge Pro is a real OPEA-aligned wearable edge industrial AI agent system for Manufacturing that routes first-person M400 evidence into five bounded agents: maintenance, IQC, changeover, work instruction, and hazard observation.

## Final Product Shape

The competition deliverable is not an Android-only APK and not an ephemeral contest artifact. It is the Docker-runnable OPEA Manufacturing Agent Suite package for the WearEdge Pro industrial AI agent system, with a browser evaluation console and API surface.

Judge-facing entry point:

```text
http://127.0.0.1:8088/demo
```

The Vuzix M400 / Android client is the real deployment front end and field-evidence source from the full WearEdge-Pro product. The Web Demo Console is the reproducible evaluation surface for judges who do not have M400 hardware.

Single-node hardware proof:

```text
Google Cloud C3 c3-standard-4, us-central1-a
4 vCPU, 16 GiB RAM, no GPU
Intel Xeon Platinum 8481C
AVX-512 and AMX flags detected
Challenge fit: single node, <=64GB RAM, 4-core CPU profile, GPU optional
```

## Why This Fits Manufacturing

Manufacturing losses rarely live in one silo. A frontline operator may see a gearbox vibration issue, a machined-part defect, a changeover mismatch, a work-instruction question, or an unsafe walkway. WearEdge Pro uses one OPEA-style Gateway and Manufacturing Megaservice to convert those observations into auditable action cards for plant systems.

| Agent | Manufacturing decision | Integration target |
| --- | --- | --- |
| `maintenance` | Is this machine condition ready for CMMS escalation? | `maintenance_work_order` |
| `iqc` | Should this part or lot be held for quality review? | `qms_quality_event` |
| `changeover` | Is the SKU changeover evidence ready for first-piece sign-off? | `changeover_checklist` |
| `wi` | What released work instruction should guide the operator? | `wi_reference` |
| `hazard` | Does the scene require stop, report, or EHS correction? | `ehs_case` |

The hero scenario remains the lao-shi-fu predictive-maintenance loop for packaging-line gearbox `PKG-L3-GBX-03`, because it has the strongest archived M400/Jetson evidence. The submitted repository now also includes runnable samples and route-specific guardrails for IQC, changeover, WI, and hazard.

## OPEA Claim

Current submission components:

```text
LLM, RAG, Vector DB, Orchestration, Guardrails
```

Implemented OPEA-style path:

```text
Gateway -> Manufacturing Megaservice -> Dataprep -> Retriever/RAG -> Vector DB -> LLM adapter -> Evaluator -> Guardrails -> Action Card
```

Evaluation path:

```text
/v1/scorecard + GenAIEval-compatible JSONL dataset, runner, metrics, benchmark JSON, and summary.md
```

The Docker Compose profile uses Qdrant as the Vector DB. The local no-dependency demo keeps an in-memory vector fallback so reviewers can run the same route contracts without Docker.

The repository also includes an official OPEA-compatible embedding microservice profile:

```bash
docker compose -f docker-compose.yml -f docker-compose.opea.yml up --build -d
```

That profile adds a separate `/v1/embeddings` microservice and configures the Gateway with `WEAREDGE_EMBEDDING_BACKEND=opea`, so Qdrant indexing and search use a microservice boundary instead of only in-process embeddings.

The repository also includes a stronger official TEI component profile:

```bash
docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml up -d
```

That profile follows OPEA's TEI embedding pattern with Hugging Face TEI,
`TEI_EMBEDDING_ENDPOINT`, `EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`, the
OPEA embedding microservice, Qdrant, and the same five WearEdge manufacturing
routes. It is the right profile to rerun on Google Cloud C3 for official
production embedding evidence.

The FastAPI gateway also serves a browser Manufacturing Demo Console at `/demo`, so reviewers can inspect requests, RAG evidence, action cards, guardrails, and scorecard results without writing curl commands.

The LLM adapter now supports both the deterministic no-secret path and an
OpenAI/OPEA-compatible chat-completions endpoint. The submitted evidence
includes a local adapter contract benchmark; production LLM wording should only
be used after a configured endpoint benchmark reports
`production_llm_endpoint_benchmarked`.

## Challenge Task Compliance

| Official task | WearEdge Pro submission |
| --- | --- |
| Design and build a domain-specific GenAI application | OPEA-style Manufacturing suite with Gateway, Megaservice, LLM adapter, official TEI embedding profile, Qdrant RAG, route evaluators, guardrails, and scorecard |
| Select a concrete industry scenario | Manufacturing, covering maintenance, IQC, changeover, work instruction, and EHS hazard observation |
| Deliver a working prototype with documentation | Docker-runnable WearEdge Pro OPEA package with `README.md`, `docs/technical-report.draft.md`, `deploy.sh`, Compose profiles, and Web/API evaluation surface |
| Demonstrate performance and usability | GCP C3 4-vCPU / 16-GiB / no-GPU runs, latency JSON, Docker memory stats, 8-worker route concurrency benchmark, GenAIEval-compatible 300-call benchmark, and browser console at `/demo` |

Detailed mapping: `docs/challenge-task-compliance.md`.

## Evaluation Criteria Defense

WearEdge Pro is organized around the official 100 base + 40 bonus rubric:

| Rubric area | Submission defense |
| --- | --- |
| Creativity and Business Value, 30 pts | Five real manufacturing workflows and integration targets, not a single chatbot |
| Technical Implementation, 40 pts | OPEA-style Gateway/Megaservice/RAG/Qdrant/TEI/LLM-adapter/guardrail/evaluation architecture with local and GCP evidence |
| Prototype Quality, 30 pts | Docker-runnable Web/API product, `/demo`, five demo routes, five infer routes, scorecard, tests, and documentation |
| Open-source bonus, up to 15 pts | OPEA RFC/comments plus upstream PR #2462, CI-green from fork |
| Knowledge sharing bonus, up to 10 pts | Public Dev.to technical article and YouTube demo video |
| Hardware optimization bonus, up to 15 pts | Intel Xeon AVX-512/AMX C3 evidence plus application-level OPEA TEI/Qdrant workload records |

Detailed score defense: `docs/evaluation-criteria-scorecard.md`.

## Runnable Evidence

```bash
docker compose up --build -d
# Open in browser: http://127.0.0.1:8088/demo
curl http://127.0.0.1:8088/v1/agents
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/agents/iqc/demo
curl http://127.0.0.1:8088/v1/agents/changeover/demo
curl http://127.0.0.1:8088/v1/agents/wi/demo
curl http://127.0.0.1:8088/v1/agents/hazard/demo
curl http://127.0.0.1:8088/v1/scorecard
```

The scorecard reports route latency, contract pass, guardrail pass, RAG/source match, action-target correctness, and route-isolation pass/fail for all five agents.

The lightweight GenAIEval-compatible evaluation pack in `evals/genaieval/`
adds 15 committed route cases and records 15/15 pass across contract, target,
channel, risk, human gate, guardrail, RAG source, and route-isolation metrics.

## Source Evidence

Full engineering source:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

Key archived evidence already mapped into this submission package:

- M400 real-device full chain
- Jetson local multimodal inference
- five-agent deterministic validation
- lao-shi-fu maintenance evidence loop
- manufacturing RAG / maintenance KB
- IQC quality plan and released-source checks
- guardrailed action cards
- runtime stream and audit logs
- automated tests

## Remaining Champion Bonus Work

- OPEA issue/PR/blueprint feedback: public RFC issue posted at `https://github.com/opea-project/GenAIExamples/issues/2461`; implementation and official TEI update comments posted upstream; real upstream PR opened at `https://github.com/opea-project/GenAIExamples/pull/2462`; DCO, pre-commit.ci, dependency-review, get-test-matrix, get-test-case, and compose-test passed; public tracker posted at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`. The prepared contribution package and `git format-patch` artifact remain under `docs/opea-upstream/pr-ready/`.
- Champion risk burn-down: each known non-winning risk has a mitigation and claim boundary in `docs/champion-risk-burn-down.md`, including OPEA-native depth, production LLM benchmark path, skim-friendly demo positioning, data provenance, upstream PR status, and telecom-vs-manufacturing positioning.
- LLM adapter benchmark path: `src/wear_edge_opea/llm_adapter.py` and `scripts/llm_adapter_benchmark.py` provide a production endpoint benchmark path while keeping the default judge run deterministic and reproducible.
- GenAIEval-compatible evaluation: `evals/genaieval/` and `evidence/genaieval/` provide a dataset, benchmark config, runner, 15-case route evaluation JSON, throughput/latency benchmark JSON, and summary.
- OPEA-compatible embedding profile: `docker-compose.opea.yml` adds a separate `/v1/embeddings` microservice and routes Qdrant RAG embeddings through it.
- Official OPEA TEI profile: `docker-compose.opea-tei.yml` wires Hugging Face TEI, the OPEA embedding microservice, Qdrant, and the five agent routes for production embedding evidence; local E2E and Google Cloud C3 fresh-clone E2E both passed.
- Knowledge sharing: the external technical article is published on Dev.to at `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh`; the demo video is published on YouTube at `https://www.youtube.com/watch?v=dd9k8m6PDco`; the GitHub article/video backups remain public evidence.
- Intel AVX-512/AMX: Google Cloud C3 `c3-standard-4` single-node run captured in `us-central1-a` with 4 vCPU, 16 GiB RAM, no GPU, Intel Xeon Platinum 8481C, `avx512f`, `amx_tile`, `amx_int8`, and `amx_bf16` detected; scorecard passed; `docs/intel-effective-use-evidence.md` and `evidence/benchmarks/intel_effective_use.summary.json` connect the C3 CPU feature run to Docker/Qdrant, OPEA-compatible embedding, and official OPEA TEI workloads.
- Docker/Qdrant E2E: Google Cloud C3 `c3-standard-4` single-node 4-vCPU / 16-GiB-RAM / no-GPU fresh-clone run captured in `us-central1-a`; Docker Compose started Qdrant plus the Manufacturing Gateway, `/demo` returned HTTP 200, five demo routes and five infer routes returned correct action cards, `/v1/scorecard` passed, and the VM was deleted after the run.
- OPEA profile E2E: Google Cloud C3 `c3-standard-4` single-node 4-vCPU / 16-GiB-RAM / no-GPU fresh-clone run captured in `us-central1-a`; Docker Compose started Qdrant, the OPEA-compatible `/v1/embeddings` service, and the Manufacturing Gateway; five routes reported `qdrant-opea-compatible-embedding-vector-store`, `/v1/scorecard` passed, and the VM was deleted after the run.
- Local official OPEA TEI E2E: Docker Desktop started `opea/embedding:latest`, Hugging Face TEI, Qdrant, and the Manufacturing Gateway; `/v1/embeddings` returned 768-dimensional embeddings; all five demos reported `qdrant-opea-tei-vector-store`; `/v1/scorecard` passed.
- GCP C3 official OPEA TEI E2E: Google Cloud C3 `c3-standard-4` single-node 4-vCPU / 16-GiB-RAM / no-GPU fresh-clone run captured in `us-central1-a`; Docker Compose started Qdrant, `opea/embedding:latest`, Hugging Face TEI, and the Manufacturing Gateway; 768-dimensional embeddings, five `qdrant-opea-tei-vector-store` route demos, and `/v1/scorecard` passed; temporary VM `wearedge-opea-tei-0527103938` was deleted after the run.

## Bonus URLs And Artifacts

- `publication_url`: `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh`
- `publication_record_url`: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1`
- OPEA RFC issue: `https://github.com/opea-project/GenAIExamples/issues/2461`
- OPEA upstream PR: `https://github.com/opea-project/GenAIExamples/pull/2462`
- OPEA TEI update comment: `https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017`
- OPEA tracker: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`
- Upstream PR record: `docs/upstream-pr-attempt-2026-05-28.md`
- OPEA RFC issue draft: `docs/opea-upstream/rfc-issue-draft.md`
- OPEA blueprint feedback: `docs/opea-upstream/blueprint-feedback.md`
- OPEA contribution package used for PR #2462: `docs/opea-upstream/pr-ready/`
- OPEA PR patch artifact: `docs/opea-upstream/pr-ready/0001-add-manufacturing-agent-suite.patch`
- Champion risk burn-down: `docs/champion-risk-burn-down.md`
- OPEA native depth matrix: `docs/opea-native-depth-matrix.md`
- Production LLM benchmark path: `docs/production-llm-benchmark-path.md`
- GenAIEval-compatible evaluation: `docs/genaieval-compatible-evaluation.md`
- GenAIEval-compatible route eval JSON: `evidence/genaieval/route_eval_results.json`
- GenAIEval-compatible benchmark JSON: `evidence/genaieval/benchmark_results.json`
- Official OPEA profile: `docs/official-opea-profile.md`
- Official OPEA TEI profile: `docs/official-opea-tei-profile.md`
- Local OPEA TEI report: `docs/local-opea-tei-profile-e2e-report.md`
- GCP C3 OPEA TEI report: `docs/gcp-c3-opea-tei-profile-e2e-report.md`
- Submission URL dry run report: `docs/submission-url-dry-run.md`
- Local Docker Desktop final validation: `docs/local-docker-desktop-final-validation.md`
- GCP OPEA profile report: `docs/gcp-c3-opea-profile-e2e-report.md`
- Intel benchmark report: `docs/intel-avx512-amx-benchmark-report.md`
- Intel effective-use evidence: `docs/intel-effective-use-evidence.md`
- Intel effective-use summary JSON: `evidence/benchmarks/intel_effective_use.summary.json`
- GCP Docker/Qdrant E2E report: `docs/gcp-c3-docker-qdrant-e2e-report.md`
- Demo video source package: `public/demo-video/`
- Demo video render report: `docs/demo-video-render-report.md`
- Demo video URL: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4`
- Final form fill guide: `docs/final-submission-form-fill-guide.md`
- Local benchmark JSON: `evidence/benchmarks/intel_cpu_benchmark.local-smoke.json`
- Xeon AVX-512/AMX benchmark JSON: `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json`
- GCP Docker/Qdrant E2E summary JSON: `evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json`
- GCP OPEA profile E2E summary JSON: `evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json`
