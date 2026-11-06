# Official Qwen confirmatory seed-4 recollection quality-gate decision

Date evaluated: 2026-11-02.

The authorized fresh `qwen3.5-27b` seed-4 replacement block completed all ten
frozen cells and all 180 expected episode files. The audit is restricted to
`data/attack_confirmatory_official_two_deployment_qwen_seed4_recollection1`
and excludes the original failed seed-4 block, all other seeds, Mistral data,
and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 0/12,960 (0.000%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 0 | classified and retained | Pass |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

The complete replacement passes every prospectively fixed technical quality
gate and is admitted as official-Qwen confirmatory seed 4. The original failed
block remains separate and excluded. This decision concerns technical
eligibility only; no treatment contrast is interpreted here. Qwen seed 5,
Mistral seed 4, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/qwen_official_confirmatory_seed4_recollection_results.csv`; the
generated local report is
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED4_RECOLLECTION_REPORT.md`.
