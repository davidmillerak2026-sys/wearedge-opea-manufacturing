# SPDX-License-Identifier: MIT

"""Benchmark the optional local or production LLM adapter path.

The default run is a deterministic contract smoke test. Set
WEAREDGE_LLM_BACKEND=openai-compatible and WEAREDGE_LLM_URL or
WEAREDGE_LLM_BASE_URL to benchmark an OpenAI-compatible LLM endpoint. Local
Ollama, LM Studio, vLLM, and llama.cpp servers can be benchmarked the same way.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import statistics
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wear_edge_opea.agents import ROUTES, load_sample_request  # noqa: E402
from wear_edge_opea.llm_adapter import configured_url  # noqa: E402
from wear_edge_opea.megaservice import run_pipeline  # noqa: E402


LOCAL_PROFILES = {
    "ollama": {
        "backend": "ollama",
        "base_url": "http://127.0.0.1:11434",
        "url": "http://127.0.0.1:11434/api/chat",
    },
    "lmstudio": {
        "backend": "openai-compatible",
        "base_url": "http://127.0.0.1:1234/v1",
    },
    "vllm": {
        "backend": "openai-compatible",
        "base_url": "http://127.0.0.1:8000/v1",
    },
    "llamacpp": {
        "backend": "openai-compatible",
        "base_url": "http://127.0.0.1:8080/v1",
    },
}


def summarize(values: list[float]) -> dict:
    if not values:
        return {"count": 0, "min_ms": 0, "mean_ms": 0, "p50_ms": 0, "p95_ms": 0, "max_ms": 0}
    ordered = sorted(values)
    p95_index = min(len(ordered) - 1, int(round((len(ordered) - 1) * 0.95)))
    return {
        "count": len(values),
        "min_ms": round(min(values), 2),
        "mean_ms": round(statistics.fmean(values), 2),
        "p50_ms": round(statistics.median(values), 2),
        "p95_ms": round(ordered[p95_index], 2),
        "max_ms": round(max(values), 2),
    }


def endpoint_scope(url: str) -> str:
    lowered = url.lower()
    if any(host in lowered for host in ("127.0.0.1", "localhost", "::1")):
        return "local_model_endpoint"
    if url:
        return "remote_model_endpoint"
    return "no_endpoint_configured"


def claim_status(model_endpoint_used: bool, scope: str) -> str:
    if not model_endpoint_used:
        return "deterministic_llm_adapter_contract_smoke_test"
    if scope == "local_model_endpoint":
        return "local_llm_endpoint_benchmarked"
    return "production_llm_endpoint_benchmarked"


def run(iterations: int) -> dict:
    calls: list[dict] = []
    pipeline_latencies: list[float] = []
    llm_latencies: list[float] = []
    started = time.perf_counter()

    for _ in range(iterations):
        for mode, route in ROUTES.items():
            result = run_pipeline(load_sample_request(mode), mode=mode)
            llm_runtime = result["llm_runtime"]
            calls.append(
                {
                    "mode": mode,
                    "ok": result["ok"],
                    "integration_target": result["action_card"]["integration_target"],
                    "expected_integration_target": route.integration_target,
                    "guardrail_pass": bool(result["action_card"]["blocked_claims"]),
                    "rag_source_match": bool(result["rag"]["hits"]),
                    "llm_backend": llm_runtime["backend"],
                    "llm_fallback_used": llm_runtime["fallback_used"],
                    "llm_claim_status": llm_runtime["claim_status"],
                    "llm_latency_ms": llm_runtime["latency_ms"],
                    "pipeline_latency_ms": result["timing"]["pipeline_latency_ms"],
                }
            )
            pipeline_latencies.append(result["timing"]["pipeline_latency_ms"])
            llm_latencies.append(llm_runtime["latency_ms"])

    backend_names = sorted({call["llm_backend"] for call in calls})
    fallbacks = [call for call in calls if call["llm_fallback_used"]]
    model_endpoint_used = bool(calls) and not fallbacks and backend_names != ["deterministic"]
    service_url = configured_url()
    scope = endpoint_scope(service_url)
    all_contracts_pass = all(
        call["ok"]
        and call["integration_target"] == call["expected_integration_target"]
        and call["guardrail_pass"]
        and call["rag_source_match"]
        for call in calls
    )

    return {
        "benchmark": "WearEdge OPEA Manufacturing LLM adapter benchmark",
        "schema_version": "2026-05-28",
        "claim_status": claim_status(model_endpoint_used, scope),
        "configuration": {
            "WEAREDGE_LLM_BACKEND": os.getenv("WEAREDGE_LLM_BACKEND", "deterministic"),
            "WEAREDGE_LLM_URL_CONFIGURED": bool(os.getenv("WEAREDGE_LLM_URL") or os.getenv("WEAREDGE_LLM_BASE_URL")),
            "WEAREDGE_LLM_MODEL": os.getenv("WEAREDGE_LLM_MODEL", "manufacturing-action-card-adapter"),
            "WEAREDGE_LLM_STRICT": os.getenv("WEAREDGE_LLM_STRICT", "false"),
            "WEAREDGE_LLM_API_KEY_CONFIGURED": bool(os.getenv("WEAREDGE_LLM_API_KEY") or os.getenv("OPENAI_API_KEY")),
            "service_url": service_url or "in-process",
            "endpoint_scope": scope,
        },
        "iterations_per_route": iterations,
        "total_calls": len(calls),
        "total_seconds": round(time.perf_counter() - started, 4),
        "llm_latency": summarize(llm_latencies),
        "pipeline_latency": summarize(pipeline_latencies),
        "backend_names": backend_names,
        "fallback_count": len(fallbacks),
        "all_contracts_pass": all_contracts_pass,
        "model_endpoint_used": model_endpoint_used,
        "production_endpoint_used": model_endpoint_used and scope == "remote_model_endpoint",
        "local_endpoint_used": model_endpoint_used and scope == "local_model_endpoint",
        "sample_calls": calls[: min(len(calls), 10)],
        "claim_boundary": (
            "Use local_llm_endpoint_benchmarked for localhost model services such as Ollama, "
            "LM Studio, vLLM, or llama.cpp. Use production_llm_endpoint_benchmarked only when "
            "a remote production endpoint is configured and fallback_count is zero. Otherwise "
            "this is a deterministic adapter contract smoke test."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--backend")
    parser.add_argument("--url")
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--local-profile", choices=sorted(LOCAL_PROFILES))
    args = parser.parse_args()

    if args.local_profile:
        profile = LOCAL_PROFILES[args.local_profile]
        os.environ["WEAREDGE_LLM_BACKEND"] = profile["backend"]
        if "url" in profile:
            os.environ["WEAREDGE_LLM_URL"] = profile["url"]
        else:
            os.environ["WEAREDGE_LLM_BASE_URL"] = profile["base_url"]
    if args.backend:
        os.environ["WEAREDGE_LLM_BACKEND"] = args.backend
    if args.url:
        os.environ["WEAREDGE_LLM_URL"] = args.url
    if args.base_url:
        os.environ["WEAREDGE_LLM_BASE_URL"] = args.base_url
    if args.model:
        os.environ["WEAREDGE_LLM_MODEL"] = args.model
    if args.strict:
        os.environ["WEAREDGE_LLM_STRICT"] = "true"

    artifact = run(max(1, args.iterations))
    text = json.dumps(artifact, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if artifact["all_contracts_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
