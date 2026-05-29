# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .agents import AgentRoute, get_route


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KB = ROOT / "data" / "maintenance_kb" / "pkg_l3_gbx_03.json"


@dataclass(frozen=True)
class KnowledgeChunk:
    id: str
    title: str
    content: str
    asset_id: str
    revision: str
    mode: str = "maintenance"


def load_maintenance_kb(path: Path = DEFAULT_KB) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_route_kb(mode: str | None) -> dict:
    route = get_route(mode)
    return load_kb_for_route(route)


def load_kb_for_route(route: AgentRoute) -> dict:
    return json.loads(route.kb_path.read_text(encoding="utf-8"))


def build_chunks(kb: dict, mode: str | None = None) -> list[KnowledgeChunk]:
    chunk_mode = mode or kb.get("mode") or "maintenance"
    entity_id = kb.get("asset_id") or kb.get("entity_id") or "unknown"
    chunks: list[KnowledgeChunk] = []
    for section in kb["sections"]:
        chunks.append(
            KnowledgeChunk(
                id=section["id"],
                title=section["title"],
                content=section["content"],
                asset_id=entity_id,
                revision=kb["revision"],
                mode=chunk_mode,
            )
        )
    return chunks
