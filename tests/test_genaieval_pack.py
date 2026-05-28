from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from evals.genaieval.wear_edge_eval import DEFAULT_DATASET, evaluate_dataset, load_dataset


class GenAIEvalPackTest(unittest.TestCase):
    def test_genaieval_compatible_dataset_passes_all_route_metrics(self) -> None:
        report = evaluate_dataset(load_dataset(DEFAULT_DATASET), DEFAULT_DATASET)

        self.assertTrue(report["summary"]["ok"])
        self.assertEqual(report["summary"]["total_cases"], 15)
        self.assertEqual(report["summary"]["passed_cases"], 15)
        self.assertEqual(list(report["summary"]["per_route"]), ["maintenance", "iqc", "changeover", "wi", "hazard"])


if __name__ == "__main__":
    unittest.main()
