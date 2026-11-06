# Official Mistral confirmatory seed-9 quality-gate decision

Date evaluated: 2026-11-05.

The official `mistral-small-2603` seed-9 block completed all ten frozen cells
and all 180 expected episodes. This audit is filtered to this deployment and
seed and excludes all other seeds, Qwen data, previously excluded or replaced
blocks, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 55/12,960 (0.424%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 55 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 39/2,880 (1.354%) | at most 1% | **Fail** |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All 55 raw zero spins were request errors: 41 connection errors and 14 request
timeouts. There were no exhausted parse failures and no recovered parse
retries. The 39 unique sender message-call failures comprised 35 connection
errors and four request timeouts. Their combined rate of 1.354% exceeds the
prospectively frozen at-most-1% limit.

The entire official-Mistral seed-9 block therefore fails the frozen technical
gate and is excluded in full. No episode from this block may be reused and no
treatment contrast is interpreted. A replacement, if authorized, must be a
prospectively documented full-block recollection in a fresh output root after
a new matching connectivity preflight.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed9_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED9_REPORT.md`.
