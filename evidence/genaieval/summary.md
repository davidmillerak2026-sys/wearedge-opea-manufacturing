# WearEdge GenAIEval-Compatible Evaluation Summary

Generated UTC: `2026-06-05T04:48:50+00:00`

Claim boundary: lightweight GenAIEval-compatible evidence package; not a official GenAIEval/RAGAS/AutoRAG/LLM-as-evaluation run.

Overall: `ok=true`, `15/15` cases passed, pass rate `1.0`.

| Route | Cases | Passed | Pass rate | Mean eval latency ms | P95 eval latency ms | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `maintenance` | 3 | 3 | 1.0 | 1.0359 | 1.1333 | `pass` |
| `iqc` | 3 | 3 | 1.0 | 0.935 | 1.0084 | `pass` |
| `changeover` | 3 | 3 | 1.0 | 0.7804 | 0.81 | `pass` |
| `wi` | 3 | 3 | 1.0 | 0.8651 | 1.008 | `pass` |
| `hazard` | 3 | 3 | 1.0 | 0.859 | 0.9252 | `pass` |

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
