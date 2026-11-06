# Paper Outline and Evidence Map

## Structure pattern

Empirical IMRaD article with a separate Related Work section. Target length is 8,000 words, excluding abstracts, references, tables, figure captions, and appendices.

## Overview

The paper begins from a tension in LLM multi-agent systems: communication can improve collective reasoning, but the same social responsiveness creates an attack surface. It then distinguishes malicious content and corrupted-agent attacks from the identity-multiplication threat studied here. The Methods section defines a frozen, two-deployment confirmatory experiment in which unauthenticated external identities claim positive relationships and target an eight-agent signed network. Results test the attack-budget slope and two credential-aware routing policies before reporting extrapolative critical-budget estimates. The Discussion interprets the findings as evidence for deterministic trust enforcement at the communication boundary while preserving strict limits on cross-deployment and physical-model claims.

## Detailed outline

### 1. Introduction (~900 words)

**Purpose**: Establish the benefit-risk tension, define the external-identity threat, state the research question and preregistered hypotheses, and summarize the contribution without priority claims.

**Content**:

- **1.1 Communication as capability and attack surface**
  - Multi-agent debate and structured collaboration can improve reasoning.
  - Collective outcomes depend on social influence, topology, and protocol design.
- **1.2 From malicious messages to unauthenticated identities**
  - Existing work studies prompt injection, persuasive adversaries, or corrupted participants.
  - A sender that can mint identities and claim relationships changes apparent social evidence without compromising an enrolled agent.
- **1.3 Study question and contributions**
  - RQ: How do external-identity budget and credential-routing policy affect incorrect terminal majorities?
  - H1: attack success increases with budget under no defense.
  - H2-H3: downgrade and drop reduce attack odds relative to no defense.
  - H4: credential defenses increase the fitted critical budget directionally.
  - Contributions: threat model, deterministic credential-routing interventions, preregistered two-deployment experiment, and reproducible error-gated dataset.

**Sources**: S01-S02, S05-S09, S14-S20, S24-S26.

**Transition**: The gap statement requires separating collective-reasoning benefits, social failure modes, and identity/security mechanisms.

### 2. Related Work (~1,300 words)

**Purpose**: Position the study at the intersection of collective LLM reasoning, adversarial social influence, and authenticated communication.

**Content**:

- **2.1 Collective reasoning and communication topology**
  - Debate, role-playing, frameworks, and sparse communication.
  - Regime dependence and limits of multi-agent gains.
- **2.2 Conformity, consensus, and collective failure**
  - Opinion dynamics, majority effects, committed minorities, and belief entrenchment.
  - Distinguish descriptive collective dynamics from security evaluation.
- **2.3 Adversarial collaboration and indirect injection**
  - Corrupted participants, persuasive adversaries, and tool-output injection.
  - Why these are adjacent to but not identical with relationship spoofing by external identities.
- **2.4 Identity, credentials, and deterministic enforcement**
  - Sybil attacks, authenticated delegation, DID/VC systems, HMAC, and classical Byzantine assumptions.
  - Research gap: no controlled budget-response test of relationship-bound credential routing in LLM-agent collectives.

**Sources**: S02-S26, with S09 as counterevidence and S18-S23 anchoring the identity distinction.

**Transition**: The related-work synthesis yields a threat model that holds message content constant while manipulating identity budget and credential treatment.

### 3. Methods (~1,800 words)

**Purpose**: Make the confirmatory design, data-generation process, defenses, quality gates, and statistical tests fully reproducible.

**Content**:

- **3.1 Preregistration, deployments, and design boundaries**
  - Qwen3.5-27B via Alibaba Cloud Model Studio Singapore and `mistral-small-2603` via Mistral's official API.
  - Independent replications because serving stacks differ.
  - Frozen matrix: 10 seeds per deployment, 10 cells per seed, 180 episodes per block.
- **3.2 Tasks and honest-agent network**
  - Eighteen held-out text-only mathematics questions, balanced 9/9.
  - Eight honest agents, 28 nonzero symmetric graph entries, two synchronous updates, and three opinion samples.
- **3.3 External-identity threat model**
  - Every external identity sends the false option, claims a positive relationship, and targets up to four honest recipients.
  - Attack budgets 0, 1, 2, and 4; deterministic target selection.
  - Explain why the model is Sybil-like but does not claim a full real-world Sybil implementation.
- **3.4 Relationship credentials and routing policies**
  - HMAC token binds sender, receiver, signed relationship, and step nonce.
  - `none`: trust claimed relation; `downgrade`: retain in unknown-relation inbox; `drop`: discard.
  - Valid honest messages preserve their signed relationship.
- **3.5 Outcomes and technical quality gates**
  - Primary endpoint: incorrect terminal majority; ties are failures for the attacker.
  - Secondary outcomes and failure taxonomy.
  - Full-block admission and replacement rules; list five recollected blocks without reusing predecessor episodes.
- **3.6 Statistical analysis**
  - Mixed-effects logistic model, fixed and random effects, H1-H3 contrasts, Holm-adjusted secondary contrasts.
  - Deployment-specific estimates before pooled estimates.
  - Nondecreasing logistic curves, 2,000 question-cluster bootstraps, and infinite crossings.
  - H4 interpretation rules and model-mismatch restriction.

**Sources/evidence**: Frozen protocol and amendments; accepted-block manifest; analysis metadata; S20-S23 for security terminology. External literature does not substitute for the study's own design records.

**Transition**: The design yields three evidence layers: data integrity, confirmatory odds-ratio contrasts, and exploratory/directional critical-budget estimates.

### 4. Results (~1,600 words)

**Purpose**: Report prespecified results in a fixed order, separating technical validity, confirmatory tests, secondary contrasts, and extrapolative quantities.

**Content**:

- **4.1 Accepted data and technical validity**
  - 20 accepted blocks, 3,600 episodes.
  - 151/259,200 raw zero spins (0.058%), all request errors.
  - 28/57,600 message-call failures (0.049%), no exhausted parse failures, no invalid honest credentials.
- **4.2 Descriptive attack-success trajectories**
  - Table of rates by deployment, budget, and defense.
  - Describe patterns without inferential language.
- **4.3 Confirmatory H1-H3 tests**
  - Deployment-specific results first, then pooled model.
  - Pooled H1 OR 1.229; H2 OR 0.794; H3 OR 0.592, with full intervals and p values.
  - State that deployment magnitudes are not controlled model-family comparisons.
- **4.4 Secondary budget-specific contrasts**
  - Report Holm-adjusted results and distinguish adjusted from unadjusted significance.
- **4.5 Critical budgets and directional H4 evidence**
  - Report all crossings and intervals, including infinity.
  - Mark every crossing as beyond the maximum tested budget.
  - Conclude directional consistency only; no quantitative calibration claim.

**Evidence**: `cell_rates.csv`, `primary_contrasts.csv`, `secondary_contrasts.csv`, `deployment_specific_contrasts.csv`, `critical_budgets.csv`, `critical_budget_bootstrap.csv`, and `confirmatory_curves.png`.

**Transition**: The results establish that credential-aware routing changes collective vulnerability, but interpretation depends on distinguishing structural enforcement from model reasoning.

### 5. Discussion (~1,700 words)

**Purpose**: Interpret the findings against prior evidence, specify the security mechanism, and state what the experiment does and does not establish.

**Content**:

- **5.1 Principal findings**
  - Budget-dependent external influence exists under unverified relationship claims.
  - Both credential-aware policies reduce pooled odds; dropping has the larger pooled effect.
  - Directional critical-budget shifts are consistent with increased resistance.
- **5.2 Relation to collective-dynamics research**
  - Compare with debate benefits, conformity, committed minorities, and belief entrenchment.
  - Explain why counting senders is not equivalent to counting independent evidence.
- **5.3 Relation to agent-security research**
  - Contrast malicious enrolled agents and indirect prompt injection with external identity multiplication.
  - Explain why receiver-side verification is deterministic and does not ask an LLM to infer authenticity.
- **5.4 Downgrade versus drop as security-utility choices**
  - Downgrade preserves potentially useful but unverified content; drop minimizes influence.
  - Avoid claiming a universal ranking because only attack success, not a broad benign-utility suite, was tested.
- **5.5 Cross-deployment heterogeneity**
  - Same directional H1-H3 pattern, different magnitudes.
  - Serving-stack confounding prevents model-family causal interpretation.
- **5.6 Implications for multi-agent architecture**
  - Bind identity, relationship, recipient, and freshness outside the language model.
  - Treat graph relations as authorization data rather than natural-language claims.
  - Expose unknown or invalid provenance to routing policy before deliberation.

**Sources**: S01, S07-S20, S24-S26. S09 is used to prevent overclaiming general multi-agent benefits; S18-S23 support architectural implications.

**Transition**: Architectural implications remain bounded by the experimental scale, task domain, and extrapolative threshold analysis.

### 6. Limitations and Future Work (~400 words)

**Purpose**: Consolidate limitations rather than dispersing them as qualifications that readers may miss.

**Content**:

- Eighteen binary-answer mathematics questions and two official deployments.
- Maximum tested budget of four; all 50% crossings require extrapolation.
- Fixed graph size, two interaction steps, and standardized false-message content.
- HMAC credentials are an experimental mechanism, not a complete production identity system.
- No controlled model-family comparison and no broad benign-utility evaluation of downgrade/drop.
- H4 lacks model-matched coupling estimates for both deployments.
- Future work: larger budgets, adaptive attackers, credential compromise/replay, dynamic graphs, longer horizons, benign unknown senders, and matched physical-model calibration.

**Sources/evidence**: Study protocol and analysis report; S18-S20, S24-S26 for external-validity comparisons.

**Transition**: The conclusion states the narrow result supported by the experiment.

### 7. Conclusion (~300 words)

**Purpose**: Answer the research question directly without repeating every result.

**Content**:

- Unauthenticated external identities can shift collective decisions as their number increases.
- Relationship-bound credential verification followed by downgrade or drop reduces this influence across two independent deployments.
- Security-relevant social structure should be enforced at the message-routing boundary, not inferred from self-declared text.
- The evidence supports directional robustness improvement, not universal immunity or model-family ranking.

**Sources/evidence**: The paper's confirmatory results; no new literature introduced.

## Evidence map

| Claim or section | Assigned evidence | Status |
|---|---|---|
| Multi-agent interaction can improve reasoning | S05-S08 | Supported |
| Benefits are regime- and protocol-dependent | S09, S15 | Counterbalanced |
| Social influence can amplify incorrect positions | S10-S17 | Supported |
| Identity multiplication undermines redundancy | S20, S23 | Supported, foundational |
| Agent systems need explicit authentication/authorization | S18-S19, S21-S22 | Supported |
| External-input attacks are widespread in agent systems | S24-S26 | Supported |
| Relationship-credential routing lowers incorrect-majority odds | Primary study tables | Direct empirical evidence |
| Deployment magnitudes differ | Deployment-specific contrasts | Descriptive/conditional only |
| H4 quantitative calibration | Critical-budget tables plus coupling audit | Not established; directional only |

## Planned tables and figures

1. **Table 1**: Frozen experimental design and accepted sample.
2. **Table 2**: Descriptive attack-success rates by deployment, defense, and budget.
3. **Table 3**: Deployment-specific and pooled H1-H3 contrasts.
4. **Table 4**: Critical budgets and downgrade-to-none multipliers.
5. **Figure 1**: Experimental threat model and credential-routing paths (new schematic).
6. **Figure 2**: Observed rates and nondecreasing logistic curves (`confirmatory_curves.png`).
7. **Appendix tables**: Holm-adjusted secondary contrasts, block manifest, and technical-error taxonomy.

## Word-count summary

| Section | Target words |
|---|---:|
| Introduction | 900 |
| Related Work | 1,300 |
| Methods | 1,800 |
| Results | 1,600 |
| Discussion | 1,700 |
| Limitations and Future Work | 400 |
| Conclusion | 300 |
| **Total** | **8,000** |

Abstracts are excluded from the total: English 200-250 words and Traditional Chinese 300-500 characters, with 5-7 keywords in each language.

