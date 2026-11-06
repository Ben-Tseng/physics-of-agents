# Argument Blueprint

## Central thesis

Unauthenticated external identities can convert apparent social support into a scalable attack on an LLM-agent collective. Binding relationship claims to receiver-verifiable credentials and applying deterministic routing before deliberation reduces that influence across two independent deployments, although the experiment supports only directional, extrapolative claims about critical attack budgets.

## Sub-arguments

### 1. Sender multiplicity is a security variable, not merely more evidence

- **Claim:** When receivers accept self-declared relationships, increasing the number of external identities increases the chance of an incorrect terminal majority.
- **Evidence:** The preregistered H1 contrast is positive in both deployments and in the pooled model. Classical Sybil analysis explains why nominal redundancy fails when one actor can mint identities [20], while recent collective-agent studies show sensitivity to majority size, committed minorities, and adversarial social pressure [11], [12], [14], [16], [17].
- **Reasoning:** Multiple sender labels need not represent independent sources. If the routing layer treats them as distinct trusted neighbors, identity multiplication changes the collective's effective evidence structure before any reasoning-quality judgment occurs.
- **Counter-argument:** The observed effect may be attributable only to repeated false content rather than identity.
- **Response:** Concede that content repetition contributes to influence. The design isolates the operational question relevant to routing: whether the system accepts multiple uncredentialed senders as relationship-bearing participants. It does not claim to decompose identity count from every content-frequency mechanism.

### 2. Deterministic credential routing reduces attack influence

- **Claim:** Receiver-side downgrade and drop policies reduce incorrect-majority odds relative to trusting an invalid relationship claim.
- **Evidence:** The pooled H2 and H3 contrasts favor downgrade and drop. The direction replicates in both official deployments. Authenticated delegation, verifiable credentials, HMAC, and classical multi-agent security research support moving identity and authorization checks outside language-model inference [18], [19], [21], [22].
- **Reasoning:** Verification removes the attacker's ability to choose a privileged relationship label. Downgrade changes the message's routing context without discarding its content; drop removes both the claim and the message. Neither policy asks an LLM to infer authenticity from prose.
- **Counter-argument:** Authentication does not protect against compromised credentialed agents or malicious authenticated content.
- **Response:** Acknowledge as a scope boundary. The intervention addresses external relationship spoofing, not the full agent-security problem.

### 3. Credential treatment is a policy choice with different security-utility implications

- **Claim:** Drop produced the larger pooled reduction, but the experiment does not establish that drop is universally preferable to downgrade.
- **Evidence:** H3 is stronger than H2 in the pooled model, and Holm-adjusted budget-specific differences for drop versus none are significant at budgets two and four. Agent-security benchmarks warn that defenses can trade security against task utility [24], [25].
- **Reasoning:** Downgrade preserves potentially useful unknown-origin content, whereas drop minimizes its immediate influence. The present endpoint measures attack success, not performance on a broad benign-unknown-sender suite.
- **Counter-argument:** The lower attack rate under drop proves that discarding invalid traffic is the best architecture.
- **Response:** Reject the universal inference. It exceeds the measured outcome and task domain.

### 4. Replicated direction is stronger than a single deployment, but not a model-family comparison

- **Claim:** The same directional H1-H3 pattern across two official deployments supports replication of the mechanism, while differences in magnitude remain deployment-conditional.
- **Evidence:** Qwen3.5-27B and `mistral-small-2603` each show positive H1 and protective H2-H3 estimates, but they were served by different providers and stacks.
- **Reasoning:** Agreement in sign across independently operated deployments reduces dependence on one endpoint. Provider, configuration, and model family remain confounded, so coefficients cannot identify model-family causation.
- **Counter-argument:** The much larger Qwen effect implies greater inherent susceptibility or defensibility.
- **Response:** Reject that interpretation because the experimental design did not control the deployment stack.

### 5. Critical-budget shifts are mechanistically suggestive but not calibrated

- **Claim:** Point estimates are directionally consistent with credential defenses raising the attack budget required to cross 50% success, but do not validate a quantitative physical coupling prediction.
- **Evidence:** Both downgrade-to-none point multipliers exceed one. All crossings lie beyond the maximum tested budget of four; intervals are wide or infinite; model-matched coupling estimates are absent for both live deployments.
- **Reasoning:** Monotone curve extrapolation can summarize direction, but a threshold outside the support of the data cannot be treated as a directly observed robustness margin.
- **Counter-argument:** Reporting precise critical budgets invites quantitative interpretation.
- **Response:** Label every estimate as extrapolative, retain infinite intervals, and limit H4 to directional consistency.

## Logical flow

Introduction defines the capability-security tension and the external-identity gap. Related Work separates cooperative collective reasoning, social failure modes, adversarial collaboration, and identity enforcement. Methods freezes the threat model, credential policies, block-admission rules, and confirmatory tests. Results proceed from data integrity to descriptive rates, H1-H3, secondary contrasts, and H4 last. Discussion interprets the mechanism, compares it with adjacent attacks, and states architectural implications. Limitations bound deployment, task, graph, credential, and extrapolation claims. The Conclusion answers the research question without adding new evidence.

## Strength assessment

| Sub-argument | Evidence strength | Logical validity | Counter-argument risk |
|---|---|---|---|
| Identity budget increases risk | Strong | Qualified | Medium |
| Credential routing reduces risk | Strong | Valid within scope | Low |
| Downgrade/drop encode a tradeoff | Moderate | Qualified | Medium |
| Direction replicates, magnitude does not compare families | Strong | Valid | Low |
| H4 is directional only | Adequate | Qualified | High if overphrased |

## Drafting notes

- Use direct computer-science prose and first-person plural only for study decisions.
- Do not claim novelty by priority.
- State odds ratios as conditional model estimates, not causal effects.
- Keep deployment-specific estimates before pooled estimates.
- Repeat the tested-budget boundary wherever critical budgets appear.
- Treat `none`, `downgrade`, and `drop` as routing policies, not model behaviors.
- Use IEEE numeric citations and introduce no unverified source.
