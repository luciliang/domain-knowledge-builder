---
id: src-rumelhart-nature-1986
type: paper
value: both
channel: web
url: https://www.nature.com/articles/323533a0
collected_at: 2026-06-28
format: html
title: "Learning representations by back-propagating errors"
authors: ["David E. Rumelhart", "Geoffrey E. Hinton", "Ronald J. Williams"]
year: 1986
venue: "Nature 323, 533-536"
---

## 来源摘要

反向传播算法的奠基性论文（Rumelhart-Hinton-Williams 三作）。证明多层前馈网络可通过链式法则反向递推高效计算所有隐藏层梯度，使深度网络训练在计算上可行。

### 核心贡献

- 形式化反向传播的链式法则递推：$\delta_j^{(l)} = \varphi'(z_j^{(l)}) \sum_k w_{jk}^{(l+1)} \delta_k^{(l+1)}$
- 证明隐藏层梯度可在 $O(E)$ 时间计算，无需数值差分
- 用 XOR、family-tree 等任务演示隐藏层自发学到有意义表示

### 覆盖范围

本来源覆盖知识节点 `thm-rumelhart1986-backprop-chain-rule`，并支撑多个 judgment（分布式表示学习机制、深度前提、反传历史地位）。

### 可信度

**高**。Nature 期刊正式发表，Hinton 为共同作者，是深度学习史上被引最高的论文之一。URL HTTP 可达（Nature 官网）。

### 关联 source id（同一工作的其他引用形式）

- 在 judgment provenance 中以 `src-rumelhart-nature-1986` 引用
