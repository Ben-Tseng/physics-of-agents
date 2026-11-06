"""Estimate live confirmatory cost from completed episode prompt lengths."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.datagen.samplers import OBJECTIVE_SPIN_INSTRUCTION, _objective_context


def inboxes(envelopes, n):
    routed = {name: [[] for _ in range(n)] for name in ("agree", "disagree", "unknown")}
    for envelope in envelopes:
        route = envelope["route"]
        if route in routed:
            routed[route][envelope["receiver"]].append(envelope["message"])
    return routed


def message_instruction(spin):
    letter = "A" if spin > 0 else "B"
    return (
        "# Instruction\n"
        f"Your current answer to the problem is {letter}. Write a brief message "
        f"to a fellow panelist stating that you favor option {letter} and giving "
        "the single strongest reason from your reasoning.\n"
        "## Response Format\n"
        "Respond only with a two-sentence message. Do not output anything else."
    )


def episode_characters(path):
    episode = json.loads(path.read_text())
    n = len(episode["personas"])
    k = episode["meta"]["k"]
    empty = {name: [[] for _ in range(n)] for name in ("agree", "disagree", "unknown")}
    current = empty
    input_chars = 0
    output_chars = n * k  # Initial A/B samples.

    for agent, persona in enumerate(episode["personas"]):
        prompt = _objective_context(
            persona, episode["statement"], episode["choices"], [], [], []
        ) + OBJECTIVE_SPIN_INSTRUCTION
        input_chars += k * len(prompt)

    for step, envelopes in enumerate(episode["envelope_history"]):
        messages = {}
        for key, value in episode["messages_history"][step].items():
            sender = int(key.split(",", 1)[0])
            messages[sender] = value
        for sender, message in messages.items():
            prompt = _objective_context(
                episode["personas"][sender], episode["statement"], episode["choices"],
                current["agree"][sender], current["disagree"][sender],
                current["unknown"][sender],
            ) + message_instruction(episode["spins_history"][step][sender])
            input_chars += len(prompt)
            output_chars += len(message)

        current = inboxes(envelopes, n)
        for agent, persona in enumerate(episode["personas"]):
            prompt = _objective_context(
                persona, episode["statement"], episode["choices"],
                current["agree"][agent], current["disagree"][agent],
                current["unknown"][agent],
            ) + OBJECTIVE_SPIN_INSTRUCTION
            input_chars += k * len(prompt)
            output_chars += k
    return input_chars, output_chars


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--target-episodes", type=int, required=True)
    parser.add_argument("--input-price", type=float, default=0.10,
                        help="USD per million input tokens")
    parser.add_argument("--output-price", type=float, default=0.15,
                        help="USD per million output tokens")
    args = parser.parse_args()
    paths = sorted(
        path for path in args.input.rglob("*.json") if path.name != "manifest.json"
    )
    totals = [episode_characters(path) for path in paths]
    input_chars = sum(value[0] for value in totals)
    output_chars = sum(value[1] for value in totals)
    scale = args.target_episodes / len(paths)
    estimates = {}
    for chars_per_token in (3.5, 4.0, 4.5):
        input_tokens = input_chars / chars_per_token * scale
        output_tokens = output_chars / chars_per_token * scale
        cost = (
            input_tokens * args.input_price / 1_000_000
            + output_tokens * args.output_price / 1_000_000
        )
        estimates[str(chars_per_token)] = {
            "input_tokens": round(input_tokens),
            "output_tokens": round(output_tokens),
            "estimated_usd": round(cost, 4),
        }
    print(json.dumps({
        "source_episodes": len(paths),
        "target_episodes": args.target_episodes,
        "source_input_characters": input_chars,
        "source_output_characters": output_chars,
        "prices_per_million_tokens": {
            "input": args.input_price, "output": args.output_price,
        },
        "estimates_by_characters_per_token": estimates,
    }, indent=2))


if __name__ == "__main__":
    main()
