from __future__ import annotations

import json
import os
from pathlib import Path

try:
    from fastapi import FastAPI
    import uvicorn
except ImportError as exc:  # pragma: no cover - import guard for local no-deps demo
    raise SystemExit("Install server dependencies with `pip install -r requirements.txt`.") from exc

from .megaservice import run_pipeline


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_REQUEST = ROOT / "data" / "sample_request.json"

app = FastAPI(title="WearEdge OPEA Manufacturing Gateway", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict:
    return {
        "ok": True,
        "service": "wear-edge-opea-manufacturing-gateway",
        "vector_backend": os.getenv("WEAREDGE_VECTOR_BACKEND", "memory"),
        "qdrant_url": os.getenv("WEAREDGE_QDRANT_URL", "not-set"),
    }


@app.get("/v1/manufacturing/demo")
def manufacturing_demo() -> dict:
    request = json.loads(SAMPLE_REQUEST.read_text(encoding="utf-8"))
    return run_pipeline(request)


@app.post("/v1/manufacturing/infer")
def manufacturing_infer(request: dict) -> dict:
    return run_pipeline(request)


def main() -> None:
    host = os.getenv("WEAREDGE_HOST", "127.0.0.1")
    port = int(os.getenv("WEAREDGE_PORT", "8088"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()

