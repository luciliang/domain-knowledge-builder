---
id: exp-ho2020-lsun-results
type: experiment
label: LSUN and CelebA-HQ 256 Results
source: ho2020
section: Section 4.1
tokens: 700
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 339
  end_line: 352
  page: "6"
---

## 精确表述

DDPM 在 256×256 高分辨率数据集上同样取得接近 ProgressiveGAN 的样本质量（Table、Figs 3-4）：

- **LSUN Church**：FID = **7.89**
- **LSUN Bedroom**：FID = **4.90**
- **CelebA-HQ 256×256**、LSUN Cat：高质量样本（FID 用 StyleGAN2 代码在 50000 样本上计算）。

样本质量与 ProgressiveGAN 相当（abstract 原文："sample quality similar to ProgressiveGAN"）。256×256 模型用 114M 参数（LSUN Bedroom 另训一个约 256M 的更大变体）。

## 适用条件

- 无条件生成，256×256 图像。
- $T=1000$，线性 β 表（→ meth-ho2020-variance-schedule）；batch 64，lr 降到 2e-5（大图训练更易不稳）。
- 训练步数：CelebA-HQ 0.5M、LSUN Bedroom 2.4M、Cat 1.8M、Church 1.2M。

## 直觉解释

扩散模型不只在小图 CIFAR 上有效，把同样的配方直接放大到 256×256 自然图像（教堂/卧室/人脸），无需架构级改动即可得到与 ProgressiveGAN 同级的样本质量，说明方法的可扩展性。

## 与其他知识的关系

← 用 → meth-ho2020-ddpm-training + → meth-ho2020-ddpm-sampling。
↔ 与 → exp-ho2020-cifar10-results 共同支撑扩散模型"高质量生成"结论。

## 来源引用

Ho et al. 2020, Section 4.1, Figures 3-4；Appendix B。full-text.txt lines 339-352, 839-847。
