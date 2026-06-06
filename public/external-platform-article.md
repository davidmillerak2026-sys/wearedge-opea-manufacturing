# WearEdge Pro: An OPEA Manufacturing Five-Agent Suite For Frontline Operators

This is the ready-to-use external-platform version of the WearEdge OPEA article.
It is suitable for LinkedIn Articles, Medium, Dev.to, or another public
technical blog platform.

## Suggested Metadata

Title:

```text
WearEdge Pro: An OPEA Manufacturing Five-Agent Suite for Frontline Operators
```

Subtitle:

```text
How a wearable edge AI workflow uses OPEA-style Gateway, Megaservice, RAG,
Qdrant, TEI embeddings, guardrails, and evaluation to cover maintenance,
quality, changeover, work instructions, and safety.
```

Tags:

```text
OPEA, Manufacturing AI, RAG, Edge AI, Intel Xeon, GenAI
```

## Article Body

WearEdge Pro is a real industrial AI agent system, not a sample-only chatbot.
Manufacturing operators often see early warning signs before enterprise systems
do: an unusual gearbox sound, a quality defect, a label changeover mismatch, a
work-instruction question, missing PPE, or a blocked walkway. These observations
are valuable, but they often stay trapped in verbal handoffs.

WearEdge Pro packages that frontline evidence into an OPEA-aligned
Manufacturing Agent Suite. The released public product artifact is not an
Android-only application. It is a Docker-runnable Web/API package with a
browser manufacturing console, five agent routes, Qdrant-backed RAG, official OPEA TEI
embedding profile, guardrails, and evaluation evidence.

The public repository uses sanitized fixtures. The broader WearEdge program has
private enterprise production-data lineage, including quality-inspection work
such as toothbrush workshop visual inspection for IQC/OQC-style defect
detection. Raw customer plant images, labels, lot IDs, and production records
are not published.

The five agent routes are:

| Agent | Workflow | Target |
| --- | --- | --- |
| `maintenance` | Predictive maintenance from M400 evidence | `maintenance_work_order` |
| `iqc` | Incoming and in-process quality checks | `qms_quality_event` |
| `changeover` | SKU setup and first-piece verification | `changeover_checklist` |
| `wi` | Released work-instruction guidance | `wi_reference` |
| `hazard` | PPE, moving-parts, and walkway observations | `ehs_case` |

The architecture follows an OPEA-style path:

```text
M400 / API evidence
  -> Gateway
  -> Manufacturing Megaservice
  -> route registry
  -> Dataprep
  -> RAG / Retriever
  -> Qdrant Vector DB
  -> OPEA-compatible embedding service or official OPEA TEI profile
  -> LLM adapter or deterministic sample path
  -> deterministic evaluator
  -> guardrails
  -> bounded action card
```

The most important design decision is route isolation. Maintenance must not
issue safety clearance. Hazard observations must not invent final root cause.
Quality must not release a lot. Changeover must not grant restart permission.
Work-instruction guidance must stay tied to released source evidence.

For OPEA evidence, the repository includes:

- Docker Compose base profile with Qdrant and the Manufacturing Gateway;
- OPEA-compatible `/v1/embeddings` profile;
- official OPEA TEI profile using Hugging Face TEI, `opea/embedding:latest`,
  `TEI_EMBEDDING_ENDPOINT`, and `OPEA_TEI_EMBEDDING`;
- OpenAI/OPEA-compatible LLM adapter boundary;
- GenAIEval-compatible route evaluation package;
- upstream OPEA RFC, comments, and an open GenAIExamples PR with key check-run evidence.

The evaluation package includes 15 cases across the five routes and verifies:

- action-card contract;
- integration target correctness;
- channel correctness;
- risk-level correctness;
- human gate correctness;
- guardrail pass;
- RAG source match;
- route isolation.

The hardware evidence was captured on Google Cloud C3 `c3-standard-4`: a
single-node, 4-vCPU, 16-GiB-RAM, no-GPU Intel Xeon host exposing AVX-512 and AMX
flags. On that class of host, WearEdge validated the deterministic five-agent
route benchmark, Docker/Qdrant E2E, OPEA-compatible embedding profile E2E, and
official OPEA TEI profile E2E.

The public repository is here:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing
```

The upstream OPEA PR is here:

```text
https://github.com/opea-project/GenAIExamples/pull/2462
```

WearEdge is still a prototype, not a certified safety or release controller.
The important point is the platform pattern: one OPEA-aligned manufacturing
suite can convert frontline evidence into bounded, auditable action cards
across maintenance, quality, changeover, work instructions, and safety.
