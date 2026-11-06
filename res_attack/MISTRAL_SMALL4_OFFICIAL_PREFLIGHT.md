# Mistral Small 4 official-API preflight

Date: 2026-10-28

The project key successfully authenticated to `GET /v1/models`: the endpoint
returned HTTP 200, listed 53 models, and included the version-pinned
`mistral-small-2603`. Four sequential eight-token connectivity requests then
returned HTTP 429 before inference. A separate diagnostic request confirmed the
same error and returned these provider headers:

- `x-ratelimit-limit-req-minute: 0`
- `x-ratelimit-remaining-req-minute: 0`

This is an account/workspace quota block, not an observed model failure and not
a concurrency issue. No eligibility episode or attack outcome was generated.
Collection remains stopped until the workspace has a positive completion request
limit. After activation, the same four-call preflight must pass before the frozen
six-question control screen runs.

After pay-as-you-go activation, the repeated preflight passed 4/4 with exact
`READY` responses in 0.577--2.355 seconds. A successful diagnostic response
reported limits of 100 requests/minute and 100,000 tokens/minute. Before the
eligibility run, request starts were therefore prospectively spaced by 0.8
seconds (at most 75/minute) with four workers, leaving headroom under both
limits based on the measured prompt sizes.
