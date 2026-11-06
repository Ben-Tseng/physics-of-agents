# Execution status

## Completed

- Fixed upstream commit `62bf0e7ddb94e6be936bed6a35aefea94e8d54a9` on branch
  `attack-authentication`.
- Created a Python 3.9 virtual environment from the official requirements.
- Passed the offline mock data-generation pipeline without an API key.
- Executed `res/4_prediction.ipynb` on the released data.
- Reproduced 372 stored numeric parameters with maximum absolute difference
  `5.11e-13`.
- Confirmed that all 20 five-coupling values used by the draft are the official
  fitted values rounded to two decimals.
- Added and ran a released-data counterfactual attack experiment using objective
  test episodes, real signed graphs, fitted fields, truth labels, and initial
  spins.
- Ran four random seeds for all four models and three defenses.
- Ran random, hub, and weak-field targeting for GPT-4o-mini and Llama-3-8B.
- Passed three unit tests for nested budgets, drop invariance, and false-message
  pressure.

## Main random-target result

| Model | No defense k* | Downgrade k* | Observed multiplier | Weight-ratio prediction |
| --- | ---: | ---: | ---: | ---: |
| GPT-4o-mini | 2.310 | 5.961 | 2.581 | 3.133 |
| Gemma-3n-E4B | 8.674 | 10.687 | 1.232 | 1.207 |
| Qwen3.5-9B | 4.963 | 8.771 | 1.767 | 1.767 |
| Llama-3-8B | 7.496 | 13.878 | 1.851 | 1.859 |

Values are means over four seeds. Full standard deviations and curves are in
`res_attack/results/`.

## Interpretation boundary

The fitted model's no-attack terminal-majority agreement with the released LLM
episodes ranges from about 0.656 to 0.901 across models. The new experiment is
therefore evidence about the fitted statistical model, not yet direct evidence
that live LLM agents respond identically under attack.

The next publication gate is a small live-model pilot with at least two open
models. It should preserve the original prompt/control path at `k=0`, verify
credentials before prompt construction, and record sender, receiver, claimed
relationship, verification result, message, raw samples, seed, and model build.

## Live-model pilot completed

The authenticated live pilot ran through OpenRouter with provider pinning to
DeepInfra, fallback disabled, data collection denied, and reasoning disabled.
It used two open-weight models: `qwen/qwen3.5-9b` and
`meta-llama/llama-3.1-8b-instruct`.

- Qwen: control plus three attack defenses, with three API repetitions per
  condition.
- Llama: control plus three attack defenses, with one API repetition per
  condition.
- Each run used one objective question, 8 agents, 2 interaction steps, 3 spin
  samples, attack budget 1, and attacker degree 4.
- Across 16 runs and 1,408 API calls there were zero raw-spin parse failures,
  zero message-call errors, and zero invalid honest credentials.
- All attacker envelopes followed the intended policy: `agree` under no
  defense, `unknown` under downgrade, and `drop` under drop.
- At the post-run audit, OpenRouter reported cumulative usage of `$0.11744779`
  and `$1.88255221` remaining under the `$2` key limit.

The machine-readable table is `res_attack/live_pilot_results.csv`; the readable
audit is `res_attack/LIVE_PILOT_REPORT.md`. The pilot validates model access,
prompt execution, authentication, routing, and logging. It does **not** estimate
an attack or defense effect: there is only one question, Llama has one API
repetition, and stochastic API conditions do not share random draws. A
publication experiment still requires a preregistered question set, multiple
budgets and graph/attack configurations, adequate independent repetitions,
uncertainty intervals, and multiplicity-aware comparisons.

## Formal experiment preparation and power screen

The confirmatory design is preregistered in
`res_attack/EXPERIMENT_PREREGISTRATION.md`, with the machine-readable design in
`res_attack/formal_experiment_config.json`. It reserves six balanced, text-only
training questions for the power screen and 18 balanced, text-only test questions
for confirmation. The command matrix contains 16 jobs, 96 episodes, and 8,448
estimated calls.

The Qwen power screen is complete: 8 jobs and 48 episodes across two seeds. Llama
seed 0 has complete control, no-defense, and downgrade cells (18 episodes); drop
was stopped during its initial spin phase and produced no episode file. Complete
data have zero parse failures, zero message errors, and zero invalid honest
credentials. The partial audit is `res_attack/POWER_SCREEN_PARTIAL_REPORT.md`,
and descriptive effect/sensitivity results are in
`res_attack/POWER_SCREEN_ANALYSIS.md`.

DeepInfra produced one approximately 33-minute response in the seed-1 control.
An operational amendment then added a 60-second per-request timeout and disabled
SDK-internal retries, retaining only the project's explicit retry loop. On resume,
the next job again encountered repeated timeouts, so collection was paused under
the preregistered quality gate. Its incomplete directory contains only a manifest
and is excluded from summaries; the resumable matrix runner skips only jobs with
all six episode files.

Llama was subsequently reduced from eight to four request workers. This reduced
request pressure but did not eliminate multi-minute timeout/retry bursts, so its
remaining cells are paused. Resume only when the pinned DeepInfra route is stable;
do not switch providers mid-experiment without a new design amendment and separate
batch label.

The Llama route is now designated feasibility-only rather than an eligible
confirmatory model: its seed-0 control had 3/6 incorrect terminal majorities and
mean agent accuracy 0.417, in addition to the route instability. Before sending
any replacement-model request, a dated amendment fixed a control-only eligibility
screen for `google/gemma-3-12b-it` on the same six questions and pinned DeepInfra
provider. Passing requires at least 4/6 correct terminal majorities, mean agent
accuracy at least 0.60, and zero parsing, message-call, credential, or terminal
retry failures. Complete Llama episodes remain in the audit trail and will not be
silently pooled with confirmatory results.

Gemma passed that frozen eligibility screen: 4/6 correct terminal majorities,
mean agent accuracy 0.667, and zero parse, message-call, or credential failures.
The six eligibility episodes are kept separate from effect estimation. A fresh
eight-job Gemma replacement matrix is generated in
`res_attack/gemma_power_screen_matrix.csv`.

The first fresh Gemma control attempt then encountered an approximately
18-minute message-call stall and was interrupted before any episode file was
written. The audit is in `res_attack/ABORTED_RUN_LOG.md`. The explicit SDK timeout
was already active, but the project wrapper still permitted four retries. The
replacement matrix now fixes wrapper retries at zero: each failed request remains
visible to the predeclared error-rate quality gate instead of creating a long,
opaque retry burst.

That zero-retry attempt also stalled beyond the stated 60-second boundary before
writing an episode, so Gemma 3 12B is retired for provider operability. No Gemma
attack outcome has been observed. The next candidate is Gemma 3 27B IT on
DeepInfra, selected before requests because its listed FP8 endpoint showed 100%
30-minute and about 99.86% one-day uptime. It must pass the same separate
control-only eligibility screen before a replacement power matrix is run.

Gemma 3 27B passed: 4/6 correct terminal majorities, mean agent accuracy 0.729,
and zero parse, message-call, or credential failures. Its six eligibility
episodes remain separate. The formal eligible pair is now Qwen 3.5 9B plus
Gemma 3 27B, both routed through DeepInfra with provider fallback disabled.

The first complete 48-episode Gemma power batch then failed the frozen quality
gate despite complete files: 161/3,456 spin failures (4.66%) and 90/768 unique
sender message-call failures (11.72%), with zero credential failures. It is
excluded in full. The decision is recorded in
`res_attack/POWER_SCREEN_QUALITY_GATE.md`. A new eight-job clean batch uses one
worker, zero API retries, and `data/attack_power_screen_clean`; Gemma is not yet
confirmatory-eligible until that entire batch stays at or below 1% for both error
rates.

The first single-worker clean control also failed because the provider returned
HTTP 429: 138/432 spin failures and 59/96 message-call failures. Error metadata
identified an 80-request/minute shared-capacity limit plus DeepInfra
`engine_overloaded`. A new throttled batch spaces starts by 1.1 seconds (about
55/minute maximum), retains one worker and zero retries, and writes to
`data/attack_power_screen_throttled`. Only its control runs before the remaining
cells are authorized by the same 1% quality gate.

The throttled DeepInfra control still failed at 20.83% for both spin and message
calls because DeepInfra continued returning `engine_overloaded`. DeepInfra Gemma
collection is stopped. The next design uses the common Parasail provider for both
Qwen 3.5 9B and Gemma 3 27B, so model effects are not confounded with provider.
Both deployments must pass separate six-question control eligibility runs before
any Parasail attack cell is collected; all prior DeepInfra outcomes remain
separate engineering/feasibility evidence.

Parasail preflight passed 4/4 for Qwen but failed 0/4 for Gemma 3 27B with
upstream 429 responses; no Parasail episode was launched. Gemma is retired from
the replacement search. The next sole candidate is open-weight Mistral Nemo 12B
on DeepInfra, selected before requests because its FP8 route listed 100% uptime
over both 30 minutes and one day. It must pass the same six-question control
screen before any attack cell.

Mistral completed cleanly with zero infrastructure or credential errors, but
failed the frozen task-competence gates: 3/6 correct terminal majorities and mean
agent accuracy 0.500. No Mistral attack cell is authorized. Only Qwen currently
qualifies, so the minimum two-model publication requirement remains unmet.
Public-route candidate shopping is stopped; the next defensible path is a local
open-weight deployment or provider BYOK capacity, then the same control-only
screen. Current OpenRouter key usage is approximately $0.969 of its $2 limit.

A local-hosting audit found an Apple M2 with 8 GB memory and about 15 GB free
disk, insufficient for a robust 12B+ local deployment. One final candidate is
therefore admitted before requests: open-weight Llama 3.3 70B Instruct on the
same DeepInfra provider, whose FP8 route listed 100% 30-minute and about 99.86%
one-day uptime. It must pass the frozen control screen; failure ends candidate
search and requires BYOK capacity or additional hardware.

Llama 3.3 70B completed all six frozen control episodes without parse,
message-call, or credential failures, but failed task competence: only 2/6
terminal majorities were correct and mean agent accuracy was 0.292. No attack
cell was run. Public-route candidate search is now stopped as preregistered.
The current publishable scope is therefore the released-data statistical-model
experiment plus a one-model (Qwen) live power screen and multi-model feasibility
audit; a paper claiming live two-model generalization remains blocked until a
BYOK or better-equipped local deployment passes the same prospective screen.
After this screen, OpenRouter reported cumulative key usage of `$1.023237502`
and `$0.976762498` remaining under the `$2` key limit. Collection is stopped, so
the remaining balance is preserved for a future preregistered deployment rather
than further post-outcome candidate search.

An independently provisioned official Mistral deployment was preregistered for
`mistral-small-2603`. The API key is valid and the version-pinned model is visible,
but all bounded preflight completions were rejected before inference. A direct
diagnostic response reported a workspace limit of zero completion requests per
minute. No eligibility or attack episode was started. Resume only after the
Mistral workspace has a positive completion rate limit, then repeat the same
four-call preflight before the frozen six-question control screen.

The Mistral workspace was subsequently activated for pay-as-you-go use. Its
four-call preflight and six-question eligibility screen passed; the latter had
4/6 correct terminal majorities, mean agent accuracy 0.6875, and zero audit
failures. The complete fresh 48-episode power screen also passed: 1/3,456 parse
failures (0.029%), 5/768 message-call failures (0.651%), and zero invalid honest
credentials. The two publication-eligible deployments are now Qwen 3.5 9B on
DeepInfra and Mistral Small 4 on the official Mistral API.

The combined descriptive screen is heterogeneous. Qwen's incorrect-majority
rates for control/no-defense/downgrade/drop were 0.083/0.250/0.083/0.083;
Mistral's were 0.333/0.333/0.333/0.333. The confirmatory design therefore uses
the preregistered maximum of ten repetitions rather than extrapolating a positive
Mistral effect. The frozen two-deployment matrix has 200 jobs, 3,600 episodes,
and 316,800 estimated calls. It has not been started.

The first validly launched confirmatory tranche, Qwen seed 0, completed all ten
cells and 180 episode files but failed the frozen quality gate catastrophically:
7,284/12,960 raw-spin parse failures (56.20%) and 1,739/2,880 unique sender
message-call failures (60.38%), with zero invalid credentials. DeepInfra showed
repeated multi-minute and one approximately 48-minute response stall during the
block. The entire seed-0 block is excluded from confirmatory inference, no
treatment contrast is inspected, and further confirmatory collection is paused.
Qwen seed 1 and every Mistral confirmatory block remain unstarted.

The replacement DeepInfra-direct route was then evaluated prospectively and
outside the confirmatory dataset. Authentication and the pinned direct model
identifier `Qwen/Qwen3.5-9B` were valid. A 20-call infrastructure probe using
four workers, a 0.5-second start interval, a 60-second request timeout, and zero
retries produced only 6/20 nonempty completions; 8 calls timed out and 6 used
their output allowance without returning content. After adding DeepInfra's
documented `reasoning_effort=none`, a second four-worker probe failed 10/10,
with every call ending around the 60-second timeout. A final single-request
diagnostic under the same no-reasoning setting succeeded in about two seconds.
This isolates concurrency/capacity as the active failure mode rather than the
API key, endpoint, or model identifier. No eligibility or experimental episode
was started. The four-worker Qwen route remains frozen; any proposed one-worker
replacement must be documented prospectively and pass a fresh infrastructure
probe, six-question eligibility screen, and 48-episode training-data stability
screen before confirmatory collection can resume.

DeepInfra's documented priority tier was then tested as a prospective capacity
remedy. A 10-call four-worker probe passed 10/10, followed by an independent
20-call gate that passed 20/20 with median latency 1.924 seconds and maximum
latency 2.658 seconds. The replacement candidate is therefore DeepInfra direct
priority with four workers, a 0.5-second request-start interval, zero retries,
a 60-second timeout, and reasoning disabled. This route is frozen in
`res_attack/DEEPINFRA_DIRECT_PRIORITY_AMENDMENT.md` before any replacement
eligibility or experiment outcome. It must still pass the six-question control
screen and fresh 48-episode training-data screen before confirmatory use.

The sustained six-question eligibility attempt then failed infrastructure
qualification. One early request group stalled roughly 3 minutes 44 seconds,
and two later request groups stalled about 15 minutes each despite the nominal
60-second SDK timeout. The run was interrupted after one of two interaction
steps and its remaining process was explicitly terminated. Only `manifest.json`
was written; no episode outcome exists or was inspected. DeepInfra direct
priority is therefore not authorized for the 48-episode screen or confirmatory
collection. Details are recorded in
`res_attack/DEEPINFRA_DIRECT_PRIORITY_QUALIFICATION_FAILURE.md`.

An official Alibaba Cloud Model Studio deployment was subsequently provisioned
prospectively for `qwen3.5-27b` in Singapore using a workspace-dedicated
endpoint. Authentication succeeded, and an independent four-worker 20-call
infrastructure probe passed 20/20 with median latency 1.491 seconds and maximum
latency 4.993 seconds. Because this replaces both the model checkpoint and the
deployment path, it is frozen as a new candidate in
`res_attack/QWEN_OFFICIAL_27B_REPLACEMENT_AMENDMENT.md` before any eligibility
or paper outcome. It must pass the six-question control screen and fresh
48-episode training-data screen before confirmatory use.

The official Qwen3.5-27B six-question control eligibility screen then passed:
6/6 episodes completed, 5/6 terminal majorities were correct, mean final agent
accuracy was 0.8333, raw-spin parse failures were 0/432, unique sender
message-call failures were 0/96, and invalid honest credentials were zero. The
deployment is authorized for a fresh 48-episode training-data stability/power
screen under the same route, but confirmatory collection remains unauthorized.

The first official-Qwen power-screen seed-0 tranche completed 4/4 cells and
24/24 episodes but failed the frozen raw-spin quality limit: 77/1,728 samples
were zero (4.456%), while message-call failures were 0/384 and invalid honest
credentials were zero. All zeros occurred in the initial pre-message phase of
one cell and clustered by question. Because the legacy collector collapsed
parse exhaustion and request exceptions into the same zero without diagnostic
metadata, the cause is not identifiable and the tranche is excluded in full.
Seed 1 was not started. An observability-only amendment now records parse
failures, recovered parse retries, and request errors separately without
changing any scientific parameter. The failed files remain in the audit trail;
the same frozen seed-0 matrix must pass in a fresh output directory before seed
1 or confirmatory collection is authorized. See
`res_attack/QWEN_OFFICIAL_27B_POWER_SEED0_QUALITY_FAILURE.md`.

The fresh observability-amended seed-0 rerun then passed cleanly: 4/4 cells,
24/24 episodes, 0/1,728 raw zero spins, zero exhausted parse failures, zero
spin request errors, zero recovered parse retries, 0/384 unique sender message
failures, and zero invalid honest credentials. The legacy tranche remains
excluded and separate. Seed 1 of the unchanged power/stability screen is now
authorized. See
`res_attack/QWEN_OFFICIAL_27B_POWER_SEED0_RERUN_QUALITY_GATE.md`.

Seed 1 also completed cleanly. The accepted official-Qwen 48-episode screen has
0/3,456 raw zero spins, zero parse failures, zero spin request errors, zero
recovered parse retries, 0/768 unique sender message failures, and zero invalid
honest credentials. Official Qwen3.5-27B is therefore confirmatory-eligible.
Its training-data incorrect-majority rate was 2/12 in every condition; these
descriptive values are not confirmatory evidence.

A new official-two-deployment confirmatory design is frozen prospectively for
official Qwen3.5-27B and official Mistral Small 4. It retains ten seeds, ten
cells, and 18 test questions per deployment: 200 jobs, 3,600 episodes, and
316,800 estimated calls. The retired Qwen3.5-9B/DeepInfra matrix must not be
resumed. No new confirmatory job has been launched. See
`res_attack/OFFICIAL_TWO_DEPLOYMENT_CONFIRMATORY_AMENDMENT.md`.

Official Qwen confirmatory seed 0 subsequently completed all ten frozen cells
and all 180 expected episodes. Its raw-zero rate passed at 9/12,960 (0.069%):
all nine were classified as spin request errors, with zero exhausted parse
failures. Invalid honest credentials were also zero. The block nevertheless
failed the frozen message-call gate: 37/2,880 unique sender calls failed
(1.285%), exceeding the at-most-1% ceiling. All 37 were concentrated in the
`attack1_downgrade` cell (36 connection errors and one timeout); the other nine
cells had none. The entire block is excluded, no treatment contrast is
interpreted, and Qwen seed 1 plus all Mistral confirmatory blocks remain
unstarted. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED0_QUALITY_GATE.md`.

A prospective recollection amendment was then frozen before any replacement
request. It preserves every scientific and runtime setting, first requires a
20/20 connectivity probe under the same four-worker route, and—only after a
pass—recollects all ten seed-0 cells in a fresh output root. No episode from the
excluded block may be reused. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED0_RECOLLECTION_AMENDMENT.md`.

The external-network recollection preflight passed 20/20 calls with median
latency 1.972 seconds, maximum latency 2.035 seconds, and zero failures. The
complete fresh seed-0 replacement block is authorized; Qwen seed 1 and all
Mistral blocks remain unauthorized until it completes and passes.

The complete replacement block then passed every frozen quality gate: 10/10
cells, 180/180 episodes, 0/12,960 raw zero spins, zero exhausted parse
failures, zero spin request errors, zero recovered parse retries, 0/2,880
unique sender message-call failures, and zero invalid honest credentials. It is
admitted as the official-Qwen confirmatory seed-0 block. The excluded first
attempt remains separate and unchanged. Qwen seed 1 and all Mistral blocks have
not been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED0_RECOLLECTION_QUALITY_GATE.md`.

Before Mistral confirmatory seed 0, the official deployment passed a fresh
four-call health check (4/4 exact `READY` responses; latency 0.458--1.054
seconds). The complete balanced Mistral seed-0 block is authorized under the
original frozen matrix. No Qwen seed-1 block is authorized concurrently.

Mistral confirmatory seed 0 then completed all ten cells and all 180 episodes.
It passed every frozen technical gate: 2/12,960 raw zero spins (0.015%), both
classified as request errors; zero exhausted parse failures; zero recovered
parse retries; 2/2,880 unique sender message-call failures (0.069%); and zero
invalid honest credentials. The block is admitted as official-Mistral
confirmatory seed 0. No treatment contrast was interpreted, and no seed-1
block has been started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED0_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 1, the matching four-worker 20-call
health check passed 20/20 with median latency 1.986 seconds, maximum latency
2.081 seconds, and zero failures. The complete balanced Qwen seed-1 block is
authorized under the original frozen matrix; Mistral seed 1 is not authorized
concurrently.

Official-Qwen confirmatory seed 2 then completed all ten cells and all 180
episodes with a completely clean technical audit: 0/12,960 raw zero spins,
zero exhausted parse failures, zero spin request errors, zero recovered parse
retries, 0/2,880 unique sender message-call failures, and zero invalid honest
credentials. The block is admitted as official-Qwen confirmatory seed 2. No
treatment contrast was interpreted, and no Qwen seed-3 or Mistral seed-2 block
has been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED2_QUALITY_GATE.md`.

Official-Qwen confirmatory seed 1 then completed all ten cells and all 180
episodes with a completely clean technical audit: 0/12,960 raw zero spins,
zero exhausted parse failures, zero spin request errors, zero recovered parse
retries, 0/2,880 unique sender message-call failures, and zero invalid honest
credentials. The block is admitted as official-Qwen confirmatory seed 1. No
treatment contrast was interpreted, and no Qwen seed-2 or Mistral seed-1 block
has been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED1_QUALITY_GATE.md`.

Before official-Mistral confirmatory seed 1, a fresh four-call health check
passed 4/4 exact `READY` responses with latency 0.584--1.175 seconds. The
complete balanced Mistral seed-1 block is authorized under the frozen matrix;
Qwen seed 2 is not authorized concurrently.

Official-Mistral confirmatory seed 1 completed all ten cells and all 180
episodes but failed the frozen raw-zero quality gate: 267/12,960 raw spins were
zero (2.060%), above the at-most-1% limit. All were classified as request
errors—249 connection errors and 18 timeouts—with zero exhausted parse
failures. Unique sender message-call failures were 14/2,880 (0.486%), and
invalid honest credentials were zero. The entire block is excluded, no
treatment contrast is interpreted, and no later block has been started. Any
replacement must be a prospectively documented full-block recollection. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED1_QUALITY_GATE.md`.

A prospective full-block recollection amendment was frozen on 2026-10-31
before any replacement request. It preserves every scientific and runtime
setting, first requires a matching four-worker 20/20 connectivity probe, and
then—only after a pass—recollects all ten Mistral seed-1 cells in a fresh root.
No episode from the excluded block may be reused. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED1_RECOLLECTION_AMENDMENT.md`.

The matching external-network Mistral recollection preflight passed 20/20 calls
with median latency 3.113 seconds, maximum latency 3.484 seconds, and zero
failures. The complete fresh Mistral seed-1 replacement block is authorized;
Mistral seed 2 and Qwen seed 2 remain unstarted.

The complete replacement then passed every frozen quality gate: 10/10 cells,
180/180 episodes, 4/12,960 raw zero spins (0.031%), all classified as
connection-request errors; zero exhausted parse failures; zero recovered parse
retries; 0/2,880 unique sender message-call failures; and zero invalid honest
credentials. It is admitted as official-Mistral confirmatory seed 1. The first
failed attempt remains separate and excluded. No seed-2 block has been started.
See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED1_RECOLLECTION_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 2, the matching four-worker 20-call
health check passed 20/20 with median latency 1.896 seconds, maximum latency
5.153 seconds, and zero failures. The complete balanced Qwen seed-2 block is
authorized under the frozen matrix; Mistral seed 2 is not authorized
concurrently.

Before official-Mistral confirmatory seed 2, the matching four-worker 20-call
health check passed 20/20 with median latency 3.123 seconds, maximum latency
3.628 seconds, and zero failures. The complete balanced Mistral seed-2 block
is authorized under the frozen matrix; Qwen seed 3 is not authorized
concurrently.

Official-Mistral confirmatory seed 2 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 1/12,960 raw zero spins
(0.008%), classified as one connection-request error; zero exhausted parse
failures; zero recovered parse retries; 0/2,880 unique sender message-call
failures; and zero invalid honest credentials. The block is admitted as
official-Mistral confirmatory seed 2. No treatment contrast was interpreted,
and no Mistral seed 3 or Qwen seed 3 block has been started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED2_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 3, the matching four-worker 20-call
health check passed 20/20 with median latency 3.148 seconds, maximum latency
6.177 seconds, and zero failures. The complete balanced Qwen seed-3 block is
authorized under the frozen matrix; Mistral seed 3 is not authorized
concurrently.

Official-Qwen confirmatory seed 3 then completed all ten cells and all 180
episodes with a completely clean technical audit: 0/12,960 raw zero spins,
zero exhausted parse failures, zero spin request errors, zero recovered parse
retries, 0/2,880 unique sender message-call failures, and zero invalid honest
credentials. The block is admitted as official-Qwen confirmatory seed 3. No
treatment contrast was interpreted, and no Qwen seed 4 or Mistral seed 3 block
has been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED3_QUALITY_GATE.md`.

Before official-Mistral confirmatory seed 3, the matching four-worker 20-call
health check passed 20/20 with median latency 3.195 seconds, maximum latency
4.103 seconds, and zero failures. The complete balanced Mistral seed-3 block
is authorized under the frozen matrix; Qwen seed 4 is not authorized
concurrently.

Official-Mistral confirmatory seed 3 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 33/12,960 raw zero spins
(0.255%), all classified as HTTP 503 high-load request errors; zero exhausted
parse failures; zero recovered parse retries; 12/2,880 unique sender
message-call failures (0.417%); and zero invalid honest credentials. The block
is admitted as official-Mistral confirmatory seed 3. No treatment contrast was
interpreted, and no Mistral seed 4 or Qwen seed 4 block has been started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED3_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 4, the matching four-worker 20-call
health check passed 20/20 with median latency 3.184 seconds, maximum latency
3.230 seconds, and zero failures. The complete balanced Qwen seed-4 block is
authorized under the frozen matrix; Mistral seed 4 is not authorized
concurrently.

Official-Qwen confirmatory seed 4 completed all ten cells and all 180 episodes
but failed the frozen raw-zero quality gate: 320/12,960 raw spins were zero
(2.469%), above the at-most-1% limit. All were classified as request errors—
318 connection errors and 2 timeouts—with zero exhausted parse failures.
Unique sender message-call failures were 4/2,880 (0.139%), and invalid honest
credentials were zero. The entire block is excluded, no treatment contrast is
interpreted, and no later block has been started. Any replacement must be a
prospectively documented full-block recollection in a fresh output root. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED4_QUALITY_GATE.md`.

A prospective full-block recollection amendment was frozen on 2026-11-02
before any replacement request. It preserves every scientific and runtime
setting, first requires a matching four-worker 20/20 connectivity probe, and
then—only after a pass—recollects all ten Qwen seed-4 cells in the fresh root
`data/attack_confirmatory_official_two_deployment_qwen_seed4_recollection1`.
No episode from the excluded block may be reused. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED4_RECOLLECTION_AMENDMENT.md`.

The authorized external-network Qwen recollection preflight passed 20/20 calls
with median latency 3.111 seconds, maximum latency 3.502 seconds, and zero
failures. The complete fresh Qwen seed-4 replacement block is authorized;
Qwen seed 5 and Mistral seed 4 remain unstarted.

The complete Qwen seed-4 replacement then passed every frozen quality gate:
10/10 cells, 180/180 episodes, 0/12,960 raw zero spins, zero exhausted parse
failures, zero spin request errors, zero recovered parse retries, 0/2,880
unique sender message-call failures, and zero invalid honest credentials. It
is admitted as official-Qwen confirmatory seed 4. The first failed attempt
remains separate and excluded. No seed-5 Qwen or seed-4 Mistral block has been
started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED4_RECOLLECTION_QUALITY_GATE.md`.

Before official-Mistral confirmatory seed 4, the matching four-worker 20-call
health check passed 20/20 with median latency 3.095 seconds, maximum latency
7.107 seconds, and zero failures. The complete balanced Mistral seed-4 block
is authorized under the frozen matrix; Qwen seed 5 is not authorized
concurrently.

Official-Mistral confirmatory seed 4 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 3/12,960 raw zero spins
(0.023%), all classified as upstream disconnect/reset request errors caused by
remote connection failure; zero exhausted parse failures; zero recovered
parse retries; 0/2,880 unique sender message-call failures; and zero invalid
honest credentials. The block is admitted as official-Mistral confirmatory
seed 4. No treatment contrast was interpreted, and no Mistral seed 5 or Qwen
seed 5 block has been started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED4_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 5, the matching four-worker 20-call
health check passed 20/20 with median latency 3.149 seconds, maximum latency
4.844 seconds, and zero failures. The complete balanced Qwen seed-5 block is
authorized under the frozen matrix; Mistral seed 5 is not authorized
concurrently.

Official-Qwen confirmatory seed 5 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 4/12,960 raw zero spins
(0.031%), classified as three connection-request errors and one timeout; zero
exhausted parse failures; zero recovered parse retries; 0/2,880 unique sender
message-call failures; and zero invalid honest credentials. The block is
admitted as official-Qwen confirmatory seed 5. No treatment contrast was
interpreted, and no Qwen seed 6 or Mistral seed 5 block has been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED5_QUALITY_GATE.md`.

Before official-Mistral confirmatory seed 5, the matching four-worker 20-call
health check passed 20/20 with median latency 3.184 seconds, maximum latency
3.490 seconds, and zero failures. The complete balanced Mistral seed-5 block
is authorized under the frozen matrix; Qwen seed 6 is not authorized
concurrently.

Official-Mistral confirmatory seed 5 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 60/12,960 raw zero spins
(0.463%), all classified as request errors (44 connection errors, 15 request
timeouts, and one upstream disconnect/reset); zero exhausted parse failures;
zero recovered parse retries; 10/2,880 unique sender message-call failures
(0.347%); and zero invalid honest credentials. The block is admitted as
official-Mistral confirmatory seed 5. No treatment contrast was interpreted,
and no Mistral seed 6 or Qwen seed 6 block has been started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED5_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 6, the matching four-worker 20-call
health check passed 20/20 with median latency 3.147 seconds, maximum latency
4.384 seconds, and zero failures. The complete balanced Qwen seed-6 block is
authorized under the frozen matrix; Mistral seed 6 is not authorized
concurrently.

Official-Qwen confirmatory seed 6 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 0/12,960 raw zero spins,
zero exhausted parse failures, zero spin request errors, zero recovered parse
retries, 0/2,880 unique sender message-call failures, and zero invalid honest
credentials. The block is admitted as official-Qwen confirmatory seed 6. No
treatment contrast was interpreted, and no Qwen seed 7 or Mistral seed 6
block has been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED6_QUALITY_GATE.md`.

Before official-Mistral confirmatory seed 6, the matching four-worker 20-call
health check passed 20/20 with median latency 3.149 seconds, maximum latency
4.468 seconds, and zero failures. The complete balanced Mistral seed-6 block
is authorized under the frozen matrix; Qwen seed 7 is not authorized
concurrently.

Official-Mistral confirmatory seed 6 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 2/12,960 raw zero spins
(0.015%), classified as one connection error and one request timeout; zero
exhausted parse failures; zero recovered parse retries; 1/2,880 unique sender
message-call failures (0.035%); and zero invalid honest credentials. The block
is admitted as official-Mistral confirmatory seed 6. No treatment contrast was
interpreted, and no Mistral seed 7 or Qwen seed 7 block has been started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED6_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 7, the first four-worker 20-call health
check returned 19/20 successes and therefore did not authorize collection. A
fresh full retry then passed 20/20 with median latency 3.171 seconds, maximum
latency 3.298 seconds, and zero failures. The failed probe is retained as
infrastructure metadata and is not experiment data. The complete balanced
Qwen seed-7 block is authorized under the frozen matrix; Mistral seed 7 is not
authorized concurrently.

Official-Qwen confirmatory seed 7 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 29/12,960 raw zero spins
(0.224%), all classified as connection-request errors; zero exhausted parse
failures; zero recovered parse retries; 0/2,880 unique sender message-call
failures; and zero invalid honest credentials. The block is admitted as
official-Qwen confirmatory seed 7. No treatment contrast was interpreted, and
no Qwen seed 8 or Mistral seed 7 block has been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED7_QUALITY_GATE.md`.

Before official-Mistral confirmatory seed 7, the matching four-worker 20-call
health check passed 20/20 with median latency 3.083 seconds, maximum latency
4.544 seconds, and zero failures. The complete balanced Mistral seed-7 block
is authorized under the frozen matrix; Qwen seed 8 is not authorized
concurrently.

Official-Mistral confirmatory seed 7 completed all ten cells and all 180
episodes but failed the frozen raw-zero quality gate: 279/12,960 raw spins
were zero (2.153%), above the at-most-1% limit. All were classified as request
errors—265 connection errors, 13 upstream disconnect/reset failures, and one
HTTP 503 service-unavailable response—with zero exhausted parse failures.
Unique sender message-call failures were 17/2,880 (0.590%), and invalid honest
credentials were zero. The entire block is excluded, no treatment contrast is
interpreted, and no later block has been started. Any replacement must be a
prospectively documented full-block recollection in a fresh output root. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED7_QUALITY_GATE.md`.

A prospective full-block recollection amendment was frozen on 2026-11-04
before any replacement request. It preserves every scientific and runtime
setting, first requires a matching four-worker 20/20 connectivity probe, and
then—only after a pass—recollects all ten Mistral seed-7 cells in the fresh
root
`data/attack_confirmatory_official_two_deployment_mistral_seed7_recollection1`.
No episode from the excluded block may be reused. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED7_RECOLLECTION_AMENDMENT.md`.

The authorized external-network Mistral seed-7 recollection preflight passed
20/20 calls with median latency 3.054 seconds, maximum latency 3.909 seconds,
and zero failures. The complete fresh Mistral seed-7 replacement block is
authorized; Mistral seed 8 and Qwen seed 8 remain unstarted.

The fresh official-Mistral seed-7 recollection then completed all ten cells
and all 180 episodes. It passed every frozen technical gate: 0/12,960 raw
zero spins, zero exhausted parse failures, zero spin request errors, zero
recovered parse retries, 0/2,880 unique sender message-call failures, and zero
invalid honest credentials. This fresh block is admitted as the official
Mistral seed-7 confirmatory block; the original failed block remains excluded
in full and none of its episodes are reused. No treatment contrast was
interpreted, and Mistral seed 8 and Qwen seed 8 remain unstarted. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED7_RECOLLECTION_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 8, the matching four-worker 20-call
health check passed 20/20 with median latency 1.958 seconds, maximum latency
2.093 seconds, and zero failures. The complete balanced Qwen seed-8 block is
authorized under the frozen matrix; Mistral seed 8 is not authorized
concurrently.

Official-Qwen confirmatory seed 8 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 0/12,960 raw zero spins,
zero exhausted parse failures, zero spin request errors, zero recovered parse
retries, 0/2,880 unique sender message-call failures, and zero invalid honest
credentials. The block is admitted as official-Qwen confirmatory seed 8. No
treatment contrast was interpreted, and no Qwen seed 9 or Mistral seed 8
block has been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED8_QUALITY_GATE.md`.

Before official-Mistral confirmatory seed 8, the matching four-worker 20-call
health check passed 20/20 with median latency 3.156 seconds, maximum latency
3.378 seconds, and zero failures. The complete balanced Mistral seed-8 block
is authorized under the frozen matrix; Qwen seed 9 is not authorized
concurrently.

Official-Mistral confirmatory seed 8 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 0/12,960 raw zero spins,
zero exhausted parse failures, zero spin request errors, zero recovered parse
retries, 2/2,880 unique sender message-call failures (0.069%; one connection
error and one request timeout), and zero invalid honest credentials. The
block is admitted as official-Mistral confirmatory seed 8. No treatment
contrast was interpreted, and no Mistral seed 9 or Qwen seed 9 block has been
started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED8_QUALITY_GATE.md`.

Before official-Qwen confirmatory seed 9, the matching four-worker 20-call
health check passed 20/20 with median latency 1.778 seconds, maximum latency
15.514 seconds, and zero failures. The complete balanced Qwen seed-9 block is
authorized under the frozen matrix; Mistral seed 9 is not authorized
concurrently.

Official-Qwen confirmatory seed 9 then completed all ten cells and all 180
episodes. It passed every frozen technical gate: 1/12,960 raw zero spins
(0.008%), classified as one request timeout; zero exhausted parse failures;
zero recovered parse retries; 0/2,880 unique sender message-call failures;
and zero invalid honest credentials. The block is admitted as official-Qwen
confirmatory seed 9. No treatment contrast was interpreted, and Mistral seed
9 has not been started. See
`res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED9_QUALITY_GATE.md`.

Before official-Mistral confirmatory seed 9, the matching four-worker 20-call
health check passed 20/20 with median latency 3.040 seconds, maximum latency
3.893 seconds, and zero failures. The complete balanced Mistral seed-9 block
is authorized as the final uncollected block in the frozen confirmatory
matrix.

Official-Mistral confirmatory seed 9 completed all ten cells and all 180
episodes, but failed the frozen unique-sender message-call quality gate:
39/2,880 calls failed (1.354%), above the at-most-1% limit. These comprised
35 connection errors and four request timeouts. Raw zero spins were
55/12,960 (0.424%), within their limit, and all were classified as request
errors (41 connection errors and 14 request timeouts). There were zero
exhausted parse failures, zero recovered parse retries, and zero invalid
honest credentials. The entire block is excluded, no episode may be reused,
and no treatment contrast is interpreted. The frozen confirmatory matrix is
therefore not yet complete: its final formal block requires a prospectively
documented full-block recollection in a fresh output root. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED9_QUALITY_GATE.md`.

A prospective full-block Mistral seed-9 recollection amendment was frozen on
2026-11-06 before any replacement request. It preserves every scientific and
runtime setting, first requires a matching four-worker 20/20 connectivity
probe, and then—only after a pass—recollects all ten cells in the fresh root
`data/attack_confirmatory_official_two_deployment_mistral_seed9_recollection1`.
No episode from the excluded block may be reused. Full-matrix statistical
analysis remains blocked pending a passing replacement. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED9_RECOLLECTION_AMENDMENT.md`.

The first matching Mistral seed-9 replacement preflight on 2026-11-06 failed
0/20 calls, all classified as connection errors; a separate one-call
diagnostic returned the same class. The replacement was therefore not
started, and the fresh output root remains unused. No API credential was
displayed. A new dated 20-call infrastructure preflight is required before
the replacement can be authorized. See
`res_attack/mistral_small4_seed9_recollection_preflight.json`.

A second independently recorded Mistral seed-9 replacement preflight on
2026-11-06 again failed 0/20 calls with connection errors. Follow-up checks
showed general DNS resolution failure for both the Mistral API hostname and a
separate control API hostname. The replacement remains unstarted and its
fresh output root unused. Collection must wait until DNS/network access is
restored, then pass a new dated 20/20 preflight. See
`res_attack/mistral_small4_seed9_recollection_preflight2.json`.

With external-network access restored, the third independently recorded
Mistral seed-9 replacement preflight passed 20/20 calls on 2026-11-06, with
median latency 3.084 seconds, maximum latency 3.327 seconds, and zero
failures. The complete fresh ten-cell replacement block is authorized in
`data/attack_confirmatory_official_two_deployment_mistral_seed9_recollection1`;
the excluded original block remains untouched and none of its episodes may be
reused.

The authorized fresh official-Mistral seed-9 recollection completed all ten
cells and all 180 episodes on 2026-11-06. It passed every frozen technical
gate: 12/12,960 raw zero spins (0.093%), comprising 11 upstream connection
timeout/reset failures and one HTTP 502 origin bad-gateway response; zero
exhausted parse failures; zero recovered parse retries; 1/2,880 unique sender
message-call failures (0.035%, one HTTP 503 service-unavailable response);
and zero invalid honest credentials. The replacement is admitted as the
official Mistral seed-9 block; the original failed block remains excluded in
full and none of its episodes are reused. The frozen confirmatory matrix is
now complete at 20/20 official model-seed blocks and 3,600/3,600 accepted
episodes. No treatment contrast, full-matrix statistical analysis, or new
experiment has been started. See
`res_attack/MISTRAL_OFFICIAL_CONFIRMATORY_SEED9_RECOLLECTION_QUALITY_GATE.md`.

Formal frozen-matrix analysis completed on 2026-11-06 using only the 20
prospectively accepted model-seed blocks (3,600 episodes). The locked input
manifest records every admitted file and hash; excluded original blocks,
pilots, power screens, and legacy-provider data are absent. The preregistered
mixed-effects logistic analysis supports H1 (pooled no-defense budget-slope
OR 1.229, 95% CI 1.119–1.349, p=1.45e-05), H2 (downgrade versus none at the
mean positive budget OR 0.794, 95% CI 0.639–0.986, p=.0373), and H3 (drop
versus none OR 0.592, 95% CI 0.474–0.740, p=4.10e-06). Critical-budget point
ratios are directionally above one for both deployments, but every estimated
50% crossing is beyond the largest tested budget of four, the Mistral ratio
interval includes one, and the repository lacks model-matched couplings for
the live Qwen3.5-27B and Mistral deployments. H4 is therefore recorded as a
directional, extrapolative result rather than a precise quantitative
calibration. Question-cluster critical-budget intervals use 2,000 bootstrap
resamples with seed 20261106. MAP and variational-Bayes mixed-model fits agree
closely and report successful optimization. No new experiment or external API
request was started. See
`res_attack/confirmatory_analysis/CONFIRMATORY_ANALYSIS_REPORT.md`.

A manuscript-integration package was prepared on 2026-11-06 because no LaTeX,
DOCX, or other paper master file is present in the workspace. The English
insertion draft contains evidence-bound Methods, Results, Discussion,
Limitations, figure caption, tables, reproducibility statements, and submission
statement placeholders. A companion audit records the authoritative source
order and prevents the retired Qwen3.5-9B/DeepInfra configuration from being
mistaken for the accepted Qwen3.5-27B/Alibaba Cloud deployment. No citation was
invented and no new analysis or API request was run. See
`res_attack/confirmatory_analysis/MANUSCRIPT_CONFIRMATORY_SECTIONS.md` and
`res_attack/confirmatory_analysis/MANUSCRIPT_INTEGRATION_AUDIT.md`.
