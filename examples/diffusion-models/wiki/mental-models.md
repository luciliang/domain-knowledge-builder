---
title: Diffusion Models — Mental Models
domain: diffusion-models
stage: S5
method: nuwa-validation triple-check（领域化三重验证，双源跨源）
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
run_ids: [09207eda-1bc6-46b7-a8f3-779abb928d4f, 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9]
sources: [ho2020, song2021]
last_updated: 2026-06-28
mental_models: 4
decision_heuristics: 9
---

# Diffusion Models — 心智模型与决策启发式（双源）

> 本文件是 DAG 流水线 S5 的产出：把 30 个知识节点（ho2020 DDPM + song2021 Score-SDE）蒸馏成**可运行的镜片**，而非定义堆砌。
> 方法论：`engines/nuwa-validation.md` §2 三重验证——(1) 跨场景复现 ≥2 子问题/来源；(2) 有生成力（能推断对新问题的立场）；(3) 领域排他性（换领域即失效）。
> **3 重全过 = 心智模型；1–2 重 = 决策启发式；0 重 = 丢弃。**
>
> **本版（双源）相对单源版的变化**：M1/M2 的「单源未交叉验证」警示**解除**（song2021 独立确证）；新增 **M4 连续时间 SDE 统一**（单源版因无支撑节点而「未纳入」，song2021 入库后 3 重全过，升为心智模型）；M3 的率-失真分解视角仍主要来自 ho2020（song2021 确认粗→细并提供精确码长），排他性仍 ◐。

## §0 三重验证总表（双源）

| # | 候选镜片 | 跨场景 | 生成力 | 排他性 | 归类 | 双源评级变化 |
|---|----------|:------:|:------:|:------:|------|------|
| M1 | 前向即引擎：固定前向过程后，训练目标/可解析后验/采样方差/Langevin 步长/**reverse SDE/PF-ODE**全由它派生耦合 | ✓×8 | ✓ | ✓ | **心智模型** | 单源→**跨源**（song2021 把「前向 SDE 决定 reverse-SDE/PF-ODE」补上，证据更强）|
| M2 | 变分下界 ⟺ 去噪 score matching：训练即 score matching，采样即 Langevin；**score 是唯一依赖量** | ✓×7 | ✓ | ✓ | **心智模型** | 单源（NCSN 对比为 ho2020 单方面）→**跨源确证**（song2021 提升为框架级定理，caveat 解除）|
| M3 | 生成即渐进有损解码：ELBO=率(ΣL_t)+失真(L_0)，采样粗→细，过半 bit 仅精修不可感知细节 | ✓ | ✓ | ◐ | **心智模型** | 不变（率-失真分解仍主要 ho2020；song2021 确认粗→细+精确码长 2.99）|
| M4 | **连续时间 SDE 统一**：DDPM/SMLD 只是某 SDE 的离散化，生成=解 reverse-time SDE，一切统一于估计 score | ✓×3+ | ✓ | ✓ | **心智模型（新）** | **未纳入→升为 M4**（song2021 入库，3 重全过）|
| H1–H4 | ε+L_simple 协同 / 固定方差 / 感知重加权 / β 表慢且 x_T≈N | — | ✓ | ✗/◐ | 决策启发式 | 不变（ho2020）|
| H5–H8 | 选 SDE=选目标 / PC 采样器 / 精确似然走 PF-ODE / 条件 SDE 可控生成 | — | ✓ | ✗/◐ | 决策启发式（新，song2021）|
| H9 | FID/IS 与 NLL 正交评估轴 | ✓ | ✓ | ◐ | 决策启发式 | 单源→**跨源证据**（FID 3.17/ELBO≤3.75 vs 2.20/精确2.99）|
| — | 「扩散模型是潜变量模型」 | ✓ | ✗ | ✗ | **丢弃**（是定义不是镜片）| 不变 |
| — | 单网络+时间嵌入共享所有 t | ✓ | ✓ | ✗ | 实操规则（次要，未升模型）| 不变 |

---

## §1 心智模型（4 个）

### M1 — 前向即引擎（forward-as-engine）

> **一句话**：一旦固定那条前向破坏过程（离散的 β 加噪链 / 连续的前向 SDE），整台机器的其余部件——高效训练目标、可解析后验、反向采样方差、Langevin 步长、乃至 **reverse-time SDE 与 probability flow ODE**——全部由它**派生并耦合**，无需手工设定。

- **跨源证据**（≥2 来源，此处跨 ho2020 + song2021，共 8 处）：
  - **ho2020**（离散）：闭式边际 q(x_t|x_0) → 高效随机训练（`def-ho2020-forward-diffusion-process`）；可解析前向后验 → KL 目标全闭式（`def-ho2020-forward-posterior`）；β 表同时设定前向与反向 σ²（`meth-ho2020-variance-schedule`）；L_T 因 β 固定为常数可忽略（`thm-ho2020-elbo-variational-bound`）；去噪系数由 β 严格推导（`thm-ho2020-score-matching-langevin-equivalence`）。
  - **song2021**（连续）：reverse-time SDE（Anderson）由前向 SDE 的漂移/扩散 + score **完全决定**（`thm-song2021-reverse-time-sde`）；probability flow ODE 同样由前向 SDE + score 决定（`thm-song2021-probability-flow-ode`）；**前向 SDE 的选择本身就是设计旋钮**——VE-SDE 偏样本质量、VP/sub-VP 偏似然（`ins-song2021-unified-continuous-framework`、`def-song2021-ve-sde`、`def-song2021-vp-sde`）。
- **生成力**：新问题「为一种新破坏方式（模糊/运动退化）做生成」——镜片的第一反应是「先把前向过程设计成后验/转移核可解析，让它统一定义采样调度与似然计算」，而不是找现成方法。这正预测了后续广义扩散/条件化的设计路径，也预测了 song2021「自造 sub-VP SDE」的做法。
- **排他性**：VAE 学编码器、normalizing flow 双向都学、GAN 无前向破坏链。「前向固定 + 全部件由它解析派生」是扩散/score 家族特有 → ✓（双源后更清晰：连续 SDE 框架在 GAN/VAE 中无对应物）。
- **应用场景**：设计自定义前向破坏、跨模态迁移配方、解释「为何固定方差、为何不学编码器」。
- **局限**：当破坏方式的逆过程不再可解析（非高斯、非马尔可夫）时，这套「引擎」优势减弱——这恰是 DDIM（非马尔可夫）等后续工作的扩展动机。

### M2 — 变分下界 ⟺ 去噪 score matching（objective equivalence）

> **一句话**：在 ε-预测参数化下，最小化变分下界等价于做跨多个噪声尺度的去噪 score matching，采样等价于沿学习到的密度梯度走 Langevin dynamics——双源后，**score $\nabla_x\log p_t(x)$ 被确立为整个生成框架的唯一依赖量**：reverse-time SDE、PF-ODE、训练三者都只认它。

- **跨源证据**（7 处，跨 ho2020 + song2021）：
  - **ho2020**（离散、启发式）：L_{t-1} 化简为去噪 score matching（`thm-ho2020-score-matching-langevin-equivalence` Eqs.10-12）；ε 参数化是钥匙（`meth-ho2020-epsilon-prediction`）；L_simple 即去加权去噪 MSE（`meth-ho2020-ddpm-training`）；采样 ↔ Langevin（`meth-ho2020-ddpm-sampling`）；与 NCSN 的设计差异对比（Related Work / Appendix C）。
  - **song2021**（连续、框架级定理）：score 是 reverse-time SDE / PF-ODE / 训练的**唯一**依赖（`def-song2021-score-function`）；连续去噪 score matching 训练（`meth-song2021-score-based-training` Eq 7）；**离散-连续等价定理**——DDPM 目标本就是加权去噪 score matching，SMLD 与 DDPM 都只是同一连续 score matching 目标的离散化（`thm-song2021-sde-discretization-equivalence`）。
  - **跨源边**：`xsrc-equiv-scorelang`（ho2020 启发式等价 → song2021 框架级定理，extends）、`xsrc-training-eps`（ε-预测 → 连续 score matching，extends）。
- **生成力**：新问题「换连续时间 / 换噪声分布」——镜片断言目标仍化归为「该尺度下的去噪 score matching」、采样仍是密度梯度行走；新问题「改预测目标（v / x₀）」——镜片说目标 ↔ score ↔ 采样器三者绑定，改一个要同步推另两个；新问题「能否用一个量统一训练与采样」——镜片直接指向 score。
- **排他性**：VAE 的 ELBO 不是 score matching、GAN/自回归也都不是。这条等价是扩散/score 家族的标志性视角 → ✓。**单源版曾标注「与 NCSN 的对比由 ho2020 单方面刻画，待 Score-SDE 跨源验证」——song2021 已独立确证并把 NCSN(SMLD) 与 DDPM 一并纳入，caveat 解除。**
- **应用场景**：把任意似然型扩散目标翻译成 score 视角、推导新参数化的采样器、判断一个新模型是否「本质是扩散」。
- **局限**：等价性依赖「前向高斯 + ε 参数化 + 固定方差 + 小 β」一揽子前提；脱离这些前提时等价叙述需修正。

### M3 — 生成即渐进有损解码（progressive lossy decoding）

> **一句话**：扩散生成天然是一个**率-失真**过程——ELBO 拆成「率 = ΣL_t」与「失真 = L_0」；采样从粗到细显形，而**过半的码长只用来精修肉眼几乎不可察觉的细节**，所以它是优秀的有损压缩器，而非追求极致无损。

- **跨源证据**（ho2020 为主 + song2021 确认）：
  - **ho2020**：率-失真分解 + CIFAR-10 实测 rate=1.78 / distortion=1.97 bits/dim（`ins-ho2020-progressive-lossy-compression`）；渐进有损码 Algorithms 3-4（同上 Figure 5）；渐进生成粗→细（`meth-ho2020-ddpm-sampling`）；ELBO 的 L_0 vs ΣL_t 分项（`thm-ho2020-elbo-variational-bound`）；与自回归推广互为 ELBO 的两种诠释（`ins-ho2020-autoregressive-generalization`，`compares_with`）。
  - **song2021**（确认粗→细 + 提供精确码长）：reverse-time SDE 采样同样是大尺度结构先现、细节后补；PF-ODE 给出**精确**码长 2.99 bits/dim（`exp-song2021-cifar10-results`），与 ho2020 的 ELBO 上界 ≤3.75 形成跨源对照（`xsrc-cifar-cifar` compares_with）。
  - ⚠️ **诚实标注**：率-失真**分解视角**本身是 ho2020 的诠释；song2021 并未重写为率-失真，只确认了「粗→细」并给出更准的码长。故 M3 的排他性仍偏弱（见下）。
- **生成力**：新问题「采样该在第几步停 / 该用几步」——镜片说粗结构早期就定、细节在后且不可感知，故早停主要损失细节；新问题「做有损传输/渐进加载」——直接套渐进码；新问题「优化感知还是码率」——它是有损压缩器，默认押质量。
- **排他性**：◐（中等）。率-失真是通用信息论视角，但「把生成模型的目标分解成粗→细比特流、且大部分 bit 不可感知」是扩散特有的解读（自回归是左→右而非粗→细，GAN 无此分解）。
- **应用场景**：解释「为何码长不顶尖但样本极佳」、决定采样步数/早停、设计渐进传输。
- **局限**：率-失真分析以真下界 L 为准；L_simple 牺牲码长，故该镜片对 L_simple 模型的码长结论需谨慎。

> **核心张力（nuwa §3 本质性张力）——似然 vs 样本质量（双源深化）**
> - 一方：真变分下界 L → 更好码长（NLL）但 FID 较差（ho2020 `exp-ho2020-ablation`；song2021 PF-ODE 路线偏似然）。
> - 另一方：L_simple → FID 最佳但码长略差（ho2020 `exp-ho2020-cifar10-results`；song2021 VE-SDE 路线偏样本质量）。
> - **双源深化**：song2021 把这个张力**显式化为设计空间旋钮**——选哪条前向 SDE（VE vs VP/sub-VP）就是在「押样本质量」与「押似然」之间取舍（`ins-song2021-unified-continuous-framework`）。不可调和点仍在：天然 ELBO/似然加权与「人眼感知重要性」不一致，只能按评估目标取舍。
> - 这是 M3 的内在张力，不是 bug。

### M4 — 连续时间 SDE 统一（continuous-time SDE unification）【新】

> **一句话**：扩散生成的本质是「一条前向 SDE + 它的 reverse-time SDE（Anderson 1982，只依赖 score）」；DDPM、SMLD/NCSN 这些离散方法都只是某条连续 SDE（VP-SDE / VE-SDE）的离散化。一旦退到连续时间，生成、似然、可控、编码全统一在「估计 score $\nabla_x\log p_t(x)$」这一个任务下——**统一即力量**。

- **跨源证据**（song2021 为主 + ho2020 跨源确证，3+ 子设定）：
  - **song2021**（统一框架本体）：离散-连续等价定理——SMLD→VE-SDE、DDPM→VP-SDE（`thm-song2021-sde-discretization-equivalence`）；统一框架洞察（`ins-song2021-unified-continuous-framework`）；VE/VP 两条 SDE（`def-song2021-ve-sde`、`def-song2021-vp-sde`）；reverse-time SDE 是引擎（`thm-song2021-reverse-time-sde`）；PF-ODE 是第三条确定性路线（`thm-song2021-probability-flow-ode`）；conditional SDE 是第四条可控路线（`meth-song2021-conditional-sde`）。
  - **ho2020**（跨源确证被统一的离散物）：DDPM 前向链确为 VP-SDE 的离散化（`def-ho2020-forward-diffusion-process`，`xsrc-vpsde-fwd` generalizes）；ho2020 的 score-matching-Langevin 等价正是被统一的离散启发式（`thm-ho2020-score-matching-langevin-equivalence`，`xsrc-framework-scorelang` generalizes）；ε-预测即 score matching（`meth-ho2020-epsilon-prediction`，`xsrc-training-eps` extends）。
  - **跨场景复现**：该镜片在 (a) DDPM/ho2020、(b) SMLD/NCSN、(c) PF-ODE 确定性路线、(d) conditional-SDE 可控路线 四个独立子设定上一致复现 → ✓×3+。
- **生成力**（能推断对新问题的立场）：
  - 「DDIM 是 SDE 还是 ODE？」→ 镜片断言：DDIM 的确定性采样对应 **probability flow ODE**（非随机、可逆），属 ODE 路线。
  - 「想要扩散模型的精确似然」→ 镜片指向 PF-ODE（瞬时变量替换），而非 ELBO 上界。
  - 「为新数据类型设计扩散模型」→ 镜片说：选一条转移核可解析的前向 SDE，reverse-SDE/PF-ODE/score 训练随之而定。
  - 「能否用一个训好的模型做条件/无条件两种生成」→ 镜片说：能，conditional reverse-time SDE 复用无条件 score + 条件似然梯度（`meth-song2021-conditional-sde`）。
- **排他性**：✓。「连续时间 SDE，其逆过程只依赖 score」是扩散/score 家族独有——GAN 无 SDE、VAE 无 reverse-time SDE、自回归无 SDE；套到 normalizing flow（确定性可逆映射、无前向破坏 SDE）即失效 → 领域镜片成立。
- **应用场景**：把任意离散扩散方法连续化、判断「两个看似不同的生成模型是否本质同源」、决定用 SDE（随机，质量好）还是 ODE（确定性，可精确似然/可编辑）路线、统一规划可控生成。
- **局限**：等价/统一依赖「前向 SDE 漂移仿射 → 转移核高斯」；非仿射漂移时 reverse-time SDE 仍存在但不再闭式。DDIM、guidance、latent diffusion 等后续工作尚未 ingest，M4 对它们的外推属推测（见诚实边界）。

---

## §2 决策启发式（9 条）

> 从只过 1–2 重的候选降级而来。每条带触发场景与支撑节点。H1–H4、H9 来自 ho2020；H5–H8 来自 song2021（新）。

1. **ε-预测 + L_simple 必须同时启用**——ε 单独（配真下界）只与 μ̃ 预测打平；只有 ε+L_simple 协同才到 FID 3.17。*触发*：选参数化与目标时。*节点*：`exp-ho2020-ablation`、`meth-ho2020-epsilon-prediction`、`meth-ho2020-ddpm-training`。
2. **优先固定方差，不要学对角 Σ**——学习反向方差导致训练不稳、样本变差；两种固定 σ² 选择结果相近。*触发*：决定是否学习反向协方差。*节点*：`meth-ho2020-variance-schedule`、`exp-ho2020-ablation`。
3. **按「感知/任务难度」重加权，宁舍码长换质量**——L_simple 等价于降低小-t（几乎无噪、琐碎）项权重，专注大-t 难题。*触发*：评估指标是 FID 而非 NLL 时。*节点*：`ins-ho2020-simplified-objective-downweights`、`exp-ho2020-ablation`。（精神与分类里的 focal loss 同源，非扩散独有。）
4. **β 表要慢（小步长）且保证 x_T ≈ N(0,I)**——满足 L_T≈0（如 ≤10⁻⁵ bits/dim）才让先验匹配成立。*触发*：选 T 与 β schedule。*节点*：`meth-ho2020-variance-schedule`、`def-ho2020-reverse-process`。
5. **【新】选前向 SDE = 选优化目标**——VE-SDE 偏样本质量、VP/sub-VP SDE 偏似然；选哪条前向过程就是在「押质量」与「押似然」间取舍。*触发*：设计连续扩散模型、权衡 FID vs NLL 时。*节点*：`ins-song2021-unified-continuous-framework`、`def-song2021-ve-sde`、`def-song2021-vp-sde`。
6. **【新】采样用 Predictor-Corrector（PC），优于纯 predictor 或纯 corrector**——PC（数值 SDE solver + score MCMC 纠正）统一并改进 SMLD/DDPM 采样器；DDPM ancestral 只是它的 predictor-only 退化。*触发*：选反向采样器时。*节点*：`meth-song2021-pc-sampler`、`exp-song2021-sampler-comparison`、`meth-ho2020-ddpm-sampling`（`xsrc-pc-ancestral`）。
7. **【新】要精确似然走 probability flow ODE（黑盒自适应求解器），ELBO 只是上界**——PF-ODE 经瞬时变量替换给精确 NLL（CIFAR-10 2.99 bits/dim 新纪录），还附带唯一可识别编码与 latent 可编辑性。*触发*：需要似然/编码/可复现时。*节点*：`thm-song2021-probability-flow-ode`、`meth-song2021-pf-ode-sampling`、`ins-song2021-uniquely-identifiable-encoding`、`exp-song2021-cifar10-results`。
8. **【新】可控生成：训一个无条件 score 模型 + conditional reverse-time SDE，不必为每类重训**——条件采样只在 reverse-time SDE 去噪力上加一项条件似然梯度 ∇_x log p_t(y|x)。*触发*：做类条件生成/补全/着色/inverse problem 时。*节点*：`meth-song2021-conditional-sde`。
9. **FID/IS 与 NLL 是正交评估轴**（双源证据）——FID/IS 量样本质量、NLL 量码长/过拟合；二者可背离。跨源对照：ho2020 FID 3.17 / ELBO≤3.75 vs song2021 FID 2.20 / 精确 NLL 2.99 bits/dim。*触发*：评估模型、解读「质量好但码长一般」。*节点*：`exp-ho2020-cifar10-results`、`exp-song2021-cifar10-results`（`xsrc-cifar-cifar`）、`ins-ho2020-simplified-objective-downweights`。

> **保留的实操规则（次要，未升模型，过 1 重）**：放大分辨率要降学习率防训练不稳（`exp-ho2020-lsun-results`）；单网络 + 时间嵌入共享所有 t、均匀采样 t（`meth-ho2020-epsilon-prediction`）；ancestral 采样器 t=1 时 z=0 保证终态干净（`meth-ho2020-ddpm-sampling`）。它们是 ho2020 的有效工程细节，但缺乏跨场景复现与领域排他性，故不入镜片清单。

---

## §3 丢弃/降级的候选

- **「扩散模型是潜变量模型」**：只是 `def-ho2020-reverse-process` 的定义陈述，缺乏作为镜片的生成力与排他性（VAE/flow 都是潜变量模型）→ 丢弃。
- **（常识类）**：如「深度网络能拟合复杂分布」「数据缩放到 [-1,1] 利训练」「相关≠因果」——通用 ML 常识，无领域镜片价值，未纳入。
- **单源版曾有的「连续时间统一视角」条目**：单源版因 Score-SDE 未 ingest 而**无支撑节点、无法跑三重验证**，归入待补；**本次 song2021 入库后 3 重全过，已升为 M4**（见 §1）。

---

## §4 诚实边界

**本知识库做不到什么 / 未覆盖什么：**

1. **~~单源未交叉验证~~（已解除）**：双源后，M1（前向即引擎）、M2（变分⟺score）的 score/Langevin 等价、连续统一等结论**已由 ho2020 + song2021 跨源交叉验证**。**仅 M3 的率-失真分解视角仍主要由 ho2020 单方面刻画**（song2021 确认粗→细并提供精确码长，但未重写为率-失真），使用 M3 时请据此降权。
2. **~~连续时间统一缺失~~（已覆盖）**：Score-SDE（song2021）已 ingest，reverse-time SDE/ODE、probability flow ODE、PC 采样器、conditional SDE、精确似然/唯一编码**均已覆盖**（见 M4）。
3. **DDIM 未单独覆盖**：Score-SDE 的 PF-ODE 提供 ODE 视角的确定性采样，对 DDIM 有外推（见 M4 生成力），但 DDIM 具体的非马尔可夫前向族、少步采样尚未单独 ingest——M4 对 DDIM 的具体断言属推测，待 DDIM 入库后验证。
4. **条件生成与引导部分覆盖**：song2021 的 **conditional reverse-time SDE（classifier-style）已覆盖**（类条件、补全、着色）；但 **classifier guidance（Dhariwal & Nichol 2021）/ classifier-free guidance（Ho & Salimans 2022）/ 文本条件 / Stable Diffusion 仍未覆盖**。
5. **潜空间扩散缺失**：latent diffusion / Stable Diffusion（Rombach et al. 2022）未覆盖。
6. **闭式细节未提取**：各 SDE 的 reverse-time SDE 闭式、reverse diffusion sampler 离散化公式（song2021 Appendix E）、Appendix B-F 推导、NCSN++/DDPM++ 架构细节未提取。
7. **提取模式限制**：ho2020 用 text_fallback（pdftotext），部分公式排版丢失，source_span.page 为估计值；song2021 用 ar5iv HTML（663 LaTeX 公式完整保留，质量更高）。

**开放问题（领域尚无定论，不替领域拍板）：**
- 为何学习对角 Σ 会导致训练不稳？（ho2020 仅给经验现象，无理论解释）
- 最优 T 与 β schedule 的选择（论文未对 T 系统扫描）。
- 连续时间下采样步数的理论下界（song2021 的 PF-ODE 自适应采样给出实践路径，但未给紧下界）。

**来源清单与调研时间**
- 已 ingest：Ho, Jain, Abbeel. *Denoising Diffusion Probabilistic Models.* NeurIPS 2020 (arXiv:2006.11239). 提取于 2026-06-28，mode=text_fallback，run_id `09207eda-…`。
- 已 ingest：Song, Sohl-Dickstein, Kingma, Kumar, Ermon, Poole. *Score-Based Generative Modeling through Stochastic Differential Equations.* ICLR 2021 (arXiv:2011.13456). 提取于 2026-06-28，mode=ar5iv_html，run_id `9bab0aa5-…`。
- 待补：DDIM（Song et al. 2021）；classifier / classifier-free guidance；latent diffusion / Stable Diffusion。

---

## §5 质量自检清单（nuwa §5，双源版）

- [x] 每个模型有 ≥2 来源/子问题的跨源证据——M1（ho2020 5 + song2021 3）、M2（ho2020 5 + song2021 2 + 跨源边）、M4（song2021 6 + ho2020 跨源 3）；M3 主要 ho2020 + song2021 确认（已诚实标注）
- [x] 模型数量在 3–7（双源升至 **4**，宁精勿滥）
- [x] 每个模型有应用场景**与**局限边界
- [x] 模型间可并存（M1 引擎 / M2 等价 / M3 解码 / M4 统一，互为补充非互斥）；M3 内含似然-质量张力已显式标注，并经 song2021 深化为 SDE 设计旋钮
- [x] 每条启发式有具体案例 / 节点支撑（H5–H9 含跨源节点）
- [x] 启发式可被新情况触发（非仅适用原案例）
- [x] 诚实边界写了未覆盖子领域（DDIM/guidance/latent）+ M3 单源降权 + 开放问题
- [x] 标注来源清单与调研时间（双 run_id）
- [x] 换皮测试：删掉「扩散/diffusion」字样，M1（前向固定→全部件解析派生）、M2（变分⟺去噪 score matching+Langevin，score 是唯一依赖）、M3（粗→细有损解码、率-失真）、M4（连续时间 SDE 统一、reverse-time SDE 只依赖 score）仍能辨认出这是扩散/score 生成范式的思维，而非通用常识 → 领域镜片成立
