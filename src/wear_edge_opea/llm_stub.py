from __future__ import annotations


def explain(asset_id: str, observation: str, rag_hits: list[dict], evaluation: dict) -> str:
    source_ids = ", ".join(
        hit["payload"].get("id", "unknown")
        for hit in rag_hits
        if hit.get("payload")
    )
    return (
        f"Asset {asset_id} has {evaluation['breach_count']} accepted signal breaches. "
        f"The strongest retrieved maintenance sources are {source_ids}. "
        f"Operator observation: {observation}. "
        "The system should create a bounded action card and require technician confirmation."
    )

