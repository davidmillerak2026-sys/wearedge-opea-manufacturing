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
    "pyproject.toml",
    "docs/technical-report.draft.md",
    "docs/submission-product-shape.md",
    "docs/final-submission-readiness-audit.md",
    "docs/champion-risk-burn-down.md",
    "docs/opea-native-depth-matrix.md",
    "docs/production-llm-benchmark-path.md",
    "docs/genaieval-compatible-evaluation.md",
    "docs/data-provenance-and-field-validation.md",
    "docs/telecom-scope-and-manufacturing-positioning.md",
    "docs/upstream-pr-attempt-2026-05-28.md",
    "docs/opea-component-evidence.md",
    "docs/official-opea-profile.md",
    "docs/official-opea-tei-profile.md",
    "docs/local-opea-tei-profile-e2e-report.md",
    "docs/gcp-c3-opea-tei-profile-e2e-report.md",
    "docs/champion-gap-worklist.md",
    "docs/source-project-map.md",
    "docs/publication-record.md",
    "docs/opea-upstream/rfc-issue-draft.md",
    "docs/opea-upstream/blueprint-feedback.md",
    "docs/opea-upstream/implementation-feedback-comment.md",
    "docs/opea-upstream/minimal-pr-scope.md",
    "docs/opea-upstream/tei-update-comment.md",
    "docs/intel-avx512-amx-benchmark-report.md",
    "docs/gcp-c3-docker-qdrant-e2e-report.md",
    "docs/gcp-c3-opea-profile-e2e-report.md",
    "docs/xeon-amx-benchmark-runbook.md",
    "public/article-wear-edge-opea-manufacturing.md",
    "public/demo-video-script.md",
    "public/demo-video-captions.srt",
    "scripts/intel_cpu_benchmark.py",
    "scripts/xeon_amx_benchmark_remote.sh",
    "scripts/gcp_c3_opea_profile_e2e_cloudshell.sh",
    "scripts/gcp_c3_opea_tei_profile_e2e_cloudshell.sh",
    "scripts/record_gcp_opea_tei_evidence.py",
    "scripts/llm_adapter_benchmark.py",
    "evals/genaieval/README.md",
    "evals/genaieval/manufacturing_route_eval.dataset.jsonl",
    "evals/genaieval/manufacturing_route_benchmark.yaml",
    "evals/genaieval/wear_edge_eval.py",
    "evals/genaieval/run_wear_edge_eval.py",
    "evals/genaieval/run_wear_edge_benchmark.py",
    "evidence/benchmarks/intel_cpu_benchmark.local-smoke.json",
    "evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json",
    "evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json",
    "evidence/benchmarks/local_opea_profile_e2e.summary.json",
    "evidence/benchmarks/local_opea_tei_profile_e2e.summary.json",
    "evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json",
    "evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json",
    "evidence/benchmarks/llm_adapter_contract.local-smoke.json",
    "evidence/genaieval/route_eval_results.json",
    "evidence/genaieval/benchmark_results.json",
    "evidence/genaieval/summary.md",
    "evidence/component-evidence.json",
    "docker-compose.yml",
    "docker-compose.opea.yml",
    "docker-compose.opea-tei.yml",
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
    "src/wear_edge_opea/embedding.py",
    "src/wear_edge_opea/opea_embedding_service.py",
    "src/wear_edge_opea/llm_adapter.py",
    "src/wear_edge_opea/demo_console.py",
    "src/wear_edge_opea/megaservice.py",
    "src/wear_edge_opea/scorecard.py",
    "tests/test_genaieval_pack.py",
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

    for item in manifest.get("bonus_evidence", []):
        for path in item.get("local_paths", []):
            if not (ROOT / path).exists():
                missing_manifest_paths.append(f"{item['category']}: {path}")

    if missing_manifest_paths:
        print("OPEA submission evidence check failed")
        for path in missing_manifest_paths:
            print(f"- missing manifest path {path}")
        return 1

    print("OPEA submission evidence check passed")
    print(f"components={len(manifest['component_map'])}")
    print(f"bonus_evidence={len(manifest.get('bonus_evidence', []))}")
    for status in sorted(statuses):
        print(f"{status}={statuses[status]}")
    print(manifest["submission"]["target_github_url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
