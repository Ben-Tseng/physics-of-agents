"""Alibaba Cloud Model Studio (DashScope) OpenAI-compatible `Pi` factory."""

from __future__ import annotations

import os

from ..datagen.samplers import Pi
from ..datagen.utils import make_openai_pi


def make_dashscope_pi(
    model: str = "qwen3.5-27b",
    temperature: float = 0.7,
    max_output_tokens: int = 256,
    max_retries: int = 0,
    api_key: str | None = None,
    base_url: str | None = None,
    request_timeout: float = 60.0,
    min_request_interval: float = 0.0,
    enable_thinking: bool = False,
) -> Pi:
    """Create a `Pi` for a workspace-dedicated Model Studio endpoint."""
    if api_key is None:
        api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "DASHSCOPE_API_KEY is not set. Export it or pass api_key=..."
        )
    if base_url is None:
        base_url = os.environ.get("DASHSCOPE_BASE_URL")
    if not base_url:
        raise RuntimeError(
            "DASHSCOPE_BASE_URL is not set. Use the workspace-dedicated "
            "OpenAI-compatible base URL ending in /compatible-mode/v1."
        )
    return make_openai_pi(
        model=model,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        max_retries=max_retries,
        base_url=base_url.rstrip("/"),
        api_key=api_key,
        extra_body={"enable_thinking": enable_thinking},
        request_timeout=request_timeout,
        min_request_interval=min_request_interval,
    )
