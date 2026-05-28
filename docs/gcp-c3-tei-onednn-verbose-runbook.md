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

or, if TEI does not emit verbose kernel logs:

```text
claim_status=tei_verbose_not_emitted_cpu_feature_evidence_only
```

Both cases are honest. The first gives stronger low-level proof; the second
still proves official TEI + OPEA embedding + Qdrant + five-agent scorecard ran
on C3 hardware with Intel ISA flags present.

## Scoring Use

Use this as hardware bonus evidence only with precise wording:

```text
We ran official OPEA TEI embeddings and Qdrant RAG on a single GCP C3
c3-standard-4 node: 4 vCPU, 16 GiB RAM, no GPU, Intel Xeon C3 with AVX-512 and
AMX flags. The artifact records CPU flags, Docker stats, scorecard pass, and
TEI/OPEA logs searched for oneDNN/ISA dispatch markers.
```

Do not claim oneDNN or AMX kernel dispatch unless the artifact actually
contains matching marker lines.

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
