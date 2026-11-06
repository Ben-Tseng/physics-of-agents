# Confirmatory execution plan

Status: design frozen; no valid confirmatory episode has been collected.

## Frozen scope

- Deployments: Qwen 3.5 9B on DeepInfra through OpenRouter, and version-pinned
  Mistral Small 4 (`mistral-small-2603`) on Mistral AI's official API.
- Held-out questions: 18 text-only test questions.
- Cells: one budget-zero control plus budgets 1, 2, and 4 crossed with `none`,
  `downgrade`, and `drop` defenses.
- Repetitions: ten graph/attack seeds, fixed before valid confirmatory outcomes.
- Total: 200 jobs, 3,600 episodes, and 316,800 estimated model calls.

The two serving stacks differ. Results support a cross-deployment replication
claim, not an isolated model-family causal contrast.

## Execution unit

The smallest authorized tranche is one complete model-by-seed block: all ten
cells and all 18 questions, or 180 episodes and 15,840 estimated calls. Do not
interpret or select conditions from a partial block. Start a block only when the
applicable account balance and daily key limit can cover it.

Run a block with:

```text
.venv/bin/python res_attack/run_experiment_matrix.py \
  --matrix res_attack/two_deployment_confirmatory_matrix.csv \
  --model MODEL --seed SEED
```

The runner skips a job only when its manifest and all 18 episode files exist.
Interrupted incomplete jobs are rerun in full under the same frozen command.

## Block audit

After each complete block, summarize it without inspecting treatment contrasts
for stopping decisions. Continue only when:

- raw-spin parse failures are at most 1%;
- unique sender message-call failures are at most 1%;
- invalid honest credentials equal zero; and
- all 180 episode files are present.

Pause on a failed quality gate. Do not substitute a model, provider, question,
seed, or defense and do not retain only the cleaner cells.

## Final analysis boundary

Power-screen, eligibility, feasibility, sandbox-failure, and interrupted data are
excluded from confirmatory tests. Primary analysis begins only after the frozen
matrix is complete or a preregistered infrastructure stopping rule terminates
collection. Report deployment-specific estimates before any pooled estimate.
