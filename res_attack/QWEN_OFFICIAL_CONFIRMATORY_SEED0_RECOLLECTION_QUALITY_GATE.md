# Official Qwen confirmatory seed-0 recollection quality-gate decision

Date evaluated: 2026-10-30.

The replacement `qwen3.5-27b` seed-0 block completed all ten frozen cells and
all 180 expected episode files in the fresh recollection root. The excluded
first seed-0 block was not included in this audit.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 0/12,960 (0.000%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 0 | classified and retained | Pass |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

The replacement block passes every prospectively fixed technical quality gate
and is admitted as the official-Qwen confirmatory seed-0 block. This decision
concerns technical eligibility only; no treatment contrast is interpreted here.
Qwen seed 1 and every Mistral confirmatory block remain unstarted.

The episode-level audit is
`res_attack/qwen_official_confirmatory_seed0_recollection_results.csv`; the
generated local report is
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED0_RECOLLECTION_REPORT.md`. Raw files
are in
`data/attack_confirmatory_official_two_deployment_recollection1/qwen3.5-27b`.
