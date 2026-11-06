# Prospective official-Mistral seed-1 recollection amendment

Date frozen: 2026-10-31, after the first seed-1 block failed its technical
quality gate and before any replacement-block request.

## Reason

The first official `mistral-small-2603` confirmatory seed-1 block completed
180/180 episodes but is excluded in full. It contained 267/12,960 raw zero
spins (2.060%), above the fixed 1% ceiling. All were request errors: 249
connection errors and 18 timeouts. The message-call and credential gates passed.
This pattern is consistent with transient connectivity instability but does not
establish a unique cause. No treatment contrast from the failed block was used
to alter this plan.

## Frozen replacement procedure

1. Run a 20-call connectivity probe using the same official endpoint, version-
   pinned model, four workers, 0.8-second minimum request interval, 60-second
   timeout, and zero retries.
2. Authorize recollection only if all 20 calls return nonempty responses. The
   probe is infrastructure evidence, never experimental data.
3. If the probe passes, recollect the entire balanced ten-cell seed-1 block in
   the fresh root
   `data/attack_confirmatory_official_two_deployment_mistral_seed1_recollection1`.
   Do not copy or reuse any episode from the excluded block.
4. Preserve every scientific and runtime setting from the frozen matrix: 18
   test questions, control plus budgets 1/2/4 crossed with
   none/downgrade/drop, eight agents, 28 edges, two interaction steps, three
   spin samples, attack degree four, temperature 0.7, seed 1, four workers,
   0.8-second request interval, 60-second timeout, and zero retries.
5. Evaluate the replacement as one indivisible 180-episode block: exactly
   180/180 episodes, at most 1% raw zero spins, at most 1% unique sender
   message-call failures, and zero invalid honest credentials. Parse exhaustion
   and request errors remain separately classified. Any failure excludes the
   entire replacement block.
6. Do not start Mistral seed 2, Qwen seed 2, or any later block until this
   replacement completes and passes.

The excluded first block remains unchanged in the original Mistral output root,
with its audit in
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED1_QUALITY_GATE.md`.

## Preflight result

The matching external-network probe passed 20/20 calls on 2026-10-31. Median
latency was 3.113 seconds and maximum latency was 3.484 seconds, with zero
failures. The replacement seed-1 block is therefore authorized. The
machine-readable probe is
`res_attack/mistral_small4_seed1_recollection_preflight.json`.

## Replacement-block result

The authorized replacement completed 10/10 cells and 180/180 episodes. It had
4/12,960 raw zero spins (0.031%), all classified as connection-request errors;
zero exhausted parse failures; zero recovered parse retries; 0/2,880 unique
sender message-call failures; and zero invalid honest credentials. The complete
replacement passes and is admitted as official-Mistral confirmatory seed 1. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED1_RECOLLECTION_QUALITY_GATE.md`.
