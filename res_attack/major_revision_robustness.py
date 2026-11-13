"""Robustness analyses requested during major-revision review.

The script operates only on the locked accepted episode table.  It does not
select, replace, or recollect any experimental block.
"""

from __future__ import annotations

import argparse
import json
import math
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from patsy import build_design_matrices
from scipy.stats import norm
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM


DEFENSE_ORDER = ["none", "downgrade", "drop"]
MODEL_ORDER = ["qwen3.5-27b", "mistral-small-2603"]
CONDITION_ORDER = ["control"] + [
    f"attack{budget}_{defense}"
    for budget in (1, 2, 4)
    for defense in DEFENSE_ORDER
]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("res_attack/confirmatory_analysis/accepted_episode_data.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("res_attack/confirmatory_analysis/major_revision"),
    )
    return parser.parse_args()


def prepare(data: pd.DataFrame) -> pd.DataFrame:
    frame = data.copy()
    frame["defense"] = pd.Categorical(frame["defense"], DEFENSE_ORDER)
    frame["model"] = pd.Categorical(frame["model"], MODEL_ORDER)
    frame["condition"] = pd.Categorical(frame["condition"], CONDITION_ORDER)
    return frame


def contrast(names, means, covariance, weights):
    vector = np.zeros(len(names))
    for term, weight in weights.items():
        vector[names.index(term)] = weight
    estimate = float(vector @ means)
    standard_error = math.sqrt(max(float(vector @ covariance @ vector), 0.0))
    z_value = estimate / standard_error
    return {
        "estimate_log_odds": estimate,
        "standard_error": standard_error,
        "z": z_value,
        "p_two_sided": float(2 * norm.sf(abs(z_value))),
        "odds_ratio": math.exp(estimate),
        "ci95_low_or": math.exp(estimate - 1.96 * standard_error),
        "ci95_high_or": math.exp(estimate + 1.96 * standard_error),
    }


def primary_contrasts(names, means, covariance):
    positive_mean = 7 / 3
    definitions = {
        "H1: budget slope under no defense": {"attack_budget": 1},
        "H2: downgrade vs none at mean positive budget": {
            "defense[T.downgrade]": 1,
            "attack_budget:defense[T.downgrade]": positive_mean,
        },
        "H3: drop vs none at mean positive budget": {
            "defense[T.drop]": 1,
            "attack_budget:defense[T.drop]": positive_mean,
        },
    }
    rows = []
    for label, weights in definitions.items():
        rows.append({"contrast": label, **contrast(names, means, covariance, weights)})
    return rows


def fit_map(frame, fe_p=5.0, vcp_p=0.5):
    model = BinomialBayesMixedGLM.from_formula(
        "incorrect_terminal_majority ~ attack_budget * defense + model",
        {"question": "0 + C(question_id)", "seed_graph": "0 + C(seed)"},
        frame,
        fe_p=fe_p,
        vcp_p=vcp_p,
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = model.fit_map(method="BFGS", minim_opts={"maxiter": 2000})
    if caught:
        # The broadest random-effect prior can leave BFGS just above the
        # gradient tolerance.  Refit the same objective with bounded-memory
        # BFGS rather than reporting a numerically flagged sensitivity point.
        with warnings.catch_warnings(record=True) as fallback_caught:
            warnings.simplefilter("always")
            result = model.fit_map(
                method="L-BFGS-B", minim_opts={"maxiter": 10000}
            )
        caught = fallback_caught
    size = len(model.exog_names)
    covariance = np.asarray(result.cov_params())[:size, :size]
    return model, result, covariance, [str(item.message) for item in caught]


def prior_sensitivity(frame):
    rows = []
    for fe_p in (2.5, 5.0, 10.0):
        for vcp_p in (0.1, 0.25, 0.5):
            model, result, covariance, warning_text = fit_map(frame, fe_p, vcp_p)
            for row in primary_contrasts(
                model.exog_names, np.asarray(result.fe_mean), covariance
            ):
                rows.append(
                    {
                        "fixed_effect_prior_sd": fe_p,
                        "log_random_effect_sd_prior_sd": vcp_p,
                        "optimizer_warning_count": len(warning_text),
                        **row,
                    }
                )
    return pd.DataFrame(rows)


def design_row(result, condition):
    row = pd.DataFrame(
        {"condition": [condition], "model": [MODEL_ORDER[0]], "seed": [0]}
    )
    row["condition"] = pd.Categorical(row["condition"], CONDITION_ORDER)
    row["model"] = pd.Categorical(row["model"], MODEL_ORDER)
    matrix = build_design_matrices([result.model.data.design_info], row)[0]
    return np.asarray(matrix)[0]


def gee_sensitivity(frame):
    result = smf.gee(
        "incorrect_terminal_majority ~ C(condition) + model + C(seed)",
        groups="question_id",
        data=frame,
        family=sm.families.Binomial(),
        cov_struct=sm.cov_struct.Exchangeable(),
    ).fit(maxiter=200)
    means = result.params.to_numpy()
    covariance = result.cov_params().to_numpy()
    names = list(result.params.index)
    rows = []
    control = design_row(result, "control")
    for budget in (1, 2, 4):
        vector = design_row(result, f"attack{budget}_none") - control
        rows.append(
            {
                "contrast": f"H1 sensitivity: none budget {budget} vs control",
                **contrast(names, means, covariance, dict(zip(names, vector))),
            }
        )
    for defense, label in (("downgrade", "H2"), ("drop", "H3")):
        vector = sum(
            design_row(result, f"attack{budget}_{defense}")
            - design_row(result, f"attack{budget}_none")
            for budget in (1, 2, 4)
        ) / 3
        rows.append(
            {
                "contrast": f"{label} sensitivity: {defense} vs none, mean positive-budget log-odds contrast",
                **contrast(names, means, covariance, dict(zip(names, vector))),
            }
        )
    output = pd.DataFrame(rows)
    output.insert(0, "question_clusters", frame["question_id"].nunique())
    output.insert(1, "working_correlation", "exchangeable")
    output.insert(2, "converged", bool(result.converged))
    return output


def leave_one_question_out(frame):
    rows = []
    for question_id in sorted(frame["question_id"].unique()):
        subset = frame[frame["question_id"] != question_id].copy()
        model, result, covariance, warning_text = fit_map(subset)
        for row in primary_contrasts(
            model.exog_names, np.asarray(result.fe_mean), covariance
        ):
            rows.append(
                {
                    "omitted_question_id": question_id,
                    "optimizer_warning_count": len(warning_text),
                    **row,
                }
            )
    return pd.DataFrame(rows)


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    frame = prepare(pd.read_csv(args.data))

    prior = prior_sensitivity(frame)
    prior.to_csv(args.output_dir / "prior_sensitivity.csv", index=False)

    gee = gee_sensitivity(frame)
    gee.to_csv(args.output_dir / "gee_question_cluster_robust.csv", index=False)

    loo = leave_one_question_out(frame)
    loo.to_csv(args.output_dir / "leave_one_question_out.csv", index=False)

    summary = {
        "accepted_episode_rows": len(frame),
        "question_clusters": int(frame["question_id"].nunique()),
        "prior_grid_fits": int(prior[["fixed_effect_prior_sd", "log_random_effect_sd_prior_sd"]].drop_duplicates().shape[0]),
        "prior_grid_all_h1_or_above_one": bool((prior[prior["contrast"].str.startswith("H1")]["odds_ratio"] > 1).all()),
        "prior_grid_all_h2_or_below_one": bool((prior[prior["contrast"].str.startswith("H2")]["odds_ratio"] < 1).all()),
        "prior_grid_all_h3_or_below_one": bool((prior[prior["contrast"].str.startswith("H3")]["odds_ratio"] < 1).all()),
        "leave_one_question_out_all_h1_or_above_one": bool((loo[loo["contrast"].str.startswith("H1")]["odds_ratio"] > 1).all()),
        "leave_one_question_out_all_h2_or_below_one": bool((loo[loo["contrast"].str.startswith("H2")]["odds_ratio"] < 1).all()),
        "leave_one_question_out_all_h3_or_below_one": bool((loo[loo["contrast"].str.startswith("H3")]["odds_ratio"] < 1).all()),
    }
    (args.output_dir / "robustness_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))
    print(gee.to_string(index=False))


if __name__ == "__main__":
    main()
