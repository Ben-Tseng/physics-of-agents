"""Build auditable command matrices from the frozen live-experiment config."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FIELDS = [
    "phase", "model", "seed", "label", "question_file", "question_ids",
    "attack_budget", "defense", "episodes", "estimated_calls", "output_dir",
    "command",
]


def model_slug(model: str) -> str:
    return model.split("/")[-1]


def build_power_screen(config: dict) -> list[dict]:
    common = config["common"]
    phase = config["power_screen"]
    qids = phase["question_ids"]
    rows = []
    for model in config["models"]:
        runtime = phase.get("model_runtimes", {}).get(model, {})
        backend = runtime.get("backend", "openrouter")
        provider = runtime.get("provider", config["provider"])
        max_workers = runtime.get(
            "max_workers", config["model_max_workers"][model]
        )
        min_interval = runtime.get(
            "min_request_interval_seconds",
            common.get("min_request_interval_seconds", 0),
        )
        output_root = runtime.get("output_root", "data/attack_power_screen")
        for seed in phase["seeds"]:
            for cell in phase["cells"]:
                output = (
                    f"{output_root}/"
                    f"{model_slug(model)}/{cell['label']}__seed{seed}"
                )
                command = " ".join([
                    ".venv/bin/python -m lib.datagen_attack.collect_pilot",
                    f"--backend {backend}",
                    f"--model {model}",
                    f"--provider {provider}",
                    f"--question-file {phase['question_file']}",
                    f"--question-ids {','.join(qids)}",
                    f"--num-agents {common['num_agents']}",
                    f"--num-edges {common['num_edges']}",
                    f"--num-steps {common['num_steps']}",
                    f"--k {common['spin_samples']}",
                    f"--attack-degree {common['attack_degree']}",
                    f"--temperature {common['temperature']}",
                    f"--request-timeout {common['request_timeout_seconds']}",
                    f"--api-max-retries {common.get('api_max_retries', 4)}",
                    f"--min-request-interval {min_interval}",
                    f"--max-workers {max_workers}",
                    f"--attack-budget {cell['attack_budget']}",
                    f"--defense {cell['defense']}",
                    f"--seed {seed}",
                    f"--output-dir {output}",
                ])
                rows.append({
                    "phase": "power_screen",
                    "model": model,
                    "seed": seed,
                    "label": cell["label"],
                    "question_file": phase["question_file"],
                    "question_ids": ",".join(qids),
                    "attack_budget": cell["attack_budget"],
                    "defense": cell["defense"],
                    "episodes": len(qids),
                    "estimated_calls": len(qids) * common["calls_per_episode"],
                    "output_dir": output,
                    "command": command,
                })
    return rows


def build_model_eligibility(config: dict) -> list[dict]:
    common = config["common"]
    amendment = config["model_eligibility_amendment"]
    screen = amendment["screen"]
    power = config["power_screen"]
    models = amendment.get(
        "provider_eligibility_models", [amendment["replacement_candidate"]]
    )
    output_root = amendment.get(
        "provider_eligibility_output_root", "data/attack_model_eligibility"
    )
    backend = amendment.get("provider_eligibility_backend", "openrouter")
    provider = amendment.get("provider_eligibility_provider", config["provider"])
    max_workers = amendment.get(
        "provider_eligibility_max_workers", config["model_max_workers"][models[0]]
    )
    min_interval = amendment.get(
        "provider_eligibility_min_request_interval_seconds",
        common.get("min_request_interval_seconds", 0),
    )
    cell = screen["cell"]
    qids = power["question_ids"]
    seed = screen["seed"]
    rows = []
    for model in models:
        output = f"{output_root}/{model_slug(model)}/{cell['label']}__seed{seed}"
        command = " ".join([
            ".venv/bin/python -m lib.datagen_attack.collect_pilot",
            f"--backend {backend}",
            f"--model {model}",
            f"--provider {provider}",
            f"--question-file {power['question_file']}",
            f"--question-ids {','.join(qids)}",
            f"--num-agents {common['num_agents']}",
            f"--num-edges {common['num_edges']}",
            f"--num-steps {common['num_steps']}",
            f"--k {common['spin_samples']}",
            f"--attack-degree {common['attack_degree']}",
            f"--temperature {common['temperature']}",
            f"--request-timeout {common['request_timeout_seconds']}",
            f"--api-max-retries {common.get('api_max_retries', 4)}",
            f"--min-request-interval {min_interval}",
            f"--max-workers {max_workers}",
            f"--attack-budget {cell['attack_budget']}",
            f"--defense {cell['defense']}",
            f"--seed {seed}",
            f"--output-dir {output}",
        ])
        rows.append({
            "phase": "model_eligibility",
            "model": model,
            "seed": seed,
            "label": cell["label"],
            "question_file": power["question_file"],
            "question_ids": ",".join(qids),
            "attack_budget": cell["attack_budget"],
            "defense": cell["defense"],
            "episodes": len(qids),
            "estimated_calls": len(qids) * common["calls_per_episode"],
            "output_dir": output,
            "command": command,
        })
    return rows


def build_replacement_power_screen(config: dict) -> list[dict]:
    common = config["common"]
    phase = config["power_screen"]
    amendment = config["model_eligibility_amendment"]
    model = amendment["replacement_candidate"]
    backend = amendment.get("provider_eligibility_backend", "openrouter")
    provider = amendment.get("provider_eligibility_provider", config["provider"])
    max_workers = amendment.get(
        "provider_eligibility_max_workers", config["model_max_workers"][model]
    )
    min_interval = amendment.get(
        "provider_eligibility_min_request_interval_seconds",
        common.get("min_request_interval_seconds", 0),
    )
    output_root = amendment.get(
        "replacement_power_screen_output_root", "data/attack_power_screen"
    )
    qids = phase["question_ids"]
    rows = []
    for seed in phase["seeds"]:
        for cell in phase["cells"]:
            output = f"{output_root}/{model_slug(model)}/{cell['label']}__seed{seed}"
            command = " ".join([
                ".venv/bin/python -m lib.datagen_attack.collect_pilot",
                f"--backend {backend}",
                f"--model {model}",
                f"--provider {provider}",
                f"--question-file {phase['question_file']}",
                f"--question-ids {','.join(qids)}",
                f"--num-agents {common['num_agents']}",
                f"--num-edges {common['num_edges']}",
                f"--num-steps {common['num_steps']}",
                f"--k {common['spin_samples']}",
                f"--attack-degree {common['attack_degree']}",
                f"--temperature {common['temperature']}",
                f"--request-timeout {common['request_timeout_seconds']}",
                f"--api-max-retries {common.get('api_max_retries', 4)}",
                f"--min-request-interval {min_interval}",
                f"--max-workers {max_workers}",
                f"--attack-budget {cell['attack_budget']}",
                f"--defense {cell['defense']}",
                f"--seed {seed}",
                f"--output-dir {output}",
            ])
            rows.append({
                "phase": "replacement_power_screen",
                "model": model,
                "seed": seed,
                "label": cell["label"],
                "question_file": phase["question_file"],
                "question_ids": ",".join(qids),
                "attack_budget": cell["attack_budget"],
                "defense": cell["defense"],
                "episodes": len(qids),
                "estimated_calls": len(qids) * common["calls_per_episode"],
                "output_dir": output,
                "command": command,
            })
    return rows


def build_confirmatory(config: dict) -> list[dict]:
    common = config["common"]
    phase = config["confirmatory"]
    qids = phase["question_ids"]
    output_root = phase["output_root"]
    cells = [{"label": "control", "attack_budget": 0, "defense": "none"}]
    cells.extend(
        {
            "label": f"attack{budget}_{defense}",
            "attack_budget": budget,
            "defense": defense,
        }
        for budget in phase["attack_budgets"]
        for defense in phase["defenses"]
    )
    rows = []
    for seed in phase["seeds"]:
        for model in phase["models"]:
            runtime = phase.get("model_runtimes", {}).get(model, {})
            backend = runtime.get("backend", "openrouter")
            provider = runtime.get("provider", config["provider"])
            max_workers = runtime.get(
                "max_workers", config["model_max_workers"][model]
            )
            min_interval = runtime.get(
                "min_request_interval_seconds",
                common.get("min_request_interval_seconds", 0),
            )
            for cell in cells:
                output = (
                    f"{output_root}/{model_slug(model)}/"
                    f"{cell['label']}__seed{seed}"
                )
                command = " ".join([
                    ".venv/bin/python -m lib.datagen_attack.collect_pilot",
                    f"--backend {backend}",
                    f"--model {model}",
                    f"--provider {provider}",
                    f"--question-file {phase['question_file']}",
                    f"--question-ids {','.join(qids)}",
                    f"--num-agents {common['num_agents']}",
                    f"--num-edges {common['num_edges']}",
                    f"--num-steps {common['num_steps']}",
                    f"--k {common['spin_samples']}",
                    f"--attack-degree {common['attack_degree']}",
                    f"--temperature {common['temperature']}",
                    f"--request-timeout {common['request_timeout_seconds']}",
                    f"--api-max-retries {common.get('api_max_retries', 4)}",
                    f"--min-request-interval {min_interval}",
                    f"--max-workers {max_workers}",
                    f"--attack-budget {cell['attack_budget']}",
                    f"--defense {cell['defense']}",
                    f"--seed {seed}",
                    f"--output-dir {output}",
                ])
                rows.append({
                    "phase": "confirmatory",
                    "model": model,
                    "seed": seed,
                    "label": cell["label"],
                    "question_file": phase["question_file"],
                    "question_ids": ",".join(qids),
                    "attack_budget": cell["attack_budget"],
                    "defense": cell["defense"],
                    "episodes": len(qids),
                    "estimated_calls": len(qids) * common["calls_per_episode"],
                    "output_dir": output,
                    "command": command,
                })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", type=Path,
        default=Path("res_attack/formal_experiment_config.json"),
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path("res_attack/power_screen_matrix.csv"),
    )
    parser.add_argument(
        "--phase",
        choices=("power-screen", "model-eligibility", "replacement-power-screen", "confirmatory"),
        default="power-screen",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.phase == "power-screen":
        rows = build_power_screen(config)
    elif args.phase == "model-eligibility":
        rows = build_model_eligibility(config)
    elif args.phase == "replacement-power-screen":
        rows = build_replacement_power_screen(config)
    else:
        rows = build_confirmatory(config)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    episodes = sum(row["episodes"] for row in rows)
    calls = sum(row["estimated_calls"] for row in rows)
    print(f"wrote {len(rows)} jobs, {episodes} episodes, {calls} calls -> {args.output}")


if __name__ == "__main__":
    main()
