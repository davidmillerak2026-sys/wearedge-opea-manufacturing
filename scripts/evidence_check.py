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
]


def main() -> int:
    missing = [path for path in REQUIRED_LOCAL_FILES if not (ROOT / path).exists()]
    if missing:
        print("OPEA submission evidence check failed")
        for path in missing:
            print(f"- missing {path}")
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    accidental_claims = []
    statuses: dict[str, int] = {}

    for item in manifest["component_map"]:
        status = item["status"]
        statuses[status] = statuses.get(status, 0) + 1
        if item["opea_layer"] in {"Vector DB", "Embeddings"} and status != "planned":
            accidental_claims.append(item["opea_layer"])

    if accidental_claims:
        print("OPEA submission evidence check failed")
        for layer in accidental_claims:
            print(f"- {layer} must stay planned until implemented")
        return 1

    print("OPEA submission evidence check passed")
    print(f"components={len(manifest['component_map'])}")
    for status in sorted(statuses):
        print(f"{status}={statuses[status]}")
    print(manifest["submission"]["target_github_url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

