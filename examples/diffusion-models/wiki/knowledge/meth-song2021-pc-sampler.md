---
id: meth-song2021-pc-sampler
type: method
label: Predictor-Corrector (PC) Samplers
source: song2021
section: Section 4.2
tokens: 1200
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1719
  end_line: 1865
  page: "Unknown"
---

## 精确表述

Score-SDE 提出的核心采样创新——**Predictor-Corrector (PC) 采样器**。与通用 SDE 求解器不同，score 模型 $\mathbf{s}_{\boldsymbol{\theta}^{*}}(\mathbf{x},t)\approx\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$ 提供了额外信息，可用于在每个时间步**纠正**边际分布。

**两步交替**：
- **Predictor（预测器）**：用数值 SDE 求解器（Euler-Maruyama、ancestral sampling、reverse diffusion sampler）沿 reverse-time SDE 给出下一时间步的样本估计。
- **Corrector（校正器）**：用基于 score 的 MCMC（Langevin MCMC / HMC）在该时间步直接从 $p_{t}$ 采样，纠正预测器的误差。

每个 predictor 步后加一个 corrector 步（PC1000 = 1000 predictor + 1000 corrector 步）即可在相同计算量下持续提升样本质量。PC 采样器统一并改进了既有方法：SMLD = identity predictor + annealed Langevin corrector；DDPM = ancestral sampling predictor + identity corrector。

## 适用条件

- 已有训练好的 score 模型 $\mathbf{s}_{\boldsymbol{\theta}^{*}}(\mathbf{x},t)$。
- 需选择 predictor 类型（ancestral / reverse diffusion）和 corrector 类型（Langevin / HMC）及各自步数。
- 引入超参数（corrector 步数、步长），论文指出这是需要调参的代价。

## 直觉解释

通用 SDE 求解器只"预测"下一时刻的样本，但离散化会引入误差，使样本偏离真实边际 $p_{t}$。既然我们手里有 score（密度的梯度），就可以在每一时刻用 MCMC 把样本"拉回"正确的 $p_{t}$ 分布——这就是"纠正"。预测+纠正交替，比任何单一手段都更准。

## 与其他知识的关系

← 求解 → thm-song2021-reverse-time-sde（reverse-time SDE），corrector 直接利用 → def-song2021-score-function。
→ 性能由 → exp-song2021-sampler-comparison（Table 1）评估。
↔ 统一并改进 → meth-ho2020-ddpm-sampling（DDPM ancestral sampling 是 PC 的 predictor-only 退化，见 → ins-song2021-unified-continuous-framework）。

## 来源引用

Song et al. 2021, Section 4.2, Table 1；Algorithms 2-3（Appendix G）。full-text.txt lines 1719-1865。
