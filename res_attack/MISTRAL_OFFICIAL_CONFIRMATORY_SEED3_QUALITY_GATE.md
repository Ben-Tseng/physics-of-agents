# Official Mistral confirmatory seed-3 quality-gate decision

Date evaluated: 2026-11-01.

The official `mistral-small-2603` seed-3 block completed all ten frozen cells
and all 180 expected episode files. The audit is filtered to this deployment
and seed and excludes all other seeds, Qwen data, previously excluded blocks,
and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 33/12,960 (0.255%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 33 HTTP 503 high-load errors | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 12/2,880 (0.417%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All 33 raw zero spins were classified as HTTP 503 request errors reporting
temporary service unavailability due to high load, not exhausted parse
failures. The block passes every prospectively fixed technical quality gate
and is admitted as official-Mistral confirmatory seed 3. This decision
concerns technical eligibility only; no treatment contrast is interpreted
here. Mistral seed 4, Qwen seed 4, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed3_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED3_REPORT.md`.
