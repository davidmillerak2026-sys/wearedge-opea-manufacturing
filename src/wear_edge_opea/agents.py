# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


@dataclass(frozen=True)
class AgentRoute:
    mode: str
    name: str
    business_value: str
    entity_key: str
    integration_target: str
    owner: str
    human_gate: bool
    sample_request_path: Path
    kb_path: Path
    blocked_claims: tuple[str, ...]


ROUTES: dict[str, AgentRoute] = {
    "maintenance": AgentRoute(
        mode="maintenance",
        name="lao-shi-fu predictive maintenance",
        business_value="Reduce downtime by converting M400 evidence into CMMS-ready maintenance work-order proposals.",
        entity_key="asset_id",
        integration_target="maintenance_work_order",
        owner="maintenance_engineer",
        human_gate=True,
        sample_request_path=DATA / "sample_requests" / "maintenance.json",
        kb_path=DATA / "maintenance_kb" / "pkg_l3_gbx_03.json",
        blocked_claims=("final_root_cause", "remaining_useful_life", "restart_permission", "maintenance_release"),
    ),
    "iqc": AgentRoute(
        mode="iqc",
        name="incoming and in-process quality control",
        business_value="Reduce scrap and customer escapes by turning first-person defect evidence into QMS hold events.",
        entity_key="product_id",
        integration_target="qms_quality_event",
        owner="quality_engineer",
        human_gate=True,
        sample_request_path=DATA / "sample_requests" / "iqc.json",
        kb_path=DATA / "agent_kb" / "iqc_quality_plan.json",
        blocked_claims=("quality_release", "final_disposition", "customer_acceptance", "measurement_certification"),
    ),
    "changeover": AgentRoute(
        mode="changeover",
        name="SKU changeover verification",
        business_value="Reduce changeover loss and mix-up risk by validating released setup evidence before restart.",
        entity_key="machine_id",
        integration_target="changeover_checklist",
        owner="operator_quality",
        human_gate=True,
        sample_request_path=DATA / "sample_requests" / "changeover.json",
        kb_path=DATA / "agent_kb" / "changeover_sku_c500.json",
        blocked_claims=("restart_permission", "quality_release", "recipe_release", "first_piece_release"),
    ),
    "wi": AgentRoute(
        mode="wi",
        name="released work-instruction guidance",
        business_value="Reduce training time and procedure drift by guiding operators from released source instructions.",
        entity_key="machine_id",
        integration_target="wi_reference",
        owner="operator",
        human_gate=False,
        sample_request_path=DATA / "sample_requests" / "wi.json",
        kb_path=DATA / "agent_kb" / "wi_cartoner_st2.json",
        blocked_claims=("unreleased_instruction", "bypass_interlock", "quality_release", "restart_permission"),
    ),
    "hazard": AgentRoute(
        mode="hazard",
        name="EHS hazard observation",
        business_value="Reduce safety risk by converting near-miss scenes into bounded EHS action cards.",
        entity_key="area_id",
        integration_target="ehs_case",
        owner="operator",
        human_gate=True,
        sample_request_path=DATA / "sample_requests" / "hazard.json",
        kb_path=DATA / "agent_kb" / "hazard_policy.json",
        blocked_claims=("area_safe", "restart_permission", "safety_clearance", "incident_root_cause"),
    ),
}


def normalize_mode(mode: str | None) -> str:
    normalized = (mode or "maintenance").strip().lower().replace("_", "-")
    aliases = {
        "pm": "maintenance",
        "lao-shi-fu": "maintenance",
        "quality": "iqc",
        "change-over": "changeover",
        "work-instruction": "wi",
        "work_instruction": "wi",
        "safety": "hazard",
        "ehs": "hazard",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in ROUTES:
        raise ValueError(f"Unsupported agent mode: {mode}")
    return normalized


def get_route(mode: str | None) -> AgentRoute:
    return ROUTES[normalize_mode(mode)]


def list_agents() -> list[dict]:
    return [
        {
            **asdict(route),
            "sample_request_path": str(route.sample_request_path.relative_to(ROOT)),
            "kb_path": str(route.kb_path.relative_to(ROOT)),
            "blocked_claims": list(route.blocked_claims),
        }
        for route in ROUTES.values()
    ]


def load_sample_request(mode: str | None) -> dict:
    route = get_route(mode)
    return json.loads(route.sample_request_path.read_text(encoding="utf-8"))


def entity_id_for(route: AgentRoute, request: dict, kb: dict | None = None) -> str:
    if route.entity_key in request:
        return str(request[route.entity_key])
    if kb:
        return str(kb.get("asset_id") or kb.get("entity_id") or "unknown")
    return "unknown"
