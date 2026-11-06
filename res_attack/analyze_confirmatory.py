"""Analyze the locked, quality-gated two-deployment confirmatory dataset."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import statsmodels
from scipy.special import expit
from scipy.stats import norm
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM


QWEN_FILES = {
    0: "qwen_official_confirmatory_seed0_recollection_results.csv",
    1: "qwen_official_confirmatory_seed1_results.csv",
    2: "qwen_official_confirmatory_seed2_results.csv",
    3: "qwen_official_confirmatory_seed3_results.csv",
    4: "qwen_official_confirmatory_seed4_recollection_results.csv",
    5: "qwen_official_confirmatory_seed5_results.csv",
    6: "qwen_official_confirmatory_seed6_results.csv",
    7: "qwen_official_confirmatory_seed7_results.csv",
    8: "qwen_official_confirmatory_seed8_results.csv",
    9: "qwen_official_confirmatory_seed9_results.csv",
}

MISTRAL_FILES = {
    0: "mistral_official_confirmatory_seed0_results.csv",
    1: "mistral_official_confirmatory_seed1_recollection_results.csv",
    2: "mistral_official_confirmatory_seed2_results.csv",
    3: "mistral_official_confirmatory_seed3_results.csv",
    4: "mistral_official_confirmatory_seed4_results.csv",
    5: "mistral_official_confirmatory_seed5_results.csv",
    6: "mistral_official_confirmatory_seed6_results.csv",
    7: "mistral_official_confirmatory_seed7_recollection_results.csv",
    8: "mistral_official_confirmatory_seed8_results.csv",
    9: "mistral_official_confirmatory_seed9_recollection_results.csv",
}

MODEL_ORDER = ["qwen3.5-27b", "mistral-small-2603"]
DEFENSE_ORDER = ["none", "downgrade", "drop"]
BUDGETS = [0, 1, 2, 4]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--res-dir", type=Path, default=Path("res_attack"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("res_attack/confirmatory_analysis"),
    )
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--bootstrap-seed", type=int, default=20261106)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_locked_data(res_dir: Path):
    selected = []
    for model, files in ((MODEL_ORDER[0], QWEN_FILES), (MODEL_ORDER[1], MISTRAL_FILES)):
        for seed, name in files.items():
            path = res_dir / name
            frame = pd.read_csv(path)
            selected.append(
                {
                    "model": model,
                    "seed": seed,
                    "path": str(path),
                    "sha256": sha256(path),
                    "rows": len(frame),
                    "replacement": "recollection" in name,
                }
            )
    manifest = pd.DataFrame(selected)
    frames = []
    for row in selected:
        frame = pd.read_csv(row["path"])
        frame["source_file"] = row["path"]
        frames.append(frame)
    data = pd.concat(frames, ignore_index=True)
    return manifest, data


def validate_data(manifest: pd.DataFrame, data: pd.DataFrame):
    if len(manifest) != 20 or not (manifest["rows"] == 180).all():
        raise ValueError("accepted manifest must contain 20 blocks of 180 episodes")
    if len(data) != 3600:
        raise ValueError(f"expected 3600 accepted episodes, found {len(data)}")
    if set(data["model"]) != set(MODEL_ORDER):
        raise ValueError("unexpected model set")
    if set(data["seed"]) != set(range(10)):
        raise ValueError("unexpected seed set")
    if data.duplicated(["model", "seed", "condition", "question_id"]).any():
        raise ValueError("duplicate model-seed-condition-question rows")
    expected_conditions = {
        "control",
        "attack1_none",
        "attack1_downgrade",
        "attack1_drop",
        "attack2_none",
        "attack2_downgrade",
        "attack2_drop",
        "attack4_none",
        "attack4_downgrade",
        "attack4_drop",
    }
    counts = data.groupby(["model", "seed"])["condition"].agg(lambda x: set(x))
    if not all(value == expected_conditions for value in counts):
        raise ValueError("one or more accepted blocks are not ten-cell complete")
    per_cell = data.groupby(["model", "seed", "condition"]).size()
    if not (per_cell == 18).all():
        raise ValueError("one or more accepted cells do not contain 18 questions")
    if data["invalid_honest_credentials"].sum() != 0:
        raise ValueError("accepted data contain invalid honest credentials")


def cell_rates(data: pd.DataFrame) -> pd.DataFrame:
    grouped = data.groupby(["model", "attack_budget", "defense"], observed=True)
    result = grouped.agg(
        episodes=("incorrect_terminal_majority", "size"),
        attack_successes=("incorrect_terminal_majority", "sum"),
        attack_success_rate=("incorrect_terminal_majority", "mean"),
        mean_correct_fraction=("final_correct_fraction", "mean"),
        mean_terminal_margin=("final_margin", "mean"),
        raw_zero_spins=("raw_zero_spins", "sum"),
        spin_request_errors=("spin_request_errors", "sum"),
        message_errors=("message_errors", "sum"),
    ).reset_index()
    return result.sort_values(["model", "attack_budget", "defense"])


def fit_glmm(data: pd.DataFrame, include_model=True):
    frame = data.copy()
    frame["defense"] = pd.Categorical(frame["defense"], DEFENSE_ORDER)
    frame["model"] = pd.Categorical(frame["model"], MODEL_ORDER)
    formula = "incorrect_terminal_majority ~ attack_budget * defense"
    if include_model:
        formula += " + model"
    variance_components = {
        "question": "0 + C(question_id)",
        "seed_graph": "0 + C(seed)",
    }
    model = BinomialBayesMixedGLM.from_formula(
        formula, variance_components, frame, vcp_p=0.5, fe_p=5.0
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = model.fit_map(method="BFGS", minim_opts={"maxiter": 2000})
    warning_text = [str(item.message) for item in caught]
    names = model.exog_names
    means = np.asarray(result.fe_mean)
    covariance = np.asarray(result.cov_params())[: len(names), : len(names)]
    standard_errors = np.sqrt(np.diag(covariance))
    z_values = means / standard_errors
    fixed = pd.DataFrame(
        {
            "term": names,
            "estimate_log_odds": means,
            "standard_error": standard_errors,
            "z": z_values,
            "p_two_sided": 2 * norm.sf(np.abs(z_values)),
            "odds_ratio": np.exp(means),
            "ci95_low_or": np.exp(means - 1.96 * standard_errors),
            "ci95_high_or": np.exp(means + 1.96 * standard_errors),
        }
    )
    return model, result, fixed, covariance, warning_text


def contrast_row(label, weights, names, means, covariance):
    vector = np.zeros(len(names))
    for term, weight in weights.items():
        vector[names.index(term)] = weight
    estimate = float(vector @ means)
    variance = float(vector @ covariance @ vector)
    standard_error = math.sqrt(max(variance, 0.0))
    z_value = estimate / standard_error if standard_error else math.nan
    p_value = 2 * norm.sf(abs(z_value)) if np.isfinite(z_value) else math.nan
    return {
        "contrast": label,
        "estimate_log_odds": estimate,
        "standard_error": standard_error,
        "z": z_value,
        "p_two_sided": p_value,
        "odds_ratio": math.exp(estimate),
        "ci95_low_or": math.exp(estimate - 1.96 * standard_error),
        "ci95_high_or": math.exp(estimate + 1.96 * standard_error),
    }


def holm_adjust(values):
    values = np.asarray(values, dtype=float)
    order = np.argsort(values)
    adjusted = np.empty(len(values))
    running = 0.0
    for rank, index in enumerate(order):
        candidate = (len(values) - rank) * values[index]
        running = max(running, candidate)
        adjusted[index] = min(running, 1.0)
    return adjusted


def build_contrasts(model, result, covariance):
    names = model.exog_names
    means = np.asarray(result.fe_mean)
    positive_mean = np.mean([1, 2, 4])
    main = [
        contrast_row("H1: budget slope under no defense", {"attack_budget": 1}, names, means, covariance),
        contrast_row(
            "H2 primary: downgrade vs none at mean positive budget",
            {"defense[T.downgrade]": 1, "attack_budget:defense[T.downgrade]": positive_mean},
            names,
            means,
            covariance,
        ),
        contrast_row(
            "H3: drop vs none at mean positive budget",
            {"defense[T.drop]": 1, "attack_budget:defense[T.drop]": positive_mean},
            names,
            means,
            covariance,
        ),
    ]
    secondary = []
    for budget in (1, 2, 4):
        secondary.append(
            contrast_row(
                f"downgrade vs none at budget {budget}",
                {"defense[T.downgrade]": 1, "attack_budget:defense[T.downgrade]": budget},
                names,
                means,
                covariance,
            )
        )
        secondary.append(
            contrast_row(
                f"drop vs none at budget {budget}",
                {"defense[T.drop]": 1, "attack_budget:defense[T.drop]": budget},
                names,
                means,
                covariance,
            )
        )
        secondary.append(
            contrast_row(
                f"drop vs downgrade at budget {budget}",
                {
                    "defense[T.drop]": 1,
                    "defense[T.downgrade]": -1,
                    "attack_budget:defense[T.drop]": budget,
                    "attack_budget:defense[T.downgrade]": -budget,
                },
                names,
                means,
                covariance,
            )
        )
    secondary_frame = pd.DataFrame(secondary)
    secondary_frame["p_holm"] = holm_adjust(secondary_frame["p_two_sided"])
    return pd.DataFrame(main), secondary_frame


def fit_monotone_logistic(successes, totals, budgets=BUDGETS):
    x = np.asarray(budgets, dtype=float)
    y = np.asarray(successes, dtype=float)
    n = np.asarray(totals, dtype=float)
    overall = np.clip(y.sum() / n.sum(), 1e-6, 1 - 1e-6)
    design = np.column_stack([np.ones(len(x)), x])
    params = np.array([math.log(overall / (1 - overall)), 0.1])
    for _ in range(50):
        probability = np.clip(expit(design @ params), 1e-9, 1 - 1e-9)
        gradient = design.T @ (y - n * probability)
        weights = n * probability * (1 - probability)
        information = design.T @ (weights[:, None] * design)
        try:
            step = np.linalg.solve(information + np.eye(2) * 1e-10, gradient)
        except np.linalg.LinAlgError:
            break
        params += step
        if np.max(np.abs(step)) < 1e-10:
            break
    intercept, slope = params
    if slope < 0:
        intercept = math.log(overall / (1 - overall))
        slope = 0.0
    if slope <= 1e-8:
        critical = math.inf
    else:
        critical = -intercept / slope
        if critical < 0:
            critical = 0.0
    return intercept, slope, critical


def precompute_question_counts(data):
    questions = np.array(sorted(data["question_id"].unique()))
    arrays = {}
    for model_name in MODEL_ORDER:
        for defense in DEFENSE_ORDER:
            success = np.zeros((len(questions), len(BUDGETS)), dtype=float)
            total = np.zeros((len(questions), len(BUDGETS)), dtype=float)
            for question_index, question in enumerate(questions):
                subset = data[
                    (data["model"] == model_name) & (data["question_id"] == question)
                ]
                for budget_index, budget in enumerate(BUDGETS):
                    if budget == 0:
                        cell = subset[subset["attack_budget"] == 0]
                    else:
                        cell = subset[
                            (subset["attack_budget"] == budget)
                            & (subset["defense"] == defense)
                        ]
                    success[question_index, budget_index] = cell[
                        "incorrect_terminal_majority"
                    ].sum()
                    total[question_index, budget_index] = len(cell)
            arrays[(model_name, defense)] = (success, total)
    return questions, arrays


def curve_counts(data, model_name, defense, sampled_questions=None):
    subset = data[data["model"] == model_name]
    if sampled_questions is not None:
        parts = [subset[subset["question_id"] == question] for question in sampled_questions]
        subset = pd.concat(parts, ignore_index=True)
    successes, totals = [], []
    for budget in BUDGETS:
        if budget == 0:
            cell = subset[subset["attack_budget"] == 0]
        else:
            cell = subset[(subset["attack_budget"] == budget) & (subset["defense"] == defense)]
        successes.append(int(cell["incorrect_terminal_majority"].sum()))
        totals.append(len(cell))
    return successes, totals


def estimate_critical_budgets(data, bootstrap, bootstrap_seed):
    questions, arrays = precompute_question_counts(data)
    point_rows = []
    point_values = {}
    for model_name in MODEL_ORDER:
        for defense in DEFENSE_ORDER:
            success_array, total_array = arrays[(model_name, defense)]
            successes = success_array.sum(axis=0)
            totals = total_array.sum(axis=0)
            intercept, slope, critical = fit_monotone_logistic(successes, totals)
            point_values[(model_name, defense)] = critical
            point_rows.append(
                {
                    "model": model_name,
                    "defense": defense,
                    "intercept": intercept,
                    "nonnegative_budget_slope": slope,
                    "critical_budget_50pct": critical,
                    "beyond_tested_maximum": not np.isfinite(critical) or critical > 4,
                }
            )

    rng = np.random.default_rng(bootstrap_seed)
    boot_rows = []
    for iteration in range(bootstrap):
        sampled_indices = rng.integers(0, len(questions), size=len(questions))
        question_weights = np.bincount(sampled_indices, minlength=len(questions))
        values = {}
        for model_name in MODEL_ORDER:
            for defense in DEFENSE_ORDER:
                success_array, total_array = arrays[(model_name, defense)]
                successes = question_weights @ success_array
                totals = question_weights @ total_array
                _, _, critical = fit_monotone_logistic(successes, totals)
                values[(model_name, defense)] = critical
                boot_rows.append(
                    {
                        "bootstrap": iteration,
                        "model": model_name,
                        "defense": defense,
                        "critical_budget_50pct": critical,
                    }
                )
        for model_name in MODEL_ORDER:
            none_value = values[(model_name, "none")]
            downgrade_value = values[(model_name, "downgrade")]
            multiplier = downgrade_value / none_value if none_value > 0 else math.inf
            boot_rows.append(
                {
                    "bootstrap": iteration,
                    "model": model_name,
                    "defense": "downgrade_over_none_multiplier",
                    "critical_budget_50pct": multiplier,
                }
            )

    boot_frame = pd.DataFrame(boot_rows)
    summary = pd.DataFrame(point_rows)
    interval_rows = []
    for (model_name, defense), group in boot_frame.groupby(["model", "defense"]):
        values = group["critical_budget_50pct"].to_numpy()
        finite = values[np.isfinite(values)]
        finite_fraction = len(finite) / len(values)

        def mixture_quantile(probability):
            if not len(finite) or probability > finite_fraction:
                return math.inf
            conditional_probability = probability / finite_fraction
            return np.quantile(finite, min(conditional_probability, 1.0))

        interval_rows.append(
            {
                "model": model_name,
                "defense": defense,
                "bootstrap_finite_fraction": finite_fraction,
                "bootstrap_ci95_low": mixture_quantile(0.025),
                "bootstrap_ci95_high": mixture_quantile(0.975),
            }
        )
    intervals = pd.DataFrame(interval_rows)
    summary = summary.merge(
        intervals[intervals["defense"].isin(DEFENSE_ORDER)], on=["model", "defense"]
    )
    multiplier_rows = []
    for model_name in MODEL_ORDER:
        none_value = point_values[(model_name, "none")]
        downgrade_value = point_values[(model_name, "downgrade")]
        point_multiplier = downgrade_value / none_value if none_value > 0 else math.inf
        interval = intervals[
            (intervals["model"] == model_name)
            & (intervals["defense"] == "downgrade_over_none_multiplier")
        ].iloc[0]
        multiplier_rows.append(
            {
                "model": model_name,
                "defense": "downgrade_over_none_multiplier",
                "intercept": math.nan,
                "nonnegative_budget_slope": math.nan,
                "critical_budget_50pct": point_multiplier,
                "beyond_tested_maximum": True,
                "bootstrap_finite_fraction": interval["bootstrap_finite_fraction"],
                "bootstrap_ci95_low": interval["bootstrap_ci95_low"],
                "bootstrap_ci95_high": interval["bootstrap_ci95_high"],
            }
        )
    summary = pd.concat([summary, pd.DataFrame(multiplier_rows)], ignore_index=True)
    return summary, boot_frame


def make_curve_plot(data, critical, output_path):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    colors = {"none": "#1f77b4", "downgrade": "#ff7f0e", "drop": "#2ca02c"}
    grid = np.linspace(0, 12, 250)
    for axis, model_name in zip(axes, MODEL_ORDER):
        for defense in DEFENSE_ORDER:
            successes, totals = curve_counts(data, model_name, defense)
            rates = np.asarray(successes) / np.asarray(totals)
            row = critical[(critical["model"] == model_name) & (critical["defense"] == defense)].iloc[0]
            fitted = expit(row["intercept"] + row["nonnegative_budget_slope"] * grid)
            axis.plot(grid, fitted, color=colors[defense], label=defense)
            axis.scatter(BUDGETS, rates, color=colors[defense], s=30, zorder=3)
        axis.axhline(0.5, color="black", linestyle="--", linewidth=0.8)
        axis.axvline(4, color="#777777", linestyle=":", linewidth=0.8)
        axis.set_title(model_name)
        axis.set_xlabel("attack budget")
        axis.set_xlim(0, 12)
        axis.set_ylim(0, 1)
        axis.grid(alpha=0.18)
    axes[0].set_ylabel("incorrect terminal-majority probability")
    axes[1].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def format_number(value, digits=3):
    if pd.isna(value):
        return "NA"
    if np.isposinf(value):
        return "∞"
    if np.isneginf(value):
        return "−∞"
    return f"{value:.{digits}f}"


def write_report(
    output_dir,
    cell_frame,
    deployment_primary,
    primary,
    secondary,
    critical,
    warnings_found,
):
    lines = [
        "# Frozen confirmatory analysis",
        "",
        "This report analyzes only the 20 model-seed blocks that passed their",
        "prospectively fixed technical gates (3,600 episodes). Replaced and",
        "excluded blocks, power screens, pilots, and legacy-provider data are absent.",
        "",
        "## Descriptive attack-success rates",
        "",
        "| Model | Budget | Defense | Successes / N | Rate |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for row in cell_frame.itertuples():
        lines.append(
            f"| {row.model} | {row.attack_budget} | {row.defense} | "
            f"{row.attack_successes}/{row.episodes} | {row.attack_success_rate:.3f} |"
        )
    lines += [
        "",
        "## Deployment-specific mixed-effects estimates",
        "",
        "The preregistered reporting boundary requires deployment-specific estimates",
        "before any pooled estimate. Each model below has the same fixed defense and",
        "budget structure and random intercepts for question and seed/graph.",
        "",
        "| Deployment | Contrast | Odds ratio | 95% CI | p |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for row in deployment_primary.itertuples():
        lines.append(
            f"| {row.deployment} | {row.contrast} | {row.odds_ratio:.3f} | "
            f"[{row.ci95_low_or:.3f}, {row.ci95_high_or:.3f}] | {row.p_two_sided:.4g} |"
        )
    lines += [
        "",
        "## Pooled preregistered mixed-effects model",
        "",
        "The model uses fixed effects for attack budget, defense, deployment, and",
        "budget-by-defense interactions, with random intercepts for question and",
        "seed/graph. Reported tests are two-sided.",
        "",
        "| Contrast | Odds ratio | 95% CI | p |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in primary.itertuples():
        lines.append(
            f"| {row.contrast} | {row.odds_ratio:.3f} | "
            f"[{row.ci95_low_or:.3f}, {row.ci95_high_or:.3f}] | {row.p_two_sided:.4g} |"
        )
    lines += [
        "",
        "Secondary budget-specific defense contrasts are Holm-corrected across the",
        "nine predeclared pairwise comparisons and saved in `secondary_contrasts.csv`.",
        "",
        "## Critical budgets",
        "",
        "Critical budgets are the 50% crossing of nondecreasing logistic attack-success",
        "curves. Question-cluster bootstrap intervals use 2,000 resamples. Every point",
        "estimate is beyond the largest tested budget (4), so these values are",
        "model-based extrapolations and must not be presented as directly observed",
        "thresholds.",
        "",
        "| Model | Defense / ratio | Estimate | Bootstrap 95% interval | Finite bootstrap fraction |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for row in critical.itertuples():
        lines.append(
            f"| {row.model} | {row.defense} | {format_number(row.critical_budget_50pct)} | "
            f"[{format_number(row.bootstrap_ci95_low)}, {format_number(row.bootstrap_ci95_high)}] | "
            f"{row.bootstrap_finite_fraction:.3f} |"
        )
    lines += [
        "",
        "## Prediction-calibration boundary",
        "",
        "The repository's fitted physical model contains a weight-ratio prediction",
        "for Qwen3.5-9B (1.7666), not for the live Qwen3.5-27B deployment, and contains",
        "no fitted Mistral coupling. It is therefore suitable only as a directional",
        "reference here; a model-matched two-deployment quantitative calibration claim",
        "cannot be made from the available coupling file.",
        "",
        "## Confirmatory interpretation",
        "",
        "H1 is supported in the pooled model: each additional unauthenticated attacker",
        "raises the odds of an incorrect terminal majority under no defense. The H2",
        "primary contrast is also supported: downgrade lowers the pooled odds over the",
        "positive budgets. H3 is supported more strongly: drop lowers those odds further.",
        "Both deployment-specific critical-budget point ratios exceed one, matching the",
        "predicted direction, but every critical budget lies beyond the tested range and",
        "the Mistral multiplier interval includes one. H4 is therefore directional but",
        "not a precise or model-matched quantitative calibration result.",
        "",
        "## Technical notes",
        "",
        f"Mixed-model optimizer warnings recorded: {len(warnings_found)}.",
        "The locked source hashes are in `accepted_block_manifest.csv`; analysis",
        "metadata and package versions are in `analysis_metadata.json`.",
        "Independent MAP–variational-Bayes checks are saved in",
        "`glmm_stability_diagnostics.json`.",
    ]
    (output_dir / "CONFIRMATORY_ANALYSIS_REPORT.md").write_text("\n".join(lines) + "\n")


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest, data = load_locked_data(args.res_dir)
    validate_data(manifest, data)
    manifest.to_csv(args.output_dir / "accepted_block_manifest.csv", index=False)
    data.to_csv(args.output_dir / "accepted_episode_data.csv", index=False)

    rates = cell_rates(data)
    rates.to_csv(args.output_dir / "cell_rates.csv", index=False)
    model, result, fixed, covariance, warnings_found = fit_glmm(data)
    fixed.to_csv(args.output_dir / "glmm_fixed_effects.csv", index=False)
    primary, secondary = build_contrasts(model, result, covariance)
    primary.to_csv(args.output_dir / "primary_contrasts.csv", index=False)
    secondary.to_csv(args.output_dir / "secondary_contrasts.csv", index=False)

    deployment_rows = []
    deployment_warnings = []
    for model_name in MODEL_ORDER:
        local_model, local_result, _, local_covariance, local_warnings = fit_glmm(
            data[data["model"] == model_name], include_model=False
        )
        local_primary, _ = build_contrasts(
            local_model, local_result, local_covariance
        )
        local_primary.insert(0, "deployment", model_name)
        deployment_rows.append(local_primary)
        deployment_warnings.extend(local_warnings)
    deployment_primary = pd.concat(deployment_rows, ignore_index=True)
    deployment_primary.to_csv(
        args.output_dir / "deployment_specific_contrasts.csv", index=False
    )
    warnings_found.extend(deployment_warnings)

    critical, boot = estimate_critical_budgets(
        data, args.bootstrap, args.bootstrap_seed
    )
    critical.to_csv(args.output_dir / "critical_budgets.csv", index=False)
    boot.to_csv(args.output_dir / "critical_budget_bootstrap.csv", index=False)
    make_curve_plot(data, critical, args.output_dir / "confirmatory_curves.png")

    metadata = {
        "accepted_blocks": len(manifest),
        "accepted_episodes": len(data),
        "bootstrap_resamples": args.bootstrap,
        "bootstrap_seed": args.bootstrap_seed,
        "glmm_formula": "incorrect_terminal_majority ~ attack_budget * defense + model",
        "random_intercepts": ["question_id", "seed"],
        "optimizer_warnings": warnings_found,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "scipy_version": scipy.__version__,
        "statsmodels_version": statsmodels.__version__,
    }
    (args.output_dir / "analysis_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    write_report(
        args.output_dir,
        rates,
        deployment_primary,
        primary,
        secondary,
        critical,
        warnings_found,
    )
    print(f"analyzed {len(data)} accepted episodes from {len(manifest)} blocks")
    print(primary.to_string(index=False))
    print(critical.to_string(index=False))


if __name__ == "__main__":
    main()
