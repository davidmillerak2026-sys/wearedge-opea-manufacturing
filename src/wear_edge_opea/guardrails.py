from __future__ import annotations


def build_action_card(asset_id: str, evaluation: dict, rag_hits: list[dict]) -> dict:
    has_identity = asset_id == "PKG-L3-GBX-03"
    risk_level = evaluation["risk_level"]
    source_ids = [hit["payload"].get("id") for hit in rag_hits if hit.get("payload")]

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

    return {
        "channel": channel,
        "priority": priority,
        "owner": "maintenance_engineer" if priority in {"high", "medium"} else "operator",
        "requires_human_confirmation": True,
        "integration_target": "maintenance_work_order",
        "action": action,
        "source_ids": source_ids,
        "blocked_claims": [
            "final_root_cause",
            "remaining_useful_life",
            "restart_permission",
            "maintenance_release",
        ],
    }

