# Repository structure

This fork contains the upstream *Physics of Agents* reproduction and a separate authenticated-external-traffic study. The two workflows share the repository but have different canonical inputs and outputs.

## Top-level map

```text
physics-of-agents/
├── lib/                    # upstream generation code and fork attack runner
│   └── datagen_attack/     # credentials, routing policies, provider adapters
├── data/                   # question banks and raw/local episode stores
├── res/                    # upstream analysis notebooks
├── res_attack/             # attack-study matrices, audits, scripts, and results
│   └── confirmatory_analysis/  # accepted merged data and formal outputs
├── paper/                  # current paper, supplements, reviews, and archives
├── baseline_reproduction/  # upstream-paper reproduction audit
├── online_appendix/        # static message-data browser
├── tests/                  # attack and credential tests
└── tmp/                    # local temporary render/review files; Git-ignored
```

## Canonical confirmatory data

Do not infer accepted runs by recursively scanning `data/`. The authoritative selection is:

- `res_attack/confirmatory_analysis/accepted_block_manifest.csv`: the 20 accepted model-seed blocks, hashes, and replacement flags.
- `res_attack/confirmatory_analysis/accepted_episode_data.csv`: the merged 3,600-episode analysis table.
- `res_attack/confirmatory_analysis/analysis_metadata.json`: frozen metadata and source hashes.
- `res_attack/confirmatory_analysis/question_within_deployment/`: post-review primary-model and robustness outputs.

The many `data/attack_*` directories preserve pilots, provider checks, failed blocks, and full-block recollections. They remain in place for provenance and must not be merged into the accepted analysis unless the manifest is deliberately revised and re-audited.

## Canonical paper

The source of truth is `paper/MANUSCRIPT.md`. See `paper/README.md` for the paper-specific tree and the distinction among the current manuscript, archived drafts, and the separate Claude PDF.

## Editing rules

1. Edit current prose only in `paper/MANUSCRIPT.md`; regenerate `paper/manuscript.tex` and `paper/manuscript.pdf`.
2. Edit citations in both the manuscript reference list and `paper/references.bib`.
3. Put protocol/statistical supplements in `paper/appendices/`.
4. Put review reports and writing-process records in `paper/reviews/`.
5. Keep superseded versions in `paper/archive/`; do not overwrite them.
6. Keep externally returned artifacts without editable source in `paper/external/`.
7. Use the accepted-block manifest rather than folder names to decide which experimental runs are formal data.
