"""Validate the standalone OPEA Manufacturing submission package.

The check is dependency-free. It verifies the local submission files and
ensures that no planned component is accidentally marked as implemented.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence" / "component-evidence.json"
REQUIRED_LOCAL_FILES = [
    "README.md",
    "SUBMISSION.md",
    "submission-fields.draft.json",
    "docs/technical-report.draft.md",
    "docs/opea-component-evidence.md",
    "docs/champion-gap-worklist.md",
    "docs/source-project-map.md",
    "evidence/component-evidence.json",
    "docker-compose.yml",
    "deploy.sh",
    "run_manufacturing_demo.sh",
    "data/sample_requests/maintenance.json",
    "data/sample_requests/iqc.json",
    "data/sample_requests/changeover.json",
    "data/sample_requests/wi.json",
    "data/sample_requests/hazard.json",
    "data/agent_kb/iqc_quality_plan.json",
    "data/agent_kb/changeover_sku_c500.json",
    "data/agent_kb/wi_cartoner_st2.json",
    "data/agent_kb/hazard_policy.json",
    "src/wear_edge_opea/agents.py",
    "src/wear_edge_opea/megaservice.py",
    "src/wear_edge_opea/scorecard.py",
    "tests/test_pipeline.py",
]


def main() -> int:
    missing = [path for path in REQUIRED_LOCAL_FILES if not (ROOT / path).exists()]
    if missing:
        print("OPEA submission evidence check failed")
        for path in missing:
            print(f"- missing {path}")
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    statuses: dict[str, int] = {}
    missing_manifest_paths: list[str] = []

    for item in manifest["component_map"]:
        status = item["status"]
        statuses[status] = statuses.get(status, 0) + 1
        for path in item.get("local_paths", []):
            if not (ROOT / path).exists():
                missing_manifest_paths.append(f"{item['opea_layer']}: {path}")

    if missing_manifest_paths:
        print("OPEA submission evidence check failed")
        for path in missing_manifest_paths:
            print(f"- missing manifest path {path}")
        return 1

    print("OPEA submission evidence check passed")
    print(f"components={len(manifest['component_map'])}")
    for status in sorted(statuses):
        print(f"{status}={statuses[status]}")
    print(manifest["submission"]["target_github_url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
