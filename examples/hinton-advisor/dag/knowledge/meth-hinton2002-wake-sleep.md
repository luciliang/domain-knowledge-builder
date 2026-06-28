---
id: meth-hinton2002-wake-sleep
type: method
label: Wake-Sleep Algorithm (Hinton et al. 1995)
source: hinton1995
section: Section 2 (The Wake-Sleep Algorithm)
tokens: 950
created: 2026-06-28
generated_by_step: S2
run_id: golden-hinton-advisor-0001
source_span:
  file: hinton1995-wake-sleep.pdf
  start_line: 1
  end_line: 1
  page: "1208-1224"
---

## 精确表述

赫尔姆霍茨机（Helmholtz Machine）含两个网络：**生成模型** $P(\mathbf{h}|\mathbf{v}) \to P(\mathbf{v}|\mathbf{h})$（自顶向下）与**识别模型** $Q(\mathbf{h}|\mathbf{v})$（自底向上）。Wake-Sleep 用两阶段交替学习逼近最大似然：

- **Wake 阶段**：用识别模型 $Q$ 从真实数据推断隐藏表示，然后更新**生成模型** $P$ 的参数（梯度下降对数似然 $\log P(\mathbf{v}|\mathbf{h})$）
- **Sleep 阶段**：用生成模型 $P$ 自由"做梦"生成幻想数据，然后更新**识别模型** $Q$（把幻想数据当作监督标签反传）

两个网络互为对方的目标——识别网络教生成网络"怎么生成"，生成网络教识别网络"怎么识别"。

## 适用条件

1. 分层生成模型（如 sigmoid 信念网），层间条件概率可解析
2. 隐藏单元条件独立（便于采样）
3. 接受近似——Wake-Sleep 并非严格最大似然，因 Sleep 阶段假设的 $Q$ 分布与真后验有偏差

## 直觉解释

这是 Hinton 在变分推断流行之前，对"如何训练深层生成模型"给出的第一个实用答案。它绕开了 Boltzmann 机漫长的 Gibbs 采样：用**两个互补网络**——一个负责"看见→理解"（识别），一个负责"想象→生成"（生成）——互相教学。虽不严格等于最大似然，但首次让深层概率模型可训练，是 DBN/RBM 路线的思想前身。

## 与其他知识的关系

→ thm-ackley1985-boltzmann-learning（Wake-Sleep 用识别模型绕开 Gibbs 平衡采样，是 Boltzmann 学习的另一种实用化）
→ meth-hinton2006-contrastive-divergence（CD 用截断 Gibbs 解决单层 RBM，Wake-Sleep 用双网络解决多层信念网）
→ def-hinton2014-distributed-representation（识别模型的隐藏激活即学到的分布式表示）

## 来源引用

Hinton, Dayan, Frey & Neal (1995), "The Wake-Sleep Algorithm for Unsupervised Neural Networks", *Science* 268(5214), pp. 1158-1161。
