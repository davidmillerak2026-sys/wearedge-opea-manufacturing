from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wear_edge_opea.megaservice import run_pipeline


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


if __name__ == "__main__":
    unittest.main()

