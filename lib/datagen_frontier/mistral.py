"""Mistral AI `Pi` factory using the official OpenAI-compatible API."""

from __future__ import annotations

import os

from ..datagen.samplers import Pi
from ..datagen.utils import make_openai_pi

MISTRAL_BASE_URL = "https://api.mistral.ai/v1"


def make_mistral_pi(
    model: str = "mistral-small-2603",
    temperature: float = 0.7,
    max_output_tokens: int = 256,
    max_retries: int = 0,
    api_key: str | None = None,
    request_timeout: float = 60.0,
    min_request_interval: float = 0.0,
) -> Pi:
    """Create a `Pi` for a version-pinned model on Mistral's official API."""
    if api_key is None:
        api_key = os.environ.get("MISTRAL_API_KEY")
        if api_key is None:
            raise RuntimeError(
                "MISTRAL_API_KEY is not set. Export it or pass api_key=... "
                "to make_mistral_pi."
            )
    return make_openai_pi(
        model=model,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        max_retries=max_retries,
        base_url=MISTRAL_BASE_URL,
        api_key=api_key,
        request_timeout=request_timeout,
        min_request_interval=min_request_interval,
    )
