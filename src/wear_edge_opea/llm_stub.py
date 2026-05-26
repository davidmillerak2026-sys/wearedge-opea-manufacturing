from __future__ import annotations

from .agents import AgentRoute


def explain(route: AgentRoute, entity_id: str, observation: str, rag_hits: list[dict], evaluation: dict) -> str:
    source_ids = ", ".join(
        hit["payload"].get("id", "unknown")
        for hit in rag_hits
        if hit.get("payload")
    ) or "no-source"
    return (
        f"{route.name} for {entity_id} has {evaluation['breach_count']} accepted evidence flags. "
        f"The strongest retrieved {route.mode} sources are {source_ids}. "
        f"Operator observation: {observation}. "
        "The system should create a bounded action card, preserve source IDs, and keep restricted decisions human-confirmed."
    )
