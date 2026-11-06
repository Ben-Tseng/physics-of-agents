# Prospective official-Qwen seed-0 recollection amendment

Date frozen: 2026-10-30, after the first seed-0 block failed its technical
quality gate and before any replacement-block request.

## Reason

The first official `qwen3.5-27b` confirmatory seed-0 block completed 180/180
episodes but is excluded in full. It contained 37/2,880 unique sender
message-call failures (1.285%), above the prospectively fixed 1% ceiling. All 37
were concentrated in `attack1_downgrade`; the other nine cells had none. The
raw-zero rate and credential gate passed. No treatment contrast from the failed
block was inspected or used to alter this plan.

## Frozen replacement procedure

1. Run a 20-call connectivity probe using the same official endpoint, model,
   four workers, 0.5-second minimum request interval, 60-second timeout, zero
   retries, and thinking disabled.
2. Authorize recollection only if all 20 calls return nonempty responses. A
   failed probe stops collection and may be repeated later as a new dated
   infrastructure check; it is never experimental data.
3. If the probe passes, recollect the entire balanced ten-cell seed-0 block in
   the fresh root
   `data/attack_confirmatory_official_two_deployment_recollection1`. Do not copy
   or reuse any episode from the excluded block.
4. Preserve every scientific and runtime setting from the frozen official
   matrix: 18 test questions, control plus budgets 1/2/4 crossed with
   none/downgrade/drop, eight agents, 28 edges, two interaction steps, three
   spin samples, attack degree four, temperature 0.7, seed 0, four workers,
   0.5-second request interval, 60-second timeout, and zero retries.
5. Evaluate the replacement as one indivisible 180-episode block: exactly
   180/180 episodes, at most 1% raw zero spins, at most 1% unique sender
   message-call failures, and zero invalid honest credentials. Parse exhaustion
   and request errors remain separately classified. Any failure excludes the
   entire replacement block.
6. Do not start Qwen seed 1 or any Mistral confirmatory block until this
   replacement block completes and passes.

The excluded first block remains unchanged at
`data/attack_confirmatory_official_two_deployment/qwen3.5-27b` with its audit in
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED0_QUALITY_GATE.md`.

## Preflight result

The authorized external-network probe passed 20/20 calls on 2026-10-30. Median
latency was 1.972 seconds and maximum latency was 2.035 seconds, with zero
failures. The replacement seed-0 block is therefore authorized under the frozen
procedure. The machine-readable probe is
`res_attack/dashscope_qwen35_27b_seed0_recollection_preflight.json`.

## Replacement-block result

The authorized replacement completed 10/10 cells and 180/180 episodes. It had
0/12,960 raw zero spins, zero exhausted parse failures, zero spin request
errors, zero recovered parse retries, 0/2,880 unique sender message-call
failures, and zero invalid honest credentials. The complete replacement block
passes and is admitted as official-Qwen confirmatory seed 0. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED0_RECOLLECTION_QUALITY_GATE.md`.
