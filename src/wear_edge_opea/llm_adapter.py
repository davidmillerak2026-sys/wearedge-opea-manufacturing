from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import time
import urllib.error
import urllib.request

from .agents import AgentRoute
from .llm_stub import explain as deterministic_explain


OPENAI_COMPATIBLE_BACKENDS = {"openai", "openai-compatible", "opea", "opea-compatible"}


@dataclass(frozen=True)
class LLMResult:
    text: str
    backend: str
    model: str
    latency_ms: float
    service_url: str
    fallback_used: bool
    claim_status: str
    error: str | None = None

    def to_metadata(self) -> dict:
        return asdict(self)


def configured_backend() -> str:
    return os.getenv("WEAREDGE_LLM_BACKEND", "deterministic").strip().lower() or "deterministic"


def configured_model() -> str:
    return os.getenv("WEAREDGE_LLM_MODEL", "manufacturing-action-card-adapter")


def configured_url() -> str:
    explicit_url = os.getenv("WEAREDGE_LLM_URL", "").strip()
    if explicit_url:
        return explicit_url

    base_url = os.getenv("WEAREDGE_LLM_BASE_URL", os.getenv("OPENAI_BASE_URL", "")).strip().rstrip("/")
    if not base_url:
        return ""
    if base_url.endswith("/v1"):
        return f"{base_url}/chat/completions"
    return f"{base_url}/v1/chat/completions"


def build_prompt(
    route: AgentRoute,
    entity_id: str,
    observation: str,
    rag_hits: list[dict],
    evaluation: dict,
) -> str:
    source_ids = [
        hit.get("payload", {}).get("id", "unknown")
        for hit in rag_hits
        if hit.get("payload")
    ]
    source_lines = [
        f"- {hit.get('payload', {}).get('id', 'unknown')}: {hit.get('payload', {}).get('content', '')}"
        for hit in rag_hits
        if hit.get("payload")
    ]
    return "\n".join(
        [
            f"Agent mode: {route.mode}",
            f"Agent name: {route.name}",
            f"Entity: {entity_id}",
            f"Integration target: {route.integration_target}",
            f"Business value: {route.business_value}",
            f"Operator observation: {observation}",
            f"Accepted evidence flags: {evaluation.get('breach_count', 0)}",
            f"Risk level: {evaluation.get('risk_level', 'unknown')}",
            f"Retrieved source IDs: {', '.join(source_ids) or 'none'}",
            "Retrieved evidence:",
            *source_lines,
            "",
            "Write one concise manufacturing action-card explanation.",
            "Preserve source IDs, avoid unsupported final decisions, and keep restricted claims human-confirmed.",
        ]
    )


def _post_json(url: str, payload: dict, timeout: float) -> dict:
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("WEAREDGE_LLM_API_KEY", os.getenv("OPENAI_API_KEY", "")).strip()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _extract_text(body: dict) -> str:
    choices = body.get("choices")
    if isinstance(choices, list) and choices:
        choice = choices[0]
        message = choice.get("message") if isinstance(choice, dict) else None
        if isinstance(message, dict) and message.get("content"):
            return str(message["content"])
        if isinstance(choice, dict) and choice.get("text"):
            return str(choice["text"])

    if body.get("text"):
        return str(body["text"])
    if body.get("generated_text"):
        return str(body["generated_text"])
    raise ValueError("LLM response did not contain text")


def _deterministic_result(
    route: AgentRoute,
    entity_id: str,
    observation: str,
    rag_hits: list[dict],
    evaluation: dict,
    *,
    start: float,
    fallback_used: bool = False,
    error: str | None = None,
) -> LLMResult:
    return LLMResult(
        text=deterministic_explain(route, entity_id, observation, rag_hits, evaluation),
        backend="deterministic",
        model="deterministic-action-card-template",
        latency_ms=round((time.perf_counter() - start) * 1000, 2),
        service_url="in-process",
        fallback_used=fallback_used,
        claim_status="deterministic_llm_adapter_contract",
        error=error,
    )


def generate_explanation(
    route: AgentRoute,
    entity_id: str,
    observation: str,
    rag_hits: list[dict],
    evaluation: dict,
) -> LLMResult:
    start = time.perf_counter()
    backend = configured_backend()
    if backend in {"deterministic", "stub", "template"}:
        return _deterministic_result(route, entity_id, observation, rag_hits, evaluation, start=start)

    if backend not in OPENAI_COMPATIBLE_BACKENDS:
        if os.getenv("WEAREDGE_LLM_STRICT", "").lower() == "true":
            raise ValueError(f"Unsupported WEAREDGE_LLM_BACKEND={backend}")
        return _deterministic_result(
            route,
            entity_id,
            observation,
            rag_hits,
            evaluation,
            start=start,
            fallback_used=True,
            error=f"unsupported backend: {backend}",
        )

    url = configured_url()
    if not url:
        if os.getenv("WEAREDGE_LLM_STRICT", "").lower() == "true":
            raise ValueError("WEAREDGE_LLM_URL or WEAREDGE_LLM_BASE_URL is required for OpenAI-compatible LLM")
        return _deterministic_result(
            route,
            entity_id,
            observation,
            rag_hits,
            evaluation,
            start=start,
            fallback_used=True,
            error="missing LLM service URL",
        )

    model = configured_model()
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an OPEA manufacturing action-card explanation service. "
                    "Return concise, source-grounded text. Do not grant restart, release, "
                    "final root-cause, safety-clearance, or quality-disposition authority."
                ),
            },
            {"role": "user", "content": build_prompt(route, entity_id, observation, rag_hits, evaluation)},
        ],
        "temperature": float(os.getenv("WEAREDGE_LLM_TEMPERATURE", "0")),
        "max_tokens": int(os.getenv("WEAREDGE_LLM_MAX_TOKENS", "160")),
    }

    try:
        body = _post_json(url, payload, timeout=float(os.getenv("WEAREDGE_LLM_TIMEOUT", "30")))
        text = _extract_text(body)
        return LLMResult(
            text=text,
            backend=backend,
            model=model,
            latency_ms=round((time.perf_counter() - start) * 1000, 2),
            service_url=url,
            fallback_used=False,
            claim_status="production_llm_endpoint_used",
        )
    except (OSError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        if os.getenv("WEAREDGE_LLM_STRICT", "").lower() == "true":
            raise
        return _deterministic_result(
            route,
            entity_id,
            observation,
            rag_hits,
            evaluation,
            start=start,
            fallback_used=True,
            error=str(exc),
        )


def explain(route: AgentRoute, entity_id: str, observation: str, rag_hits: list[dict], evaluation: dict) -> str:
    return generate_explanation(route, entity_id, observation, rag_hits, evaluation).text
