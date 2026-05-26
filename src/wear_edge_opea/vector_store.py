from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict
from typing import Protocol

from .dataprep import KnowledgeChunk
from .embedding import cosine_similarity, embed_text


class VectorStore(Protocol):
    name: str

    def index(self, chunks: list[KnowledgeChunk]) -> None:
        ...

    def search(self, query: str, limit: int = 3) -> list[dict]:
        ...


class InMemoryVectorStore:
    name = "in-memory-hashing-vector-store"

    def __init__(self) -> None:
        self._rows: list[tuple[list[float], KnowledgeChunk]] = []

    def index(self, chunks: list[KnowledgeChunk]) -> None:
        self._rows = [(embed_text(f"{chunk.title} {chunk.content}"), chunk) for chunk in chunks]

    def search(self, query: str, limit: int = 3) -> list[dict]:
        query_vector = embed_text(query)
        scored = [
            (cosine_similarity(query_vector, vector), chunk)
            for vector, chunk in self._rows
        ]
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "score": round(score, 4),
                "payload": asdict(chunk),
            }
            for score, chunk in scored[:limit]
        ]


class QdrantVectorStore:
    name = "qdrant-hashing-vector-store"

    def __init__(
        self,
        url: str | None = None,
        collection: str | None = None,
        dimensions: int = 64,
        timeout: float = 3.0,
    ) -> None:
        self.url = (url or os.getenv("WEAREDGE_QDRANT_URL") or "http://127.0.0.1:6333").rstrip("/")
        self.collection = collection or os.getenv("WEAREDGE_COLLECTION") or "wearedge_manufacturing_kb"
        self.dimensions = dimensions
        self.timeout = timeout

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            f"{self.url}{path}",
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            text = response.read().decode("utf-8")
            return json.loads(text) if text else {}

    def index(self, chunks: list[KnowledgeChunk]) -> None:
        try:
            self._request(
                "PUT",
                f"/collections/{self.collection}",
                {"vectors": {"size": self.dimensions, "distance": "Cosine"}},
            )
        except urllib.error.HTTPError as exc:
            if exc.code != 409:
                raise
        points = []
        for idx, chunk in enumerate(chunks, start=1):
            points.append(
                {
                    "id": idx,
                    "vector": embed_text(f"{chunk.title} {chunk.content}", self.dimensions),
                    "payload": asdict(chunk),
                }
            )
        self._request(
            "PUT",
            f"/collections/{self.collection}/points?wait=true",
            {"points": points},
        )

    def search(self, query: str, limit: int = 3) -> list[dict]:
        result = self._request(
            "POST",
            f"/collections/{self.collection}/points/search",
            {"vector": embed_text(query, self.dimensions), "limit": limit, "with_payload": True},
        )
        return [
            {
                "score": round(item.get("score", 0.0), 4),
                "payload": item.get("payload", {}),
            }
            for item in result.get("result", [])
        ]


def build_vector_store(collection: str | None = None) -> VectorStore:
    backend = os.getenv("WEAREDGE_VECTOR_BACKEND", "memory").lower()
    if backend == "qdrant":
        qdrant = QdrantVectorStore(collection=collection)
        try:
            qdrant._request("GET", "/")
            return qdrant
        except (OSError, urllib.error.URLError, TimeoutError):
            return InMemoryVectorStore()
    return InMemoryVectorStore()
