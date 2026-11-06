# Manuscript integration audit

## Scope

This audit maps the frozen confirmatory experiment to manuscript claims before
the prose is inserted into a paper. It covers the accepted 3,600-episode matrix
only. It does not treat eligibility screens, power screens, interrupted jobs,
excluded blocks, or legacy-provider runs as confirmatory evidence.

## Authoritative source order

The deployment specification in `formal_experiment_config.json` is historical.
Its Qwen3.5-9B/DeepInfra matrix was retired before the accepted experiment. The
manuscript must use the following sources, in this order:

1. `OFFICIAL_TWO_DEPLOYMENT_CONFIRMATORY_AMENDMENT.md` for the final deployment
   identities and frozen design.
2. `official_two_deployment_confirmatory_matrix.csv` for the executable cell
   definitions and runtime parameters.
3. `accepted_block_manifest.csv` for the 20 admitted model-seed blocks and their
   hashes.
4. `accepted_episode_data.csv` and the generated analysis tables for results.
5. Individual quality-gate reports for the disposition of replacement and
   excluded blocks.

## Claim-evidence map

| Manuscript claim | Evidence | Status |
| --- | --- | --- |
| The accepted matrix contains 20 model-seed blocks and 3,600 episodes. | `accepted_block_manifest.csv`; `analysis_metadata.json` | Verified |
| The experiment uses Qwen3.5-27B and Mistral Small 4 as separate deployments. | Official amendment; executable matrix | Verified |
| H1 is supported in the pooled model. | `primary_contrasts.csv` | Verified |
| Downgrade reduces pooled attack odds over positive budgets. | `primary_contrasts.csv` | Verified |
| Drop reduces pooled attack odds more strongly. | `primary_contrasts.csv` | Verified |
| Both critical-budget multipliers point above one. | `critical_budgets.csv` | Verified as a point-estimate direction only |
| The statistical-mechanics prediction is quantitatively calibrated. | No model-matched Qwen3.5-27B or Mistral coupling is available. | Not supported |
| The defenses are robust to compromised authenticated agents or stolen credentials. | Outside the frozen threat model. | Not supported |
| Results generalize beyond text-only mathematics questions. | No additional confirmatory corpus. | Not supported |

## Writing risks and required fixes

- Do not call the critical budgets observed thresholds. Every estimated crossing
  lies beyond the largest tested budget of four.
- Do not describe the two deployments as a controlled model-family comparison.
  Model family, provider, and serving stack vary together.
- Do not report the Qwen and Mistral conditional odds ratios as directly
  comparable effect sizes without noting question heterogeneity and
  non-collapsibility.
- Do not interpret full-block replacement as outcome-based exclusion. Five
  replacement blocks were recollected under prospectively documented technical
  gates, and their failed predecessors were excluded in full.
- Report H4 as directional and extrapolative. The Mistral multiplier interval
  includes one, the Qwen upper interval is open-ended, and the repository lacks
  live-deployment coupling estimates.

## Style audit

The manuscript insertion draft uses evidence-bound verbs, reports effect sizes
with intervals, and avoids promotional language. It removes throat-clearing
openers, unsupported significance language, and em dashes. No citation was
invented. All numerical claims are traceable to the generated analysis files.
