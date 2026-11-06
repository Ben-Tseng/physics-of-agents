# Aborted live-run audit log

## 2026-10-28: Gemma replacement control, seed 0

- Output target: `data/attack_power_screen/gemma-3-12b-it/control__seed0`
- Observed issue: an approximately 18-minute message-call stall during step 1.
- Action: manually interrupted under the provider-stability quality gate.
- Data disposition: the directory contained only `manifest.json`; no completed
  episode JSON was written or analyzed.
- Amendment: subsequent replacement-model jobs use a 60-second request timeout
  with zero project-wrapper API retries. Individual failures remain observable in
  parse/message error fields.

## 2026-10-28: Gemma 3 12B replacement control retry, seed 0

- Output target: `data/attack_power_screen/gemma-3-12b-it/control__seed0`
- Observed issue: with wrapper retries fixed at zero, multiple concurrent calls
  still failed to return beyond the stated 60-second boundary.
- Action: manually interrupted before dynamics completed.
- Data disposition: the directory still contained only `manifest.json`; no
  completed episode JSON was written or analyzed.
- Candidate disposition: Gemma 3 12B was retired for route operability before any
  attack outcome. Gemma 3 27B on the same provider requires a new, separate
  control-only eligibility screen.
# 2026-10-28 Qwen confirmatory sandbox-network failure

The first seed-0 invocation was accidentally executed in a network-restricted
local sandbox. All 15,840 attempted calls failed immediately with the identical
local `Connection error`; the resulting 180 episode files contained 12,960 raw
spin failures and 2,880 message-call failures. No model response was obtained,
so these are not scientific outcomes and they are excluded in full. The files
were preserved, without deletion, under
`data/attack_confirmatory_qwen_sandbox_failure_20261028`. The clean output root
was recreated before a network-enabled rerun of the same frozen matrix.
