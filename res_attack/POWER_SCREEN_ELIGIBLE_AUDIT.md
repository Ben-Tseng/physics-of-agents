# Authenticated live-model pilot

This audit contains 96 episodes from 2 model(s) across 4 model-seed group(s). API sampling is stochastic, so conditions do not share random draws. Statistical interpretation must follow the applicable preregistration rather than this descriptive table.

| Model | Condition | Seed | Final correct | Margin | Parse failures | Message errors | Attacker routes (agree/unknown/drop) | Invalid honest credentials |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| gemma-3-27b-it | attack_downgrade | 0 | 5/8 | 0.250 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 0 | 3/8 | -0.250 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 0 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 0 | 6/8 | 0.500 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 0 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 0 | 4/8 | 0.000 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 1 | 3/8 | -0.250 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 1 | 0/8 | -1.000 | 4 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 1 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 1 | 6/8 | 0.500 | 2 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 1 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_downgrade | 1 | 6/8 | 0.750 | 12 | 0 | 0/8/0 | 0 |
| gemma-3-27b-it | attack_drop | 0 | 6/8 | 0.500 | 0 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 0 | 1/8 | 0.000 | 20 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 0 | 8/8 | 1.000 | 0 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 0 | 3/8 | -0.250 | 1 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 0 | 8/8 | 1.000 | 0 | 3 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 0 | 2/8 | 0.250 | 21 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 1 | 3/8 | -0.250 | 0 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 1 | 1/8 | -0.750 | 3 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 1 | 8/8 | 1.000 | 0 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 1 | 4/8 | 0.000 | 2 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 1 | 7/8 | 0.750 | 0 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_drop | 1 | 7/8 | 0.750 | 0 | 0 | 0/0/8 | 0 |
| gemma-3-27b-it | attack_none | 0 | 4/8 | 0.000 | 0 | 0 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 0 | 0/8 | -1.000 | 0 | 0 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 0 | 8/8 | 1.000 | 0 | 0 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 0 | 4/8 | 0.000 | 0 | 0 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 0 | 6/8 | 0.500 | 0 | 0 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 0 | 4/8 | 0.000 | 0 | 0 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 1 | 3/8 | -0.250 | 4 | 1 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 1 | 0/8 | -1.000 | 5 | 1 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 1 | 8/8 | 1.000 | 6 | 1 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 1 | 3/8 | -0.250 | 3 | 0 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 1 | 4/8 | 0.000 | 0 | 3 | 8/0/0 | 0 |
| gemma-3-27b-it | attack_none | 1 | 7/8 | 0.750 | 10 | 5 | 8/0/0 | 0 |
| gemma-3-27b-it | control | 0 | 2/8 | -0.500 | 0 | 0 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 0 | 5/8 | 0.250 | 0 | 0 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 0 | 8/8 | 1.000 | 0 | 0 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 0 | 2/8 | -0.500 | 0 | 0 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 0 | 8/8 | 1.000 | 0 | 0 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 0 | 8/8 | 1.000 | 0 | 0 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 1 | 0/8 | 0.000 | 24 | 8 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 1 | 1/8 | -0.750 | 2 | 16 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 1 | 8/8 | 1.000 | 7 | 16 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 1 | 6/8 | 0.625 | 3 | 16 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 1 | 3/8 | 0.125 | 32 | 4 | 0/0/0 | 0 |
| gemma-3-27b-it | control | 1 | 6/8 | 0.500 | 0 | 16 | 0/0/0 | 0 |
| qwen3.5-9b | attack_downgrade | 0 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 0 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 0 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 0 | 6/8 | 0.500 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 0 | 5/8 | 0.250 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 0 | 5/8 | 0.250 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 1 | 7/8 | 0.750 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 1 | 5/8 | 0.250 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 1 | 5/8 | 0.250 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 1 | 2/8 | -0.500 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 1 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_downgrade | 1 | 8/8 | 1.000 | 0 | 0 | 0/8/0 | 0 |
| qwen3.5-9b | attack_drop | 0 | 8/8 | 1.000 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 0 | 1/8 | -0.750 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 0 | 8/8 | 1.000 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 0 | 7/8 | 0.750 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 0 | 8/8 | 1.000 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 0 | 7/8 | 0.750 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 1 | 7/8 | 0.750 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 1 | 7/8 | 0.750 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 1 | 7/8 | 0.750 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 1 | 6/8 | 0.500 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 1 | 7/8 | 0.750 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_drop | 1 | 5/8 | 0.250 | 0 | 0 | 0/0/8 | 0 |
| qwen3.5-9b | attack_none | 0 | 6/8 | 0.500 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 0 | 1/8 | -0.750 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 0 | 6/8 | 0.500 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 0 | 7/8 | 0.750 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 0 | 4/8 | 0.000 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 0 | 4/8 | 0.000 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 1 | 7/8 | 0.750 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 1 | 1/8 | -0.750 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 1 | 6/8 | 0.500 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 1 | 2/8 | -0.500 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 1 | 5/8 | 0.250 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | attack_none | 1 | 6/8 | 0.500 | 0 | 0 | 8/0/0 | 0 |
| qwen3.5-9b | control | 0 | 8/8 | 1.000 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 0 | 3/8 | -0.250 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 0 | 6/8 | 0.500 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 0 | 6/8 | 0.500 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 0 | 6/8 | 0.500 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 0 | 7/8 | 0.750 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 1 | 8/8 | 1.000 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 1 | 4/8 | 0.000 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 1 | 7/8 | 0.750 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 1 | 8/8 | 1.000 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 1 | 8/8 | 1.000 | 0 | 0 | 0/0/0 | 0 |
| qwen3.5-9b | control | 1 | 4/8 | 0.000 | 0 | 0 | 0/0/0 | 0 |

## Audit interpretation

- Every attacker envelope should route to `agree` under `none`, to `unknown` under `downgrade`, and to `drop` under `drop`.
- Every honest envelope should have a valid credential. Any nonzero value in the final column is an implementation or data-integrity failure.
- A zero raw spin is a parse failure after retries, not a substantive answer.
- Differences in final correctness at this sample size are descriptive only.
