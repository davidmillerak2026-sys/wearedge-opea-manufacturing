# SPDX-License-Identifier: MIT

"""Create submission evidence files from a full GCP OPEA TEI E2E artifact."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "evidence" / "benchmarks" / "gcp_c3_opea_tei_profile_e2e.summary.json"
REPORT_PATH = ROOT / "docs" / "gcp-c3-opea-tei-profile-e2e-report.md"


def compact(value: Any, limit: int = 1600) -> Any:
    text = json.dumps(value, ensure_ascii=False)
    if len(text) <= limit:
        return value
    return {"truncated": True, "json_prefix": text[:limit]}


def split_metadata(value: str | None) -> str:
    return (value or "").split("/")[-1]


def build_summary(artifact: dict[str, Any]) -> dict[str, Any]:
    embedding = (
        artifact.get("endpoints", {})
        .get("embedding_response_sample", {})
        .get("data", [{}])[0]
        .get("embedding", [])
    )
    scorecard = artifact.get("endpoints", {}).get("scorecard", {})
    demos = artifact.get("endpoints", {}).get("demos", {})

    return {
        "benchmark": "WearEdge official OPEA TEI embedding profile C3 E2E",
        "schema_version": "2026-05-27",
        "captured_at": artifact.get("captured_at") or datetime.now(timezone.utc).isoformat(),
        "claim_status": artifact.get("claim_status", "fresh_clone_official_opea_tei_embedding_profile_e2e"),
        "repo": artifact.get("repo", {}),
        "gcp": artifact.get("gcp", {}),
        "runtime": artifact.get("runtime", {}),
        "official_references": artifact.get("official_references", []),
        "validation": artifact.get("validation", {}),
        "all_checks_pass": artifact.get("all_checks_pass") is True,
        "embedding": {
            "dimensions": len(embedding),
            "openai_shape": bool(embedding),
            "health_raw": artifact.get("endpoints", {}).get("embedding_health_raw", ""),
        },
        "gateway_healthz": artifact.get("endpoints", {}).get("gateway_healthz", {}),
        "rag_vector_store_markers": artifact.get("rag_vector_store_markers", {}),
        "scorecard": {
            "ok": scorecard.get("ok"),
            "routes": scorecard.get("routes", []),
        },
        "demos": {
            mode: {
                "ok": demo.get("ok"),
                "vector_store": demo.get("rag", {}).get("vector_store"),
                "integration_target": demo.get("action_card", {}).get("integration_target"),
                "latency_ms": demo.get("timing", {}).get("pipeline_latency_ms"),
            }
            for mode, demo in demos.items()
        },
        "docker": {
            "stats": artifact.get("docker", {}).get("stats", []),
            "compose_ps": artifact.get("docker", {}).get("compose_ps", []),
            "compose_logs_tail": compact(artifact.get("docker", {}).get("compose_logs_tail", "")),
        },
        "claim_boundary": (
            "This GCP C3 fresh-clone run validates the official OPEA TEI embedding "
            "component path for WearEdge OPEA Manufacturing. It does not claim "
            "production LLM acceleration."
        ),
    }


def markdown_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Route | Status | Latency | Integration target |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row.get('mode')}` | {row.get('status')} | {row.get('latency_ms')} ms | `{row.get('integration_target')}` |"
        )
    return "\n".join(lines)


def build_report(summary: dict[str, Any]) -> str:
    gcp = summary.get("gcp", {})
    runtime = summary.get("runtime", {})
    gateway = summary.get("gateway_healthz", {})
    scorecard = summary.get("scorecard", {})
    validation = summary.get("validation", {})

    validation_lines = "\n".join(
        f"- `{key}`: `{value}`" for key, value in validation.items()
    )

    return f"""# GCP C3 OPEA TEI Profile E2E Report

Captured: {summary.get("captured_at")}

## Summary

The official OPEA TEI profile was run from a fresh clone on Google Cloud C3.

```text
docker-compose.yml + docker-compose.opea-tei.yml
```

Overall result: `{summary.get("all_checks_pass")}`

## Host

| Field | Value |
| --- | --- |
| Project | `{gcp.get("project_id")}` |
| Zone | `{split_metadata(gcp.get("zone"))}` |
| Machine type | `{split_metadata(gcp.get("machine_type"))}` |
| CPU platform | `{gcp.get("cpu_platform")}` |
| Setup seconds | `{runtime.get("setup_seconds")}` |

## Component Path

```text
Manufacturing Gateway
  -> OPEA embedding microservice
  -> Hugging Face Text Embeddings Inference
  -> Qdrant
  -> five WearEdge manufacturing agents
  -> scorecard
```

Gateway embedding URL:

```text
{gateway.get("embedding_url")}
```

Embedding dimensions: `{summary.get("embedding", {}).get("dimensions")}`

## Scorecard

{markdown_table(scorecard.get("routes", []))}

## Validation

{validation_lines}

## Evidence

```text
evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json
scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh
```

## Claim Boundary

{summary.get("claim_boundary")}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path, help="Full JSON artifact emitted by the Cloud Shell runner")
    args = parser.parse_args()

    artifact = json.loads(args.artifact.read_text(encoding="utf-8"))
    summary = build_summary(artifact)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    REPORT_PATH.write_text(build_report(summary), encoding="utf-8")

    print(f"wrote {SUMMARY_PATH}")
    print(f"wrote {REPORT_PATH}")
    if not summary["all_checks_pass"]:
        raise SystemExit("artifact did not pass all checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
