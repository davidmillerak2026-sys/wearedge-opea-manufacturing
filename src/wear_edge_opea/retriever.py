# SPDX-License-Identifier: MIT

from __future__ import annotations

import os

from .agents import get_route
from .dataprep import build_chunks, load_kb_for_route
from .reranker import rerank_hits
from .vector_store import build_vector_store


def retrieve_context(mode: str, query: str, limit: int = 3) -> dict:
    route = get_route(mode)
    kb = load_kb_for_route(route)
    chunks = build_chunks(kb, route.mode)
    base_collection = os.getenv("WEAREDGE_COLLECTION") or "wearedge_manufacturing_kb"
    collection = f"{base_collection}_{route.mode}"
    vector_store = build_vector_store(collection=collection)
    vector_store.index(chunks)
    vector_hits = vector_store.search(query, limit=limit)
    hits, reranker = rerank_hits(query, vector_hits, limit=limit)
    return {
        "mode": route.mode,
        "entity_id": kb.get("asset_id") or kb.get("entity_id"),
        "revision": kb["revision"],
        "thresholds": kb.get("thresholds", {}),
        "vector_store": vector_store.name,
        "reranker": reranker,
        "hits": hits,
    }
