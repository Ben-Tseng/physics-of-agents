# Manuscript insertion draft: confirmatory attack experiment

This document is written for insertion into an English-language manuscript.
Section and table numbers are placeholders and should be reconciled with the
main paper. The deployment amendment, executable matrix, accepted-block
manifest, and generated analysis tables are the authoritative sources.

## Methods

### Study design

We conducted a preregistered, two-deployment confirmatory experiment to test
whether unauthenticated external senders can move an LLM-agent collective toward
an incorrect terminal majority and whether relationship credentials reduce this
risk. The accepted deployments were Qwen3.5-27B through Alibaba Cloud Model
Studio's official Singapore endpoint and the version-pinned
`mistral-small-2603` deployment through Mistral AI's official API. The serving
stacks were different, so the two deployments were treated as independent
replications rather than as a controlled comparison of model families.

The confirmatory corpus contained 18 held-out, text-only mathematics questions.
Two test questions that required Asymptote diagrams were excluded before outcome
collection. Ground-truth labels were balanced across the two answer options
(nine A and nine B). Each deployment was evaluated on ten graph and attack seeds.
For every seed, the experiment crossed attack budgets of one, two, and four
external identities with three routing conditions: no authentication defense,
downgrade, and drop. A budget-zero control completed the ten-cell design. Each
cell therefore contained 180 episodes per deployment, and the complete accepted
matrix contained 3,600 episodes (Table 1).

| Design component | Frozen value |
| --- | --- |
| Deployments | Qwen3.5-27B; Mistral Small 4 (`mistral-small-2603`) |
| Held-out questions | 18 text-only mathematics questions, balanced 9/9 by answer |
| Honest agents | 8 |
| Nonzero graph entries | 28, corresponding to 14 undirected edges |
| Interaction steps | 2 synchronous updates |
| Opinion samples | 3 per agent and state |
| Attack budgets | 0, 1, 2, 4 external identities |
| Recipients per attacker | Up to 4 honest agents |
| Defense conditions | none, downgrade, drop |
| Seeds | 10 per deployment |
| Accepted episodes | 3,600 |

### External senders and relationship credentials

The honest population communicated over a signed, symmetric interaction graph.
Before routing an honest message, an HMAC-based credential authority issued a
token bound to the sender, receiver, signed relation, and step-specific nonce.
The receiver-side router verified this token before assigning the message to an
agreement-conditioned or disagreement-conditioned inbox. Across accepted data,
no honest credential failed verification.

Each external identity sent the objectively false option and claimed a positive
relationship. External senders had no valid relationship credential. For every
episode, each attacker targeted up to four honest agents. Target sets were drawn
deterministically from the frozen attack seed, episode identifier, and attack
budget. Honest and external messages were delivered before the next synchronous
opinion update.

The three routing conditions differed only in their treatment of an invalid or
missing credential. Under *none*, the receiver trusted the claimed relation and
routed the external message as an agreement source. Under *downgrade*, the
receiver retained the message but routed it to a relationship-unknown inbox.
Under *drop*, the receiver discarded the message. Valid honest messages retained
their verified signed relation under both authenticated conditions.

Each episode used eight honest agents, 28 nonzero entries in the symmetric
interaction matrix, two synchronous updates, and three opinion samples per agent
and state. Sampling temperature was 0.7. Requests used four workers, a 60-second
timeout, and zero API retries. Request starts were separated by at least 0.5
seconds for Qwen and 0.8 seconds for Mistral to respect deployment-specific rate
limits.

### Outcomes and technical quality gates

The primary outcome was an indicator that the terminal majority was incorrect.
A tied terminal population was not counted as attack success. Secondary outcomes
included the truth-aligned terminal margin, the fraction of correct agents,
incorrect consensus, raw zero spins, request and parsing errors, message-call
errors, credential-validation failures, and the fitted 50% critical budget.
A raw zero spin was retained as a technical failure and was not interpreted as a
substantive answer.

Collection proceeded in balanced model-by-seed blocks containing all ten cells
and all 180 corresponding episodes. A block was eligible only if it contained
180 episode files, raw zero spins did not exceed 1% of spin calls, unique-sender
message failures did not exceed 1% of message calls, and invalid honest
credentials equaled zero. A failing block was excluded in full. Five failed
blocks were replaced under dated, prospective full-block recollection amendments:
Qwen seeds 0 and 4, and Mistral seeds 1, 7, and 9. No episode from an excluded
predecessor was reused.

Across the 3,600 accepted episodes, 151 of 259,200 raw spin calls returned zero
(0.058%); all 151 were classified as request errors rather than exhausted parse
failures. Twenty-eight of 57,600 unique-sender message calls failed (0.049%).
There were no exhausted parse failures, no recovered parse retries, and no
invalid honest credentials.

### Statistical analysis

We fit the preregistered mixed-effects logistic model to the incorrect-terminal-
majority indicator. Fixed effects were attack budget, defense, deployment, and
the budget-by-defense interaction. Random intercepts accounted for held-out
question and seed/graph. The H1 contrast estimated the per-attacker budget slope
under no defense. The primary H2 contrast compared downgrade with no defense at
the mean of the positive tested budgets, (1 + 2 + 4) / 3 = 7/3. H3 used the same
contrast definition for drop versus no defense. Tests were two-sided, and we
report odds ratios (ORs), 95% confidence intervals (CIs), and p values.
Deployment-specific models with the same defense and budget structure were
reported before the pooled model.

Nine secondary, budget-specific pairwise defense contrasts were adjusted by the
Holm procedure. Critical budgets were defined as the budget at which a
nondecreasing logistic attack-success curve crossed 50%. Curves were estimated
separately by deployment and defense from the observed budgets 0, 1, 2, and 4.
Confidence intervals used 2,000 question-cluster bootstrap resamples with random
seed 20261106. Bootstrap samples without a finite crossing were retained as
infinite values. The downgrade-to-none critical-budget multiplier was used for
the directional H4 comparison.

The analysis locked all 20 admitted source files by SHA-256 hash before merging
them. Maximum a posteriori mixed-model fits completed without optimizer warnings.
Independent variational-Bayes fits produced closely aligned fixed-effect means,
providing a numerical stability check.

## Results

### Descriptive attack-success rates

Attack success increased with budget under no defense in both deployments
(Table 2). For Qwen3.5-27B, the observed incorrect-majority rate increased from
0.161 in the control condition to 0.194, 0.211, and 0.261 at budgets one, two,
and four. The corresponding Mistral rates increased from 0.211 to 0.294, 0.311,
and 0.361.

Downgrade and drop altered these trajectories differently across deployments.
For Qwen, downgrade rates were 0.200, 0.194, and 0.189, while drop rates were
0.178, 0.167, and 0.144. For Mistral, downgrade rates were 0.228, 0.272, and
0.322, while drop rates were 0.222, 0.222, and 0.239. Thus, authenticated
routing did not eliminate incorrect majorities, but it generally reduced their
growth relative to the no-defense condition.

| Deployment | Control | None: b=1 | None: b=2 | None: b=4 | Downgrade: b=1 | Downgrade: b=2 | Downgrade: b=4 | Drop: b=1 | Drop: b=2 | Drop: b=4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3.5-27B | 0.161 | 0.194 | 0.211 | 0.261 | 0.200 | 0.194 | 0.189 | 0.178 | 0.167 | 0.144 |
| Mistral Small 4 | 0.211 | 0.294 | 0.311 | 0.361 | 0.228 | 0.272 | 0.322 | 0.222 | 0.222 | 0.239 |

### Preregistered hypothesis tests

The pooled mixed-effects model supported H1. Under no defense, each additional
external identity increased the odds of an incorrect terminal majority by 22.9%
(OR 1.229, 95% CI 1.119 to 1.349, p = 1.45 x 10^-5). The primary H2 contrast
also supported an average downgrade effect over positive budgets: downgrade
reduced the odds relative to no defense (OR 0.794, 95% CI 0.639 to 0.986,
p = .0373). Drop produced a larger reduction for the H3 contrast (OR 0.592,
95% CI 0.474 to 0.740, p = 4.10 x 10^-6).

The deployment-specific models produced the same direction for all three
contrasts. For Qwen, the no-defense budget slope had OR 3.161 (95% CI 2.076 to
4.812, p = 7.99 x 10^-8), downgrade versus none had OR 0.275 (95% CI 0.113 to
0.667, p = .00433), and drop versus none had OR 0.057 (95% CI 0.021 to 0.153,
p = 1.26 x 10^-8). For Mistral, the corresponding ORs were 1.634 (95% CI 1.343
to 1.989, p = 9.29 x 10^-7), 0.558 (95% CI 0.358 to 0.870, p = .0101), and
0.283 (95% CI 0.178 to 0.449, p = 8.51 x 10^-8). These conditional estimates
describe each deployment separately; their magnitudes should not be interpreted
as a controlled comparison between model families.

| Scope | Contrast | OR | 95% CI | p |
| --- | --- | ---: | --- | ---: |
| Pooled | H1: budget slope under none | 1.229 | 1.119 to 1.349 | 1.45 x 10^-5 |
| Pooled | H2: downgrade vs none at mean positive budget | 0.794 | 0.639 to 0.986 | .0373 |
| Pooled | H3: drop vs none at mean positive budget | 0.592 | 0.474 to 0.740 | 4.10 x 10^-6 |
| Qwen3.5-27B | H1 | 3.161 | 2.076 to 4.812 | 7.99 x 10^-8 |
| Qwen3.5-27B | H2 | 0.275 | 0.113 to 0.667 | .00433 |
| Qwen3.5-27B | H3 | 0.057 | 0.021 to 0.153 | 1.26 x 10^-8 |
| Mistral Small 4 | H1 | 1.634 | 1.343 to 1.989 | 9.29 x 10^-7 |
| Mistral Small 4 | H2 | 0.558 | 0.358 to 0.870 | .0101 |
| Mistral Small 4 | H3 | 0.283 | 0.178 to 0.449 | 8.51 x 10^-8 |

After Holm correction across the nine secondary comparisons, drop differed from
no defense at budget two (OR 0.638, Holm-adjusted p = .000635) and budget four
(OR 0.406, Holm-adjusted p = 2.05 x 10^-5). The downgrade-versus-none contrast
at budget four had an unadjusted p value of .0250 but did not remain significant
after correction (Holm-adjusted p = .150). No other secondary comparison passed
the Holm-adjusted .05 threshold.

### Critical budgets and directional calibration

The monotone curves placed every 50% crossing beyond the maximum tested budget
of four (Figure 1). For Qwen, the estimated critical budget was 11.10 under no
defense (bootstrap 95% CI 4.72 to infinity), 48.98 under downgrade (11.37 to
infinity), and infinite under drop (infinity to infinity). The corresponding
downgrade-to-none multiplier was 4.41 (1.78 to infinity). For Mistral, the
estimated critical budgets were 7.18 under no defense (2.57 to 24.98), 8.93
under downgrade (4.07 to 23.73), and 35.18 under drop (12.40 to infinity). The
Mistral downgrade-to-none multiplier was 1.24 (0.60 to 2.18).

| Deployment | None | Downgrade | Drop | Downgrade / none |
| --- | ---: | ---: | ---: | ---: |
| Qwen3.5-27B | 11.10 [4.72, infinity] | 48.98 [11.37, infinity] | infinity [infinity, infinity] | 4.41 [1.78, infinity] |
| Mistral Small 4 | 7.18 [2.57, 24.98] | 8.93 [4.07, 23.73] | 35.18 [12.40, infinity] | 1.24 [0.60, 2.18] |

Both point multipliers were greater than one, which is consistent with the H4
direction. This evidence does not establish quantitative calibration. The
Mistral multiplier interval included one, the Qwen interval was open-ended, and
all underlying crossings required extrapolation beyond the tested range. The
available fitted coupling file also pertains to Qwen3.5-9B rather than the live
Qwen3.5-27B deployment and contains no Mistral coupling. A model-matched,
two-deployment calibration test was therefore not possible.

**Figure 1. Attack success by external-attacker budget and credential-routing
condition.** Points show observed incorrect-terminal-majority rates at budgets
0, 1, 2, and 4. Lines show separately fitted nondecreasing logistic curves. The
horizontal line marks 50% attack success, and the vertical line marks the
largest tested budget. Curves beyond budget four are extrapolations and are
shown to make that boundary explicit.

## Discussion

### Principal findings

Increasing the number of unauthenticated external identities raised the risk of
an incorrect terminal majority under no defense in both deployments. Routing
messages according to verified relationship credentials reduced this risk on
average. Downgrade preserved message content while removing the attacker's
unverified positive-relation claim, whereas drop removed the unauthenticated
message entirely. The pooled estimates support the predicted ordering: no
defense produced the greatest budget sensitivity, downgrade reduced average
attack odds, and drop produced the strongest reduction.

The deployment-specific trajectories were not identical. Qwen's observed attack
rate under downgrade remained approximately flat across the tested budgets,
while Mistral's rate increased but stayed below the no-defense curve. This
heterogeneity matters for interpretation. The experiment supports replication
of the directional defense effect across two deployed systems, but it does not
identify whether the different magnitudes arise from model family, provider,
serving configuration, or other deployment-level factors.

### Implications for interaction physics

The results connect an operational security mechanism to the interaction terms
used in collective-agent models. An unauthenticated sender can claim a trusted
relationship under the no-defense condition. Downgrade removes that relationship
label while leaving the message available, which weakens the sender's effective
position without requiring content classification. The positive point estimates
for the critical-budget multipliers are consistent with the prediction that
reducing effective coupling raises the attack budget needed to move the
collective.

That agreement is directional rather than quantitative. None of the fitted
curves crossed 50% within the observed budget range, and the live deployments do
not have matched coupling estimates in the existing physics fit. The present
experiment therefore supports the qualitative mechanism but does not validate a
numerical weight-ratio prediction. Testing that stronger claim requires coupling
estimates for the exact deployments and direct observations at budgets high
enough to bracket the 50% crossing.

### Limitations

The attack model covers external senders that lack valid relationship
credentials. It does not cover compromised honest agents, stolen credentials,
colluding authenticated nodes, or prompt injection inside an authenticated
message. The HMAC credential authority is an experimental implementation of
edge-bound provenance, not a production identity or key-management system.

The corpus contains text-only mathematics questions and binary answer choices.
Open-ended deliberation, subjective tasks, long-horizon interaction, and larger
collectives may produce different dynamics. The deployments also differ in both
model family and provider, which prevents an isolated causal interpretation of
the deployment coefficient.

The tested attack budgets ended at four. Every reported 50% critical budget is
therefore a model-based extrapolation, and several bootstrap intervals are
open-ended. H4 should be interpreted only as evidence about direction. Finally,
five model-seed blocks required complete technical recollection. Prospective
block-level gates prevented selective retention of favorable cells, but the
need for replacement documents the operational fragility of large API-based
multi-agent experiments.

### Conclusion

Across 3,600 accepted episodes, unauthenticated external senders increased the
risk of incorrect collective decisions as attack budget grew. Edge-bound
relationship credentials reduced this risk when invalid messages were
downgraded or dropped. These findings support H1 through H3 across two deployed
systems. The critical-budget shifts followed the predicted direction, but the
available budget range and coupling fits do not support a precise calibration
claim for H4.

## Reproducibility and submission statements

### Data and code availability

The accepted-block manifest, source-file hashes, merged episode table, analysis
script, model outputs, bootstrap draws, and figure source are available in
`res_attack/confirmatory_analysis/`. The analysis script explicitly enumerates
the 20 accepted blocks and does not glob excluded output directories.

### Ethics declaration

This experiment used language-model deployments and synthetic agent personas on
mathematics questions. It involved no human participants, personal data, or
intervention with human subjects.

### Author contributions

**To complete before submission.** Replace this note with a CRediT statement for
the actual author list. Do not infer roles from repository activity alone.

### Conflict of interest

**To complete before submission.** State the authors' actual conflicts or use
the target venue's no-conflict wording after author confirmation.

### Funding

**To complete before submission.** Insert verified grant and institutional
support information, or the target venue's no-specific-funding statement.

### AI assistance disclosure

**Draft for author and venue review.** OpenAI Codex was used to assist code
inspection, numerical cross-checking, and language editing. The authors retained
responsibility for the experimental design, analysis decisions, verification of
all numerical results, and final manuscript text. This statement must be adapted
to the disclosure policy of the target venue.
