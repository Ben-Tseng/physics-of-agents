# Official Mistral confirmatory seed-6 quality-gate decision

Date evaluated: 2026-11-03.

The official `mistral-small-2603` seed-6 block completed all ten frozen cells
and all 180 expected episode files. The audit is filtered to this deployment
and seed and excludes all other seeds, Qwen data, previously excluded or
replaced blocks, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 2/12,960 (0.015%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 2 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 1/2,880 (0.035%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

Both raw zero spins were classified as request errors, not exhausted parse
failures: one connection error and one request timeout. The block passes every
prospectively fixed technical quality gate and is admitted as
official-Mistral confirmatory seed 6. This decision concerns technical
eligibility only; no treatment contrast is interpreted here. Mistral seed 7,
Qwen seed 7, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed6_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED6_REPORT.md`.
