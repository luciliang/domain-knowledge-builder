---
id: meth-hinton2008-tsne
type: method
label: t-Distributed Stochastic Neighbor Embedding (t-SNE, van der Maaten & Hinton 2008)
source: vandermaaten2008
section: Section 2-3
tokens: 1050
created: 2026-06-28
generated_by_step: S2
run_id: golden-hinton-advisor-0001
source_span:
  file: vandermaaten2008-tsne.pdf
  start_line: 1
  end_line: 1
  page: "2579-2605"
---

## 精确表述

t-SNE 是非线性降维方法，目标是在低维空间（通常 2D/3D）保持高维数据的局部邻域结构。

**高维**：用高斯核定义点对相似度

$$p_{j|i} = \frac{\exp(-\|\mathbf{x}_i - \mathbf{x}_j\|^2 / 2\sigma_i^2)}{\sum_{k \neq i} \exp(-\|\mathbf{x}_i - \mathbf{x}_k\|^2 / 2\sigma_i^2)}, \quad p_{ij} = \frac{p_{j|i} + p_{i|j}}{2n}$$

**低维**：用（重尾的）Student-t 核定义相似度

$$q_{ij} = \frac{(1 + \|\mathbf{y}_i - \mathbf{y}_j\|^2)^{-1}}{\sum_{k \neq l}(1 + \|\mathbf{y}_k - \mathbf{y}_l\|^2)^{-1}}$$

最小化两分布的 KL 散度 $C = \text{KL}(P \| Q) = \sum_{i \neq j} p_{ij} \log \frac{p_{ij}}{q_{ij}}$，梯度下降。

## 适用条件

1. 数据点数 $n$ 为千~万级（原始 t-SNE 是 $O(n^2)$，Barnes-Hut 近似为 $O(n \log n)$）
2. 主要用于**可视化**（降到 2-3 维），不用于后续建模输入
3. $\sigma_i$ 由困惑度（perplexity）二分搜索确定，是关键超参

## 直觉解释

t-SNE 的核心创新是用**重尾 Student-t 替代低维高斯**，解决"拥挤问题"（crowding problem）：高维中适度远的点在低维会被强行挤到一起。重尾让远点在低维被推开得更远，从而**保局部聚类、放全局位置**。t-SNE 的成功使高维特征（如深度网络的隐藏层激活）可视化成为常规诊断手段，间接推动了"看 hidden representation 才理解网络"的工程文化。

## 与其他知识的关系

→ def-hinton2014-distributed-representation（t-SNE 可视化常用于检验分布式表示是否聚类成有意义的簇）
→ exp-hinton2012-dropout（dropout 论文用 t-SNE 可视化隐藏单元激活的类别分离）
→ ins-hinton2007-deep-vs-breadth（深度网络逐层激活的 t-SNE 图直观展示特征层次化）

## 来源引用

van der Maaten & Hinton (2008), "Visualizing Data using t-SNE", *JMLR* 9, pp. 2579-2605, Sections 2-3。
