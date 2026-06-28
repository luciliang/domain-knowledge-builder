---
id: judg-hinton-capsule-over-pooling
type: judgment
label: Capsule 替代 max-pooling，因为池化丢弃了位置信息
status: verified
trigger: "Capsule 为什么替代池化 / Hinton 怎么看 max-pooling"
derived_from: mm-hinton-distributed-representation
judgment: "max-pooling 丢弃'东西在哪里'只保留'最强烈特征是什么'，对视觉不自然；Capsule 用向量激活 + 动态路由保留实例化参数（pose/scale/rotation）"
reasoning: "Hinton 终身批评 max-pooling：它扔掉空间位置信息，与'视觉理解 = 学到结构化表示'信念冲突。Capsule 把标量激活升级为向量（长度=存在性，方向=实例化参数），用动态路由让低层零件预测与高层整体一致——这是'层级化组合 = 视觉理解'在架构层面的体现，也是分布式表示的结构化加强版。"
grounded_in:
  - node: meth-sabour2017-capsule-routing
    role: supports
    quote: "Capsule 向量激活：长度表存在性，方向表实例化参数；动态路由 b_ij ← b_ij + û·v 即一致协议"
  - node: def-hinton2014-distributed-representation
    role: supports
    quote: "Capsule 向量是分布式表示的强化版——结构化的分布式"
counter_evidence:
  - node: meth-hinton2008-tsne
    role: context
    note: "Capsule 在 MNIST/smallNORB 上验证但未在大规模数据集上超越 CNN；max-pooling CNN 凭工程效率仍主流"
confidence: medium
provenance:
  sources:
    - src-sabour-capsules-2017
    - src-hinton-lex-2023
---

# Capsule 替代 max-pooling，因为池化丢弃了位置信息

## 判断背景

Capsule 是 Hinton 2017 年提出的架构，公开挑战 max-pooling CNN 范式，是用户常问的争议点。

## 判断立场

**max-pooling 对视觉不自然，Capsule 保留位置信息**。

## 推理链

1. **批评池化**：max-pooling 丢弃位置信息，违反"结构化表示"信念
2. **向量激活**：长度=存在性，方向=实例化参数（pose/scale/rotation）
3. **动态路由**：低层预测与高层一致则路由加强（routing-by-agreement）
4. **哲学延续**：层级组合 = 视觉理解，是分布式表示的结构化版

## 诚实边界

- Capsule 在 MNIST/smallNORB 验证，但未在 ImageNet 等大规模数据上超越 CNN
- max-pooling CNN 凭工程效率（速度、硬件友好）仍是主流
