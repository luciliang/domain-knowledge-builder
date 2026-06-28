---
name: hinton-advisor
description: 顶级专家顾问 skill——Geoffrey Hinton（深度学习之父）的心智模型 + 知识依据 + 紧耦合判断。用于回答"Hinton 怎么看深度学习 / 反向传播 / 生成式模型 / 符号 AI"等问题。此为 expert-advisor-builder（domain-knowledge-builder 扩展）的人工策展 A 级黄金参照。
expert: Geoffrey Hinton
domain: 深度学习与神经网络
sources: 5
nodes: 9
edges: 22
mental_elements: 4
judgments: 6
created: 2026-06-28
version: 1.0.0
golden_reference: true
classification: expert-advisor
---

# Geoffrey Hinton 顾问 Skill

## 专家心智摘要

Geoffrey Hinton 是深度学习从寒冬到复兴再到统治的核心推动者（2018 图灵奖）。其 40 年学术工作有四条核心信念：

1. **分布式表示优于符号**（`mm-hinton-distributed-representation`）：概念不是离散符号，而是高维空间联合激活的模式——带来相似度结构、指数级容量、鲁棒性、可学习性四大优势。
2. **深度优于宽度**（`mm-hinton-depth-beats-breadth`）：深层逐层抽象参数量指数级少于浅而宽网络，深度本身是归纳偏置。
3. **理解即生成**（`mm-hinton-generative-energy-model`）：真正理解 = 能自由运行复现统计，纯判别式"会分类但不理解"。
4. **反对纯符号 AI**（`ap-hinton-against-symbolic-ai`）：GOFAI 的离散符号 + 手写规则在四维全输，必须用分布式表示 + 学习。

---

## 查询协议（三模式路由）

按问题意图路由：

| 问题类型 | 模式 | 流程 |
|---------|------|------|
| "什么是 X / X 的定义/定理" | **知识模式** | 遍历 `dag/dag-index.json` 找节点，返回定理/方法原文（含 LaTeX） |
| "Hinton 怎么看 X / 会怎么选" | **心智模式** | 加载心智镜片 + 匹配 `expert-mind/judgments.md`，返回判断 + 推理链 + `grounded_in` 依据节点 ID |
| "Hinton 为什么认为 X / X 的依据" | **融合模式** ⭐ | 镜片理解 → 找 judgment → 加载 `grounded_in` 节点全文 → 综合「立场 + 理论依据 + 替代方案 + 局限」 |
| 模糊 | **融合模式**（默认，最全） | 同上 |

### 融合模式回答示例

> **问**：Hinton 会怎么看「用纯符号规则引擎做常识推理」？
>
> **答**：
> - **[立场]** 大概率反对——符号 localist 表示无相似度结构、无指数级容量 *(judg-hinton-distributed-vs-symbolic)*
> - **[理论依据]** 分布式表示在高维空间编码 $O(2^d)$ 概念，支持类比泛化 *(def-hinton2014-distributed-representation)*；反传让这种表示可学 *(thm-rumelhart1986-backprop-chain-rule)*
> - **[他的替代方案]** 用深度神经网络学分布式向量表示 + 端到端学习
> - **[诚实边界]** 符号 AI 在封闭世界确定性推理（定理证明）上仍有价值，Hinton 反对的是"纯符号、无学习"

### 加载效率

- **核心查询**：SKILL.md（心智 + 协议）≈ 2.5K tokens
- **完整融合查询**：SKILL.md + judgment + 2-3 知识节点 ≈ 6-8K tokens
- **原则**：judgment 的 `grounded_in` 节点 ID 按需加载，不全量读

---

## 知识节点索引（9 个，详见 `wiki/index.md`）

- **Theorem（2）**：`thm-rumelhart1986-backprop-chain-rule`（反传链式法则）、`thm-ackley1985-boltzmann-learning`（Boltzmann 学习规则）
- **Method（4）**：`meth-hinton2006-contrastive-divergence`（CD）、`meth-hinton2002-wake-sleep`、`meth-hinton2008-tsne`、`meth-sabour2017-capsule-routing`
- **Definition（1）**：`def-hinton2014-distributed-representation`（分布式表示）
- **Experiment（1）**：`exp-hinton2012-dropout`
- **Insight（1）**：`ins-hinton2007-deep-vs-breadth`

---

## 术语映射

| 英文 | 中文 |
|------|------|
| Distributed Representation | 分布式表示 |
| Backpropagation | 反向传播 |
| Boltzmann Machine | 玻尔兹曼机 |
| Contrastive Divergence (CD) | 对比散度 |
| Wake-Sleep Algorithm | 醒眠算法 |
| Deep Belief Net (DBN) | 深度信念网 |
| Restricted Boltzmann Machine (RBM) | 受限玻尔兹曼机 |
| Capsule Network | 胶囊网络 |
| Dynamic Routing-by-Agreement | 一致性动态路由 |
| GOFAI | 经典符号 AI |
| grandmother cell | 祖母细胞（局部表示） |

---

## 诚实边界

**已覆盖**：反向传播链式法则、Boltzmann 学习规则、CD/Wake-Sleep 生成式训练、t-SNE 可视化、Dropout 正则化、Capsule 动态路由、分布式表示理论、深度优于宽度洞察。

**未覆盖**：Hinton 后期对前向-前向算法（Forward-Forward Algorithm, 2022）的工作、知识蒸馏（Distillation）、矩阵胶囊等较新方向未纳入本黄金参照（V1 可扩展）。

**有争议**：Capsule 在大规模数据上未超越 CNN（仍开放）；"理解即生成"是哲学立场，难实验证伪；深度优于宽度是渐近论证，非对所有任务严格成立。

---

## 维护说明

- **查询**：读 `dag/dag-index.json` → 遍历边 → 按需加载 `dag/knowledge/*.md`；心智查询读 `expert-mind/judgments.md`
- **Ingest 新内容**：按 `schema/` 四文件规范（schema.md/expert-mind.md/coupling.md/source.md）
- **Lint**：`python3 pipeline/state/lint_d7.py --target-skill-root .` 验证硬门③（无孤儿 judgment）+ 硬门①（mental_model 3 重必 grounded_in）
