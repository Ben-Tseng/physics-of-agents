"""DeepInfra `Pi` factory using its OpenAI-compatible API."""

from __future__ import annotations

import os

from ..datagen.samplers import Pi
from ..datagen.utils import make_openai_pi

DEEPINFRA_BASE_URL = "https://api.deepinfra.com/v1/openai"


def make_deepinfra_pi(
    model: str = "Qwen/Qwen3.5-9B",
    temperature: float = 0.7,
    max_output_tokens: int = 256,
    max_retries: int = 0,
    api_key: str | None = None,
    request_timeout: float = 60.0,
    min_request_interval: float = 0.0,
    reasoning_effort: str = "none",
    service_tier: str | None = None,
    fail_fast: bool = False,
) -> Pi:
    """Create a `Pi` that calls DeepInfra directly, bypassing OpenRouter."""
    if api_key is None:
        api_key = os.environ.get("DEEPINFRA_API_KEY")
        if api_key is None:
            raise RuntimeError(
                "DEEPINFRA_API_KEY is not set. Export it or pass api_key=... "
                "to make_deepinfra_pi."
            )
    extra_body: dict[str, object] = {"reasoning_effort": reasoning_effort}
    if service_tier is not None:
        extra_body["service_tier"] = service_tier
    if fail_fast:
        extra_body["fail_fast"] = True
    return make_openai_pi(
        model=model,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        max_retries=max_retries,
        base_url=DEEPINFRA_BASE_URL,
        api_key=api_key,
        extra_body=extra_body,
        request_timeout=request_timeout,
        min_request_interval=min_request_interval,
    )
