---
id: ins-song2021-unified-continuous-framework
type: insight
label: Unified Continuous-Time Framework (SMLD & DDPM Are SDE Special Cases)
source: song2021
section: Section 1, Section 3.4, Section 4
tokens: 1000
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1145
  end_line: 1200
  page: "Unknown"
---

## 精确表述

论文的首要贡献是提供一个**连续时间统一框架**：把此前独立的 SMLD（score matching + Langevin）和 DDPM（变分 ELBO + ε-prediction）统一为"扰动数据的一个 SDE + 其 reverse-time SDE"这同一种语言。二者的差别仅在于选择哪条前向 SDE——VE-SDE（无收缩，方差爆炸）对应 SMLD，VP-SDE（有收缩，方差保持）对应 DDPM（→ thm-song2021-sde-discretization-equivalence）。

统一带来的实际收益：
1. **灵活采样**：PC 采样器统一并改进了 SMLD（identity predictor + Langevin corrector）和 DDPM（ancestral predictor + identity corrector）的采样器。
2. **新能力**：probability flow ODE 给出精确似然、唯一可识别编码、latent 操控；conditional SDE 给出可控生成——这些在离散 DDPM/SMLD 框架中均不可得。
3. **设计空间**：可在统一框架内自由探索新 SDE（如 sub-VP SDE），针对不同目标（样本质量 vs 似然）调优。作者证明 VE-SDE 偏样本质量、VP/sub-VP 偏似然。

## 适用条件

- 适用于任何可写成 SDE 的连续扩散过程（漂移仿射时转移核为高斯，最实用）。

## 直觉解释

Score-SDE 的洞见是"不要在离散方法层面比较 SMLD 和 DDPM，而要退一步看它们背后的连续过程"。一旦放到连续时间，两种方法的共性（都在估计 score）和差异（不同的加噪 SDE）一目了然，而且连续视角天然解锁了 ODE、精确似然、可控生成等离散视角看不到的能力。这是"统一即力量"的典范。

## 与其他知识的关系

← 由 → thm-song2021-sde-discretization-equivalence（离散-连续等价）理论支撑。
→ PC 采样器（→ meth-song2021-pc-sampler）和 sub-VP SDE（→ def-song2021-vp-sde）是框架"设计空间"的实例。
→ **跨源（→ thm-ho2020-score-matching-langevin-equivalence）**：ho2020 的核心贡献是发现 DDPM ≈ score matching + Langevin（离散、启发式）；本洞察把它提升为框架级定理——DDPM 恰是某个连续 SDE 的离散化，且只是统一框架的一个特例（`generalizes` / `extends`）。
→ **跨源（→ ins-ho2020-autoregressive-generalization）**：ho2020 把扩散诠释为广义自回归解码；Score-SDE 则诠释为连续 SDE/ODE，是更高层的统一视角。

## 来源引用

Song et al. 2021, Section 1（contributions）, Section 3.4, Section 4。full-text.txt lines 1145-1200, 1574-1670。
