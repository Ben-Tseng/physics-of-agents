## Dimension Scores

### D1: originality

Score: pass. The Introduction identifies a specific gap—controlled budget-response evidence for relationship-bound credential routing against unauthenticated external identities—and states concrete contributions without an unsupported priority claim. Related Work distinguishes the threat from enrolled malicious participants, indirect prompt injection, classical Sybil attacks, and generic identity mechanisms, while the Discussion returns to those distinctions and explains the added empirical and architectural perspective rather than merely listing sources.

### D2: methodological_rigor

Score: block. The experimental design is carefully bounded, the threat model and routing policies fit the research question, the block-admission rules and limitations are explicit, and aggregate spot checks reproduce 3,600 episodes, 151 raw-zero spins, 28 message-call failures, and five replacement blocks. However, the analysis description is not reproducible because the deployment-specific contrasts in Table 3 cannot be reconciled with the stated per-identity interpretation and the reported cell rates: for Qwen, `none` rises only from 0.194 at budget 1 to 0.261 at budget 4 while the reported per-identity OR is 3.161; for Mistral, the corresponding rates are 0.294 and 0.361 while the OR is 1.634. The deployment-specific H2/H3 magnitudes are likewise much stronger than the raw policy differences, yet the paper provides no coding, scaling, prior, random-effect, or contrast-construction detail capable of explaining the discrepancy. This is a significant design flaw in the analysis report until the deployment-specific models are audited and either corrected or transparently derived.

### D3: evidence_sufficiency

Score: pass. The paper supports its external factual claims with a continuous IEEE citation sequence, the citation audit reports no orphan or uncited entries and verifies all 26 sources, and the principal pooled, secondary, critical-budget, cell-count, and block-manifest claims match the frozen CSV outputs checked. The Discussion does not cherry-pick the threshold analysis: it repeatedly states that all 50% crossings exceed the tested maximum, preserves infinite intervals, notes that the Mistral multiplier interval includes one, and limits H4 to directional interpretation.

### D4: argument_coherence

Score: pass. The research question and four hypotheses in the Introduction determine the Methods and Results order, the Discussion addresses the same threat-boundary distinction, and the Conclusion answers the original question while retaining the stated exclusions concerning universal immunity, model-family ranking, benign utility, and quantitative physical calibration. Section transitions and the abstract-to-conclusion thesis remain consistent, with no central self-contradiction.

### D5: writing_quality

Score: pass. The manuscript maintains a precise academic register, defines the three routing policies consistently, separates conditional odds ratios from probability changes, uses internally consistent numeric citations, and references both figures and all four tables in the text. The prose is dense but readable, grammatical errors are rare, and the presentation remains suitable for a computer-science security or trustworthy-AI venue; remaining author and venue metadata are visibly marked for submission-stage confirmation rather than silently presented as final.

## Failure Condition Checks

### F1

Fired. Mandatory dimension D2 (`methodological_rigor`) scores block because the deployment-specific model outputs and their claimed per-identity interpretation are not reproducible from the stated model specification and conflict sharply with the balanced within-deployment descriptive trajectories; the required action is `evaluator_decision=request_revision`.

### F2

Did not fire. Neither mandatory dimension scores warn: D2 scores block and D3 scores pass.

### F3

Did not fire. Both high-priority dimensions, D1 (`originality`) and D4 (`argument_coherence`), score pass.

### F6

Did not fire. The normal-priority D5 (`writing_quality`) dimension scores pass.

### F4

Did not fire. No high- or normal-priority dimension scores warn, and the mandatory D2 dimension scores block.

### F5

Did not fire. The supplied artifacts do not establish a round-2 recurrence of a mandatory-dimension block after an in-phase writer revision.

### F0

Did not fire. Mandatory dimension D2 does not score pass, and one dimension scores block.

## Review Body

The paper has a strong conceptual spine. It defines a narrow external-identity threat, keeps message content fixed, distinguishes authentication from semantic moderation, and maps `none`, `downgrade`, and `drop` to understandable routing semantics. Its literature positioning is substantive, its limitations are unusually disciplined, and its frozen descriptive and pooled results are consistently carried into the abstract, Results, Discussion, and Conclusion. The block is therefore not about framing or prose; it concerns whether a key inferential layer can be independently understood and trusted.

Revision must first audit and regenerate `deployment_specific_contrasts.csv` from the frozen accepted episodes. For each deployment, report the exact fixed-effect formula, attack-budget encoding and scale, defense reference level, treatment of the shared budget-zero control, random-effect structure and grouping keys, estimator/class, prior or penalty settings, optimizer or variational settings, and covariance calculation used for H1–H3 contrasts. State explicitly whether each reported OR is per one nominal identity, per standardized budget unit, across a multi-identity contrast, or conditional on another transformation. Add a compact reproducibility check showing model-implied contrasts on the same budget scale as Table 2. If the current deployment-specific values arose from a scaling, extraction, or labeling error, correct the CSV, Table 3, and every abstract, Results, Discussion, and Conclusion statement that relies on them.

The revision should also explain why the deployment-specific adjusted effects differ so sharply from the complete, balanced cell trajectories, rather than relying only on the phrase "mixed-effects model." A defensible explanation must identify the estimand and show how adjustment produces the reported contrast; otherwise the deployment-specific inferential claims should be withdrawn or replaced with a correctly specified analysis. The pooled H1–H3 values, Holm-adjusted contrasts, critical-budget values, and technical totals match the frozen outputs in the checks performed here, so they need not be changed unless the model audit reveals a shared implementation problem.

Finally, retain the current safeguards during revision: deployment-specific estimates should precede pooled estimates, critical budgets must remain explicitly extrapolative, infinity must not be capped for presentation, and the paper must continue to avoid model-family causal comparisons and a universal ranking of downgrade versus drop. After the model audit and manuscript reconciliation, D2 can be reassessed without reopening dimensions that already pass unless the corrected results materially alter the central thesis.

## Evaluator Decision

evaluator_decision=request_revision
