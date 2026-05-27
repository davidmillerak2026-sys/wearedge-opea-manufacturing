from __future__ import annotations

import os

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    import uvicorn
except ImportError as exc:  # pragma: no cover - import guard for local no-deps demo
    raise SystemExit("Install server dependencies with `pip install -r requirements.txt`.") from exc

from .agents import list_agents, load_sample_request
from .demo_console import build_demo_console_html
from .megaservice import run_agent_demo, run_all_agent_demos, run_pipeline
from .scorecard import build_scorecard


app = FastAPI(title="WearEdge OPEA Manufacturing Gateway", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def root_console() -> str:
    return build_demo_console_html()


@app.get("/demo", response_class=HTMLResponse)
def demo_console() -> str:
    return build_demo_console_html()


@app.get("/healthz")
def healthz() -> dict:
    return {
        "ok": True,
        "service": "wear-edge-opea-manufacturing-gateway",
        "vector_backend": os.getenv("WEAREDGE_VECTOR_BACKEND", "memory"),
        "qdrant_url": os.getenv("WEAREDGE_QDRANT_URL", "not-set"),
        "agents": ["maintenance", "iqc", "changeover", "wi", "hazard"],
    }


@app.get("/v1/manufacturing/demo")
def manufacturing_demo() -> dict:
    return run_agent_demo("maintenance")


@app.post("/v1/manufacturing/infer")
def manufacturing_infer(request: dict) -> dict:
    return run_pipeline(request, mode=request.get("mode") or "maintenance")


@app.get("/v1/manufacturing/suite")
def manufacturing_suite() -> dict:
    return run_all_agent_demos()


@app.get("/v1/agents")
def agents() -> dict:
    catalog = list_agents()
    return {
        "ok": True,
        "modes": [agent["mode"] for agent in catalog],
        "agents": catalog,
    }


@app.get("/v1/agents/{mode}/demo")
def agent_demo(mode: str) -> dict:
    return run_agent_demo(mode)


@app.post("/v1/agents/{mode}/infer")
def agent_infer(mode: str, request: dict) -> dict:
    merged = {**load_sample_request(mode), **request, "mode": mode}
    return run_pipeline(merged, mode=mode)


@app.get("/v1/scorecard")
def scorecard() -> dict:
    return build_scorecard()


def main() -> None:
    host = os.getenv("WEAREDGE_HOST", "127.0.0.1")
    port = int(os.getenv("WEAREDGE_PORT", "8088"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
