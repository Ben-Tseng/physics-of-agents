# Official Qwen confirmatory seed-9 quality-gate decision

Date evaluated: 2026-11-05.

The official `qwen3.5-27b` seed-9 block completed all ten frozen cells and all
180 expected episodes. This audit is filtered to this deployment and seed and
excludes all other seeds, Mistral data, previously excluded or replaced
blocks, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 1/12,960 (0.008%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 1 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

The single raw zero spin was classified as a request timeout, not an
exhausted parse failure. Its rate remains below the prospectively fixed 1%
limit. The entire block therefore passes every frozen technical gate and is
admitted as official-Qwen confirmatory seed 9. No treatment contrast is
interpreted at this stage. Mistral seed 9 remains unstarted.

The episode-level audit is
`res_attack/qwen_official_confirmatory_seed9_results.csv`; the generated local
report is `res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED9_REPORT.md`.
