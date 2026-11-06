# Counterfactual threat model

This experiment is a fitted-model counterfactual over the released objective
test episodes. It is not evidence from new LLM calls.

- The honest population, signed graph, persona/question field, truth label, and
  initial spin are taken from the released `clean_runs.json` data.
- An attacker sends the objectively false spin and claims a positive
  relationship with up to `d` honest recipients.
- Under `none`, the message receives the fitted false-friend weight
  `beta_pos_F + beta_0`.
- Under `downgrade`, failed edge authentication removes the claimed-friend
  component and leaves only `beta_0`.
- Under `drop`, failed authentication removes the message completely.
- Budget `k` counts external attacker identities. Target placements are nested:
  the targets at budget `k` are the first `k` rows of one sampled placement.
- The primary endpoint is the fraction of no-attack-successful test episodes
  whose terminal population majority becomes non-correct under attack.

The experiment tests consequences of the fitted statistical model. A later LLM
experiment must separately test whether credential routing changes actual model
responses in the same way.
