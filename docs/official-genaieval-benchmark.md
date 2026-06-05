# Official GenAIEval Benchmark Path

Date: 2026-06-05

## Status

Official GenAIEval `chatqna.e2e` benchmark integration is prepared and has
been executed locally against the WearEdge Gateway.

What is implemented:

- WearEdge Gateway exposes `/v1/chatqna` as a GenAIEval `chatqna.e2e`
  compatible alias.
- `evals/genaieval/official_wearedge_benchmark.yaml` follows the official
  OPEA GenAIEval benchmark YAML shape.
- `scripts/run_official_genaieval_benchmark.ps1` copies the YAML into a local
  official GenAIEval checkout and runs `evals/benchmark/benchmark.py`.
- `evidence/genaieval/official_benchmark_summary.json` records the latest
  official local run summary.

Official reference checked:

```text
https://github.com/opea-project/GenAIEval
HEAD: b4fe6fc20f69ed3644525bd71c2e1f5ed7955dfd
```

## Why This Is First Stage

The existing `evals/genaieval/` runner remains dependency-free and already
records 15 route cases and a 300-call benchmark. The official GenAIEval
benchmark path is heavier because it depends on the OPEA benchmark framework,
`stresscli`, and Locust.

This gives the project a real official-entry YAML, a compatible service
endpoint, and captured official benchmark evidence without weakening the
default dependency-light reproducible path.

## Run

Start the WearEdge gateway first:

```powershell
$env:PYTHONPATH="src"
python -m wear_edge_opea.gateway
```

In another terminal:

```powershell
.\scripts\run_official_genaieval_benchmark.ps1
```

The script sets `MODEL_NAME=bert-base-uncased` by default because the official
`aistress.py` loader currently uses `MODEL_NAME` for tokenizer statistics and
otherwise defaults to the gated `meta-llama/Meta-Llama-3-8B-Instruct` model.
Override it only if the selected tokenizer is public or already available in
your Hugging Face cache:

```powershell
.\scripts\run_official_genaieval_benchmark.ps1 -TokenizerModel "bert-base-uncased"
```

On native Windows, the wrapper applies a local compatibility patch to the
checked-out GenAIEval `stresscli` copy so Locust runs without the unsupported
`--processes` flag. It also checks the latest output directory for internal
tracebacks and requires Locust `*_stats.csv` files before treating the run as
valid.

Before invoking the official runner, the wrapper validates that the tokenizer
can be loaded from the local Hugging Face cache. If it is not cached, it attempts
one online fetch, then forces Hugging Face offline mode for the benchmark runs
to avoid per-run network flakiness.

If the official dependencies are not installed in the selected Python
environment, use:

```powershell
.\scripts\run_official_genaieval_benchmark.ps1 -InstallDeps
```

The script uses `C:\tmp\GenAIEval` by default. Override it if needed:

```powershell
.\scripts\run_official_genaieval_benchmark.ps1 -GenAIEvalDir "D:\GenAIEval"
```

## Benchmark Target

The official tool will target:

```text
http://127.0.0.1:8088/v1/chatqna
```

For the official `chatqnafixed` benchmark path, the alias returns SSE events
compatible with the OPEA Locust parser. For JSON inspection, send
`"stream": false`; that response returns an OpenAI-like shape with
`choices[0].message.content` and preserves the full WearEdge result under
`wear_edge_result` for route, RAG, evaluator, guardrail, and action-card
inspection.

## Claim Boundary

Safe wording after this stage:

```text
WearEdge includes an official GenAIEval benchmark configuration, a GenAIEval
chatqna.e2e compatible endpoint alias, and a captured official local benchmark
summary.
```

After the official benchmark script completes and output artifacts are captured,
the following wording is also supported:

```text
Official OPEA GenAIEval benchmark executed against the WearEdge Gateway.
```

Do not claim RAGAS, AutoRAG, or LLM-as-evaluator execution from this first-stage
benchmark path. Those are separate evaluation tracks.
