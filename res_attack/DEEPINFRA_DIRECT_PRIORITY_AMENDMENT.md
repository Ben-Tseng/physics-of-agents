# Prospective Infrastructure Amendment: Qwen Direct Priority Route

Date frozen: 2026-10-29, before any replacement eligibility, power-screen, or
confirmatory outcome was generated.

## Reason for the amendment

The preregistered Qwen seed-0 confirmatory block routed through OpenRouter's
shared DeepInfra pool failed the frozen technical quality gate and is excluded
in full. Subsequent infrastructure-only probes showed that the DeepInfra direct
standard tier was also unreliable under four concurrent requests, while the
DeepInfra direct priority tier passed an independent 20-call stress test with
20/20 nonempty completions, median latency 1.924 seconds, and maximum latency
2.658 seconds.

## Frozen replacement route

- Model: `Qwen/Qwen3.5-9B`
- Backend: DeepInfra OpenAI-compatible API, direct (no OpenRouter intermediary)
- Service tier: `priority`
- Reasoning: disabled with `reasoning_effort=none`
- Workers: 4
- Minimum request-start interval: 0.5 seconds
- Request timeout: 60 seconds
- API retries: 0
- Temperature and all scientific simulation parameters: unchanged

The priority tier has a 50% token-price surcharge. It is used to obtain stable
capacity, not selected based on any attack outcome.

## Required prospective gates

1. Six-question control-only eligibility screen on the frozen training items.
2. Fresh 48-episode training-data stability/power screen under the exact route.
3. Raw-spin parse failures no greater than 1%, unique sender message-call
   failures no greater than 1%, and zero invalid honest credentials.
4. Only after all gates pass may the complete Qwen confirmatory seed-0 block be
   rerun from scratch in a new output root. No partial reuse is allowed.

The failed OpenRouter seed-0 block and all connectivity probes are engineering
audit evidence only and cannot enter confirmatory inference.

## Qualification disposition

The subsequent six-question eligibility run did not complete. Sustained load
produced one roughly 3-minute-44-second stall and two roughly 15-minute stalls,
all beyond the nominal 60-second SDK timeout. The run was interrupted after one
of two interaction steps; only its manifest exists and no episode outcome was
written. This candidate route therefore failed infrastructure qualification.
See `DEEPINFRA_DIRECT_PRIORITY_QUALIFICATION_FAILURE.md`. No power screen or
confirmatory rerun is authorized under this route.
