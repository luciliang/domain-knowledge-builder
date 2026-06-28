---
id: meth-ho2020-ddpm-sampling
type: method
label: DDPM Ancestral Sampling
source: ho2020
section: Section 3.2, Algorithm 2
tokens: 800
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 193
  end_line: 220
  page: "3"
---

## 精确表述

从训练好的反向过程生成样本的 **ancestral sampling**（Algorithm 2）：

1. $x_T \sim \mathcal{N}(0, I)$
2. `for` $t = T, \dots, 1$:
   - 采样 $z \sim \mathcal{N}(0,I)$（若 $t=1$ 则 $z=0$）
   - $x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\,\epsilon_\theta(x_t, t)\right) + \sigma_t\, z$
3. `return` $x_0$

其中 $\sigma_t^2 = \beta_t$ 或 $\sigma_t^2 = \tilde{\beta}_t = \frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\beta_t$（两种极端选择，实验上结果相近，见 → meth-ho2020-variance-schedule）。

该过程类比于以 $\epsilon_\theta$ 为学习到的数据密度梯度的 **Langevin dynamics**（→ thm-ho2020-score-matching-langevin-equivalence）。共需 $T=1000$ 次神经网络评估。

## 适用条件

- 已训练 → meth-ho2020-epsilon-prediction 的 $\epsilon_\theta$。
- $T$ 足够大、$\beta_t$ 足够小，使反向高斯转移能近似真实反向过程。

## 直觉解释

采样就是反复执行"按预测噪声的方向退一步去噪，再加一点点随机扰动"。从纯噪声出发迭代 $T$ 步，逐步显露出大尺度结构、最后补上细节（→ ins-ho2020-autoregressive-generalization 的渐进生成）。$t=1$ 时不再加噪以保证最终是干净图。

## 与其他知识的关系

← 用 → meth-ho2020-epsilon-prediction 的网络。
← $\sigma_t$ 取自 → meth-ho2020-variance-schedule。
→ 被 → thm-ho2020-score-matching-langevin-equivalence 解释为 Langevin dynamics。
→ 支撑渐进解码 → ins-ho2020-progressive-lossy-compression、→ ins-ho2020-autoregressive-generalization。

## 来源引用

Ho et al. 2020, Section 3.2, Algorithm 2。full-text.txt lines 193-220。
