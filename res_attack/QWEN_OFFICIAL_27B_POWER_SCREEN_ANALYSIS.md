# Power-screen descriptive analysis

These are descriptive power-screen statistics, not confirmatory tests. Incomplete jobs are absent, and no inferential comparison is made for a model unless all predeclared cells are complete.

| Model | Condition | Episodes | Incorrect majorities | Rate (95% Wilson CI) | Mean agent accuracy |
| --- | --- | ---: | ---: | ---: | ---: |
| qwen3.5-27b | attack_downgrade | 12 | 2 | 0.167 (0.047, 0.448) | 0.833 |
| qwen3.5-27b | attack_drop | 12 | 2 | 0.167 (0.047, 0.448) | 0.812 |
| qwen3.5-27b | attack_none | 12 | 2 | 0.167 (0.047, 0.448) | 0.760 |
| qwen3.5-27b | control | 12 | 2 | 0.167 (0.047, 0.448) | 0.833 |

## Confirmatory sensitivity

The table below uses a conservative two-independent-proportion approximation at two-sided alpha 0.05 and 80% power, with worst-case variance. The mixed-effects analysis and within-question structure may change realized power; this is a transparent planning bound, not a post hoc significance claim.

| Repetitions | Questions | Episodes per cell | Approximate minimum detectable risk difference |
| ---: | ---: | ---: | ---: |
| 5 | 18 | 90 | 0.209 |
| 6 | 18 | 108 | 0.191 |
| 7 | 18 | 126 | 0.176 |
| 8 | 18 | 144 | 0.165 |
| 9 | 18 | 162 | 0.156 |
| 10 | 18 | 180 | 0.148 |

The preregistered minimum of five repetitions targets effects of roughly 0.21 or larger; ten repetitions targets roughly 0.15. Because the current screen has only six questions and two seeds, it should select between these bounds only after both model matrices are complete.
