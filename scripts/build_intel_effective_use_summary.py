"""Build a compact Intel effective-use evidence summary.

The summary deliberately separates proven workload evidence from claims that
would need lower-level kernel instrumentation, such as oneDNN verbose logs or
production LLM acceleration.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BENCHMARKS = ROOT / "evidence" / "benchmarks"
OUTPUT = BENCHMARKS / "intel_effective_use.summary.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    cpu = load_json(BENCHMARKS / "intel_cpu_benchmark.xeon-amx.json")
    docker_qdrant = load_json(BENCHMARKS / "gcp_c3_docker_qdrant_e2e.summary.json")
    opea_profile = load_json(BENCHMARKS / "gcp_c3_opea_profile_e2e.summary.json")
    opea_tei = load_json(BENCHMARKS / "gcp_c3_opea_tei_profile_e2e.summary.json")
    tei_verbose = load_json(BENCHMARKS / "gcp_c3_tei_onednn_verbose.summary.json")

    feature_detection = cpu["cpu"]["feature_detection"]
    route_pipeline = cpu["pipeline"]

    summary = {
        "evidence": "WearEdge Intel effective-use evidence for OPEA Manufacturing",
        "schema_version": "2026-05-28",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "claim_status": "intel_xeon_avx512_amx_hosted_opea_workloads_passed",
        "claim_boundary": (
            "This evidence proves that WearEdge OPEA Manufacturing workloads were "
            "run and validated on a Google Cloud C3 Intel Xeon host exposing "
            "AVX-512 and AMX flags. The supplemental TEI/oneDNN verbose attempt "
            "captured TEI logs but did not emit dispatch marker lines. This does "
            "not prove oneDNN/TEI microkernel dispatch and does not claim "
            "production LLM acceleration."
        ),
        "single_node_challenge_fit": {
            "machine_type": "c3-standard-4",
            "zone": "us-central1-a",
            "vcpus": 4,
            "memory_gib": 16,
            "gpu": "none",
            "within_limit": True,
        },
        "cpu_features": {
            "processor": cpu["cpu"]["processor"],
            "system": cpu["cpu"]["system"],
            "release": cpu["cpu"]["release"],
            "avx512f": feature_detection["avx512f"],
            "avx512_bf16": feature_detection["avx512_bf16"],
            "avx512_vnni": feature_detection["avx512_vnni"],
            "amx_tile": feature_detection["amx_tile"],
            "amx_int8": feature_detection["amx_int8"],
            "amx_bf16": feature_detection["amx_bf16"],
        },
        "workloads_validated_on_c3": [
            {
                "name": "deterministic five-agent route pipeline",
                "source": "evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json",
                "total_calls": route_pipeline["total_calls"],
                "calls_per_second": route_pipeline["calls_per_second"],
                "p50_ms": route_pipeline["overall"]["p50_ms"],
                "p95_ms": route_pipeline["overall"]["p95_ms"],
                "scorecard_ok": route_pipeline["scorecard"]["ok"],
                "routes": {
                    route: {
                        "count": values["count"],
                        "p50_ms": values["p50_ms"],
                        "p95_ms": values["p95_ms"],
                    }
                    for route, values in route_pipeline["routes"].items()
                },
            },
            {
                "name": "Docker/Qdrant fresh-clone E2E",
                "source": "evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json",
                "runtime_profile": docker_qdrant["runtime_profile"],
                "validation": docker_qdrant["validation"],
                "latency": docker_qdrant["latency"],
                "all_checks_pass": docker_qdrant["all_checks_pass"],
            },
            {
                "name": "OPEA-compatible embedding microservice profile",
                "source": "evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json",
                "runtime_profile": opea_profile["runtime_profile"],
                "scorecard": opea_profile["scorecard"],
                "demo_pipeline_latency_ms": opea_profile["demo_pipeline_latency_ms"],
                "docker_stats_snapshot": opea_profile["docker_stats_snapshot"],
                "validation": opea_profile["validation"],
                "all_checks_pass": opea_profile["all_checks_pass"],
            },
            {
                "name": "official OPEA TEI embedding profile",
                "source": "evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json",
                "official_components": opea_tei["official_components"],
                "runtime": opea_tei["runtime"],
                "rag_vector_store_markers": opea_tei["rag_vector_store_markers"],
                "validation": opea_tei["validation"],
                "route_examples_visible_in_transcript": opea_tei["route_examples_visible_in_transcript"],
                "docker_stats": opea_tei["docker_stats"],
                "all_checks_pass": opea_tei["all_checks_pass"],
            },
            {
                "name": "supplemental official OPEA TEI oneDNN verbose attempt",
                "source": "evidence/benchmarks/gcp_c3_tei_onednn_verbose.summary.json",
                "runtime_profile": tei_verbose["runtime_profile"],
                "validation": tei_verbose["validation"],
                "dispatch_evidence": tei_verbose["dispatch_evidence"],
                "claim_status": tei_verbose["claim_status"],
                "all_checks_pass": tei_verbose["all_checks_pass"],
            },
        ],
        "effective_use_interpretation": [
            "The same single-node C3 class is used for CPU feature detection, route benchmark, Docker/Qdrant E2E, OPEA-compatible embedding E2E, and official OPEA TEI E2E.",
            "The official TEI profile validates a real embedding workload through Hugging Face TEI, opea/embedding:latest, /v1/embeddings, Qdrant, and all five route demos.",
            "The Docker evidence stays inside the challenge envelope: single node, 4 vCPU, 16 GiB RAM, no GPU.",
            "The benchmark is an application-level effective-use record, not a low-level AMX/AVX-512 kernel dispatch proof.",
            "The r20 TEI/oneDNN verbose attempt passed application checks but recorded dispatch_markers_captured=false.",
        ],
        "next_stronger_optional_evidence": [
            "Collect perf counters or use a TEI build that emits oneDNN/DNNL dispatch marker lines.",
            "Add a non-C3 baseline on a CPU without AMX for direct comparative latency.",
            "Benchmark a production LLM endpoint on the same C3 host only if the endpoint is configured and strict fallback is disabled.",
        ],
    }

    OUTPUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(summary["claim_status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
