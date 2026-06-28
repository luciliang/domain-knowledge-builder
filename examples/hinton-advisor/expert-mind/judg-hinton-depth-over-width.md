---
id: judg-hinton-depth-over-width
type: judgment
label: 深度优于宽度，是深度学习的根本归纳偏置
status: verified
trigger: "深度网络为什么比浅层宽网络好 / Hinton 怎么看深度"
derived_from: mm-hinton-depth-beats-breadth
judgment: "深度本身是归纳偏置——表示复杂概念，深层逐层抽象所需参数量指数级少于浅而宽的网络"
reasoning: "深层网络通过逐层重新表示（each layer re-represent）把简单特征组合成高层特征；某些函数族用深度 k 网络需 O(k) 单元，用深度 log k 网络需 O(2^k) 单元。Hinton 把 1990s 神经网络寒冬归因于'网络太浅 + 没好的逐层训练法'，而非联结主义本身错——这正是他推动 DBN 预训练和 2012 AlexNet 的动机。"
grounded_in:
  - node: ins-hinton2007-deep-vs-breadth
    role: supports
    quote: "某些函数族用深度 k 网络需 O(k) 单元，用深度 log k 网络需 O(2^k) 单元"
  - node: thm-rumelhart1986-backprop-chain-rule
    role: supports
    quote: "反传使深层组合特征可学，是'深优于宽'的技术前提"
  - node: meth-hinton2006-contrastive-divergence
    role: supports
    quote: "CD 逐层预训练是 2006-2012 让深层网络训得动的关键工具"
counter_evidence:
  - node: exp-hinton2012-dropout
    role: context
    note: "极深网络（>100 层）出现梯度消失/退化，催生 ResNet 残差连接；'深优于宽'是经验 + 渐近论证，非对所有任务严格成立"
confidence: high
provenance:
  sources:
    - src-hinton-science-2006
    - src-hinton-nc-2006
    - src-hinton-krizhevsky-2012
---

# 深度优于宽度，是深度学习的根本归纳偏置

## 判断背景

「为什么用深层网络而非浅而宽的网络」是 Hinton 在 2006-2012 深度学习复兴期反复论证的核心命题。

## 判断立场

**深度本身是归纳偏置**——深比宽更值钱。

## 推理链

1. **逐层抽象**：深层每层重新表示，浅层只能线性堆砌
2. **参数效率**：组合函数在深层参数量指数级更省
3. **寒冬归因**：1990s 失败 = 太浅 + 无逐层训练法，非联结主义错
4. **兑现**：2006 DBN 预训练 + 2012 AlexNet（深 + Dropout）实证深优于宽

## 诚实边界

- 极深网络梯度消失，需 ResNet 残差连接（Hinton 工作启发了这条线）
- "深优于宽"是渐近论证，非对所有任务严格成立
