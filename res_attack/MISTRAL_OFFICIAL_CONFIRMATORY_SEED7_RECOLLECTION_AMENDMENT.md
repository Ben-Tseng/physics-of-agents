# Prospective official-Mistral seed-7 recollection amendment

Date frozen: 2026-11-04, after the first seed-7 block failed its technical
quality gate and before any replacement-block request.

## Reason

The first official `mistral-small-2603` confirmatory seed-7 block completed
180/180 episodes but is excluded in full. It contained 279/12,960 raw zero
spins (2.153%), above the prospectively fixed 1% ceiling. All were request
errors: 265 connection errors, 13 upstream disconnect/reset failures, and one
HTTP 503 service-unavailable response. The message-call and credential gates
passed. No treatment contrast from the failed block was inspected or used to
alter this plan.

## Frozen replacement procedure

1. Run a 20-call connectivity probe using the same official endpoint,
   version-pinned model, four workers, 0.8-second minimum request interval,
   60-second timeout, and zero retries.
2. Authorize recollection only if all 20 calls return nonempty responses. A
   failed probe stops collection and may be repeated later as a new dated
   infrastructure check; it is never experimental data.
3. If the probe passes, recollect the entire balanced ten-cell seed-7 block in
   the fresh root
   `data/attack_confirmatory_official_two_deployment_mistral_seed7_recollection1`.
   Do not copy or reuse any episode from the excluded block.
4. Preserve every scientific and runtime setting from the frozen official
   matrix: 18 test questions, control plus budgets 1/2/4 crossed with
   none/downgrade/drop, eight agents, 28 edges, two interaction steps, three
   spin samples, attack degree four, temperature 0.7, seed 7, four workers,
   0.8-second request interval, 60-second timeout, and zero retries.
5. Evaluate the replacement as one indivisible 180-episode block: exactly
   180/180 episodes, at most 1% raw zero spins, at most 1% unique sender
   message-call failures, and zero invalid honest credentials. Parse
   exhaustion and request errors remain separately classified. Any failure
   excludes the entire replacement block.
6. Do not start Mistral seed 8, Qwen seed 8, or any later block until this
   replacement completes and passes.

The excluded first block remains unchanged at
`data/attack_confirmatory_official_two_deployment/mistral-small-2603` with its
audit in `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED7_QUALITY_GATE.md`.

## Preflight result

The matching external-network probe passed 20/20 calls on 2026-11-04. Median
latency was 3.054 seconds and maximum latency was 3.909 seconds, with zero
failures. The replacement seed-7 block is therefore authorized. The
machine-readable probe is
`res_attack/mistral_small4_seed7_recollection_preflight.json`.

## Replacement-block result

The authorized fresh recollection completed all ten cells and 180/180
episodes on 2026-11-04. It passed every frozen technical gate: 0/12,960 raw
zero spins, zero exhausted parse failures, zero spin request errors, zero
recovered parse retries, 0/2,880 unique sender message-call failures, and zero
invalid honest credentials. The fresh block is admitted as the official
Mistral seed-7 confirmatory block. The original failed block remains excluded
in full and none of its episodes are reused. No treatment contrast was
interpreted, and Mistral seed 8 and Qwen seed 8 remain unstarted. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED7_RECOLLECTION_QUALITY_GATE.md`.
