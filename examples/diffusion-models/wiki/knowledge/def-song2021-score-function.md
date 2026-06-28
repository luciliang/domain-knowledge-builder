---
id: def-song2021-score-function
type: definition
label: Score Function (Time-Dependent Gradient Field)
source: song2021
section: Section 1, Section 3.3
tokens: 800
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1490
  end_line: 1544
  page: "Unknown"
---

## 精确表述

**Score function**（分数函数）定义为概率密度对数据的梯度，即对数密度的梯度：

$$\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$$

在 Score-SDE 框架中，$p_{t}(\mathbf{x})$ 是前向 SDE（→ def-song2021-forward-sde）在时间 $t$ 的边际密度，因此 score 是一个**时间依赖的梯度场**——它在每个时刻 $t$ 指向"数据密度增大"的方向。

整个框架的关键事实是：**reverse-time SDE 只依赖于 score** $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$（见 Eq. 6），而 score 可由一个时间依赖的神经网络 $\mathbf{s}_{\boldsymbol{\theta}}(\mathbf{x},t)$ 通过 score matching 估计（→ meth-song2021-score-based-training）。在足够数据和模型容量下，最优 $\mathbf{s}_{\boldsymbol{\theta}^{*}}(\mathbf{x},t)$ 几乎处处等于 $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$。

## 适用条件

- 概率密度 $p_{t}(\mathbf{x})$ 可微（对支撑集内部成立）。
- 通过 denoising score matching 估计时，需知道转移核 $p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))$（仿射漂移时为高斯）。

## 直觉解释

Score 是"去往更高数据密度方向"的指南针。在带噪图像上，score 指向"更像真实图像"的方向；沿着 score 走就能逐步去噪。Score-SDE 的洞见是：只要能估计每个时刻 $t$ 的 score，就能完全确定反向生成过程——既可走随机路径（reverse-time SDE），也可走确定性路径（probability flow ODE）。

## 与其他知识的关系

→ 是 → thm-song2021-reverse-time-sde 和 → thm-song2021-probability-flow-ode 的唯一未知量。
→ 由 → meth-song2021-score-based-training（连续去噪 score matching，Eq. 7）估计。
→ **跨源（→ thm-ho2020-score-matching-langevin-equivalence）**：DDPM 的 $\epsilon$-prediction 隐式地在每个噪声尺度计算 score（$\mathbf{s}_{\boldsymbol{\theta}^{*}}\propto -\epsilon_{\theta}/\sigma$）；Score-SDE 把 score 提升为一等公民，明确以 $\nabla_{\mathbf{x}}\log p_{t}$ 为建模对象并推广到连续时间。

## 来源引用

Song et al. 2021, Abstract, Section 1, Section 3.3, Eq. (7)。full-text.txt lines 1080-1083, 1490-1544。
