"""OpenRouter `Pi` factory: OpenAI-compatible endpoint, one pi per model."""

from __future__ import annotations

import os
from typing import Dict, Optional

from ..datagen.samplers import Pi
from ..datagen.utils import make_openai_pi

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# OpenRouter's unified reasoning parameter (https://openrouter.ai/docs).
# Every level is sent as {"reasoning": {"effort": ...}}; "none" is the effort
# level that disables reasoning tokens (e.g. on openai/gpt-5.6-sol).
# "default" -> omit the parameter entirely (provider default).
REASONING_CHOICES = ("default", "none", "minimal", "low", "medium", "high")


def reasoning_extra_body(reasoning: str) -> Optional[dict]:
    """Map a --reasoning flag value to the OpenRouter ``extra_body`` payload."""
    if reasoning not in REASONING_CHOICES:
        raise ValueError(f"reasoning must be one of {REASONING_CHOICES}, got {reasoning!r}")
    if reasoning == "default":
        return None
    return {"reasoning": {"effort": reasoning}}


def make_openrouter_pi(
    model: str,
    temperature: float = 0.7,
    max_output_tokens: int = 256,
    max_retries: int = 4,
    api_key: str | None = None,
    reasoning: str = "default",
    provider: str | None = None,
    allow_fallbacks: bool = False,
    data_collection: str = "deny",
    request_timeout: float = 60.0,
    min_request_interval: float = 0.0,
) -> Pi:
    """`Pi` via OpenRouter's OpenAI-compatible endpoint; key from ``OPENROUTER_API_KEY``."""
    if api_key is None:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if api_key is None:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. Export it or pass api_key=... "
                "to make_openrouter_pi."
            )
    extra_body = reasoning_extra_body(reasoning) or {}
    provider_options: dict[str, object] = {
        "allow_fallbacks": allow_fallbacks,
        "data_collection": data_collection,
    }
    if provider:
        provider_options["order"] = [provider]
    extra_body["provider"] = provider_options
    return make_openai_pi(
        model=model,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        max_retries=max_retries,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        extra_body=extra_body,
        request_timeout=request_timeout,
        min_request_interval=min_request_interval,
    )


def make_openrouter_pis(
    models: list[str],
    temperature: float = 0.7,
    max_output_tokens: int = 256,
    max_retries: int = 4,
    api_key: str | None = None,
    reasoning: str = "default",
    provider: str | None = None,
    allow_fallbacks: bool = False,
    data_collection: str = "deny",
    request_timeout: float = 60.0,
    min_request_interval: float = 0.0,
) -> Dict[str, Pi]:
    """One `Pi` per unique model name, keyed by model name."""
    return {
        m: make_openrouter_pi(
            model=m,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            max_retries=max_retries,
            api_key=api_key,
            reasoning=reasoning,
            provider=provider,
            allow_fallbacks=allow_fallbacks,
            data_collection=data_collection,
            request_timeout=request_timeout,
            min_request_interval=min_request_interval,
        )
        for m in dict.fromkeys(models)
    }
