# Xeon AVX-512 / AMX Benchmark Runbook

Goal: reproduce `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json` on a real Xeon host that exposes both AVX-512 and AMX flags.

## Captured Machine

The benchmark evidence was captured on Google Cloud:

```text
Google Cloud C3 c3-standard-4
Zone: us-central1-a
CPU: Intel(R) Xeon(R) Platinum 8481C CPU @ 2.70GHz
Detected: avx512f, avx512_bf16, avx512_vnni, amx_tile, amx_int8, amx_bf16
Result: evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json
```

The temporary VM `wearedge-amx-bench-0527072816` was deleted after the run.

## Recommended Rerun Machines

Use Google Cloud `c3-standard-4` first because it has already produced the accepted evidence in this repository.

Backup options:

| Provider | Instance | Notes |
| --- | --- | --- |
| Google Cloud | `c3-standard-4` | Captured evidence on Intel Xeon Platinum 8481C with AVX-512 and AMX flags. |
| Azure | `Standard_D4s_v6` | Best claim language because docs explicitly mention AVX-512 and AMX. |
| AWS | `c7i.xlarge` | 4th Gen Intel Xeon Scalable with Intel AMX. Verify `avx512f` and AMX flags in JSON. |

Official references:

- AWS C7i: https://aws.amazon.com/ec2/instance-types/c7i/
- Google Cloud C3: https://cloud.google.com/compute/docs/general-purpose-machines#c3_machine_series
- Google Cloud CPU platforms: https://cloud.google.com/compute/docs/cpu-platforms

## Azure Cloud Shell Path

Open Azure Cloud Shell in Bash mode and run:

```bash
set -euo pipefail

RG=wearedge-amx-bench-rg
LOC=eastus2
VM=wearedge-amx-bench
SIZE=Standard_D4s_v6
USER=azureuser

az group create -n "$RG" -l "$LOC"
az vm create \
  -g "$RG" \
  -n "$VM" \
  --image Ubuntu2204 \
  --size "$SIZE" \
  --admin-username "$USER" \
  --generate-ssh-keys \
  --public-ip-sku Standard

az vm run-command invoke \
  -g "$RG" \
  -n "$VM" \
  --command-id RunShellScript \
  --scripts "curl -fsSL https://raw.githubusercontent.com/davidmillerak2026-sys/wearedge-opea-manufacturing/main/scripts/xeon_amx_benchmark_remote.sh | bash"

az vm run-command invoke \
  -g "$RG" \
  -n "$VM" \
  --command-id RunShellScript \
  --scripts "cat /home/$USER/wearedge-opea-manufacturing/evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json"
```

Save the final JSON output locally as:

```text
evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json
```

Clean up immediately:

```bash
az group delete -n "$RG" --yes --no-wait
```

## AWS Path

Use `c7i.xlarge` in a region where C7i is available.

```bash
INSTANCE_TYPE=c7i.xlarge
REGION=us-east-1
```

Run `scripts/xeon_amx_benchmark_remote.sh` on the instance and copy back:

```bash
bash scripts/xeon_amx_benchmark_remote.sh
scp ubuntu@<public-ip>:~/wearedge-opea-manufacturing/evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json evidence/benchmarks/
```

## Google Cloud Path

Use `c3-standard-4`. The submitted evidence used `us-central1-a`:

```bash
gcloud compute instances create wearedge-amx-bench \
  --zone=us-central1-a \
  --machine-type=c3-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud
```

SSH and run:

```bash
gcloud compute ssh wearedge-amx-bench --zone=us-central1-a
curl -fsSL https://raw.githubusercontent.com/davidmillerak2026-sys/wearedge-opea-manufacturing/main/scripts/xeon_amx_benchmark_remote.sh | bash
```

Copy the result:

```bash
gcloud compute scp \
  wearedge-amx-bench:~/wearedge-opea-manufacturing/evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json \
  evidence/benchmarks/ \
  --zone=us-central1-a
```

## Acceptance Criteria

The benchmark JSON must show:

```json
{
  "feature_detection": {
    "avx512f": true,
    "amx_tile": true
  }
}
```

At least one AMX flag must be true:

```text
amx_tile, amx_int8, amx_bf16
```

The scorecard must show:

```json
"scorecard": { "ok": true }
```
