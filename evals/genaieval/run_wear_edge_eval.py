# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
from pathlib import Path

from wear_edge_eval import DEFAULT_DATASET, evaluate_dataset, load_dataset, write_json_report, write_markdown_summary


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the WearEdge GenAIEval-compatible route evaluation.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "genaieval" / "route_eval_results.json")
    parser.add_argument("--summary-output", type=Path, default=ROOT / "evidence" / "genaieval" / "summary.md")
    args = parser.parse_args()

    cases = load_dataset(args.dataset)
    report = evaluate_dataset(cases, args.dataset)
    write_json_report(report, args.output)
    write_markdown_summary(report, args.summary_output)

    status = "passed" if report["summary"]["ok"] else "requires review"
    print(
        f"WearEdge GenAIEval-compatible route evaluation {status}: "
        f"{report['summary']['passed_cases']}/{report['summary']['total_cases']} cases"
    )
    print(args.output)
    print(args.summary_output)
    return 0 if report["summary"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
