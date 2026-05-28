# GCP C3 TEI oneDNN Verbose Report

Date: 2026-05-28

## Result

The supplemental GCP C3 TEI/oneDNN verbose run passed the WearEdge OPEA
Manufacturing application checks.

| Field | Value |
| --- | --- |
| Project | `gen-lang-client-0555254036` |
| Zone | `us-central1-a` |
| VM | `wearedge-tei-onednn-0528111751` |
| Machine | `c3-standard-4` |
| Challenge profile | single node, 4 vCPU, 15.61 GiB observed RAM, no GPU |
| Branch/tag | `final-submission-2026-05-28-r20` |
| Full artifact in Cloud Shell | `/home/ryan_on2008/gcp_c3_tei_onednn_verbose.json` |
| Summary artifact | `evidence/benchmarks/gcp_c3_tei_onednn_verbose.summary.json` |
| Overall result | `all_checks_pass=true` |

## What Passed

| Check | Result |
| --- | --- |
| Gateway health | true |
| Five-agent scorecard | true |
| Five demo routes | true |
| Docker stats captured | true |
| Compose service list captured | true |
| C3 CPU flags include AVX-512 | true |
| C3 CPU flags include AMX | true |
| TEI logs present | true |
| oneDNN/ISA dispatch markers captured | false |

The run started the official OPEA TEI profile:

| Service | Image | Memory snapshot |
| --- | --- | ---: |
| Manufacturing Gateway | `wearedge-opea-tei-onednn-manufacturing-gateway` | 36.36 MiB / 15.61 GiB |
| OPEA embedding TEI wrapper | `opea/embedding:latest` | 93.68 MiB / 15.61 GiB |
| Qdrant | `qdrant/qdrant:v1.12.6` | 57.57 MiB / 15.61 GiB |
| Hugging Face TEI | `ghcr.io/huggingface/text-embeddings-inference:cpu-latest` | 879.5 MiB / 15.61 GiB |

The pasted artifact also shows an OpenAI-compatible embedding response with
`data[0].object=embedding`, proving that the OPEA embedding wrapper and TEI
serving path responded during the run.

## Why Scorecard Was Included

The goal was not merely to start TEI. The scorecard forces the real WearEdge
application path to execute: Gateway, Manufacturing Megaservice, Retriever/RAG,
Qdrant Vector DB, OPEA TEI embeddings, evaluator, and guardrails across the
five manufacturing agents. That makes the hardware evidence application-level
evidence for the submitted industrial AI agent system, not a standalone CPU
smoke test.

## Claim Boundary

This is strong hardware bonus evidence for the rubric phrase "effective use of
Intel hardware features (AMX, AVX-512)" because the same OPEA TEI + Qdrant +
five-agent scorecard workload ran on a single-node C3 Xeon profile and detected
AVX-512 and AMX CPU flags.

It is not low-level microkernel-dispatch proof. The run enabled verbose capture
and searched TEI/OPEA logs for oneDNN, DNNL, MKLDNN, AVX, AMX, BF16, VNNI,
BRGEMM, and matmul markers, but the captured TEI build did not emit matching
dispatch lines:

```text
dispatch_markers_captured=false
marker_count=0
```

Use the following wording in the final submission:

```text
We validated the official OPEA TEI embedding profile on a Google Cloud C3
c3-standard-4 single-node host with 4 vCPU, about 16 GiB RAM, no GPU, and
AVX-512/AMX CPU flags detected. The run passed Gateway health, the five-agent
scorecard, five demo routes, Docker stats capture, and TEI log capture. The
verbose attempt did not emit oneDNN dispatch marker lines, so we claim
application-level effective use of Intel C3 hardware, not instruction-level
AMX/AVX-512 kernel dispatch proof.
```
