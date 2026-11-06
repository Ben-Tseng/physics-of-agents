# Official Qwen confirmatory seed-1 quality-gate decision

Date evaluated: 2026-10-30.

The official `qwen3.5-27b` seed-1 block completed all ten frozen cells and all
180 expected episode files. The audit is filtered to this deployment and seed;
it excludes the failed seed-0 attempt, the accepted seed-0 recollection,
Mistral data, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 0/12,960 (0.000%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 0 | classified and retained | Pass |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

The block passes every prospectively fixed technical quality gate and is
admitted as official-Qwen confirmatory seed 1. This decision concerns technical
eligibility only; no treatment contrast is interpreted here. Qwen seed 2,
Mistral seed 1, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/qwen_official_confirmatory_seed1_results.csv`; the generated local
report is `res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED1_REPORT.md`.
