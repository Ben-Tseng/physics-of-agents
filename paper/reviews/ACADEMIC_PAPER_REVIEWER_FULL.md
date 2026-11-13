# Full Multi-Perspective Peer Review

**Manuscript:** *Authenticated Relationship Routing Mitigates External-Identity Attacks in LLM-Agent Collectives*  
**Review date:** 2026-11-07  
**Mode:** `academic-paper-reviewer` full review  
**Editorial calibration:** selective Q1/Q2 AI-security / agent-systems venue  
**Manuscript state:** pre-submission

## Process disclosure

The manuscript was treated as read-only. Methodology, domain, and cross-disciplinary reviewers examined the paper independently and did not read one another's reports before synthesis. The EIC and Devil's Advocate roles were executed as role-separated reviews by the orchestrator. The local skill installation did not contain the referenced v3.6.2 sprint-contract JSON/schema, so the documented full-mode rubrics and editorial decision standards were used instead. This is a simulated pre-submission review, not a substitute for human peer review.

---

# Phase 0: Field Analysis and Reviewer Configuration

## Field analysis

| Dimension | Assessment |
|---|---|
| Primary discipline | AI security / trustworthy multi-agent systems |
| Secondary disciplines | distributed authorization; statistical evaluation of LLM systems; collective intelligence |
| Research paradigm | quantitative confirmatory computational experiment |
| Methodology | crossed experimental design, hierarchical binary-outcome modeling, cluster bootstrap |
| Target tier | strong specialized Q1/Q2 venue; not yet ready for a top general-security venue |
| Paper maturity | pre-submission, with several substantive revisions still required |

## Candidate venue families

1. **Computers & Security** — strongest fit if the paper emphasizes the security boundary, threat model, and deployment protocol.
2. **ACM Transactions on Intelligent Systems and Technology** — plausible if the agent-systems contribution and reproducible evaluation are emphasized.
3. **Transactions on Machine Learning Research** — plausible if the empirical methodology, open artifacts, and robustness analyses are strengthened.

## Reviewer configuration cards

### EIC

**Identity:** Senior editor for a selective AI-security and trustworthy-agent-systems venue.  
**Focus:** strategic contribution, scope, novelty, claim discipline, submission readiness.  
**Blind spot:** does not independently adjudicate the GLMM implementation.

### Reviewer 1 — Methodology

**Identity:** Quantitative-methods reviewer specializing in hierarchical binary models, simulation-based power, and reproducibility of API-mediated AI experiments.  
**Focus:** replication units, GLMM inference, priors, uncertainty, functional-form sensitivity, recollection rules.  
**Blind spot:** does not judge whether all domain literature is covered.

### Reviewer 2 — Domain

**Identity:** Senior researcher in LLM multi-agent security, distributed authorization, and trustworthy agentic systems.  
**Focus:** novelty, security-property definitions, threat-model positioning, literature integration.  
**Blind spot:** does not rederive the statistical model.

### Reviewer 3 — Cross-disciplinary / Practical

**Identity:** Security-systems researcher specializing in cryptographic authorization, distributed trust boundaries, and operational AI-agent infrastructure.  
**Focus:** deployability, trust assumptions, prompt-channel implementation, security-utility tradeoffs, stakeholders, ethics.  
**Blind spot:** does not determine statistical coverage properties.

### Devil's Advocate

**Identity:** Adversarial reviewer tasked with constructing the strongest counter-narrative and locating logic-chain failures.  
**Focus:** identity/message-volume confounding, bundled-treatment interpretation, alternative explanations, overgeneralization.  
**Blind spot:** does not score journal fit or perform literature completeness checks.

---

# Phase 1: Independent Review Reports

## EIC Review Report

### Recommendation

**Major Revision** — confidence **4/5**.

### Summary assessment

The manuscript presents a timely, technically disciplined study of receiver-side provenance enforcement in LLM-agent collectives. Its most persuasive contribution is the distinction between semantic moderation and deterministic relationship authorization: the router, not the LLM, decides whether an unverified relationship receives privileged social semantics. The frozen block design, two official deployments, explicit technical gates, and unusually careful limitation language make the paper substantially stronger than many API-mediated agent evaluations.

The paper is not yet ready for acceptance at a selective venue. The central construct is nominal external-identity budget, but increasing that budget also increases the number of false-message instances; the experiment therefore does not isolate identity multiplicity from exposure volume. The statistical analysis is promising but needs more transparent uncertainty construction and sensitivity analyses. The operational security story also requires exact prompt/channel and credential-protocol specifications. These issues do not invalidate the bounded finding that the tested routing policies reduce the tested attack, but they affect what the paper can claim is novel and why the effect occurs.

### Strengths

1. **Clear architectural contribution:** Sections 3.3-3.4 and 5.6 place verification before prompt construction and distinguish authentication, authorization, routing, and semantic judgment.
2. **Strong experimental governance:** Section 3.5 uses whole-block admission and replacement, preserves excluded predecessors, and locks accepted sources with hashes.
3. **Responsible claim boundaries:** Sections 4.5-6 repeatedly mark the critical-budget estimates as extrapolative and avoid model-family causal claims.
4. **High reproducibility potential:** software versions, priors, bootstrap seed, deployment boundaries, failure rates, and artifact paths are disclosed.

### Weaknesses

1. **Identity multiplicity is not separated from message volume (Major):** add a fixed-exposure control, such as one sender producing the same number of message instances as multiple identities, or narrow all causal language to the bundled external-identity/message-exposure treatment.
2. **The novelty hierarchy is blurred (Major):** the paper empirically evaluates provenance-aware routing; it does not introduce HMAC, solve enrollment, or prove that receiver-specific relationship binding is necessary. State this hierarchy explicitly in the Introduction and Conclusion.
3. **Submission package is not self-contained (Major):** provide persistent preregistration/amendment links, stable artifact version, exact prompts, and protocol/test-vector details.
4. **H4 occupies too much conceptual space (Minor/Major):** every crossing is outside the observed range. Recast H4 as exploratory or move it to a secondary analysis unless higher budgets are collected.

### Dimension scores

| Dimension | Score |
|---|---:|
| Originality | 80 |
| Methodological rigor | 72 |
| Evidence sufficiency | 73 |
| Argument coherence | 86 |
| Writing quality | 89 |
| **Weighted average** | **78.5** |

The numerical score falls in the minor-revision band, but the recommendation is elevated to Major Revision because the construct-validity and inferential-transparency issues affect the central contribution.

---

## Reviewer 1 — Methodology

### Recommendation

**Major Revision** — confidence **4/5**.

### Summary assessment

The crossed experiment and complete-block admission protocol are methodologically strong. Separating request errors, parse failures, message-call failures, and invalid honest credentials is especially important for interpreting a treatment that intentionally drops traffic. The main weakness is inferential calibration rather than data collection. The paper reports frequentist-looking confidence intervals and p values from a penalized Bayesian MAP GLMM without fully specifying their construction. The effective generalization dimensions are 18 questions and 10 seeds per deployment, not simply 3,600 episodes. The linear raw-budget effect, random-intercept-only structure, and prior sensitivity require robustness checks.

### Principal strengths

1. Direct alignment between the research question and crossed manipulations.
2. Prospective full-block replacement limits selective retention.
3. Technical and substantive failure modes are separated.
4. Primary ORs, intervals, and exact p values are reported, and conditional/marginal distinctions are explained.
5. Infinite critical-budget crossings are retained instead of artificially capped.

### Required methodological revisions

1. **Define the inferential construction (Major):** give the exact equations/code path from `fit_map` and `cov_params()` to SEs, intervals, contrasts, and two-sided p values. Use terminology consistent with penalized-MAP Wald inference or replace it with an explicitly Bayesian or bootstrap interpretation.
2. **Add simulation-based power/precision analysis (Major):** base it on 18 questions, 10 seeds per deployment, and plausible random-effect variances. Report minimum detectable effects or expected interval widths for H1-H3.
3. **Test functional-form and treatment heterogeneity (Major):** refit budget categorically or with a nonlinear/monotone alternative, and assess heterogeneous policy effects with random slopes where feasible, question-cluster bootstrap inference, or a question-level sensitivity analysis.
4. **Add prior and approximation sensitivity (Major):** compare at least two prior scales; report changes in H1-H3, random-effect SDs, and uncertainty. Compare MAP, VB, and one independent/bootstrap implementation beyond coefficient means.
5. **Expose the replacement audit (Major):** give original failure reason, gate exceeded, dated amendment, output identifier, and accepted replacement for each of the five recollected blocks. Link the immutable preregistration.

### Questions for the author

1. How exactly were the reported intervals and p values calculated from the MAP fit?
2. Are seed effects shared across deployments or nested within deployment, and how sensitive are results to that coding?
3. Do H1-H3 remain supported with categorical budget and question-cluster uncertainty?
4. What immutable record establishes that the five replacement rules and H1-H4 were fixed before recollection/analysis?

### Statistical-reporting assessment

**Adequate (approximately 76/100).** Effect sizes, denominators, technical missingness, and secondary multiplicity control are strong. Power, functional-form checks, inferential terminology, and approximation sensitivity require improvement. No clear p-hacking or selective-reporting signal was detected.

### Dimension scores

| Dimension | Score |
|---|---:|
| Originality | 82 |
| Methodological rigor | 68 |
| Evidence sufficiency | 77 |
| Argument coherence | 87 |
| Writing quality | 89 |
| **Weighted average** | **78.0** |

---

## Reviewer 2 — Domain

### Recommendation

**Major Revision** — confidence **4/5**.

### Summary assessment

The strongest domain contribution is a controlled empirical demonstration that provenance-aware routing changes collective outcomes, particularly the downgrade condition that retains content while removing claimed relationship privilege. The manuscript is commendably careful not to equate authentication with truth or claim protection against credentialed malicious agents. Domain positioning is nevertheless incomplete. Communication-layer attacks, propagation, topology-aware defenses, and provenance loss need to be placed alongside the present threat. The paper also moves at times from evidence about a bundled admission/routing treatment to claims about the necessity of relationship-bound credentials, which was not isolated by the design.

### Principal strengths

1. Precise separation of provenance enforcement from semantic moderation.
2. Strong boundaries around compromised credentials, revocation, model-family comparison, and extrapolated thresholds.
3. Meaningful empirical novelty in the downgrade condition.
4. Related Work is thematic rather than a citation list.

### Required domain revisions

1. **Add directly relevant communication-security literature (Major):** include a threat-model comparison covering attacker position, manipulated object, provenance assumptions, topology, and defense layer. Verified candidates include *Prompt Infection* (arXiv:2410.07283), *Red-Teaming LLM Multi-Agent Systems via Communication Attacks* (Findings of ACL 2025), *G-Safeguard* (ACL 2025), and *Trust Cascade through Provenance Erasure* (EMNLP 2026).
2. **Separate four properties (Major):** sender authentication, enrollment/membership, receiver-specific relationship authorization, and routing after failed verification. State which are assumed and which are experimentally manipulated.
3. **Narrow component-level claims (Major):** the experiment evaluates the full credential/routing bundle; it does not establish incremental necessity over sender-only authentication, allowlisting, principal deduplication, or rate limiting.
4. **Recast H4 (Minor/Major):** call it an exploratory security-margin summary motivated by collective-dynamics vocabulary, not a test or validation of the *Physics of Agents* model.

### Questions for the author

1. Which property is primary: authentication, membership, relationship authorization, or routing after failure?
2. What evidence attributes the effect to nominal identities rather than repeated false-message exposure?
3. Would sender-only allowlisting reproduce the `drop` outcome, and what incremental protection is supplied by edge binding?
4. Is H4 a formal theoretical test or an exploratory summary?

### Dimension scores

| Dimension | Score |
|---|---:|
| Originality | 71 |
| Methodological rigor | 80 |
| Evidence sufficiency | 76 |
| Argument coherence | 77 |
| Writing quality | 85 |
| Literature integration | 58 |
| **Weighted average** | **77.5** |

---

## Reviewer 3 — Cross-disciplinary / Practical

### Recommendation

**Major Revision** — confidence **4/5**.

### Summary assessment

The paper places the decision at the right trust boundary and clearly separates authentication, authorization, routing, and truth. Edge-bound tokens and freshness are conceptually stronger than sender-only identity. The practical mechanism, however, is underspecified as a deployable protocol. The experiment assumes an authority that knows valid relationships but does not specify enrollment, key distribution, canonical serialization, nonce state, revocation, or compromise recovery. It also lacks benign unknown senders, so the security-utility cost of downgrade and drop is unmeasured. Finally, the prompt-level implementation of the unknown-relation channel must be shown because formatting or salience may partly explain the downgrade effect.

### Principal strengths

1. Correct placement of credential validation before LLM deliberation.
2. Accurate separation of authentication from content moderation.
3. Useful receiver-specific edge authorization and freshness framing.
4. Operational failures are treated as first-class evidence.
5. Deployment limitations are candid.

### Required practical revisions

1. **Specify the credential protocol (Major):** authenticated byte string, canonical encoding, domain/version tag, key scope, nonce lifecycle, verifier state machine, replay behavior, failure semantics, rotation/revocation assumptions, and test vectors.
2. **Measure or sharply bound the utility tradeoff (Major):** add legitimate unknown-origin messages or confine conclusions to attack resistance under the tested closed-world condition.
3. **Publish exact prompt/channel serialization (Major):** show positive- and unknown-relation inbox wording, labels, ordering, separators, and token-count matching.
4. **State the trusted-enrollment assumption prominently (Major):** the mechanism blocks forged edge claims; it does not prevent one principal from obtaining multiple valid credentials.
5. **Add operational cost/ethics context (Minor):** verification latency/state/log volume, audit-data privacy, provider-policy compliance, and dual-use release rationale.

### Questions for the author

1. What exact canonical fields are authenticated and how are they versioned/domain-separated?
2. How is nonce replay handled across steps and verifier restarts?
3. Are positive- and unknown-relation prompts identical except for the relationship label?
4. How would legitimate unknown senders be admitted and evaluated?

### Dimension scores

| Dimension | Score |
|---|---:|
| Originality | 82 |
| Methodological rigor | 72 |
| Evidence sufficiency | 73 |
| Argument coherence | 87 |
| Writing quality | 89 |
| Significance and impact | 78 |
| **Weighted average** | **79.1** |

---

## Devil's Advocate Review

### Strongest counter-argument

The study may be interpreted as demonstrating a general and unsurprising exposure effect rather than an identity-specific security effect. At higher “identity budgets,” the attacker sends more instances of the same false option to honest agents. Because the design does not hold message volume, recipient exposure, and nominal sender count separately constant, the rising incorrect-majority rate under `none` could be explained by repeated false-message exposure alone. Likewise, `drop` removes the entire added message stream, so its protective effect does not establish that receiver-specific relationship credentials are necessary; a simple allowlist, principal-level rate limit, or generic rejection of all external messages might produce the same outcome. `Downgrade` is more informative, but without exact prompt serialization its effect may reflect altered salience or formatting rather than loss of relationship privilege. The paper therefore provides credible evidence that the tested bundled routing policy improves robustness against the tested bundled external-traffic treatment. It does not yet establish that nominal identity multiplicity is the operative mechanism, that edge binding is incrementally necessary, or that the policy improves utility in an open system. The manuscript already acknowledges pieces of this counterargument, but acknowledgment alone does not supply the missing factorial controls. The central claim must either be narrowed to the bundled treatment or supported by identity-versus-volume and credential-component ablations.

### CRITICAL issues

None. The bounded claim that the tested routing policies reduce the tested attack is not contradicted by the data.

### MAJOR issues

| # | Dimension | Issue | Location |
|---|---|---|---|
| DA1 | Construct validity | Identity budget is confounded with false-message volume and exposure. | Sections 3.3, 5.2 |
| DA2 | Alternative explanation | `drop` removes the attack channel; the data do not show incremental necessity of relationship binding over simpler admission controls. | Sections 3.4, 5.4, 5.6 |
| DA3 | Treatment interpretation | The unknown-relation channel may change prompt salience/formatting, not only relationship semantics. | Sections 3.4, 5.1 |
| DA4 | Selection/time | Five block recollections may introduce provider-time drift; prospective replacement prevents cell cherry-picking but does not itself demonstrate temporal exchangeability. | Sections 3.5, 6 |

### MINOR issues

| # | Dimension | Issue | Location |
|---|---|---|---|
| DA5 | Theoretical framing | H4 is entirely extrapolative and should not carry confirmatory-theory weight. | Sections 3.6, 4.5, 5.7 |
| DA6 | Generalization | Binary mathematics with eight agents and two updates is a narrow behavioral regime. | Section 6 |

### Ignored or under-tested alternative paths

1. Principal-level deduplication or rate limiting without relationship credentials.
2. Sender-only authentication or an enrolled-sender allowlist.
3. Topology-aware anomaly detection and message-propagation controls.
4. Benign unknown-origin traffic evaluated jointly with malicious traffic.

### Unexamined premise

The paper assumes that an LLM's relationship-conditioned inbox label corresponds to a meaningful and stable “social privilege.” Because the exact prompt representation and its invariance are not shown, that premise is not yet independently auditable.

### Observations

- The manuscript's explicit limitations substantially reduce, but do not eliminate, the risks above.
- The downgrade condition remains a promising contribution because it can potentially distinguish provenance semantics from content removal once prompt serialization is documented.

---

# Phase 2: Editorial Decision Package

## Decision

# Major Revision

No reviewer identified a fatal or irreparable flaw, and the Devil's Advocate found no CRITICAL issue. However, all four scored reviewers recommend Major Revision because several central claims require either additional controls/robustness analyses or explicit narrowing.

## Reviewer summary

| Reviewer | Recommendation | Confidence | Weighted score |
|---|---|---:|---:|
| EIC | Major Revision | 4/5 | 78.5 |
| Methodology | Major Revision | 4/5 | 78.0 |
| Domain | Major Revision | 4/5 | 77.5 |
| Cross-disciplinary / Practical | Major Revision | 4/5 | 79.1 |
| Devil's Advocate | No CRITICAL; four MAJOR findings | — | — |

## Consensus analysis

### [CONSENSUS-4] Strengths

1. The separation of provenance/authorization from semantic moderation is clear and valuable.
2. Whole-block admission, technical-failure accounting, and claim boundaries are unusually strong.
3. The paper supports a credible bounded result: the tested routing policies reduce the tested external-traffic attack.
4. The manuscript is polished, coherent, and close to submission quality at the prose level.

### [CONSENSUS-4] Required improvements

1. The primary security property and novelty hierarchy must be stated more precisely.
2. The artifact package must expose enough protocol, prompt, preregistration, and model detail for independent audit.
3. Practical recommendations must remain bounded by the absence of benign unknown senders and production identity/enrollment mechanisms.

### [CONSENSUS-3] High-priority issues

1. Identity count is not isolated from message exposure.
2. Exact prompt/channel serialization is necessary to interpret `downgrade`.
3. H4 should be reduced to an exploratory, extrapolative summary.

### Disagreement and arbitration

**Issue: numerical score band versus revision severity.** All scored reviews fall around 77-79, normally a minor-revision range. Reviewers nevertheless recommend Major Revision. The EIC accepts the elevation because the missing identity/message control, inferential robustness, and protocol transparency concern central construct interpretation rather than copyediting. The decision is therefore Major Revision, not Minor Revision.

**Issue: need for new data.** Some concerns can be resolved by claim narrowing and documentation; the identity-versus-volume and benign-utility concerns are strongest with new experiments. The author may choose a documentation-only route, but then the title, abstract, contribution statement, and architectural recommendations must explicitly describe the treatment as a bundled external-traffic/routing experiment.

## Decision rationale

This is a promising and unusually careful paper with a defensible core result. The evidence supports the statement that receiver-side credential-aware routing changes collective outcomes under a controlled unauthenticated external-traffic attack. The paper also makes a useful systems argument for verifying provenance before prompt construction. The present version, however, sometimes assigns the effect more specifically to identity multiplicity and relationship-bound credentials than the factorial design warrants. The method review further identifies unresolved uncertainty-calibration questions in the MAP GLMM, while the domain and practical reviews show that the protocol and literature positioning are not yet sufficient for independent security evaluation. These are substantial but fixable issues. A rejection would be too severe because the accepted dataset, experimental governance, bounded conclusions, and downgrade result retain clear value. A minor revision would be too lenient because resolving the issues requires additional analyses, a more exact protocol specification, and possibly new control conditions. The appropriate decision is Major Revision with re-review.

## Required revisions

### R1 — Separate identity multiplicity from message exposure, or narrow the central claim

**Sources:** EIC, Domain, Devil's Advocate.  
**Acceptance criteria:** either add a fixed-volume control/ablation that independently varies nominal identities and message instances, or revise the title, abstract, RQ, H1 interpretation, Discussion, and Conclusion to describe a bundled external-identity/message-exposure treatment. Explicitly state what remains unidentified.

### R2 — Strengthen GLMM uncertainty and robustness reporting

**Source:** Methodology reviewer.  
**Acceptance criteria:** define interval/p-value construction; report complete fixed/random effects; add prior sensitivity; add categorical/nonlinear budget sensitivity; assess clustered or heterogeneous treatment effects; provide simulation-based power/precision tied to questions and seeds.

### R3 — Publish prompt and protocol specifications

**Sources:** Practical reviewer, EIC, Devil's Advocate.  
**Acceptance criteria:** exact positive/unknown inbox serialization, message order and token-count treatment, authenticated byte format, domain/version tag, key scope, nonce lifecycle, verifier state machine, failure semantics, and test vectors.

### R4 — Sharpen security-property and novelty definitions

**Sources:** Domain and Practical reviewers.  
**Acceptance criteria:** distinguish authentication, enrollment, relationship authorization, and routing; state which are assumed/tested; describe the contribution as evaluation of provenance-aware routing rather than a complete Sybil defense or new authentication primitive.

### R5 — Make preregistration and recollection independently auditable

**Sources:** Methodology and EIC.  
**Acceptance criteria:** persistent preregistration and amendment identifiers/timestamps; block-level table for all five replacements; collection chronology; failure reasons; accepted source identifiers; sensitivity discussion of provider-time drift.

### R6 — Address the security-utility boundary

**Sources:** Practical reviewer and EIC.  
**Acceptance criteria:** add benign unknown-origin conditions and joint utility/security outcomes, or narrow deployment recommendations to attack resistance under the tested closed-world condition.

### R7 — Reposition H4

**Sources:** EIC, Domain, Devil's Advocate.  
**Acceptance criteria:** label H4 exploratory and fully extrapolative, reduce its role in the contribution/abstract, or collect budgets that bracket the 50% transition and estimate deployment-matched physical parameters.

### R8 — Complete submission metadata and stable artifacts

**Sources:** all reviewers.  
**Acceptance criteria:** stable repository URL plus commit/DOI, one-command analysis environment, prompts and supplementary tables, final affiliation/corresponding author, and confirmed CRediT/funding/conflict/AI-disclosure statements.

## Revision roadmap

### Priority 1 — Structural and analytical work (3-5 weeks)

- [ ] Decide between new identity/message-volume control data and explicit claim narrowing.
- [ ] Run GLMM sensitivity, clustered uncertainty, and simulation-based precision analyses.
- [ ] Reframe H4 as exploratory or extend the budget range.
- [ ] Rewrite the contribution hierarchy and threat-model definitions.

### Priority 2 — Reproducibility and systems detail (1-2 weeks)

- [ ] Add prompt serialization and credential protocol appendix.
- [ ] Publish preregistration/amendment and recollection audit table.
- [ ] Add the communication-security literature comparison table.
- [ ] Add stable artifact versioning and one-command regeneration instructions.

### Priority 3 — Submission preparation (2-4 days)

- [ ] Resolve author metadata and declarations.
- [ ] Normalize inferential terminology and p-value/interval formatting.
- [ ] Apply the selected venue template and page limits.

**Recommended revision window:** 6-8 weeks, followed by re-review.

## Final editorial note

The most efficient path without new data is to narrow the identity-specific and production-deployment claims, fully document the bundled treatment, add statistical robustness analyses, and present the study as a rigorous first empirical evaluation of receiver-side provenance routing. The strongest path is to add a fixed-message-volume identity ablation and a benign-unknown utility condition; those additions would materially improve both construct validity and practical significance.
