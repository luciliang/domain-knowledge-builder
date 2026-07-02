---
id: thm-sem-crc-validity
type: theorem
label: "Proposition 1: Validity of sem-CRC"
source: teneggi2025
section: Section 3, Proposition 1
tokens: 1100
created: 2026-06-23
---

## 精确表述

**Proposition 1.** For a risk tolerance $\epsilon > 0$, segmentation model $s : \mathcal{Y} \to [K]^d$, anchor point $\tilde{\lambda}_{\text{sem}} \in \mathbb{R}_{\geq 0}^K$, and exchangeable calibration and test points $S_{\text{cal}} = \{(X^{(i)}, Y^{(i)})\}_{i=1}^{n_{\text{cal}}}$, $(X, Y)$, the choice of $\hat{\lambda}_{\text{sem}}$ as in (9) provides risk control, i.e.,

$$\mathbb{E}[\ell_{01}(g_{\hat{\lambda}_{\text{sem}}}(Y), X)] \leq \epsilon.$$

**Proof.** Let $\lambda_{\text{sem}}(\omega) = \tilde{\lambda}_{\text{sem}} + \omega\mathbf{1}_K$, $\omega \in \mathbb{R}$, and note that $\ell_{01}(g_{\lambda_{\text{sem}}(\omega)}(y), x)$ is bounded by 1 and monotonically non-increasing in $\omega$. Since $s$ is fixed, the random functions $L_i(\omega) = \ell_{01}(g_{\lambda_{\text{sem}}(\omega)}(Y^{(i)}), X^{(i)})$ and $L(\omega) = \ell_{01}(g_{\lambda_{\text{sem}}(\omega)}(Y), X)$ are exchangeable. The result then follows by applying [Angelopoulos et al. 2024, Theorem 1] to $\omega$.

**命题 1.** 对于风险容差 $\epsilon > 0$、分割模型 $s$、锚点 $\tilde{\lambda}_{\text{sem}}$，以及可交换的校准集和测试点，按式 (9) 选择的 $\hat{\lambda}_{\text{sem}}$ 提供风险控制，即期望损失不超过 $\epsilon$。

## 适用条件

- 分割模型 $s$ 必须是**固定的**（不随校准数据变化）——这是保证可交换性的关键
- 校准数据 $(X^{(i)}, Y^{(i)})$ 和测试数据 $(X, Y)$ 必须可交换
- 损失函数 $\ell_{01}$ 关于 $\omega$ 有界且单调非递增
- 锚点 $\tilde{\lambda}_{\text{sem}}$ 是从优化集 $S_{\text{opt}}$ 求得的（与 $S_{\text{ecal}}$ 独立）

## 直觉解释

证明的关键在于：虽然分组依赖 $y$（通过 $s(y)$），但由于 $s$ 是固定的（不依赖于校准数据），复合函数 $L_i(\omega)$ 和 $L(\omega)$ 仍然保持可交换性。因此可以直接应用 CRC 的原始定理（Angelopoulos et al. 2024, Theorem 1）到标量参数 $\omega$ 上。换言之，语义分组的实例依赖性不破坏保证，因为分割模型只是一个固定的变换。

## 与其他知识的关系

← def-conformal-coverage（基于 CRC 的基本风险控制保证）
← def-teneggi2025-crc（建立在 CRC 框架之上）
guarantees → meth-sem-crc（保证 sem-CRC 方法在期望意义下控制风险）
→ meth-sem-crc-per-organ（逐器官版本通过将此命题应用到每个维度得到）

## 来源引用

- Teneggi et al. 2025, Section 3, Proposition 1, Equation (10)
- Proof applies: Angelopoulos et al. 2024 (ICLR), Theorem 1
