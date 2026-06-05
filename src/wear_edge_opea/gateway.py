# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import os
from collections.abc import Iterator

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse, StreamingResponse
    import uvicorn
except ImportError as exc:  # pragma: no cover - import guard for local no-deps run
    raise SystemExit("Install server dependencies with `pip install -r requirements.txt`.") from exc

from .agents import list_agents, load_sample_request
from .demo_console import build_demo_console_html
from .llm_adapter import configured_backend, configured_model, configured_url
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
        "embedding_backend": os.getenv("WEAREDGE_EMBEDDING_BACKEND", "hashing"),
        "embedding_url": os.getenv("WEAREDGE_EMBEDDING_URL", "in-process"),
        "llm_backend": configured_backend(),
        "llm_model": configured_model(),
        "llm_url": configured_url() or "in-process",
        "agents": ["maintenance", "iqc", "changeover", "wi", "hazard"],
    }


@app.get("/v1/manufacturing/demo")
def manufacturing_demo() -> dict:
    return run_agent_demo("maintenance")


@app.post("/v1/manufacturing/infer")
def manufacturing_infer(request: dict) -> dict:
    return run_pipeline(request, mode=request.get("mode") or "maintenance")


@app.post("/v1/chatqna", response_model=None)
def chatqna_compatible(request: dict) -> dict | StreamingResponse:
    response = build_chatqna_response(request)
    if _wants_stream(request):
        return StreamingResponse(_chatqna_sse_events(response), media_type="text/event-stream")
    return response


def build_chatqna_response(request: dict) -> dict:
    mode = request.get("mode") or request.get("analysis_mode") or "maintenance"
    observation = _extract_chatqna_query(request)
    merged = {**load_sample_request(mode), **request, "mode": mode}
    if observation and not request.get("operator_observation"):
        merged["operator_observation"] = observation
    result = run_pipeline(merged, mode=mode)
    return {
        "ok": result["ok"],
        "model": result["llm_runtime"]["model"],
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result["llm_explanation"],
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": len(observation.split()) if observation else 0,
            "completion_tokens": len(result["llm_explanation"].split()),
            "total_tokens": (len(observation.split()) if observation else 0) + len(result["llm_explanation"].split()),
        },
        "wear_edge_result": result,
        "compatibility": "OPEA GenAIEval chatqna e2e endpoint alias",
    }


def _wants_stream(request: dict) -> bool:
    value = request.get("stream", True)
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "no", "off"}
    return bool(value)


def _chatqna_sse_events(response: dict) -> Iterator[str]:
    text = response["choices"][0]["message"]["content"]
    yield "data: " + json.dumps({"type": "LLMResult", "text": text}, separators=(",", ":")) + "\n\n"
    yield "data: [DONE]\n\n"


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


def _extract_chatqna_query(request: dict) -> str:
    for key in ("query", "question", "prompt", "text", "input"):
        value = request.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    messages = request.get("messages")
    if isinstance(messages, str) and messages.strip():
        return messages.strip()
    if isinstance(messages, list):
        for message in reversed(messages):
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"].strip()
    return ""


def main() -> None:
    host = os.getenv("WEAREDGE_HOST", "127.0.0.1")
    port = int(os.getenv("WEAREDGE_PORT", "8088"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
