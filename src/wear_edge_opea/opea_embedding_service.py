# SPDX-License-Identifier: MIT

from __future__ import annotations

import os
from typing import Any

try:
    from fastapi import FastAPI
    import uvicorn
except ImportError as exc:  # pragma: no cover - import guard for container setup
    raise SystemExit("Install server dependencies with `pip install -r requirements.txt`.") from exc

from .embedding import DEFAULT_DIMENSIONS, hashing_embed_text

try:  # pragma: no cover - optional OPEA package is not required for the fast local path
    from comps import EmbedDoc, ServiceType, TextDoc, register_microservice
except ImportError:  # pragma: no cover
    EmbedDoc = None
    ServiceType = None
    TextDoc = None
    register_microservice = None


MODEL_NAME = os.getenv("WEAREDGE_EMBEDDING_MODEL", "wear-edge-hashing-embedding")
DEFAULT_HOST = os.getenv("WEAREDGE_EMBEDDING_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("WEAREDGE_EMBEDDING_PORT", "6000"))

app = FastAPI(
    title="WearEdge OPEA-Compatible Embedding Microservice",
    version="0.1.0",
)


@app.get("/healthz")
def healthz() -> dict:
    return {
        "ok": True,
        "service": "wear-edge-opea-compatible-embedding",
        "opea_component": "Embedding Microservice",
        "api": "/v1/embeddings",
        "model": MODEL_NAME,
        "dimensions": int(os.getenv("WEAREDGE_EMBEDDING_DIMENSIONS", str(DEFAULT_DIMENSIONS))),
        "compatibility": "OpenAI-compatible embeddings API used by OPEA embedding services",
        "genaicomps_register_microservice_available": register_microservice is not None,
    }


@app.post("/v1/embeddings")
def embeddings(request: dict[str, Any]) -> dict:
    dimensions = int(request.get("dimensions") or os.getenv("WEAREDGE_EMBEDDING_DIMENSIONS", str(DEFAULT_DIMENSIONS)))
    inputs = _extract_inputs(request)
    data = [
        {
            "object": "embedding",
            "index": index,
            "embedding": hashing_embed_text(text, dimensions),
        }
        for index, text in enumerate(inputs)
    ]
    return {
        "object": "list",
        "model": request.get("model") or MODEL_NAME,
        "data": data,
        "usage": {
            "prompt_tokens": sum(len(text.split()) for text in inputs),
            "total_tokens": sum(len(text.split()) for text in inputs),
        },
        "opea_component": "Embedding Microservice",
        "compatibility": "OPEA/OpenAI-compatible /v1/embeddings",
    }


def _extract_inputs(request: dict[str, Any]) -> list[str]:
    value = request.get("input", request.get("text", request.get("texts", "")))
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


if register_microservice is not None:  # pragma: no cover - exercised only with opea-comps installed

    @register_microservice(
        name="opea_service@wearedge_embedding",
        service_type=ServiceType.EMBEDDING,
        endpoint="/v1/embeddings",
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        input_datatype=TextDoc,
        output_datatype=EmbedDoc,
    )
    def opea_registered_embedding(input: TextDoc) -> EmbedDoc:
        vector = hashing_embed_text(input.text, int(os.getenv("WEAREDGE_EMBEDDING_DIMENSIONS", str(DEFAULT_DIMENSIONS))))
        return EmbedDoc(text=input.text, embedding=vector)


def main() -> None:
    uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT)


if __name__ == "__main__":
    main()
