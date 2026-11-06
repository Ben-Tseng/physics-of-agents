# Official Qwen confirmatory seed-8 quality-gate decision

Date evaluated: 2026-11-05.

The official `qwen3.5-27b` seed-8 block completed all ten frozen cells and all
180 expected episodes. This audit is filtered to this deployment and seed and
excludes all other seeds, Mistral data, previously excluded or replaced
blocks, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 0/12,960 (0.000%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 0 | classified and retained | Pass |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

No exhausted parse failures or request errors occurred, so there are no
error subtypes to classify. The entire block passes every frozen technical
gate and is admitted as official-Qwen confirmatory seed 8. No treatment
contrast is interpreted at this stage. Qwen seed 9, Mistral seed 8, and all
later blocks remain unstarted.

The episode-level audit is
`res_attack/qwen_official_confirmatory_seed8_results.csv`; the generated local
report is `res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED8_REPORT.md`.
