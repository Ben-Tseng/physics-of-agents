# Academic Humanizer Audit

Audit target: `MANUSCRIPT_DRAFT.md`  
Document type: empirical computer-science paper  
Venue profile: venue-neutral, direct ICLR/NeurIPS-style technical register  
Author sample: no independent prose sample supplied; default precise scholarly voice used

This audit precedes language editing. It does not change manuscript text.

## Pattern findings and planned fixes

| Location | Pattern | Assessment | Planned fix |
|---|---|---|---|
| Abstract | Two result sentences exceed 35 words because each contains OR, CI, and p | Legitimate statistical density, but rhythm can improve | Split policy findings into separate sentences without changing any number |
| Introduction, final three paragraphs | Repeated “The study/The results/The paper” openers | Mild formulaic cadence | Vary grammatical subject while keeping the same claims |
| Related Work 2.1 | Range citation [2]–[6] follows a broad background clause | Citation cluster is valid but slightly compressed | Preserve all citations and clarify which works support frameworks, debate, and protocol dependence |
| Related Work 2.2 | Range citation [10]–[17] covers several distinct social mechanisms | Evidence is appropriate but risks citation dumping | Retain every citation and keep mechanism-specific sentences adjacent to their sources |
| Methods 3.5 | Gate sentence exceeds 35 words | Exact multi-condition definition requires density | Split the eligibility rule into two sentences without changing thresholds |
| Results 4.3 | Mistral statistics appear in one long sentence | All values are necessary | Split into H1, H2, and H3 clauses/sentences while preserving numbers |
| Discussion 5.1 | “three principal findings” | The grouping is substantive, not rule-of-three padding | Retain the grouping but reduce recap language around it |
| Discussion 5.6 | Several paragraphs begin “The control/The design/Verification” | Mild template repetition | Use direct technical subjects and shorter topic sentences |
| Throughout | “establish” sometimes appears near credential semantics | Usually means cryptographic or relational establishment, not evidentiary proof | Retain technical uses; soften any empirical use that could imply universality |
| Throughout | “robust” appears in cited titles or the term “robustness” | Discipline-standard usage | Preserve titles and calibrated robustness terminology |
| Throughout | 10 semicolons in roughly 8,000 total words | Within the stated writing-quality limit | Retain only where they clarify parallel clauses |
| Throughout | 0 em dashes | Passes the humanizer's zero-em-dash requirement | Preserve zero count |

## Claim-evidence audit

| Claim class | Evidence status | Required action |
|---|---|---|
| Communication and debate benefits | Supported by [2]–[8], with limitation from [9] | Preserve balanced framing |
| Majority, conformity, convention, and persuasion mechanisms | Supported by [10]–[17] | Preserve mechanism-specific attribution |
| Identity multiplication and membership assumptions | Supported by [20], [23] | Preserve analogy boundaries |
| External-input security risk | Supported by [24]–[26] | Preserve distinction from peer identity spoofing |
| H1-H3 estimates | Directly backed by Tables 2–3 and frozen CSV outputs | Do not alter numbers or strength of claims |
| Secondary contrasts | Directly backed by Holm-adjusted table | Preserve adjusted/unadjusted distinction |
| H4 direction | Backed by extrapolative curve estimates only | Keep “directionally consistent”; never strengthen to confirmation or calibration |
| Cross-deployment differences | Observed but confounded | Preserve non-causal language |
| Drop versus downgrade policy ranking | Attack outcome favors drop; benign utility unmeasured | Preserve the explicit non-universal conclusion |

## Editing constraints

- Preserve all section and subsection headings.
- Preserve all 3,600-episode design facts, rates, odds ratios, confidence intervals, p values, thresholds, equations, and table entries exactly.
- Preserve every citation number and every reference entry.
- Preserve the distinction among confirmatory, secondary, and directional analyses.
- Do not remove the AI Assistance Disclosure or imply that editing is intended to evade disclosure.
- Remove no limitation and add no unsupported claim.
