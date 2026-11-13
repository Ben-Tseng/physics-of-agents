# Major-revision plan

This plan translates the five-reviewer `Major Revision` decision into a
claim-controlled revision. It does not add uncollected API experiments or infer
results that are absent from the locked data.

## Revised paper story

The paper evaluates a bundled external-traffic treatment in an eight-agent
collective: increasing the number of nominal external senders also increases the
number of standardized false-message instances, and receiver policies change
whether those messages enter a positive-relation, unverified-source, or dropped
channel. The experiment therefore establishes the effect of this operational
bundle and the value of deterministic relationship-credential routing. It does
not isolate a pure identity-count mechanism, evaluate benign unverified traffic,
or prove deployment-independent threshold calibration.

## Section mini-outline and paragraph roles

### Introduction

1. **Task and boundary:** explain why relationship-conditioned routing is a
   security boundary in LLM-agent systems.
2. **Prior approaches and gap:** distinguish enrolled malicious agents, prompt
   injection, provenance loss, and unauthenticated external peer traffic.
3. **Threat and confounding boundary:** define the external-sender/message-volume
   bundle and state that identity and exposure are not separately identified.
4. **Intervention:** explain verified relation, downgrade, and drop as routing
   policies rather than semantic truth classifiers.
5. **Contributions and evidence:** state the controlled design, two-deployment
   replication, technical admission gates, and robustness analyses.
6. **Non-claims:** exclude benign-utility, compromised-key, universal-model, and
   in-range threshold claims.

### Methods

1. **Design:** frozen 20-block, 3,600-episode matrix and deployment boundary.
2. **Protocol:** exact prompts, deterministic message text, target selection,
   message multiplicity, recipient shuffling, and synchronous updates.
3. **Trust architecture:** separate authentication, enrollment, relationship
   authorization, routing, and content truthfulness.
4. **Admission audit:** give dated freeze/recollection chain and accepted-source
   manifest rule.
5. **Primary statistics:** document MAP priors, Laplace covariance block, Wald
   intervals/tests, contrasts, and multiplicity.
6. **Robustness:** prior grid, question-cluster GEE with categorical cells, and
   leave-one-question-out fits.
7. **Exploratory H4:** label all critical-budget analysis exploratory and
   extrapolative.

### Results

1. **Technical validity:** report denominator-specific failures and credentials.
2. **Primary H1-H3:** give deployment-specific then pooled results.
3. **Robustness:** report what is stable and explicitly note that H2's Wald
   significance is sensitive to omission of some questions although its sign is
   stable.
4. **Exploratory H4:** retain threshold estimates only as out-of-range model
   extrapolations.

### Discussion and conclusion

1. **Interpretation:** attribute results to the bundled unauthenticated-traffic
   treatment and deterministic routing.
2. **Trust boundary:** specify what credentials do and do not establish.
3. **Utility boundary:** state that benign unknown traffic was not evaluated.
4. **Validity:** foreground message-volume confounding, 18-question scope,
   deployment confounding, prior/model assumptions, and extrapolation.
5. **Conclusion:** make only the routing-boundary claim supported by the study.

## Claim–evidence map

| Claim | Evidence | Revision status |
|---|---|---|
| Increasing the bundled external-sender treatment raises error under `none` | Preregistered pooled MAP H1; both deployment-specific signs; categorical-cell question-cluster GEE | Retain, with bundle wording |
| Downgrade reduces the mean positive-budget contrast | Preregistered pooled MAP H2; both deployment signs; GEE; prior grid | Retain with qualification: leave-one-question-out direction stable, significance not uniform |
| Drop reduces the mean positive-budget contrast | Preregistered pooled MAP H3; both deployment signs; GEE; prior grid and leave-one-question-out stability | Retain |
| Credential-aware routing moves fitted critical budgets upward | Point multipliers above one, but crossings are beyond budget 4 and Mistral interval includes one | Exploratory only |
| Identity multiplicity itself causes the effect | Not identified because each added identity adds standardized message instances | Remove/narrow |
| Policies preserve benign open-system utility | No benign unverified-traffic condition | Do not claim; mark as future work |
| HMAC tokens solve membership or key compromise | Not tested; experimental authority presupposes enrollment and secret integrity | Do not claim |
| Effects generalize to arbitrary models/providers/tasks | Two deployments and 18 mathematics questions | Do not claim |

## Deliverables

- Revised `MANUSCRIPT.md`, LaTeX, bibliography, and rendered PDF.
- Exact prompt and trust-boundary appendix.
- Machine-readable prior, clustered-GEE, and leave-one-question-out robustness
  outputs plus a reproducible analysis script.
- Revision self-review and stable repository/commit metadata.
