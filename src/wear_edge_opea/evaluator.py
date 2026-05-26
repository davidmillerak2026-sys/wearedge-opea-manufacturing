from __future__ import annotations


def evaluate_signals(signals: dict, thresholds: dict) -> dict:
    breaches: list[dict] = []

    checks = [
        ("vibration_rms_mm_s", "vibration_rms_mm_s_high", "mm/s"),
        ("gearbox_temperature_c", "gearbox_temperature_c_high", "C"),
        ("bearing_temperature_c", "bearing_temperature_c_high", "C"),
        ("lubrication_interval_days", "lubrication_interval_days_max", "days"),
    ]
    for signal_key, threshold_key, unit in checks:
        value = signals.get(signal_key)
        threshold = thresholds.get(threshold_key)
        if value is not None and threshold is not None and float(value) > float(threshold):
            breaches.append(
                {
                    "signal": signal_key,
                    "value": value,
                    "threshold": threshold,
                    "unit": unit,
                }
            )

    if signals.get("plc_alarm"):
        breaches.append(
            {
                "signal": "plc_alarm",
                "value": signals["plc_alarm"],
                "threshold": "no active gearbox vibration alarm",
                "unit": "alarm",
            }
        )

    risk_level = "low"
    if len(breaches) >= 4:
        risk_level = "high"
    elif len(breaches) >= 2:
        risk_level = "medium"

    return {
        "status": "breach_detected" if breaches else "within_bounds",
        "risk_level": risk_level,
        "breach_count": len(breaches),
        "breaches": breaches,
    }


def evaluate_request(mode: str, request: dict, thresholds: dict) -> dict:
    if mode == "maintenance":
        return evaluate_signals(request.get("signals", {}), thresholds)
    if mode == "iqc":
        return evaluate_iqc(request, thresholds)
    if mode == "changeover":
        return evaluate_changeover(request)
    if mode == "wi":
        return evaluate_wi(request)
    if mode == "hazard":
        return evaluate_hazard(request)
    raise ValueError(f"Unsupported evaluation mode: {mode}")


def evaluate_iqc(request: dict, thresholds: dict) -> dict:
    detector = request.get("detector", {})
    min_confidence = float(thresholds.get("detector_min_confidence", 0.62))
    defects = [
        {"defect": name, "confidence": confidence}
        for name, confidence in detector.items()
        if float(confidence) >= min_confidence
    ]
    critical = {item["defect"] for item in defects} & {"label_mismatch", "missing_feature"}
    risk_level = "high" if critical else "medium" if defects else "low"
    status = "defect_detected" if defects else "detector_clear"
    return {
        "status": status,
        "risk_level": risk_level,
        "breach_count": len(defects),
        "breaches": defects,
        "detector_min_confidence": min_confidence,
    }


def evaluate_changeover(request: dict) -> dict:
    confirmations = request.get("confirmations", {})
    required = ("line_clearance", "label_roll_match", "recipe_match", "first_piece_verified")
    missing = [name for name in required if confirmations.get(name) is not True]
    risk_level = "medium" if missing == ["first_piece_verified"] else "high" if missing else "low"
    return {
        "status": "verification_required" if missing else "ready_for_quality_signoff",
        "risk_level": risk_level,
        "breach_count": len(missing),
        "breaches": [{"confirmation": name, "required": True, "value": confirmations.get(name)} for name in missing],
        "required_confirmations": list(required),
    }


def evaluate_wi(request: dict) -> dict:
    confirmations = request.get("confirmations", {})
    missing = [
        name
        for name in ("machine_identity", "released_revision_visible", "guard_closed")
        if confirmations.get(name) is not True
    ]
    active_alarm = confirmations.get("active_alarm") is True
    risk_level = "high" if active_alarm else "medium" if missing else "low"
    breaches = [{"confirmation": name, "required": True, "value": confirmations.get(name)} for name in missing]
    if active_alarm:
        breaches.append({"confirmation": "active_alarm", "required": False, "value": True})
    return {
        "status": "stop_required" if active_alarm else "source_check_required" if missing else "guidance_ready",
        "risk_level": risk_level,
        "breach_count": len(breaches),
        "breaches": breaches,
    }


def evaluate_hazard(request: dict) -> dict:
    hazards = request.get("hazards", {})
    active = [name for name, value in hazards.items() if value is True]
    high_risk = {"moving_parts_exposure", "blocked_walkway", "missing_ppe"} & set(active)
    risk_level = "high" if len(high_risk) >= 2 else "medium" if active else "low"
    return {
        "status": "unsafe_condition" if active else "no_visible_hazard",
        "risk_level": risk_level,
        "breach_count": len(active),
        "breaches": [{"hazard": name, "value": True} for name in active],
    }
