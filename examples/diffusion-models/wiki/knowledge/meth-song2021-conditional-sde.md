---
id: meth-song2021-conditional-sde
type: method
label: Conditional Reverse-Time SDE for Controllable Generation
source: song2021
section: Section 5
tokens: 1100
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 2210
  end_line: 2276
  page: "Unknown"
---

## 精确表述

Score-SDE 框架的条件生成能力：给定前向 SDE（Eq. 5），若 $p_{t}(\mathbf{y}\mid\mathbf{x}(t))$ 已知，可通过求解如下**条件 reverse-time SDE**（Eq. 14）从 $p_{0}(\mathbf{x}(0)\mid\mathbf{y})$ 采样：

$$\mathrm{d}\mathbf{x}=\big\{\mathbf{f}(\mathbf{x},t)-g(t)^{2}\,[\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})+\nabla_{\mathbf{x}}\log p_{t}(\mathbf{y}\mid\mathbf{x})]\big\}\,\mathrm{d}t+g(t)\,\mathrm{d}\bar{\mathbf{w}}$$

相比无条件 reverse-time SDE（Eq. 6），仅多了一项 $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{y}\mid\mathbf{x})$——前向过程的梯度。关键优势：**条件 score 可由无条件 score 直接估计**，无需重训练生成模型。只需估计 $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{y}\mid\mathbf{x})$（可训练单独的时间依赖分类器，或用启发式/领域知识估计）。

论文演示三类应用：类条件生成（训练时间依赖分类器 $p_{t}(\mathbf{y}\mid\mathbf{x}(t))$）、图像补全（imputation，已知子集 $\Omega(\mathbf{y})$）、着色（colorization，经正交变换解耦后做 imputation）。

## 适用条件

- 需估计 $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{y}\mid\mathbf{x})$：分类器法需训练时间依赖分类器；inverse problem 可用启发式或 Appendix I.4 的免辅助模型方法。
- 无条件 score 模型已训练好（生成主干不变）。

## 直觉解释

条件采样只需在 reverse-time SDE 的"去噪力"上再加一个"指向满足条件 $\mathbf{y}$ 的力"。因为这个额外的力只用前向过程（已知）和条件模型，所以同一个无条件生成模型就能做条件生成、补全、着色——这是连续框架独有的灵活性。

## 与其他知识的关系

← 是 → thm-song2021-reverse-time-sde 的条件推广（多一项 $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{y}\mid\mathbf{x})$）。
← 复用 → meth-song2021-score-based-training 训练的无条件 score。
→ **跨源**：DDPM（ho2020）为纯无条件生成，不含条件/可控生成能力；本方法是 Score-SDE 相对 DDPM 的显著能力扩展。

## 来源引用

Song et al. 2021, Section 5, Eq. (14)；Appendix I。full-text.txt lines 2210-2276。
