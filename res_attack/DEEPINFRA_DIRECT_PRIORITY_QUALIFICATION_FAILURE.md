# DeepInfra Direct Priority Qualification Failure

Date: 2026-10-29

Disposition: **failed infrastructure qualification; excluded from all analyses.**

The prospective six-question control-only eligibility run used the exact route
frozen in `DEEPINFRA_DIRECT_PRIORITY_AMENDMENT.md`. It did not complete. During
the initial spin phase, one request group stalled for roughly 3 minutes 44
seconds despite the declared 60-second SDK timeout. During the next spin phase,
two further stalls lasted approximately 15 minutes each. The process was
interrupted after one of two interaction steps and then explicitly terminated
to prevent further billing.

Only `manifest.json` exists in the output directory. No episode JSON file was
written, so no task outcome, treatment contrast, or eligibility result is
available or inspected.

The short 10-call and 20-call priority probes remain valid connectivity checks,
but they did not predict stability under the sustained 528-call workload. The
DeepInfra direct priority route therefore fails the prospective infrastructure
gate. No 48-episode screen or confirmatory rerun is authorized.

The immediate engineering lesson is that the OpenAI SDK timeout used by the
current threaded runner is not a strict wall-clock deadline. A future route can
only be reconsidered after implementing hard per-call isolation/cancellation
and fail-fast capacity rejection, followed by a new prospective qualification.
