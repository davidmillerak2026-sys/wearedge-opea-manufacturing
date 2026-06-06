# GCP C3 TEI oneDNN Verbose Report

Date: 2026-05-29

## Result

The supplemental GCP C3 TEI/oneDNN run passed the WearEdge OPEA Manufacturing
application checks and the same-host oneDNN BF16/AMX probe.

| Field | Value |
| --- | --- |
| Project | `gen-lang-client-0555254036` |
| Zone | `us-central1-a` |
| VM | `wearedge-tei-onednn-0529024359` |
| Machine | `c3-standard-4` |
| Target profile | single node, 4 vCPU, 15.61 GiB observed RAM, no GPU |
| Branch/tag | historical May 29 submission series, now represented by `final-submission-2026-05-29-r23` |
| Full artifact in Cloud Shell | `/home/ryan_on2008/gcp_c3_tei_onednn_verbose.json` |
| Summary artifact | `evidence/benchmarks/gcp_c3_tei_onednn_verbose.summary.json` |
| Overall result | `all_checks_pass=true` |

## What Passed

| Check | Result |
| --- | --- |
| Gateway health | true |
| Five-agent scorecard | true |
| Five sample routes | true |
| Docker stats captured | true |
| Compose service list captured | true |
| C3 CPU flags include AVX-512 | true |
| C3 CPU flags include AMX | true |
| TEI logs present | true |
| TEI container oneDNN/ISA dispatch markers captured | false |
| Same-host oneDNN BF16/AMX probe compiled | true |
| Same-host oneDNN BF16/AMX probe executed | true |
| Same-host oneDNN BF16/AMX probe dispatch markers captured | true |

The run started the official OPEA TEI profile and captured Docker Compose
service evidence:

| Service | Image / role | Evidence |
| --- | --- | --- |
| Manufacturing Gateway | `wearedge-opea-tei-onednn-manufacturing-gateway` | running in Compose |
| OPEA embedding TEI wrapper | `opea/embedding:latest` | running in Compose |
| Qdrant | `qdrant/qdrant:v1.12.6` | running in Compose |
| Hugging Face TEI | `ghcr.io/huggingface/text-embeddings-inference:cpu-latest` | running in Compose |

The artifact also shows an OpenAI-compatible embedding response with
`data[0].object=embedding`, proving that the OPEA embedding wrapper and TEI
serving path responded during the run. The compact summary records the
validation booleans from the pasted Cloud Shell result; the full 80 KB artifact
remains in Cloud Shell at the path above.

## Why Scorecard Was Included

The goal was not merely to start TEI. The scorecard forces the real WearEdge
application path to execute: Gateway, Manufacturing Megaservice, Retriever/RAG,
Qdrant Vector DB, OPEA TEI embeddings, evaluator, and guardrails across the
five manufacturing agents. That makes the hardware evidence application-level
evidence for the released industrial AI agent system, not a standalone CPU
smoke test.

## Claim Boundary

This is strong hardware public evidence for the evaluation criteria phrase "effective use of
Intel hardware features (AMX, AVX-512)" because the same OPEA TEI + Qdrant +
five-agent scorecard workload ran on a single-node C3 Xeon profile, detected
AVX-512 and AMX CPU flags, and a same-host oneDNN BF16/AMX probe emitted
dispatch markers.

The boundary is TEI-specific. The run enabled verbose capture and searched
TEI/OPEA logs for oneDNN, DNNL, MKLDNN, AVX, AMX, BF16, VNNI, BRGEMM, and
matmul markers, but the captured TEI build did not emit matching dispatch
lines:

```text
dispatch_markers_captured=false
probe_dispatch_markers_captured=true
```

Use the following wording in the release:

```text
We validated the official OPEA TEI embedding profile on a Google Cloud C3
c3-standard-4 single-node host with 4 vCPU, about 16 GiB RAM, no GPU, and
AVX-512/AMX CPU flags detected. The run passed Gateway health, the five-agent
scorecard, five sample routes, Docker stats capture, and TEI log capture. The
same-host oneDNN BF16/AMX probe captured dispatch markers on that host. The TEI
container logs themselves did not emit oneDNN dispatch marker lines, so we
claim application-level OPEA workload validation plus same-host oneDNN BF16/AMX
dispatch evidence, not TEI-internal AMX dispatch proof.
```
