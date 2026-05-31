# WearEdge GenAIEval-Compatible Evaluation Pack

This folder adds a lightweight GenAIEval-compatible evaluation layer for the
WearEdge OPEA Manufacturing project. It is intentionally dependency-free so
evaluators can run it from a fresh clone.

Claim boundary: this package provides a GenAIEval-compatible dataset, benchmark
config, runner, metrics, and evidence outputs. It does not claim full official
GenAIEval, RAGAS, AutoRAG, or LLM-as-evaluator execution.

## Run

```powershell
$env:PYTHONPATH="src"
python evals\genaieval\run_wear_edge_eval.py --output evidence\genaieval\route_eval_results.json --summary-output evidence\genaieval\summary.md
python evals\genaieval\run_wear_edge_benchmark.py --iterations 20 --output evidence\genaieval\benchmark_results.json
```

## What It Measures

- `contract_pass`: action card contains the required structured fields.
- `action_target_correctness`: route maps to the expected CMMS/QMS/MES/WI/EHS target.
- `channel_correctness`: route produces the expected action channel for the case.
- `risk_level_correctness`: deterministic evaluator reports the expected risk level.
- `human_gate_correctness`: human confirmation matches route and risk expectations.
- `guardrail_pass`: blocked claims include required restrictions and exclude route-isolation conflicts.
- `rag_source_match`: source IDs come from the expected route knowledge base.
- `route_isolation_pass`: each mode stays inside its own route, target, and claim boundary.

## Artifacts

- `manufacturing_route_eval.dataset.jsonl`: 15 cases across five Manufacturing agents.
- `manufacturing_route_benchmark.yaml`: GenAIEval-compatible benchmark metadata.
- `run_wear_edge_eval.py`: route metric runner.
- `run_wear_edge_benchmark.py`: latency and throughput runner.
- `evidence/genaieval/route_eval_results.json`: generated route evaluation evidence.
- `evidence/genaieval/benchmark_results.json`: generated benchmark evidence.
- `evidence/genaieval/summary.md`: generated human-readable summary.
