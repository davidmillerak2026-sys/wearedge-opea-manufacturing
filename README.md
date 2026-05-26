# WearEdge OPEA Manufacturing

Dedicated ITU AI for Good / OPEA Manufacturing submission package for WearEdge Pro.

Target GitHub URL:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

This repository is intentionally separated from the original WearEdge Pro engineering repository so judges can review the OPEA-specific architecture, component mapping, reproducibility plan, and Manufacturing evidence without mixing it with earlier contest material.

## Submission Focus

WearEdge OPEA Manufacturing packages WearEdge Pro as an OPEA-aligned enterprise GenAI application for Manufacturing. The primary use case is a `lao-shi-fu` predictive-maintenance workflow for a packaging-line gearbox:

```text
Vuzix M400 first-person evidence
  -> edge gateway
  -> OPEA-style Manufacturing Megaservice
  -> RAG / maintenance KB
  -> LLM service
  -> deterministic threshold evaluation
  -> guardrailed action card
  -> CMMS-ready work-order event
```

The workflow asks for missing evidence instead of inventing final root cause. High-risk recommendations remain human-confirmed.

## Official OPEA Component Mapping

| OPEA layer | WearEdge implementation evidence | Claim status |
| --- | --- | --- |
| Gateway | FastAPI edge gateway for M400, audit, and maintenance sessions | implemented in source project |
| Megaservice | Manufacturing orchestration across evidence, RAG, LLM, evaluator, guardrails, and action cards | implemented in source project |
| Dataprep | Industrial document loading and chunking for SOPs, logs, quality plans | adapter-ready |
| Retriever / RAG | Machine-specific maintenance KB and local industrial retriever | implemented in source project |
| LLM service | OpenAI-compatible local LLM/VLM endpoint | adapter-ready |
| Prompt contract | Mode-specific output contract and action-starter constraints | implemented in source project |
| Guardrails | Source guard, action map, uncertainty guard, human gate | implemented in source project |
| Evaluation | Repo-native benchmark and deterministic scorecard | adapter-ready for GenAIEval-style report |
| Vector DB | Qdrant/Chroma/Milvus/Redis profile not committed yet | do not claim yet |

Detailed machine-readable evidence: [`evidence/component-evidence.json`](evidence/component-evidence.json).

## Submission Fields

Draft fields for the challenge form are in [`submission-fields.draft.json`](submission-fields.draft.json).

Recommended current component selection:

```text
LLM, RAG, Orchestration, Guardrails
```

Do not select `Vector DB` until a vector-store profile is committed in this repository.

## Included Materials

| Path | Purpose |
| --- | --- |
| [`SUBMISSION.md`](SUBMISSION.md) | Challenge-facing summary and evidence checklist |
| [`docs/technical-report.draft.md`](docs/technical-report.draft.md) | Draft <=2 page technical report |
| [`docs/opea-component-evidence.md`](docs/opea-component-evidence.md) | Human-readable OPEA architecture evidence |
| [`docs/champion-gap-worklist.md`](docs/champion-gap-worklist.md) | Remaining work to compete for first prize |
| [`docs/source-project-map.md`](docs/source-project-map.md) | Mapping from this submission repo to the full WearEdge Pro source repo |
| [`scripts/evidence_check.py`](scripts/evidence_check.py) | Dependency-free local evidence manifest checker |

## Evidence Check

Run:

```powershell
& "C:\Users\ryan hui\anaconda3\python.exe" scripts\evidence_check.py
```

Expected:

```text
OPEA submission evidence check passed
```

## Source Repository

Full engineering source currently lives at:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

Before final submission, choose one of two clean publication strategies:

1. Mirror the necessary source code into this repository so the challenge `project_url` is fully self-contained.
2. Keep this as the OPEA submission landing repository and use the original WearEdge Pro repo as the complete source-code link.

For the official challenge, self-contained source is stronger.

