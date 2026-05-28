# WearEdge-Pro Real VLM E2E Evidence Map

Date: 2026-05-28

This OPEA submission package is the runnable challenge deliverable. The
broader WearEdge-Pro repository contains the real edge VLM product path that
proved the same industrial agent loop with first-person image evidence, a
Jetson gateway, local Gemma 4 E2B vision-language inference, output contracts,
action cards, audit logs, and M400 client integration.

Source repository:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

Local source snapshot inspected:

```text
WearEdge-Pro commit: 1abc65333e877b4206bdd4f7af5de71f9e97b061
```

## Real VLM Runtime Path

```text
Vuzix M400 / browser image
  -> WearEdge-Pro FastAPI Gateway /v1/infer
  -> build_multimodal_payload()
  -> llama.cpp llama-server /v1/chat/completions
  -> Gemma 4 E2B Q4_K_S GGUF
  -> mmproj-F16 vision projector
  -> route-specific contract validation
  -> agent loop / guardrails / action card
  -> CMMS, QMS, MES, WI, or EHS integration event
```

This is the real WearEdge-Pro VLM chain. The OPEA challenge repository then
packages the manufacturing agent suite into a judge-runnable OPEA architecture:
Gateway, Manufacturing Megaservice, Dataprep, OPEA TEI embeddings, Qdrant RAG,
LLM adapter boundary, deterministic evaluators, route guardrails, scorecard,
and GenAIEval-compatible evidence.

The local VLM chain and the external LMM benchmark are complementary. The
Jetson/Gemma 4 E2B path proves WearEdge can run on edge hardware without
depending on a cloud model. The Gemini/OpenAI-compatible benchmark path proves
the same OPEA-style industrial agent pipeline can also connect to external
enterprise or cloud model APIs through a strict adapter boundary.

## Source Code Evidence

| Capability | WearEdge-Pro source path | What it proves |
| --- | --- | --- |
| Image upload gateway | `jetson/app.py` | `/v1/infer` accepts multipart image, device metadata, route mode, and returns structured JSON. |
| Multimodal model payload | `jetson/llama_client.py` | Encodes the image as OpenAI-compatible `image_url` and posts to `/v1/chat/completions`. |
| Five-route orchestration | `jetson/agently_orchestrator.py` | Locks route, plans modality, retrieves KB/source context, calls the model, validates contract, and builds action artifacts. |
| Output contracts | `jetson/output_contract.py` | Turns VLM text into required route fields before action-card creation. |
| Maintenance KB and thresholds | `jetson/maintenance_kb.py`, `jetson/maintenance_signal_eval.py` | Keeps maintenance claims bounded by accepted readings and source thresholds. |
| M400 client path | `clients/m400/android/`, `clients/m400/README.md` | Captures first-person evidence and sends it to `/v1/infer`. |
| Repro smoke path | `scripts/smoke_test.sh` | Verifies gateway health, llama-server text health, image upload, contract, audit query, and agent run query. |

## Archived Run Evidence

| Evidence file in WearEdge-Pro | Result |
| --- | --- |
| `docs/poc-results/gemma4-e2b-safety-sample-result.json` | `ok=true`, model `gemma4`, 3.17 MB JPEG, `latency_ms=5824`, structured safety output. |
| `docs/poc-results/gemma4-e2b-autostart-browser-result.json` | Jetson reboot/autostart browser run, `latency_ms=8734`, `ok=true`. |
| `docs/gemma4-e2b-poc-summary.md` | Documents Jetson Orin Nano 8GB, Gemma 4 E2B Q4_K_S, `mmproj-F16`, llama.cpp, FastAPI, systemd, and contract repair. |
| `docs/edge-runtime-benchmark.md` | Summarizes repeated VLM latency evidence, token-budget tradeoffs, and local edge hardware context. |
| `docs/poc-results/full-agent-gateway-poc-summary.json` | Real gateway five-agent cases passed: maintenance, hazard, IQC, WI, changeover allow/block. |
| `docs/poc-results/lao-shi-fu-maintenance-poc-summary.json` | Multi-step maintenance VLM evidence loop, including oil leak / sensory evidence route to maintenance work-order style action. |
| `docs/poc-results/m400-hotspot-audit-recent.json` | Audited M400 maintenance runs include `model.call.completed`, action cards, integration events, and request IDs. |
| `docs/poc-results/m400-hotspot-agent-runs-recent.json` | Agent run query exposes closed runtime stream, action cards, and latest workflow event. |

## Metrics To Reuse In Submission Narrative

| Metric | Evidence |
| --- | --- |
| Edge VLM hardware | Jetson Orin Nano 8GB, JetPack 6.2.1 / L4T R36.4.4, Ubuntu 22.04, aarch64. |
| VLM model | Gemma 4 E2B Q4_K_S GGUF + `mmproj-F16.gguf`. |
| Lightweight safety image run | 3.17 MB JPEG, `latency_ms=5824`, `ok=true`. |
| Autostart browser run | 3.17 MB JPEG, `latency_ms=8734`, `ok=true`. |
| Full five-agent gateway cases | 6/6 cases passed through real gateway or maintenance session API. |
| Maintenance E2E hero path | Maintenance session produced `maintenance_work_order`, `breach_count=5`, `maintenance_eval_status=breach_detected`, `integration_target=maintenance_work_order`. |
| Lao-shi-fu oil/sensory route | Step 6 recorded oil leakage, burnt-oil smell, visible shaking, high-frequency noise, `maintenance_stop`, `priority=critical`, `integration_target=maintenance_work_order`. |
| M400 audit path | Recent audit events include `model.call.completed`, request IDs, route-locked action cards, and integration events. |

## Claim Boundary

Use precise wording:

```text
WearEdge-Pro has already run a real edge VLM product path on Jetson with
Gemma 4 E2B + mmproj and M400-style image evidence. The OPEA competition repo
packages that industrial system into a reproducible, model-flexible,
OPEA-aligned five-agent suite using official TEI embeddings, Qdrant RAG,
guardrails, scorecards, and one-click Docker. The same architecture can use
local edge VLMs or external production LMM APIs without changing the route,
RAG, evaluator, guardrail, or action-card layers.
```

Avoid wording that would over-claim the OPEA challenge Docker path:

```text
Do not say the default OPEA Docker demo runs Gemma 4 E2B VLM locally.
Do not say the Gemini benchmark is the local WearEdge-Pro product model.
Do not say the public package contains private production images or large GGUF
model weights. Do not claim final root cause, restart permission, quality
release, or safety clearance.
```

## How To Pull This Forward

1. Keep WearEdge-Pro as the product evidence repository for M400, Jetson, VLM,
   and field workflow proof.
2. Keep this OPEA repository as the judge-facing runnable package.
3. Add strict LMM/VLM benchmark scripts here that can call an image-capable
   endpoint when credentials or a local server are available.
4. Use the public oil-leak maintenance image as a redacted benchmark fixture,
   not as private customer production data.
5. In the final submission, place this source-evidence map beside the OPEA
   TEI/Qdrant/GCP C3 evidence to show both real industrial product depth and
   OPEA-native reproducibility.
