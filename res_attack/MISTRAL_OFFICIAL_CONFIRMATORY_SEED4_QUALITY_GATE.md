# Official Mistral confirmatory seed-4 quality-gate decision

Date evaluated: 2026-11-02.

The official `mistral-small-2603` seed-4 block completed all ten frozen cells
and all 180 expected episode files. The audit is filtered to this deployment
and seed and excludes all other seeds, Qwen data, previously excluded blocks,
and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 3/12,960 (0.023%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 3 remote connection failures | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All three raw zero spins were classified as upstream disconnect/reset request
errors caused by remote connection failure, not exhausted parse failures. The
block passes every prospectively fixed technical quality gate and is admitted
as official-Mistral confirmatory seed 4. This decision concerns technical
eligibility only; no treatment contrast is interpreted here. Mistral seed 5,
Qwen seed 5, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed4_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED4_REPORT.md`.
