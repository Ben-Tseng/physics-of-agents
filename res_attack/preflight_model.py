"""Run a small, bounded provider/model connectivity check."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.datagen_frontier.openrouter import make_openrouter_pi
from lib.datagen_frontier.mistral import make_mistral_pi
from lib.datagen_attack.collect_pilot import load_local_key


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("openrouter", "mistral"), default="openrouter")
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider", default="DeepInfra")
    parser.add_argument("--calls", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    if args.backend == "mistral":
        load_local_key(variable="MISTRAL_API_KEY")
        pi = make_mistral_pi(
            model=args.model, temperature=0.0, max_output_tokens=8,
            max_retries=0, request_timeout=args.timeout,
        )
    else:
        load_local_key(variable="OPENROUTER_API_KEY")
        pi = make_openrouter_pi(
            model=args.model,
            temperature=0.0,
            max_output_tokens=8,
            max_retries=0,
            reasoning="none",
            provider=args.provider,
            allow_fallbacks=False,
            data_collection="deny",
            request_timeout=args.timeout,
        )
    results = []
    for index in range(args.calls):
        started = time.monotonic()
        try:
            reply = pi("Reply with exactly: READY")
            results.append(
                {
                    "call": index + 1,
                    "ok": reply.strip().upper() == "READY",
                    "seconds": round(time.monotonic() - started, 3),
                    "reply": reply.strip(),
                }
            )
        except Exception as exc:
            results.append(
                {
                    "call": index + 1,
                    "ok": False,
                    "seconds": round(time.monotonic() - started, 3),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    print(json.dumps(results, indent=2))
    if not all(result["ok"] for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
