---
id: meth-ho2020-ddpm-training
type: method
label: DDPM Training (Simplified Objective Lsimple)
source: ho2020
section: Section 3.4, Algorithm 1
tokens: 1000
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 261
  end_line: 308
  page: "4"
---

## 精确表述

完整训练用真变分下界 $L$（→ thm-ho2020-elbo-variational-bound）可微分，但论文发现训练其**简化变体 Lsimple**（Eq. 14）对样本质量更好且更易实现：

$$L_{\text{simple}}(\theta) := \mathbb{E}_{t, x_0, \epsilon}\!\left[\|\epsilon - \epsilon_\theta(\sqrt{\bar{\alpha}_t}\,x_0 + \sqrt{1-\bar{\alpha}_t}\,\epsilon,\, t)\|^2\right]$$

其中 $t \sim \text{Uniform}\{1,\dots,T\}$。

**Algorithm 1（Training）：**
1. `repeat`
2. 采样 $x_0 \sim q(x_0)$
3. 采样 $t \sim \text{Uniform}\{1,\dots,T\}$
4. 采样 $\epsilon \sim \mathcal{N}(0,I)$
5. 对 $\|\epsilon - \epsilon_\theta(\sqrt{\bar{\alpha}_t}\,x_0 + \sqrt{1-\bar{\alpha}_t}\,\epsilon,\, t)\|^2$ 做一步梯度下降
6. `until converged`

边界情形：$t=1$ 对应 $L_0$（离散解码器，Eq. 13），$t>1$ 对应 Eq.(12) 的去加权版本。$L_T$ 不出现（前向 $\beta_t$ 固定）。

Lsimple 丢弃了 Eq.(12) 的加权项，是一个**加权变分下界**，强调不同的重建方面（→ ins-ho2020-simplified-objective-downweights）。

## 适用条件

- 采用 → meth-ho2020-epsilon-prediction。
- $t$ 均匀采样；前向过程方差固定（→ meth-ho2020-variance-schedule）。

## 直觉解释

每次迭代随机抽一个时间步 $t$、一张干净图、一份噪声，把噪声加到图上，再让网络从带噪图预测这份噪声。Lsimple 相比真下界去掉了随 $t$ 变化的权重，倾向于多关注较难的大-$t$ 去噪任务，从而提升样本质量（但牺牲一点码长）。

## 与其他知识的关系

← 简化自 → thm-ho2020-elbo-variational-bound（specializes）。
← 依赖 → meth-ho2020-epsilon-prediction。
→ 其设计理由 → ins-ho2020-simplified-objective-downweights。
→ 由 → exp-ho2020-ablation、→ exp-ho2020-cifar10-results 评估。

## 来源引用

Ho et al. 2020, Section 3.4, Eq. (14), Algorithm 1。full-text.txt lines 261-308, 193-203。
