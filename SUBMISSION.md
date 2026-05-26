# ITU AI for Good OPEA Manufacturing Submission

Challenge: Innovation Challenge on Generative AI Applications for Enterprise Scenarios Using OPEA

Vertical: Manufacturing

Application name: WearEdge Pro

## One-Sentence Summary

WearEdge Pro is an OPEA-aligned wearable edge AI agent for Manufacturing that turns first-person M400 evidence, local industrial RAG, deterministic maintenance evaluation, and guardrailed action cards into human-confirmed maintenance work-order workflows.

## Why This Fits Manufacturing

Manufacturing failures often begin as small frontline observations: abnormal vibration, high temperature, oil leakage, missing lubrication evidence, repeated alarms, or operator sensory concerns. WearEdge Pro captures those observations at the point of work and converts them into structured, auditable maintenance evidence.

The primary demo scenario is `PKG-L3-GBX-03`, a packaging-line gearbox. The lao-shi-fu workflow asks the operator for:

- asset identity
- condition screen / HMI evidence
- temperature gauge evidence
- lubrication record
- recent maintenance record
- operator sensory check

The final output is not an unsafe autonomous decision. It is a bounded action card and CMMS-ready work-order draft requiring human confirmation.

## OPEA Claim

Current honest submission components:

```text
LLM, RAG, Orchestration, Guardrails
```

The repository includes explicit OPEA component evidence and a worklist for making the claim fully executable through an OPEA-style runtime wrapper.

## Current Source Evidence

Full source project:

```text
https://github.com/davidmillerak2026-sys/WearEdge-Pro
```

Key existing evidence in the source project:

- M400 real-device full chain
- Jetson local multimodal inference
- maintenance session evidence loop
- manufacturing RAG / maintenance KB
- deterministic threshold evaluation
- guardrailed action cards
- runtime stream and audit logs
- automated tests

## Remaining Before Final Submission

P0:

- Make this repository self-contained or clearly linked to the source repository.
- Add one-click challenge deployment.
- Add final two-page technical report.
- Add 1-3 minute real prototype demo video.

P1:

- Add OPEA-compatible vector-store profile.
- Add GenAIEval-style scorecard.
- Add OPEA issue/PR/blueprint feedback link.
- Add Intel CPU/OpenVINO or AVX-512/AMX optimization evidence.

