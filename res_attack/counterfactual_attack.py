"""Counterfactual attack-budget experiment on the released objective episodes.

This is a fitted-model experiment, not a new LLM experiment. It keeps the
released graphs, persona/question fields, truth labels, and initial states, then
adds external false messages to the fitted five-coupling update.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from res.utils import MODELS, build_episodes, load_data  # noqa: E402


DEFAULT_KS = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40]


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30.0, 30.0)))


def fitted_step(phi, J, s, tau, fit, attack_count, attack_weight, draws):
    """One five-coupling update in the original A/B spin coordinates."""
    beta = fit["betas"]
    J_pos = np.maximum(J, 0.0)
    J_neg = np.minimum(J, 0.0)
    correct = s * tau[:, None] > 0
    s_true = np.where(correct, s, 0.0)
    s_false = np.where(correct, 0.0, s)

    h = phi @ np.asarray(fit["field"])
    h += beta["beta_pos_T"] * np.einsum("eij,ej->ei", J_pos, s_true)
    h += beta["beta_pos_F"] * np.einsum("eij,ej->ei", J_pos, s_false)
    h += beta["beta_neg_T"] * np.einsum("eij,ej->ei", J_neg, s_true)
    h += beta["beta_neg_F"] * np.einsum("eij,ej->ei", J_neg, s_false)
    h += beta["beta_0"] * np.einsum("eij,ej->ei", np.abs(J), s)

    # Every injected message claims a positive relationship and sends the
    # objectively false spin. Authentication changes only its channel weight.
    h += attack_count * attack_weight * (-tau[:, None])
    votes = (draws < sigmoid(h)[..., None]).mean(axis=-1) * 2.0 - 1.0
    return np.where(votes > 0.0, 1.0, -1.0)


def rollout(phi, J, s0, tau, fit, attack_count, attack_weight, draws):
    s = s0.copy()
    for step_draws in draws:
        s = fitted_step(
            phi, J, s, tau, fit, attack_count, attack_weight, step_draws
        )
    return s


def target_sequence(J, truth_field, max_k, d, strategy, pool, rng):
    """Nested attack placements: budget k is the first k attacker rows."""
    episodes, n, _ = J.shape
    targets = np.empty((episodes, max_k, d), dtype=np.int16)
    degree = (J > 0).sum(axis=2)
    for episode in range(episodes):
        if strategy == "random":
            candidates = np.arange(n)
        elif strategy == "hub":
            candidates = np.argsort(-degree[episode])[:pool]
        elif strategy == "weak":
            candidates = np.argsort(truth_field[episode])[:pool]
        else:
            raise ValueError(f"unknown targeting strategy: {strategy}")
        size = min(d, len(candidates))
        for attacker in range(max_k):
            chosen = rng.choice(candidates, size=size, replace=False)
            if size < d:
                chosen = np.resize(chosen, d)
            targets[episode, attacker] = chosen
    return targets


def counts_at_budget(targets, k, n):
    counts = np.zeros((targets.shape[0], n), dtype=float)
    if k == 0:
        return counts
    episode = np.repeat(np.arange(targets.shape[0]), k * targets.shape[2])
    node = targets[:, :k].reshape(-1)
    np.add.at(counts, (episode, node), 1.0)
    return counts


def crossing(ks, values, threshold=0.5):
    for left, right, y0, y1 in zip(ks[:-1], ks[1:], values[:-1], values[1:]):
        if y0 < threshold <= y1:
            return left + (threshold - y0) * (right - left) / (y1 - y0)
    if values[0] >= threshold:
        return float(ks[0])
    return None


def run_model(short, seed, strategy, ks, d, pool, trajectories, data):
    runs, banks, personas, graph_class, coupling_data = data
    model, label, _ = next(item for item in MODELS if item[2] == short)
    ep = build_episodes(model, "objective", runs, banks, personas, graph_class)
    test = ep["split"] == "test"
    phi, J = ep["phi"][test], ep["J"][test]
    s0, tau = ep["spins"][test, 0], ep["tau"][test]
    fit = coupling_data["params"][short]["objective"]["five"]
    truth_field = tau[:, None] * (phi @ np.asarray(fit["field"]))

    rng = np.random.default_rng(seed)
    draws = rng.random((8, len(phi), phi.shape[1], trajectories))
    targets = target_sequence(
        J, truth_field, max(ks), d=d, strategy=strategy, pool=pool, rng=rng
    )

    zero_count = np.zeros_like(s0)
    terminal_base = rollout(phi, J, s0, tau, fit, zero_count, 0.0, draws)
    base_margin = (terminal_base * tau[:, None]).mean(axis=1)
    eligible = base_margin > 0.0
    observed_margin = (ep["spins"][test, -1] * tau[:, None]).mean(axis=1)

    beta = fit["betas"]
    weights = {
        "none": beta["beta_pos_F"] + beta["beta_0"],
        "downgrade": beta["beta_0"],
        "drop": 0.0,
    }
    rows = []
    for defense, weight in weights.items():
        curve = []
        for k in ks:
            attack_count = counts_at_budget(targets, k, J.shape[1])
            terminal = rollout(
                phi, J, s0, tau, fit, attack_count, weight, draws
            )
            margin = (terminal * tau[:, None]).mean(axis=1)
            flips = eligible & (margin <= 0.0)
            rate = float(flips.sum() / max(eligible.sum(), 1))
            curve.append(rate)
            rows.append({
                "model_key": short,
                "model": label,
                "seed": seed,
                "strategy": strategy,
                "defense": defense,
                "k": k,
                "flip_rate": rate,
                "eligible_episodes": int(eligible.sum()),
                "test_episodes": int(len(phi)),
                "base_predicted_success_rate": float(eligible.mean()),
                "observed_success_rate": float((observed_margin > 0.0).mean()),
                "base_observed_majority_agreement": float(
                    ((base_margin > 0.0) == (observed_margin > 0.0)).mean()
                ),
                "attack_weight_per_message": float(weight),
            })
        for row in rows[-len(ks):]:
            row["k_star_50"] = crossing(ks, curve)
    return rows


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=[item[2] for item in MODELS])
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3])
    parser.add_argument("--strategies", nargs="+", default=["random"])
    parser.add_argument("--ks", nargs="+", type=int, default=DEFAULT_KS)
    parser.add_argument("--d", type=int, default=4)
    parser.add_argument("--pool", type=int, default=8)
    parser.add_argument("--trajectories", type=int, default=5)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "res_attack" / "results"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    runs, banks, personas, graph_class = load_data(ROOT / "data")
    coupling_data = json.loads((ROOT / "res" / "couplings.json").read_text())
    data = runs, banks, personas, graph_class, coupling_data

    rows = []
    for short in args.models:
        for seed in args.seeds:
            for strategy in args.strategies:
                print(f"model={short} seed={seed} strategy={strategy}", flush=True)
                rows.extend(
                    run_model(
                        short, seed, strategy, args.ks, args.d, args.pool,
                        args.trajectories, data
                    )
                )

    csv_path = args.output / "counterfactual_attack.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    config = {
        "models": args.models,
        "seeds": args.seeds,
        "strategies": args.strategies,
        "ks": args.ks,
        "d": args.d,
        "target_pool": args.pool,
        "thermal_trajectories": args.trajectories,
        "episode_filter": "objective test-question episodes",
        "interpretation": "fitted-model counterfactual; no new LLM calls",
    }
    (args.output / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
