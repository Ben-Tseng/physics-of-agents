# Official Qwen confirmatory seed-7 quality-gate decision

Date evaluated: 2026-11-03.

The official `qwen3.5-27b` seed-7 block completed all ten frozen cells and all
180 expected episode files. The audit is filtered to this deployment and seed
and excludes all other seeds, Mistral data, previously excluded or replaced
blocks, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 29/12,960 (0.224%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 29 connection errors | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All 29 raw zero spins were classified as connection-request errors, not
exhausted parse failures. The block passes every prospectively fixed technical
quality gate and is admitted as official-Qwen confirmatory seed 7. This
decision concerns technical eligibility only; no treatment contrast is
interpreted here. Qwen seed 8, Mistral seed 7, and all later blocks remain
unstarted.

The episode-level audit is
`res_attack/qwen_official_confirmatory_seed7_results.csv`; the generated local
report is `res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED7_REPORT.md`.
