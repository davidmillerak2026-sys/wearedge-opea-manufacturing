# Source Project Map

This repository is the dedicated OPEA Manufacturing submission package. The current full engineering source is in:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

## Mapping

| Submission claim | Source project path |
| --- | --- |
| Gateway | `jetson/app.py`, `scripts/run_fastapi.sh` |
| LLM service adapter | `jetson/llama_client.py`, `scripts/run_llama_server.sh` |
| Manufacturing orchestration | `jetson/agently_orchestrator.py`, `jetson/agent_loop.py` |
| Maintenance session | `jetson/maintenance_session.py` |
| Maintenance RAG / KB | `jetson/maintenance_kb.py`, `data/maintenance_kb/pkg_l3_gbx_03.json` |
| Deterministic evaluator | `jetson/maintenance_signal_eval.py` |
| Output contract | `jetson/output_contract.py` |
| Source guard | `jetson/released_source.py`, `data/released_sources/` |
| Industrial RAG agent | `industrial-rag-agent/` |
| M400 client | `clients/m400/android/` |
| Deployment | `scripts/`, `deploy/systemd/` |
| Tests | `tests/` |
| Benchmark | `docs/edge-runtime-benchmark.md` |
| ROI | `docs/impact-and-roi.md` |
| Evidence logs | `docs/poc-results/` |

## Publication Strategy

Preferred final strategy:

1. Keep `WearEdge-Pro` as the full engineering repository.
2. Keep `wearedge-opea-manufacturing` as the competition landing repository.
3. Before final submission, either mirror selected source directories into this repository or add a clear source release package so judges can reproduce from one place.

The safest official `project_url` is the URL that contains both source and OPEA submission evidence.

