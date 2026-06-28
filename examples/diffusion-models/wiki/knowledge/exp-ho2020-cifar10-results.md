---
id: exp-ho2020-cifar10-results
type: experiment
label: CIFAR-10 Sample Quality Results
source: ho2020
section: Section 4, Section 4.1
tokens: 850
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 268
  end_line: 335
  page: "5"
---

## 精确表述

在**无条件 CIFAR-10** 上，DDPM 取得当时最优（state-of-the-art）的样本质量（Table 1）：

| 模型 | IS | FID | NLL Test (Train) bits/dim |
|------|-----|-----|---------------------------|
| Ours (Lsimple) | **9.46 ± 0.11** | **3.17** | ≤ 3.75 (3.72) |
| Ours (L, fixed isotropic Σ) | 7.67 ± 0.13 | 13.51 | ≤ 3.70 (3.69) |
| StyleGAN2+ADA (条件) | 9.74 | 3.26 | — |
| BigGAN (条件) | 9.22 | 14.73 | — |
| NCSN | 8.87 | 25.32 | — |

FID 3.17 优于当时绝大多数模型（含许多**类条件**模型）。FID 按惯例对训练集计算；对测试集算得 5.24，仍优于文献中多数训练集 FID。NLL 在 50000 样本上用 OpenAI/TTUR 代码计算；test-train 差距 ≤ 0.03 bits/dim，表明未过拟合。

最佳配置来自 → meth-ho2020-ddpm-training（Lsimple）+ → meth-ho2020-epsilon-prediction，验证了 → thm-ho2020-score-matching-langevin-equivalence 驱动的参数化。

## 适用条件

- 无条件生成，CIFAR-10（32×32×3）。
- $T=1000$，线性 β 表（→ meth-ho2020-variance-schedule），CIFAR 模型 35.7M 参数。
- 50000 样本评估；dropout=0.1，随机水平翻转，Adam lr=2e-4，batch 128，EMA 0.9999。

## 直觉解释

用 ε-prediction + 简化目标 Lsimple 训练的扩散模型，在无条件设置下就把 FID 压到 3.17，逼近甚至超过强条件 GAN——这是扩散模型"能生成高质量样本"的首次有力证明，扭转了此前扩散模型样本质量不佳的印象。

## 与其他知识的关系

← 评估 → meth-ho2020-ddpm-training、→ meth-ho2020-epsilon-prediction、→ meth-ho2020-variance-schedule。
→ 验证 → thm-ho2020-score-matching-langevin-equivalence（最佳结果来自该参数化）。
↔ 与 → exp-ho2020-ablation 的 L+Σ 配置对比（13.51 vs 3.17）。

## 来源引用

Ho et al. 2020, Section 4.1, Table 1；Appendix B。full-text.txt lines 268-335, 832-881。
