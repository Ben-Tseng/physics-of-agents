# Counterfactual attack summary

These results use the fitted five-coupling model on released objective test episodes; they are not new LLM attack trials.

| model | strategy | defense | k_star_mean | k_star_sd | empirical_multiplier | weight_ratio_prediction | base_observed_agreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4o-mini | hub | downgrade | 5.842 | 0.274 | 3.01 | 3.133 | 0.656 |
| GPT-4o-mini | hub | none | 1.941 | 0.083 | 3.01 | 3.133 | 0.656 |
| GPT-4o-mini | random | downgrade | 5.961 | 0.27 | 2.581 | 3.133 | 0.656 |
| GPT-4o-mini | random | none | 2.31 | 0.091 | 2.581 | 3.133 | 0.656 |
| GPT-4o-mini | weak | downgrade | 7.402 | 0.241 | 2.853 | 3.133 | 0.656 |
| GPT-4o-mini | weak | none | 2.594 | 0.048 | 2.853 | 3.133 | 0.656 |
| Llama-3-8B | hub | downgrade | 13.101 | 0.234 | 1.789 | 1.859 | 0.844 |
| Llama-3-8B | hub | none | 7.325 | 0.059 | 1.789 | 1.859 | 0.844 |
| Llama-3-8B | random | downgrade | 13.878 | 0.25 | 1.851 | 1.859 | 0.844 |
| Llama-3-8B | random | none | 7.496 | 0.121 | 1.851 | 1.859 | 0.844 |
| Llama-3-8B | weak | downgrade |  |  |  | 1.859 | 0.844 |
| Llama-3-8B | weak | none |  |  |  | 1.859 | 0.844 |

`drop` produced no flips at any budget, as expected from its zero message weight. A missing finite k-star therefore means k-star is larger than the maximum tested budget, not zero.
