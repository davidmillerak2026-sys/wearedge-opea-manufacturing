#!/usr/bin/env bash
set -euo pipefail

# Cloud Shell controller for the judge-facing Docker/Qdrant E2E benchmark.
# It creates a temporary Google Cloud C3 VM, performs a fresh clone, runs
# docker compose with Qdrant, captures API/latency/container evidence, copies
# the artifact back to Cloud Shell, and deletes the VM unless KEEP_VM=1.

PROJECT_ID="${PROJECT_ID:-gen-lang-client-0555254036}"
REPO_URL="${REPO_URL:-https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing.git}"
BRANCH="${BRANCH:-main}"
MACHINE_TYPE="${MACHINE_TYPE:-c3-standard-4}"
IMAGE_FAMILY="${IMAGE_FAMILY:-ubuntu-2404-lts-amd64}"
IMAGE_PROJECT="${IMAGE_PROJECT:-ubuntu-os-cloud}"
BOOT_DISK_SIZE="${BOOT_DISK_SIZE:-30GB}"
VM_NAME="${VM_NAME:-wearedge-docker-e2e-$(date +%m%d%H%M%S)}"
ARTIFACT_NAME="${ARTIFACT_NAME:-gcp_c3_docker_qdrant_e2e.json}"
LOCAL_ARTIFACT="${LOCAL_ARTIFACT:-$HOME/$ARTIFACT_NAME}"
REMOTE_SCRIPT="/tmp/wearedge_gcp_c3_docker_qdrant_e2e_remote.sh"
REMOTE_ARTIFACT="/tmp/$ARTIFACT_NAME"

if [ -n "${ZONE:-}" ]; then
  CANDIDATE_ZONES=("$ZONE")
else
  CANDIDATE_ZONES=(
    us-central1-a
    us-central1-b
    us-central1-c
    us-central1-f
    us-east1-b
    us-east1-c
    us-east4-a
    us-east4-b
  )
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
echo "Machine: $MACHINE_TYPE"

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

echo "Created VM: $VM_NAME in $CREATED_ZONE"
echo "GCP instance CPU platform:"
gcloud compute instances describe "$VM_NAME" \
  --project "$PROJECT_ID" \
  --zone "$CREATED_ZONE" \
  --format="value(cpuPlatform)" || true

echo "Waiting for SSH..."
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
OUTPUT="${OUTPUT:-/tmp/gcp_c3_docker_qdrant_e2e.json}"
WORKDIR="${WORKDIR:-$HOME/wearedge-opea-manufacturing-fresh}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8088}"
MODES=(maintenance iqc changeover wi hazard)

sudo apt-get update
if ! sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  ca-certificates \
  curl \
  docker-compose-v2 \
  docker.io \
  git \
  jq \
  procps \
  python3 \
  python3-venv; then
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ca-certificates \
    curl \
    docker-compose \
    docker.io \
    git \
    jq \
    procps \
    python3 \
    python3-venv
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

mkdir -p /tmp/wearedge-e2e
lscpu -J > /tmp/wearedge-e2e/lscpu.json || true
uname -a > /tmp/wearedge-e2e/uname.txt
python3 --version > /tmp/wearedge-e2e/python_version.txt
docker --version > /tmp/wearedge-e2e/docker_version.txt
compose version > /tmp/wearedge-e2e/docker_compose_version.txt
git rev-parse HEAD > /tmp/wearedge-e2e/git_commit.txt

metadata() {
  local path="$1"
  curl -fsS -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/$path" || true
}

{
  printf '{"project_id":"%s",' "$(metadata project/project-id)"
  printf '"instance_id":"%s",' "$(metadata instance/id)"
  printf '"hostname":"%s",' "$(metadata instance/hostname)"
  printf '"machine_type":"%s",' "$(metadata instance/machine-type)"
  printf '"zone":"%s",' "$(metadata instance/zone)"
  printf '"cpu_platform":"%s"}\n' "$(metadata instance/cpu-platform)"
} > /tmp/wearedge-e2e/gcp_metadata.json

SETUP_START="$(date +%s)"
compose up --build -d

for _ in $(seq 1 90); do
  if curl -fsS "$BASE_URL/healthz" > /tmp/wearedge-e2e/healthz.json; then
    break
  fi
  sleep 2
done
SETUP_SECONDS="$(( $(date +%s) - SETUP_START ))"
printf '%s\n' "$SETUP_SECONDS" > /tmp/wearedge-e2e/setup_seconds.txt

DEMO_HTTP_CODE="$(curl -sS -o /tmp/wearedge-e2e/demo.html -w "%{http_code}" "$BASE_URL/demo")"
printf '%s\n' "$DEMO_HTTP_CODE" > /tmp/wearedge-e2e/demo_http_code.txt
curl -fsS "$BASE_URL/healthz" > /tmp/wearedge-e2e/healthz.json
curl -fsS "$BASE_URL/v1/agents" > /tmp/wearedge-e2e/agents.json
curl -fsS "$BASE_URL/v1/scorecard" > /tmp/wearedge-e2e/scorecard.json
curl -fsS "http://127.0.0.1:6333/" > /tmp/wearedge-e2e/qdrant_root.json || true

for mode in "${MODES[@]}"; do
  curl -fsS "$BASE_URL/v1/agents/$mode/demo" > "/tmp/wearedge-e2e/demo_$mode.json"
  curl -fsS -X POST \
    -H "Content-Type: application/json" \
    -d '{}' \
    "$BASE_URL/v1/agents/$mode/infer" > "/tmp/wearedge-e2e/infer_$mode.json"
done

python3 - <<'PY'
from __future__ import annotations

import json
import math
import statistics
import time
import urllib.request
from pathlib import Path

base_url = "http://127.0.0.1:8088"
modes = ["maintenance", "iqc", "changeover", "wi", "hazard"]
endpoints: list[tuple[str, str, bytes | None]] = [
    ("GET /healthz", "/healthz", None),
    ("GET /v1/agents", "/v1/agents", None),
    ("GET /v1/scorecard", "/v1/scorecard", None),
]
for mode in modes:
    endpoints.append((f"GET /v1/agents/{mode}/demo", f"/v1/agents/{mode}/demo", None))
for mode in modes:
    endpoints.append((f"POST /v1/agents/{mode}/infer", f"/v1/agents/{mode}/infer", b"{}"))

def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil((p / 100.0) * len(ordered)) - 1))
    return ordered[index]

def call(path: str, body: bytes | None) -> int:
    headers = {"Content-Type": "application/json"} if body is not None else {}
    method = "POST" if body is not None else "GET"
    req = urllib.request.Request(base_url + path, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as resp:
        resp.read()
        return int(resp.status)

summary = {}
for label, path, body in endpoints:
    samples = []
    statuses = []
    for _ in range(30):
        start = time.perf_counter()
        statuses.append(call(path, body))
        samples.append((time.perf_counter() - start) * 1000)
    summary[label] = {
        "count": len(samples),
        "status_codes": sorted(set(statuses)),
        "min_ms": round(min(samples), 4),
        "mean_ms": round(statistics.mean(samples), 4),
        "p50_ms": round(percentile(samples, 50), 4),
        "p95_ms": round(percentile(samples, 95), 4),
        "max_ms": round(max(samples), 4),
    }

Path("/tmp/wearedge-e2e/latency_summary.json").write_text(
    json.dumps(summary, indent=2),
    encoding="utf-8",
)
PY

sudo docker stats --no-stream --format '{{json .}}' > /tmp/wearedge-e2e/docker_stats.jsonl || true
compose ps --format json > /tmp/wearedge-e2e/docker_compose_ps.jsonl || true
sudo docker image ls --format '{{json .}}' > /tmp/wearedge-e2e/docker_images.jsonl || true
compose logs --tail=160 > /tmp/wearedge-e2e/docker_compose_logs.txt || true

python3 - <<'PY'
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

root = Path("/tmp/wearedge-e2e")
output = Path(os.environ.get("OUTPUT", "/tmp/gcp_c3_docker_qdrant_e2e.json"))
modes = ["maintenance", "iqc", "changeover", "wi", "hazard"]
expected_targets = {
    "maintenance": "maintenance_work_order",
    "iqc": "qms_quality_event",
    "changeover": "changeover_checklist",
    "wi": "wi_reference",
    "hazard": "ehs_case",
}

def text(name: str) -> str:
    path = root / name
    return path.read_text(encoding="utf-8", errors="replace").strip() if path.exists() else ""

def load_json(name: str) -> dict:
    value = text(name)
    return json.loads(value) if value else {}

def load_jsonl(name: str) -> list[dict]:
    path = root / name
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"raw": line})
    return rows

cpuinfo = Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace")
flags_match = re.search(r"^flags\s*:\s*(.+)$", cpuinfo, re.MULTILINE)
flags = set(flags_match.group(1).split()) if flags_match else set()
feature_detection = {
    "avx2": "avx2" in flags,
    "avx512f": "avx512f" in flags,
    "avx512_bf16": "avx512_bf16" in flags,
    "avx512_vnni": "avx512_vnni" in flags,
    "amx_tile": "amx_tile" in flags,
    "amx_int8": "amx_int8" in flags,
    "amx_bf16": "amx_bf16" in flags,
}

health = load_json("healthz.json")
agents = load_json("agents.json")
scorecard = load_json("scorecard.json")
demos = {mode: load_json(f"demo_{mode}.json") for mode in modes}
infers = {mode: load_json(f"infer_{mode}.json") for mode in modes}
latency = load_json("latency_summary.json")
score_routes = scorecard.get("routes", [])

infer_target_checks = {
    mode: infers[mode].get("action_card", {}).get("integration_target") == expected_targets[mode]
    for mode in modes
}
demo_target_checks = {
    mode: demos[mode].get("action_card", {}).get("integration_target") == expected_targets[mode]
    for mode in modes
}

validation = {
    "demo_http_200": text("demo_http_code.txt") == "200",
    "health_ok": health.get("ok") is True,
    "qdrant_backend": health.get("vector_backend") == "qdrant",
    "qdrant_endpoint_responds": bool(load_json("qdrant_root.json")),
    "five_agents": sorted(agents.get("modes", [])) == sorted(modes),
    "all_demo_ok": all(demos[mode].get("ok") is True for mode in modes),
    "all_infer_ok": all(infers[mode].get("ok") is True for mode in modes),
    "demo_action_targets_correct": all(demo_target_checks.values()),
    "infer_action_targets_correct": all(infer_target_checks.values()),
    "scorecard_ok": scorecard.get("ok") is True,
    "scorecard_has_five_routes": sorted(route.get("mode") for route in score_routes) == sorted(modes),
    "scorecard_routes_pass": all(route.get("status") == "pass" for route in score_routes),
    "docker_stats_captured": bool(text("docker_stats.jsonl")),
}

artifact = {
    "benchmark": "WearEdge OPEA Manufacturing GCP C3 Docker/Qdrant fresh-clone E2E benchmark",
    "schema_version": "2026-05-27",
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "claim_status": "fresh_clone_docker_qdrant_e2e_on_gcp_c3_xeon",
    "repo": {
        "url": os.environ.get("REPO_URL", "https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing.git"),
        "branch": os.environ.get("BRANCH", "main"),
        "commit": text("git_commit.txt"),
    },
    "gcp": load_json("gcp_metadata.json"),
    "host": {
        "uname": text("uname.txt"),
        "lscpu": load_json("lscpu.json"),
        "feature_detection": feature_detection,
    },
    "runtime": {
        "python_version": text("python_version.txt"),
        "docker_version": text("docker_version.txt"),
        "docker_compose_version": text("docker_compose_version.txt"),
        "setup_seconds": int(text("setup_seconds.txt") or "0"),
        "base_url": "http://127.0.0.1:8088",
    },
    "docker": {
        "stats": load_jsonl("docker_stats.jsonl"),
        "compose_ps": load_jsonl("docker_compose_ps.jsonl"),
        "images": load_jsonl("docker_images.jsonl"),
        "compose_logs_tail": text("docker_compose_logs.txt")[-12000:],
    },
    "endpoints": {
        "demo_http_code": text("demo_http_code.txt"),
        "healthz": health,
        "qdrant_root": load_json("qdrant_root.json"),
        "agents": agents,
        "scorecard": scorecard,
        "demos": demos,
        "infers": infers,
    },
    "latency": latency,
    "validation": validation,
    "all_checks_pass": all(validation.values()),
}

output.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

print("Benchmark artifact:", output)
print("all_checks_pass:", artifact["all_checks_pass"])
print("setup_seconds:", artifact["runtime"]["setup_seconds"])
print("feature_detection:", json.dumps(feature_detection, sort_keys=True))
for label, item in latency.items():
    print(f"{label}: p50={item['p50_ms']}ms p95={item['p95_ms']}ms statuses={item['status_codes']}")

if not artifact["all_checks_pass"]:
    failed = [name for name, ok in validation.items() if not ok]
    raise SystemExit("E2E validation failed: " + ", ".join(failed))
PY

compose down >/dev/null 2>&1 || true
REMOTE_EOF

chmod +x "$REMOTE_SCRIPT"

echo "Copying remote benchmark script..."
gcloud compute scp "$REMOTE_SCRIPT" "$VM_NAME:$REMOTE_SCRIPT" \
  --project "$PROJECT_ID" \
  --zone "$CREATED_ZONE" \
  --quiet

echo "Running Docker/Qdrant fresh-clone E2E benchmark on $VM_NAME..."
gcloud compute ssh "$VM_NAME" \
  --project "$PROJECT_ID" \
  --zone "$CREATED_ZONE" \
  --command "REPO_URL='$REPO_URL' BRANCH='$BRANCH' OUTPUT='$REMOTE_ARTIFACT' bash '$REMOTE_SCRIPT'" \
  --quiet

echo "Copying artifact back to Cloud Shell..."
gcloud compute scp "$VM_NAME:$REMOTE_ARTIFACT" "$LOCAL_ARTIFACT" \
  --project "$PROJECT_ID" \
  --zone "$CREATED_ZONE" \
  --quiet

echo
echo "Benchmark summary:"
python3 - "$LOCAL_ARTIFACT" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
artifact = json.loads(path.read_text(encoding="utf-8"))
features = artifact["host"]["feature_detection"]
latency = artifact["latency"]
print(json.dumps({
    "file": str(path),
    "machine_type": artifact["gcp"].get("machine_type", "").split("/")[-1],
    "zone": artifact["gcp"].get("zone", "").split("/")[-1],
    "cpu_platform": artifact["gcp"].get("cpu_platform"),
    "avx512f": features.get("avx512f"),
    "amx_tile": features.get("amx_tile"),
    "amx_int8": features.get("amx_int8"),
    "amx_bf16": features.get("amx_bf16"),
    "setup_seconds": artifact["runtime"]["setup_seconds"],
    "all_checks_pass": artifact["all_checks_pass"],
    "scorecard_ok": artifact["endpoints"]["scorecard"].get("ok"),
    "health_backend": artifact["endpoints"]["healthz"].get("vector_backend"),
    "scorecard_p95_ms": latency.get("GET /v1/scorecard", {}).get("p95_ms"),
}, indent=2))

if not artifact["all_checks_pass"]:
    raise SystemExit("Benchmark did not pass all validation checks.")
PY

echo
echo "=== BEGIN GCP C3 DOCKER/QDRANT E2E JSON ==="
cat "$LOCAL_ARTIFACT"
echo
echo "=== END GCP C3 DOCKER/QDRANT E2E JSON ==="
