---
id: src-hinton-science-2006
type: paper
value: both
channel: web
url: https://www.science.org/doi/10.1126/science.1127647
collected_at: 2026-06-28
format: html
title: "Reducing the Dimensionality of Data with Neural Networks"
authors: ["Geoffrey E. Hinton", "Ruslan R. Salakhutdinov"]
year: 2006
venue: "Science 313(5786), 504-507"
---

## 来源摘要

DBN 降维论文（Hinton-Salakhutdinov），2006 年深度学习复兴双子星之一。用 RBM 逐层预训练的深度自编码器在 MNIST 上将降维重建误差大幅低于 PCA，证明深网络可训得动且优于传统方法。

### 核心贡献

- 用 RBM 堆叠预训练 + 反传微调的深度自编码器降维
- MNIST 重建 MSE 显著低于 PCA（2.3× 优势）
- 与 Neural Computation DBN 论文（`src-hinton-nc-2006`）共同开启深度学习复兴

### 覆盖范围

本来源覆盖知识节点 `meth-hinton2006-contrastive-divergence`（CD 训练机制）与 `ins-hinton2007-deep-vs-breadth`，支撑心智模型 `mm-hinton-depth-beats-breadth` 与判断 `judg-hinton-depth-over-width`。

### 可信度

**高**。Science 期刊正式发表，Hinton 为第一作者，深度学习复兴标志性工作。URL HTTP 可达（Science）。
