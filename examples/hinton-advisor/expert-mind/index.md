# Hinton 专家心智导航

> 本文件是 `expert-mind/` 的纯导航层（不存数据，只引用 ID）。
> 心智元素定义见 `mental-models.md`，判断见 `judgments.md`。

---

## 心智元素（4 个）

### mental_model（3 个，3 重验证全过）

| ID | 标签 | 一句话 | grounded_in 核心节点 |
|----|------|--------|---------------------|
| `mm-hinton-distributed-representation` | 分布式表示优于符号表示 | 概念是高维空间联合激活模式，非离散符号 | `def-hinton2014-distributed-representation`, `thm-rumelhart1986-backprop-chain-rule`, `meth-sabour2017-capsule-routing` |
| `mm-hinton-depth-beats-breadth` | 深度优于宽度 | 深层逐层抽象参数量指数级少于浅而宽网络 | `ins-hinton2007-deep-vs-breadth`, `thm-rumelhart1986-backprop-chain-rule`, `meth-hinton2006-contrastive-divergence` |
| `mm-hinton-generative-energy-model` | 理解即生成 | 真正理解 = 能自由运行复现统计，生成式是关键 | `thm-ackley1985-boltzmann-learning`, `meth-hinton2002-wake-sleep`, `meth-hinton2006-contrastive-divergence` |

### anti_pattern（1 个）

| ID | 标签 | 反对什么 | refutes 节点 |
|----|------|----------|-------------|
| `ap-hinton-against-symbolic-ai` | 反对纯符号 AI | GOFAI 离散符号 + 手写规则 | `def-hinton2014-distributed-representation`（role: refutes） |

---

## 判断（6 个，紧耦合枢纽）

回答「Hinton 怎么看 X」的核心载体。每条 `derived_from` 继承心智元素验证，`grounded_in` 挂知识节点。

| ID | 标签 | 触发问题 | derived_from |
|----|------|---------|--------------|
| `judg-hinton-distributed-vs-symbolic` | 分布式 vs 符号 | 分布式表示和符号表示哪个更好 | `mm-hinton-distributed-representation` |
| `judg-hinton-depth-over-width` | 深度优于宽度 | 深度网络为什么比浅层宽网络好 | `mm-hinton-depth-beats-breadth` |
| `judg-hinton-prefers-generative` | 偏好生成式 | Hinton 为什么偏好生成式模型 | `mm-hinton-generative-energy-model` |
| `judg-hinton-dropout-intuition` | Dropout 直觉 | Dropout 的直觉是什么 | `mm-hinton-distributed-representation` |
| `judg-hinton-capsule-over-pooling` | Capsule 替代池化 | Capsule 为什么替代池化 | `mm-hinton-distributed-representation` |
| `judg-hinton-backprop-legacy` | 反传历史地位 | Hinton 怎么评价反向传播 | `mm-hinton-distributed-representation` |

---

## 查询路由

- 问「Hinton 怎么看 X」→ 查 `judgments.md` 找匹配 trigger 的 judgment
- 问「Hinton 为什么认为 X / X 的依据」→ 融合查询：judgment + `grounded_in` 节点全文
- 无现成 judgment → 加载心智元素镜片推断，标注「推断·非原话」
