# Local Gemma LLM Benchmark

Date: 2026-06-05

## Purpose

This project does not require an OpenAI API key to prove the LLM adapter path.
The requirement is a real model endpoint. A local Gemma model is acceptable if
it is served through an HTTP API that the WearEdge adapter can call.

The local model file or desktop UI alone is not enough for benchmark evidence.
The model must be exposed through one of these service shapes:

- Ollama native `/api/chat`
- OpenAI-compatible `/v1/chat/completions`
- OPEA-compatible LLM service using the same chat-completions contract

## Supported Local Profiles

The benchmark script now supports local profiles:

| Profile | Default endpoint | Backend |
| --- | --- | --- |
| `ollama` | `http://127.0.0.1:11434/api/chat` | Ollama native |
| `lmstudio` | `http://127.0.0.1:1234/v1/chat/completions` | OpenAI-compatible |
| `vllm` | `http://127.0.0.1:8000/v1/chat/completions` | OpenAI-compatible |
| `llamacpp` | `http://127.0.0.1:8080/v1/chat/completions` | OpenAI-compatible |

## Ollama

Start Ollama and confirm the Gemma model name:

```powershell
ollama list
```

Run the benchmark with the exact model name shown by Ollama:

```powershell
$env:PYTHONPATH="src"
python scripts\llm_adapter_benchmark.py --local-profile ollama `
  --model <your-gemma-model-name> `
  --strict --iterations 1 `
  --output evidence\benchmarks\llm_adapter.local-gemma.json
```

No API key is required for the default local Ollama endpoint.

If Ollama is installed inside WSL rather than Windows, run the benchmark from
the WSL shell so `127.0.0.1:11434` resolves inside the same environment:

```bash
cd "/mnt/c/Users/ryan hui/Documents/New project/wearedge-opea-manufacturing"
PYTHONPATH=src \
WEAREDGE_LLM_TIMEOUT=600 \
WEAREDGE_LLM_MAX_TOKENS=96 \
WEAREDGE_LLM_OLLAMA_THINK=false \
python3 scripts/llm_adapter_benchmark.py \
  --local-profile ollama \
  --model gemma4:31b \
  --strict --iterations 1 \
  --output evidence/benchmarks/llm_adapter.local-gemma.json
```

On this workstation, Windows PowerShell cannot directly reach the WSL Ollama
loopback endpoint because the service listens on WSL `127.0.0.1:11434`. Expose
Ollama with a wider `OLLAMA_HOST` only if a Windows-hosted service must call it.

## LM Studio

In LM Studio, load the Gemma model and start the Local Server. Then run:

```powershell
$env:PYTHONPATH="src"
python scripts\llm_adapter_benchmark.py --local-profile lmstudio `
  --model <lm-studio-model-id> `
  --strict --iterations 1 `
  --output evidence\benchmarks\llm_adapter.local-gemma.json
```

If LM Studio reports a different port, pass it explicitly:

```powershell
python scripts\llm_adapter_benchmark.py --backend openai-compatible `
  --base-url http://127.0.0.1:<port>/v1 `
  --model <lm-studio-model-id> `
  --strict --iterations 1 `
  --output evidence\benchmarks\llm_adapter.local-gemma.json
```

## vLLM

Serve the local or downloaded Gemma model through the OpenAI-compatible API:

```powershell
python -m vllm.entrypoints.openai.api_server `
  --model <model-or-local-path> `
  --host 127.0.0.1 --port 8000
```

Then run:

```powershell
$env:PYTHONPATH="src"
python scripts\llm_adapter_benchmark.py --local-profile vllm `
  --model <model-or-local-path> `
  --strict --iterations 1 `
  --output evidence\benchmarks\llm_adapter.local-gemma.json
```

## llama.cpp

Serve a GGUF Gemma model:

```powershell
llama-server -m <path-to-gemma.gguf> --host 127.0.0.1 --port 8080
```

Then run:

```powershell
$env:PYTHONPATH="src"
python scripts\llm_adapter_benchmark.py --local-profile llamacpp `
  --model <model-name> `
  --strict --iterations 1 `
  --output evidence\benchmarks\llm_adapter.local-gemma.json
```

## Success Criteria

Use the local Gemma evidence only when the output reports:

```text
claim_status=local_llm_endpoint_benchmarked
local_endpoint_used=true
fallback_count=0
all_contracts_pass=true
```

## Captured Local Run

This repository includes a captured strict local run:

```text
evidence/benchmarks/llm_adapter.local-gemma.json
```

Observed environment:

```text
WSL Ubuntu Ollama 0.21.0
Model: gemma4:31b
Parameters: 31.3B
Quantization: Q4_K_M
GPU visible in WSL: NVIDIA GeForce RTX 3090, 24 GiB VRAM
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

The Ollama adapter sends top-level `think=false` by default so Gemma4 returns
normal `message.content` instead of spending the response budget in
`message.thinking`.

Safe wording:

```text
WearEdge OPEA Manufacturing successfully benchmarked a local Gemma model
endpoint through the LLM adapter with strict no-fallback execution.
```

Avoid:

```text
Production cloud LLM endpoint benchmarked.
```

That wording should only be used for a remote production endpoint that reports
`claim_status=production_llm_endpoint_benchmarked`.

## Hardware Note

A 31B-class local Gemma model can be heavy. It may need significant system RAM,
VRAM, or a quantized GGUF/Ollama build. The benchmark evidence should record the
endpoint behavior and route contract status; hardware performance claims should
be made separately only after CPU/GPU and memory evidence is captured.
