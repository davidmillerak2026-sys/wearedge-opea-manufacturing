from __future__ import annotations

from .dataprep import build_chunks, load_maintenance_kb
from .vector_store import build_vector_store


def retrieve_context(query: str, limit: int = 3) -> dict:
    kb = load_maintenance_kb()
    chunks = build_chunks(kb)
    vector_store = build_vector_store()
    vector_store.index(chunks)
    hits = vector_store.search(query, limit=limit)
    return {
        "asset_id": kb["asset_id"],
        "revision": kb["revision"],
        "thresholds": kb["thresholds"],
        "vector_store": vector_store.name,
        "hits": hits,
    }

