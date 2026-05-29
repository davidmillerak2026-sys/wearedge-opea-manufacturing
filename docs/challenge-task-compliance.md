# Challenge Task Compliance

Date: 2026-05-28

This document maps the official challenge task to the submitted WearEdge Pro
OPEA Manufacturing package. The wording uses the challenge term "prototype"
only to describe the executable evaluation deliverable; WearEdge Pro itself is
a real industrial AI agent system.

## 1. Domain-Specific GenAI Application

WearEdge Pro is submitted as a Manufacturing GenAI application using OPEA-style
modular components:

| Required capability | WearEdge implementation | Evidence |
| --- | --- | --- |
| LLMs | OpenAI/OPEA-compatible LLM adapter with deterministic fallback and endpoint benchmark harness | `src/wear_edge_opea/llm_adapter.py`, `scripts/llm_adapter_benchmark.py`, `docs/production-llm-benchmark-path.md` |
| Embedding models | OPEA-compatible `/v1/embeddings` profile plus official OPEA TEI embedding profile | `docker-compose.opea.yml`, `docker-compose.opea-tei.yml`, `docs/official-opea-tei-profile.md` |
| Retrieval modules | Route-specific Retriever/RAG over manufacturing knowledge sources | `src/wear_edge_opea/rag.py`, `data/maintenance_kb/`, `data/agent_kb/` |
| Vector database | Qdrant collections per route, with in-memory fallback for dependency-free local execution | `docker-compose.yml`, `src/wear_edge_opea/vector_store.py` |
| Prompt / reasoning layer | Route-specific bounded explanation and action-card contract | `src/wear_edge_opea/llm_stub.py`, `src/wear_edge_opea/agents.py` |
| Orchestration workflow | Gateway -> Manufacturing Megaservice -> Dataprep -> RAG -> LLM adapter -> evaluator -> guardrails -> action card | `src/wear_edge_opea/gateway.py`, `src/wear_edge_opea/megaservice.py` |
| Evaluation methodology | `/v1/scorecard` and lightweight GenAIEval-compatible route evaluation pack | `src/wear_edge_opea/scorecard.py`, `evals/genaieval/`, `evidence/genaieval/` |

## 2. Concrete Industry Scenario

The selected vertical is Manufacturing. The submitted package covers five
frontline enterprise workflows instead of a single chatbot. The real product
has private enterprise production-data lineage; the public challenge package
uses sanitized fixtures so customer images, labels, lot IDs, and plant records
are not exposed.

| Agent | Enterprise workflow | Integration target |
| --- | --- | --- |
| `maintenance` | Lao-shi-fu predictive maintenance from M400/edge evidence | `maintenance_work_order` |
| `iqc` | IQC/OQC quality inspection, including private lineage such as toothbrush workshop visual inspection | `qms_quality_event` |
| `changeover` | SKU changeover and first-piece verification | `changeover_checklist` |
| `wi` | Released work-instruction guidance | `wi_reference` |
| `hazard` | EHS hazard observation and stop-and-make-safe escalation | `ehs_case` |

## 3. Working Prototype With Documentation

The executable challenge deliverable is the Docker-runnable OPEA Manufacturing
Agent Suite package for WearEdge Pro.

| Requirement | Submission evidence |
| --- | --- |
| Functioning source code | `src/wear_edge_opea/`, `docker-compose.yml`, `docker-compose.opea-tei.yml` |
| README | `README.md` |
| Technical report under 2 pages | `TECHNICAL_REPORT.md`; source draft retained at `docs/technical-report.draft.md` |
| Architecture and component usage | `README.md`, `docs/opea-component-evidence.md`, `docs/opea-native-depth-matrix.md` |
| Deployment strategy | `README.md`, `deploy.sh`, `docker-compose.yml`, `docker-compose.opea.yml`, `docker-compose.opea-tei.yml` |
| Use-case alignment | `SUBMISSION.md`, `docs/submission-product-shape.md`, `docs/telecom-scope-and-manufacturing-positioning.md` |
| OneClick setup | `docker compose up --build -d` and `./deploy.sh` |

OneClick smoke path:

```bash
docker compose up --build -d
curl http://127.0.0.1:8088/healthz
curl http://127.0.0.1:8088/v1/agents
curl http://127.0.0.1:8088/v1/scorecard
```

## 4. Performance And Usability

WearEdge was validated inside the challenge hardware envelope and includes
explicit response-time, memory-footprint, and user-experience evidence.

| Metric requested by challenge | WearEdge evidence |
| --- | --- |
| Typical enterprise hardware | Google Cloud C3 `c3-standard-4`, single node, 4 vCPU, 16 GiB RAM, no GPU |
| Installation and initial run within 10 minutes | Default Docker/Qdrant C3 timed run on VM `wearedge-docker-e2e-0529041313` reached `setup_seconds=23`, `clean_initial_run_seconds=45`, `validation.clean_initial_run_under_10_min=true`, and `all_checks_pass=true` |
| System response time | C3 Docker/Qdrant E2E latency JSON and official OPEA TEI E2E route timings |
| Memory footprint | Docker stats for Gateway, Qdrant, `opea/embedding:latest`, and TEI serving containers |
| Scalability under requests | Local concurrent route benchmark with 8 workers / 100 total requests passing, GenAIEval-compatible benchmark with 300 route evaluations, plus endpoint benchmark harnesses for route and LLM adapter paths |
| User experience clarity | Upgraded browser command console at `/demo`, public YouTube walkthrough, public Dev.to article, OPEA docs Publications PR #395, route-specific action cards, RAG source evidence, OPEA pipeline rail, and scorecard state |

Key evidence files:

```text
evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json
evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json
evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json
evidence/benchmarks/intel_effective_use.summary.json
evidence/benchmarks/route_concurrency.local-smoke.json
evidence/genaieval/benchmark_results.json
docs/local-docker-desktop-final-validation.md
docs/intel-effective-use-evidence.md
```

Claim boundary: these records prove application-level WearEdge OPEA workloads
running on the target hardware profile. They do not claim certified safety
release, autonomous maintenance release, TEI-internal AMX dispatch proof, or
production LLM acceleration without a separately configured endpoint benchmark.
The r23/r24 hardware evidence does include same-host oneDNN BF16/AMX probe
dispatch markers on the same C3 VM as the OPEA TEI/Qdrant/five-agent scorecard
path.
