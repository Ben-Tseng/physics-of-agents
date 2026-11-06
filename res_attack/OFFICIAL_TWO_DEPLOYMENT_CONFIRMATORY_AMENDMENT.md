# Prospective Official Two-Deployment Confirmatory Amendment

Date frozen: 2026-10-29, before any outcome from this matrix.

The prior confirmatory matrix containing Qwen3.5-9B on DeepInfra is retired and
must not be resumed. Its failed seed-0 block remains excluded. The replacement
confirmatory deployments are:

- `qwen3.5-27b` through Alibaba Cloud Model Studio's official Singapore API;
- `mistral-small-2603` through the official Mistral API.

Both deployments passed separate prospective eligibility and complete fresh
48-episode training-data stability screens. Official Qwen's accepted screen
contained 0/3,456 raw zero spins, zero parse or request errors, 0/768 unique
sender message failures, and zero invalid honest credentials. Mistral's screen
contained 1/3,456 parse failures, 5/768 message failures, and zero invalid
honest credentials.

The new matrix retains the 18 frozen test questions, attack budgets 1/2/4,
defenses none/downgrade/drop, one control cell, ten seeds, eight agents, 28
edges, two interaction steps, three spin samples, temperature 0.7, and zero API
retries. Deployment-specific rate controls remain 0.5 seconds for Qwen and 0.8
seconds for Mistral, each with four workers and a 60-second request timeout.

The study is a cross-deployment replication, not a controlled provider,
parameter-count, or model-family comparison. Each balanced ten-cell model-seed
block is quality-gated as a unit: at most 1% raw zero spins, at most 1% unique
sender message failures, and zero invalid honest credentials. A failing block
is excluded in full. No confirmatory block may start unless provider balance and
spending limits cover its conservative projected cost.

The frozen design contains 200 jobs, 3,600 episodes, and 316,800 estimated model
calls. No job from this matrix has yet been launched.

## Post-freeze collection status

Official Qwen seed 0 later completed all ten cells and 180 episodes, but failed
the frozen block-level message-call quality gate: 37/2,880 unique sender calls
failed (1.285%). Raw zero spins were 9/12,960 (0.069%), comprising nine request
errors and zero exhausted parse failures, and invalid honest credentials were
zero. The entire block is excluded and no treatment contrast is interpreted.
Qwen seed 1 and all Mistral blocks remain unstarted. The auditable decision is
in `res_attack/QWEN_OFFICIAL_CONFIRMATORY_SEED0_QUALITY_GATE.md`.
