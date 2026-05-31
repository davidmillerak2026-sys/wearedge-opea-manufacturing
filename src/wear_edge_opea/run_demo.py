# SPDX-License-Identifier: MIT

from __future__ import annotations

import json

from .megaservice import run_all_agent_demos
from .scorecard import build_scorecard


def main() -> int:
    result = run_all_agent_demos()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    scorecard = build_scorecard()
    print(json.dumps(scorecard, indent=2, ensure_ascii=False))
    if not result["ok"] or not scorecard["ok"]:
        print("WearEdge OPEA five-agent sample failed")
        return 1
    print("WearEdge OPEA Manufacturing five-agent sample passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
