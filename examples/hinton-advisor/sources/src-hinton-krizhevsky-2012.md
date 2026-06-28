---
id: src-hinton-krizhevsky-2012
type: paper
value: both
channel: web
url: https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html
collected_at: 2026-06-28
format: html
title: "ImageNet Classification with Deep Convolutional Neural Networks（AlexNet）"
authors: ["Alex Krizhevsky", "Ilya Sutskever", "Geoffrey E. Hinton"]
year: 2012
venue: "Advances in Neural Information Processing Systems (NeurIPS) 25, 1097-1105"
---

## 来源摘要

AlexNet 论文（Krizhevsky-Sutskever-Hinton），2012 ImageNet ILSVRC 冠军，深度学习革命引爆点。8 层深度卷积网络 + ReLU + Dropout + GPU 训练，将 ImageNet top-5 错误率从 ~26% 降至 ~15.3%，实证"深度优于宽度"信念。

### 核心贡献

- 证明深度 CNN 在大规模视觉任务上压倒性优势，终结传统手工特征
- 首次大规模使用 ReLU、Dropout、GPU 训练组合
- 与 Hinton 团队 Dropout 工作（`src-hinton-dropout-2012`/`src-srivastava-dropout-2014`）配套

### 覆盖范围

本来源支撑心智模型 `mm-hinton-depth-beats-breadth` 与判断 `judg-hinton-depth-over-width`，与 `src-hinton-science-2006` 共同构成"深度学习复兴"叙事（2006 DBN 理论 + 2012 AlexNet 实证）。

### 可信度

**高**。NeurIPS 2012 正式发表，Hinton 为通讯作者，深度学习史上最具影响力论文之一。URL HTTP 可达（NeurIPS proceedings）。
