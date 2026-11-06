"""Concrete `Pi` (language-model) factories: OpenAI, Together, mock."""

from __future__ import annotations

import hashlib
import os
import threading
import time

from .samplers import Pi

TOGETHER_BASE_URL = "https://api.together.xyz/v1"


def make_openai_pi(
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_output_tokens: int = 256,
    max_retries: int = 4,
    base_url: str | None = None,
    api_key: str | None = None,
    extra_body: dict | None = None,
    request_timeout: float | None = None,
    min_request_interval: float = 0.0,
) -> Pi:
    """`Pi` via the OpenAI chat-completions API (or any compatible ``base_url``),
    with exponential-backoff retries; key defaults to ``OPENAI_API_KEY``."""
    from openai import APIConnectionError, APIError, OpenAI, RateLimitError

    client_kwargs: dict[str, object] = {}
    if base_url is not None:
        client_kwargs["base_url"] = base_url
    if api_key is not None:
        client_kwargs["api_key"] = api_key
    elif "OPENAI_API_KEY" not in os.environ:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it or pass api_key=... to make_openai_pi."
        )
    if request_timeout is not None:
        client_kwargs["timeout"] = request_timeout
        # Keep retry behavior in the explicit loop below so latency and attempts
        # are bounded and auditable rather than multiplied by SDK retries.
        client_kwargs["max_retries"] = 0
    client = OpenAI(**client_kwargs)
    if min_request_interval < 0:
        raise ValueError("minimum request interval must be nonnegative")
    schedule_lock = threading.Lock()
    next_request_start = [0.0]

    def wait_for_request_slot() -> None:
        if min_request_interval == 0:
            return
        with schedule_lock:
            now = time.monotonic()
            start = max(now, next_request_start[0])
            next_request_start[0] = start + min_request_interval
        delay = start - now
        if delay > 0:
            time.sleep(delay)

    def pi(prompt: str) -> str:
        last_exc: Exception | None = None
        for attempt in range(max_retries + 1):
            try:
                wait_for_request_slot()
                resp = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_output_tokens,
                    **({"extra_body": extra_body} if extra_body else {}),
                )
                return resp.choices[0].message.content or ""
            except (RateLimitError, APIConnectionError, APIError) as exc:
                last_exc = exc
                if attempt == max_retries:
                    break
                time.sleep(2.0 ** attempt)
        raise RuntimeError(f"OpenAI call failed after {max_retries} retries: {last_exc}")

    return pi


def make_together_pi(
    model: str = "meta-llama/Meta-Llama-3-8B-Instruct-Lite",
    temperature: float = 0.7,
    max_output_tokens: int = 256,
    max_retries: int = 4,
    api_key: str | None = None,
    extra_body: dict | None = None,
) -> Pi:
    """`Pi` via Together's OpenAI-compatible endpoint; key from ``TOGETHER_API_KEY``."""
    if api_key is None:
        api_key = os.environ.get("TOGETHER_API_KEY")
        if api_key is None:
            raise RuntimeError(
                "TOGETHER_API_KEY is not set. Export it or pass api_key=... "
                "to make_together_pi."
            )
    return make_openai_pi(
        model=model,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        max_retries=max_retries,
        base_url=TOGETHER_BASE_URL,
        api_key=api_key,
        extra_body=extra_body,
    )


def make_mock_pi(seed: int = 0) -> Pi:
    """Deterministic offline `Pi` for smoke tests (hash-based answers, canned message)."""
    salt = f"mock-pi-{seed}".encode()

    def pi(prompt: str) -> str:
        h = hashlib.sha256(salt + prompt.encode()).digest()
        if "two-sentence message" in prompt:
            return (
                "Speaking for my persona, here is how I see the statement. "
                "The considerations that matter most to me point in a clear direction."
            )
        # "A or B" is the sentinel in OBJECTIVE_SPIN_INSTRUCTION (samplers.py).
        if "A or B" in prompt:
            return "A" if h[0] & 1 else "B"
        return "AGREE" if h[0] & 1 else "DISAGREE"

    return pi
