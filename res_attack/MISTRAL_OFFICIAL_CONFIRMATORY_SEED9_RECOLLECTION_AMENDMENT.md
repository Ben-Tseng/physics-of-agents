# Prospective official-Mistral seed-9 recollection amendment

Date frozen: 2026-11-06, after the first seed-9 block failed its technical
quality gate and before any replacement-block request.

## Reason

The first official `mistral-small-2603` confirmatory seed-9 block completed
180/180 episodes but is excluded in full. It contained 39/2,880 unique sender
message-call failures (1.354%), above the prospectively fixed 1% ceiling:
35 connection errors and four request timeouts. Raw zero spins were
55/12,960 (0.424%), within their limit, and invalid honest credentials were
zero. No treatment contrast from the failed block was inspected or used to
alter this plan.

## Frozen replacement procedure

1. Run a 20-call connectivity probe using the same official endpoint,
   version-pinned model, four workers, 0.8-second minimum request interval,
   60-second timeout, and zero retries.
2. Authorize recollection only if all 20 calls return nonempty responses. A
   failed probe stops collection and may be repeated later as a new dated
   infrastructure check; it is never experimental data.
3. If the probe passes, recollect the entire balanced ten-cell seed-9 block in
   the fresh root
   `data/attack_confirmatory_official_two_deployment_mistral_seed9_recollection1`.
   Do not copy or reuse any episode from the excluded block.
4. Preserve every scientific and runtime setting from the frozen official
   matrix: 18 test questions, control plus budgets 1/2/4 crossed with
   none/downgrade/drop, eight agents, 28 edges, two interaction steps, three
   spin samples, attack degree four, temperature 0.7, seed 9, four workers,
   0.8-second request interval, 60-second timeout, and zero retries.
5. Evaluate the replacement as one indivisible 180-episode block: exactly
   180/180 episodes, at most 1% raw zero spins, at most 1% unique sender
   message-call failures, and zero invalid honest credentials. Parse
   exhaustion and request errors remain separately classified. Any failure
   excludes the entire replacement block.
6. Do not start full-matrix statistical analysis or any new experiment until
   this replacement completes and passes.

The excluded first block remains unchanged at
`data/attack_confirmatory_official_two_deployment/mistral-small-2603` with its
audit in `res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED9_QUALITY_GATE.md`.

## First replacement preflight result

The first matching replacement preflight on 2026-11-06 failed 0/20 calls.
Every call returned a connection error; a separate single-call diagnostic
confirmed the same connection-error class without exposing credentials. In
accordance with the frozen procedure, no replacement episode was started and
the fresh output root remains unused. The probe may be repeated later as a
new dated infrastructure check. Its machine-readable record is
`res_attack/mistral_small4_seed9_recollection_preflight.json`.

## Second replacement preflight result

A second, independently recorded preflight on 2026-11-06 also failed 0/20
calls, again uniformly classified as connection errors. A DNS-level check
then showed that the execution environment could not resolve either
`api.mistral.ai` or a separate control API hostname, identifying general DNS
unavailability rather than an experimental or parsing failure. No replacement
episode was started and the fresh output root remains unused. The second
machine-readable probe is
`res_attack/mistral_small4_seed9_recollection_preflight2.json`.

## Third replacement preflight result

After external-network access was restored, a third independently recorded
preflight on 2026-11-06 passed 20/20 calls. Median latency was 3.084 seconds,
maximum latency was 3.327 seconds, and there were zero failures. The complete
fresh Mistral seed-9 replacement block is therefore authorized under the
frozen procedure. The machine-readable probe is
`res_attack/mistral_small4_seed9_recollection_preflight3.json`.

## Replacement-block result

The authorized fresh recollection completed all ten cells and 180/180
episodes on 2026-11-06. It passed every frozen technical gate: 12/12,960 raw
zero spins (0.093%), all classified as request errors; zero exhausted parse
failures; zero recovered parse retries; 1/2,880 unique sender message-call
failures (0.035%); and zero invalid honest credentials. The fresh block is
admitted as the official Mistral seed-9 confirmatory block. The original
failed block remains excluded in full and none of its episodes are reused.
The frozen confirmatory matrix is now complete at 20/20 formal blocks and
3,600/3,600 accepted episodes. No full-matrix statistical analysis or new
experiment was started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED9_RECOLLECTION_QUALITY_GATE.md`.
