"""Evaluate a replacement model against the frozen control-only gates."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("res_attack/formal_experiment_config.json"))
    parser.add_argument("--results", type=Path, default=Path("res_attack/model_eligibility_results.csv"))
    parser.add_argument("--output", type=Path, default=Path("res_attack/model_eligibility_decision.json"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text())
    gate = config["model_eligibility_amendment"]["screen"]
    with args.results.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    episodes = len(rows)
    correct_majorities = sum(
        int(row["final_correct"]) > int(row["num_agents"]) / 2 for row in rows
    )
    total_correct = sum(int(row["final_correct"]) for row in rows)
    total_agents = sum(int(row["num_agents"]) for row in rows)
    mean_agent_accuracy = total_correct / total_agents
    parse_failures = sum(int(row["raw_parse_failures"]) for row in rows)
    message_failures = sum(int(row["message_errors"]) for row in rows)
    invalid_credentials = sum(int(row["invalid_honest_credentials"]) for row in rows)
    expected_episodes = len(config["power_screen"]["question_ids"])

    checks = {
        "all_expected_episodes_complete": episodes == expected_episodes,
        "correct_terminal_majorities": correct_majorities >= gate["minimum_correct_terminal_majorities"],
        "mean_agent_accuracy": mean_agent_accuracy >= gate["minimum_mean_agent_accuracy"],
        "parse_failures": parse_failures <= gate["maximum_parse_failures"],
        "message_call_failures": message_failures <= gate["maximum_message_call_failures"],
        "invalid_honest_credentials": invalid_credentials <= gate["maximum_invalid_honest_credentials"],
    }
    decision = {
        "model": config["model_eligibility_amendment"]["replacement_candidate"],
        "passed": all(checks.values()),
        "observed": {
            "episodes": episodes,
            "correct_terminal_majorities": correct_majorities,
            "mean_agent_accuracy": round(mean_agent_accuracy, 6),
            "parse_failures": parse_failures,
            "message_call_failures": message_failures,
            "invalid_honest_credentials": invalid_credentials,
        },
        "checks": checks,
    }
    args.output.write_text(json.dumps(decision, indent=2) + "\n")
    print(json.dumps(decision, indent=2))
    if not decision["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
