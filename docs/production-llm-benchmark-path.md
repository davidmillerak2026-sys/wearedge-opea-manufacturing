# Production LLM Benchmark Path

Date: 2026-06-05

## Status

The reproducible sample path remains deterministic by default so evaluators can run it
without model credentials or a large model download. The LLM service boundary is
now implemented as a real adapter:

```text
Manufacturing Megaservice
  -> llm_adapter.generate_explanation()
  -> deterministic template by default
  -> OpenAI/OPEA-compatible chat completions endpoint when configured
  -> action-card explanation + runtime metadata
```

Runtime files:

```text
src/wear_edge_opea/llm_adapter.py
scripts/llm_adapter_benchmark.py
scripts/lmm_image_benchmark.py
evidence/benchmarks/llm_adapter_contract.local-smoke.json
evidence/benchmarks/llm_adapter.local-gemma.json
evidence/benchmarks/llm_adapter.deepseek.json
docs/local-gemma-llm-benchmark.md
```

## Local Contract Smoke Test

```powershell
$env:PYTHONPATH="src"
python scripts\llm_adapter_benchmark.py --iterations 1 `
  --output evidence\benchmarks\llm_adapter_contract.local-smoke.json
```

Expected committed status:

```text
claim_status=deterministic_llm_adapter_contract_smoke_test
fallback_count=0
all_contracts_pass=true
production_endpoint_used=false
```

This is a contract test, not a production LLM acceleration claim.

## Local Gemma Benchmark

An OpenAI API key is not required if a local model service is available. The
requirement is a real model endpoint. A local Gemma model can be benchmarked
through Ollama native `/api/chat` or an OpenAI-compatible local server such as
LM Studio, vLLM, or llama.cpp.

Examples:

```powershell
$env:PYTHONPATH="src"
python scripts\llm_adapter_benchmark.py --local-profile ollama `
  --model <your-gemma-model-name> `
  --strict --iterations 1 `
  --output evidence\benchmarks\llm_adapter.local-gemma.json
```

```powershell
$env:PYTHONPATH="src"
python scripts\llm_adapter_benchmark.py --local-profile lmstudio `
  --model <lm-studio-model-id> `
  --strict --iterations 1 `
  --output evidence\benchmarks\llm_adapter.local-gemma.json
```

Use local model wording only when the output says:

```text
claim_status=local_llm_endpoint_benchmarked
local_endpoint_used=true
fallback_count=0
all_contracts_pass=true
```

See [`docs/local-gemma-llm-benchmark.md`](local-gemma-llm-benchmark.md).

## Current Decision

Do not claim a production LLM or LMM end-to-end benchmark unless a real model
endpoint is configured and the benchmark output proves:

```text
production_endpoint_used=true
fallback_count=0
all_contracts_pass=true
```

The current repository is endpoint-ready and has both local-model and
production-endpoint evidence captured. It should be described as local-model
benchmarked only when `llm_adapter.local-gemma.json` reports strict
no-fallback success, and production-endpoint benchmarked only when a remote
production endpoint reports strict no-fallback success. That boundary protects
the project from over-claiming when evidence is refreshed.

## Captured Local Gemma Benchmark

A strict local WSL/Ollama `gemma4:31b` endpoint run is captured in:

```text
evidence/benchmarks/llm_adapter.local-gemma.json
```

Captured result:

```text
claim_status=local_llm_endpoint_benchmarked
local_endpoint_used=true
production_endpoint_used=false
fallback_count=0
all_contracts_pass=true
total_calls=5
```

## Captured DeepSeek Endpoint Benchmark

A strict DeepSeek OpenAI-compatible endpoint run is captured in:

```text
evidence/benchmarks/llm_adapter.deepseek.json
```

Captured result:

```text
claim_status=production_llm_endpoint_benchmarked
fallback_count=0
production_endpoint_used=true
all_contracts_pass=true
total_calls=5
```

The artifact records only safe metadata such as endpoint URL, model name,
latency, fallback count, and pass/fail status. It does not store the API key.

This statement applies to the text-only LLM explanation adapter. The
multimodal image path now also has a separate strict LMM benchmark harness and
a passing external endpoint artifact for the public oil-leak fixture.

## Production Endpoint Benchmark

Use this only when an OpenAI-compatible OPEA LLM endpoint, vLLM proxy, or other
chat-completions service is available:

```bash
export PYTHONPATH=src
export WEAREDGE_LLM_BACKEND=openai-compatible
export WEAREDGE_LLM_URL=http://<llm-service>:<port>/v1/chat/completions
export WEAREDGE_LLM_MODEL=<model-id>
export WEAREDGE_LLM_STRICT=true
python scripts/llm_adapter_benchmark.py \
  --iterations 5 \
  --output evidence/benchmarks/llm_adapter.production.json
```

Only use production LLM wording when the output says:

```text
claim_status=production_llm_endpoint_benchmarked
fallback_count=0
production_endpoint_used=true
all_contracts_pass=true
```

## Multimodal LMM/VLM Benchmark Boundary

The real WearEdge product uses M400 visual evidence and private
quality-inspection lineage. The mother repository has already run a real edge
VLM path on Jetson:

```text
WearEdge-Pro /v1/infer
  -> llama.cpp /v1/chat/completions
  -> Gemma 4 E2B Q4_K_S + mmproj-F16
  -> route-specific contract validation
  -> action cards and audit logs
```

Source evidence is mapped in
[`docs/source-vlm-e2e-evidence-map.md`](source-vlm-e2e-evidence-map.md). In
this OPEA public package, visual evidence is represented through structured
detector fields, observations, source IDs, and guarded action cards so the
package stays runnable without private images or a large vision model.

The model strategy is intentionally modular:

- local Jetson/Gemma 4 E2B proves WearEdge is not a cloud-wrapper;
- external LMM endpoints such as Gemini prove the same agent pipeline can use
  enterprise-hosted or cloud-hosted vision models;
- OpenAI/OPEA-compatible adapters keep the Gateway, Megaservice, RAG,
  evaluator, guardrail, and action-card layers unchanged when the model changes.

A true production LMM/VLM end-to-end benchmark would require:

- an image-capable endpoint;
- a redacted image set cleared for public benchmark use;
- strict no-fallback execution;
- route-level pass/fail metrics for IQC, hazard, and maintenance observations.

The strict public oil-leak benchmark harness is now included:

```text
scripts/lmm_image_benchmark.py
docs/lmm-machine-oil-leak-benchmark-report.md
evidence/images/machine_oil_leak.png
```

With the source Jetson/Gemma evidence and the strict public oil-leak LMM run,
the honest claim is:

```text
WearEdge-Pro has a real edge VLM product path and visual-evidence lineage, and
the OPEA project is model-flexible by design. The same five-agent
manufacturing pipeline can run with a local Jetson/Gemma 4 E2B VLM or attach
to external production LMM APIs through a strict adapter boundary, while the
OPEA-native package remains reproducible with TEI, Qdrant, guardrails, and
scorecards.
```

## Why This Matters

This closes the architectural gap without weakening reproducibility:

- evaluators can run the no-secret deterministic path immediately;
- the same megaservice now exposes LLM runtime metadata in `/demo` results;
- real local and cloud endpoint benchmarks can be attached or refreshed without
  rewriting the agent pipeline;
- the project stays honest about what was actually benchmarked.
