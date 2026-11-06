# Official Mistral confirmatory seed-0 quality-gate decision

Date evaluated: 2026-10-30.

The official `mistral-small-2603` seed-0 block completed all ten frozen cells
and all 180 expected episode files. The audit contains only this deployment and
seed; no Qwen or legacy DeepInfra data are included.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 2/12,960 (0.015%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 2 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 2/2,880 (0.069%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

Both raw zero spins were classified as request errors, not exhausted parse
failures. The two unique sender message-call failures were connection errors.
The block passes every prospectively fixed technical quality gate and is
admitted as official-Mistral confirmatory seed 0. This decision concerns
technical eligibility only; no treatment contrast is interpreted here.
Mistral seed 1, Qwen seed 1, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed0_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED0_REPORT.md`.
