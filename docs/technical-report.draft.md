# WearEdge Pro: OPEA Manufacturing Five-Agent Suite

## 1. Problem And Business Value

Manufacturing operators see early evidence before enterprise systems do: abnormal machine sound, visible defects, label mix-up risk, unclear work-instruction steps, missing PPE, blocked walkways, and unsafe moving-parts exposure. These observations often stay as verbal handoffs instead of becoming structured maintenance, quality, MES, work-instruction, or EHS records.

WearEdge Pro addresses this "last ten meters" problem with a wearable edge AI workflow. A Vuzix M400 captures first-person evidence, an edge gateway runs OPEA-style orchestration, route-specific RAG retrieves the released knowledge source, deterministic evaluators check thresholds or confirmations, and guardrails produce bounded action cards for human-confirmed plant workflows.

The challenge submission packages this product as a Docker-runnable OPEA Manufacturing Agent Suite with a browser demo console at `/demo`. The M400 Android client remains the real deployment front end and field-evidence source, but the judge-facing artifact is the reproducible Web/API package in this repository.

The submission covers five Manufacturing agents:

| Agent | Target workflow | Action target |
| --- | --- | --- |
| `maintenance` | Lao-shi-fu predictive maintenance for `PKG-L3-GBX-03` | `maintenance_work_order` |
| `iqc` | Machined aluminum housing quality inspection | `qms_quality_event` |
| `changeover` | Labeler SKU-C500 changeover verification | `changeover_checklist` |
| `wi` | Released work-instruction guidance for `CARTONER-ST2` | `wi_reference` |
| `hazard` | PPE, moving-parts, and walkway hazard observation | `ehs_case` |

## 2. OPEA Architecture Mapping

```text
M400 / API request
  -> Gateway
  -> Manufacturing Megaservice
  -> route registry: maintenance / iqc / changeover / wi / hazard
  -> Dataprep + route-specific knowledge source
  -> Retriever / RAG + Qdrant Vector DB profile
  -> optional OPEA-compatible Embedding Microservice /v1/embeddings
  -> optional official OPEA TEI Embedding Microservice profile
  -> OpenAI/OPEA-compatible LLM service adapter or deterministic no-model evaluation path
  -> route-specific evaluator
  -> Guardrails and blocked claims
  -> CMMS / QMS / MES / WI / EHS action card
```

Current component claim: `LLM`, `RAG`, `Vector DB`, `Orchestration`, `Guardrails`.

The submitted Docker Compose profile starts Qdrant and a FastAPI Manufacturing Gateway. The local runtime can also run without dependencies through an in-memory vector fallback. This keeps the evaluation package reproducible while preserving the OPEA component boundaries. An optional `docker-compose.opea.yml` profile adds a separate OPEA-compatible `/v1/embeddings` microservice and configures the Gateway to call it during Qdrant indexing and retrieval. A second optional `docker-compose.opea-tei.yml` profile follows the official OPEA TEI embedding pattern by connecting Hugging Face TEI to the OPEA embedding microservice through `TEI_EMBEDDING_ENDPOINT` and `EMBEDDING_COMPONENT_NAME=OPEA_TEI_EMBEDDING`; that profile has local Docker Desktop and Google Cloud C3 fresh-clone E2E evidence. The LLM boundary is implemented through an OpenAI/OPEA-compatible adapter with a benchmark harness; the submitted default remains deterministic unless a real endpoint is configured.

## 3. Implementation

The route registry defines each agent's business value, entity key, sample request, knowledge source, integration target, owner, human gate, and blocked claims. The same megaservice code runs all five agents; differences are driven by data and route-specific deterministic evaluation.

Examples:

- Maintenance evaluates vibration, gearbox temperature, bearing temperature, lubrication interval, and PLC alarm before creating a CMMS work-order draft.
- IQC evaluates detector confidence against a released quality plan before holding a lot in QMS.
- Changeover checks line clearance, label roll, recipe, and first-piece verification before restart sign-off.
- WI uses released work-instruction evidence and blocks guidance when identity, revision, guard, or alarm context is unsafe.
- Hazard converts PPE, moving-parts, and blocked-walkway evidence into EHS action cards without granting safety clearance.

The full engineering project also contains the M400 Android client, Jetson FastAPI gateway, local edge LLM path, audit logs, runtime stream, and more than 120 local tests. This OPEA repository packages the judge-facing runnable path.

## 4. Product Evidence And Evaluation

Runnable commands:

```bash
docker compose up --build -d
# Open in browser: http://127.0.0.1:8088/demo
curl http://127.0.0.1:8088/v1/agents
curl http://127.0.0.1:8088/v1/manufacturing/suite
curl http://127.0.0.1:8088/v1/scorecard
```

The scorecard reports:

- route latency
- contract pass
- guardrail pass
- RAG/source match
- action target correctness
- route isolation

The repository also includes a lightweight GenAIEval-compatible evaluation pack
under `evals/genaieval/`. It provides a JSONL dataset, benchmark metadata,
runner scripts, metric outputs, and committed evidence under
`evidence/genaieval/`. The captured local run reports 15/15 cases passing across
contract, target, channel, risk, human gate, guardrail, RAG source, and
route-isolation metrics, plus a 300-call route benchmark. This is intentionally
claimed as GenAIEval-compatible evidence, not full official GenAIEval/RAGAS/
AutoRAG/LLM-as-judge execution.

Archived WearEdge-Pro evidence includes a real Vuzix M400 -> Jetson -> local edge LLM -> M400 result chain, lao-shi-fu multi-evidence maintenance validation, five-agent validation, power/runtime notes, and edge-runtime benchmark records. The OPEA submission package was also fresh-cloned on Google Cloud C3 `c3-standard-4` single-node 4-vCPU / 16-GiB-RAM / no-GPU configurations, started with Docker Compose, verified Qdrant plus the Manufacturing Gateway, passed all five demo and infer routes, and passed `/v1/scorecard`.

## 5. Safety, Licensing, And Limits

WearEdge Pro is MIT licensed. It is an assistive industrial AI decision-support system, not a certified industrial safety controller or autonomous maintenance-release system. Guardrails block unsupported claims including final root cause, remaining useful life, restart permission, quality release, safety clearance, incident root cause, and maintenance release. High-risk outputs require human confirmation.

Bonus evidence package: the OPEA RFC issue is posted at `https://github.com/opea-project/GenAIExamples/issues/2461`, the upstream implementation and official TEI update comments are posted in that issue, upstream PR #2462 is open at `https://github.com/opea-project/GenAIExamples/pull/2462`, the public OPEA tracker is posted at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2`, the technical article is recorded at `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1`, and the Intel benchmark harness plus Google Cloud C3 Xeon AVX-512/AMX JSON are in `scripts/intel_cpu_benchmark.py` and `evidence/benchmarks/`. The Docker/Qdrant, OPEA-compatible embedding, official OPEA TEI, local Docker Desktop, submission URL dry-run, upstream PR evidence and patch, LLM adapter benchmark path, champion risk burn-down, and public demo video evidence are all linked from `docs/final-submission-readiness-audit.md`.
