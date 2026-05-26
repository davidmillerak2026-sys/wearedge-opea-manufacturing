from __future__ import annotations

import hashlib
import math
import re


TOKEN_RE = re.compile(r"[a-zA-Z0-9_\-]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def embed_text(text: str, dimensions: int = 64) -> list[float]:
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


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))

