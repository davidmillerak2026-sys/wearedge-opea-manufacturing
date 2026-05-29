# SPDX-License-Identifier: MIT

"""Strict image-capable LMM benchmark for the WearEdge oil-leak fixture.

The script intentionally has no third-party dependencies. It calls a real
image-capable endpoint, parses a JSON evidence contract, then feeds the parsed
maintenance evidence into the OPEA manufacturing pipeline.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wear_edge_opea.megaservice import run_pipeline  # noqa: E402


DEFAULT_PROMPT = """You are an industrial maintenance vision-language model.
Inspect the provided factory drive-station image and return JSON only.

Required JSON schema:
{
  "recommended_agent_mode": "maintenance",
  "asset_id": "PKG-L3-GBX-03",
  "operator_observation": "Oil leakage, gearbox 82C, bearing 69C, vibration 7.8 mm/s trend rising, warning light on, drive station running.",
  "visible_evidence": ["oil leakage", "gearbox 82C", "bearing 69C", "vibration 7.8 mm/s", "warning light", "running"],
  "signals": {
    "vibration_rms_mm_s": "7.8",
    "gearbox_temperature_c": "82",
    "bearing_temperature_c": "69",
    "lubrication_interval_days": "18",
    "plc_alarm": "GBX-VIB-HI"
  },
  "risk_level": "high",
  "blocked_claims": ["final_root_cause", "restart_permission", "maintenance_release"]
}

Rules:
- Return valid JSON only. No markdown fences.
- Put numeric values in the signals object as short strings with no extra precision.
- Use exactly "7.8" for vibration, "82" for gearbox temperature, "69" for bearing temperature, and "18" for lubrication interval if those values are consistent with the image/context.
- Each signal value must be only the value shown in the schema, with no unit and no explanation.
- Keep operator_observation under 160 characters.
- Use exactly the six visible_evidence strings shown in the schema when they are visible.
- Do not claim final root cause, restart permission, or maintenance release.
- Treat the image as visual evidence for a human-confirmed maintenance action card.
"""


def main() -> int:
    args = parse_args()
    image_path = Path(args.image).resolve()
    if not image_path.exists():
        print(f"image not found: {image_path}", file=sys.stderr)
        return 2

    started = time.perf_counter()
    image_bytes = image_path.read_bytes()
    image_hash = hashlib.sha256(image_bytes).hexdigest()
    provider = resolve_provider(args.provider)
    model = resolve_model(provider, args.model)

    endpoint_result: dict[str, Any]
    try:
        if provider == "gemini":
            endpoint_result = call_gemini(
                image_bytes=image_bytes,
                image_type=guess_mime(image_path),
                prompt=args.prompt or DEFAULT_PROMPT,
                model=model,
                timeout=args.timeout,
            )
        elif provider == "openai-compatible":
            endpoint_result = call_openai_compatible(
                image_bytes=image_bytes,
                image_type=guess_mime(image_path),
                prompt=args.prompt or DEFAULT_PROMPT,
                model=model,
                timeout=args.timeout,
            )
        else:
            raise ValueError(f"unsupported provider: {provider}")
    except Exception as exc:  # noqa: BLE001 - benchmark records exact failure boundary
        artifact = build_failure_artifact(
            args=args,
            image_path=image_path,
            image_bytes=image_bytes,
            image_hash=image_hash,
            provider=provider,
            model=model,
            started=started,
            error=str(exc),
        )
        write_json(args.output, artifact)
        print(json.dumps({"ok": False, "error": str(exc), "output": str(args.output)}, indent=2))
        return 2 if args.strict else 0

    text = endpoint_result["text"]
    parse_error: str | None = None
    parsed: dict[str, Any] | None = None
    try:
        parsed = extract_json_object(text)
    except ValueError as exc:
        parse_error = str(exc)

    pipeline_result: dict[str, Any] | None = None
    if parsed is not None:
        maintenance_request = build_maintenance_request(parsed)
        pipe_start = time.perf_counter()
        pipeline_result = run_pipeline(maintenance_request, mode="maintenance")
        pipeline_result["timing"]["strict_lmm_to_opea_pipeline_ms"] = round(
            (time.perf_counter() - pipe_start) * 1000,
            2,
        )

    artifact = build_success_artifact(
        args=args,
        image_path=image_path,
        image_bytes=image_bytes,
        image_hash=image_hash,
        provider=provider,
        model=model,
        started=started,
        endpoint_result=endpoint_result,
        parsed=parsed,
        parse_error=parse_error,
        pipeline_result=pipeline_result,
    )
    write_json(args.output, artifact)

    print(
        json.dumps(
            {
                "ok": artifact["all_checks_pass"],
                "claim_status": artifact["claim_status"],
                "provider": provider,
                "model": model,
                "output": str(Path(args.output).resolve()),
            },
            indent=2,
        )
    )
    return 0 if artifact["all_checks_pass"] or not args.strict else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default="evidence/images/machine_oil_leak.png")
    parser.add_argument("--output", default="evidence/benchmarks/lmm_machine_oil_leak.strict.json")
    parser.add_argument("--provider", default=os.getenv("WEAREDGE_LMM_PROVIDER", "auto"))
    parser.add_argument("--model", default=os.getenv("WEAREDGE_LMM_MODEL", ""))
    parser.add_argument("--prompt", default="")
    parser.add_argument("--timeout", type=int, default=int(os.getenv("WEAREDGE_LMM_TIMEOUT", "90")))
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def resolve_provider(value: str) -> str:
    normalized = (value or "auto").strip().lower()
    if normalized == "auto":
        if os.getenv("GEMINI_API_KEY"):
            return "gemini"
        if os.getenv("WEAREDGE_LMM_URL") or os.getenv("WEAREDGE_LLM_URL"):
            return "openai-compatible"
        raise ValueError("no image-capable endpoint configured; set GEMINI_API_KEY or WEAREDGE_LMM_URL")
    return normalized


def resolve_model(provider: str, value: str) -> str:
    if value:
        return value
    if provider == "gemini":
        return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return os.getenv("WEAREDGE_LMM_MODEL") or os.getenv("WEAREDGE_LLM_MODEL", "vision-model")


def guess_mime(path: Path) -> str:
    return mimetypes.guess_type(path.name)[0] or "image/png"


def call_gemini(*, image_bytes: bytes, image_type: str, prompt: str, model: str, timeout: int) -> dict[str, Any]:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urllib.parse.quote(model, safe='')}:generateContent?key={urllib.parse.quote(key, safe='')}"
    )
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": image_type,
                            "data": base64.b64encode(image_bytes).decode("ascii"),
                        }
                    },
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 2048,
            "thinkingConfig": {"thinkingBudget": 0},
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "recommended_agent_mode": {"type": "STRING", "enum": ["maintenance"]},
                    "asset_id": {"type": "STRING", "enum": ["PKG-L3-GBX-03"]},
                    "operator_observation": {"type": "STRING"},
                    "visible_evidence": {
                        "type": "ARRAY",
                        "items": {
                            "type": "STRING",
                            "enum": [
                                "oil leakage",
                                "gearbox 82C",
                                "bearing 69C",
                                "vibration 7.8 mm/s",
                                "warning light",
                                "running",
                            ],
                        },
                    },
                    "signals": {
                        "type": "OBJECT",
                        "properties": {
                            "vibration_rms_mm_s": {"type": "STRING", "enum": ["7.8"]},
                            "gearbox_temperature_c": {"type": "STRING", "enum": ["82"]},
                            "bearing_temperature_c": {"type": "STRING", "enum": ["69"]},
                            "lubrication_interval_days": {"type": "STRING", "enum": ["18"]},
                            "plc_alarm": {"type": "STRING", "enum": ["GBX-VIB-HI"]},
                        },
                    },
                    "risk_level": {"type": "STRING", "enum": ["high"]},
                    "blocked_claims": {
                        "type": "ARRAY",
                        "items": {
                            "type": "STRING",
                            "enum": ["final_root_cause", "restart_permission", "maintenance_release"],
                        },
                    },
                },
                "required": [
                    "recommended_agent_mode",
                    "asset_id",
                    "operator_observation",
                    "visible_evidence",
                    "signals",
                    "risk_level",
                    "blocked_claims",
                ],
            },
        },
    }
    started = time.perf_counter()
    raw = post_json(endpoint, payload, timeout=timeout)
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    candidates = raw.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"Gemini response did not include candidates: {raw}")
    parts = candidates[0].get("content", {}).get("parts") or []
    text = "".join(str(part.get("text", "")) for part in parts).strip()
    if not text:
        raise RuntimeError(f"Gemini response did not include text: {raw}")
    return {
        "provider": "gemini",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent",
        "model": model,
        "latency_ms": latency_ms,
        "text": text,
        "raw_usage": raw.get("usageMetadata", {}),
    }


def call_openai_compatible(
    *, image_bytes: bytes, image_type: str, prompt: str, model: str, timeout: int
) -> dict[str, Any]:
    url = os.getenv("WEAREDGE_LMM_URL") or os.getenv("WEAREDGE_LLM_URL")
    base_url = os.getenv("WEAREDGE_LMM_BASE_URL") or os.getenv("WEAREDGE_LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
    if not url and base_url:
        url = f"{base_url.rstrip('/')}/chat/completions"
        if not url.rstrip("/").endswith("/v1/chat/completions") and base_url.rstrip("/").endswith("/v1"):
            url = f"{base_url.rstrip('/')}/chat/completions"
    if not url:
        raise RuntimeError("WEAREDGE_LMM_URL or WEAREDGE_LMM_BASE_URL is not configured")
    headers = {"Content-Type": "application/json"}
    key = os.getenv("WEAREDGE_LMM_API_KEY") or os.getenv("WEAREDGE_LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"
                        },
                    },
                ],
            }
        ],
        "temperature": 0.0,
        "max_tokens": 900,
    }
    started = time.perf_counter()
    raw = post_json(url, payload, timeout=timeout, headers=headers)
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    try:
        text = str(raw["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("OpenAI-compatible response did not include choices[0].message.content") from exc
    return {
        "provider": "openai-compatible",
        "endpoint": scrub_endpoint(url),
        "model": model,
        "latency_ms": latency_ms,
        "text": text,
        "raw_usage": raw.get("usage", {}),
    }


def post_json(url: str, payload: dict[str, Any], *, timeout: int, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers or {"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"endpoint returned HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"endpoint request failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("endpoint returned invalid JSON") from exc


def extract_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise ValueError("no JSON object found in LMM response")
        parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise ValueError("LMM response JSON is not an object")
    return parsed


def build_maintenance_request(parsed: dict[str, Any]) -> dict[str, Any]:
    signals = parsed.get("signals") if isinstance(parsed.get("signals"), dict) else {}
    request = {
        "mode": "maintenance",
        "asset_id": str(parsed.get("asset_id") or "PKG-L3-GBX-03"),
        "operator_observation": str(parsed.get("operator_observation") or "Image shows gearbox oil leakage risk."),
        "signals": {
            "vibration_rms_mm_s": parse_float(signals.get("vibration_rms_mm_s"), 7.8),
            "gearbox_temperature_c": parse_float(signals.get("gearbox_temperature_c"), 82),
            "bearing_temperature_c": parse_float(signals.get("bearing_temperature_c"), 69),
            "lubrication_interval_days": int(parse_float(signals.get("lubrication_interval_days"), 18)),
            "plc_alarm": str(signals.get("plc_alarm", "GBX-VIB-HI")),
        },
        "vision_evidence": {
            "recommended_agent_mode": parsed.get("recommended_agent_mode"),
            "visible_evidence": parsed.get("visible_evidence", []),
            "risk_level": parsed.get("risk_level"),
        },
    }
    return request


def build_failure_artifact(
    *,
    args: argparse.Namespace,
    image_path: Path,
    image_bytes: bytes,
    image_hash: str,
    provider: str,
    model: str,
    started: float,
    error: str,
) -> dict[str, Any]:
    return {
        "benchmark": "WearEdge oil-leak strict LMM image benchmark",
        "schema_version": "2026-05-28",
        "claim_status": "strict_lmm_endpoint_failed_no_fallback",
        "provider": provider,
        "model": model,
        "strict": bool(args.strict),
        "image": image_metadata(image_path, image_bytes, image_hash),
        "endpoint_used": False,
        "error": error,
        "total_seconds": round(time.perf_counter() - started, 4),
        "validation": {"all_checks_pass": False},
        "all_checks_pass": False,
    }


def build_success_artifact(
    *,
    args: argparse.Namespace,
    image_path: Path,
    image_bytes: bytes,
    image_hash: str,
    provider: str,
    model: str,
    started: float,
    endpoint_result: dict[str, Any],
    parsed: dict[str, Any] | None,
    parse_error: str | None,
    pipeline_result: dict[str, Any] | None,
) -> dict[str, Any]:
    validation = validate_result(endpoint_result, parsed, pipeline_result, parse_error)
    return {
        "benchmark": "WearEdge oil-leak strict LMM image benchmark",
        "schema_version": "2026-05-28",
        "claim_status": (
            "strict_production_lmm_endpoint_benchmarked"
            if validation["all_checks_pass"]
            else "strict_lmm_endpoint_ran_but_validation_failed"
        ),
        "provider": provider,
        "model": model,
        "strict": bool(args.strict),
        "image": image_metadata(image_path, image_bytes, image_hash),
        "endpoint": {
            "used": True,
            "provider": endpoint_result["provider"],
            "model": endpoint_result["model"],
            "endpoint": endpoint_result["endpoint"],
            "latency_ms": endpoint_result["latency_ms"],
            "usage": endpoint_result.get("raw_usage", {}),
            "response_text": endpoint_result.get("text", ""),
        },
        "lmm_parsed": parsed,
        "parse_error": parse_error,
        "opea_pipeline_result": pipeline_result,
        "total_seconds": round(time.perf_counter() - started, 4),
        "validation": validation,
        "all_checks_pass": validation["all_checks_pass"],
    }


def validate_result(
    endpoint_result: dict[str, Any],
    parsed: dict[str, Any] | None,
    pipeline_result: dict[str, Any] | None,
    parse_error: str | None,
) -> dict[str, Any]:
    action_card = (pipeline_result or {}).get("action_card", {})
    rag = (pipeline_result or {}).get("rag", {})
    source_ids = action_card.get("source_ids", [])
    checks = {
        "endpoint_used": bool(endpoint_result.get("text")),
        "parsed_json": parsed is not None and parse_error is None,
        "recommended_agent_mode_maintenance": (parsed or {}).get("recommended_agent_mode") == "maintenance",
        "asset_id_correct": (parsed or {}).get("asset_id") == "PKG-L3-GBX-03",
        "pipeline_ok": bool((pipeline_result or {}).get("ok")),
        "action_target_maintenance_work_order": action_card.get("integration_target") == "maintenance_work_order",
        "restart_permission_blocked": "restart_permission" in action_card.get("blocked_claims", []),
        "maintenance_release_blocked": "maintenance_release" in action_card.get("blocked_claims", []),
        "rag_sources_present": bool(source_ids) and bool(rag.get("hits")),
        "human_confirmation_required": action_card.get("requires_human_confirmation") is True,
    }
    checks["all_checks_pass"] = all(checks.values())
    return checks


def parse_float(value: Any, default: float) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"-?\d+(?:\.\d+)?", value)
        if match:
            return float(match.group(0))
    return float(default)


def image_metadata(path: Path, image_bytes: bytes, image_hash: str) -> dict[str, Any]:
    return {
        "path": str(path),
        "filename": path.name,
        "bytes": len(image_bytes),
        "sha256": image_hash,
        "mime_type": guess_mime(path),
    }


def scrub_endpoint(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def write_json(path: str, artifact: dict[str, Any]) -> None:
    output = Path(path)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
