#!/usr/bin/env bash
# SPDX-License-Identifier: MIT

set -euo pipefail

# Cloud Shell controller for the official OPEA TEI embedding profile E2E check.
# It validates:
# fresh clone -> docker-compose.opea-tei.yml -> TEI -> OPEA embedding microservice
# -> Qdrant -> Manufacturing Gateway -> five-agent scorecard.

PROJECT_ID="${PROJECT_ID:-gen-lang-client-0555254036}"
REPO_URL="${REPO_URL:-https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing.git}"
BRANCH="${BRANCH:-main}"
MACHINE_TYPE="${MACHINE_TYPE:-c3-standard-4}"
IMAGE_FAMILY="${IMAGE_FAMILY:-ubuntu-2404-lts-amd64}"
IMAGE_PROJECT="${IMAGE_PROJECT:-ubuntu-os-cloud}"
BOOT_DISK_SIZE="${BOOT_DISK_SIZE:-50GB}"
VM_NAME="${VM_NAME:-wearedge-opea-tei-$(date +%m%d%H%M%S)}"
ARTIFACT_NAME="${ARTIFACT_NAME:-gcp_c3_opea_tei_profile_e2e.json}"
LOCAL_ARTIFACT="${LOCAL_ARTIFACT:-$HOME/$ARTIFACT_NAME}"
REMOTE_SCRIPT="/tmp/wearedge_gcp_c3_opea_tei_profile_e2e_remote.sh"
REMOTE_ARTIFACT="/tmp/$ARTIFACT_NAME"

if [ -n "${ZONE:-}" ]; then
  CANDIDATE_ZONES=("$ZONE")
else
  CANDIDATE_ZONES=(us-central1-a us-central1-b us-central1-c us-central1-f us-east1-b us-east4-a)
fi

CREATED_ZONE=""

cleanup() {
  if [ "${KEEP_VM:-0}" = "1" ]; then
    echo "KEEP_VM=1; leaving VM $VM_NAME in zone ${CREATED_ZONE:-unknown}."
    return
  fi
  if [ -n "$CREATED_ZONE" ]; then
    echo "Cleaning up VM: $VM_NAME in $CREATED_ZONE"
    gcloud compute instances delete "$VM_NAME" \
      --project "$PROJECT_ID" \
      --zone "$CREATED_ZONE" \
      --quiet || true
  fi
}
trap cleanup EXIT

echo "This benchmark creates a billable temporary C3 VM and deletes it on exit."
echo "Project: $PROJECT_ID"
echo "Repo: $REPO_URL ($BRANCH)"
echo "Profile: docker-compose.yml + docker-compose.opea-tei.yml"
echo "Machine type: $MACHINE_TYPE"

gcloud config set project "$PROJECT_ID" >/dev/null
gcloud services enable compute.googleapis.com --project "$PROJECT_ID" >/dev/null

for candidate in "${CANDIDATE_ZONES[@]}"; do
  echo "Trying zone: $candidate"
  if gcloud compute instances create "$VM_NAME" \
    --project "$PROJECT_ID" \
    --zone "$candidate" \
    --machine-type "$MACHINE_TYPE" \
    --image-family "$IMAGE_FAMILY" \
    --image-project "$IMAGE_PROJECT" \
    --boot-disk-size "$BOOT_DISK_SIZE" \
    --scopes cloud-platform \
    --metadata enable-oslogin=FALSE \
    --quiet; then
    CREATED_ZONE="$candidate"
    break
  fi
done

if [ -z "$CREATED_ZONE" ]; then
  echo "Could not create $MACHINE_TYPE in the candidate zones." >&2
  exit 1
fi

for _ in $(seq 1 30); do
  if gcloud compute ssh "$VM_NAME" \
    --project "$PROJECT_ID" \
    --zone "$CREATED_ZONE" \
    --command "echo ssh-ready" \
    --quiet >/dev/null 2>&1; then
    break
  fi
  sleep 10
done

cat > "$REMOTE_SCRIPT" <<'REMOTE_EOF'
#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing.git}"
BRANCH="${BRANCH:-main}"
OUTPUT="${OUTPUT:-/tmp/gcp_c3_opea_tei_profile_e2e.json}"
WORKDIR="${WORKDIR:-$HOME/wearedge-opea-tei-fresh}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8088}"
EMBED_URL="${EMBED_URL:-http://127.0.0.1:6000}"
EMBEDDING_MODEL_ID="${EMBEDDING_MODEL_ID:-BAAI/bge-base-en-v1.5}"
OPEA_EMBEDDING_IMAGE="${OPEA_EMBEDDING_IMAGE:-opea/embedding:latest}"
TEI_IMAGE="${TEI_IMAGE:-ghcr.io/huggingface/text-embeddings-inference:cpu-latest}"
MODES=(maintenance iqc changeover wi hazard)

sudo apt-get update
if ! sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  ca-certificates curl docker-compose-v2 docker.io git jq procps python3 python3-venv; then
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ca-certificates curl docker-compose docker.io git jq procps python3 python3-venv
fi
sudo systemctl enable --now docker

compose() {
  if sudo docker compose version >/dev/null 2>&1; then
    sudo docker compose "$@"
  elif command -v docker-compose >/dev/null 2>&1; then
    sudo docker-compose "$@"
  else
    echo "Docker Compose is not available." >&2
    return 127
  fi
}

rm -rf "$WORKDIR"
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$WORKDIR"
cd "$WORKDIR"

mkdir -p /tmp/wearedge-opea-tei
lscpu -J > /tmp/wearedge-opea-tei/lscpu.json || true
uname -a > /tmp/wearedge-opea-tei/uname.txt
docker --version > /tmp/wearedge-opea-tei/docker_version.txt
compose version > /tmp/wearedge-opea-tei/docker_compose_version.txt
git rev-parse HEAD > /tmp/wearedge-opea-tei/git_commit.txt

metadata() {
  local path="$1"
  curl -fsS -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/$path" || true
}

{
  printf '{"project_id":"%s",' "$(metadata project/project-id)"
  printf '"machine_type":"%s",' "$(metadata instance/machine-type)"
  printf '"zone":"%s",' "$(metadata instance/zone)"
  printf '"cpu_platform":"%s"}\n' "$(metadata instance/cpu-platform)"
} > /tmp/wearedge-opea-tei/gcp_metadata.json

{
  echo "OPEA_EMBEDDING_IMAGE=$OPEA_EMBEDDING_IMAGE"
  echo "TEI_IMAGE=$TEI_IMAGE"
  echo "EMBEDDING_MODEL_ID=$EMBEDDING_MODEL_ID"
} > /tmp/wearedge-opea-tei/profile_env.txt

START="$(date +%s)"

if ! sudo docker pull "$OPEA_EMBEDDING_IMAGE"; then
  echo "Could not pull $OPEA_EMBEDDING_IMAGE; building OPEA embedding image from GenAIComps."
  rm -rf /tmp/GenAIComps
  git clone --depth 1 https://github.com/opea-project/GenAIComps /tmp/GenAIComps
  sudo docker build -t "$OPEA_EMBEDDING_IMAGE" -f /tmp/GenAIComps/comps/embeddings/src/Dockerfile /tmp/GenAIComps
fi

sudo docker pull "$TEI_IMAGE"

TEI_IMAGE="$TEI_IMAGE" \
OPEA_EMBEDDING_IMAGE="$OPEA_EMBEDDING_IMAGE" \
EMBEDDING_MODEL_ID="$EMBEDDING_MODEL_ID" \
compose -f docker-compose.yml -f docker-compose.opea-tei.yml up -d

for _ in $(seq 1 180); do
  if curl -fsS "$EMBED_URL/v1/health_check" > /tmp/wearedge-opea-tei/embedding_health_raw.txt; then
    break
  fi
  sleep 5
done

for _ in $(seq 1 120); do
  if curl -fsS -X POST \
    -H "Content-Type: application/json" \
    -d '{"input":"WearEdge OPEA TEI embedding profile smoke test"}' \
    "$EMBED_URL/v1/embeddings" > /tmp/wearedge-opea-tei/embedding_response.json; then
    break
  fi
  sleep 5
done

for _ in $(seq 1 90); do
  if curl -fsS "$BASE_URL/healthz" > /tmp/wearedge-opea-tei/healthz.json; then
    break
  fi
  sleep 2
done

curl -fsS "$BASE_URL/healthz" > /tmp/wearedge-opea-tei/healthz.json
curl -fsS "$BASE_URL/v1/scorecard" > /tmp/wearedge-opea-tei/scorecard.json

for mode in "${MODES[@]}"; do
  curl -fsS "$BASE_URL/v1/agents/$mode/demo" > "/tmp/wearedge-opea-tei/demo_$mode.json"
done

SETUP_SECONDS="$(( $(date +%s) - START ))"
printf '%s\n' "$SETUP_SECONDS" > /tmp/wearedge-opea-tei/setup_seconds.txt

sudo docker stats --no-stream --format '{{json .}}' > /tmp/wearedge-opea-tei/docker_stats.jsonl || true
compose ps --format json > /tmp/wearedge-opea-tei/docker_compose_ps.jsonl || true
compose logs --tail=220 > /tmp/wearedge-opea-tei/docker_compose_logs.txt || true

python3 - <<'PY'
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

root = Path("/tmp/wearedge-opea-tei")
output = Path(os.environ.get("OUTPUT", "/tmp/gcp_c3_opea_tei_profile_e2e.json"))
modes = ["maintenance", "iqc", "changeover", "wi", "hazard"]

def text(name: str) -> str:
    path = root / name
    return path.read_text(encoding="utf-8", errors="replace").strip() if path.exists() else ""

def load_json(name: str):
    value = text(name)
    return json.loads(value) if value else {}

def load_jsonl(name: str):
    rows = []
    for line in text(name).splitlines():
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"raw": line})
    return rows

health = load_json("healthz.json")
embedding_response = load_json("embedding_response.json")
scorecard = load_json("scorecard.json")
samples = {mode: load_json(f"demo_{mode}.json") for mode in modes}

embedding_vector = embedding_response.get("data", [{}])[0].get("embedding", [])
rag_markers = {
    mode: samples[mode].get("rag", {}).get("vector_store")
    for mode in modes
}

validation = {
    "gateway_ok": health.get("ok") is True,
    "qdrant_backend": health.get("vector_backend") == "qdrant",
    "gateway_embedding_backend_opea": health.get("embedding_backend") == "opea",
    "gateway_embedding_url_is_opea_tei": health.get("embedding_url") == "http://opea-embedding-tei:6000/v1/embeddings",
    "embedding_health_endpoint_responds": bool(text("embedding_health_raw.txt")),
    "embedding_endpoint_openai_shape": bool(embedding_vector),
    "embedding_dimensions_768": len(embedding_vector) == 768,
    "all_samples_ok": all(samples[mode].get("ok") is True for mode in modes),
    "all_rag_uses_opea_tei_marker": all(
        marker == "qdrant-opea-tei-vector-store"
        for marker in rag_markers.values()
    ),
    "scorecard_ok": scorecard.get("ok") is True,
    "scorecard_routes_pass": all(route.get("status") == "pass" for route in scorecard.get("routes", [])),
}

artifact = {
    "benchmark": "WearEdge official OPEA TEI embedding profile E2E",
    "schema_version": "2026-05-27",
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "claim_status": "fresh_clone_official_opea_tei_embedding_profile_e2e",
    "official_references": [
        "https://opea-project.github.io/latest/GenAIComps/comps/embeddings/src/README_tei.html",
        "https://github.com/opea-project/GenAIComps",
        "https://github.com/opea-project/GenAIExamples",
        "https://huggingface.co/docs/text-embeddings-inference/index",
    ],
    "repo": {
        "url": os.environ.get("REPO_URL", "https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing.git"),
        "branch": os.environ.get("BRANCH", "main"),
        "commit": text("git_commit.txt"),
    },
    "gcp": load_json("gcp_metadata.json"),
    "runtime": {
        "setup_seconds": int(text("setup_seconds.txt") or "0"),
        "docker_version": text("docker_version.txt"),
        "docker_compose_version": text("docker_compose_version.txt"),
        "profile_env": text("profile_env.txt").splitlines(),
    },
    "host": {
        "uname": text("uname.txt"),
        "lscpu": load_json("lscpu.json"),
    },
    "endpoints": {
        "gateway_healthz": health,
        "embedding_health_raw": text("embedding_health_raw.txt"),
        "embedding_response_sample": embedding_response,
        "scorecard": scorecard,
        "samples": samples,
    },
    "rag_vector_store_markers": rag_markers,
    "docker": {
        "stats": load_jsonl("docker_stats.jsonl"),
        "compose_ps": load_jsonl("docker_compose_ps.jsonl"),
        "compose_logs_tail": text("docker_compose_logs.txt")[-16000:],
    },
    "validation": validation,
    "all_checks_pass": all(validation.values()),
}

output.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
print("artifact:", output)
print("all_checks_pass:", artifact["all_checks_pass"])
print("setup_seconds:", artifact["runtime"]["setup_seconds"])
print("embedding_dimensions:", len(embedding_vector))
print("rag_vector_store_markers:", json.dumps(rag_markers, sort_keys=True))

if not artifact["all_checks_pass"]:
    failed = [name for name, ok in validation.items() if not ok]
    raise SystemExit("Official OPEA TEI profile E2E failed: " + ", ".join(failed))
PY

compose -f docker-compose.yml -f docker-compose.opea-tei.yml down >/dev/null 2>&1 || true
REMOTE_EOF

chmod +x "$REMOTE_SCRIPT"
gcloud compute scp "$REMOTE_SCRIPT" "$VM_NAME:$REMOTE_SCRIPT" \
  --project "$PROJECT_ID" \
  --zone "$CREATED_ZONE" \
  --quiet

gcloud compute ssh "$VM_NAME" \
  --project "$PROJECT_ID" \
  --zone "$CREATED_ZONE" \
  --command "REPO_URL='$REPO_URL' BRANCH='$BRANCH' OUTPUT='$REMOTE_ARTIFACT' bash '$REMOTE_SCRIPT'" \
  --quiet

gcloud compute scp "$VM_NAME:$REMOTE_ARTIFACT" "$LOCAL_ARTIFACT" \
  --project "$PROJECT_ID" \
  --zone "$CREATED_ZONE" \
  --quiet

echo
echo "Official OPEA TEI profile summary:"
python3 - "$LOCAL_ARTIFACT" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
artifact = json.loads(path.read_text(encoding="utf-8"))
embedding = artifact["endpoints"]["embedding_response_sample"].get("data", [{}])[0].get("embedding", [])
print(json.dumps({
    "file": str(path),
    "machine_type": artifact["gcp"].get("machine_type", "").split("/")[-1],
    "zone": artifact["gcp"].get("zone", "").split("/")[-1],
    "cpu_platform": artifact["gcp"].get("cpu_platform"),
    "setup_seconds": artifact["runtime"]["setup_seconds"],
    "all_checks_pass": artifact["all_checks_pass"],
    "embedding_backend": artifact["endpoints"]["gateway_healthz"].get("embedding_backend"),
    "embedding_dimensions": len(embedding),
    "scorecard_ok": artifact["endpoints"]["scorecard"].get("ok"),
    "rag_vector_store_markers": artifact["rag_vector_store_markers"],
}, indent=2))

if not artifact["all_checks_pass"]:
    raise SystemExit("Official OPEA TEI profile benchmark did not pass all checks.")
PY

echo
echo "=== BEGIN GCP C3 OFFICIAL OPEA TEI PROFILE E2E JSON ==="
cat "$LOCAL_ARTIFACT"
echo
echo "=== END GCP C3 OFFICIAL OPEA TEI PROFILE E2E JSON ==="
