# Prospective Replacement Amendment: Official Qwen3.5-27B Deployment

Date frozen: 2026-10-29, before any eligibility, power-screen, or confirmatory
outcome from this deployment was generated.

## Rationale

Qwen3.5-9B on both the OpenRouter/DeepInfra shared route and DeepInfra direct
priority route failed sustained infrastructure qualification. Alibaba Cloud
Model Studio does not offer that exact 9B checkpoint as a standard managed API,
so the official open-weight `qwen3.5-27b` endpoint is admitted as a new Qwen
deployment. This is a model-and-deployment replacement, not a continuation of
the failed 9B confirmatory block.

## Frozen route

- Model ID: `qwen3.5-27b`
- Provider: Alibaba Cloud Model Studio (official Qwen API)
- Region: Singapore
- Endpoint: workspace-dedicated OpenAI-compatible endpoint
- Thinking mode: disabled (`enable_thinking=false`)
- Workers: 4
- Minimum request-start interval: 0.5 seconds
- Request timeout: 60 seconds
- API retries: 0
- Temperature and all scientific simulation parameters: unchanged

An independent 20-call infrastructure probe passed 20/20, with median latency
1.491 seconds and maximum latency 4.993 seconds. The probe contains no paper
questions and is not analysis data.

## Required gates

1. Control-only eligibility on the same six frozen training questions.
2. Fresh 48-episode training-data power/stability screen under the exact route.
3. At most 1% raw-spin parse failures, at most 1% unique sender message-call
   failures, and zero invalid honest credentials.
4. Only after every gate passes may a new confirmatory matrix be frozen for
   this deployment. No failed or partial Qwen3.5-9B episode may be reused.

The official Qwen3.5-27B deployment and Mistral Small 4 official deployment will
be interpreted as cross-deployment replication, not a controlled model-size
comparison.

## Eligibility result

The frozen six-question control screen completed 6/6 episodes. Five of six had
a correct terminal majority, mean final agent accuracy was 0.8333, raw-spin
parse failures were 0/432, unique sender message-call failures were 0/96, and
invalid honest credentials were zero. The competence and technical quality
gates both passed. The deployment is authorized for the fresh 48-episode
training-data stability/power screen, but not yet for confirmatory collection.

## First seed-0 power tranche and diagnostic amendment

The first four-cell seed-0 tranche completed 24/24 episodes but failed the
frozen raw-spin quality gate: 77/1,728 raw samples were zero (4.456%), versus
the at-most-1% limit. Message-call failures were 0/384 and invalid honest
credentials were zero. Seed 1 was not started, and no treatment contrast is
admitted from this tranche.

The 77 zeros all occurred in the initial, pre-message phase of one cell and
were clustered by question. The legacy collector collapsed exhausted parsing
and request exceptions into the same zero value without recording their type.
This makes the cause unidentifiable from the completed files. The tranche is
excluded and retained as an auditable infrastructure-quality failure.

Before any rerun, instrumentation was changed to record per-sample
`parse_failure`, `parse_retry`, and `request_error` diagnostics. This is an
observability-only amendment: no prompt, parser, model, temperature, retry
count, concurrency, question, attack, defense, or outcome definition changed.
The same frozen seed-0 matrix may be rerun into a fresh output directory. It
must independently satisfy the original at-most-1% raw-zero gate, at-most-1%
message-call gate, and zero-invalid-credential gate before seed 1 is authorized.

## Seed-0 rerun result

The fresh observability-amended rerun completed 4/4 cells and 24/24 episodes.
It recorded 0/1,728 raw zero spins, zero exhausted parse failures, zero spin
request errors, zero recovered parse retries, 0/384 unique sender message-call
failures, and zero invalid honest credentials. It therefore passes all frozen
technical quality gates. The legacy tranche remains excluded and separate.
Seed 1 is authorized under the unchanged frozen matrix.

## Complete power/stability screen

Seed 1 also completed cleanly. Across the accepted 48 episodes, the official
Qwen deployment recorded 0/3,456 raw zero spins, zero exhausted parse failures,
zero spin request errors, zero recovered parse retries, 0/768 unique sender
message failures, and zero invalid honest credentials. The deployment passes
the full stability gate and is eligible for a newly frozen confirmatory matrix.

Training-data descriptive incorrect-majority rates were 2/12 in every condition
(control, no defense, downgrade, and drop). Mean agent accuracy was 0.833,
0.760, 0.833, and 0.812, respectively. These screening statistics are not
confirmatory tests and are not used to alter the frozen scientific design.
