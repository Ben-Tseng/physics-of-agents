"""Compare MAP and variational-Bayes GLMM fits for numerical stability."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM


def fit(frame, include_model):
    frame = frame.copy()
    frame["defense"] = pd.Categorical(frame["defense"], ["none", "downgrade", "drop"])
    frame["model"] = pd.Categorical(
        frame["model"], ["qwen3.5-27b", "mistral-small-2603"]
    )
    formula = "incorrect_terminal_majority ~ attack_budget * defense"
    if include_model:
        formula += " + model"
    model = BinomialBayesMixedGLM.from_formula(
        formula,
        {"question": "0 + C(question_id)", "seed_graph": "0 + C(seed)"},
        frame,
        vcp_p=0.5,
        fe_p=5.0,
    )
    map_result = model.fit_map(method="BFGS", minim_opts={"maxiter": 5000})
    vb_result = model.fit_vb(
        fit_method="BFGS", minim_opts={"maxiter": 5000}, verbose=False
    )
    return {
        "names": model.exog_names,
        "map_fe": map_result.fe_mean.tolist(),
        "map_fe_sd": map_result.fe_sd.tolist(),
        "map_log_sd": map_result.vcp_mean.tolist(),
        "map_optim": {
            "success": bool(map_result.optim_retvals.get("success", False)),
            "message": str(map_result.optim_retvals.get("message", "")),
            "gradient_max_abs": float(
                np.max(np.abs(map_result.optim_retvals.get("jac", np.array([np.nan]))))
            ),
        },
        "vb_fe": vb_result.fe_mean.tolist(),
        "vb_fe_sd": vb_result.fe_sd.tolist(),
        "vb_log_sd": vb_result.vcp_mean.tolist(),
        "vb_optim": {
            "success": bool(vb_result.optim_retvals.get("success", False)),
            "message": str(vb_result.optim_retvals.get("message", "")),
            "gradient_max_abs": float(
                np.max(np.abs(vb_result.optim_retvals.get("jac", np.array([np.nan]))))
            ),
        },
    }


def main():
    data = pd.read_csv(
        Path("res_attack/confirmatory_analysis/accepted_episode_data.csv")
    )
    diagnostics = {}
    for label, frame, include_model in [
        ("pooled", data, True),
        ("qwen3.5-27b", data[data.model == "qwen3.5-27b"], False),
        ("mistral-small-2603", data[data.model == "mistral-small-2603"], False),
    ]:
        result = fit(frame, include_model)
        diagnostics[label] = result
        print("\n", label)
        print(result)
    output = Path("res_attack/confirmatory_analysis/glmm_stability_diagnostics.json")
    output.write_text(json.dumps(diagnostics, indent=2) + "\n")
    print(f"\nwrote {output}")


if __name__ == "__main__":
    main()
