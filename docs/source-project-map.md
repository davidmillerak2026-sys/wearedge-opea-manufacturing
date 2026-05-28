# Source Project Map

This repository is the dedicated OPEA Manufacturing submission package. It
contains the complete runnable OPEA challenge product: Gateway, five-agent
route registry, Manufacturing Megaservice, RAG, Qdrant/TEI profiles, LLM
adapter, guardrails, scorecard, browser console, evaluation pack, tests, and
evidence scripts.

The broader WearEdge-Pro engineering source tree is in:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

## Mapping

| Submission claim | Source project path |
| --- | --- |
| Gateway | `jetson/app.py`, `scripts/run_fastapi.sh` |
| LLM service adapter | `jetson/llama_client.py`, `scripts/run_llama_server.sh` |
| Five-agent manufacturing orchestration | `jetson/agently_orchestrator.py`, `jetson/agent_loop.py`, `jetson/agent_profiles.py` |
| Maintenance session | `jetson/maintenance_session.py` |
| Maintenance RAG / KB | `jetson/maintenance_kb.py`, `data/maintenance_kb/pkg_l3_gbx_03.json` |
| IQC quality plan | `data/iqc_quality_plans/al_housing_line3.json`, `jetson/iqc_quality_eval.py` |
| Changeover and WI released sources | `data/released_sources/`, `jetson/released_source.py` |
| Deterministic evaluator | `jetson/maintenance_signal_eval.py` |
| Output contract | `jetson/output_contract.py` |
| Source guard | `jetson/released_source.py`, `data/released_sources/` |
| Industrial RAG agent | `industrial-rag-agent/` |
| M400 client | `clients/m400/android/` |
| Judge-facing Web Demo Console | `src/wear_edge_opea/demo_console.py` in this OPEA submission repo |
| Deployment | `scripts/`, `deploy/systemd/` |
| Tests | `tests/` |
| Benchmark | `docs/edge-runtime-benchmark.md` |
| ROI | `docs/impact-and-roi.md` |
| Evidence logs | `docs/poc-results/` |

## Real VLM E2E Source Evidence

The WearEdge-Pro mother repository has a real VLM path that has already run on
Jetson:

```text
M400/browser image
  -> FastAPI /v1/infer
  -> llama.cpp /v1/chat/completions
  -> Gemma 4 E2B Q4_K_S + mmproj-F16
  -> route-specific contract validation
  -> agent loop / guardrails / action card / audit log
```

The source evidence is mapped in
[`source-vlm-e2e-evidence-map.md`](source-vlm-e2e-evidence-map.md), with a
machine-readable summary in
[`../evidence/source-wearedge-vlm/e2e-summary.json`](../evidence/source-wearedge-vlm/e2e-summary.json).

Important boundary: this OPEA repository is the judge-runnable OPEA package;
WearEdge-Pro is the product evidence repository for M400, Jetson, VLM, and
field workflow proof. The two repositories should be presented as one product
with two surfaces, not as unrelated demos.

## Code Quality Position

Do not frame the challenge repository as "only docs" or "only a wrapper." The
correct position is:

```text
wearedge-opea-manufacturing is the full runnable OPEA challenge product
package. WearEdge-Pro is the broader industrial engineering repository for
M400 Android, Jetson edge runtime, field evidence, and larger product history.
```

Why not move every WearEdge-Pro file here?

- The OPEA challenge asks for a working prototype with documentation and
  one-click setup, not a full monorepo dump.
- Customer/private production data and plant-specific artifacts must not be
  published.
- Keeping the OPEA package focused improves judge reproducibility and code
  review.

Optional final hardening:

1. Keep `WearEdge-Pro` as the full engineering repository.
2. Keep `wearedge-opea-manufacturing` as the competition landing repository.
3. If judges need deeper code review, add a source-release snapshot or mirror
   selected M400/Jetson directories with private data removed.

The safest official `project_url` is this OPEA submission repository because it contains the reproducible Docker/Web/API evaluation path. The full WearEdge-Pro repository remains the engineering source for the M400 Android client, Jetson edge gateway, and field evidence.
