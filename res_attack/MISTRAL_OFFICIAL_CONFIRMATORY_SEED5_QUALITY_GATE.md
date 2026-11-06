# Official Mistral confirmatory seed-5 quality-gate decision

Date evaluated: 2026-11-02.

The official `mistral-small-2603` seed-5 block completed all ten frozen cells
and all 180 expected episode files. The audit is filtered to this deployment
and seed and excludes all other seeds, Qwen data, previously excluded blocks,
and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 60/12,960 (0.463%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 60 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 10/2,880 (0.347%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All 60 raw zero spins were classified as request errors, not exhausted parse
failures: 44 connection errors, 15 request timeouts, and one upstream
disconnect/reset before response headers. The block passes every
prospectively fixed technical quality gate and is admitted as
official-Mistral confirmatory seed 5. This decision concerns technical
eligibility only; no treatment contrast is interpreted here. Mistral seed 6,
Qwen seed 6, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed5_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED5_REPORT.md`.
