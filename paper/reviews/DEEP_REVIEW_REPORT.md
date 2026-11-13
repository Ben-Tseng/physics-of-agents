# Deep Review 报告

**稿件：** *Relationship-Credential Routing Mitigates Unauthenticated External Traffic in LLM-Agent Collectives*（`paper/MANUSCRIPT.md`，2026-11-08 版）
**审稿标准：** Workshop / arXiv 预印本
**深度：** deep。第一轮 9 个独立专项审查（统计模型、实验设计与识别、数字一致性、代码与协议、稳健性与 H4、文献与新颖性、参考文献核查、预注册审计链、威胁模型与安全论证）→ 每条发现由独立辩护方反驳 → 原审查方答辩 → 独立裁决。本报告只列出通过全部检验的发现。
**日期：** 2026-11-11

---

## Overall assessment

在声明的 threat model 内，实证核心是成立的。题内随机化（within-question permutation）稳健地表明两点：允许非成员自称 positive relationship 会提高集体错误率；把这类流量移除或单独隔离会降低错误率。问题在于论文的表述超出了证据：
- 实验实际检验的是成员资格检查加一段 prompt 警告，并没有检验 relationship-bound credential；
- H3 本质上是 manipulation check；
- pooled 的 headline OR 出自设定错误的模型；
- Qwen 的统计精度只依赖 4 道题。

按 workshop/arXiv 标准，结论是 **borderline accept：需要较大幅度的文字修订，基本不需要新实验**（置信度约 75%）。如果投安全类主会，需要补 neutral-header 和 credential-challenge 两组消融。

**没有发现 critical 问题。** 数字一致性审查从原始数据重算了正文中几乎所有数字（Table 2–5、技术失败率、Holm、GEE、LOQO、critical budgets），全部吻合。代码路由与论文描述一致，13 个测试全部通过。

---

## Critical issues

无。第一轮提出的 4 条 critical 候选（D1、D2、D7、D8）在辩护和裁决后都降为 significant：它们不改变 H1/H2 的方向，而 D7 的偏差方向是保守的。

---

## Significant concerns

### 1. 实验没有检验被命名的机制：任何对比都不需要 relationship-bound credential（D2，并入 D3）

- **Location:** 标题；Abstract 末句；§3.4（L132 "the episode-step nonce supplied within-experiment freshness"）；§5.6（"The experimental token therefore binds an edge, not just a node"；L318 "demonstrates that provenance includes when and where a statement is authorized"）；§7。代码：`lib/datagen_attack/dynamics.py`（`_message_phase`、`_route_envelopes`）、`lib/datagen_attack/credentials.py` L41–61。
- **Problem:**
  - 攻击方使用非成员 sender ID（8–11），并且 `credential=None`。所有攻击信封的验证结果都是 `missing`，诚实信封全部是 `valid`，没有出现任何其他验证结果。
  - 因此，一个不用密码学的成员资格检查（"sender 在不在 J 里？"）会产生完全相同的路由。
  - receiver binding、relation binding 和 nonce 都没有被挑战过：实验里没有冒充诚实 ID、替换关系符号、错边 token 或重放。
  - 另外，`verify(token, sender, receiver)` 并不比对当前的 `episode|step`。我们用跨 step/episode 重放的 token 实测，验证结果仍为 valid。key 是 `sha256("edge-auth-pilot|{seed}")`，可以从公开字符串推出来；nonce 也不含 seed/cell 信息，所以会在不同 cell 之间重复。
- **Why it matters:** 数据支持的结论是"不要信任非成员自称的关系"，而标题和 §5.6 把效果归功于 relationship-credential routing。§3.4 和 §5.6 关于 freshness 的两句话与实现不符。所有结果都不受影响，因为没有攻击者持有 token。
- **Suggested fix:**
  - 明确写出：在本实验中，membership gating 与 credential 检查等价。
  - 标题改为限定式，例如 "Membership-Verified / Credential-Gated Routing…"；或者把 §5.6 的 edge-binding 论证明确标为未经检验的设计理由。
  - 删除或改写 freshness 相关的两句话（或者在 `verify()` 里加上 nonce 比对）。
  - 如果有预算，加一组冒充成员 ID 或错边 token 的攻击，这样标题里的机制才有实证支持。
- **Confidence:** High。三位审查方独立复现。

### 2. H3（drop vs none）在构造上等同于对照组，却被计为第三个独立的 confirmatory 成功（D1）

- **Location:** Abstract（"drop produced a larger reduction (OR 0.592 …)"）；§1（"H1 through H3 were supported"）；§4.3；§5.4。代码：`dynamics.py` L80–94。预注册 `EXPERIMENT_PREREGISTRATION.md` L249 把 drop 称为 "an oracle-like upper bound"。
- **Problem:** drop 在构建 prompt 之前丢弃所有攻击信封，所以 drop cell 的 prompt 内容与 budget-0 control 相同，只有诚实消息的 shuffle 顺序不同。数据也印证了这一点：
  - Qwen：control 0.161，drop 0.178 / 0.167 / 0.144；
  - Mistral：control 0.211，drop 0.222 / 0.222 / 0.239；
  - 按 question × seed 配对后，drop − control 为 +0.014 / +0.008 / +0.006。
  所以 H3 在 b̄ = 7/3 处实质上是在重测 H1。
- **Why it matters:** "三个 confirmatory 假设均获支持"的说法夸大了独立证据的数量。
- **Suggested fix:** 把 H3 改称为 manipulation / positive check（证明攻击只通过被路由的通道进入、没有泄漏），报告 drop vs control 的对比，并写明 drop 的 prompt 与 control 相同。
- **Confidence:** High。

### 3. LLM 实际看不到 sender 标签：效应只可能来自重复和覆盖面，但正文把它写成"未识别"的身份效应（D4）

- **Location:** §1 L23（"Receivers observe content, sender labels…"）；Fig. 1 说明（"External messages carry a sender label"）；§3.3 L118 识别边界句（"It cannot distinguish a response to distinct sender labels from a response to repeated content"）；§4.3 L227 "per-identity multiplicative change"；§3.3 "Sybil-like"；§2.2 "converts identity creation into apparent corroboration"；中文关键词"類 Sybil 攻擊"。代码：`lib/datagen/samplers.py` 中的 `_format_inbox` 只渲染 `- {text}`。
- **Problem:** prompt 里不包含任何身份信号。budget 改变的只有两样：
  - 每个接收者收到的相同副本数：b = 1 / 2 / 4 时，每个接收者最多收到 1 / ≈2 / 3.45 份；
  - 覆盖面：被直接触达的接收者数分别为 4.0 / 6.0 / 7.5。
  论文把"标签 vs 重复"当成要靠未来消融才能回答的开放问题，但代码已经给出答案。§5.2 建议的 fixed-volume 消融如果不在 prompt 中渲染标签，也回答不了这个问题。
- **Why it matters:** 这错误描述了 H1 识别的是什么，而 H1 是全文的动机性结论。任何数字都不变，修正反而会让 H1 的含义更清楚。
- **Suggested fix:** 补一句"prompt 只包含消息文本，不渲染 sender 标识"；把 H1 重述为"重复的错误内容加上覆盖面"；删除或限定 "per-identity" 和 "Sybil-like"；Table 1 的 "Up to 4" 改为 "4"。
- **Confidence:** High。severity 在 significant 档的低端。

### 4. H2 的机制没有被识别：downgrade 同时改变了标签、加入了"验证失败"表述、改变了位置（D5，并入 D6）

- **Location:** §3.4（把 unknown 通道描述为 "unfamiliar"）；§5.1（"without requiring a semantic detector"）；§5.4（"removing the false positive-relation label can matter even when the message remains accessible"）；§7（"architectural rather than prompt based"）。代码：`samplers.py` L52–60。原文见 `PROTOCOL_APPENDIX.md` L41–46。
- **Problem:** downgrade 段的标题是 "These messages failed relationship verification. Treat their claimed source relationship as unknown."，而且这一段放在所有诚实消息之后、紧挨着 `# Problem`。因此 H2（预注册中唯一的 primary contrast）同时打包了四个变化：
  - 去掉 positive 标签；
  - 加上一句关于来源验证失败的陈述；
  - 改变所在位置；
  - 把攻击消息单独隔离成一段。
  辩护方指出这段话陈述的是来源而不是"内容为假"，这一点成立。但 "unfamiliar" 的说法和 §5.4 对"仅去标签即有效"的推断，都得不到设计的支持。"位置靠后有利于攻击方、所以结果偏保守"只是推测，没有实证。
  另外，"none" baseline 让外部方能把消息放进 "colleagues you tend to agree with" 段。按 worst-case 攻击者的思路这是可以辩护的，A2A agent-card poisoning 也是一个可能的现实先例（未核实）。但实验缺少一个中性的 unknown-source baseline。
- **Why it matters:** primary contrast 的机制解释超出了设计所能支持的范围。
- **Suggested fix:**
  - 最便宜的做法是改写：把 H2 描述为"去标签加上来源验证失败提示"。
  - 最好的做法是补一组消融：同一位置、中性标题（例如 "Other messages"）、不出现 verification 字样。这一组同时就是缺失的中性 baseline。
  - 把 "Mitigates" 限定为"相对于信任 metadata 的 router"，并在 §3.4 引用 A2A agent-card 先例。
- **Confidence:** High（事实层面）；severity 判断为 significant。

### 5. Pooled 模型让两个 deployment 共用同一个 question random intercept，headline OR 被扭曲（D7）

- **Location:** §3.6 方程；§4.3 第 2 段；Table 3 pooled 行；Table 4（prior grid、GEE、LOQO 都沿用了这一结构）；Abstract（"22.9%"、OR 1.229 / 0.794 / 0.592）；§4.5 的 "H2 is weaker evidence" 叙述。代码：`analyze_confirmatory.py` L158–161。
- **Problem:** 题目难度在两个 deployment 之间呈负相关（logit rate r ≈ −0.49）。例如 math_test_388：Mistral 0.98、Qwen 0.00；math_test_461 和 479：Qwen 1.00、Mistral 0.00。使用 question×deployment intercept（参数数量相同）后：
  - 收敛后 NLL ≤ 538，而原设定为 1481；
  - 同样先验下的 MAP 估计为 **H1 1.900、H2 0.480（p ≈ 2e-4）、H3 0.200**。
  原报告的 pooled OR 落在两个 deployment 各自 OR 的范围之外，例如 H1 为 1.229，而两个 deployment 分别是 1.63 和 3.16。在修正后的模型里，LOQO 最差情况下 H2 的 p = .005，所以"H2 较弱"在很大程度上是模型设定错误造成的。
- **Why it matters:** 方向不变，偏差也是保守的，但 headline 效应量和稳健性叙述都需要改。预注册只写了 "question random intercepts"，并没有要求两个 deployment 共用。
- **Suggested fix:** 用 question nested in deployment 重新拟合 pooled 模型，或者改为以 deployment-specific 结果为主；Table 4 也用修正后的结构重做；明确定义 pooled estimand。
- **Note:** 第一轮曾报告 deployment×treatment 交互 LRT p ≈ 1.6e-5。收敛重拟合后为 p = .17，**该结论已撤回**。
- **Confidence:** High。

### 6. Qwen 的统计精度只依赖 4 道题（D8，并入 D9、D10）

- **Location:** Table 3 的 Qwen 行（p 低至 1.26e-8）；§4.3；Abstract（"Both directions appeared in each deployment"）；§3.6（"fitted question-level SD 4.150"）；MODEL_AUDIT.md。
- **Problem:**
  - Qwen 的 18 道题里，12 道始终正确、2 道（461、479）始终错误，只有 132、21、157、426 这 4 道有信息量；Mistral 有 10 道。
  - 同时去掉 157 和 21 后，Qwen 的 H1 / H2 / H3 分别为 p = .73 / .53 / .14。
  - 按 question 聚类的 GEE 下，Qwen 的 p ≈ .11 / .12 / .09；Mistral 的 H2 也只有 p ≈ .07。
  - 各题的 budget slope 存在异质性（LRT p = .0015），而模型没有 random slope。
  - 题内随机化 permutation test 在这 18 道题的条件下仍然显著：Qwen downgrade p = .0034，drop p < 5e-5。条件推断本身是成立的，但它支持不了关于"新题目"的总体精度。
  - "fitted SD 4.150" 主要由 log-SD 先验决定：`fit_map` 最大化的是联合后验，Qwen 的 σ_q 在 marginal likelihood 下不可识别。随先验不同，Qwen H3 OR 在 0.133 到 0.029 之间变动。
  - 用拟合率与观测率之比作为审计，可以发现 fixed effect 的严重遗漏，但发现不了 random-effect 的设定错误（例如第 5 条）。
- **Why it matters:** Table 3 的 p 值和"每个 deployment 都复现"的说法，暗含了数据无法支持的推广性。
- **Suggested fix:**
  - 报告每个 deployment 中有信息量的题数；
  - 补充 permutation test 和 leave-two-out 结果；
  - 把推断明确表述为"以这 18 道题为条件"；
  - 去掉 1e-8 这类精度表述；
  - 把 "fitted SD" 改称为依赖先验的量；
  - 把 prior grid 扩展到 deployment 模型；
  - 把拟合率审计改称为 consistency check。
- **Confidence:** High。

### 7. 与预注册的偏差没有披露（D13）

- **Location:** §1（"preregistered two-deployment evaluation"）；§3.5（"frozen on 2026-10-29 before its first outcome"）；§3.6（"The analysis plan separated confirmatory and descriptive claims before results were interpreted"）；Table 3 标题 "Preregistered deployment-specific…"。证据文件：`EXPERIMENT_PREREGISTRATION.md`、`RUN_STATUS.md`、`QWEN_CONFIRMATORY_SEED0_VALID_AUDIT.md`、`OFFICIAL_TWO_DEPLOYMENT_CONFIRMATORY_AMENDMENT.md`、`paper/MAJOR_REVISION_PLAN.md`。
- **Problem:** 以下事实没有争议：
  - (a) 原预注册的模型组合是 Qwen3.5-9B 加 Llama-3.1-8B，之后筛选了约 7 个候选。在 18 道测试题上采集了一个完整的 9B confirmatory block（因技术门槛失败，逐题结果已打印出来），之后才换成 Qwen3.5-27B。而预注册的 stopping rule 写的是 "do not replace it with another model or provider"。
  - (b) 预注册中，H4 是 confirmatory claim 的成立条件；它是在 11-06 分析之后、应审稿意见才被降为 exploratory 的。因此 §3.6 那句话与事实不符。
  - (c) 预注册的 H2 是复合假设（降低攻击成功率**并且**提高 critical budget），后半部分在 Mistral 上不成立（CI 0.60–2.18）。预注册只把 downgrade vs none 定为 primary。
  - (d) 估计细节（线性 raw budget、control 编码为 none、7/3 contrast、MAP 先验）最早出现在分析代码里。
  - (e) 预注册只描述了 pooled 模型，Table 3 的 deployment-specific 拟合却标注为 "Preregistered"。
- **Why it matters:** 辩护方的论证成立：更换模型是基础设施故障所迫（9B block 的 raw zero 达 56%），27B 的 amendment 日期早于该 deployment 的任何结果，筛选只用了训练题，H4 降级对作者反而不利。所以这里没有偏倚或恶意的迹象。但一篇自称 "preregistered" 的论文必须披露这些。
- **Suggested fix:** 增加一张 deviations-from-preregistration 表，更正 §3.6 那句话，把 Table 3 的标题改为只有 pooled 是预注册的。
- **Confidence:** High。

### 8. 遗漏了直接相关的先前工作，新颖性需要收窄（D15）

- **Location:** §1 第 3 段（"Content filters and prompt-injection defenses inspect language"）；§2.3（"These methods target message content or communication patterns"）；贡献 (ii)。
- **Problem:** 以下工作都已独立核实存在，内容也与所述相符：
  - **Paul & Nandy, arXiv:2609.22949**（2026-09-19 发布）：对 inter-agent 消息做 Ed25519 签名并附 provenance，接收方验证后隔离未签名消息，inter-agent injection 成功率从 31% 降到 2.8%。是否被 workshop 接收未确认。这是本文"先验证、再 drop/quarantine"原则的直接先例。
  - **Prompt Infection [29]**（已引用）本身就测试了 "LLM Tagging" 来源标注防御，但正文只引用了它的传播结果。
  - **MAD-Spear, arXiv:2507.13038**：针对 multi-agent debate 的 conformity / Sybil 式攻击。
  - **Hu & Qu, arXiv:2607.05545**：不带说话人的单纯重复就能引发大部分 conformity。这直接支持第 3 条，并能解释 downgrade 为什么效果弱。
  - 其他：spotlighting（Hines et al., 2403.14720）、instruction hierarchy（2404.13208）、CaMeL（2503.18813）、FIDES（2505.23643）；BFT / credibility 类 LLM-MAS 工作（2511.10400、2505.24239）。
- **Why it matters:** "注入防御只检查语言"的说法已经过时，节点级签名后隔离也不再新颖。真正有区别的贡献是：edge 级关系凭证、对集体结果（incorrect majority）的剂量-反应测量、downgrade 与 drop 的对比，以及两个 deployment 的 confirmatory 协议。论文目前没有这样自我定位。
- **Suggested fix:** 引用并对比上述工作，重写 §1 第 3 段和 §2.3，并把贡献 (ii) 收窄为上述几个真正有区别的点。
- **Confidence:** High。

### 9. 实验底座来自 Physics of Agents [1]，Methods 中没有注明（D16）

- **Location:** §3.1–3.2；§2.1（"it is primarily descriptive"）。
- **Problem:** 二元数学题、带 worked solution 的 persona、带符号的图（J ∈ {−1, 0, +1}）、opinion 采样、按关系区分的 inbox，都继承自 [1]，而 [1] 只在 §2.1 和 §5.7 被引用。[1] 拟合的是可预测的 coupling 模型（标题就叫 "Predicts"），称其 "primarily descriptive" 并不准确。repo README 写明这是 fork，论文正文却没有说。
- **Suggested fix:** 在 §3.2 写明继承了哪些部分、新增了哪些部分；改写 §2.1 的措辞。还可以利用 [1] 中 β⁺ / β⁻ / β₀ 的分解来表述 H4：downgrade 相当于把外部边从 β⁺ 移到 ≈β₀。
- **Confidence:** High。容易修。

---

## Minor issues

- **D18（Abstract、§7）：** "reduced the influence … before language-model deliberation" 只对 drop 字面成立。在 downgrade 下，攻击内容仍会进入 prompt，并在 step 2 通过带有效凭证的诚实消息继续传播（`dynamics.py` L204–211）。建议改为 "applied deterministic routing before deliberation"，并说明结果已包含这种转发。
- **D12（Abstract、§4.6、§5.7、Table 5）：**
  - 单调拟合把负斜率截为 0，所以 ∞ 是构造产物。例如 Qwen drop 的非约束斜率为 −0.041，p = .55。
  - Qwen downgrade 的 48.98 基于一个不显著的斜率（p = .63）。
  - 只有 3 条曲线的斜率显著不为 0。
  - 建议：Abstract 注明 Mistral 的 multiplier CI 包含 1，或删掉这句；§5.7 删除 "informative"；Table 5 中 Qwen downgrade/drop 改报 "no detectable positive slope"，并删除 4.41 [1.78, ∞]。
- **D14（§3.5、§4.5）：** 5 个替换 block 的规则是机械执行的，没有选择性迹象。但如果改用失败的那次采集，H2 为 OR 0.843、p = .124；去掉受污染 cell 后为 p ≈ .15，看起来是抽样噪声。建议把这项敏感性分析写进 §4.5，并把 §3.5 的 "prospective" 改为"在每次失败之后、替换之前写成"。原预注册写的是 "pause and diagnose"。
- **D17（参考文献）：** 作者名错误：[11] 应为 Min Choi（原作 J.），[13] Nicola Zomer（E.），[14] Changgeon Ko（M.），[15] Jihwan Oh（C.），[17] Insaf Kraidia（A.），[19] Sandro Rodriguez Garzon（I.）；bib 中 [7]、[10]、[21] 的名字也有误。[17] 正文说它 "traces how persuasive influence accumulates across rounds"，原文摘要不支持这一点。[19] 的 "warn against" 措辞偏强。[26] 应改引 Findings ACL 2024 正式版，[7] 页码应为 14544–14607。所有文献都真实存在，DOI 基本正确。AI disclosure 写了"已核对引用"，与这些错误不符。
- **M4（`analyze_confirmatory.py` L403/L444）：** 当 none 的 critical budget = 0 时，multiplier 被赋为 ∞，而这并不是"无交点"。Qwen 有 110 次 ∞/∞ = NaN 被静默计为 +∞。报告的数字不变，但需要一句方法说明。
- **M6：** cell 按固定顺序运行（control → b1 → b2 → b4），budget 与采集时间相关。请求错误集中在后面的 cell（Mistral attack4_drop 47 次，Qwen attack4_none 29 次）。量级很小，但应在 §6 披露。
- **M9（§4.4）：** 所谓 "budget-specific" 次级对比，其实是线性交互线上的点，不是逐个 cell 的检验。categorical GEE 给出的模式不同：drop vs none 在 b = 1 时 p = .003。建议改写措辞。
- **M10：** spin prompt 要求 "Do NOT work through the problem … snap judgement"，这会让社会线索的影响最大化，与 "pool reasoning" 的框架有张力，但 §6 没有讨论。
- **M11：** `accepted_block_manifest.csv` 的 20 个 SHA-256 在快照中需要先把 LF 转成 CRLF 才能匹配。请核对 tag 版本，然后说明换行约定或重新计算哈希。
- **M14：** 每个 persona 都嵌入了一道已解出的示例题及答案，PROTOCOL_APPENDIX 只显示了 `{persona}` 占位符，应说明其内容。
- **M15（§3.2）：** 每个 agent 的状态由 3 个样本多数决定，平票时取第一个样本；undecided 时的 stance 来自未设种子的全局 `random`。这一规则应写入正文并设种子。

---

## Questions for the authors

1. 能否补跑一组 neutral-header downgrade（同一位置，不含 "verification" 字样）？这能直接区分 H2 中去标签与来源提示各自的作用。
2. 能否加一组冒充成员 ID、错边 token 或重放 token 的攻击？没有这一组，标题中 "relationship-credential" 的机制主张就没有实证支持。
3. Pooled 模型共用 question intercept 是有意的设计，还是默认写法？换成 question-within-deployment 后 H2 会明显变强，你倾向于把它作为主模型还是稳健性分析？
4. Qwen 只有 4 道有信息量的题。你是否考虑增加题量，或者改用更难的题集，以获得总体层面的推断？
5. 9B confirmatory block 的逐题结果在更换模型前就已经可见。是否有其他记录（例如 commit 时间）能证明 27B amendment 写成时没有参考这些结果？

---

## 审查过程与已验证项（供参考）

- **数字：** Table 2–5、技术失败计数（259,200 次 spin、151 个 raw zero、57,600 次消息调用、28 次失败、0 个无效凭证）、Holm、GEE、LOQO 和 critical budget 全部从 `accepted_episode_data.csv` 重算，结果吻合。
- **代码：** 路由、HMAC tuple、目标选择（跨 policy 和 deployment 完全一致、按 budget 嵌套）、同步更新、只用诚实 agent 计算结果、平票不算攻击成功，全部与描述一致。13 个测试通过。
- **已撤回的第一轮结论：**
  - deployment×treatment 交互显著（收敛后 p = .17）；
  - D11 的修正数值（0.147 / 0.026 来自未收敛的拟合；收敛值为 0.192 / 0.048，且 cell-mean 模型能复现原报告值，整条撤回）；
  - "bib 由 LLM 生成"的推测；
  - "诚实消息讨论示例题"的子论点。
- **主要局限：** 快照中只有 3 个 block 的原始 episode JSON；部分 DOI 无法直接在 doi.org 解析验证；A2A 先例的两个网页来源未能二次核实。
