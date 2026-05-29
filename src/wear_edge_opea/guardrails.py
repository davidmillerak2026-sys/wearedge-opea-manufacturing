# SPDX-License-Identifier: MIT

from __future__ import annotations

from .agents import AgentRoute


def build_action_card(route: AgentRoute, entity_id: str, evaluation: dict, rag_hits: list[dict]) -> dict:
    if route.mode == "maintenance":
        return _maintenance_action_card(route, entity_id, evaluation, rag_hits)
    if route.mode == "iqc":
        return _iqc_action_card(route, entity_id, evaluation, rag_hits)
    if route.mode == "changeover":
        return _changeover_action_card(route, entity_id, evaluation, rag_hits)
    if route.mode == "wi":
        return _wi_action_card(route, entity_id, evaluation, rag_hits)
    if route.mode == "hazard":
        return _hazard_action_card(route, entity_id, evaluation, rag_hits)
    raise ValueError(f"Unsupported action-card mode: {route.mode}")


def _source_ids(rag_hits: list[dict]) -> list[str]:
    return [hit["payload"].get("id") for hit in rag_hits if hit.get("payload")]


def _base_card(route: AgentRoute, channel: str, priority: str, owner: str, action: str, rag_hits: list[dict]) -> dict:
    return {
        "mode": route.mode,
        "channel": channel,
        "priority": priority,
        "owner": owner,
        "requires_human_confirmation": route.human_gate or priority in {"high", "critical"},
        "integration_target": route.integration_target,
        "action": action,
        "source_ids": _source_ids(rag_hits),
        "blocked_claims": list(route.blocked_claims),
    }


def _maintenance_action_card(route: AgentRoute, asset_id: str, evaluation: dict, rag_hits: list[dict]) -> dict:
    has_identity = asset_id == "PKG-L3-GBX-03"
    risk_level = evaluation["risk_level"]

    if not has_identity:
        channel = "maintenance_identification_required"
        priority = "medium"
        action = "Inspect asset identity and station sign before making machine-specific maintenance recommendations."
    elif risk_level == "high":
        channel = "maintenance_report"
        priority = "high"
        action = "Report a high-risk gearbox condition and prepare a human-confirmed maintenance work-order draft."
    elif risk_level == "medium":
        channel = "schedule_maintenance"
        priority = "medium"
        action = "Schedule maintenance inspection and collect confirmatory vibration, temperature, and lubrication evidence."
    else:
        channel = "condition_monitoring"
        priority = "low"
        action = "Monitor the gearbox condition and keep collecting routine evidence during the shift."

    owner = "maintenance_engineer" if priority in {"high", "medium"} else "operator"
    return _base_card(route, channel, priority, owner, action, rag_hits)


def _iqc_action_card(route: AgentRoute, product_id: str, evaluation: dict, rag_hits: list[dict]) -> dict:
    if evaluation["risk_level"] == "high":
        return _base_card(
            route,
            "stop_production",
            "critical",
            "quality_engineer",
            f"Stop station output for {product_id}, contain the affected lot window, and require quality engineer disposition.",
            rag_hits,
        )
    if evaluation["risk_level"] == "medium":
        return _base_card(
            route,
            "quality_hold",
            "high",
            "quality_engineer",
            f"Hold {product_id}, expand inspection, and create a QMS quality event with detector evidence.",
            rag_hits,
        )
    return _base_card(
        route,
        "quality_review",
        "medium",
        "quality_engineer",
        f"Record detector-clear evidence for {product_id} and keep release authority with quality.",
        rag_hits,
    )


def _changeover_action_card(route: AgentRoute, machine_id: str, evaluation: dict, rag_hits: list[dict]) -> dict:
    if evaluation["breach_count"]:
        return _base_card(
            route,
            "changeover_verification",
            "medium",
            "operator_quality",
            f"Hold restart on {machine_id} until missing checklist confirmations are completed and first-piece sign-off is recorded.",
            rag_hits,
        )
    return _base_card(
        route,
        "changeover_ready_for_signoff",
        "medium",
        "operator_quality",
        f"Package {machine_id} changeover evidence for human first-piece sign-off before restart.",
        rag_hits,
    )


def _wi_action_card(route: AgentRoute, machine_id: str, evaluation: dict, rag_hits: list[dict]) -> dict:
    if evaluation["status"] == "stop_required":
        return _base_card(
            route,
            "wi_stop_and_escalate",
            "high",
            "line_lead",
            f"Stop guided operation on {machine_id}; active alarm context requires line-lead confirmation.",
            rag_hits,
        )
    if evaluation["status"] == "source_check_required":
        return _base_card(
            route,
            "wi_source_check_required",
            "medium",
            "operator",
            f"Confirm machine identity, released WI revision, and guard state before giving {machine_id} work guidance.",
            rag_hits,
        )
    return _base_card(
        route,
        "guided_operation",
        "low",
        "operator",
        f"Guide {machine_id} from released WI: keep guards closed, align only released guide marks, and escalate repeated jams.",
        rag_hits,
    )


def _hazard_action_card(route: AgentRoute, area_id: str, evaluation: dict, rag_hits: list[dict]) -> dict:
    if evaluation["risk_level"] == "high":
        return _base_card(
            route,
            "stop_and_make_safe",
            "critical",
            "operator",
            f"Stop work in {area_id}, clear the walkway or exposure, restore required PPE, and create an EHS observation.",
            rag_hits,
        )
    if evaluation["risk_level"] == "medium":
        return _base_card(
            route,
            "ehs_report",
            "high",
            "ehs_coordinator",
            f"Report the visible hazard in {area_id} and assign corrective action before work continues.",
            rag_hits,
        )
    return _base_card(
        route,
        "hazard_monitoring",
        "low",
        "operator",
        f"Record no visible high-risk hazard in {area_id}; continue normal checks without granting safety clearance.",
        rag_hits,
    )
