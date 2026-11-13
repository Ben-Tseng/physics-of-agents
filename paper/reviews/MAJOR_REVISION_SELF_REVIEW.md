# Major-revision self-review

This adversarial self-review follows the `research-paper-writing` checklist.
Items marked `needs new experiment` have been removed from the paper's claimed
contribution rather than presented as resolved.

## Reverse outline

| Section | Function in the argument | Evidence carried |
|---|---|---|
| Abstract | Define bundled treatment, intervention, main estimates, robustness, and non-claims | H1–H3 estimates; GEE and leave-one-question-out summary |
| Introduction | Establish routing as a trust boundary and identify the provenance/authorization gap | Closest communication-attack, provenance, and credential literature |
| Related Work | Separate content attacks, topology defenses, provenance loss, and relationship authorization | References [16]–[30] |
| Methods 3.1–3.2 | Freeze deployment, task, graph, and episode procedure | Matrix and accepted-block design |
| Methods 3.3 | Define exposure arithmetic and the sender/message confounding boundary | Exact external template; 4b deliveries per step |
| Methods 3.4 | Separate enrollment, authentication, authorization, routing, and truth | HMAC edge token and three policies |
| Methods 3.5 | Explain technical gates and prospective replacement audit | Dated five-amendment sequence and accepted manifest |
| Methods 3.6 | Specify MAP/Wald inference, contrasts, robustness, and exploratory H4 | Exact priors, covariance source, GEE, prior grid, LOO, bootstrap |
| Results 4.1–4.4 | Report quality gates and preregistered H1–H3 | 3,600 episodes and primary/secondary contrasts |
| Results 4.5 | Test prior, functional-form, clustering, and question influence assumptions | Nine prior fits, categorical GEE, 18 LOO fits |
| Results 4.6 | Report critical budgets without treating extrapolation as confirmation | Point crossings and question bootstrap |
| Discussion | Interpret routing effect, not identity-only mechanism; state security-utility and trust limits | Claim–evidence reconciliation |
| Limitations | Foreground unresolved design and inference constraints | Confounding, 18 questions, approximate Wald, 18 clusters, deployment scope |
| Conclusion | State the supported routing claim and decisive next experiment | Bundled-treatment evidence only |

## Adversarial checklist

### 1. Contribution

| Question | Status | Evidence/action |
|---|---|---|
| What new knowledge is provided? | pass | Controlled evidence that relationship-route enforcement changes collective outcomes for unauthenticated external traffic, with two deployment replications. |
| Is the failure case meaningful? | pass | False relationship metadata changes which prompt channel receives peer traffic; adjacent work documents communication attacks and provenance erasure. |
| Is the idea non-obvious? | pass with scope | Cryptographic verification itself is established; the contribution is empirical linkage to collective outcomes and explicit relationship-route semantics, not a new MAC primitive. |
| Is the gain insightful? | pass | Downgrade retains content yet reduces pooled attack odds, indicating that route semantics matter independently of outright filtering within this design. |
| Is novelty explicit? | pass | Threat protocol, relationship-bound routing evaluation, block-level technical audit, and robustness findings are stated separately. |

### 2. Writing clarity

| Question | Status | Evidence/action |
|---|---|---|
| Can a reader reproduce the method? | pass | Exact prompt/channel appendix, literal token body, exposure arithmetic, source hashes, matrix, and analysis scripts are included. |
| Are technical details sufficient? | pass | Priors, optimizer, covariance block, Wald construction, contrasts, cluster definition, and bootstrap seed are specified. |
| Is every module motivated? | pass | Methods connect provenance ambiguity to credential verification and route selection. |
| Are terms consistent? | pass | Main causal term is `bundled sender/message budget`; `external sender` replaces identity-only language where mechanism matters. |
| Does each paragraph have one role? | pass | Reverse outline and paragraph-level edit completed. |

### 3. Experimental strength

| Question | Status | Evidence/action |
|---|---|---|
| Are effects meaningful? | pass with caution | H1 and H3 are stable; H2 is directionally stable but question-sensitive and is labeled weaker. |
| Is absolute performance sufficient? | pass for threat study | Outcomes remain below 50%; analysis evaluates changes in failure odds, not a claim of catastrophic takeover. |
| Are gains consistent across settings? | pass with scope | Signs replicate across two deployments and robustness models; magnitudes differ and no model-family ranking is made. |
| Are failure modes reported? | pass | Five excluded full blocks, request/message failures, H2 influence sensitivity, infinite threshold intervals, and audit limits are reported. |

### 4. Evaluation completeness

| Question | Status | Evidence/action |
|---|---|---|
| Fixed-volume sender-label ablation? | needs new experiment | Not available. Identity-specific claims were removed; orthogonal label/volume manipulation is the first future experiment. |
| Benign unknown-traffic utility baseline? | needs new experiment | Not available. No general downgrade-vs-drop ranking is claimed. |
| Closest recent baselines covered? | pass for positioning | AiTM, Prompt Infection, G-Safeguard, Trust Cascade, AgentDojo, and Agent Security Bench are compared by mechanism. They are not executable baselines for this distinct routing protocol. |
| Metrics sufficient? | pass with scope | Incorrect majority, margins, technical failures, credential validity, secondary contrasts, and exploratory thresholds are reported. Benign utility is explicitly absent. |
| Protocol documented? | pass | Prompt appendix and source hashes make the executed protocol auditable. |

### 5. Method design soundness

| Question | Status | Evidence/action |
|---|---|---|
| Is the setting realistic? | pass with scope | Self-declared relationship metadata is plausible, while account economics and provider identity proofing are explicitly excluded. |
| Hidden assumptions? | pass after disclosure | Enrollment, secret integrity, graph authorization, shared control coding, and message-volume coupling are explicit. |
| Robust without tuning? | pass | Policies are deterministic; prior-grid and categorical analyses preserve directions without scenario-specific retuning. |
| Do benefits outweigh complexity? | unresolved outside tested threat | Security benefit is measured; benign-open-system utility is not. The manuscript does not claim a universal net benefit. |
| Could net benefit be negative? | possible in open systems | Drop may reject useful unknown senders; this is stated and motivates the missing benign-traffic experiment. |

## Final claim–evidence decisions

- **Retained:** bundled budget effect under `none`; downgrade and drop contrasts;
  two-deployment directional replication; deterministic routing interpretation.
- **Qualified:** H2 inferential strength; GEE with 18 clusters; repository rather
  than third-party preregistration; H4 as exploratory extrapolation.
- **Removed/not claimed:** pure identity-count causality; benign-utility optimum;
  protection against authenticated malicious agents or stolen keys; universal
  model generalization; quantitative physical calibration.

## Remaining author-only submission blockers

1. Confirm affiliation and corresponding-author details.
2. Confirm CRediT, funding, and conflict-of-interest statements.
3. Select a venue and apply its template, page limit, and AI-disclosure policy.
4. If the venue requires third-party preregistration, describe the repository
   audit honestly rather than retroactively labeling it as independently
   registered.
