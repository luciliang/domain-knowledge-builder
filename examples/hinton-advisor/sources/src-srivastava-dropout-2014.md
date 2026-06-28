---
id: src-srivastava-dropout-2014
type: paper
value: both
channel: web
url: https://jmlr.org/papers/v15/srivastava14a.html
collected_at: 2026-06-28
format: html
title: "Dropout: A Simple Way to Prevent Neural Networks from Overfitting"
authors: ["Nitish Srivastava", "Geoffrey Hinton", "Alex Krizhevsky", "Ilya Sutskever", "Ruslan Salakhutdinov"]
year: 2014
venue: "JMLR 15, 1929-1958（2012 arXiv:1207.0580 初版）"
---

## 来源摘要

Dropout 正则化奠基论文（Srivastava-Hinton 等）。与 `src-hinton-dropout-2012` 为同一工作的不同 provenance 引用形式（2012 arXiv 初版 vs 2014 JMLR 正式版）。训练时随机置零隐藏单元防共适应，多基准降错率，并用 t-SNE 显示激活更清晰聚类。

### 核心贡献

- Dropout 机制：训练时以概率 p 置零，测试时缩放
- MNIST ~1.1%→~0.8%、TIMIT ~12% 降幅等实证
- t-SNE 可视化证明分布式表示质量提升
- 配套 AlexNet（`src-hinton-krizhevsky-2012`）实证深度 + Dropout

### 覆盖范围

本来源与 `src-hinton-dropout-2012` 共同覆盖知识节点 `exp-hinton2012-dropout`，支撑判断 `judg-hinton-dropout-intuition`、`judg-hinton-depth-over-width`。两个 id 引用同一工作，黄金参照中保留以精确反映 provenance 的两种历史引用形式。

### 可信度

**高**。JMLR 期刊正式发表，Hinton 为共同作者，深度学习最广为使用的正则化之一。URL HTTP 可达（JMLR）。
