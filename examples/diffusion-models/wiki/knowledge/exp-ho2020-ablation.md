---
id: exp-ho2020-ablation
type: experiment
label: Reverse Process Parameterization & Objective Ablation
source: ho2020
section: Section 4.2, Table 2
tokens: 850
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 268
  end_line: 294
  page: "5"
---

## 精确表述

Table 2 消融了反向过程参数化与训练目标在**无条件 CIFAR-10** 上的影响：

| 参数化 | 目标 | IS | FID |
|--------|------|-----|-----|
| $\tilde{\mu}$ 预测 | L, learned diag Σ | 7.28±0.10 | 23.69 |
| $\tilde{\mu}$ 预测 | L, fixed isotropic Σ | 8.06±0.09 | 13.22 |
| $\tilde{\mu}$ 预测 | $\|\tilde{\mu}-\tilde{\mu}_\theta\|^2$ | 不稳定 | 不稳定 |
| ε 预测 | L, learned diag Σ | 不稳定 | 不稳定 |
| ε 预测 | L, fixed isotropic Σ | 7.67±0.13 | 13.51 |
| **ε 预测** | **$\|\tilde{\epsilon}-\epsilon_\theta\|^2$ (Lsimple)** | **9.46±0.11** | **3.17** |

**结论：**
1. 预测 $\tilde{\mu}$ 只在用真变分下界 $L$（非去加权 MSE）训练时才好用。
2. **学习对角 $\Sigma_\theta$** 导致训练不稳、样本变差——固定方差更优（→ meth-ho2020-variance-schedule）。
3. ε 预测在真下界+固定方差下与 $\tilde{\mu}$ 预测相当；但配合 → meth-ho2020-ddpm-training 的 Lsimple 时**显著更好**（FID 3.17 vs 13.51）。

## 适用条件

- 无条件 CIFAR-10；同上 → exp-ho2020-cifar10-results 的训练配置。
- 空白条目表示该组合训练不稳定、产生越界分数无法评估。

## 直觉解释

ε 预测本身不神奇（配真下界时和 μ̃ 预测打平），但它和 Lsimple 这一"去加权"目标搭配时产生巨大的协同增益。这条消融直接证明了论文两个核心设计（ε 参数化 + Lsimple）必须同时启用才有效，也为后续工作锁定"ε + 固定方差"为标准配方。

## 与其他知识的关系

← 评估 → meth-ho2020-epsilon-prediction、→ meth-ho2020-ddpm-training、→ meth-ho2020-variance-schedule。
→ 实证支撑 → thm-ho2020-score-matching-langevin-equivalence 与 → ins-ho2020-simplified-objective-downweights。

## 来源引用

Ho et al. 2020, Section 4.2, Table 2。full-text.txt lines 268-294, 354-363。
