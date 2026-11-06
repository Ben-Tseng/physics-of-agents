# Official Qwen confirmatory seed-0 quality-gate decision

Date evaluated: 2026-10-30.

The official `qwen3.5-27b` seed-0 block completed all ten frozen cells and all
180 expected episode files. The block is evaluated as one indivisible unit
under the prospectively fixed technical quality gate.

| Check | Observed | Frozen requirement | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Raw zero spins | 9/12,960 (0.069%) | at most 1% | Pass |
| Exhausted parse failures | 0 | classified and retained | Pass |
| Spin request errors | 9 | classified and retained | Audit |
| Unique sender message-call failures | 37/2,880 (1.285%) | at most 1% | **Fail** |
| Invalid honest credentials | 0 | exactly 0 | Pass |

All nine raw zero spins were classified as request errors (`RuntimeError`), not
as exhausted parse failures. The 37 unique sender message-call failures were
concentrated in the `attack1_downgrade` cell: 36 connection errors and one
request timeout. The remaining nine cells had no message-call failures.

Because 37/2,880 exceeds the frozen 1% ceiling, the entire official-Qwen seed-0
confirmatory block fails the technical quality gate and is excluded from
confirmatory inference. No treatment contrast from this block is interpreted.
Qwen seed 1 and every Mistral confirmatory block remain unstarted pending a
prospective decision about whether and how to recollect a replacement block.

The episode-level audit table is
`res_attack/qwen_official_confirmatory_seed0_results.csv`; the generated local
summary is `res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED0_REPORT.md`. Raw episode
files remain unchanged in
`data/attack_confirmatory_official_two_deployment/qwen3.5-27b`.
