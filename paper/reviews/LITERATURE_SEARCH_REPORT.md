# Literature Search Report

Search date: 2026-11-06

## Search strategy

### Concepts

1. LLM-agent collectives, multi-agent debate, and collective decision-making.
2. Social influence, conformity, belief entrenchment, and opinion dynamics.
3. Adversarial agents, indirect prompt injection, and agent-security evaluation.
4. Sybil identities, authenticated delegation, verifiable credentials, and message authentication.
5. Byzantine behavior, network topology, and robust collective aggregation.

### Sources searched

ACL Anthology, PMLR, NeurIPS Proceedings, ICLR Proceedings, IJCAI Proceedings, arXiv, Springer Nature, Science Advances, USENIX, NIST CSRC, SciTePress, and DOI-indexed publisher pages. Citation chaining from the *Physics of Agents*, multi-agent-debate, agent-security, and digital-identity papers supplemented keyword search.

Representative Boolean strings were:

```text
("LLM agent" OR "language model agent") AND (collective OR debate OR consensus)
AND (adversarial OR conformity OR persuasion)

("multi-agent" AND "large language model") AND
(identity OR authentication OR credential OR delegation)

(Sybil OR "external identity") AND (agent OR distributed system)
AND (authentication OR trust)

("prompt injection" OR "malicious agent") AND
(multi-agent OR tool-integrated agent) AND (defense OR benchmark)
```

### Inclusion and exclusion criteria

- Included peer-reviewed papers and standards directly supporting the threat model, collective dynamics, adversarial influence, identity/authentication, or evaluation methodology.
- Included recent preprints only where they define the focal baseline or fill a gap not yet represented by a peer-reviewed source.
- Included seminal work older than ten years for Sybil attacks, Byzantine faults, multi-agent security, and HMAC.
- Excluded general agent-framework papers without substantive communication, security, or collective-decision relevance.
- Excluded news, blogs, vendor claims, and papers whose only connection was single-agent jailbreak behavior.

### Screening results

Search interfaces did not expose comparable global hit counts, so the reproducible unit is the captured candidate set rather than an estimated database total. Forty-six surfaced records were captured across the searches above. After deduplication and title/abstract screening, 31 records remained; 26 were retained after source-level assessment. Twenty-two of the 26 are peer-reviewed conference or journal papers, three are standards or seminal proceedings, and one is the focal arXiv preprint. Twenty-two sources were published during 2023-2026.

The search met four stopping conditions: the source-count target was exceeded; every theme has at least three sources; citation chaining closed around the focal debate/security papers; and both seminal and 2024-2026 work are represented.

## Annotated bibliography

### S01. El et al. (2026), *Physics of Agents: Statistical Mechanics Predicts Collective Behavior of AI Agents*
- **Type/verification**: arXiv preprint, arXiv:2608.16578.
- **Finding**: Interacting LLM-agent communities exhibit indifference, polarization, and consensus regimes that can be modeled with compact statistical-mechanics dynamics.
- **Use/stance/quality**: Focal antecedent and experimental substrate; supports the collective-dynamics framing but does not test authentication. **Supports; Medium** (preprint).

### S02. Guo et al. (2024), *Large Language Model Based Multi-agents: A Survey of Progress and Challenges*
- **Type/verification**: IJCAI 2024 Survey Track, DOI: 10.24963/ijcai.2024/890.
- **Finding**: Organizes LLM multi-agent systems by environment, profiling, communication, capability acquisition, and application.
- **Use/stance/quality**: Establishes the broader design space and the central role of communication structure. **Neutral; High**.

### S03. Li et al. (2023), *CAMEL: Communicative Agents for Mind Exploration of Large Scale Language Model Society*
- **Type/verification**: NeurIPS 2023, DOI: 10.52202/075280-2264.
- **Finding**: Demonstrates autonomous role-playing cooperation among communicative agents.
- **Use/stance/quality**: Background for message-mediated agent societies and role-based collaboration. **Supports; High**.

### S04. Wu et al. (2024), *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversations*
- **Type/verification**: COLM 2024 conference paper, OpenReview ID BAakY1hNKS.
- **Finding**: Provides a framework for composing conversational agents into flexible multi-agent workflows.
- **Use/stance/quality**: Shows why message trust boundaries matter in practical orchestrated systems. **Neutral; High**.

### S05. Du et al. (2024), *Improving Factuality and Reasoning in Language Models through Multiagent Debate*
- **Type/verification**: ICML 2024, PMLR 235:11733-11763.
- **Finding**: Multi-round debate can improve reasoning and factuality on several tasks.
- **Use/stance/quality**: Motivates collective reasoning while providing the cooperative baseline that adversarial studies qualify. **Supports; High**.

### S06. Liang et al. (2024), *Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate*
- **Type/verification**: EMNLP 2024, DOI: 10.18653/v1/2024.emnlp-main.992.
- **Finding**: Structured debate can reduce degeneration of thought, but outcomes depend on debate control and judge behavior.
- **Use/stance/quality**: Supports benefits of interaction and the importance of protocol design. **Supports; High**.

### S07. Zhang et al. (2024), *Exploring Collaboration Mechanisms for LLM Agents: A Social Psychology View*
- **Type/verification**: ACL 2024, DOI: 10.18653/v1/2024.acl-long.782.
- **Finding**: Agent traits and interaction patterns shape collaboration, conformity, consensus, and efficiency.
- **Use/stance/quality**: Links collective outcomes to social influence rather than independent reasoning alone. **Supports; High**.

### S08. Li et al. (2024), *Improving Multi-Agent Debate with Sparse Communication Topology*
- **Type/verification**: Findings of EMNLP 2024, DOI: 10.18653/v1/2024.findings-emnlp.427.
- **Finding**: Sparse topologies can match or exceed all-to-all debate while reducing cost.
- **Use/stance/quality**: Justifies treating graph topology as a first-class experimental component. **Supports; High**.

### S09. Wang et al. (2024), *Rethinking the Bounds of LLM Reasoning: Are Multi-Agent Discussions the Key?*
- **Type/verification**: ACL 2024, DOI: 10.18653/v1/2024.acl-long.331.
- **Finding**: Strong single-agent prompting can approach the best discussion methods, and multi-agent gains are regime-dependent.
- **Use/stance/quality**: Provides a necessary counterweight to unconditional claims about collaboration. **Opposes broad benefit claims; High**.

### S10. Chuang et al. (2024), *Simulating Opinion Dynamics with Networks of LLM-based Agents*
- **Type/verification**: Findings of NAACL 2024, DOI: 10.18653/v1/2024.findings-naacl.211.
- **Finding**: Networked agents tend toward truth-aligned consensus unless prompted biases alter update dynamics.
- **Use/stance/quality**: Connects message content and network interaction to emergent opinion trajectories. **Supports; High**.

### S11. Choi et al. (2025), *An Empirical Study of Group Conformity in Multi-Agent Systems*
- **Type/verification**: Findings of ACL 2025, DOI: 10.18653/v1/2025.findings-acl.265.
- **Finding**: Neutral agents conform to numerical majorities and can be disproportionately influenced by more capable agents.
- **Use/stance/quality**: Direct evidence that sender count can affect an agent's stance. **Supports; High**.

### S12. Ashery, Aiello, and Baronchelli (2025), *Emergent Social Conventions and Collective Bias in LLM Populations*
- **Type/verification**: *Science Advances* 11, eadu9368, DOI: 10.1126/sciadv.adu9368.
- **Finding**: LLM populations form conventions and can be shifted by committed adversarial minorities.
- **Use/stance/quality**: Supports budget/tipping-point reasoning, while using a different task and adversary model. **Supports; High**.

### S13. Zomer and De Domenico (2026), *Unraveling the Emergence of Collective Behavior in Networks of Cognitive Agents*
- **Type/verification**: *npj Artificial Intelligence* 2, 36, DOI: 10.1038/s44387-026-00091-5.
- **Finding**: Information flow and cognitive-agent interaction alter emergent dynamics relative to classical particles.
- **Use/stance/quality**: Supports explicit modeling of communication architecture and emergent behavior. **Neutral; High**.

### S14. Ko et al. (2026), *Social Dynamics as Critical Vulnerabilities that Undermine Objective Decision-Making in LLM Collectives*
- **Type/verification**: ACL 2026, DOI: 10.18653/v1/2026.acl-long.1756.
- **Finding**: Adversary count, apparent expertise, speaking dominance, and rhetoric degrade representative-agent accuracy.
- **Use/stance/quality**: Closest evidence for adversarial social pressure, but it does not authenticate relationship claims. **Supports; High**.

### S15. Oh et al. (2026), *From Belief Entrenchment to Robust Reasoning in LLM Agents*
- **Type/verification**: TACL 14:1286-1307, DOI: 10.1162/tacl.a.728.
- **Finding**: Homogeneous debate dynamics can reinforce shared errors; enforced diversity reduces entrenchment.
- **Use/stance/quality**: Frames incorrect consensus as an interaction failure, not only a base-model error. **Supports; High**.

### S16. Amayuelas et al. (2024), *MultiAgent Collaboration Attack: Investigating Adversarial Attacks in Large Language Model Collaborations via Debate*
- **Type/verification**: Findings of EMNLP 2024, DOI: 10.18653/v1/2024.findings-emnlp.407.
- **Finding**: A malicious participant can lower collaboration accuracy, with persuasive ability affecting attack success.
- **Use/stance/quality**: Closest prior adversarial-collaboration study; corrupts a participant rather than injecting uncredentialed identities. **Supports; High**.

### S17. Kraidia et al. (2026), *When Collaboration Fails: Persuasion Driven Adversarial Influence in Multi Agent Large Language Model Debate*
- **Type/verification**: *Scientific Reports* 16, 11640, DOI: 10.1038/s41598-026-42705-7.
- **Finding**: Inference-time persuasive adversaries can cause gradual false-consensus formation across debate rounds.
- **Use/stance/quality**: Supports the claim that natural-language collaboration creates a structural attack surface. **Supports; High**.

### S18. South et al. (2025), *Position: AI Agents Need Authenticated Delegation*
- **Type/verification**: ICML 2025, PMLR 267:82211-82231.
- **Finding**: Agent delegation requires authenticated, auditable authority chains and scoped permissions.
- **Use/stance/quality**: Establishes identity and authorization as architectural controls outside model reasoning. **Supports; High**.

### S19. Rodriguez Garzon et al. (2026), *AI Agents with Decentralized Identifiers and Verifiable Credentials*
- **Type/verification**: ICAART 2026, DOI: 10.5220/0014234400004052.
- **Finding**: DID-bound verifiable credentials can establish differentiated inter-agent trust; delegating security procedures to an LLM remains unreliable.
- **Use/stance/quality**: Closely motivates deterministic credential verification and relationship-bound routing. **Supports; High**.

### S20. Douceur (2002), *The Sybil Attack*
- **Type/verification**: IPTPS 2002, DOI: 10.1007/3-540-45748-8_24.
- **Finding**: Redundancy fails when one entity can present multiple identities; trusted certification is a central defense.
- **Use/stance/quality**: Supplies the classical identity-multiplication threat model. **Supports; High, seminal**.

### S21. Jung et al. (2012), *A Survey of Security Issue in Multi-Agent Systems*
- **Type/verification**: *Artificial Intelligence Review* 37:239-260, DOI: 10.1007/s10462-011-9228-8.
- **Finding**: Multi-agent security depends on access control, trust, reputation, and protected communication.
- **Use/stance/quality**: Historical basis for separating security enforcement from agent reasoning. **Neutral; High, foundational**.

### S22. NIST (2008), *The Keyed-Hash Message Authentication Code (HMAC)*
- **Type/verification**: FIPS 198-1, DOI: 10.6028/NIST.FIPS.198-1.
- **Finding**: Defines keyed-hash message authentication for source authenticity and message integrity.
- **Use/stance/quality**: Technical basis for the relationship credential used in the experiment. **Supports; High, standard**.

### S23. Castro and Liskov (1999), *Practical Byzantine Fault Tolerance*
- **Type/verification**: OSDI 1999, USENIX proceedings.
- **Finding**: Replication can tolerate arbitrary faulty behavior under explicit fault and identity assumptions.
- **Use/stance/quality**: Distinguishes authenticated participants and Byzantine robustness from uncontrolled identity creation. **Neutral; High, seminal**.

### S24. Debenedetti et al. (2024), *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*
- **Type/verification**: NeurIPS 2024 Datasets and Benchmarks Track.
- **Finding**: Tool-using agents remain vulnerable when untrusted data can inject instructions, and defenses trade security against task utility.
- **Use/stance/quality**: Situates the study within external-input security but uses tool outputs rather than peer messages. **Supports; High**.

### S25. Zhang et al. (2025), *Agent Security Bench: Formalizing and Benchmarking Attacks and Defenses in LLM-Based Agents*
- **Type/verification**: ICLR 2025 conference paper.
- **Finding**: Broad evaluation across attacks, defenses, tools, and model backbones finds substantial unresolved agent-security vulnerabilities.
- **Use/stance/quality**: Supports systematic security evaluation and joint security-utility measurement. **Supports; High**.

### S26. Zhan et al. (2024), *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents*
- **Type/verification**: arXiv:2403.02691.
- **Finding**: External content can manipulate tool-integrated agents into harmful actions across a large benchmark.
- **Use/stance/quality**: Supports the external-input threat premise but differs from identity and relationship spoofing. **Supports; Medium** (preprint).

## Literature matrix

| Source | Collective dynamics | Adversarial influence | Identity/authentication | Security evaluation | Network/protocol | Quality |
|---|---:|---:|---:|---:|---:|---|
| S01 El et al. | Main | x |  | x | Main | Medium |
| S02 Guo et al. | Main | x | x | x | Main | High |
| S03 Li et al. (CAMEL) | Main |  |  |  | x | High |
| S04 Wu et al. | x |  | x |  | Main | High |
| S05 Du et al. | Main |  |  | x | x | High |
| S06 Liang et al. | Main | x |  | x | Main | High |
| S07 Zhang et al. | Main | x |  | x | x | High |
| S08 Li et al. (topology) | Main |  |  | x | Main | High |
| S09 Wang et al. | Main |  |  | Main | x | High |
| S10 Chuang et al. | Main | x |  | x | Main | High |
| S11 Choi et al. | Main | Main |  | x | x | High |
| S12 Ashery et al. | Main | Main |  | x | x | High |
| S13 Zomer and De Domenico | Main |  |  | x | Main | High |
| S14 Ko et al. | Main | Main |  | Main | x | High |
| S15 Oh et al. | Main | Main |  | Main | x | High |
| S16 Amayuelas et al. | x | Main |  | Main | x | High |
| S17 Kraidia et al. | x | Main |  | Main | x | High |
| S18 South et al. |  | x | Main |  | Main | High |
| S19 Rodriguez Garzon et al. |  | x | Main | x | Main | High |
| S20 Douceur |  | Main | Main |  | Main | High |
| S21 Jung et al. |  | x | Main | x | Main | High |
| S22 NIST |  |  | Main |  | Main | High |
| S23 Castro and Liskov | x | Main | Main | x | Main | High |
| S24 Debenedetti et al. |  | Main | x | Main | Main | High |
| S25 Zhang et al. (ASB) |  | Main | x | Main | x | High |
| S26 Zhan et al. |  | Main |  | Main | x | Medium |

## Identified research gaps

1. Existing adversarial-collaboration studies usually corrupt an enrolled participant or optimize persuasive content. They do not isolate an attack in which an external actor multiplies unauthenticated identities and makes false relationship claims.
2. Emerging agent-identity work argues for credentials and delegation chains, but there is little controlled evidence connecting credential verification to collective decision outcomes.
3. Prompt-level defenses remain common. Few studies test deterministic receiver-side policies that retain an invalid message with reduced trust versus dropping it entirely.
4. Prior work rarely combines a frozen attack-budget design, two independent official deployments, block-level technical admission gates, and explicit separation of request, parsing, message, and credential failures.
5. Collective-dynamics work discusses thresholds and critical masses, but a model-matched quantitative link between physical coupling parameters and authentication-induced attack-budget shifts remains unestablished. The current study can test direction only.

## Recommended sources by paper section

| Section | Key sources |
|---|---|
| Introduction | S01, S02, S05, S14, S16, S18, S20 |
| Related work: collective reasoning | S03-S15 |
| Related work: adversarial collaboration | S14-S17, S24-S26 |
| Related work: identity and trust | S18-S23 |
| Methods: credentials/threat model | S20-S23 |
| Discussion | S01, S09-S20, S24-S26 |

