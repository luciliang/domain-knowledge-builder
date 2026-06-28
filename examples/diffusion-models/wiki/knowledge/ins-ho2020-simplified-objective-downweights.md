---
id: ins-ho2020-simplified-objective-downweights
type: insight
label: Lsimple Down-Weights Small-t Terms, Improving Sample Quality
source: ho2020
section: Section 3.4, Section 4.2
tokens: 800
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 309
  end_line: 316
  page: "4"
---

## 精确表述

作者判断：简化目标 Lsimple（→ meth-ho2020-ddpm-training）丢弃了 Eq.(12) 中随 $t$ 变化的加权项 $\frac{\beta_t^2}{2\sigma_t^2\alpha_t(1-\bar{\alpha}_t)}$，因此是一个**加权变分下界**。论文 §4 的扩散设置使 Lsimple **降低（down-weight）对应小 $t$ 的损失项**的权重。

这些小-$t$ 项训练网络去噪"噪声量极小"的数据。作者认为应降低其权重，使网络能专注于更难的大-$t$ 去噪任务。实验上，这种重加权带来更好的样本质量（FID 3.17 vs 真下界 13.51，见 → exp-ho2020-ablation）。

代价：真变分下界 $L$ 给出更好的码长（codelength），Lsimple 牺牲一点似然换取样本质量——即"扩散模型更像是优秀的**有损压缩器**而非无损压缩器"。

## 适用条件

- 评估标准是**样本质量**（FID/IS）而非 log-likelihood；若关心码长则用真下界 $L$ 更优。

## 直觉解释

小 $t$ 对应"几乎没噪"的图，去噪它很琐碎；大 $t$ 对应"几乎纯噪"，去噪它才难。Lsimple 等价于让网络少花精力在琐碎任务上、多练难题，因此生成质量更高——这是任务难度加权优于天然 ELBO 加权的经验证据。

## 与其他知识的关系

← 解释 → meth-ho2020-ddpm-training（Lsimple）的设计动机。
← 基于 → thm-ho2020-elbo-variational-bound 与 → thm-ho2020-score-matching-langevin-equivalence 的加权结构。
→ 由 → exp-ho2020-ablation 量化验证。
↔ 互补于 → ins-ho2020-progressive-lossy-compression（解释为何"码长差但样本好"）。

## 来源引用

Ho et al. 2020, Section 3.4 (最后两段), Section 4.2。full-text.txt lines 309-316, 349-363。
