# Official Mistral confirmatory seed-2 quality-gate decision

Date evaluated: 2026-11-01.

The official `mistral-small-2603` seed-2 block completed all ten frozen cells
and all 180 expected episode files. The audit is filtered to this deployment
and seed and excludes all other seeds, Qwen data, previously excluded blocks,
and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 1/12,960 (0.008%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 1 connection error | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

The single raw zero spin was classified as a connection-request error, not an
exhausted parse failure. The block passes every prospectively fixed technical
quality gate and is admitted as official-Mistral confirmatory seed 2. This
decision concerns technical eligibility only; no treatment contrast is
interpreted here. Mistral seed 3, Qwen seed 3, and all later blocks remain
unstarted.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed2_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED2_REPORT.md`.
