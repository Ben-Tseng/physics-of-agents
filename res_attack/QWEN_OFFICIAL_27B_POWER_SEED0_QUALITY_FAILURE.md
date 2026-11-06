# Qwen3.5-27B Power Screen Seed-0 Quality Failure

Date: 2026-10-29

## Decision

The first official-Qwen seed-0 tranche is excluded in full and is not eligible
for treatment-effect analysis. Seed 1 was not started.

## Observed quality result

- Complete cells: 4/4
- Complete episodes: 24/24
- Zero-valued raw spin samples: 77/1,728 (4.456%)
- Unique sender message-call failures: 0/384
- Invalid honest credentials: 0

The frozen raw-spin quality limit was at most 1%, so the tranche fails even
though every episode file was written.

All 77 zero samples occurred during the initial spin phase of `attack_none`,
before any attacker message had been injected. They were concentrated by
question (24 each on three questions, four on one, and one on another), while
the other three cells had zero such samples. This pattern cannot be interpreted
as an attack effect.

## Instrumentation defect

The collection code represented both an exhausted answer-format parse and an
API/request exception as spin value zero. It did not persist the exception type
or the rejected model response. Therefore the completed files cannot establish
whether this tranche failed because of formatting or transient service errors.
The legacy summary label `raw_parse_failures` is not sufficiently specific for
these 77 samples.

Before any rerun, the collector was amended to persist per-sample diagnostics
with separate `parse_failure`, `parse_retry`, and `request_error` categories.
The scientific prompt, parser, retry count, model, temperature, concurrency,
attack, defense, questions, and all outcome definitions remain unchanged. API
credentials are redacted from diagnostic strings. Thirteen unit tests pass.

The failed files remain in the audit trail and will not be pooled with a rerun.
