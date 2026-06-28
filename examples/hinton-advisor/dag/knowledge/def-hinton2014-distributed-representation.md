---
id: def-hinton2014-distributed-representation
type: definition
label: Distributed Representation (Hinton 1984/2014)
source: hinton2014
section: Section 1-2
tokens: 900
created: 2026-06-28
generated_by_step: S2
run_id: golden-hinton-advisor-0001
source_span:
  file: hinton2014-distributed-representations.pdf
  start_line: 1
  end_line: 1
  page: "1-12"
---

## 精确表述

**分布式表示**（distributed representation）：一个概念 / 实体由多个特征维度的**联合激活模式**表示，而非由单一符号或单一"祖母细胞"表示。

形式化：设特征空间 $\mathbb{R}^d$，实体 $x$ 的表示是向量 $\mathbf{r}(x) \in \mathbb{R}^d$。$x$ 的"身份"由 $\mathbf{r}(x)$ 在**多个维度上的取值组合**决定，而非任一单个维度。相似实体（如"猫""狗"）的向量在多数维度上重合、少数维度上不同，从而支持**泛化**与**相似度计算**。

对比 **localist representation**（局部表示）：每个概念对应一个独立单元（one-hot），概念间无内在结构，无法天然表达相似度。

容量论证：$d$ 维二值分布式表示可编码 $O(2^d)$ 个不同模式，而 localist 只能编码 $O(d)$ 个。

## 适用条件

1. 表示空间维度 $d \gg 1$（分布式优势在高维才显现）
2. 学习目标鼓励"相似输入→相似表示"（如端到端梯度训练）
3. 需要泛化 / 组合性 / 鲁棒性（单一单元损坏不应丢失整个概念）

## 直觉解释

这是 Hinton 贯穿 40 年的核心信念。在符号 AI 时代，他坚持"概念不是离散符号，而是高维空间的区域"。分布式表示带来三大红利：(1) **相似度结构**——天然支持类比与泛化；(2) **指数级容量**——有限维度编码海量概念；(3) **鲁棒性**——损坏部分维度不摧毁整个概念。这一思想是反向传播（学习好表示）、Boltzmann 机（生成式学表示）、capsule（结构化向量表示）、word2vec 等所有表示学习工作的共同根基。

## 与其他知识的关系

→ thm-rumelhart1986-backprop-chain-rule（反传是学习分布式表示的核心机制）
→ thm-ackley1985-boltzmann-learning（Boltzmann 机的隐藏层激活即学到的分布式表示）
→ meth-sabour2017-capsule-routing（capsule 向量是分布式表示的"结构化"加强版）
→ meth-hinton2008-tsne（t-SNE 用于检验分布式表示是否聚类成语义簇）
→ exp-hinton2012-dropout（dropout 防止单元共适应，强化分布式表示的鲁棒性）

## 来源引用

Hinton, McClelland & Rumelhart (1986), "Distributed Representations", in *Parallel Distributed Processing*, Vol. 1, Ch. 3。
Hinton (2014), "Distributed Representations", lectures & cogsci work。
