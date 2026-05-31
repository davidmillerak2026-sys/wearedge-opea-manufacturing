# Telecom Scope And Manufacturing Positioning

Date: 2026-05-28

## Decision

Keep the official vertical as:

```text
Manufacturing
```

Do not pivot the project to telecom. The project is strongest when it owns
the manufacturing edge-AI story: wearable evidence, plant workflows, CMMS/QMS/
MES/WI/EHS action cards, and human-confirmed safety boundaries.

## How To Handle A Telecom-Leaning Evaluator

Use enterprise reliability language without changing the vertical:

- route isolation mirrors operations workflows in telecom and manufacturing;
- edge gateway + RAG + action-card pattern is reusable for network operations;
- manufacturing is a high-value enterprise scenario with real physical-world
  safety, downtime, quality, and changeover constraints;
- OPEA is shown as a reusable enterprise application platform, not a one-off
  factory script.

## Project Wording

Use:

```text
WearEdge Pro demonstrates OPEA for enterprise manufacturing operations: the
same Gateway/Megaservice/RAG/Guardrails architecture can route evidence to five
plant workflows while preserving source IDs, human gates, and integration
targets. This is the manufacturing equivalent of a network operations copilot:
evidence comes from the edge, RAG retrieves approved context, and bounded
action cards flow to the correct enterprise system.
```

Avoid:

```text
telecom product, network-only agent, generic operations chatbot
```

## Why This Matters For Enterprise Evaluation

If another team has a telecom reference implementation, our counter-position is platform breadth
and physical-world enterprise value:

- five workflows instead of one;
- real wearable/edge product lineage;
- official OPEA TEI path and C3 validation;
- guardrails for safety, release authority, quality, and maintenance claims;
- evaluator-verifiable scorecard instead of only a polished UI.
