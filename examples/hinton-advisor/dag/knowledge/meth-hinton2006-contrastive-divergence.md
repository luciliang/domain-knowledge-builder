---
id: meth-hinton2006-contrastive-divergence
type: method
label: Contrastive Divergence (Hinton 2002/2006)
source: hinton2006
section: Section 3 (Training Deep Belief Nets)
tokens: 1000
created: 2026-06-28
generated_by_step: S2
run_id: golden-hinton-advisor-0001
source_span:
  file: hinton2006-fast-learning.pdf
  start_line: 1
  end_line: 1
  page: "1527-1554"
---

## 精确表述

完整 Boltzmann 学习规则需网络自由运行到热平衡以估计 $\langle s_i s_j \rangle_{\text{model}}$，计算上不可行。**对比散度（Contrastive Divergence, CD-k）** 用 $k$ 步（通常 $k=1$）Gibbs 采样的重构近似负相位：

1. 用真实数据 $\mathbf{v}_0$ 初始化可见层
2. 交替采样 $k$ 步：$\mathbf{h}_0 \sim P(\mathbf{h}|\mathbf{v}_0)$, $\mathbf{v}_1 \sim P(\mathbf{v}|\mathbf{h}_0)$, $\mathbf{h}_1 \sim P(\mathbf{h}|\mathbf{v}_1)$
3. 权重更新用 1 步重构替代平衡期望：

$$\Delta w_{ij} = \epsilon \left( \langle v_i h_j \rangle_{\mathbf{v}_0} - \langle v_i h_j \rangle_{\mathbf{v}_1} \right)$$

**CD-1** 即 $k=1$：只用一次前向-反向-前向，几乎不收敛就更新。

## 适用条件

1. 限制型 Boltzmann 机（RBM）——可见层与隐藏层间无层内连接（保证条件分布可解析采样）
2. $k$ 取小值（1-5）——精度让位于速度的工程取舍
3. 作为深度信念网（DBN）逐层预训练的 building block

## 直觉解释

Hinton 的关键洞察：**"不需要等到模型完全做梦，只要让重构偏离数据一步即可"**。完整 CD 是最小化 $\text{KL}(\text{data} \| \text{model})$，而 CD-1 实际最小化的是 $\text{KL}(\text{data} \| \text{model}) - \text{KL}(\text{reconstruction} \| \text{model})$——比真目标少减一项，但在实践中给出与完整学习几乎一样好的方向，速度却快几个量级。这是 2006 年深度学习复兴的关键催化剂：它让训练深层生成式模型第一次变得可行。

## 与其他知识的关系

→ thm-ackley1985-boltzmann-learning（CD 是 Boltzmann 学习规则的快速近似）
→ meth-hinton2002-wake-sleep（Wake-Sleep 用别的方式（识别模型）绕开 Gibbs，CD 用截断 Gibbs，殊途同归）
→ ins-hinton2007-deep-vs-breadth（CD 逐层预训练 + 反向传播微调，是 2006-2012 深度网络能学起来的组合拳）

## 来源引用

Hinton, Osindero & Teh (2006), "A Fast Learning Algorithm for Deep Belief Nets", *Neural Computation* 18(7), pp. 1527-1554。
Hinton (2002), "Training Products of Experts by Minimizing Contrastive Divergence", *Neural Computation* 14(8)。
