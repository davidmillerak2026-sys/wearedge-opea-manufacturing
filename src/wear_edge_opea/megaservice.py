from __future__ import annotations

import time

from .evaluator import evaluate_signals
from .guardrails import build_action_card
from .llm_stub import explain
from .retriever import retrieve_context


def run_pipeline(request: dict) -> dict:
    start = time.perf_counter()
    asset_id = request.get("asset_id", "unknown")
    observation = request.get("operator_observation", "")
    signals = request.get("signals", {})
    query = f"{asset_id} {observation} vibration temperature lubrication alarm maintenance"

    rag = retrieve_context(query)
    evaluation = evaluate_signals(signals, rag["thresholds"])
    explanation = explain(asset_id, observation, rag["hits"], evaluation)
    action_card = build_action_card(asset_id, evaluation, rag["hits"])

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    return {
        "ok": True,
        "architecture": "OPEA-style Gateway -> Manufacturing Megaservice -> RAG -> LLM -> Evaluator -> Guardrails",
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
        "asset_id": asset_id,
        "rag": rag,
        "maintenance_evaluation": evaluation,
        "llm_explanation": explanation,
        "action_card": action_card,
        "timing": {
            "pipeline_latency_ms": elapsed_ms,
            "note": "Dependency-free demo timing; production model latency is measured in the WearEdge source project.",
        },
    }

