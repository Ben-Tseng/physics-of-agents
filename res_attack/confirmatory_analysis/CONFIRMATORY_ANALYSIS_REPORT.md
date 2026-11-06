# Frozen confirmatory analysis

This report analyzes only the 20 model-seed blocks that passed their
prospectively fixed technical gates (3,600 episodes). Replaced and
excluded blocks, power screens, pilots, and legacy-provider data are absent.

## Descriptive attack-success rates

| Model | Budget | Defense | Successes / N | Rate |
| --- | ---: | --- | ---: | ---: |
| mistral-small-2603 | 0 | none | 38/180 | 0.211 |
| mistral-small-2603 | 1 | downgrade | 41/180 | 0.228 |
| mistral-small-2603 | 1 | drop | 40/180 | 0.222 |
| mistral-small-2603 | 1 | none | 53/180 | 0.294 |
| mistral-small-2603 | 2 | downgrade | 49/180 | 0.272 |
| mistral-small-2603 | 2 | drop | 40/180 | 0.222 |
| mistral-small-2603 | 2 | none | 56/180 | 0.311 |
| mistral-small-2603 | 4 | downgrade | 58/180 | 0.322 |
| mistral-small-2603 | 4 | drop | 43/180 | 0.239 |
| mistral-small-2603 | 4 | none | 65/180 | 0.361 |
| qwen3.5-27b | 0 | none | 29/180 | 0.161 |
| qwen3.5-27b | 1 | downgrade | 36/180 | 0.200 |
| qwen3.5-27b | 1 | drop | 32/180 | 0.178 |
| qwen3.5-27b | 1 | none | 35/180 | 0.194 |
| qwen3.5-27b | 2 | downgrade | 35/180 | 0.194 |
| qwen3.5-27b | 2 | drop | 30/180 | 0.167 |
| qwen3.5-27b | 2 | none | 38/180 | 0.211 |
| qwen3.5-27b | 4 | downgrade | 34/180 | 0.189 |
| qwen3.5-27b | 4 | drop | 26/180 | 0.144 |
| qwen3.5-27b | 4 | none | 47/180 | 0.261 |

## Deployment-specific mixed-effects estimates

The preregistered reporting boundary requires deployment-specific estimates
before any pooled estimate. Each model below has the same fixed defense and
budget structure and random intercepts for question and seed/graph.

| Deployment | Contrast | Odds ratio | 95% CI | p |
| --- | --- | ---: | ---: | ---: |
| qwen3.5-27b | H1: budget slope under no defense | 3.161 | [2.076, 4.812] | 7.994e-08 |
| qwen3.5-27b | H2 primary: downgrade vs none at mean positive budget | 0.275 | [0.113, 0.667] | 0.004335 |
| qwen3.5-27b | H3: drop vs none at mean positive budget | 0.057 | [0.021, 0.153] | 1.257e-08 |
| mistral-small-2603 | H1: budget slope under no defense | 1.634 | [1.343, 1.989] | 9.286e-07 |
| mistral-small-2603 | H2 primary: downgrade vs none at mean positive budget | 0.558 | [0.358, 0.870] | 0.01009 |
| mistral-small-2603 | H3: drop vs none at mean positive budget | 0.283 | [0.178, 0.449] | 8.505e-08 |

## Pooled preregistered mixed-effects model

The model uses fixed effects for attack budget, defense, deployment, and
budget-by-defense interactions, with random intercepts for question and
seed/graph. Reported tests are two-sided.

| Contrast | Odds ratio | 95% CI | p |
| --- | ---: | ---: | ---: |
| H1: budget slope under no defense | 1.229 | [1.119, 1.349] | 1.453e-05 |
| H2 primary: downgrade vs none at mean positive budget | 0.794 | [0.639, 0.986] | 0.03728 |
| H3: drop vs none at mean positive budget | 0.592 | [0.474, 0.740] | 4.102e-06 |

Secondary budget-specific defense contrasts are Holm-corrected across the
nine predeclared pairwise comparisons and saved in `secondary_contrasts.csv`.

## Critical budgets

Critical budgets are the 50% crossing of nondecreasing logistic attack-success
curves. Question-cluster bootstrap intervals use 2,000 resamples. Every point
estimate is beyond the largest tested budget (4), so these values are
model-based extrapolations and must not be presented as directly observed
thresholds.

| Model | Defense / ratio | Estimate | Bootstrap 95% interval | Finite bootstrap fraction |
| --- | --- | ---: | ---: | ---: |
| qwen3.5-27b | none | 11.098 | [4.723, ∞] | 0.945 |
| qwen3.5-27b | downgrade | 48.985 | [11.370, ∞] | 0.646 |
| qwen3.5-27b | drop | ∞ | [∞, ∞] | 0.003 |
| mistral-small-2603 | none | 7.181 | [2.565, 24.976] | 1.000 |
| mistral-small-2603 | downgrade | 8.927 | [4.065, 23.729] | 1.000 |
| mistral-small-2603 | drop | 35.181 | [12.400, ∞] | 0.952 |
| qwen3.5-27b | downgrade_over_none_multiplier | 4.414 | [1.783, ∞] | 0.646 |
| mistral-small-2603 | downgrade_over_none_multiplier | 1.243 | [0.603, 2.180] | 0.998 |

## Prediction-calibration boundary

The repository's fitted physical model contains a weight-ratio prediction
for Qwen3.5-9B (1.7666), not for the live Qwen3.5-27B deployment, and contains
no fitted Mistral coupling. It is therefore suitable only as a directional
reference here; a model-matched two-deployment quantitative calibration claim
cannot be made from the available coupling file.

## Confirmatory interpretation

H1 is supported in the pooled model: each additional unauthenticated attacker
raises the odds of an incorrect terminal majority under no defense. The H2
primary contrast is also supported: downgrade lowers the pooled odds over the
positive budgets. H3 is supported more strongly: drop lowers those odds further.
Both deployment-specific critical-budget point ratios exceed one, matching the
predicted direction, but every critical budget lies beyond the tested range and
the Mistral multiplier interval includes one. H4 is therefore directional but
not a precise or model-matched quantitative calibration result.

## Technical notes

Mixed-model optimizer warnings recorded: 0.
The locked source hashes are in `accepted_block_manifest.csv`; analysis
metadata and package versions are in `analysis_metadata.json`.
Independent MAP–variational-Bayes checks are saved in
`glmm_stability_diagnostics.json`.
