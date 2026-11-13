# Current Paper Output Package

Updated after the Claude revision and directory reorganization on 13 November 2026.

## Canonical submission files

- `MANUSCRIPT.md`: canonical editable manuscript.
- `manuscript.tex`: generated LaTeX source.
- `manuscript.pdf`: canonical 26-page PDF.
- `references.bib`: 39-entry bibliography.
- `build_latex.py`: Markdown-to-LaTeX build script.

## Supporting material

- `appendices/`: protocol, statistical appendix, and reproducibility table.
- `figures/`: editable figure source and rendered PDF/PNG assets.
- `reviews/`: outlines, audits, peer-review reports, and revision records.
- `archive/`: pre-deep-review and advisor-feedback snapshots.
- `external/claude/`: the PDF returned separately by Claude; it is preserved for comparison and is not the canonical source.
- `exports/`: standalone HTML exports.
- `build/`: local LaTeX logs; ignored by Git.

## Verified facts

- Frozen accepted dataset: 20 model-seed blocks and 3,600 episodes.
- References: 39 in both the manuscript list and BibTeX database.
- Current PDF: 26 US-letter pages.
- Canonical manuscript SHA-256: `d65d98ffdcbd4eae82583702c196cbb326032874272e67a84a06998c10a8f56d`.
- Canonical PDF SHA-256: `f9ec8944a4ae0a79f2fe2125a0f5e33eec02c8e78d536466d97e125d468c8514`.
- Bibliography SHA-256: `53a3d56960859fda58408845607a0f343a3e3883f9e8c0ba0e0e4e563290ba25`.

Hashes must be refreshed after any further manuscript rebuild.

## Author actions before submission

1. Confirm affiliation and corresponding-author details.
2. Confirm the CRediT, funding, and conflict-of-interest statements.
3. Select the target venue and apply its template, page limit, and disclosure policy.
4. Rebuild the PDF and refresh the integrity hashes after the final author edit.
