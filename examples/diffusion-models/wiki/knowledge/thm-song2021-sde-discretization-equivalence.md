---
id: thm-song2021-sde-discretization-equivalence
type: theorem
label: SMLD/DDPM Are Discretizations of VE/VP SDEs
source: song2021
section: Section 3.4
tokens: 1100
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1574
  end_line: 1670
  page: "Unknown"
---

## 精确表述

Score-SDE 的核心统一结果：SMLD 与 DDPM 两种此前独立的方法，分别是**两个不同 SDE 的离散化**（Section 3.4）：

| 方法 | 离散马尔可夫链 | 连续极限 SDE | 命名 |
|------|--------------|-------------|------|
| SMLD（NCSN） | $\mathbf{x}_{i}=\mathbf{x}_{i-1}+\sqrt{\sigma_{i}^{2}-\sigma_{i-1}^{2}}\,\mathbf{z}_{i-1}$ | $\mathrm{d}\mathbf{x}=\sqrt{\frac{\mathrm{d}[\sigma^{2}(t)]}{\mathrm{d}t}}\,\mathrm{d}\mathbf{w}$（Eq. 9） | VE-SDE |
| DDPM | $\mathbf{x}_{i}=\sqrt{1-\beta_{i}}\,\mathbf{x}_{i-1}+\sqrt{\beta_{i}}\,\mathbf{z}_{i-1}$ | $\mathrm{d}\mathbf{x}=-\frac{1}{2}\beta(t)\mathbf{x}\,\mathrm{d}t+\sqrt{\beta(t)}\,\mathrm{d}\mathbf{w}$（Eq. 11） | VP-SDE |

当噪声尺度数 $N\to\infty$，$\sigma_{i}\to\sigma(t)$、$\beta_{i}\to\beta(t)$、$\mathbf{z}_{i}\to\mathbf{w}(t)$，离散链收敛到连续 SDE。二者的训练目标（Eq. 1 SMLD、Eq. 3 DDPM）都是加权去噪 score matching，仅权重不同（$\sigma_{i}^{2}$ vs $(1-\alpha_{i})$），且权重与各自扰动核的方差同形。因此 SMLD 与 DDPM 在连续极限下统一为"训练一个估计 $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$ 的 score 模型"这同一任务。

## 适用条件

- $N\to\infty$ 的连续极限。
- 仿射漂移 → 高斯转移核（VE、VP、sub-VP 均满足）。

## 直觉解释

此前 SMLD（score matching + Langevin）和 DDPM（变分 ELBO + ε-prediction）看似是两套完全不同的语言。Score-SDE 证明它们其实是同一枚硬币的两面：差别仅在于选择哪条前向 SDE（VE 无收缩 vs VP 有收缩），而连续化后两者都在做同一件事——估计 score。这一等价是统一框架（→ ins-song2021-unified-continuous-framework）的理论基石。

## 与其他知识的关系

← 依赖 → def-song2021-forward-sde、→ def-song2021-ve-sde、→ def-song2021-vp-sde。
→ 直接支撑 → ins-song2021-unified-continuous-framework（连续时间统一框架洞察）。
→ **跨源（→ def-ho2020-forward-diffusion-process）**：DDPM 前向链是 VP-SDE 的离散化（`generalizes`，SDE 推广离散）。
→ **跨源（→ thm-ho2020-score-matching-langevin-equivalence）**：ho2020 在离散视角发现"训练≈score matching、采样≈Langevin"；本定理在连续时间严格证明 DDPM 训练目标确为去噪 score matching 的一种（`extends`），把 ho2020 的启发式等价提升为框架级等价。

## 来源引用

Song et al. 2021, Section 3.4, Eqs. (8)-(12)。full-text.txt lines 1574-1670。
