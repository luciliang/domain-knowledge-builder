---
id: src-sabour-capsules-2017
type: paper
value: both
channel: web
url: https://arxiv.org/abs/1710.09829
collected_at: 2026-06-28
format: html
title: "Dynamic Routing Between Capsules（Capsule Networks）"
authors: ["Sara Sabour", "Nicholas Frosst", "Geoffrey E. Hinton"]
year: 2017
venue: "Advances in Neural Information Processing Systems (NeurIPS) 30"
---

## 来源摘要

Capsule Network 与动态路由（Dynamic Routing-by-Agreement）的奠基论文（Sabour-Frosst-Hinton）。提出以"胶囊"（向量而非标量神经元）+ 一致性路由替代 max-pooling，建模部分-整体层级关系，体现 Hinton 对 max-pooling 丢失空间结构的长期批评。

### 核心贡献

- 胶囊：输出向量（活动向量编码实例化参数），模长表存在概率、方向表属性
- 动态路由-by-agreement：下层胶囊路由到与之一致的上层胶囊，替代 max-pooling
- MNIST 上超越基线 CNN，体现"理解即生成/层级结构"信念

### 覆盖范围

本来源覆盖知识节点 `meth-sabour2017-capsule-routing`，并支撑判断 `judg-hinton-capsule-over-pooling`（Hinton 为通讯作者，是其反 max-pooling 立场的直接实现）。

### 可信度

**高**。NeurIPS 2017 正式发表，Hinton 为通讯作者，Capsule 路线奠基文献。URL HTTP 可达（arXiv）。
