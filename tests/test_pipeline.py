# SPDX-License-Identifier: MIT

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
from wear_edge_opea.gateway import build_chatqna_response, chatqna_compatible
from wear_edge_opea.llm_adapter import _extract_text, build_prompt, configured_url
from wear_edge_opea.reranker import rerank_hits
from scripts.llm_adapter_benchmark import claim_status as llm_claim_status, endpoint_scope
from scripts.intel_cpu_benchmark import claim_status as intel_claim_status


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

    def test_all_five_agent_samples_return_expected_action_targets(self) -> None:
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

    def test_lexical_reranker_can_be_enabled_without_changing_contracts(self) -> None:
        with patch.dict("os.environ", {"WEAREDGE_RERANKER_BACKEND": "lexical"}, clear=True):
            result = run_pipeline(load_sample_request("maintenance"), mode="maintenance")

        self.assertTrue(result["ok"])
        self.assertEqual(result["rag"]["reranker"]["status"], "lexical")
        self.assertTrue(result["rag"]["reranker"]["applied"])
        self.assertIn("rerank_score", result["rag"]["hits"][0])
        self.assertEqual(result["action_card"]["integration_target"], "maintenance_work_order")

    def test_remote_reranker_response_shape_is_supported(self) -> None:
        hits = [
            {"score": 0.1, "payload": {"id": "a", "title": "temperature", "content": "heat"}},
            {"score": 0.2, "payload": {"id": "b", "title": "vibration", "content": "gearbox vibration"}},
        ]

        def fake_post_json(url: str, payload: dict, timeout: float) -> dict:
            self.assertEqual(url, "http://reranker:7000/v1/rerank")
            self.assertEqual(payload["top_n"], 2)
            return {
                "results": [
                    {"index": 1, "score": 0.2, "rerank_score": 2.2},
                    {"index": 0, "score": 0.1, "rerank_score": 0.4},
                ]
            }

        env = {
            "WEAREDGE_RERANKER_BACKEND": "remote",
            "WEAREDGE_RERANKER_URL": "http://reranker:7000/v1/rerank",
            "WEAREDGE_RERANKER_STRICT": "true",
        }
        with patch.dict("os.environ", env, clear=True):
            with patch("wear_edge_opea.reranker._post_json", side_effect=fake_post_json):
                reranked, metadata = rerank_hits("gearbox vibration", hits, limit=2)

        self.assertEqual(metadata["status"], "remote")
        self.assertEqual(reranked[0]["payload"]["id"], "b")
        self.assertEqual(reranked[0]["rerank_score"], 2.2)

    def test_demo_console_exposes_product_entrypoint(self) -> None:
        html = build_demo_console_html()

        self.assertIn("Manufacturing Console", html)
        self.assertIn("/v1/agents", html)
        self.assertIn("/v1/scorecard", html)
        for mode in ROUTES:
            self.assertIn(mode, html)

    def test_chatqna_compatible_endpoint_alias_returns_openai_like_shape(self) -> None:
        response = build_chatqna_response(
            {
                "mode": "maintenance",
                "messages": [{"role": "user", "content": "gearbox is hot and noisy"}],
            }
        )

        self.assertTrue(response["ok"])
        self.assertIn("choices", response)
        self.assertIn("message", response["choices"][0])
        self.assertEqual(response["wear_edge_result"]["mode"], "maintenance")
        self.assertEqual(response["wear_edge_result"]["action_card"]["integration_target"], "maintenance_work_order")

    def test_chatqna_alias_accepts_official_fixed_messages_string(self) -> None:
        response = build_chatqna_response(
            {
                "mode": "maintenance",
                "messages": "Operator reports high gearbox vibration and oil smell.",
                "max_tokens": 160,
            }
        )

        self.assertGreater(response["usage"]["prompt_tokens"], 0)
        self.assertIn(
            "Operator reports high gearbox vibration and oil smell",
            response["wear_edge_result"]["request"]["operator_observation"],
        )

    def test_chatqna_route_returns_streaming_response_by_default(self) -> None:
        response = chatqna_compatible(
            {
                "mode": "maintenance",
                "messages": "Operator reports high gearbox vibration and oil smell.",
            }
        )

        self.assertEqual(response.media_type, "text/event-stream")

    def test_benchmark_claim_status_requires_avx512_and_amx(self) -> None:
        self.assertEqual(
            intel_claim_status({"feature_detection": {"avx512f": True, "amx_tile": True}}),
            "xeon_avx512_amx_detected",
        )
        self.assertEqual(
            intel_claim_status({"feature_detection": {"avx512f": True, "amx_tile": False}}),
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

    def test_llm_runtime_defaults_to_deterministic_contract(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            result = run_pipeline(load_sample_request("maintenance"), mode="maintenance")

        self.assertEqual(result["llm_runtime"]["backend"], "deterministic")
        self.assertEqual(result["llm_runtime"]["claim_status"], "deterministic_llm_adapter_contract")
        self.assertFalse(result["llm_runtime"]["fallback_used"])

    def test_openai_compatible_llm_adapter_can_be_benchmarked(self) -> None:
        def fake_post_json(url: str, payload: dict, timeout: float) -> dict:
            self.assertEqual(url, "http://llm-service:9000/v1/chat/completions")
            self.assertEqual(payload["model"], "test-model")
            return {
                "choices": [
                    {
                        "message": {
                            "content": "LLM-backed bounded action-card explanation with preserved source IDs."
                        }
                    }
                ]
            }

        env = {
            "WEAREDGE_LLM_BACKEND": "openai-compatible",
            "WEAREDGE_LLM_URL": "http://llm-service:9000/v1/chat/completions",
            "WEAREDGE_LLM_MODEL": "test-model",
            "WEAREDGE_LLM_STRICT": "true",
        }
        with patch.dict("os.environ", env, clear=True):
            with patch("wear_edge_opea.llm_adapter._post_json", side_effect=fake_post_json):
                result = run_pipeline(load_sample_request("hazard"), mode="hazard")

        self.assertEqual(result["llm_runtime"]["backend"], "openai-compatible")
        self.assertEqual(result["llm_runtime"]["model"], "test-model")
        self.assertEqual(result["llm_runtime"]["claim_status"], "production_llm_endpoint_used")
        self.assertFalse(result["llm_runtime"]["fallback_used"])
        self.assertIn("LLM-backed", result["llm_explanation"])

    def test_ollama_native_llm_adapter_can_use_local_model_endpoint(self) -> None:
        def fake_post_json(url: str, payload: dict, timeout: float) -> dict:
            self.assertEqual(url, "http://127.0.0.1:11434/api/chat")
            self.assertEqual(payload["model"], "gemma-local")
            self.assertFalse(payload["stream"])
            self.assertFalse(payload["think"])
            return {"message": {"content": "Local Gemma-backed action-card explanation."}}

        env = {
            "WEAREDGE_LLM_BACKEND": "ollama",
            "WEAREDGE_LLM_MODEL": "gemma-local",
            "WEAREDGE_LLM_STRICT": "true",
        }
        with patch.dict("os.environ", env, clear=True):
            with patch("wear_edge_opea.llm_adapter._post_json", side_effect=fake_post_json):
                result = run_pipeline(load_sample_request("maintenance"), mode="maintenance")

        self.assertEqual(result["llm_runtime"]["backend"], "ollama")
        self.assertEqual(result["llm_runtime"]["service_url"], "http://127.0.0.1:11434/api/chat")
        self.assertEqual(result["llm_runtime"]["claim_status"], "local_llm_endpoint_used")
        self.assertFalse(result["llm_runtime"]["fallback_used"])
        self.assertIn("Local Gemma-backed", result["llm_explanation"])

    def test_ollama_response_shape_and_local_claim_status_are_supported(self) -> None:
        self.assertEqual(_extract_text({"message": {"content": "ok"}}), "ok")
        with patch.dict("os.environ", {"WEAREDGE_LLM_BACKEND": "ollama"}, clear=True):
            self.assertEqual(configured_url(), "http://127.0.0.1:11434/api/chat")
        self.assertEqual(endpoint_scope("http://127.0.0.1:11434/api/chat"), "local_model_endpoint")
        self.assertEqual(llm_claim_status(True, "local_model_endpoint"), "local_llm_endpoint_benchmarked")

    def test_llm_prompt_preserves_route_sources_and_claim_boundary(self) -> None:
        result = run_pipeline(load_sample_request("iqc"), mode="iqc")
        prompt = build_prompt(
            ROUTES["iqc"],
            result["entity_id"],
            result["request"]["operator_observation"],
            result["rag"]["hits"],
            result["agent_evaluation"],
        )

        self.assertIn("Agent mode: iqc", prompt)
        self.assertIn("Integration target: qms_quality_event", prompt)
        self.assertIn("Preserve source IDs", prompt)


if __name__ == "__main__":
    unittest.main()
