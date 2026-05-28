#!/usr/bin/env bash
set -Eeuo pipefail

# Google Cloud Shell script: create a temporary C3 VM, fresh-clone the public
# OPEA submission repo, run official OPEA TEI + Qdrant, and capture CPU flags,
# Docker stats, TEI/OPEA logs, and oneDNN/ISA dispatch markers when emitted.

PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"
ZONE="${ZONE:-us-central1-a}"
MACHINE_TYPE="${MACHINE_TYPE:-c3-standard-4}"
VM_NAME="${VM_NAME:-wearedge-tei-onednn-$(date +%m%d%H%M%S)}"
REPO_URL="${REPO_URL:-https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing.git}"
BRANCH="${BRANCH:-main}"
KEEP_VM="${KEEP_VM:-0}"
ARTIFACT_LOCAL="${ARTIFACT_LOCAL:-$HOME/gcp_c3_tei_onednn_verbose.json}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "PROJECT_ID is not set. Run: gcloud config set project <PROJECT_ID>" >&2
  exit 1
fi

cleanup() {
  if [[ "$KEEP_VM" == "1" ]]; then
    echo "KEEP_VM=1; leaving VM running: $VM_NAME"
    return
  fi
  echo "Cleaning up VM: $VM_NAME in $ZONE"
  gcloud compute instances delete "$VM_NAME" --project "$PROJECT_ID" --zone "$ZONE" --quiet || true
}
trap cleanup EXIT

echo "Project=$PROJECT_ID Zone=$ZONE Machine=$MACHINE_TYPE VM=$VM_NAME"
gcloud services enable compute.googleapis.com --project "$PROJECT_ID" >/dev/null

gcloud compute instances create "$VM_NAME" \
  --project "$PROJECT_ID" \
  --zone "$ZONE" \
  --machine-type "$MACHINE_TYPE" \
  --image-family ubuntu-2404-lts-amd64 \
  --image-project ubuntu-os-cloud \
  --boot-disk-size 80GB \
  --boot-disk-type pd-balanced \
  --scopes cloud-platform \
  --metadata enable-oslogin=FALSE \
  --quiet

for _ in {1..30}; do
  if gcloud compute ssh "$VM_NAME" --project "$PROJECT_ID" --zone "$ZONE" --command "echo ready" --quiet >/dev/null 2>&1; then
    break
  fi
  sleep 5
done

cat > /tmp/wearedge-tei-onednn-run.sh <<REMOTE_EOF
set -Eeuo pipefail

WORKDIR="\$HOME/wearedge-opea-tei-onednn"
ARTIFACT="\$HOME/gcp_c3_tei_onednn_verbose.json"

sudo apt-get update -y
sudo apt-get install -y ca-certificates curl git jq python3 docker.io docker-compose-v2
sudo systemctl enable --now docker

rm -rf "\$WORKDIR"
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "\$WORKDIR"
cd "\$WORKDIR"

cat > docker-compose.onednn-verbose.yml <<'YAML'
services:
  tei-embedding-serving:
    environment:
      ONEDNN_VERBOSE: "1"
      DNNL_VERBOSE: "1"
      MKLDNN_VERBOSE: "1"
      RUST_LOG: "info"
  opea-embedding-tei:
    environment:
      ONEDNN_VERBOSE: "1"
      DNNL_VERBOSE: "1"
      MKLDNN_VERBOSE: "1"
      RUST_LOG: "info"
YAML

docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml -f docker-compose.onednn-verbose.yml up -d --build

for _ in {1..90}; do
  if curl -fsS http://127.0.0.1:8088/healthz >/tmp/healthz.json 2>/dev/null; then
    break
  fi
  sleep 3
done

curl -fsS http://127.0.0.1:8088/healthz > /tmp/healthz.json
curl -fsS http://127.0.0.1:6000/v1/health_check > /tmp/embedding_health.json || true
curl -fsS http://127.0.0.1:8088/v1/scorecard > /tmp/scorecard.json
for mode in maintenance iqc changeover wi hazard; do
  curl -fsS "http://127.0.0.1:8088/v1/agents/\${mode}/demo" >"/tmp/demo-\${mode}.json"
done
for i in \$(seq 1 10); do
  curl -fsS http://127.0.0.1:6000/v1/embeddings \
    -H 'Content-Type: application/json' \
    -d "{\"model\":\"BAAI/bge-base-en-v1.5\",\"input\":\"WearEdge TEI oneDNN verbose smoke \${i}\"}" \
    >"/tmp/embedding-\${i}.json" || true
done

docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml -f docker-compose.onednn-verbose.yml logs --no-color > /tmp/compose.logs.txt || true
docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml -f docker-compose.onednn-verbose.yml ps --format json > /tmp/compose.ps.json || true
docker stats --no-stream --format '{{json .}}' | jq -s . > /tmp/docker.stats.json || true
lscpu > /tmp/lscpu.txt
grep -m1 '^flags' /proc/cpuinfo > /tmp/cpu.flags.txt || true
grep -Ei 'onednn|dnnl|mkldnn|avx|amx|bf16|vnni|brgemm|matmul|isa' /tmp/compose.logs.txt > /tmp/dispatch.markers.txt || true

python3 - <<'PY' > "\$ARTIFACT"
import json
import pathlib
import re
import time

root = pathlib.Path("/tmp")

def read(name, default=""):
    path = root / name
    return path.read_text(errors="replace") if path.exists() else default

def read_json(name, default=None):
    path = root / name
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        return {"parse_error": str(exc), "raw": path.read_text(errors="replace")[:2000]}

logs = read("compose.logs.txt")
markers = read("dispatch.markers.txt")
flags = read("cpu.flags.txt")
flag_tokens = set(flags.lower().split())
feature_detection = {
    "avx512f": "avx512f" in flag_tokens,
    "avx512_bf16": "avx512_bf16" in flag_tokens,
    "avx512_vnni": "avx512_vnni" in flag_tokens,
    "amx_tile": "amx_tile" in flag_tokens,
    "amx_int8": "amx_int8" in flag_tokens,
    "amx_bf16": "amx_bf16" in flag_tokens,
}
dispatch_regex = re.compile(r"(onednn|dnnl|mkldnn|amx|avx512|avx|bf16|vnni|brgemm|matmul)", re.I)
dispatch_marker_lines = [line for line in markers.splitlines() if dispatch_regex.search(line)]

scorecard = read_json("scorecard.json", {})
healthz = read_json("healthz.json", {})
embedding_health = read_json("embedding_health.json", {})
demo_modes = {mode: read_json(f"demo-{mode}.json", {}) for mode in ["maintenance", "iqc", "changeover", "wi", "hazard"]}
docker_stats = read_json("docker.stats.json", [])
compose_ps = []
for line in read("compose.ps.json").splitlines():
    try:
        compose_ps.append(json.loads(line))
    except Exception:
        pass

validation = {
    "gateway_ok": healthz.get("ok") is True,
    "scorecard_ok": scorecard.get("ok") is True,
    "five_demos_ok": all((demo_modes.get(mode) or {}).get("ok") is True for mode in demo_modes),
    "docker_stats_captured": bool(docker_stats),
    "compose_ps_captured": bool(compose_ps),
    "c3_cpu_flags_include_avx512": feature_detection["avx512f"],
    "c3_cpu_flags_include_amx": feature_detection["amx_tile"] and feature_detection["amx_int8"],
    "tei_logs_present": "tei-embedding-serving" in logs or "text-embeddings" in logs.lower(),
    "dispatch_markers_captured": bool(dispatch_marker_lines),
}
artifact = {
    "benchmark": "WearEdge OPEA TEI oneDNN verbose / Intel ISA evidence on GCP C3",
    "schema_version": "2026-05-28",
    "created_at_epoch": time.time(),
    "claim_status": (
        "tei_onednn_or_isa_dispatch_markers_captured"
        if validation["dispatch_markers_captured"]
        else "tei_verbose_not_emitted_cpu_feature_evidence_only"
    ),
    "gcp_machine": {
        "machine_type": "c3-standard-4",
        "cpu_profile": "4 vCPU, 16 GiB RAM, no GPU",
        "single_node_challenge_limit": "<=64GB RAM, 4-core CPU profile, GPU optional",
    },
    "cpu": {
        "lscpu": read("lscpu.txt"),
        "flags_line": flags.strip(),
        "feature_detection": feature_detection,
    },
    "workload": {
        "compose_files": ["docker-compose.yml", "docker-compose.opea-tei.yml", "docker-compose.onednn-verbose.yml"],
        "services": ["manufacturing-gateway", "qdrant", "opea-embedding-tei", "tei-embedding-serving"],
        "healthz": healthz,
        "embedding_health": embedding_health,
        "scorecard": scorecard,
        "demo_modes": demo_modes,
    },
    "dispatch_evidence": {
        "marker_count": len(dispatch_marker_lines),
        "marker_lines": dispatch_marker_lines[:120],
        "note": "Some TEI builds may not emit oneDNN verbose logs even when CPU ISA flags are present; this records both the env-enabled attempt and observed markers.",
    },
    "docker": {"stats": docker_stats, "compose_ps": compose_ps},
    "validation": validation,
    "all_checks_pass": all(v for k, v in validation.items() if k != "dispatch_markers_captured"),
}
print(json.dumps(artifact, indent=2))
PY

echo "=== BEGIN GCP C3 TEI ONEDNN VERBOSE JSON ==="
cat "\$ARTIFACT"
echo "=== END GCP C3 TEI ONEDNN VERBOSE JSON ==="
REMOTE_EOF

gcloud compute scp /tmp/wearedge-tei-onednn-run.sh "$VM_NAME:/tmp/wearedge-tei-onednn-run.sh" --project "$PROJECT_ID" --zone "$ZONE" --quiet
gcloud compute ssh "$VM_NAME" --project "$PROJECT_ID" --zone "$ZONE" --command "bash /tmp/wearedge-tei-onednn-run.sh" --quiet
gcloud compute scp "$VM_NAME:~/gcp_c3_tei_onednn_verbose.json" "$ARTIFACT_LOCAL" --project "$PROJECT_ID" --zone "$ZONE" --quiet || true
echo "Artifact copied to: $ARTIFACT_LOCAL"
