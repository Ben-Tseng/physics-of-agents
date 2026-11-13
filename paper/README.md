# Paper directory

This directory is organized around one canonical manuscript. Historical drafts and review artifacts are retained, but they are not submission sources.

## Current source of truth

| Path | Role |
|---|---|
| `MANUSCRIPT.md` | Canonical editable manuscript |
| `manuscript.tex` | Generated LaTeX source |
| `manuscript.pdf` | Canonical rendered paper |
| `references.bib` | Canonical bibliography |
| `build_latex.py` | Rebuild script |
| `OUTPUT_PACKAGE.md` | Deliverable inventory and current hashes |

Edit `MANUSCRIPT.md`, `references.bib`, the appendices, or figure source as needed. Do not edit archived snapshots and do not treat the Claude-only PDF as an editable source.

## Subdirectories

```text
paper/
├── MANUSCRIPT.md                 # current manuscript source
├── manuscript.tex / .pdf        # current rendered outputs
├── references.bib               # current bibliography
├── appendices/                  # protocol and statistical supplements
├── figures/                     # figure source and rendered assets
├── reviews/                     # audits, reviews, plans, and writing records
├── archive/
│   ├── pre-deep-review/        # snapshot before deep review
│   └── advisor-draft/          # feedback-oriented draft
├── external/claude/             # external Claude PDF for comparison
├── exports/                     # HTML exports
└── build/                       # ignored local build logs
```

## Version interpretation

- `MANUSCRIPT.md` and `manuscript.pdf` are the current 26-page version dated 12 November 2026.
- `external/claude/manuscript_revised.pdf` is a separate 27-page artifact. No matching Markdown, LaTeX, or BibTeX source was supplied with it, so it is not designated as canonical.
- Two pairs of pre-deep-review files were byte-identical (`MANUSCRIPT_pre_deep_review.md` / `MANUSCRIPT_pre_deepreview.md` and `references_pre_deep_review.bib` / `references_pre_deepreview.bib`). One canonical copy of each pair is retained in the archive; the redundant copies were removed during reorganization.

## Build

From the repository root:

```bash
python3 paper/build_latex.py
tectonic paper/manuscript.tex --outdir paper
```

After rebuilding, inspect the PDF visually and update `OUTPUT_PACKAGE.md` hashes.
