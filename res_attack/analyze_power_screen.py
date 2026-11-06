"""Descriptive power-screen analysis and conservative confirmatory sensitivity."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from math import sqrt
from pathlib import Path
from statistics import NormalDist


def wilson(successes: int, total: int, alpha: float = 0.05) -> tuple[float, float]:
    z = NormalDist().inv_cdf(1 - alpha / 2)
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    radius = z * sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return center - radius, center + radius


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=Path,
        default=Path("res_attack/power_screen_partial_results.csv"),
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path("res_attack/POWER_SCREEN_ANALYSIS.md"),
    )
    args = parser.parse_args()
    with args.input.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["model"], row["condition"])].append(row)

    lines = [
        "# Power-screen descriptive analysis",
        "",
        "These are descriptive power-screen statistics, not confirmatory tests. "
        "Incomplete jobs are absent, and no inferential comparison is made for a "
        "model unless all predeclared cells are complete.",
        "",
        "| Model | Condition | Episodes | Incorrect majorities | Rate (95% Wilson CI) | Mean agent accuracy |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for (model, condition), values in sorted(grouped.items()):
        errors = sum(int(row["incorrect_terminal_majority"]) for row in values)
        low, high = wilson(errors, len(values))
        accuracy = sum(float(row["final_correct_fraction"]) for row in values) / len(values)
        lines.append(
            f"| {model.split('/')[-1]} | {condition} | {len(values)} | {errors} | "
            f"{errors / len(values):.3f} ({low:.3f}, {high:.3f}) | {accuracy:.3f} |"
        )

    z_alpha = NormalDist().inv_cdf(0.975)
    z_power = NormalDist().inv_cdf(0.80)
    lines.extend([
        "",
        "## Confirmatory sensitivity",
        "",
        "The table below uses a conservative two-independent-proportion approximation "
        "at two-sided alpha 0.05 and 80% power, with worst-case variance. The mixed-effects "
        "analysis and within-question structure may change realized power; this is a "
        "transparent planning bound, not a post hoc significance claim.",
        "",
        "| Repetitions | Questions | Episodes per cell | Approximate minimum detectable risk difference |",
        "| ---: | ---: | ---: | ---: |",
    ])
    for repetitions in range(5, 11):
        n = 18 * repetitions
        mde = (z_alpha + z_power) * sqrt(0.5 / n)
        lines.append(f"| {repetitions} | 18 | {n} | {mde:.3f} |")
    lines.extend([
        "",
        "The preregistered minimum of five repetitions targets effects of roughly "
        "0.21 or larger; ten repetitions targets roughly 0.15. Because the current "
        "screen has only six questions and two seeds, it should select between these "
        "bounds only after both model matrices are complete.",
        "",
    ])
    args.output.write_text("\n".join(lines))
    print(f"analyzed {len(rows)} episodes -> {args.output}")


if __name__ == "__main__":
    main()
