# Counterfactual attack summary

These results use the fitted five-coupling model on released objective test episodes; they are not new LLM attack trials.

| model | strategy | defense | k_star_mean | k_star_sd | empirical_multiplier | weight_ratio_prediction | base_observed_agreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemma-3n-E4B | random | downgrade | 10.687 | 0.088 | 1.232 | 1.207 | 0.901 |
| Gemma-3n-E4B | random | none | 8.674 | 0.113 | 1.232 | 1.207 | 0.901 |
| GPT-4o-mini | random | downgrade | 5.961 | 0.27 | 2.581 | 3.133 | 0.656 |
| GPT-4o-mini | random | none | 2.31 | 0.091 | 2.581 | 3.133 | 0.656 |
| Llama-3-8B | random | downgrade | 13.878 | 0.25 | 1.851 | 1.859 | 0.844 |
| Llama-3-8B | random | none | 7.496 | 0.121 | 1.851 | 1.859 | 0.844 |
| Qwen3.5-9B | random | downgrade | 8.771 | 0.105 | 1.767 | 1.767 | 0.796 |
| Qwen3.5-9B | random | none | 4.963 | 0.054 | 1.767 | 1.767 | 0.796 |

`drop` produced no flips at any budget, as expected from its zero message weight. A missing finite k-star therefore means k-star is larger than the maximum tested budget, not zero.
