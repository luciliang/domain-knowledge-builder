---
id: judg-hinton-dropout-intuition
type: judgment
label: Dropout 是防共适应、强化分布式表示的正则化直觉
status: verified
trigger: "Dropout 的直觉是什么 / Hinton 为什么提出 Dropout"
derived_from: mm-hinton-distributed-representation
judgment: "Dropout 通过训练时随机置零单元，强迫每个单元都独立有用、防止单元间共适应，本质是强化分布式表示的鲁棒性"
reasoning: "若隐藏单元间形成共适应（一组单元联合编码某特征，缺一不可），表示就退化成局部符号式——违反分布式表示信念。Dropout 每次前向传播训练一个不同子网络，等价于近似集成大量共享权重的瘦网络，强迫每个单元独立承担信息。t-SNE 可视化显示加 Dropout 的激活按类别更清晰聚类，证明它不仅降过拟合，还诱导更有语义结构的分布式表示。"
grounded_in:
  - node: exp-hinton2012-dropout
    role: supports
    quote: "Dropout 在 MNIST 把错误率从 ~1.1% 降到 ~0.8%，t-SNE 显示激活按类别更清晰聚类"
  - node: def-hinton2014-distributed-representation
    role: supports
    quote: "Dropout 防止单元共适应，使每个单元独立有用——直接强化分布式表示"
  - node: thm-rumelhart1986-backprop-chain-rule
    role: context
    quote: "Dropout 在反传流程上加随机掩码，与反传正交但兼容"
confidence: high
provenance:
  sources:
    - src-hinton-dropout-2012
    - src-srivastava-dropout-2014
---

# Dropout 是防共适应、强化分布式表示的正则化直觉

## 判断背景

Dropout 是 Hinton 团队 2012 年提出的最广为使用的正则化技术之一，用户常问其设计直觉。

## 判断立场

**Dropout 本质是强化分布式表示**——防共适应 = 防退化成局部符号。

## 推理链

1. **共适应问题**：单元联合编码 → 退化成局部符号式，违反分布式信念
2. **Dropout 机制**：随机置零 → 每个单元独立有用 → 强制分布式
3. **等价集成**：每次训练不同子网络，近似集成大量瘦网络
4. **实证验证**：t-SNE 显示 Dropout 后激活按类别更清晰聚类

## 诚实边界

- Dropout 在测试时需缩放权重（或 inverted dropout），实现细节易错
- 后续 BatchNorm、Skip-Connection 部分替代了 Dropout 的作用
