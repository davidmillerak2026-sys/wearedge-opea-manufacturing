from __future__ import annotations

import time

from .agents import entity_id_for, get_route, load_sample_request
from .dataprep import load_kb_for_route
from .evaluator import evaluate_request
from .guardrails import build_action_card
from .llm_stub import explain
from .retriever import retrieve_context


def run_pipeline(request: dict, mode: str | None = None) -> dict:
    start = time.perf_counter()
    route = get_route(mode or request.get("mode") or request.get("analysis_mode"))
    kb = load_kb_for_route(route)
    entity_id = entity_id_for(route, request, kb)
    observation = request.get("operator_observation", "")
    query = f"{route.mode} {entity_id} {observation} {route.integration_target} {route.business_value}"

    rag = retrieve_context(route.mode, query)
    evaluation = evaluate_request(route.mode, request, rag["thresholds"])
    explanation = explain(route, entity_id, observation, rag["hits"], evaluation)
    action_card = build_action_card(route, entity_id, evaluation, rag["hits"])

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    result = {
        "ok": True,
        "mode": route.mode,
        "agent": {
            "name": route.name,
            "business_value": route.business_value,
            "integration_target": route.integration_target,
        },
        "architecture": "OPEA-style Gateway -> Manufacturing Megaservice -> Dataprep -> RAG -> LLM -> Evaluator -> Guardrails",
        "opea_components": [
            "Gateway",
            "Megaservice",
            "Dataprep",
            "Retriever/RAG",
            "Vector DB profile",
            "LLM service",
            "Guardrails",
            "Evaluation",
        ],
        "entity_id": entity_id,
        "rag": rag,
        "agent_evaluation": evaluation,
        "llm_explanation": explanation,
        "action_card": action_card,
        "timing": {
            "pipeline_latency_ms": elapsed_ms,
            "note": "Dependency-free demo timing; production model latency is measured in the WearEdge source project.",
        },
    }
    if route.mode == "maintenance":
        result["asset_id"] = entity_id
        result["maintenance_evaluation"] = evaluation
    return result


def run_agent_demo(mode: str) -> dict:
    return run_pipeline(load_sample_request(mode), mode=mode)


def run_all_agent_demos() -> dict:
    demos = [run_agent_demo(mode) for mode in ("maintenance", "iqc", "changeover", "wi", "hazard")]
    return {
        "ok": all(item["ok"] for item in demos),
        "suite": "WearEdge OPEA Manufacturing five-agent suite",
        "modes": [item["mode"] for item in demos],
        "results": demos,
    }
