"""Post-review refit of the pooled model with question-within-deployment intercepts.

The preregistered pooled model used one question intercept shared by both
deployments. Question difficulty is negatively correlated across deployments,
so this script refits the pooled model with a separate intercept for each
question within each deployment (same fixed effects, priors, and contrasts),
and adds influence and randomization diagnostics. These are post-review
analyses and are reported as such in the manuscript.

Run from the repository root:
    python res_attack/question_within_deployment_refit.py
"""

import itertools
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import logit
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "res_attack"))
from analyze_confirmatory import (  # noqa: E402
    DEFENSE_ORDER,
    MODEL_ORDER,
    build_contrasts,
    fit_glmm,
)

DATA = ROOT / "res_attack" / "confirmatory_analysis" / "accepted_episode_data.csv"
OUT = ROOT / "res_attack" / "confirmatory_analysis" / "question_within_deployment"
PERMUTATIONS = 20000
PERM_SEED = 20261111


def fit_qwd(data, vcp_p=0.5, fe_p=5.0, include_model=True):
    frame = data.copy()
    frame["defense"] = pd.Categorical(frame["defense"], DEFENSE_ORDER)
    frame["model"] = pd.Categorical(frame["model"], MODEL_ORDER)
    frame["question_in_deployment"] = frame["model"].astype(str) + "|" + frame["question_id"]
    formula = "incorrect_terminal_majority ~ attack_budget * defense"
    if include_model:
        formula += " + model"
    vcs = {"question_in_deployment": "0 + C(question_in_deployment)", "seed_graph": "0 + C(seed)"}
    model = BinomialBayesMixedGLM.from_formula(formula, vcs, frame, vcp_p=vcp_p, fe_p=fe_p)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = model.fit_map(method="BFGS", minim_opts={"maxiter": 2000})
    names = model.exog_names
    cov = np.asarray(result.cov_params())[: len(names), : len(names)]
    sds = np.exp(np.asarray(result.vcp_mean))
    return model, result, cov, sds, [str(w.message) for w in caught]


def contrasts(model, result, cov):
    main, secondary = build_contrasts(model, result, cov)
    return main, secondary


def tidy(main, label, extra=None):
    rows = []
    for _, r in main.iterrows():
        row = {"analysis": label, "contrast": r["contrast"].split(":")[0],
               "odds_ratio": r["odds_ratio"], "ci95_low_or": r["ci95_low_or"],
               "ci95_high_or": r["ci95_high_or"], "p_two_sided": r["p_two_sided"]}
        if extra:
            row.update(extra)
        rows.append(row)
    return rows


def informative_questions(data):
    rows = []
    for model_name, sub in data.groupby("model"):
        rates = sub.groupby("question_id")["incorrect_terminal_majority"].mean()
        rows.append({
            "model": model_name,
            "questions": len(rates),
            "always_correct_majority": int((rates == 0).sum()),
            "always_incorrect_majority": int((rates == 1).sum()),
            "informative": int(((rates > 0) & (rates < 1)).sum()),
            "informative_ids": ";".join(sorted(rates[(rates > 0) & (rates < 1)].index)),
        })
    return pd.DataFrame(rows)


def permutation_test(data, policy, rng):
    """Within question x seed x budget, swap the none/policy labels (sign flip)."""
    sub = data[(data["attack_budget"] > 0) & data["defense"].isin(["none", policy])]
    wide = sub.pivot_table(index=["question_id", "seed", "attack_budget"], columns="defense",
                           values="incorrect_terminal_majority", aggfunc="first").dropna()
    diff = (wide["none"] - wide[policy]).to_numpy()
    observed = diff.mean()
    nonzero = diff[diff != 0]
    flips = rng.choice([-1.0, 1.0], size=(PERMUTATIONS, nonzero.size))
    null = (flips * np.abs(nonzero)).sum(axis=1) / diff.size
    one_sided = (np.sum(null >= observed) + 1) / (PERMUTATIONS + 1)
    two_sided = (np.sum(np.abs(null) >= abs(observed)) + 1) / (PERMUTATIONS + 1)
    return observed, one_sided, two_sided, int(nonzero.size), int(diff.size)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(DATA)
    meta = {"statsmodels_note": "fit_map BFGS, vcp_p=0.5, fe_p=5.0 unless stated", "warnings": {}}

    # 1. Informative questions
    info = informative_questions(data)
    info.to_csv(OUT / "informative_questions.csv", index=False)

    # Cross-deployment difficulty correlation
    rates = data.groupby(["model", "question_id"])["incorrect_terminal_majority"].mean().unstack(0)
    clipped = rates.clip(0.5 / 180, 1 - 0.5 / 180)
    meta["question_logit_rate_correlation"] = float(np.corrcoef(logit(clipped.iloc[:, 0]), logit(clipped.iloc[:, 1]))[0, 1])

    # 2. Primary refit vs preregistered specification
    rows = []
    m0, r0, _, cov0, w0 = fit_glmm(data)
    main0, _ = contrasts(m0, r0, cov0)
    rows += tidy(main0, "pooled_preregistered_shared_question")
    m1, r1, cov1, sds1, w1 = fit_qwd(data)
    main1, sec1 = contrasts(m1, r1, cov1)
    rows += tidy(main1, "pooled_question_within_deployment")
    meta["warnings"]["primary_qwd"] = w1
    meta["qwd_random_effect_sds"] = {"question_in_deployment": float(sds1[0]), "seed_graph": float(sds1[1])}
    pd.DataFrame(rows).to_csv(OUT / "pooled_contrasts.csv", index=False)
    sec1.to_csv(OUT / "secondary_contrasts_qwd.csv", index=False)
    fe = pd.DataFrame({"term": m1.exog_names, "estimate_log_odds": np.asarray(r1.fe_mean),
                       "standard_error": np.sqrt(np.diag(cov1))})
    fe.to_csv(OUT / "fixed_effects_qwd.csv", index=False)

    # 3. Prior grid on the refit
    grid = []
    for fe_p, vcp_p in itertools.product([2.5, 5.0, 10.0], [0.1, 0.25, 0.5]):
        m, r, c, s, w = fit_qwd(data, vcp_p=vcp_p, fe_p=fe_p)
        mn, _ = contrasts(m, r, c)
        grid += tidy(mn, "prior_grid", {"fe_prior_sd": fe_p, "log_re_sd_prior_sd": vcp_p,
                                         "question_sd": float(s[0]), "seed_sd": float(s[1]),
                                         "warnings": len(w)})
    pd.DataFrame(grid).to_csv(OUT / "prior_grid_qwd.csv", index=False)

    # 4. Leave-one-question-out on the refit (question removed from both deployments)
    loqo = []
    for q in sorted(data["question_id"].unique()):
        m, r, c, s, w = fit_qwd(data[data["question_id"] != q])
        mn, _ = contrasts(m, r, c)
        loqo += tidy(mn, "leave_one_question_out", {"omitted": q, "warnings": len(w)})
    pd.DataFrame(loqo).to_csv(OUT / "leave_one_question_out_qwd.csv", index=False)

    # 5. Deployment-specific: prior sensitivity and leave-two-informative-out
    dep = []
    for model_name in MODEL_ORDER:
        sub = data[data["model"] == model_name]
        for vcp_p in [0.1, 0.25, 0.5]:
            m, r, c, s, w = fit_qwd(sub, vcp_p=vcp_p, include_model=False)
            mn, _ = contrasts(m, r, c)
            dep += tidy(mn, "deployment_prior", {"model": model_name, "log_re_sd_prior_sd": vcp_p,
                                                 "question_sd": float(s[0]), "warnings": len(w)})
        ids = info.loc[info["model"] == model_name, "informative_ids"].iloc[0].split(";")
        if len(ids) <= 4:
            for pair in itertools.combinations(ids, 2):
                m, r, c, s, w = fit_qwd(sub[~sub["question_id"].isin(pair)], include_model=False)
                mn, _ = contrasts(m, r, c)
                dep += tidy(mn, "deployment_leave_two_informative_out",
                            {"model": model_name, "omitted": "+".join(pair), "warnings": len(w)})
    pd.DataFrame(dep).to_csv(OUT / "deployment_sensitivity.csv", index=False)

    # 6. Within-question randomization tests
    rng = np.random.default_rng(PERM_SEED)
    perm = []
    for model_name in MODEL_ORDER:
        sub = data[data["model"] == model_name]
        for policy in ["downgrade", "drop"]:
            obs, p1, p2, nz, n = permutation_test(sub, policy, rng)
            perm.append({"model": model_name, "contrast": f"none minus {policy}",
                         "mean_risk_difference": obs, "p_one_sided": p1, "p_two_sided": p2,
                         "discordant_pairs": nz, "pairs": n, "permutations": PERMUTATIONS})
    pd.DataFrame(perm).to_csv(OUT / "within_question_permutation.csv", index=False)

    # 7. Drop versus control (manipulation check)
    chk = []
    for model_name in MODEL_ORDER:
        sub = data[data["model"] == model_name]
        ctrl = sub[sub["attack_budget"] == 0]["incorrect_terminal_majority"].mean()
        for b in [1, 2, 4]:
            d = sub[(sub["attack_budget"] == b) & (sub["defense"] == "drop")]["incorrect_terminal_majority"].mean()
            chk.append({"model": model_name, "budget": b, "control_rate": ctrl, "drop_rate": d, "drop_minus_control": d - ctrl})
    pd.DataFrame(chk).to_csv(OUT / "drop_vs_control.csv", index=False)

    (OUT / "metadata.json").write_text(json.dumps(meta, indent=2))
    print("done")


if __name__ == "__main__":
    main()
