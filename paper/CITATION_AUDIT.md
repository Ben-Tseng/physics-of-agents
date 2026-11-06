# Citation Audit Report

Audit date: 2026-11-06  
Target style: IEEE numeric  
Manuscript: `MANUSCRIPT_DRAFT.md`

## Summary

| Check | Result |
|---|---:|
| In-text citation numbers used | 26 |
| Reference-list entries | 26 |
| BibTeX entries | 26 |
| Orphan in-text citations | 0 |
| Uncited reference entries | 0 |
| Duplicate reference entries | 0 |
| Numbering continuity | PASS, [1] through [26] |
| Sources with DOI where available | 19 |
| Sources verified by official proceedings, PMLR, or arXiv URL instead of DOI | 7 |
| Direct quotations requiring page checks | 0 |
| Self-citations | 0 |

## Source verification

| # | Short source | Verification anchor | Status |
|---:|---|---|---|
| 1 | El et al., *Physics of Agents* | arXiv:2608.16578 | Verified |
| 2 | Guo et al., multi-agent survey | DOI 10.24963/ijcai.2024/890 | Verified |
| 3 | Li et al., CAMEL | DOI 10.52202/075280-2264 | Verified |
| 4 | Wu et al., AutoGen | COLM OpenReview BAakY1hNKS | Verified |
| 5 | Du et al., multiagent debate | PMLR 235 | Verified |
| 6 | Liang et al., divergent debate | DOI 10.18653/v1/2024.emnlp-main.992 | Verified |
| 7 | Zhang et al., social psychology | DOI 10.18653/v1/2024.acl-long.782 | Verified |
| 8 | Li et al., sparse topology | DOI 10.18653/v1/2024.findings-emnlp.427 | Verified |
| 9 | Wang et al., bounds of discussion | DOI 10.18653/v1/2024.acl-long.331 | Verified |
| 10 | Chuang et al., opinion dynamics | DOI 10.18653/v1/2024.findings-naacl.211 | Verified |
| 11 | Choi et al., conformity | DOI 10.18653/v1/2025.findings-acl.265 | Verified |
| 12 | Ashery et al., conventions | DOI 10.1126/sciadv.adu9368 | Verified |
| 13 | Zomer and De Domenico | DOI 10.1038/s44387-026-00091-5 | Verified |
| 14 | Ko et al., social vulnerabilities | DOI 10.18653/v1/2026.acl-long.1756 | Verified |
| 15 | Oh et al., belief entrenchment | DOI 10.1162/tacl.a.728 | Verified |
| 16 | Amayuelas et al., collaboration attack | DOI 10.18653/v1/2024.findings-emnlp.407 | Verified |
| 17 | Kraidia et al., persuasive adversaries | DOI 10.1038/s41598-026-42705-7 | Verified |
| 18 | South et al., delegation | PMLR 267 | Verified |
| 19 | Rodriguez Garzon et al., credentials | DOI 10.5220/0014234400004052 | Verified |
| 20 | Douceur, Sybil attack | DOI 10.1007/3-540-45748-8_24 | Verified |
| 21 | Jung et al., MAS security | DOI 10.1007/s10462-011-9228-8 | Verified |
| 22 | NIST HMAC | DOI 10.6028/NIST.FIPS.198-1 | Verified |
| 23 | Castro and Liskov, PBFT | USENIX OSDI proceedings | Verified |
| 24 | Debenedetti et al., AgentDojo | DOI 10.52202/079017-2636; NeurIPS proceedings | Verified |
| 25 | H. Zhang et al., Agent Security Bench | ICLR 2025 proceedings | Verified |
| 26 | Zhan et al., InjecAgent | arXiv:2403.02691 | Verified |

## Claim-evidence checks

- Collective-reasoning benefits and their limits are jointly represented by sources [3] through [9]; the manuscript does not claim unconditional superiority over single-agent prompting.
- Conformity, convention formation, and persuasive social influence are supported by [10] through [17].
- Identity, delegation, authorization, HMAC, and bounded-membership claims are supported by [18] through [23].
- External-input security and security-utility evaluation are supported by [24] through [26].
- Study results cite the frozen local data rather than external literature. Numerical values were checked against `primary_contrasts.csv`, `deployment_specific_contrasts.csv`, `secondary_contrasts.csv`, and `critical_budgets.csv`.
- No source is cited as proving the paper's empirical result.
- No broad priority claim such as “first” or “unprecedented” appears.

## Corrections made

1. Corrected the focal paper's first author from “O. El” to “B. El” and expanded the BibTeX author list from the arXiv record.
2. Replaced generic proceedings links for AgentDojo and Agent Security Bench with direct official proceedings pages.
3. Added AgentDojo's DOI and full author list.
4. Corrected Agent Security Bench's first author and inserted its full official author list.

## Items for submission-stage confirmation

- The venue-neutral IEEE list abbreviates several long author lists with “et al.” in the Markdown rendering. The BibTeX database retains full authors where verified in this audit and may be expanded further if a target venue prohibits truncation.
- Final author affiliation and corresponding-author metadata remain unconfirmed; they are not citation issues.
