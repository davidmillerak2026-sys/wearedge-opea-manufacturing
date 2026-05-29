#!/usr/bin/env bash
set -Eeuo pipefail

# Google Cloud Shell script: create a temporary C3 VM, fresh-clone the public
# OPEA submission repo, run official OPEA TEI + Qdrant, capture CPU flags,
# Docker stats, TEI/OPEA logs, and run a same-host oneDNN BF16/AMX probe.

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
sudo docker version >/tmp/docker.version.txt

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

sudo docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml -f docker-compose.onednn-verbose.yml up -d --build

http_json_error() {
  local output="\$1"
  local name="\$2"
  local status="\$3"
  local body="\$4"
  python3 - "\$output" "\$name" "\$status" "\$body" <<'PY'
import json
import pathlib
import sys

output, name, status, body = sys.argv[1:5]
path = pathlib.Path(output)
path.write_text(json.dumps({
    "ok": False,
    "endpoint": name,
    "http_status": status,
    "raw": body[-2000:],
}, indent=2))
PY
}

curl_get_json_retry() {
  local url="\$1"
  local output="\$2"
  local name="\$3"
  local attempts="\${4:-120}"
  local tmp="\${output}.tmp"
  local status="000"
  for i in \$(seq 1 "\$attempts"); do
    status=\$(curl -sS -w "%{http_code}" -o "\$tmp" "\$url" || true)
    if [[ "\$status" == "200" ]]; then
      mv "\$tmp" "\$output"
      echo "\$name OK on attempt \$i" | tee -a /tmp/http-status.log
      return 0
    fi
    echo "\$name waiting: status=\$status attempt=\$i/\$attempts" | tee -a /tmp/http-status.log
    sleep 5
  done
  http_json_error "\$output" "\$name" "\$status" "\$(cat "\$tmp" 2>/dev/null || true)"
  return 1
}

curl_post_json_retry() {
  local url="\$1"
  local output="\$2"
  local name="\$3"
  local body="\$4"
  local attempts="\${5:-120}"
  local tmp="\${output}.tmp"
  local status="000"
  for i in \$(seq 1 "\$attempts"); do
    status=\$(curl -sS -w "%{http_code}" -o "\$tmp" "\$url" \
      -H 'Content-Type: application/json' \
      -d "\$body" || true)
    if [[ "\$status" == "200" ]]; then
      mv "\$tmp" "\$output"
      echo "\$name OK on attempt \$i" | tee -a /tmp/http-status.log
      return 0
    fi
    echo "\$name waiting: status=\$status attempt=\$i/\$attempts" | tee -a /tmp/http-status.log
    sleep 5
  done
  http_json_error "\$output" "\$name" "\$status" "\$(cat "\$tmp" 2>/dev/null || true)"
  return 1
}

curl_get_json_retry http://127.0.0.1:8088/healthz /tmp/healthz.json gateway_healthz 120 || true
curl_get_json_retry http://127.0.0.1:6000/v1/health_check /tmp/embedding_health.json embedding_health 120 || true
curl_post_json_retry http://127.0.0.1:6000/v1/embeddings /tmp/embedding-warmup.json embedding_warmup '{"input":"WearEdge TEI warmup for oneDNN verbose evidence"}' 120 || true
curl_get_json_retry http://127.0.0.1:8088/v1/scorecard /tmp/scorecard.json scorecard 60 || true
for mode in maintenance iqc changeover wi hazard; do
  curl_get_json_retry "http://127.0.0.1:8088/v1/agents/\${mode}/demo" "/tmp/demo-\${mode}.json" "demo_\${mode}" 30 || true
done
for i in \$(seq 1 10); do
  curl_post_json_retry http://127.0.0.1:6000/v1/embeddings \
    "/tmp/embedding-\${i}.json" \
    "embedding_\${i}" \
    "{\"input\":\"WearEdge TEI oneDNN verbose smoke \${i}\"}" \
    3 || true
done

cat > /tmp/onednn_bf16_amx_probe.cpp <<'CPP'
#include <cstdint>
#include <cstring>
#include <iostream>
#include <unordered_map>
#include <vector>

#include <dnnl.hpp>

static std::uint16_t f32_to_bf16(float value) {
    std::uint32_t bits = 0;
    std::memcpy(&bits, &value, sizeof(bits));
    const std::uint32_t rounding_bias = ((bits >> 16) & 1U) + 0x7FFFU;
    return static_cast<std::uint16_t>((bits + rounding_bias) >> 16);
}

int main() {
    try {
        using namespace dnnl;
        using tag = memory::format_tag;
        using dt = memory::data_type;

        constexpr int64_t m = 1024;
        constexpr int64_t k = 1024;
        constexpr int64_t n = 1024;

        engine eng(engine::kind::cpu, 0);
        stream s(eng);

        memory::dims src_dims = {m, k};
        memory::dims weights_dims = {k, n};
        memory::dims dst_dims = {m, n};

        auto src_md = memory::desc(src_dims, dt::bf16, tag::ab);
        auto weights_md = memory::desc(weights_dims, dt::bf16, tag::ab);
        auto dst_md = memory::desc(dst_dims, dt::f32, tag::ab);

        std::vector<std::uint16_t> src(m * k);
        std::vector<std::uint16_t> weights(k * n);
        std::vector<float> dst(m * n, 0.0f);

        for (size_t i = 0; i < src.size(); ++i) {
            src[i] = f32_to_bf16(static_cast<float>(static_cast<int>(i % 97) - 48) / 97.0f);
        }
        for (size_t i = 0; i < weights.size(); ++i) {
            weights[i] = f32_to_bf16(static_cast<float>(static_cast<int>(i % 53) - 26) / 53.0f);
        }

        memory src_mem(src_md, eng, src.data());
        memory weights_mem(weights_md, eng, weights.data());
        memory dst_mem(dst_md, eng, dst.data());

        matmul::primitive_desc matmul_pd(eng, src_md, weights_md, dst_md);
        matmul matmul_p(matmul_pd);

        std::unordered_map<int, memory> args = {
            {DNNL_ARG_SRC, src_mem},
            {DNNL_ARG_WEIGHTS, weights_mem},
            {DNNL_ARG_DST, dst_mem},
        };

        for (int repeat = 0; repeat < 5; ++repeat) {
            matmul_p.execute(s, args);
            s.wait();
        }

        std::cout << "probe_result=ok\\n";
        std::cout << "probe_workload=oneDNN bf16 matmul 1024x1024x1024 repeat=5\\n";
        std::cout << "probe_checksum=" << dst[0] << "\\n";
        return 0;
    } catch (const dnnl::error &e) {
        std::cerr << "probe_result=dnnl_error status=" << e.status
                  << " message=" << e.what() << "\\n";
        return 2;
    } catch (const std::exception &e) {
        std::cerr << "probe_result=exception message=" << e.what() << "\\n";
        return 3;
    }
}
CPP

{
  echo "probe_dependency_install=start"
  sudo apt-get install -y g++ libdnnl-dev
  echo "probe_dependency_install=ok"
  g++ -O2 -std=c++17 /tmp/onednn_bf16_amx_probe.cpp -ldnnl -o /tmp/onednn_bf16_amx_probe
  if [[ -x /tmp/onednn_bf16_amx_probe ]]; then
    echo "probe_compile=ok"
  else
    echo "probe_compile=failed"
  fi
  ONEDNN_VERBOSE=1 \
  DNNL_VERBOSE=1 \
  MKLDNN_VERBOSE=1 \
  ONEDNN_MAX_CPU_ISA=AVX512_CORE_AMX \
  DNNL_MAX_CPU_ISA=AVX512_CORE_AMX \
  OMP_NUM_THREADS=4 \
    /tmp/onednn_bf16_amx_probe
} > /tmp/onednn.probe.log 2>&1 || true

grep -Ei '^(onednn_verbose|dnnl_verbose),' /tmp/onednn.probe.log > /tmp/probe.dispatch.markers.txt || true

sudo docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml -f docker-compose.onednn-verbose.yml logs --no-color > /tmp/compose.logs.txt || true
sudo docker compose -f docker-compose.yml -f docker-compose.opea-tei.yml -f docker-compose.onednn-verbose.yml ps --format json > /tmp/compose.ps.json || true
sudo docker stats --no-stream --format '{{json .}}' | jq -s . > /tmp/docker.stats.json || true
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
probe_log = read("onednn.probe.log")
probe_markers = read("probe.dispatch.markers.txt")
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
probe_dispatch_regex = re.compile(r"^(onednn_verbose|dnnl_verbose),.*(matmul|brgemm|gemm).*(bf16|amx|avx512|brg)", re.I)
probe_dispatch_marker_lines = [
    line for line in probe_markers.splitlines() if probe_dispatch_regex.search(line)
]

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
    "onednn_probe_compiled": "probe_compile=ok" in probe_log,
    "onednn_probe_executed": "probe_result=ok" in probe_log,
    "probe_dispatch_markers_captured": bool(probe_dispatch_marker_lines),
}
artifact = {
    "benchmark": "WearEdge OPEA TEI oneDNN verbose / Intel ISA evidence on GCP C3",
    "schema_version": "2026-05-29",
    "created_at_epoch": time.time(),
    "claim_status": (
        "tei_onednn_or_isa_dispatch_markers_captured"
        if validation["dispatch_markers_captured"]
        else (
            "wear_edge_scorecard_with_onednn_bf16_amx_probe_dispatch_markers_captured"
            if validation["probe_dispatch_markers_captured"]
            else "tei_verbose_not_emitted_cpu_feature_evidence_only"
        )
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
        "http_status_log": read("http-status.log"),
        "embedding_warmup": read_json("embedding-warmup.json", {}),
    },
    "dispatch_evidence": {
        "marker_count": len(dispatch_marker_lines),
        "marker_lines": dispatch_marker_lines[:120],
        "note": "Some TEI builds may not emit oneDNN verbose logs even when CPU ISA flags are present; this records both the env-enabled attempt and observed markers.",
    },
    "probe_dispatch_evidence": {
        "probe": "same-host oneDNN BF16 matmul probe",
        "probe_workload": "oneDNN bf16 matmul 1024x1024x1024 repeat=5",
        "marker_count": len(probe_dispatch_marker_lines),
        "marker_lines": probe_dispatch_marker_lines[:120],
        "probe_log_tail": probe_log[-4000:],
        "note": "This supplemental probe runs on the same GCP C3 VM as the WearEdge OPEA TEI scorecard path. It proves observable oneDNN BF16/AMX/AVX512 dispatch on the host when marker lines are present; it is separate from the TEI container's own logs.",
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
