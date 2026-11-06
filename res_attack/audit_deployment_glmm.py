"""Reproduce deployment-specific GLMMs and compare fitted and observed cell rates."""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "res_attack" / "confirmatory_analysis" / "accepted_episode_data.csv"
OUTPUT = ROOT / "paper" / "deployment_glmm_reproducibility_check.csv"
MODELS = ["qwen3.5-27b", "mistral-small-2603"]
DEFENSES = ["none", "downgrade", "drop"]


def fit_deployment(frame):
    frame = frame.copy()
    frame["defense"] = pd.Categorical(frame["defense"], DEFENSES)
    model = BinomialBayesMixedGLM.from_formula(
        "incorrect_terminal_majority ~ attack_budget * defense",
        {"question": "0 + C(question_id)", "seed_graph": "0 + C(seed)"},
        frame,
        vcp_p=0.5,
        fe_p=5.0,
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = model.fit_map(method="BFGS", minim_opts={"maxiter": 2000})
    if caught:
        raise RuntimeError("; ".join(str(item.message) for item in caught))

    linear_predictor = model.exog @ result.fe_mean + model.exog_vc @ result.vc_mean
    frame["fitted_conditional_probability"] = 1 / (1 + np.exp(-linear_predictor))
    return model, result, frame


def main():
    data = pd.read_csv(DATA)
    rows = []
    for deployment in MODELS:
        model, result, fitted = fit_deployment(data[data["model"] == deployment])
        fixed = dict(zip(model.exog_names, result.fe_mean))
        grouped = fitted.groupby(["attack_budget", "defense"], observed=True)
        for (budget, defense), cell in grouped:
            rows.append(
                {
                    "deployment": deployment,
                    "attack_budget": int(budget),
                    "defense": defense,
                    "observed_rate": cell["incorrect_terminal_majority"].mean(),
                    "posterior_conditional_fitted_rate": cell[
                        "fitted_conditional_probability"
                    ].mean(),
                    "conditional_none_budget_log_odds_slope": fixed["attack_budget"],
                    "conditional_none_budget_odds_ratio": np.exp(
                        fixed["attack_budget"]
                    ),
                    "question_random_effect_sd": np.exp(result.vcp_mean[0]),
                    "seed_random_effect_sd": np.exp(result.vcp_mean[1]),
                    "optimizer_success": bool(result.optim_retvals["success"]),
                }
            )
    pd.DataFrame(rows).to_csv(OUTPUT, index=False)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
