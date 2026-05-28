# WearEdge GenAIEval-Compatible Evaluation Summary

Generated UTC: `2026-05-28T06:39:23+00:00`

Claim boundary: lightweight GenAIEval-compatible evidence package; not a full official GenAIEval/RAGAS/AutoRAG/LLM-as-judge run.

Overall: `ok=true`, `15/15` cases passed, pass rate `1.0`.

| Route | Cases | Passed | Pass rate | Mean eval latency ms | P95 eval latency ms | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `maintenance` | 3 | 3 | 1.0 | 1.1841 | 1.5958 | `pass` |
| `iqc` | 3 | 3 | 1.0 | 0.7547 | 0.8065 | `pass` |
| `changeover` | 3 | 3 | 1.0 | 0.6912 | 0.7244 | `pass` |
| `wi` | 3 | 3 | 1.0 | 0.738 | 0.8444 | `pass` |
| `hazard` | 3 | 3 | 1.0 | 0.7337 | 0.8059 | `pass` |

Metrics:

- `contract_pass`: `15/15` passed, pass rate `1.0`
- `action_target_correctness`: `15/15` passed, pass rate `1.0`
- `channel_correctness`: `15/15` passed, pass rate `1.0`
- `risk_level_correctness`: `15/15` passed, pass rate `1.0`
- `human_gate_correctness`: `15/15` passed, pass rate `1.0`
- `guardrail_pass`: `15/15` passed, pass rate `1.0`
- `rag_source_match`: `15/15` passed, pass rate `1.0`
- `route_isolation_pass`: `15/15` passed, pass rate `1.0`

Artifacts:

- `evals/genaieval/manufacturing_route_eval.dataset.jsonl`
- `evals/genaieval/manufacturing_route_benchmark.yaml`
- `evals/genaieval/run_wear_edge_eval.py`
- `evals/genaieval/run_wear_edge_benchmark.py`
- `evidence/genaieval/route_eval_results.json`
- `evidence/genaieval/benchmark_results.json`
- `evidence/genaieval/summary.md`
