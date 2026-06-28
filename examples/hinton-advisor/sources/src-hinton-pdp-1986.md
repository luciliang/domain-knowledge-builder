---
id: src-hinton-pdp-1986
type: paper
value: both
channel: web
url: https://direct.mit.edu/books/book/3967/chapter-abstract/137077/Learning-Internal-Representations-by-Error
collected_at: 2026-06-28
format: html
title: "Learning Internal Representations by Error Propagation（PDP 第 2 卷第 8 章）"
authors: ["David E. Rumelhart", "Geoffrey E. Hinton", "Ronald J. Williams"]
year: 1986
venue: "Parallel Distributed Processing, Vol. 2, MIT Press, ch. 8, pp. 318-362"
---

## 来源摘要

反传算法的奠基性长文（Rumelhart-Hinton-Williams），《Parallel Distributed Processing》两卷本第 2 卷第 8 章，与 Nature 短文同期。详细推导多层网络链式法则反向传播，论证分布式内部表示的可学习性，是分布式表示信念的方法论基础。

### 核心贡献

- 系统推导反向传播链式法则递推，并讨论隐藏层表示自发涌现
- 与 PDP 两卷本整体共同确立"分布式表示 + 并行处理"认知科学范式
- 用 family-tree、XOR 等任务实证隐藏层学到结构化表示

### 覆盖范围

本来源与 `src-rumelhart-nature-1986`（同一工作的 Nature 短文形式）构成 1986 反传双子星，共同覆盖知识节点 `thm-rumelhart1986-backprop-chain-rule`，并支撑心智模型 `mm-hinton-distributed-representation` 与判断 `judg-hinton-distributed-vs-symbolic`、`ap-hinton-against-symbolic-ai`。

### 可信度

**高**。MIT Press 经典两卷本正式章节，Hinton 为共同作者，分布式表示与连接主义的奠基文献。URL HTTP 可达（MIT Press）。
