from __future__ import annotations

from .agents import ROUTES
from .megaservice import run_agent_demo


def build_scorecard() -> dict:
    route_scores = []
    for mode, route in ROUTES.items():
        result = run_agent_demo(mode)
        action_card = result["action_card"]
        evaluation = result["agent_evaluation"]
        checks = {
            "contract_pass": _has_contract_fields(action_card),
            "guardrail_pass": bool(action_card.get("blocked_claims")),
            "rag_source_match": bool(result["rag"].get("hits")),
            "action_target_correctness": action_card.get("integration_target") == route.integration_target,
            "route_isolation_pass": _route_isolation_pass(mode, action_card),
        }
        route_scores.append(
            {
                "mode": mode,
                "status": "pass" if all(checks.values()) else "review",
                "latency_ms": result["timing"]["pipeline_latency_ms"],
                "risk_level": evaluation["risk_level"],
                "channel": action_card["channel"],
                "integration_target": action_card["integration_target"],
                **checks,
            }
        )
    return {
        "ok": all(item["status"] == "pass" for item in route_scores),
        "suite": "WearEdge OPEA Manufacturing five-agent scorecard",
        "metrics": [
            "latency_ms",
            "contract_pass",
            "guardrail_pass",
            "rag_source_match",
            "action_target_correctness",
            "route_isolation_pass",
        ],
        "routes": route_scores,
    }


def _has_contract_fields(action_card: dict) -> bool:
    required = {
        "mode",
        "channel",
        "priority",
        "owner",
        "requires_human_confirmation",
        "integration_target",
        "action",
        "source_ids",
        "blocked_claims",
    }
    return required.issubset(action_card)


def _route_isolation_pass(mode: str, action_card: dict) -> bool:
    target = action_card.get("integration_target")
    blocked = set(action_card.get("blocked_claims", []))
    if mode == "maintenance":
        return target == "maintenance_work_order" and "safety_clearance" not in blocked
    if mode == "iqc":
        return target == "qms_quality_event" and target != "maintenance_work_order"
    if mode == "changeover":
        return target == "changeover_checklist" and "restart_permission" in blocked
    if mode == "wi":
        return target == "wi_reference" and "unreleased_instruction" in blocked
    if mode == "hazard":
        return target == "ehs_case" and "final_root_cause" not in blocked
    return False
