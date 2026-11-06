"""Low-cost official-Mistral connectivity probe; no experiment data."""

from __future__ import annotations

import argparse
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from lib.datagen_attack.collect_pilot import load_local_key
from lib.datagen_frontier.mistral import make_mistral_pi


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="mistral-small-2603")
    parser.add_argument("--calls", type=int, default=20)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--interval", type=float, default=0.8)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.calls < 1 or args.workers < 1:
        raise ValueError("calls and workers must be positive")
    load_local_key(variable="MISTRAL_API_KEY")
    pi = make_mistral_pi(
        model=args.model,
        temperature=0.0,
        max_output_tokens=32,
        max_retries=0,
        request_timeout=args.timeout,
        min_request_interval=args.interval,
    )

    def one_call(index: int):
        started = time.monotonic()
        try:
            response = pi(
                f"Connectivity probe {index}. Reply with exactly the single letter A."
            )
            return {
                "index": index,
                "ok": bool(response.strip()),
                "latency_seconds": round(time.monotonic() - started, 3),
                "error_type": None if response.strip() else "empty_response",
            }
        except Exception as exc:
            return {
                "index": index,
                "ok": False,
                "latency_seconds": round(time.monotonic() - started, 3),
                "error_type": type(exc).__name__,
            }

    started = time.monotonic()
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(one_call, index) for index in range(args.calls)]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: item["index"])
    latencies = [item["latency_seconds"] for item in results]
    successes = sum(item["ok"] for item in results)
    report = {
        "kind": "mistral_connectivity_probe",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "backend": "official Mistral API",
        "calls": args.calls,
        "workers": args.workers,
        "request_timeout_seconds": args.timeout,
        "minimum_request_interval_seconds": args.interval,
        "api_retries": 0,
        "successes": successes,
        "failures": args.calls - successes,
        "success_rate": successes / args.calls,
        "wall_seconds": round(time.monotonic() - started, 3),
        "latency_seconds": {
            "median": round(statistics.median(latencies), 3),
            "maximum": round(max(latencies), 3),
        },
        "results": results,
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
