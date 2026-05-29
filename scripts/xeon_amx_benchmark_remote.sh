#!/usr/bin/env bash
# SPDX-License-Identifier: MIT

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing.git}"
WORKDIR="${WORKDIR:-$HOME/wearedge-opea-manufacturing}"
ITERATIONS="${ITERATIONS:-1000}"
OUTPUT="${OUTPUT:-evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json}"

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git python3 python3-venv python3-pip
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y git python3 python3-pip
fi

if [ -d "$WORKDIR/.git" ]; then
  git -C "$WORKDIR" pull --ff-only
else
  git clone "$REPO_URL" "$WORKDIR"
fi

cd "$WORKDIR"

python3 scripts/intel_cpu_benchmark.py \
  --iterations "$ITERATIONS" \
  --output "$OUTPUT"

python3 - <<'PY'
import json
from pathlib import Path

path = Path("evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json")
report = json.loads(path.read_text(encoding="utf-8"))
features = report["cpu"]["feature_detection"]
scorecard_ok = report["pipeline"]["scorecard"]["ok"]
has_amx = any(features.get(name) for name in ("amx_tile", "amx_int8", "amx_bf16"))

print("benchmark_file=", path)
print("processor=", report["cpu"]["processor"])
print("avx512f=", features.get("avx512f"))
print("amx_detected=", has_amx)
print("scorecard_ok=", scorecard_ok)
print("calls_per_second=", report["pipeline"]["calls_per_second"])

if not features.get("avx512f"):
    raise SystemExit("AVX-512 flag was not detected; use a Xeon host that exposes avx512f.")
if not has_amx:
    raise SystemExit("AMX flag was not detected; use a Xeon host that exposes amx_tile/amx_int8/amx_bf16.")
if not scorecard_ok:
    raise SystemExit("WearEdge scorecard failed.")
PY

echo "=== benchmark JSON ==="
cat "$OUTPUT"
