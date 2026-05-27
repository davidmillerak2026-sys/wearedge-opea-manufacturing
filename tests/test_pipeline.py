from __future__ import annotations

import sys
import unittest
import urllib.error
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wear_edge_opea.megaservice import run_pipeline
from wear_edge_opea.agents import ROUTES, load_sample_request
from wear_edge_opea.dataprep import KnowledgeChunk
from wear_edge_opea.scorecard import build_scorecard
from wear_edge_opea.vector_store import QdrantVectorStore
from wear_edge_opea.demo_console import build_demo_console_html
from wear_edge_opea.embedding import _coerce_dimensions, _extract_embedding, embedding_profile_name
from scripts.intel_cpu_benchmark import claim_status


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
        self.assertEqual(result["mode"], "maintenance")
        self.assertEqual(result["rag"]["entity_id"], "PKG-L3-GBX-03")
        self.assertEqual(result["maintenance_evaluation"]["risk_level"], "high")
        self.assertEqual(result["action_card"]["channel"], "maintenance_report")
        self.assertTrue(result["action_card"]["requires_human_confirmation"])
        self.assertIn("final_root_cause", result["action_card"]["blocked_claims"])

    def test_all_five_agent_demos_return_expected_action_targets(self) -> None:
        for mode, route in ROUTES.items():
            with self.subTest(mode=mode):
                result = run_pipeline(load_sample_request(mode), mode=mode)

                self.assertTrue(result["ok"])
                self.assertEqual(result["mode"], mode)
                self.assertEqual(result["action_card"]["mode"], mode)
                self.assertEqual(result["action_card"]["integration_target"], route.integration_target)
                self.assertTrue(result["rag"]["hits"])

    def test_route_isolation_keeps_targets_separate(self) -> None:
        maintenance = run_pipeline(load_sample_request("maintenance"), mode="maintenance")
        hazard = run_pipeline(load_sample_request("hazard"), mode="hazard")
        iqc = run_pipeline(load_sample_request("iqc"), mode="iqc")

        self.assertEqual(maintenance["action_card"]["integration_target"], "maintenance_work_order")
        self.assertNotIn("safety_clearance", maintenance["action_card"]["blocked_claims"])
        self.assertEqual(hazard["action_card"]["integration_target"], "ehs_case")
        self.assertNotIn("final_root_cause", hazard["action_card"]["blocked_claims"])
        self.assertEqual(iqc["action_card"]["integration_target"], "qms_quality_event")
        self.assertNotEqual(iqc["action_card"]["integration_target"], "maintenance_work_order")

    def test_scorecard_covers_five_agent_modes(self) -> None:
        scorecard = build_scorecard()

        self.assertTrue(scorecard["ok"])
        self.assertEqual([route["mode"] for route in scorecard["routes"]], list(ROUTES))
        for route in scorecard["routes"]:
            self.assertEqual(route["status"], "pass")
            self.assertTrue(route["contract_pass"])
            self.assertTrue(route["guardrail_pass"])
            self.assertTrue(route["rag_source_match"])
            self.assertTrue(route["action_target_correctness"])

    def test_demo_console_exposes_product_entrypoint(self) -> None:
        html = build_demo_console_html()

        self.assertIn("Manufacturing Demo Console", html)
        self.assertIn("/v1/agents", html)
        self.assertIn("/v1/scorecard", html)
        for mode in ROUTES:
            self.assertIn(mode, html)

    def test_benchmark_claim_status_requires_avx512_and_amx(self) -> None:
        self.assertEqual(
            claim_status({"feature_detection": {"avx512f": True, "amx_tile": True}}),
            "xeon_avx512_amx_detected",
        )
        self.assertEqual(
            claim_status({"feature_detection": {"avx512f": True, "amx_tile": False}}),
            "local_smoke_test_not_avx512_amx_claim",
        )

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

    def test_opea_embedding_response_parser_supports_openai_shape(self) -> None:
        body = {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "index": 0,
                    "embedding": [0.1, 0.2, 0.3],
                }
            ],
        }

        self.assertEqual(_extract_embedding(body), [0.1, 0.2, 0.3])
        self.assertEqual(_coerce_dimensions([1.0], 3), [1.0, 0.0, 0.0])

    def test_default_embedding_profile_is_hashing(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(embedding_profile_name(), "hashing")

    def test_embedding_profile_can_be_named_for_official_tei(self) -> None:
        with patch.dict("os.environ", {"WEAREDGE_EMBEDDING_PROFILE": "opea-tei"}, clear=True):
            self.assertEqual(embedding_profile_name(), "opea-tei")

    def test_strict_embedding_dimensions_reject_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            _coerce_dimensions([1.0, 2.0], 3, strict=True)


if __name__ == "__main__":
    unittest.main()
