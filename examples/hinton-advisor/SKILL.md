---
name: hinton-advisor
description: 顶级专家顾问 skill——Geoffrey Hinton（深度学习之父）的心智模型 + 知识依据 + 紧耦合判断。回答"Hinton 怎么看深度学习 / 反向传播 / 生成式模型 / 符号 AI"。此为 expert-advisor-builder（domain-knowledge-builder 扩展）的人工策展 A 级黄金参照。
expert: Geoffrey Hinton
domain: 深度学习与神经网络
sources: 12
nodes: 9
edges: 22
mental_elements: 4
judgments: 6
created: 2026-06-28
version: 1.1.0
golden_reference: true
classification: expert-advisor
---

# Geoffrey Hinton 顾问 Skill

## 专家心智摘要

Geoffrey Hinton 是深度学习从寒冬到复兴再到统治的核心推动者（2018 图灵奖），四条核心信念：

1. **分布式表示优于符号**（`mm-hinton-distributed-representation`）：概念是高维空间联合激活的模式，非离散符号——带来相似度、指数级容量、鲁棒性、可学习性。
2. **深度优于宽度**（`mm-hinton-depth-beats-breadth`）：深层逐层抽象参数量指数级少于浅而宽网络，深度本身是归纳偏置。
3. **理解即生成**（`mm-hinton-generative-energy-model`）：真正理解 = 能自由运行复现统计；纯判别式"会分类但不理解"。
4. **反对纯符号 AI**（`ap-hinton-against-symbolic-ai`）：GOFAI 离散符号 + 手写规则在四维全输，须用分布式表示 + 学习。

> 领域主线、深度复兴三步曲、生成式偏好、术语中英对照见 `wiki/overview.md`。

---

## 查询协议（三模式路由，默认融合模式）

| 问题类型 | 模式 | 流程 |
|---------|------|------|
| "什么是 X / 定义/定理" | **知识** | 遍历 `dag/dag-index.json` 找节点返回原文（含 LaTeX） |
| "Hinton 怎么看 X / 会怎么选" | **心智** | 匹配 `expert-mind/judgments.md`，返回判断 + 推理链 + `grounded_in` |
| "Hinton 为什么认为 X / 依据" | **融合** ⭐ | 镜片 → judgment → `grounded_in` 节点全文 → 综合「立场 + 依据 + 替代 + 局限」 |

### 融合模式回答示例（「纯符号规则引擎做常识推理」）

- **[立场]** 大概率反对——符号 localist 表示无相似度结构、无指数级容量 *(judg-hinton-distributed-vs-symbolic)*
- **[理论依据]** 分布式表示编码 $O(2^d)$ 概念支持类比泛化 *(def-hinton2014-distributed-representation)*；反传让其可学 *(thm-rumelhart1986-backprop-chain-rule)*
- **[替代方案]** 深度神经网络学分布式向量表示 + 端到端学习
- **[诚实边界]** 符号 AI 在封闭世界确定性推理（定理证明）上仍有价值，Hinton 反对的是"纯符号、无学习"

> 加载原则：judgment 的 `grounded_in` 节点 ID 按需加载，不全量读。

---

## 知识节点索引（9 个，详见 `wiki/index.md`）

- **Theorem（2）**：`thm-rumelhart1986-backprop-chain-rule`（反传）、`thm-ackley1985-boltzmann-learning`（Boltzmann 学习）
- **Method（4）**：`meth-hinton2006-contrastive-divergence`（CD）、`meth-hinton2002-wake-sleep`、`meth-hinton2008-tsne`、`meth-sabour2017-capsule-routing`
- **Definition（1）**：`def-hinton2014-distributed-representation`（分布式表示）
- **Experiment（1）**：`exp-hinton2012-dropout`
- **Insight（1）**：`ins-hinton2007-deep-vs-breadth`

---

## 诚实边界

**已覆盖**：反传链式法则、Boltzmann 学习规则、CD/Wake-Sleep 生成式训练、t-SNE、Dropout、Capsule 路由、分布式表示理论、深度优于宽度。

**未覆盖**：前向-前向算法（FF, 2022）、知识蒸馏、矩阵胶囊等较新方向（V1 可扩展）。

**有争议**：Capsule 大规模未超 CNN（仍开放）；"理解即生成"是哲学立场，难证伪；深度优于宽度是渐近论证，非对所有任务严格成立。

---

## 维护

- **Lint**：`python3 pipeline/state/lint_d7.py --target-skill-root .` 验证硬门③（无孤儿 judgment）+ 硬门①（mental_model 3 重必 grounded_in）
- **查询入口**：`dag/dag-index.json`（知识）/ `expert-mind/judgments.md`（心智）
