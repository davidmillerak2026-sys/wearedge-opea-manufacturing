from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KB = ROOT / "data" / "maintenance_kb" / "pkg_l3_gbx_03.json"


@dataclass(frozen=True)
class KnowledgeChunk:
    id: str
    title: str
    content: str
    asset_id: str
    revision: str


def load_maintenance_kb(path: Path = DEFAULT_KB) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_chunks(kb: dict) -> list[KnowledgeChunk]:
    chunks: list[KnowledgeChunk] = []
    for section in kb["sections"]:
        chunks.append(
            KnowledgeChunk(
                id=section["id"],
                title=section["title"],
                content=section["content"],
                asset_id=kb["asset_id"],
                revision=kb["revision"],
            )
        )
    return chunks

