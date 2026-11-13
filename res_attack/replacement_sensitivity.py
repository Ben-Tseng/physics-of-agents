"""Sensitivity of H1-H3 to which attempt of the five replaced blocks is analysed.

Compares the accepted replacement blocks with the failed first attempts, under
both the preregistered shared-question specification and the post-review
question-within-deployment specification. Run from the repository root.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "res_attack"))
import analyze_confirmatory as A  # noqa: E402
from question_within_deployment_refit import fit_qwd  # noqa: E402

RES = ROOT / "res_attack"
OUT = RES / "confirmatory_analysis" / "question_within_deployment" / "replacement_sensitivity.csv"


def load(qwen_files, mistral_files):
    frames = []
    for model, files in (("qwen3.5-27b", qwen_files), ("mistral-small-2603", mistral_files)):
        for seed, name in files.items():
            frame = pd.read_csv(RES / name)
            frame["model"] = model
            frame["seed"] = seed
            frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def summarize(label, spec, model, result, cov):
    main, _ = A.build_contrasts(model, result, cov)
    return [{"data": label, "specification": spec, "contrast": r.contrast.split(":")[0],
             "odds_ratio": r.odds_ratio, "p_two_sided": r.p_two_sided} for r in main.itertuples()]


def main():
    accepted_q, accepted_m = dict(A.QWEN_FILES), dict(A.MISTRAL_FILES)
    failed_q, failed_m = dict(accepted_q), dict(accepted_m)
    for seed in (0, 4):
        failed_q[seed] = f"qwen_official_confirmatory_seed{seed}_results.csv"
    for seed in (1, 7, 9):
        failed_m[seed] = f"mistral_official_confirmatory_seed{seed}_results.csv"
    rows = []
    for label, data in (("accepted", load(accepted_q, accepted_m)),
                        ("failed_attempts_substituted", load(failed_q, failed_m))):
        m, r, _, cov, _ = A.fit_glmm(data)
        rows += summarize(label, "preregistered_shared_question", m, r, cov)
        m, r, cov, _, _ = fit_qwd(data)
        rows += summarize(label, "question_within_deployment", m, r, cov)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(pd.DataFrame(rows).round(4).to_string())


if __name__ == "__main__":
    main()
