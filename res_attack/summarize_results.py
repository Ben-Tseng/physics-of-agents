"""Create compact CSV and Markdown summaries from attack-budget curves."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def markdown_table(frame):
    values = frame.astype(object).where(frame.notna(), "").astype(str)
    header = "| " + " | ".join(values.columns) + " |"
    rule = "| " + " | ".join(["---"] * len(values.columns)) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in values.to_numpy()]
    return "\n".join([header, rule, *rows])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = args.output_dir or args.input.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    curves = pd.read_csv(args.input)
    one = curves.drop_duplicates(["model_key", "seed", "strategy", "defense"])

    summary = (
        one.groupby(["model_key", "model", "strategy", "defense"], dropna=False)
        .agg(
            k_star_mean=("k_star_50", "mean"),
            k_star_sd=("k_star_50", "std"),
            finite_seeds=("k_star_50", "count"),
            total_seeds=("seed", "count"),
            base_predicted_success=("base_predicted_success_rate", "mean"),
            observed_success=("observed_success_rate", "mean"),
            base_observed_agreement=("base_observed_majority_agreement", "mean"),
        )
        .reset_index()
    )

    pivot = summary.pivot_table(
        index=["model_key", "strategy"], columns="defense", values="k_star_mean"
    )
    multiplier = (pivot.get("downgrade") / pivot.get("none")).rename(
        "empirical_multiplier"
    )
    summary = summary.merge(multiplier, on=["model_key", "strategy"], how="left")

    couplings = json.loads((ROOT / "res" / "couplings.json").read_text())
    theory = {}
    for short, values in couplings["params"].items():
        beta = values["objective"]["five"]["betas"]
        theory[short] = (beta["beta_pos_F"] + beta["beta_0"]) / beta["beta_0"]
    summary["weight_ratio_prediction"] = summary["model_key"].map(theory)
    summary["drop_exceeds_max_k"] = (
        (summary["defense"] == "drop") & (summary["finite_seeds"] == 0)
    )
    summary.to_csv(output_dir / "summary.csv", index=False)

    focus = summary[summary["defense"].isin(["none", "downgrade"])].copy()
    columns = [
        "model", "strategy", "defense", "k_star_mean", "k_star_sd",
        "empirical_multiplier", "weight_ratio_prediction",
        "base_observed_agreement",
    ]
    text = [
        "# Counterfactual attack summary",
        "",
        "These results use the fitted five-coupling model on released objective "
        "test episodes; they are not new LLM attack trials.",
        "",
        markdown_table(focus[columns].round(3)),
        "",
        "`drop` produced no flips at any budget, as expected from its zero "
        "message weight. A missing finite k-star therefore means k-star is "
        "larger than the maximum tested budget, not zero.",
        "",
    ]
    (output_dir / "SUMMARY.md").write_text("\n".join(text))
    print(f"wrote {output_dir / 'summary.csv'}")
    print(f"wrote {output_dir / 'SUMMARY.md'}")


if __name__ == "__main__":
    main()
