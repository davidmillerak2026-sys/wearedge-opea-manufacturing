from __future__ import annotations

import sys
import unittest
import urllib.error
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wear_edge_opea.megaservice import run_pipeline
from wear_edge_opea.dataprep import KnowledgeChunk
from wear_edge_opea.vector_store import QdrantVectorStore


class PipelineTest(unittest.TestCase):
    def test_manufacturing_pipeline_returns_guarded_action_card(self) -> None:
        result = run_pipeline(
            {
                "asset_id": "PKG-L3-GBX-03",
                "operator_observation": "high-pitched noise and warm gearbox housing",
                "signals": {
                    "vibration_rms_mm_s": 7.8,
                    "gearbox_temperature_c": 82,
                    "bearing_temperature_c": 78,
                    "lubrication_interval_days": 18,
                    "plc_alarm": "GBX-VIB-HI",
                },
            }
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["rag"]["asset_id"], "PKG-L3-GBX-03")
        self.assertEqual(result["maintenance_evaluation"]["risk_level"], "high")
        self.assertEqual(result["action_card"]["channel"], "maintenance_report")
        self.assertTrue(result["action_card"]["requires_human_confirmation"])
        self.assertIn("final_root_cause", result["action_card"]["blocked_claims"])

    def test_qdrant_index_treats_existing_collection_as_idempotent(self) -> None:
        class ConflictOnceQdrant(QdrantVectorStore):
            def __init__(self) -> None:
                super().__init__(url="http://qdrant", collection="existing")
                self.paths: list[str] = []

            def _request(self, method: str, path: str, body: dict | None = None) -> dict:
                self.paths.append(path)
                if method == "PUT" and path == "/collections/existing":
                    raise urllib.error.HTTPError(
                        url="http://qdrant/collections/existing",
                        code=409,
                        msg="Conflict",
                        hdrs=None,
                        fp=None,
                    )
                return {}

        store = ConflictOnceQdrant()
        store.index(
            [
                KnowledgeChunk(
                    id="test",
                    title="Gearbox vibration",
                    content="High vibration requires maintenance review.",
                    asset_id="PKG-L3-GBX-03",
                    revision="test",
                )
            ]
        )

        self.assertIn("/collections/existing/points?wait=true", store.paths)


if __name__ == "__main__":
    unittest.main()
