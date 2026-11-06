# Official Mistral confirmatory seed-9 recollection quality-gate decision

Date evaluated: 2026-11-06.

The fresh official `mistral-small-2603` seed-9 recollection completed all ten
frozen cells and all 180 expected episodes. This audit is restricted to
`data/attack_confirmatory_official_two_deployment_mistral_seed9_recollection1`
and excludes the original failed seed-9 block, all other seeds, Qwen data,
other replaced blocks, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 12/12,960 (0.093%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 12 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 1/2,880 (0.035%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All 12 raw zero spins were request errors: 11 upstream connection
timeout/reset failures and one HTTP 502 origin bad-gateway response. There
were no exhausted parse failures and no recovered parse retries. The one
unique sender message-call failure was an HTTP 503 service-unavailable
response. Both prospectively fixed rate limits are satisfied.

The fresh replacement therefore passes every frozen technical gate and is
admitted as the official-Mistral confirmatory seed-9 block. The original
failed block remains excluded in full and none of its episodes are reused.
With this admission, the frozen confirmatory matrix contains all 20 official
model-seed blocks and 3,600/3,600 accepted episodes. No treatment contrast or
full-matrix statistical analysis is performed by this decision.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed9_recollection_results.csv`;
the generated local report is
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED9_RECOLLECTION_REPORT.md`.
