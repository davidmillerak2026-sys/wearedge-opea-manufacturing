# Project Product Shape

This repository is the evaluation-facing OPEA Manufacturing product package.

## Final Deliverable

WearEdge Pro should be released as a self-contained OPEA-aligned Manufacturing Agent Suite, not as an Android-only application and not as a sample-only project. The system is a real industrial AI agent system; this repository is the reproducible public package.

The official `project_url` points to this repository:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

An evaluator should be able to run:

```bash
docker compose up --build -d
```

Then open:

```text
http://127.0.0.1:8088/demo
```

The browser console is the reproducible product experience for evaluation. It lets reviewers switch between `maintenance`, `iqc`, `changeover`, `wi`, and `hazard`, run route scenarios, inspect the sample request, see retrieved source evidence, review guardrails, and verify the action-card output. The console now presents the five-agent suite as an industrial command console with OPEA pipeline stages, RAG source evidence, scorecard state, and private production-data boundary.

## Product Architecture

```text
Vuzix M400 / Android client / Web manufacturing console / API request
  -> OPEA-style Gateway
  -> Manufacturing Megaservice
  -> route registry
  -> Dataprep
  -> Retriever / RAG
  -> Qdrant Vector DB profile
  -> LLM adapter
  -> deterministic evaluator
  -> Guardrails
  -> CMMS / QMS / MES / WI / EHS action card
```

## Role Of Android / M400

The M400 Android client is the real deployment front end and field-evidence source. It is not the only project artifact and should not be required for review.

Use Android/M400 as proof that WearEdge Pro is grounded in a real wearable workflow:

- Captures first-person plant-floor evidence.
- Shows the edge inference result back to the operator.
- Anchors the maintenance hero route in a realistic deployment pattern.
- Differentiates the product from a generic browser chatbot.

Use the Browser Manufacturing Console as the evaluator-friendly substitute when evaluators do not have M400 hardware.

## What The Evaluator Runs

| Evaluation need | Project evidence |
| --- | --- |
| One-click deployment | `docker-compose.yml`, `deploy.sh`, README commands |
| OPEA implementation | Gateway, Megaservice, Dataprep, RAG, Qdrant, LLM adapter, Guardrails |
| Product quality | `/demo`, `/v1/agents`, `/v1/agents/{mode}/demo`, `/v1/scorecard` |
| Manufacturing value | Five route suite: maintenance, IQC, changeover, WI, hazard |
| Production-data lineage | Private enterprise quality-inspection lineage, including toothbrush workshop IQC/OQC visual inspection, represented publicly through sanitized fixtures |
| Safety and trust | Route-specific blocked claims and human confirmation gates |
| Open-source contribution | OPEA RFC issue `https://github.com/opea-project/GenAIExamples/issues/2461` |
| Intel evidence readiness | Google Cloud C3 Xeon AVX-512/AMX benchmark JSON, runbook, and harness |

## Project Wording

Use this wording in the project profile:

```text
WearEdge Pro is a real wearable edge industrial AI agent system packaged for the OPEA ecosystem as a runnable Manufacturing Agent Suite. The public GitHub repository starts an OPEA-style Gateway, Manufacturing Megaservice, Qdrant RAG profile, route-specific evaluators, guardrails, browser manufacturing console, and five action-card agents. The M400 Android client is the real deployment front end and evidence source; the Web Console is the reproducible product experience. Private customer production-data lineage, including toothbrush workshop IQC/OQC visual inspection, is represented through sanitized public fixtures without exposing customer data.
```

## Do Not Claim

- Do not claim the project is only an Android APK.
- Do not require evaluators to own a Vuzix M400.
- Do not claim certified safety release, quality release, restart permission, or autonomous maintenance release.
- Do not claim production LLM acceleration from the AVX-512/AMX benchmark; the captured JSON measures the deterministic five-agent route pipeline.
- Do not publish raw customer plant images, labels, lot identifiers, or production records.
