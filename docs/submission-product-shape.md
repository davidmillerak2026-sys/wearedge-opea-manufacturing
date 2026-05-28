# Submission Product Shape

This repository is the judge-facing OPEA Manufacturing submission product.

## Final Deliverable

WearEdge Pro should be submitted as a self-contained OPEA-aligned Manufacturing Agent Suite, not as an Android-only application.

The official `project_url` points to this repository:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

A judge should be able to run:

```bash
docker compose up --build -d
```

Then open:

```text
http://127.0.0.1:8088/demo
```

The browser console is the judge-facing product experience for evaluation. It lets reviewers switch between `maintenance`, `iqc`, `changeover`, `wi`, and `hazard`, run route scenarios, inspect the sample request, see retrieved source evidence, review guardrails, and verify the action-card output.

## Product Architecture

```text
Vuzix M400 / Android client / Web demo console / API request
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

The M400 Android client is the real deployment front end and field-evidence source. It is not the only submission artifact and should not be required for judging.

Use Android/M400 as proof that WearEdge Pro is grounded in a real wearable workflow:

- Captures first-person plant-floor evidence.
- Shows the edge inference result back to the operator.
- Anchors the maintenance hero route in a realistic deployment pattern.
- Differentiates the product from a generic browser chatbot.

Use the Web Demo Console as the judge-friendly substitute when reviewers do not have M400 hardware.

## What The Judge Evaluates

| Evaluation need | Submission evidence |
| --- | --- |
| One-click deployment | `docker-compose.yml`, `deploy.sh`, README commands |
| OPEA implementation | Gateway, Megaservice, Dataprep, RAG, Qdrant, LLM adapter, Guardrails |
| Product quality | `/demo`, `/v1/agents`, `/v1/agents/{mode}/demo`, `/v1/scorecard` |
| Manufacturing value | Five route suite: maintenance, IQC, changeover, WI, hazard |
| Safety and trust | Route-specific blocked claims and human confirmation gates |
| Open-source contribution | OPEA RFC issue `https://github.com/opea-project/GenAIExamples/issues/2461` |
| Intel bonus readiness | Google Cloud C3 Xeon AVX-512/AMX benchmark JSON, runbook, and harness |

## Submission Wording

Use this wording in the challenge form:

```text
WearEdge Pro is a real wearable edge industrial AI agent system packaged for the OPEA challenge as a runnable Manufacturing Agent Suite. The submitted GitHub repository starts an OPEA-style Gateway, Manufacturing Megaservice, Qdrant RAG profile, route-specific evaluators, guardrails, browser demo console, and five action-card agents. The M400 Android client is the real deployment front end and evidence source; the Web Console is the judge-facing experience for reproducible evaluation.
```

## Do Not Claim

- Do not claim the submission is only an Android APK.
- Do not require judges to own a Vuzix M400.
- Do not claim certified safety release, quality release, restart permission, or autonomous maintenance release.
- Do not claim production LLM acceleration from the AVX-512/AMX benchmark; the captured JSON measures the deterministic five-agent route pipeline.
