# Power-screen quality-gate decision

## Eligible-model batch audit

| Model | Episodes | Spin failures | Spin failure rate | Message-call failures | Message-call failure rate | Invalid honest credentials | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Qwen 3.5 9B | 48 | 0/3,456 | 0.00% | 0/768 | 0.00% | 0 | Pass |
| Gemma 3 27B, first batch | 48 | 161/3,456 | 4.66% | 90/768 | 11.72% | 0 | Fail; exclude entire batch |
| Mistral Small 4, official API | 48 | 1/3,456 | 0.03% | 5/768 | 0.65% | 0 | Pass |

Message failures are counted once per sender call per step, not once per copied
recipient edge. The Gemma failure is not repaired by selecting individual cells:
all eight jobs are excluded. A separate single-worker clean batch must pass the
same aggregate 1% gates before its outcomes can enter power planning.

## Replacement deployment screens

| Deployment | Infrastructure result | Competence result | Disposition |
| --- | --- | --- | --- |
| Gemma 3 12B / DeepInfra | Repeated long stalls before a complete power episode | Control passed | Retired for operability |
| Gemma 3 27B / DeepInfra | Power batch failed: 4.66% spin and 11.72% message-call errors | Control passed | Exclude all effect data |
| Gemma 3 27B / Parasail | Preflight 0/4, upstream 429 | Not tested | No episodes started |
| Mistral Nemo 12B / DeepInfra | Zero parse, message-call, and credential failures | Failed: 3/6 majorities, mean accuracy 0.500 | No attack cells |
| Llama 3.3 70B / DeepInfra | Six episodes complete; zero parse, message-call, and credential failures | Failed: 2/6 majorities, mean accuracy 0.292 | No attack cells; candidate search stopped |
| Mistral Small 4 / official Mistral API | Eligibility clean; power batch passed at 0.03% spin and 0.65% message-call failures | Passed: 4/6 majorities, mean accuracy 0.688 | Confirmatory-eligible deployment |

Qwen 3.5 9B / DeepInfra and Mistral Small 4 / official Mistral API pass the
prospective infrastructure, competence, and full-batch quality gates. Both fresh
48-episode matrices may therefore inform repetition-count planning. They remain
excluded from confirmatory inference. Because the two deployments use different
serving stacks, the confirmatory claim is framed as cross-deployment replication,
not an isolated model-family effect.
