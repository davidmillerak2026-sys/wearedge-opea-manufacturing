# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any


TOKEN_RE = re.compile(r"[a-zA-Z0-9_\-]+")
RERANKER_BACKENDS = {"lexical", "remote", "microservice", "opea", "opea-compatible"}


def reranker_backend() -> str:
    return os.getenv("WEAREDGE_RERANKER_BACKEND", "none").strip().lower() or "none"


def reranker_url() -> str:
    return os.getenv("WEAREDGE_RERANKER_URL", "http://127.0.0.1:7000/v1/rerank")


def rerank_hits(query: str, hits: list[dict], limit: int | None = None) -> tuple[list[dict], dict]:
    backend = reranker_backend()
    if backend in {"none", "disabled", "off"}:
        return hits[:limit] if limit else hits, _metadata("disabled")
    if backend == "lexical":
        reranked = lexical_rerank(query, hits, limit=limit)
        return reranked, _metadata("lexical", applied=True)
    if backend in RERANKER_BACKENDS:
        return _remote_rerank(query, hits, limit=limit)
    if _strict():
        raise ValueError(f"Unsupported WEAREDGE_RERANKER_BACKEND={backend}")
    return hits[:limit] if limit else hits, _metadata("fallback", error=f"unsupported backend: {backend}")


def lexical_rerank(query: str, hits: list[dict], limit: int | None = None) -> list[dict]:
    query_tokens = set(_tokens(query))
    scored = []
    for index, hit in enumerate(hits):
        payload = hit.get("payload", {})
        text = f"{payload.get('title', '')} {payload.get('content', '')}"
        tokens = set(_tokens(text))
        overlap = len(query_tokens & tokens)
        coverage = overlap / max(1, len(query_tokens))
        source_score = float(hit.get("score", 0.0))
        rerank_score = round((coverage * 2.0) + source_score, 4)
        enriched = {**hit, "vector_score": source_score, "rerank_score": rerank_score}
        scored.append((rerank_score, -index, enriched))
    scored.sort(reverse=True)
    output = [item[2] for item in scored]
    return output[:limit] if limit else output


def rerank_documents(query: str, documents: list[dict[str, Any]], top_n: int | None = None) -> list[dict]:
    hits = [
        {
            "score": float(document.get("score", 0.0)),
            "payload": document.get("metadata", {}),
            "document": document,
        }
        for document in documents
    ]
    reranked = lexical_rerank(query, hits, limit=top_n)
    results = []
    for rank, hit in enumerate(reranked, start=1):
        document = hit.get("document", {})
        results.append(
            {
                "index": int(document.get("index", rank - 1)),
                "id": document.get("id") or hit.get("payload", {}).get("id"),
                "text": document.get("text", ""),
                "metadata": hit.get("payload", {}),
                "score": hit.get("vector_score", 0.0),
                "rerank_score": hit["rerank_score"],
                "rank": rank,
            }
        )
    return results


def _remote_rerank(query: str, hits: list[dict], limit: int | None = None) -> tuple[list[dict], dict]:
    documents = []
    for index, hit in enumerate(hits):
        payload = hit.get("payload", {})
        documents.append(
            {
                "index": index,
                "id": payload.get("id", str(index)),
                "text": f"{payload.get('title', '')} {payload.get('content', '')}",
                "metadata": payload,
                "score": hit.get("score", 0.0),
            }
        )
    payload = {"query": query, "documents": documents, "top_n": limit or len(documents)}
    try:
        body = _post_json(reranker_url(), payload, timeout=float(os.getenv("WEAREDGE_RERANKER_TIMEOUT", "5")))
        result_hits = _extract_remote_hits(body, hits)
        return result_hits[:limit] if limit else result_hits, _metadata("remote", applied=True, url=reranker_url())
    except (OSError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        if _strict():
            raise
        fallback = lexical_rerank(query, hits, limit=limit)
        return fallback, _metadata("lexical_fallback", applied=True, error=str(exc), url=reranker_url())


def _extract_remote_hits(body: dict, original_hits: list[dict]) -> list[dict]:
    raw_results = body.get("results") or body.get("data") or []
    if not isinstance(raw_results, list):
        raise ValueError("Reranker response did not include a results list")
    output = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        index = int(item.get("index", len(output)))
        base = original_hits[index] if 0 <= index < len(original_hits) else {"payload": item.get("metadata", {})}
        output.append(
            {
                **base,
                "vector_score": float(item.get("score", base.get("score", 0.0))),
                "rerank_score": float(item.get("rerank_score", item.get("relevance_score", item.get("score", 0.0)))),
            }
        )
    if not output:
        raise ValueError("Reranker response produced no usable hits")
    output.sort(key=lambda hit: hit.get("rerank_score", 0.0), reverse=True)
    return output


def _post_json(url: str, payload: dict, timeout: float) -> dict:
    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def _strict() -> bool:
    return os.getenv("WEAREDGE_RERANKER_STRICT", "false").lower() in {"1", "true", "yes"}


def _metadata(status: str, *, applied: bool = False, error: str | None = None, url: str | None = None) -> dict:
    return {
        "backend": reranker_backend(),
        "status": status,
        "applied": applied,
        "url": url or ("in-process" if applied else "not-configured"),
        "error": error,
    }
