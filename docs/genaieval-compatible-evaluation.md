# GenAIEval-Compatible Evaluation

This submission includes a lightweight GenAIEval-compatible evaluation pack for
the five WearEdge Manufacturing agents.

Claim boundary: the artifacts in `evals/genaieval/` provide a GenAIEval-style
dataset, benchmark config, runner, metrics, and evidence JSON. They do not claim
full official GenAIEval, RAGAS, AutoRAG, or LLM-as-judge execution.

## Why It Exists

The challenge asks teams to show OPEA-style technical implementation,
efficiency, and prototype quality. OPEA also highlights standardized evaluation
as part of the ecosystem. The existing `/v1/scorecard` is useful for live API
verification; this package makes that evaluation reproducible as committed
artifacts that judges can rerun from a fresh clone.

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

## Submission Wording

Safe wording:

```text
The project includes a lightweight GenAIEval-compatible evaluation package:
a JSONL dataset, benchmark metadata, deterministic runner, route metrics, and
committed evidence outputs for 15 cases across five Manufacturing agents.
```

Avoid:

```text
Fully integrated official GenAIEval with RAGAS, AutoRAG, and LLM-as-judge.
```
