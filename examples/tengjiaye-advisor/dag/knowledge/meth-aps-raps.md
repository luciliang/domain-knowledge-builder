# APS / RAPS（分类任务的 non-conformity score）

> 节点 ID: `meth-aps-raps` | type: method | 来源: `src-angelopoulos-bates-2022`

## 背景

分类任务中，预测集应是 label 集合的子集。non-conformity score 决定预测集的大小与结构。

## APS（Adaptive Prediction Sets）

Romano et al. (2020)。按模型预测概率对 label 降序排列，cumulatively 累加概率直到超过阈值，所得 label 子集为预测集。

- **优点**：自适应——难样本给大预测集，简单样本给小预测集
- **缺点**：可能包含大量低概率"尾巴"label，预测集偏大

## RAPS（Regularized APS）

Angelopoulos et al. (2020)。在 APS 基础上加正则化项，惩罚"尾巴"label 的数量，缩短预测集同时保持 coverage。

$$
s_{\text{RAPS}}(x, y) = \text{rank}(y) + \lambda \cdot (\text{rank}(y) - k)^+
$$

- 在保证 $P(Y_{n+1} \in \mathcal{C}_{1-\alpha}) \ge 1-\alpha$ 下，预测集更短

## 在滕佳烨工作中的地位

- Feature CP 论文把 feature-level 技术部署到 RAPS（FFRAPS），证明 feature 思路的通用性
- APS/RAPS 是滕佳烨改进 non-conformity score 的"基准对手"——他证明 Feature CP / FFCP 在效率上优于 vanilla（即基于 APS/RAPS 的 output-space CP）

## 局限

- 仅适用分类（regression 用 CQR 等）
- 仍是 output-space 方法，未利用语义特征空间——这正是 Feature CP 的突破口
