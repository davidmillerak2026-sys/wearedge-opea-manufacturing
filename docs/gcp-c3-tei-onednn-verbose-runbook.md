# GCP C3 TEI oneDNN Verbose Runbook

Date: 2026-05-28

## Goal

This runbook strengthens the hardware optimization bonus evidence. It reruns
the official OPEA TEI + Qdrant profile on Google Cloud C3 `c3-standard-4`
hardware and captures:

- single-node challenge configuration: 4 vCPU, 16 GiB RAM, no GPU;
- Intel Xeon C3 CPU flags for AVX-512, AVX-512 BF16/VNNI, AMX TILE/INT8/BF16;
- official OPEA TEI embedding workload;
- Qdrant indexing and search through the five manufacturing agents;
- Docker memory and CPU stats;
- TEI/OPEA logs searched for oneDNN, DNNL, AMX, AVX, BF16, VNNI, BRGEMM, and
  matmul markers.
- a same-host Intel oneDNN BF16 matmul probe that emits `onednn_verbose` or
  `dnnl_verbose` dispatch lines when the C3 host exposes the backend path.

Script:

```text
scripts/gcp_c3_tei_onednn_verbose_cloudshell.sh
```

## Cloud Shell Command

```bash
PROJECT_ID=gen-lang-client-0555254036 \
ZONE=us-central1-a \
MACHINE_TYPE=c3-standard-4 \
bash scripts/gcp_c3_tei_onednn_verbose_cloudshell.sh
```

The script deletes the VM by default. To keep it:

```bash
KEEP_VM=1 bash scripts/gcp_c3_tei_onednn_verbose_cloudshell.sh
```

## Expected Artifact

Cloud Shell output file:

```text
~/gcp_c3_tei_onednn_verbose.json
```

Relevant fields:

```text
claim_status=tei_onednn_or_isa_dispatch_markers_captured
```

or, if TEI does not emit verbose kernel logs but the same-host probe does:

```text
claim_status=wear_edge_scorecard_with_onednn_bf16_amx_probe_dispatch_markers_captured
validation.probe_dispatch_markers_captured=true
```

or, if neither TEI nor the probe emits verbose kernel logs:

```text
claim_status=tei_verbose_not_emitted_cpu_feature_evidence_only
```

All cases are honest. The first is TEI-container dispatch evidence. The second
is same-host oneDNN BF16/AMX probe evidence plus the full WearEdge scorecard
path. The third still proves official TEI + OPEA embedding + Qdrant +
five-agent scorecard ran on C3 hardware with Intel ISA flags present.

## Scoring Use

Use this as hardware bonus evidence only with precise wording:

```text
We ran official OPEA TEI embeddings and Qdrant RAG on a single GCP C3
c3-standard-4 node: 4 vCPU, 16 GiB RAM, no GPU, Intel Xeon C3 with AVX-512 and
AMX flags. The artifact records CPU flags, Docker stats, scorecard pass, and
TEI/OPEA logs searched for oneDNN/ISA dispatch markers.
```

Do not claim TEI itself dispatched oneDNN or AMX kernels unless
`validation.dispatch_markers_captured=true`. If
`validation.probe_dispatch_markers_captured=true`, claim the narrower but
stronger statement: the same C3 host that ran the WearEdge scorecard also
produced observable oneDNN BF16/AMX/AVX512 dispatch marker lines in a
supplemental probe.

## Captured Result

The 2026-05-28 Cloud Shell run on
`final-submission-2026-05-28-r20` completed successfully:

```text
VM: wearedge-tei-onednn-0528111751
all_checks_pass=true
gateway_ok=true
scorecard_ok=true
five_demos_ok=true
c3_cpu_flags_include_avx512=true
c3_cpu_flags_include_amx=true
tei_logs_present=true
dispatch_markers_captured=false
```

Artifacts:

```text
docs/gcp-c3-tei-onednn-verbose-report.md
evidence/benchmarks/gcp_c3_tei_onednn_verbose.summary.json
```

Interpretation: this passed as application-level Intel C3 effective-use
evidence. The run did not capture oneDNN/TEI dispatch marker lines, so it must
not be described as instruction-level AMX or AVX-512 proof.

## Rerun With Same-Host oneDNN Probe

The script now includes a supplemental C++ oneDNN probe that installs
`libdnnl-dev`, compiles a BF16 `1024x1024x1024` matmul, runs it on the same C3
VM as the WearEdge OPEA TEI scorecard path, and records:

```text
validation.onednn_probe_compiled
validation.onednn_probe_executed
validation.probe_dispatch_markers_captured
probe_dispatch_evidence.marker_lines
```

Use tag `final-submission-2026-05-29-r22` or newer when rerunning from Cloud
Shell. If the probe captures marker lines while TEI still does not, the proper
claim is:

```text
WearEdge's full OPEA TEI + Qdrant + five-agent scorecard path passed on the
same GCP C3 node where a supplemental oneDNN BF16 matmul probe emitted
observable oneDNN dispatch markers. This proves host-level Intel oneDNN
BF16/AMX/AVX512 dispatch evidence alongside the WearEdge workload; it does not
claim TEI itself emitted those markers.
```
