# Prospective official-Qwen seed-4 recollection amendment

Date frozen: 2026-11-02, after the first seed-4 block failed its technical
quality gate and before any replacement-block request.

## Reason

The first official `qwen3.5-27b` confirmatory seed-4 block completed 180/180
episodes but is excluded in full. It contained 320/12,960 raw zero spins
(2.469%), above the prospectively fixed 1% ceiling. All 320 were request
errors: 318 connection errors and 2 timeouts. The message-call and credential
gates passed. No treatment contrast from the failed block was inspected or
used to alter this plan.

## Frozen replacement procedure

1. Run a 20-call connectivity probe using the same official endpoint, model,
   four workers, 0.8-second minimum request interval, 60-second timeout, zero
   retries, and thinking disabled.
2. Authorize recollection only if all 20 calls return nonempty responses. A
   failed probe stops collection and may be repeated later as a new dated
   infrastructure check; it is never experimental data.
3. If the probe passes, recollect the entire balanced ten-cell seed-4 block in
   the fresh root
   `data/attack_confirmatory_official_two_deployment_qwen_seed4_recollection1`.
   Do not copy or reuse any episode from the excluded block.
4. Preserve every scientific and runtime setting from the frozen official
   matrix: 18 test questions, control plus budgets 1/2/4 crossed with
   none/downgrade/drop, eight agents, 28 edges, two interaction steps, three
   spin samples, attack degree four, temperature 0.7, seed 4, four workers,
   0.5-second experimental request interval, 60-second timeout, and zero
   retries.
5. Evaluate the replacement as one indivisible 180-episode block: exactly
   180/180 episodes, at most 1% raw zero spins, at most 1% unique sender
   message-call failures, and zero invalid honest credentials. Parse
   exhaustion and request errors remain separately classified. Any failure
   excludes the entire replacement block.
6. Do not start Qwen seed 5 or Mistral seed 4 until this replacement block
   completes and passes.

The excluded first block remains unchanged at
`data/attack_confirmatory_official_two_deployment/qwen3.5-27b` with its audit in
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED4_QUALITY_GATE.md`.

## Preflight result

The authorized external-network probe passed 20/20 calls on 2026-11-02.
Median latency was 3.111 seconds and maximum latency was 3.502 seconds, with
zero failures. The replacement seed-4 block is therefore authorized under the
frozen procedure. The machine-readable probe is
`res_attack/dashscope_qwen35_27b_seed4_recollection_preflight.json`.

## Replacement-block result

The authorized replacement completed 10/10 cells and 180/180 episodes. It had
0/12,960 raw zero spins, zero exhausted parse failures, zero spin request
errors, zero recovered parse retries, 0/2,880 unique sender message-call
failures, and zero invalid honest credentials. The complete replacement block
passes and is admitted as official-Qwen confirmatory seed 4. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED4_RECOLLECTION_QUALITY_GATE.md`.
