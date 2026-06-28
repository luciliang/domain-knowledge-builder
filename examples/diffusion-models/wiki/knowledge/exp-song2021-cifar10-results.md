---
id: exp-song2021-cifar10-results
type: experiment
label: CIFAR-10 Record Results (IS 9.89, FID 2.20, NLL 2.99 bits/dim)
source: song2021
section: Section 4.3, Section 4.4, Tables 2-3
tokens: 1200
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1933
  end_line: 2207
  page: "Unknown"
---

## 精确表述

Score-SDE 结合连续目标（Eq. 7）、PC 采样器与改进架构（NCSN++/DDPM++ 系列），在 CIFAR-10 上取得多项记录：

**样本质量（Table 3，PC 采样器，最小 FID 检查点）**：
| 模型 | FID ↓ | IS ↑ |
|------|-------|------|
| DDPM (ho2020) | 3.17 | 9.46 |
| NCSN++ cont. (VE) | 2.38 | 9.83 |
| **NCSN++ cont. (deep, VE)** | **2.20** | **9.89** |
| DDPM++ cont. (deep, VP) | 2.41 | 9.68 |

**似然（Table 2，黑盒 ODE 求解器，最后检查点，均匀去量化）**：
| 模型 | NLL (bits/dim) ↓ |
|------|------------------|
| DDPM (ho2020, ELBO) | ≤ 3.75 |
| DDPM cont. (sub-VP) | 3.05 |
| **DDPM++ cont. (deep, sub-VP)** | **2.99** |

最佳样本质量模型 NCSN++ cont. (deep, VE) 以 FID 2.20 / IS 9.89 创无条件 CIFAR-10 新纪录，甚至超过当时最好的**类条件**生成模型（BigGAN IS 9.22）。最佳似然模型 DDPM++ cont. (deep, sub-VP) 以 2.99 bits/dim 创均匀去量化 CIFAR-10 新纪录。首次从 score-based 模型获得 CelebA-HQ **1024×1024** 高保真样本。经验上 VE-SDE 样本质量更优，VP/sub-VP SDE 似然更优。

## 适用条件

- 连续训练目标 Eq. 7 + PC 采样器 + 加深网络（NCSN++/DDPM++ deep）三者协同。
- NLL 报告用黑盒 ODE 求解器（精确似然），FID/IS 报告用 PC 采样器。

## 直觉解释

Score-SDE 把 SMLD（此前质量逊于 DDPM）通过连续目标 + PC 采样器 + 更深架构反超 DDPM，证明"统一框架"不只是理论优雅，还能带来实际 SOTA。sub-VP SDE 在似然上尤其强，VE-SDE 在样本质量上尤其强，说明不同 SDE 各有擅长领域。

## 与其他知识的关系

← 由 → meth-song2021-score-based-training + → meth-song2021-pc-sampler（样本质量）/ → meth-song2021-pf-ode-sampling（似然）驱动。
→ **跨源（→ exp-ho2020-cifar10-results）**：直接对比 ho2020 的 FID 3.17 / IS 9.46；本文 FID 2.20 / IS 9.89 显著更优，且似然从 ELBO 上界 ≤3.75 提升到精确 2.99 bits/dim（`compares_with`，high confidence）。

## 来源引用

Song et al. 2021, Tables 2-3, Section 4.4。full-text.txt lines 1933-2207。
