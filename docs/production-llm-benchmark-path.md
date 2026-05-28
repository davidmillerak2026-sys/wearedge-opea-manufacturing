# Production LLM Benchmark Path

Date: 2026-05-28

## Status

The submitted demo path remains deterministic by default so judges can run it
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

## Current Decision

Do not claim a production LLM or LMM full-chain benchmark unless a real model
endpoint is configured and the benchmark output proves:

```text
production_endpoint_used=true
fallback_count=0
all_contracts_pass=true
```

The current repository is production-endpoint-ready, not production-endpoint
benchmarked. That boundary is intentional and protects the submission from
over-claiming.

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
this OPEA challenge package, visual evidence is represented through structured
detector fields, observations, source IDs, and guarded action cards so the
package stays runnable without private images or a large vision model.

A true production LMM/VLM full-chain benchmark would require:

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

Until those are available, the honest claim is:

```text
WearEdge-Pro has a real edge VLM product path and visual-evidence lineage.
The public OPEA submission benchmarks the OPEA TEI/RAG/action-card path with
official TEI and Qdrant, while preserving strict benchmark harnesses for real
LLM/LMM endpoints.
```

## Why This Matters For Scoring

This closes the architectural gap without weakening reproducibility:

- judges can run the no-secret deterministic path immediately;
- the same megaservice now exposes LLM runtime metadata in `/demo` results;
- a real endpoint benchmark can be attached later without rewriting the agent
  pipeline;
- the submission stays honest about what was actually benchmarked.
