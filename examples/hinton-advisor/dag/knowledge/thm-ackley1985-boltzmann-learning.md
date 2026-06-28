---
id: thm-ackley1985-boltzmann-learning
type: theorem
label: Boltzmann Machine Learning Rule (Ackley-Hinton-Sejnowski 1985)
source: ackley1985
section: Section 3 (Learning in Boltzmann Machines)
tokens: 1300
created: 2026-06-28
generated_by_step: S2
run_id: golden-hinton-advisor-0001
source_span:
  file: ackley1985-boltzmann-machine.pdf
  start_line: 1
  end_line: 1
  page: "147-169"
---

## 精确表述

Boltzmann 机是带隐藏单元的能量模型，状态向量 $\mathbf{v}, \mathbf{h}$ 的联合分布：

$$P(\mathbf{v}, \mathbf{h}) = \frac{e^{-E(\mathbf{v}, \mathbf{h})}}{Z}, \quad E(\mathbf{v}, \mathbf{h}) = -\sum_i b_i s_i - \sum_{i<j} w_{ij} s_i s_j$$

对数似然 $\mathcal{L} = \log P(\mathbf{v})$ 关于权重 $w_{ij}$ 的梯度给出**学习规则**：

$$\Delta w_{ij} = \epsilon \left( \langle s_i s_j \rangle_{\text{data}} - \langle s_i s_j \rangle_{\text{model}} \right)$$

- $\langle \cdot \rangle_{\text{data}}$：数据钳制可见层后，隐藏单元在平衡分布上的期望（**正相位**，clamped / wake）
- $\langle \cdot \rangle_{\text{model}}$：网络自由运行（unclamped）达到平衡分布时的期望（**负相位**，free / sleep）

直觉表述：**"把数据里同时激活的连起来，把模型自己臆想的激活拆开"**——网络通过减小数据分布与模型分布的 KL 散度来逼近真实分布。

## 适用条件

1. 单元状态为二值 $\{0,1\}$（或 $\{-1,+1\}$），激活服从 Gibbs 分布
2. 网络通过 Gibbs 采样达到热平衡（实际中难以精确达到，故需 CD 近似，见 `meth-hinton2006-contrastive-divergence`）
3. 对称连接 $w_{ij} = w_{ji}$（保证能量函数良定义、收敛到 Boltzmann 分布）

## 直觉解释

这是 Hinton 早期"生成式学习"信念的数学基石。学习发生在两个相位：数据相位"看见"真实统计，模型相位"梦见"自由统计，二者之差就是修正方向。本质上是在最小化 $\text{KL}(\text{data} \| \text{model})$。它确立了**"理解 = 生成"**的范式：模型真正掌握了一组数据，当且仅当它能在自由运行时复现同样的统计。

## 与其他知识的关系

→ meth-hinton2002-wake-sleep（Wake-Sleep 是该规则的分层近似：用识别网络估计后验，避免漫长的 Gibbs 采样）
→ meth-hinton2006-contrastive-divergence（CD 用 1 步 Gibbs 采样近似负相位，是 Boltzmann 学习的实用化突破）
→ def-hinton2014-distributed-representation（隐藏单元的分布式激活即"内部表示"，由该规则学习）

## 来源引用

Ackley, Hinton & Sejnowski (1985), "A Learning Algorithm for Boltzmann Machines", *Cognitive Science* 9(1), pp. 147-169, Section 3。
