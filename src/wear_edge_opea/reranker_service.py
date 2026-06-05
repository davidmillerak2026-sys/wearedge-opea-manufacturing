# SPDX-License-Identifier: MIT

from __future__ import annotations

import os
from typing import Any

try:
    from fastapi import FastAPI
    import uvicorn
except ImportError as exc:  # pragma: no cover - import guard for container setup
    raise SystemExit("Install server dependencies with `pip install -r requirements.txt`.") from exc

from .reranker import rerank_documents


DEFAULT_HOST = os.getenv("WEAREDGE_RERANKER_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("WEAREDGE_RERANKER_PORT", "7000"))

app = FastAPI(
    title="WearEdge OPEA-Compatible Reranker Microservice",
    version="0.1.0",
)


@app.get("/healthz")
def healthz() -> dict:
    return {
        "ok": True,
        "service": "wear-edge-opea-compatible-reranker",
        "opea_component": "Reranking Microservice",
        "api": "/v1/rerank",
        "backend": "lexical",
        "compatibility": "OPEA-style reranking microservice boundary",
    }


@app.post("/v1/rerank")
def rerank(request: dict[str, Any]) -> dict:
    query = str(request.get("query", ""))
    documents = request.get("documents", [])
    if not isinstance(documents, list):
        documents = []
    top_n = request.get("top_n")
    results = rerank_documents(query, documents, top_n=int(top_n) if top_n else None)
    return {
        "object": "list",
        "model": os.getenv("WEAREDGE_RERANKER_MODEL", "wear-edge-lexical-reranker"),
        "results": results,
        "usage": {
            "documents": len(documents),
            "returned": len(results),
        },
        "opea_component": "Reranking Microservice",
    }


def main() -> None:
    uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT)


if __name__ == "__main__":
    main()
