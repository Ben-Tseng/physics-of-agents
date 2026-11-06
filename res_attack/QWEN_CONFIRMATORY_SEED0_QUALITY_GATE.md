# Qwen confirmatory seed-0 quality-gate decision

Status: **FAIL — pause confirmatory collection and exclude this entire block from
confirmatory inference.**

| Audit item | Observed | Frozen gate | Decision |
| --- | ---: | ---: | --- |
| Complete episodes | 180/180 | 180/180 | Pass |
| Conditions | 10/10, 18 episodes each | 10/10 balanced | Pass |
| Raw-spin parse failures | 7,284/12,960 (56.20%) | at most 1% | Fail |
| Unique sender message-call failures | 1,739/2,880 (60.38%) | at most 1% | Fail |
| Invalid honest credentials | 0 | zero | Pass |

The block produced complete files but failed both frozen API/content quality
thresholds by a very large margin. It must not be repaired by selecting cleaner
conditions or episodes, and no treatment contrast from this block is inspected
for confirmatory inference. Qwen seed 1 and all Mistral confirmatory blocks remain
unstarted. Collection is paused pending an infrastructure audit and a prospective
decision about whether the pinned Qwen deployment can be made operational without
changing the inferential target.
