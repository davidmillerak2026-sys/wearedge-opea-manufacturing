# WearEdge Pro: OPEA Manufacturing Lao-Shi-Fu Agent

Draft technical report for the ITU AI for Good OPEA Manufacturing submission.

## 1. Problem And Business Value

Manufacturing plants lose time when frontline observations, machine records, maintenance history, quality rules, and expert know-how live in separate systems. Operators can often see abnormal vibration, heat, oil leakage, repeated alarms, or unsafe access conditions first, but the evidence is not captured in a form that maintenance, quality, MES, or EHS systems can consume.

WearEdge Pro addresses this "last ten meters" problem with a wearable edge AI workflow: a Vuzix M400 captures first-person evidence, a local edge gateway performs multimodal reasoning and industrial RAG, and a bounded agent produces auditable action cards for human-confirmed plant workflows.

For the Manufacturing track, the primary scenario is a lao-shi-fu predictive-maintenance loop for packaging-line asset `PKG-L3-GBX-03`. The agent guides the operator to capture asset identity, condition screen, temperature gauge, lubrication record, recent maintenance record, and operator sensory observations. It does not claim final root cause, remaining useful life, restart permission, or maintenance release. Instead, it produces an evidence-bounded maintenance action card and CMMS-ready work-order draft requiring human confirmation.

## 2. OPEA Architecture Mapping

WearEdge Pro is packaged as an OPEA-aligned enterprise GenAI application:

```text
M400 / demo UI
  -> Gateway
  -> Manufacturing Megaservice
  -> Dataprep + RAG / maintenance KB
  -> LLM service through an OpenAI-compatible endpoint
  -> deterministic maintenance evaluator
  -> guardrailed action card and audit log
  -> GenAIEval-style latency, quality, and correctness report
```

The current source project already contains the manufacturing gateway, agent orchestration, local industrial RAG/KB, deterministic evaluators, guardrails, audit logs, and M400 client. This standalone repository makes the OPEA evidence explicit and keeps planned components from being overclaimed.

Honest current component claim: `LLM`, `RAG`, `Vector DB`, `Orchestration`, `Guardrails`.

The committed Docker Compose profile uses Qdrant as the Vector DB. The dependency-free local demo uses an in-memory hashing vector fallback so the pipeline remains runnable without Docker.

## 3. Implementation

WearEdge Pro is built around five bounded manufacturing agent routes: `maintenance`, `iqc`, `changeover`, `wi`, and `hazard`. This submission focuses on the maintenance route because it best demonstrates Manufacturing value and OPEA-style composition.

Key source modules in the original project:

- `jetson/app.py`: FastAPI gateway for `/v1/infer`, audit, and maintenance-session APIs.
- `jetson/agently_orchestrator.py` and `jetson/agent_loop.py`: route selection, evidence collection, output contract, deterministic action mapping, integration events, and runtime stream.
- `jetson/maintenance_session.py`: multi-evidence session state for the lao-shi-fu workflow.
- `jetson/maintenance_kb.py` and `jetson/maintenance_signal_eval.py`: local manufacturing KB retrieval and deterministic threshold evaluation.
- `industrial-rag-agent/`: dependency-light local industrial RAG module for manuals, SOPs, quality plans, and maintenance logs.
- `clients/m400/android/`: Vuzix M400 client with Camera2 capture, preview confirmation, voice-assisted evidence flow, Jetson upload, and final action confirmation.

The prototype runs local multimodal inference on a Jetson Orin Nano 8GB using Gemma 4 E2B GGUF and `llama.cpp` behind an OpenAI-compatible endpoint. This model/runtime choice is an edge LLM service implementation detail. The architecture can swap in an OPEA LLM microservice profile without changing the Manufacturing action-card contract.

## 4. Prototype Evidence And Results

Current evidence in the source project:

- Real M400 full chain: M400 Camera2 image -> Wi-Fi -> Jetson gateway -> local multimodal inference -> M400 result -> audit request-id match.
- Five-agent deterministic validation: maintenance, IQC, changeover, WI, and hazard routes pass route-specific action envelopes.
- Lao-shi-fu maintenance POC: multi-step maintenance evidence loop with asset identity, HMI/condition screen, temperature, lubrication, recent work record, and operator sensory check.
- Edge runtime benchmark: safety path image inference ranges from 3.5s to 13.2s, while high-detail M400 maintenance calls average about 45.8s with 560/560 visual-token budget.
- Test history: latest recorded local automated suite passed with more than 120 tests.

The prototype is honest about current limitations. The high-detail M400 maintenance loop is slower than the fast safety path because it prioritizes readable HMI, labels, gauges, and records. The next benchmark should evaluate 140/140 and 280/280 visual-token budgets and report speed/quality tradeoffs.

## 5. Deployment And Reproducibility

This repository now includes an evaluator-facing OPEA-style wrapper, Docker Compose Qdrant profile, and dependency-free local demo. The source project includes Jetson setup scripts, model download/build scripts, gateway and model-server startup scripts, systemd service templates, tests, and smoke-test commands.

Current demo commands:

```bash
./deploy.sh
./run_manufacturing_demo.sh
```

Expected output includes gateway health, vector backend status, sample manufacturing session inference, maintenance evaluation, action-card JSON, and source IDs. Final submission should still add a saved benchmark summary and GenAIEval-style scorecard.

## 6. Safety, Licensing, And Open Source

WearEdge Pro is licensed under MIT, which is allowed by the challenge rules. The system is an assistive decision-support prototype, not a certified industrial safety controller. All high-risk outputs require human confirmation, and the agent is designed to ask for missing evidence rather than invent final root cause or release decisions.

For bonus points, the team should publish an OPEA blueprint feedback issue or PR, a technical article/video explaining the Manufacturing architecture, and an Intel CPU/OpenVINO or AVX-512/AMX optimization benchmark path.
