# Hinton 领域概览

> Geoffrey Hinton（1947— ）的学术工作贯穿 40 年（1980s 至今），是深度学习从寒冬到复兴再到统治的核心推动者。本概览梳理其知识体系的主线，供导航使用（不存数据，只引用 dag 节点 ID）。

---

## 1. 一条主线：分布式表示

Hinton 终身信念是**"概念不是离散符号，而是高维空间联合激活的模式"**（`def-hinton2014-distributed-representation`）。这条主线串联他所有的工作：

- **学习机制**：反向传播（`thm-rumelhart1986-backprop-chain-rule`，1986）让分布式表示可从数据端到端学习
- **生成式学表示**：Boltzmann 机（`thm-ackley1985-boltzmann-learning`，1985）用"理解即生成"学隐藏层表示
- **结构化表示**：Capsule（`meth-sabour2017-capsule-routing`，2017）把标量激活升级为向量激活
- **强化表示**：Dropout（`exp-hinton2012-dropout`，2012）防共适应，使每个单元独立有用
- **可视化表示**：t-SNE（`meth-hinton2008-tsne`，2008）检验分布式表示是否聚类成语义簇

---

## 2. 深度学习复兴的三步曲（2006-2012）

Hinton 是 2006 年深度学习复兴的旗手，三步曲构成完整叙事：

1. **2006 理论**：对比散度（`meth-hinton2006-contrastive-divergence`）让深网络训得动；深度优于宽度洞察（`ins-hinton2007-deep-vs-breadth`）
2. **2006 工具**：Wake-Sleep（`meth-hinton2002-wake-sleep`，1995）与 CD 是深层生成模型的两种实用化路径
3. **2012 兑现**：Dropout（`exp-hinton2012-dropout`）+ 深度 + GPU 在 AlexNet 上赢 ImageNet，实证"深优于宽"

---

## 3. 生成式偏好：与判别式主流的分歧

Hinton 坚持**"理解 = 生成"**，这是他与 2012 后主流判别式 CNN 的根本分歧：

- **数学根基**：Boltzmann 学习规则 $\Delta w = \epsilon(\langle s_i s_j \rangle_{\text{data}} - \langle s_i s_j \rangle_{\text{model}})$ 本质是生成式最大似然
- **算法实现**：Wake-Sleep（双网络互教）、CD（截断 Gibbs）都是生成式训练的实用化
- **后期批评**：公开质疑纯判别 CNN"会分类但不理解"，因不会生成

这条信念在 2017 Capsule 与对能量模型的持续关注中延续。

---

## 4. 反对什么：纯符号 AI

Hinton 终身反对 GOFAI（经典符号 AI），数学根据在分布式表示的四大优势：相似度结构、指数级容量、鲁棒性、可学习性——符号 localist 表示在四维全输。详见 `ap-hinton-against-symbolic-ai`（心智层反模式）。

---

## 5. 知识体系与心智的耦合

| 知识节点 | 支撑的心智元素 / judgment |
|----------|--------------------------|
| `def-hinton2014-distributed-representation` | `mm-hinton-distributed-representation`、`ap-hinton-against-symbolic-ai`、多数 judgment |
| `thm-rumelhart1986-backprop-chain-rule` | `mm-hinton-distributed-representation`、`mm-hinton-depth-beats-breadth`、`judg-hinton-backprop-legacy` |
| `thm-ackley1985-boltzmann-learning` | `mm-hinton-generative-energy-model`、`judg-hinton-prefers-generative` |
| `ins-hinton2007-deep-vs-breadth` | `mm-hinton-depth-beats-breadth`、`judg-hinton-depth-over-width` |
| `meth-sabour2017-capsule-routing` | `mm-hinton-distributed-representation`、`judg-hinton-capsule-over-pooling` |
| `exp-hinton2012-dropout` | `judg-hinton-dropout-intuition`、`judg-hinton-depth-over-width` |

完整紧耦合关系见 `expert-mind/judgments.md` 的 `grounded_in` 字段。
