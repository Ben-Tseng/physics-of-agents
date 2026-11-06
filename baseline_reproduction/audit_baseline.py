"""Audit the reproduced coupling fit against the checked-in artifact and draft values."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent

DRAFT = {
    "gpt": {
        "beta_pos_T": 2.29,
        "beta_pos_F": 1.98,
        "beta_neg_T": 0.70,
        "beta_neg_F": 0.85,
        "beta_0": 0.93,
    },
    "gma": {
        "beta_pos_T": 0.34,
        "beta_pos_F": 0.20,
        "beta_neg_T": 0.17,
        "beta_neg_F": 0.36,
        "beta_0": 0.96,
    },
    "qwn": {
        "beta_pos_T": 1.03,
        "beta_pos_F": 0.77,
        "beta_neg_T": 0.40,
        "beta_neg_F": 0.80,
        "beta_0": 1.01,
    },
    "lma": {
        "beta_pos_T": 1.15,
        "beta_pos_F": 0.84,
        "beta_neg_T": 0.59,
        "beta_neg_F": 0.61,
        "beta_0": 0.97,
    },
}


def numeric_leaves(value, prefix=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from numeric_leaves(child, prefix + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from numeric_leaves(child, prefix + (str(index),))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        yield ".".join(prefix), float(value)


def main():
    upstream = json.loads((ROOT / "upstream_couplings.json").read_text())
    reproduced = json.loads((ROOT / "reproduced_couplings.json").read_text())

    old = dict(numeric_leaves(upstream))
    new = dict(numeric_leaves(reproduced))
    shared = sorted(old.keys() & new.keys())
    deltas = [abs(old[key] - new[key]) for key in shared]

    rows = []
    params = reproduced["params"]
    for short, label in reproduced["models"].items():
        fit = params[short]["objective"]["five"]["betas"]
        for beta, draft_value in DRAFT[short].items():
            fitted = float(fit[beta])
            rows.append({
                "model_key": short,
                "model": label,
                "coefficient": beta,
                "draft_rounded": draft_value,
                "reproduced": fitted,
                "draft_minus_reproduced": draft_value - fitted,
            })

    with (ROOT / "comparison_table.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "numeric_values_compared": len(shared),
        "max_absolute_reproduction_delta": max(deltas),
        "mean_absolute_reproduction_delta": sum(deltas) / len(deltas),
        "draft_values_are_rounded_repo_values": all(
            round(row["reproduced"], 2) == row["draft_rounded"] for row in rows
        ),
        "standardization_note": (
            "res/utils.py standardizes columns during optimization, then divides by "
            "the column standard deviations and adjusts the intercept before saving. "
            "The stored fields and couplings therefore apply to raw design rows."
        ),
    }
    (ROOT / "audit_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
