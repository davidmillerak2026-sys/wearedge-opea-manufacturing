from __future__ import annotations

import hashlib
import json
import math
import os
import re
import urllib.request


TOKEN_RE = re.compile(r"[a-zA-Z0-9_\-]+")
DEFAULT_DIMENSIONS = 64


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def embedding_backend() -> str:
    return os.getenv("WEAREDGE_EMBEDDING_BACKEND", "hashing").strip().lower()


def embedding_profile_name() -> str:
    configured = os.getenv("WEAREDGE_EMBEDDING_PROFILE", "").strip()
    if configured:
        return configured
    if embedding_backend() in {"opea", "remote", "microservice"}:
        return "opea-compatible-embedding"
    return "hashing"


def embed_text(text: str, dimensions: int = DEFAULT_DIMENSIONS) -> list[float]:
    """Embed text through the configured profile.

    The default profile stays dependency-free. The `opea` profile calls a
    remote `/v1/embeddings` microservice using the OpenAI-compatible payload
    shape documented by OPEA embedding services.
    """

    if embedding_backend() in {"opea", "remote", "microservice"}:
        return embed_text_remote(text, dimensions)
    return hashing_embed_text(text, dimensions)


def hashing_embed_text(text: str, dimensions: int = DEFAULT_DIMENSIONS) -> list[float]:
    """Deterministic hashing embedding.

    This is deliberately small and dependency-free. It gives the Qdrant profile
    a real vector path while keeping the demo runnable without model downloads.
    Production can swap this for an OPEA embedding microservice.
    """

    vector = [0.0] * dimensions
    for token in tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[idx] += sign

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def embed_text_remote(text: str, dimensions: int = DEFAULT_DIMENSIONS) -> list[float]:
    url = os.getenv("WEAREDGE_EMBEDDING_URL", "http://127.0.0.1:6000/v1/embeddings")
    timeout = float(os.getenv("WEAREDGE_EMBEDDING_TIMEOUT", "5"))
    payload = {"input": text}
    model = os.getenv("WEAREDGE_EMBEDDING_MODEL", "wear-edge-hashing-embedding").strip()
    if model:
        payload["model"] = model
    if os.getenv("WEAREDGE_EMBEDDING_SEND_DIMENSIONS", "true").lower() not in {"0", "false", "no"}:
        payload["dimensions"] = dimensions
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    embedding = _extract_embedding(body)
    return _coerce_dimensions(embedding, dimensions, strict=_strict_dimensions())


def _extract_embedding(body: dict) -> list[float]:
    if "data" in body and body["data"]:
        return [float(value) for value in body["data"][0]["embedding"]]
    if "embedding" in body:
        return [float(value) for value in body["embedding"]]
    raise ValueError("Embedding response did not include data[0].embedding")


def _strict_dimensions() -> bool:
    return os.getenv("WEAREDGE_EMBEDDING_STRICT_DIMENSIONS", "false").lower() in {"1", "true", "yes"}


def _coerce_dimensions(vector: list[float], dimensions: int, strict: bool = False) -> list[float]:
    if len(vector) == dimensions:
        return vector
    if strict:
        raise ValueError(
            f"Embedding response dimension mismatch: expected {dimensions}, got {len(vector)}"
        )
    if len(vector) > dimensions:
        return vector[:dimensions]
    return vector + [0.0] * (dimensions - len(vector))


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
