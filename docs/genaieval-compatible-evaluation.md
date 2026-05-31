# GenAIEval-Compatible Evaluation

This project includes a lightweight GenAIEval-compatible evaluation pack for
the five WearEdge Manufacturing agents.

Claim boundary: the artifacts in `evals/genaieval/` provide a GenAIEval-style
dataset, benchmark config, runner, metrics, and evidence JSON. They do not claim
official GenAIEval, RAGAS, AutoRAG, or LLM-as-evaluator execution.

## Why It Exists

The program asks teams to show OPEA-style technical implementation,
efficiency, and product quality. OPEA also highlights standardized
evaluation as part of the ecosystem. The existing `/v1/scorecard` is useful for live API
verification; this package makes that evaluation reproducible as committed
artifacts that evaluators can rerun from a fresh clone.

## Evaluation Shape

```text
JSONL route dataset
  -> WearEdge Manufacturing Megaservice
  -> RAG/source evidence
  -> deterministic evaluator
  -> guardrails/action card
  -> GenAIEval-compatible metrics JSON
  -> benchmark JSON and summary.md
```

The dataset contains 15 cases: three each for `maintenance`, `iqc`,
`changeover`, `wi`, and `hazard`.

Metrics:

- `contract_pass`
- `action_target_correctness`
- `channel_correctness`
- `risk_level_correctness`
- `human_gate_correctness`
- `guardrail_pass`
- `rag_source_match`
- `route_isolation_pass`

## Run

```powershell
$env:PYTHONPATH="src"
python evals\genaieval\run_wear_edge_eval.py --output evidence\genaieval\route_eval_results.json --summary-output evidence\genaieval\summary.md
python evals\genaieval\run_wear_edge_benchmark.py --iterations 20 --output evidence\genaieval\benchmark_results.json
```

## Captured Result

The committed local evidence reports:

| Evidence | Result |
| --- | --- |
| Route evaluation | 15/15 cases passed |
| Routes covered | maintenance, IQC, changeover, WI, hazard |
| Metrics | contract, target, channel, risk, human gate, guardrail, RAG source, route isolation |

Companion concurrency evidence is stored in
`evidence/benchmarks/route_concurrency.local-smoke.json`. It records an
8-worker, 100-request local route benchmark with all requests and action targets
passing. This complements the 300-call GenAIEval-compatible benchmark by
addressing the program's concurrent-request usability/performance prompt.
| Benchmark calls | 300 route evaluations |
| Benchmark validation | all cases pass, all routes covered |

Artifacts:

- `evals/genaieval/manufacturing_route_eval.dataset.jsonl`
- `evals/genaieval/manufacturing_route_benchmark.yaml`
- `evals/genaieval/run_wear_edge_eval.py`
- `evals/genaieval/run_wear_edge_benchmark.py`
- `evidence/genaieval/route_eval_results.json`
- `evidence/genaieval/benchmark_results.json`
- `evidence/genaieval/summary.md`

## Project Wording

Safe wording:

```text
The project includes a lightweight GenAIEval-compatible evaluation package:
a JSONL dataset, benchmark metadata, deterministic runner, route metrics, and
committed evidence outputs for 15 cases across five Manufacturing agents.
```

Avoid:

```text
Fully integrated official GenAIEval with RAGAS, AutoRAG, and LLM-as-evaluator.
```
