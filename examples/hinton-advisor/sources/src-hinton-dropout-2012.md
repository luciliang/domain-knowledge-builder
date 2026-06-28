---
id: src-hinton-dropout-2012
type: paper
value: both
channel: web
url: https://jmlr.org/papers/v15/srivastava14a.html
collected_at: 2026-06-28
format: html
title: "Dropout: A Simple Way to Prevent Neural Networks from Overfitting"
authors: ["Nitish Srivastava", "Geoffrey Hinton", "Alex Krizhevsky", "Ilya Sutskever", "Ruslan Salakhutdinov"]
year: 2014
venue: "JMLR 15, 1929-1958（含 2012 arXiv:1207.0580 初版）"
---

## 来源摘要

Dropout 正则化的奠基论文（Srivastava, Hinton 等）。提出训练时随机置零隐藏单元防共适应，在 MNIST/TIMIT/ImageNet 等多个基准降错率，并用 t-SNE 显示激活按类别更清晰聚类。

### 核心贡献

- Dropout 机制：训练时以概率 p 置零，测试时缩放（或 inverted dropout）
- 多基准实证：MNIST ~1.1%→~0.8%，TIMIT ~12% 降幅
- t-SNE 可视化证明表示质量提升（分布式表示更鲁棒）
- 配套 AlexNet（2012 ImageNet 冠军，Hinton 团队）实证深度 + Dropout

### 覆盖范围

本来源覆盖知识节点 `exp-hinton2012-dropout`，并支撑 judgment `judg-hinton-dropout-intuition`、`judg-hinton-depth-over-width`。

### 可信度

**高**。JMLR 期刊正式发表，Hinton 为共同作者，Dropout 是深度学习最广为使用的正则化之一。URL HTTP 可达（JMLR）。

### 关联 source id

- 2012 初版 arXiv:1207.0580 与 AlexNet 论文以 `src-hinton-krizhevsky-2012` 关联引用
- 在 judgment provenance 中以 `src-hinton-dropout-2012` 或 `src-srivastava-dropout-2014` 引用（同一工作）
