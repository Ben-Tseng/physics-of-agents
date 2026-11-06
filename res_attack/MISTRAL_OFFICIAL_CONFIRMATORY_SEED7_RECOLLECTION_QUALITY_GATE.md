# Official Mistral confirmatory seed-7 recollection quality-gate decision

Date evaluated: 2026-11-04.

The fresh official `mistral-small-2603` seed-7 recollection completed all ten
frozen cells and all 180 expected episodes. This audit is restricted to
`data/attack_confirmatory_official_two_deployment_mistral_seed7_recollection1`
and does not include any episode from the excluded original seed-7 block,
other seeds, Qwen data, or legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 0/12,960 (0.000%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 0 | classified and retained | Pass |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 0/2,880 (0.000%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

No exhausted parse failures or request errors occurred, so there are no
error subtypes to classify. The entire fresh recollection passes every frozen
technical gate and replaces the excluded original block for confirmatory
inference. The original seed-7 block remains excluded in full and unchanged;
none of its episodes are reused. No treatment contrast is interpreted at this
stage. Mistral seed 8, Qwen seed 8, and all later blocks remain unstarted.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed7_recollection_results.csv`;
the generated local report is
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED7_RECOLLECTION_REPORT.md`.
