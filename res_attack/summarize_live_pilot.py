"""Summarize authenticated live-model pilot runs without modifying raw data."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


FIELDS = [
    "model",
    "question_id",
    "condition",
    "seed",
    "defense",
    "attack_budget",
    "final_correct",
    "num_agents",
    "final_correct_fraction",
    "incorrect_terminal_majority",
    "final_margin",
    "raw_parse_failures",
    "raw_zero_spins",
    "spin_request_errors",
    "spin_parse_retries",
    "message_errors",
    "attacker_envelopes",
    "attacker_agree",
    "attacker_unknown",
    "attacker_drop",
    "invalid_honest_credentials",
]


def summarize_run(path: Path) -> dict:
    data = json.loads(path.read_text())
    meta = data["meta"]
    truth = int(data["truth"])
    final = data["spins_history"][-1]
    correct = sum(int(spin) == truth for spin in final)
    margin = sum(truth * int(spin) for spin in final) / len(final)

    raw_zeros = sum(
        int(spin) == 0
        for step in data["spins_raw_history"]
        for agent in step
        for spin in agent
    )
    spin_diagnostics = [
        item
        for step in data.get("spin_error_history", [])
        for item in step
    ]
    if "spin_error_history" in data:
        raw_failures = sum(
            item.get("kind") == "parse_failure" for item in spin_diagnostics
        )
        request_errors = sum(
            item.get("kind") == "request_error" for item in spin_diagnostics
        )
        parse_retries = sum(
            item.get("kind") == "parse_retry" for item in spin_diagnostics
        )
    else:
        # Legacy files did not distinguish parsing from request failures.
        raw_failures = raw_zeros
        request_errors = 0
        parse_retries = 0
    # One model-generated sender message is copied to every outgoing edge. Count
    # failed sender calls once per step rather than once per recipient edge.
    message_errors = 0
    for step in data["messages_history"]:
        failed_senders = {
            edge.split(",", 1)[0]
            for edge, message in step.items()
            if isinstance(message, str) and message.startswith("[error:")
        }
        message_errors += len(failed_senders)

    envelopes = [item for step in data["envelope_history"] for item in step]
    attackers = [item for item in envelopes if item["sender_type"] == "attacker"]
    routes = Counter(item["route"] for item in attackers)
    invalid_honest = sum(
        item["sender_type"] == "honest" and not item["credential_valid"]
        for item in envelopes
    )
    condition = path.parent.name.split("__", 1)[0]
    return {
        "model": meta["model"],
        "question_id": meta["name"].split("__", 1)[0],
        "condition": condition,
        "seed": meta["seed"],
        "defense": meta["defense"],
        "attack_budget": meta["attack_budget"],
        "final_correct": correct,
        "num_agents": len(final),
        "final_correct_fraction": f"{correct / len(final):.3f}",
        "incorrect_terminal_majority": int(correct < len(final) / 2),
        "final_margin": f"{margin:.3f}",
        "raw_parse_failures": raw_failures,
        "raw_zero_spins": raw_zeros,
        "spin_request_errors": request_errors,
        "spin_parse_retries": parse_retries,
        "message_errors": message_errors,
        "attacker_envelopes": len(attackers),
        "attacker_agree": routes["agree"],
        "attacker_unknown": routes["unknown"],
        "attacker_drop": routes["drop"],
        "invalid_honest_credentials": invalid_honest,
    }


def write_report(rows: list[dict], path: Path) -> None:
    models = len({row["model"] for row in rows})
    seeds = len({(row["model"], row["seed"]) for row in rows})
    lines = [
        "# Authenticated live-model pilot",
        "",
        f"This audit contains {len(rows)} episodes from {models} model(s) across "
        f"{seeds} model-seed group(s). API sampling is stochastic, so conditions "
        "do not share random draws. Statistical interpretation must follow the "
        "applicable preregistration rather than this descriptive table.",
        "",
        "| Model | Condition | Seed | Final correct | Margin | Parse failures | "
        "Request errors | Message errors | Attacker routes (agree/unknown/drop) | Invalid honest credentials |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |",
    ]
    for row in rows:
        model = row["model"].split("/")[-1]
        routes = "/".join(
            str(row[key])
            for key in ("attacker_agree", "attacker_unknown", "attacker_drop")
        )
        lines.append(
            f"| {model} | {row['condition']} | {row['seed']} | "
            f"{row['final_correct']}/{row['num_agents']} | {row['final_margin']} | "
            f"{row['raw_parse_failures']} | {row['spin_request_errors']} | "
            f"{row['message_errors']} | {routes} | "
            f"{row['invalid_honest_credentials']} |"
        )
    lines.extend([
        "",
        "## Audit interpretation",
        "",
        "- Every attacker envelope should route to `agree` under `none`, to `unknown` "
        "under `downgrade`, and to `drop` under `drop`.",
        "- Every honest envelope should have a valid credential. Any nonzero value in "
        "the final column is an implementation or data-integrity failure.",
        "- A zero raw spin is a failed sample, not a substantive answer. New-schema "
        "runs distinguish exhausted parse retries from API/request errors.",
        "- Differences in final correctness at this sample size are descriptive only.",
        "",
    ])
    path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/attack_pilot"))
    parser.add_argument("--output", type=Path, default=Path("res_attack/live_pilot_results.csv"))
    parser.add_argument("--report", type=Path, default=Path("res_attack/LIVE_PILOT_REPORT.md"))
    parser.add_argument(
        "--model",
        help="Keep only these exact model ids (comma-separated).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Keep only this exact seed.",
    )
    args = parser.parse_args()

    files = sorted(args.input.glob("*/*/*.json"))
    files = [path for path in files if path.name != "manifest.json"]
    rows = [summarize_run(path) for path in files]
    if args.model:
        models = {value.strip() for value in args.model.split(",") if value.strip()}
        rows = [row for row in rows if row["model"] in models]
    if args.seed is not None:
        rows = [row for row in rows if int(row["seed"]) == args.seed]
    rows.sort(key=lambda row: (row["model"], row["condition"], row["seed"]))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    write_report(rows, args.report)
    print(f"summarized {len(rows)} runs -> {args.output} and {args.report}")


if __name__ == "__main__":
    main()
