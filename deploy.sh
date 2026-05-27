#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  echo "Starting WearEdge OPEA Manufacturing with Docker Compose..."
  docker compose up -d --build
  echo "Demo:    http://127.0.0.1:8088/demo"
  echo "Gateway: http://127.0.0.1:8088/healthz"
  echo "Agents:  http://127.0.0.1:8088/v1/agents"
  echo "Suite:   http://127.0.0.1:8088/v1/manufacturing/suite"
  echo "Score:   http://127.0.0.1:8088/v1/scorecard"
else
  echo "Docker Compose not found. Running dependency-free local demo instead..."
  PYTHONPATH="$ROOT_DIR/src" python -m wear_edge_opea.run_demo
fi
