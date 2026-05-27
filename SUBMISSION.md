# ITU AI for Good OPEA Manufacturing Submission

Challenge: Innovation Challenge on Generative AI Applications for Enterprise Scenarios Using OPEA

Vertical: Manufacturing

Application name: WearEdge Pro

## One-Sentence Summary

WearEdge Pro is an OPEA-aligned wearable edge AI suite for Manufacturing that routes first-person M400 evidence into five bounded agents: maintenance, IQC, changeover, work instruction, and hazard observation.

## Final Product Shape

The competition deliverable is not an Android-only APK. It is a Docker-runnable OPEA Manufacturing Agent Suite with a browser demo console and API surface.

Judge-facing entry point:

```text
http://127.0.0.1:8088/demo
```

The Vuzix M400 / Android client is the real deployment front end and field-evidence source from the full WearEdge-Pro product. The Web Demo Console is the reproducible evaluation surface for judges who do not have M400 hardware.

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

- OPEA issue/PR/blueprint feedback: public RFC issue posted at `https://github.com/opea-project/GenAIExamples/issues/2461`; public tracker posted at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`; PR remains pending maintainer feedback.
- OPEA-compatible embedding profile: `docker-compose.opea.yml` adds a separate `/v1/embeddings` microservice and routes Qdrant RAG embeddings through it.
- Official OPEA TEI profile: `docker-compose.opea-tei.yml` wires Hugging Face TEI, the OPEA embedding microservice, Qdrant, and the five agent routes for production embedding evidence; local E2E passed and the C3 fresh-clone rerun script is included.
- Knowledge sharing: public article is published at `public/article-wear-edge-opea-manufacturing.md` and recorded at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1`; video script and captions are ready in `public/`.
- Intel AVX-512/AMX: Google Cloud C3 `c3-standard-4` run captured on Intel Xeon Platinum 8481C with `avx512f`, `amx_tile`, `amx_int8`, and `amx_bf16` detected; scorecard passed.
- Docker/Qdrant E2E: Google Cloud C3 `c3-standard-4` fresh-clone run captured in `us-central1-a`; Docker Compose started Qdrant plus the Manufacturing Gateway, `/demo` returned HTTP 200, five demo routes and five infer routes returned correct action cards, `/v1/scorecard` passed, and the VM was deleted after the run.
- OPEA profile E2E: Google Cloud C3 `c3-standard-4` fresh-clone run captured in `us-central1-a`; Docker Compose started Qdrant, the OPEA-compatible `/v1/embeddings` service, and the Manufacturing Gateway; five routes reported `qdrant-opea-compatible-embedding-vector-store`, `/v1/scorecard` passed, and the VM was deleted after the run.
- Local official OPEA TEI E2E: Docker Desktop started `opea/embedding:latest`, Hugging Face TEI, Qdrant, and the Manufacturing Gateway; `/v1/embeddings` returned 768-dimensional embeddings; all five demos reported `qdrant-opea-tei-vector-store`; `/v1/scorecard` passed.

## Bonus URLs And Artifacts

- `publication_url`: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-wear-edge-opea-manufacturing.md`
- `publication_record_url`: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1`
- OPEA RFC issue: `https://github.com/opea-project/GenAIExamples/issues/2461`
- OPEA tracker: `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`
- OPEA RFC issue draft: `docs/opea-upstream/rfc-issue-draft.md`
- OPEA blueprint feedback: `docs/opea-upstream/blueprint-feedback.md`
- Official OPEA profile: `docs/official-opea-profile.md`
- Official OPEA TEI profile: `docs/official-opea-tei-profile.md`
- Local OPEA TEI report: `docs/local-opea-tei-profile-e2e-report.md`
- GCP OPEA profile report: `docs/gcp-c3-opea-profile-e2e-report.md`
- Intel benchmark report: `docs/intel-avx512-amx-benchmark-report.md`
- GCP Docker/Qdrant E2E report: `docs/gcp-c3-docker-qdrant-e2e-report.md`
- Local benchmark JSON: `evidence/benchmarks/intel_cpu_benchmark.local-smoke.json`
- Xeon AVX-512/AMX benchmark JSON: `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json`
- GCP Docker/Qdrant E2E summary JSON: `evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json`
- GCP OPEA profile E2E summary JSON: `evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json`
