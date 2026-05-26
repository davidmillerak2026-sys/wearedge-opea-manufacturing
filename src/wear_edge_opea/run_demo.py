from __future__ import annotations

import json
from pathlib import Path

from .megaservice import run_pipeline


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_REQUEST = ROOT / "data" / "sample_request.json"


def main() -> int:
    request = json.loads(SAMPLE_REQUEST.read_text(encoding="utf-8"))
    result = run_pipeline(request)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["action_card"]["channel"] not in {"maintenance_report", "schedule_maintenance"}:
        print("Unexpected action channel")
        return 1
    print("WearEdge OPEA Manufacturing demo passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

