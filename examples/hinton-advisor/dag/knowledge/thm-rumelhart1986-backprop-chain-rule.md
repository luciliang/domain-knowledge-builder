---
id: thm-rumelhart1986-backprop-chain-rule
type: theorem
label: Backpropagation Chain Rule (Rumelhart-Hinton-Williams 1986)
source: rumelhart1986
section: Section 2 (Learning Internal Representations)
tokens: 1100
created: 2026-06-28
generated_by_step: S2
run_id: golden-hinton-advisor-0001
source_span:
  file: rumelhart1986-learning-representations.pdf
  start_line: 1
  end_line: 1
  page: "533-536"
---

## 精确表述

设多层前馈网络中，误差函数 $E$ 关于输出层激活的偏导已知。对任意隐藏层权重 $w_{ij}^{(l)}$，其梯度可通过链式法则递推计算：

$$\frac{\partial E}{\partial w_{ij}^{(l)}} = \delta_j^{(l)} \cdot o_i^{(l-1)}$$

其中误差信号 $\delta$ 反向递推：

$$\delta_j^{(l)} = \varphi'(z_j^{(l)}) \sum_k w_{jk}^{(l+1)} \, \delta_k^{(l+1)}$$

即隐藏层的误差信号 = 下一层误差信号的加权和 × 本层激活的导数。梯度下降更新：

$$w_{ij}^{(l)} \leftarrow w_{ij}^{(l)} - \epsilon \, \frac{\partial E}{\partial w_{ij}^{(l)}}$$

## 适用条件

1. 网络中每个可微的非线性激活 $\varphi(\cdot)$ 的导数存在且可计算
2. 误差函数 $E$ 关于网络输出可微
3. 误差信号从输出层逐层向输入层反向传播（故名 backpropagation）

## 直觉解释

链式法则本身是微积分的初等结论，但 1986 年的关键贡献是证明**反向递推可高效计算所有隐藏层的梯度**——前向算一遍激活，反向算一遍误差信号，每个权重梯度即可在 $O(E)$（E 为边数）时间内得到，无需对每条权重独立做数值差分。这使深度网络训练在计算上变得可行。

## 与其他知识的关系

→ def-hinton2014-distributed-representation（反向传播是学习分布式表示的核心机制）
→ ins-hinton2007-deep-vs-breadth（反向传播使深层组合特征可学，是"深优于宽"的技术前提）
→ thm-ackley1985-boltzmann-learning（Boltzmann 机学习规则也依赖梯度方向，但用统计采样估计）
→ meth-hinton2006-contrastive-divergence（CD 是避开完整梯度计算的近似，用于训练深度信念网）

## 来源引用

Rumelhart, Hinton & Williams (1986), "Learning representations by back-propagating errors", *Nature* 323, pp. 533-536, Section 2。
