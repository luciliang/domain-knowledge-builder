---
id: mm-hinton-depth-beats-breadth
type: mental_model
label: 深度优于宽度
statement: "表示复杂概念，深层逐层抽象所需的参数量指数级少于浅而宽的网络——深度本身就是归纳偏置"
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "2006 Science 论文用 RBM 逐层预训练证明深自编码器降维优于浅网络"
      - "2006 Neural Computation DBN 论文把'深度 + 逐层预训练'作为复兴深度学习的关键组合"
      - "2012 AlexNet（Hinton 团队）以深度 + Dropout 赢 ImageNet，实证'深优于宽'"
      - "Capsule 保留多层路由，延续'层级组合 = 理解'信念"
  generative:
    pass: true
    predicts: "对任何'用更宽的浅层网络替代深层网络'的提案，Hinton 持怀疑态度，倾向加深度而非加宽度"
  exclusive:
    pass: true
    vs: "SVM / 核方法 / 浅层宽网络派：认为浅层 + 复杂核足以表达任意函数"
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
  - node: exp-hinton2012-dropout
    role: supports
    quote: "Dropout 是让更深的网络不过拟合的配套正则化，使'深优于宽'在 2012 ImageNet 上兑现"
confidence: high
provenance:
  sources:
    - src-hinton-science-2006
    - src-hinton-nc-2006
    - src-hinton-krizhevsky-2012
---

# 深度优于宽度

## 核心思想

**"深度 = 逐层重新表示，宽度 = 线性堆砌"**。Hinton 把 1990s 神经网络寒冬的失败归因于"网络太浅 + 没好的逐层训练法"，而非联结主义本身错。他预言并推动了 2012 年 AlexNet 的成功——深度 + ReLU + GPU + Dropout 的组合。

## 跨场景证据

1. **理论直觉**：组合函数在深层网络参数量指数级更省（Telgarsky 等严格化）
2. **2006 复兴**：DBN + CD 逐层预训练让深网络第一次训得动
3. **2012 兑现**：AlexNet（Hinton 学生 Krizhevsky）以深 + Dropout 赢 ImageNet
4. **延续**：Capsule 保留多层路由，不信"一层足够"

## 局限

- 极深网络（>100 层）出现梯度消失/退化，催生 ResNet 残差连接（Hinton 的工作启发了这条线）
- "深优于宽"是经验 + 渐近论证，并非对所有任务严格成立
