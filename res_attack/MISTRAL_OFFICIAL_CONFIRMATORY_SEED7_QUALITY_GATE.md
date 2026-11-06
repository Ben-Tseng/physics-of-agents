# Official Mistral confirmatory seed-7 quality-gate decision

Date evaluated: 2026-11-04.

The official `mistral-small-2603` seed-7 block completed all ten frozen cells
and all 180 expected episode files. The audit is filtered to this deployment
and seed and excludes all other seeds, Qwen data, previously excluded or
replaced blocks, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 279/12,960 (2.153%) | at most 1% | **Fail** |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 279 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 17/2,880 (0.590%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All 279 raw zero spins were classified as request errors, not exhausted parse
failures: 265 connection errors, 13 upstream disconnect/reset failures, and
one HTTP 503 service-unavailable response. Because the raw-zero rate exceeds
the prospectively fixed 1% limit, the entire block is excluded from
confirmatory inference despite passing all other gates. No treatment contrast
is interpreted. Any replacement must be prospectively documented as a full
ten-cell recollection in a fresh output root; no episode from this failed
block may be reused. Mistral seed 8, Qwen seed 8, and all later blocks remain
unstarted.

The diagnostic episode-level audit is
`res_attack/mistral_official_confirmatory_seed7_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED7_REPORT.md`.
