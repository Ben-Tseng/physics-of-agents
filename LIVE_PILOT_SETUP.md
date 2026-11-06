# Live-model pilot setup

## User action required

1. Create an OpenRouter account at <https://openrouter.ai/>.
2. Add a small credit balance. Five US dollars is sufficient for the pilot.
3. Create a dedicated API key at <https://openrouter.ai/settings/keys>.
4. Give the key a spending limit of USD 2 if the dashboard offers per-key limits.
5. Keep prompt/completion logging disabled in OpenRouter privacy settings.
6. Review the OpenRouter terms/privacy policy and the Meta Llama acceptable-use
   policy. No Hugging Face, Meta download, Together AI, GPU, or model-repository
   access is required for this hosted inference route.

Do not paste the key into a paper, Git-tracked file, issue, notebook, or chat
message. Store it in the repository's ignored local `.env` file. These commands
avoid putting the key in shell history:

```bash
cd "/Users/bentseng/Downloads/美国大学申请/博士申请/博士论文写作/multi—agent/physics-of-agents"
read -s OPENROUTER_API_KEY
printf 'OPENROUTER_API_KEY=%s\n' "$OPENROUTER_API_KEY" > .env
chmod 600 .env
unset OPENROUTER_API_KEY
```

After typing the key, press Enter. The terminal intentionally displays nothing.
The pilot loader reads only `OPENROUTER_API_KEY` from this file. `.env` is
already excluded by `.gitignore`.

## Fixed pilot backends

- `qwen/qwen3.5-9b`
- `meta-llama/llama-3.1-8b-instruct`
- Provider pinned to `DeepInfra` for both models
- Provider fallbacks disabled
- Provider data collection denied in every request
- Reasoning disabled because the protocol requests snap A/B judgements

Pinning matters: allowing OpenRouter to switch providers during an experiment
would mix different serving stacks and quantizations under one model label.

## First paid run

The first run makes 88 calls: eight agents, one test question, two rounds, and
three spin samples per agent.

```bash
.venv/bin/python -m lib.datagen_attack.collect_pilot \
  --model qwen/qwen3.5-9b \
  --provider DeepInfra \
  --num-agents 8 --num-edges 28 --num-steps 2 --k 3 \
  --limit 1 --trajectories 1 --seed 0 \
  --defense none --attack-budget 0
```

Only after this control run passes should the attack conditions be launched.

## Prepared safeguards

- Every honest edge receives a valid HMAC credential bound to sender, receiver,
  relationship, replica, and round.
- External attackers cannot issue valid credentials.
- `none` trusts the claimed relationship, `downgrade` puts failed credentials
  in an explicit unverified-source section, and `drop` removes them.
- Each output records claimed relationship, verification outcome, routing
  decision, message, raw spins, seed, model, provider, and experiment settings.
- The `k=0` authenticated mock control is bit-for-bit identical to the original
  dynamics for graphs, spins, raw spins, and messages.

## Permissions and approvals

For a personal research account, the technical requirements are only outbound
HTTPS access, an OpenRouter account, a funded API key, and acceptance of the
service/model use terms. If the account or payment method belongs to a
university, obtain whatever purchasing or external-AI-vendor approval that
institution requires. The benchmark questions and synthetic personas should
not include confidential or participant data.
