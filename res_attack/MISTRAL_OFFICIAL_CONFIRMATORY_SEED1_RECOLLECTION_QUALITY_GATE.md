# Official Mistral confirmatory seed-1 recollection quality-gate decision

Date evaluated: 2026-10-31.

The replacement `mistral-small-2603` seed-1 block completed all ten frozen
cells and all 180 expected episode files in the fresh recollection root. The
excluded first seed-1 block was not included in this audit.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 4/12,960 (0.031%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 4 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All four raw zero spins were connection-request errors, not exhausted parse
failures. The replacement block passes every prospectively fixed technical
quality gate and is admitted as official-Mistral confirmatory seed 1. This
decision concerns technical eligibility only; no treatment contrast is
interpreted here. Mistral seed 2, Qwen seed 2, and all later blocks remain
unstarted.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed1_recollection_results.csv`; the
generated local report is
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED1_RECOLLECTION_REPORT.md`.
