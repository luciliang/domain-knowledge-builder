# 知识节点索引（Hinton 视角）

> 领域：深度学习与神经网络（Geoffrey Hinton 视角） | 节点数：9 | 边数：22 | 来源数：5
> 生成日期：2026-06-28 | 黄金参照：是
>
> **注意**：本文件是纯导航层（只引用 dag 节点 ID）。节点定义见 `dag/knowledge/`，关系图见 `dag/dag-index.json`。

---

## Definition（定义 · 1 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| `def-hinton2014-distributed-representation` | Distributed Representation | 概念由多维度联合激活模式表示，非单一符号——Hinton 40 年信念的根基 |

---

## Theorem（定理 · 2 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| `thm-rumelhart1986-backprop-chain-rule` | Backpropagation Chain Rule (1986) | 链式法则反向递推高效计算所有隐藏层梯度，使深度网络训练可行 |
| `thm-ackley1985-boltzmann-learning` | Boltzmann Machine Learning Rule (1985) | Δw=ε(⟨si·sj⟩data − ⟨si·sj⟩model)，"理解即生成"的数学基石 |

---

## Method（方法 · 4 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| `meth-hinton2006-contrastive-divergence` | Contrastive Divergence (2006) | 用 1 步 Gibbs 近似 Boltzmann 学习负相位，深度学习复兴催化剂 |
| `meth-hinton2002-wake-sleep` | Wake-Sleep Algorithm (1995) | 双网络（识别+生成）互教，绕开 Gibbs 采样的多层生成模型训练法 |
| `meth-hinton2008-tsne` | t-SNE (2008) | 重尾 Student-t 核保局部聚类放全局位置，高维特征可视化标准工具 |
| `meth-sabour2017-capsule-routing` | Capsule Networks (2017) | 向量激活 + 动态路由，替代 max-pooling 保留位置/实例化参数 |

---

## Experiment（实验 · 1 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| `exp-hinton2012-dropout` | Dropout Regularization (2012) | 随机置零防共适应，MNIST/TIMIT/ImageNet 多基准降错率，t-SNE 显示表示更优 |

---

## Insight（洞察 · 1 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| `ins-hinton2007-deep-vs-breadth` | Depth Beats Breadth (2006/2007) | 深层逐层抽象参数量指数级少于浅而宽网络，深度是根本归纳偏置 |

---

## 关系图摘要

22 条边覆盖 10 种关系类型（`applies_to`/`specializes`/`extends`/`compares_with`/`depends_on`/`evaluates`/`generalizes`/`uses` 等）。详见 `dag/dag-index.json` 的 `edges` 字段。

核心关系链：
- `def-hinton2014-distributed-representation` ← `thm-rumelhart1986-backprop-chain-rule`（applies_to：反传学分布式表示）
- `thm-ackley1985-boltzmann-learning` → `meth-hinton2006-contrastive-divergence`（specializes：CD 是 Boltzmann 学习的近似）
- `ins-hinton2007-deep-vs-breadth` ← `meth-hinton2006-contrastive-divergence`（applies_to：CD 让深网络训得动）
- `meth-sabour2017-capsule-routing` → `def-hinton2014-distributed-representation`（specializes：capsule 向量是分布式表示强化版）
