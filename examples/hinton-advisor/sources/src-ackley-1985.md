---
id: src-ackley-1985
type: paper
value: both
channel: web
url: https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog0901_7
collected_at: 2026-06-28
format: html
title: "A Learning Algorithm for Boltzmann Machines"
authors: ["David H. Ackley", "Geoffrey E. Hinton", "Terrence J. Sejnowski"]
year: 1985
venue: "Cognitive Science 9(1), 147-169"
---

## 来源摘要

Boltzmann 机学习规则的奠基论文（Ackley-Hinton-Sejnowski）。提出对称连接的能量模型，定义"正相位（数据钳制）- 负相位（自由运行）"学习规则 $\Delta w_{ij} = \epsilon(\langle s_i s_j \rangle_{\text{data}} - \langle s_i s_j \rangle_{\text{model}})$。

### 核心贡献

- 形式化 Boltzmann 机的能量函数与 Gibbs 分布
- 定义"理解即生成"的学习规则（最小化 KL(data||model)）
- 奠定 Hinton 终身的生成式/能量模型信念

### 覆盖范围

本来源覆盖知识节点 `thm-ackley1985-boltzmann-learning`，并支撑 judgment `judg-hinton-prefers-generative`、`judg-hinton-backprop-legacy`。

### 可信度

**高**。Cognitive Science 期刊正式发表，Hinton 为共同作者，是生成式神经网络经典文献。URL HTTP 可达（Wiley）。

### 关联 source id

- 在 judgment provenance 中以 `src-ackley-1985` 引用
