---
id: meth-sabour2017-capsule-routing
type: method
label: Capsule Networks with Dynamic Routing (Sabour, Frosst, Hinton 2017)
source: sabour2017
section: Section 2-3
tokens: 1150
created: 2026-06-28
generated_by_step: S2
run_id: golden-hinton-advisor-0001
source_span:
  file: sabour2017-capsules.pdf
  start_line: 1
  end_line: 1
  page: "3856-3866"
---

## 精确表述

传统 CNN 的标量神经元无法编码"实例化参数"（pose, scale, rotation）。Capsule 输出一个**向量** $\mathbf{u}_i$，其长度表"实体存在的概率"，方向表"实例化参数"。

**动态路由（Dynamic Routing-by-Agreement）**：低层 capsule $\mathbf{u}_i$ 经变换 $\hat{\mathbf{u}}_{j|i} = W_{ij}\mathbf{u}_i$ 后，按耦合系数 $c_{ij}$ 加权求和到高层 capsule $\mathbf{s}_j = \sum_i c_{ij}\hat{\mathbf{u}}_{j|i}$，再经 squash 非线性 $\mathbf{v}_j = \frac{\|\mathbf{s}_j\|^2}{1+\|\mathbf{s}_j\|^2}\frac{\mathbf{s}_j}{\|\mathbf{s}_j\|}$。

耦合系数由**迭代一致协议**更新：

$$c_{ij} = \text{softmax}_j(b_{ij}), \quad b_{ij} \leftarrow b_{ij} + \hat{\mathbf{u}}_{j|i} \cdot \mathbf{v}_j$$

即"预测与高层一致的低层 capsule 获得更高权重"——Hinton 称为 routing-by-agreement。

## 适用条件

1. 迭代轮数 $r$ 取小值（论文用 $r=3$，过大易过拟合训练分布）
2. 主要在 MNIST / smallNORB 等结构规整的小图像上验证
3. 替代最大池化（max-p pooling 丢弃位置信息，与 capsule"保留实例化参数"理念冲突）

## 直觉解释

Hinton 长期批评 max-pooling："它扔掉了'东西在哪里'，只保留'最强烈的特征是什么'——这对视觉是不自然的"。Capsule 把"神经元激活标量"升级为"向量激活 + 一致路由"：低层零件（眼、鼻）预测出的高层整体（脸）若与高层 capsule 自我估计一致，路由加强；否则削弱。这是"层级化组合 = 视觉理解"信念在架构层面的体现——也是 Hinton 对"分布式表示应表达结构"的一贯追求。

## 与其他知识的关系

→ def-hinton2014-distributed-representation（capsule 向量激活是分布式表示的强化版：长度=存在性，方向=参数）
→ ins-hinton2007-deep-vs-breadth（capsule 的层级路由体现"深度 = 层级组合"理念）
→ meth-hinton2008-tsne（Hinton 体系内一致的"理解 = 学到结构化表示"哲学，从 t-SNE 可视化到 capsule 架构）

## 来源引用

Sabour, Frosst & Hinton (2017), "Dynamic Routing Between Capsules", *NeurIPS 2017*, pp. 3856-3866, Sections 2-3。
