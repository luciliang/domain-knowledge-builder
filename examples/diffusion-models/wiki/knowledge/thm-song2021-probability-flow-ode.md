---
id: thm-song2021-probability-flow-ode
type: theorem
label: Probability Flow ODE (Deterministic Counterpart)
source: song2021
section: Section 4.3
tokens: 1200
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1867
  end_line: 1884
  page: "Unknown"
---

## 精确表述

对所有扩散过程，存在一个对应的**确定性过程**，其轨迹共享与 SDE 相同的边际概率密度 $\{p_{t}(\mathbf{x})\}_{t=0}^{T}$。该确定性过程满足如下 ODE（Eq. 13）：

$$\mathrm{d}\mathbf{x}=\Big[\mathbf{f}(\mathbf{x},t)-\frac{1}{2}g(t)^{2}\,\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})\Big]\,\mathrm{d}t$$

论文将其命名为 **probability flow ODE**。注意它与 reverse-time SDE（Eq. 6）的区别：ODE 中 score 项系数为 $\frac{1}{2}g(t)^{2}$（而非 $g(t)^{2}$），且**无布朗运动项**（确定性）。两者的边际分布 $p_{t}(\mathbf{x})$ 完全相同。

当 score 由神经网络近似时，此 ODE 即一个 **neural ODE**（Chen et al. 2018），从而：
- 可用瞬时变量替换公式（instantaneous change of variables）计算**精确对数似然**（→ exp-song2021-cifar10-results 的 NLL 结果）；
- 编码/解码可逆，支持 latent 操控（插值、温度缩放）；
- 可用黑盒自适应 ODE 求解器在精度与效率间权衡（→ meth-song2021-pf-ode-sampling）。

## 适用条件

- score $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$ 已知或已被估计（与 reverse-time SDE 相同前提）。
- ODE 的边际密度等于 SDE 的边际密度（理论上保证；实践中受 score 估计误差影响）。

## 直觉解释

同一个 score 场既可以驱动随机轨迹（reverse-time SDE），也可以驱动确定性轨迹（probability flow ODE），二者"统计上"等价（边际分布相同）。确定性 ODE 的好处是：它是可逆的连续归一化流（neural ODE），所以能算精确似然、能编码、能用自适应步长大幅减少采样步数；代价是样本质量通常略逊于随机 SDE 求解器（除非配 corrector，见 → exp-song2021-sampler-comparison）。

## 与其他知识的关系

← 依赖 → def-song2021-score-function（score）和 → def-song2021-forward-sde（漂移/扩散系数）。
→ 驱动 → meth-song2021-pf-ode-sampling（快速采样 + 精确似然）和 → ins-song2021-uniquely-identifiable-encoding（唯一可识别编码）。
↔ 与 → thm-song2021-reverse-time-sde 共享 score，是同一生成问题的随机/确定性两种解（`compares_with`）。
→ **跨源（→ thm-ho2020-elbo-variational-bound）**：DDPM 的似然只能通过 ELBO 给出上界（$\leq$ bits/dim）；probability flow ODE 提供**精确**似然，是似然计算能力的本质提升（`extends`）。

## 来源引用

Song et al. 2021, Section 4.3, Eq. (13)；Section D.1（推导）；Chen et al. 2018 [neural ODE]。full-text.txt lines 1867-1884。
