# Statistical appendix

## Primary pooled MAP fixed effects

Reference levels are `defense=none` and `model=qwen3.5-27b`. Intervals and p
values are two-sided normal-Wald quantities from the fixed-effect block of the
Laplace/MAP covariance matrix.

| Term | Log-odds estimate | SE | OR | 95% Wald CI | p |
|---|---:|---:|---:|---:|---:|
| Intercept | -2.6288 | 0.4910 | 0.0722 | [0.0276, 0.1889] | 8.60e-8 |
| Downgrade main effect | 0.0214 | 0.2083 | 1.0216 | [0.6791, 1.5367] | .9184 |
| Drop main effect | 0.0041 | 0.2131 | 1.0041 | [0.6613, 1.5248] | .9845 |
| Mistral deployment | 0.5773 | 0.0915 | 1.7813 | [1.4889, 2.1310] | 2.75e-10 |
| Bundled budget | 0.2059 | 0.0475 | 1.2287 | [1.1194, 1.3485] | 1.45e-5 |
| Budget x downgrade | -0.1082 | 0.0809 | 0.8975 | [0.7659, 1.0516] | .1810 |
| Budget x drop | -0.2264 | 0.0836 | 0.7974 | [0.6769, 0.9394] | .00678 |

The pooled MAP log random-effect SDs were 0.6681 for question and -2.2915 for
seed/graph, corresponding to SDs 1.9505 and 0.1011. The optimizer terminated
successfully with maximum absolute gradient `6.91e-6`.

The deployment coefficient is an adjustment term, not a controlled model-family
effect, because deployment, model, provider, and serving stack differ together.
The defense main effects correspond to the model's budget-zero intercept even
though the shared budget-zero control was coded only as `defense=none`; the
prespecified H2/H3 contrasts combine each main effect with its interaction at
budget 7/3.

## Prior sensitivity

The pooled model was refit over nine prior combinations: fixed-effect prior SD
in `{2.5, 5, 10}` crossed with log-random-effect-SD prior SD in
`{0.1, 0.25, 0.5}`.

| Contrast | OR range | p-value range |
|---|---:|---:|
| H1 | 1.224–1.229 | 1.4e-5–1.7e-5 |
| H2 | 0.793–0.796 | .0365–.0387 |
| H3 | 0.592–0.595 | 4e-6–5e-6 |

All nine fits completed without optimizer warnings. Full-precision results are
in `res_attack/confirmatory_analysis/major_revision/prior_sensitivity.csv`.

## Categorical-cell question-cluster sensitivity

The sensitivity GEE treated the ten experimental cells categorically, included
deployment and seed fixed effects, used an exchangeable working correlation,
and estimated sandwich covariance over 18 question clusters.

| Contrast | OR | 95% robust CI | p |
|---|---:|---:|---:|
| None budget 1 vs control | 1.423 | [1.077, 1.882] | .0132 |
| None budget 2 vs control | 1.557 | [1.070, 2.267] | .0209 |
| None budget 4 vs control | 1.998 | [1.244, 3.209] | .00419 |
| Downgrade vs none, mean positive-budget log-odds contrast | 0.817 | [0.701, 0.952] | .00966 |
| Drop vs none, mean positive-budget log-odds contrast | 0.647 | [0.484, 0.866] | .00336 |

The GEE converged. With only 18 clusters, the sandwich intervals should be read
as sensitivity evidence rather than a replacement for the preregistered model.

## Leave-one-question-out influence analysis

Across 18 omitted-question refits, all effect directions were retained. H1 ORs
ranged from 1.186 to 1.268 (p range 3.31e-6 to .000486); H2 ORs ranged from
0.767 to 0.840 (p range .0250 to .126); and H3 ORs ranged from 0.544 to 0.640
(p range 7.78e-7 to .000167). H2 therefore has stable direction but materially
greater task-set sensitivity than H1 or H3.

## Prospective sensitivity boundary

The original design freeze reported an approximate minimum detectable
two-proportion risk difference of 0.148 at two-sided alpha .05 and 80% power.
That calculation did not simulate the full crossed question/seed mixed-effects
design. It is retained as a planning record, not presented as achieved power or
as evidence for a null result.

## Post-review pooled specification (question within deployment)

Added after the 2026-11-11 pre-submission review. The preregistered pooled model
shares one question intercept across deployments, but question difficulty is
negatively correlated across deployments (correlation of clipped logit question
rates −0.486). The revised pooled model keeps the same fixed effects, priors,
optimizer, and contrasts and replaces the shared question intercept with a
question-within-deployment intercept; the seed intercept remains shared because
seed s used identical graphs and targets in both deployments.

| Contrast | Shared question (preregistered) | Question within deployment |
|---|---|---|
| H1 budget slope under none | OR 1.229 [1.119, 1.349], p = 1.45e-5 | OR 1.900 [1.591, 2.269], p = 1.33e-12 |
| H2 downgrade vs none at 7/3 | OR 0.794 [0.639, 0.986], p = .0373 | OR 0.480 [0.325, 0.710], p = 2.34e-4 |
| H3 drop vs none at 7/3 (check) | OR 0.592 [0.474, 0.740], p = 4.10e-6 | OR 0.200 [0.132, 0.303], p = 2.77e-14 |

Random-effect SDs in the revised model: question within deployment 3.66, seed
0.136 (both prior-dependent; see manuscript Section 3.6).

Informative questions (outcome varied across the 100 episodes of a question):
Qwen 4 of 18 (`math_test_132`, `math_test_157`, `math_test_21`,
`math_test_426`); Mistral 10 of 18.

Within-question randomization tests (sign flip within question × seed × budget,
20,000 draws, seed 20261111), mean paired risk difference and two-sided p:
Qwen none − downgrade 0.028 (p = .0017), none − drop 0.059 (p < .0001);
Mistral none − downgrade 0.048 (p = .0043), none − drop 0.094 (p < .0001).

Outputs: `res_attack/confirmatory_analysis/question_within_deployment/`
(`pooled_contrasts.csv`, `secondary_contrasts_qwd.csv`, `fixed_effects_qwd.csv`,
`prior_grid_qwd.csv`, `leave_one_question_out_qwd.csv`,
`deployment_sensitivity.csv`, `within_question_permutation.csv`,
`drop_vs_control.csv`, `replacement_sensitivity.csv`, `informative_questions.csv`).
Scripts: `res_attack/question_within_deployment_refit.py`,
`res_attack/replacement_sensitivity.py`. The primary refit and prior grid were
run with statsmodels 0.14.4; the remaining outputs were produced with
statsmodels 0.15.0, which reproduces the 0.14.4 primary contrasts to eight
significant digits.
