# Official Qwen confirmatory seed-4 quality-gate decision

Date evaluated: 2026-11-01.

The official `qwen3.5-27b` seed-4 block completed all ten frozen cells and all
180 expected episode files. The audit is filtered to this deployment and seed
and excludes all other seeds, Mistral data, the failed Qwen seed-0 attempt,
and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 320/12,960 (2.469%) | at most 1% | **Fail** |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 320 (318 connection, 2 timeout) | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 4/2,880 (0.139%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All 320 raw zero spins were classified as request errors, not exhausted parse
failures. Because the raw-zero rate exceeds the prospectively fixed 1% limit,
the entire block is excluded from confirmatory analysis even though the other
technical gates pass. No treatment contrast is interpreted. Any replacement
must be a prospectively documented full-block recollection in a fresh output
root; no episode from this excluded block may be reused. Qwen seed 5, Mistral
seed 4, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/qwen_official_confirmatory_seed4_results.csv`; the generated local
report is `res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED4_REPORT.md`.
