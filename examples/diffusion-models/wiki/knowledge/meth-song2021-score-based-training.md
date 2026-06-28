---
id: meth-song2021-score-based-training
type: method
label: Continuous Denoising Score Matching Training
source: song2021
section: Section 3.3
tokens: 1100
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

为估计 score $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$，训练一个时间依赖的 score 模型 $\mathbf{s}_{\boldsymbol{\theta}}(\mathbf{x},t)$，用 Eq. 1（SMLD）和 Eq. 3（DDPM）的连续推广（Eq. 7）：

$$\boldsymbol{\theta}^{*}=\arg\min_{\boldsymbol{\theta}}\mathbb{E}_{t}\Big\{\lambda(t)\,\mathbb{E}_{\mathbf{x}(0)}\mathbb{E}_{\mathbf{x}(t)\mid\mathbf{x}(0)}\big[\left\lVert\mathbf{s}_{\boldsymbol{\theta}}(\mathbf{x}(t),t)-\nabla_{\mathbf{x}(t)}\log p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))\right\rVert_{2}^{2}\big]\Big\}$$

其中 $\lambda:[0,T]\to\mathbb{R}_{>0}$ 是正加权函数，$t$ 在 $[0,T]$ 上均匀采样，$\mathbf{x}(0)\sim p_{0}$，$\mathbf{x}(t)\sim p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))$。在足够数据和容量下，score matching 保证最优解 $\mathbf{s}_{\boldsymbol{\theta}^{*}}(\mathbf{x},t)$ 几乎处处等于 $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$。

典型权重取 $\lambda\propto 1/\mathbb{E}[\lVert\nabla_{\mathbf{x}(t)}\log p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))\rVert_{2}^{2}]$（与 SMLD/DDPM 一致）。Eq. 7 用 denoising score matching；也可用 sliced score matching、finite-difference score matching（无需闭式转移核）。

当 $\mathbf{f}$ 仿射时，转移核 $p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))$ 恒为高斯、闭式可知，使 Eq. 7 求解尤为高效。

## 适用条件

- 需转移核 $p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))$（仿射漂移时为高斯闭式）；否则改用 sliced score matching 绕过。
- 网络需以连续时间 $t$ 为额外输入（区别于 DDPM 的离散整数 $i$）。

## 直觉解释

把 DDPM 的 $L_{\text{simple}}$（预测噪声 ε）和 SMLD 的多尺度 score matching 统一成"在连续时间上随机抽一个 $t$，加对应噪声，让网络预测该噪声下的 score"。由于噪声扰动核是高斯，score 有闭式形式 $\nabla\log p_{0t}$，所以本质还是去噪 score matching——只是从有限噪声尺度变成了连续时间。

## 与其他知识的关系

← 估计 → def-song2021-score-function（score），为 → thm-song2021-reverse-time-sde 和 → thm-song2021-probability-flow-ode 提供所需的 score。
→ 估计出的 score 用于构造 reverse-time SDE，再由 → meth-song2021-pc-sampler 采样。
→ **跨源（→ meth-ho2020-epsilon-prediction）**：DDPM 的 ε-prediction 在 Eq. 3 写法下就是加权去噪 score matching（$\mathbf{s}_{\boldsymbol{\theta}^{*}}\propto -\epsilon_{\theta}/\sqrt{1-\alpha}$）；本方法把离散的 $i$ 推广为连续 $t$，是 ε-prediction 的连续时间扩展（`extends`）。二者估计的是同一个 score，仅离散/连续之别（`compares_with`）。
→ **跨源（→ thm-ho2020-score-matching-langevin-equivalence）**：ho2020 启发式指出 DDPM 目标"形似"score matching；本方法在连续时间严格以 $\nabla_{\mathbf{x}}\log p_{t}$ 为优化目标（`extends`）。

## 来源引用

Song et al. 2021, Section 3.3, Eq. (7)。full-text.txt lines 1490-1544。
