---
id: src-hinton-nc-2006
type: paper
value: both
channel: web
url: https://direct.mit.edu/neco/article-abstract/18/7/1527/7155
collected_at: 2026-06-28
format: html
title: "A Fast Learning Algorithm for Deep Belief Nets"
authors: ["Geoffrey E. Hinton", "Simon Osindero", "Yee-Whye Teh"]
year: 2006
venue: "Neural Computation 18(7), 1527-1554"
---

## 来源摘要

深度信念网（DBN）与对比散度（CD）的奠基论文，2006 年深度学习复兴的标志性工作。提出用 CD 逐层预训练 + 反向传播微调训练深层生成式模型，证明深网络可训得动。

### 核心贡献

- 对比散度（CD-k）算法：用 k 步（通常 k=1）Gibbs 采样近似 Boltzmann 学习的负相位
- 深度信念网逐层预训练流程：RBM 堆叠 → 反传微调
- 实证深网络降维/分类优于浅网络，呼应"深优于宽"信念

### 覆盖范围

本来源覆盖知识节点 `meth-hinton2006-contrastive-divergence`，并支撑心智模型 `mm-hinton-depth-beats-breadth`、`mm-hinton-generative-energy-model`，及多个 judgment。

### 可信度

**高**。Neural Computation 期刊正式发表，Hinton 为第一作者，深度学习复兴里程碑。URL HTTP 可达（MIT Press）。

### 关联 source id

- 同期 Science 论文（降维）以 `src-hinton-science-2006` 引用，二者构成 2006 双子星
- 在 judgment provenance 中以 `src-hinton-nc-2006` 引用
