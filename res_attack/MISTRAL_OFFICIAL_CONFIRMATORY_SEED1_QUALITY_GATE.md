# Official Mistral confirmatory seed-1 quality-gate decision

Date evaluated: 2026-10-30.

The official `mistral-small-2603` seed-1 block completed all ten frozen cells
and all 180 expected episode files. The audit is filtered to this deployment
and seed and excludes all Qwen, other-seed, and legacy DeepInfra data.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 267/12,960 (2.060%) | at most 1% | **Fail** |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 267 | classified and retained | Audit |
| Recovered parse retries | 0 | classified and retained | Pass |
| Unique sender message-call failures | 14/2,880 (0.486%) | at most 1% | Pass |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All 267 raw zero spins were request errors, not exhausted parse failures: 249
connection errors and 18 request timeouts. The 14 unique sender message-call
failures comprised 13 connection errors and one timeout. Raw-zero failures were
concentrated in `attack1_downgrade` (117) and `attack4_downgrade` (133), with 16
in `attack1_none` and one in control.

Because 267/12,960 exceeds the frozen 1% ceiling, the entire Mistral seed-1
block fails the technical quality gate and is excluded from confirmatory
inference. No treatment contrast from the block is interpreted. Mistral seed 2,
Qwen seed 2, and all later blocks remain unstarted. Any replacement requires a
prospectively documented full-block recollection; no episode from this failed
block may be reused.

The episode-level audit is
`res_attack/mistral_official_confirmatory_seed1_results.csv`; the generated
local report is `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED1_REPORT.md`.
