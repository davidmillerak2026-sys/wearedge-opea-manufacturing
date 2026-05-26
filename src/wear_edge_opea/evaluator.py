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

