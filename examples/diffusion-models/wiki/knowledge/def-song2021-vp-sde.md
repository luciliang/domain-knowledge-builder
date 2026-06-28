---
id: def-song2021-vp-sde
type: definition
label: Variance Preserving (VP) SDE
source: song2021
section: Section 3.4
tokens: 950
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1617
  end_line: 1670
  page: "Unknown"
---

## 精确表述

**Variance Preserving (VP) SDE** 是 DDPM（Sohl-Dickstein 2015; Ho et al. 2020）噪声扰动的连续时间推广。DDPM 的离散马尔可夫链为（Eq. 10）：

$$\mathbf{x}_{i}=\sqrt{1-\beta_{i}}\,\mathbf{x}_{i-1}+\sqrt{\beta_{i}}\,\mathbf{z}_{i-1}$$

当 $N\to\infty$ 时，$\beta_{i}$ 变为连续函数 $\beta(t)$，该链收敛为如下 SDE（Eq. 11）：

$$\mathrm{d}\mathbf{x}=-\frac{1}{2}\beta(t)\,\mathbf{x}\,\mathrm{d}t+\sqrt{\beta(t)}\,\mathrm{d}\mathbf{w}$$

该 SDE 有向原点的线性收缩漂移 $-\frac{1}{2}\beta(t)\mathbf{x}$，当初始分布单位方差时，过程方差恒保持为 1，因此得名 Variance Preserving。

论文还提出 **sub-VP SDE**（Eq. 12），在相同 $\beta(t)$ 下方差总被 VP SDE 的方差上界界定，在似然任务上表现尤佳：

$$\mathrm{d}\mathbf{x}=-\frac{1}{2}\beta(t)\,\mathbf{x}\,\mathrm{d}t+\sqrt{\beta(t)(1-e^{-2\int_{0}^{t}\beta(s)\mathrm{d}s})}\,\mathrm{d}\mathbf{w}$$

VE、VP、sub-VP 三者漂移皆仿射，故转移核 $p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))$ 均为高斯，可闭式计算。

## 适用条件

- $\beta(t)>0$，初始分布单位方差时方差保持为 1（VP）。
- 仿射漂移 → 高斯转移核 → 训练（Eq. 7）高效。

## 直觉解释

VP-SDE 每加一份噪声的同时，把数据向原点收缩一点（乘 $\sqrt{1-\beta}$），两者抵消使总方差保持稳定——这正是 DDPM 的加噪方式。连续化后漂移项 $-\frac{1}{2}\beta(t)\mathbf{x}$ 负责"收缩"，扩散项 $\sqrt{\beta(t)}$ 负责"加噪"。

## 与其他知识的关系

→ 是 → def-song2021-forward-sde 的特例（漂移 $\mathbf{f}=-\frac{1}{2}\beta(t)\mathbf{x}$，扩散 $g=\sqrt{\beta(t)}$）。
→ 与 → def-song2021-ve-sde 并列，构成统一框架的两种典型 SDE（→ thm-song2021-sde-discretization-equivalence）。
→ **跨源（→ def-ho2020-forward-diffusion-process）**：VP-SDE 是 DDPM 离散前向过程 $q(x_t|x_{t-1})=\mathcal{N}(\sqrt{1-\beta_t}x_{t-1},\beta_t I)$ 的**连续时间推广**；DDPM 的加噪链是 VP-SDE 在 $N\to\infty$ 极限下的离散化（`generalizes`）。DDPM 的 ancestral sampling（→ meth-ho2020-ddpm-sampling）恰好是 reverse-time VP SDE 的一种特殊离散化（Section 4.1）。

## 来源引用

Song et al. 2021, Section 3.4, Eqs. (10)-(12)。full-text.txt lines 1617-1670。
