# Hinton 专家心智模型（导航）

> 本文件是 Hinton 心智元素的**导航与说明**。每个心智元素的 frontmatter 数据定义在独立文件中（见下表），供 `lint_d7.py` 扫描校验。
> 完整导航见 `index.md`。

---

## 心智元素清单（4 个）

### mental_model（3 个，3 重验证全过）

| ID | 文件 | 标签 | 一句话 |
|----|------|------|--------|
| `mm-hinton-distributed-representation` | `mm-hinton-distributed-representation.md` | 分布式表示优于符号表示 | 概念是高维空间联合激活模式，非离散符号 |
| `mm-hinton-depth-beats-breadth` | `mm-hinton-depth-beats-breadth.md` | 深度优于宽度 | 深层逐层抽象参数量指数级少于浅而宽网络 |
| `mm-hinton-generative-energy-model` | `mm-hinton-generative-energy-model.md` | 理解即生成 | 真正理解 = 能自由运行复现统计，生成式是关键 |

### anti_pattern（1 个）

| ID | 文件 | 标签 | 反对什么 |
|----|------|------|----------|
| `ap-hinton-against-symbolic-ai` | `ap-hinton-against-symbolic-ai.md` | 反对纯符号 AI | GOFAI 离散符号 + 手写规则 |

---

## 主线叙事

Hinton 的四条信念互相支撑：

1. **分布式表示**是根基（`mm-hinton-distributed-representation`）——所有工作都围绕"学出好的分布式表示"
2. **深度优于宽度**是架构选择（`mm-hinton-depth-beats-breadth`）——分布式表示在深度方向逐层组合
3. **理解即生成**是学习目标（`mm-hinton-generative-energy-model`）——用生成式能力衡量是否真理解
4. **反对纯符号**是对立面（`ap-hinton-against-symbolic-ai`）——分布式表示在四维全胜符号 localist

详见各独立元素文件。
