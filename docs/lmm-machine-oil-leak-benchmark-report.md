# Strict LMM Oil-Leak Benchmark

Date: 2026-05-28

## Purpose

This benchmark closes the gap between the real WearEdge-Pro VLM evidence path
and the OPEA challenge package. It uses a public redacted oil-leak factory
fixture, calls a real image-capable endpoint with no fallback, parses a strict
maintenance JSON evidence contract, then feeds that evidence into the OPEA
Manufacturing Megaservice.

This is an external model-adapter benchmark, not a replacement for the local
WearEdge-Pro VLM product path. WearEdge-Pro has already validated a Jetson
deployment with local Gemma 4 E2B + `mmproj-F16`; this benchmark proves the
same manufacturing agent architecture can also attach to Gemini or any
OpenAI/OPEA-compatible image model API through the LMM adapter boundary.

Fixture:

```text
evidence/images/machine_oil_leak.png
```

Script:

```text
scripts/lmm_image_benchmark.py
```

## Strict Command

```powershell
$env:PYTHONPATH="src"
$env:WEAREDGE_LMM_PROVIDER="gemini"
$env:GEMINI_MODEL="gemini-2.5-flash"
python scripts\lmm_image_benchmark.py `
  --image evidence\images\machine_oil_leak.png `
  --output evidence\benchmarks\lmm_machine_oil_leak.strict.json `
  --strict
```

Use an OpenAI/OPEA-compatible image endpoint instead:

```powershell
$env:PYTHONPATH="src"
$env:WEAREDGE_LMM_PROVIDER="openai-compatible"
$env:WEAREDGE_LMM_URL="http://localhost:8000/v1/chat/completions"
$env:WEAREDGE_LMM_MODEL="<vision-model>"
python scripts\lmm_image_benchmark.py `
  --image evidence\images\machine_oil_leak.png `
  --output evidence\benchmarks\lmm_machine_oil_leak.strict.json `
  --strict
```

## Pass Criteria

The output may be cited as strict production LMM evidence only when:

```text
claim_status=strict_production_lmm_endpoint_benchmarked
all_checks_pass=true
validation.endpoint_used=true
validation.parsed_json=true
validation.recommended_agent_mode_maintenance=true
validation.action_target_maintenance_work_order=true
validation.restart_permission_blocked=true
validation.maintenance_release_blocked=true
validation.rag_sources_present=true
```

If the endpoint fails, the script writes
`claim_status=strict_lmm_endpoint_failed_no_fallback`. That is still useful
because it proves the benchmark is honest: it does not silently replace a real
LMM with a deterministic stub.

## Submission Claim Boundary

Use this wording after a passing run:

```text
We ran a strict image-to-action benchmark on a public oil-leak maintenance
fixture. A real image-capable endpoint extracted maintenance evidence, and the
OPEA Manufacturing Megaservice converted it into a guarded maintenance work
order action card with RAG source IDs and blocked restart/release claims.
Together with the Jetson/Gemma 4 E2B source evidence, this shows that WearEdge
can run with local edge VLMs or external production LMM APIs without changing
the five-agent OPEA pipeline.
```

Do not use this wording before a passing run:

```text
The default Docker demo includes production VLM inference.
```

## Current Run

Local strict endpoint run completed on 2026-05-28:

```text
provider=gemini
model=gemini-2.5-flash
claim_status=strict_production_lmm_endpoint_benchmarked
all_checks_pass=true
endpoint.latency_ms=6280.96
endpoint.promptTokenCount=693
endpoint.imageTokenCount=258
```

The LMM parsed the oil-leak fixture as `maintenance` for
`PKG-L3-GBX-03`. The OPEA pipeline then returned a guarded
`maintenance_work_order` action card with RAG source IDs and blocked
`restart_permission` / `maintenance_release` claims.

Submission wording should call this a model-flexibility result: Gemini was used
as one production-grade external endpoint, while the architecture also supports
local llama.cpp/Gemma 4 E2B and OpenAI/OPEA-compatible image endpoints.

Artifact:

```text
evidence/benchmarks/lmm_machine_oil_leak.strict.json
```
