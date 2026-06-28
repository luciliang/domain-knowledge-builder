---
id: meth-sem-crc
type: method
label: sem-CRC (Semantic Conformal Risk Control)
source: teneggi2025
section: Section 3, Eq (7)-(9), (Psem)
tokens: 1500
created: 2026-06-23
---

## 精确表述

sem-CRC extends K-CRC to instance-dependent memberships $s(y) \in [K]^d$ by leveraging foundational segmentation models. Let $s : \mathcal{Y} \to [K]^d$ be a fixed segmentation model such that, for a vector $\lambda_{\text{sem}} \in \mathbb{R}_{\geq 0}^K$, the family of nested set predictors $\{g_{\lambda_{\text{sem}}}\}$ is:

$$g_{\lambda_{\text{sem}}}(y)_j = [\hat{q}_\alpha(y)_j - \lambda_{s(y)_j}, \hat{q}_{1-\alpha}(y)_j + \lambda_{s(y)_j}].$$

Differently from $g_\lambda(y)$ in K-CRC (Eq 5), the same pixel $j$ may receive different assignments in different scans depending on the measurement $y$.

The mean interval length becomes:

$$\bar{I}_{\lambda_{\text{sem}}}(y) = \frac{1}{d}\sum_{j \in [d]}(\hat{q}_{1-\alpha}(y)_j - \hat{q}_\alpha(y)_j) + \frac{1}{d}\sum_{k \in [K]} |S_k(y)| \lambda_k,$$

where $S_k(y) = \{j \in [d] : s(y)_j = k\}$ is the set of voxels belonging to organ $k$ for observation $y$.

The anchor point is found by solving the semantic optimization problem (Psem):

$$\tilde{\lambda}_{\text{sem}} = \arg\min_{\lambda_{\text{sem}} \in \mathbb{R}_{\geq 0}^K} \sum_{k \in [K]} \mathbb{E}_Y[|S_k(Y)|] \lambda_k \quad \text{s.t.} \quad \hat{\ell}_\gamma^{\text{opt}}(\lambda_{\text{sem}}) \leq \epsilon.$$

Then the final parameter is:

$$\hat{\lambda}_{\text{sem}} = \inf\left\{\lambda_{\text{sem}} \in \tilde{\lambda}_{\text{sem}} + \omega\mathbf{1}_K : \frac{n_{\text{cal}}}{n_{\text{cal}}+1}\hat{\ell}_{\text{cal}}^{01}(\lambda_{\text{sem}}) + \frac{1}{n_{\text{cal}}+1} \leq \epsilon\right\}.$$

**Key innovation**: The partition depends on the measurement $y$ (via segmentation model $s$), decoupling interval length optimization from the pixel domain. The optimization objective must be taken in expectation over $Y$ since $|S_k(y)|$ now depends on $y$.

sem-CRC 通过分割模型将像素按语义结构（器官）分组，每个器官有自己的不确定性参数 $\lambda_k$。这使不确定性区间能够适应不同患者的解剖结构差异。

## 适用条件

- 固定的分割模型 $s : \mathcal{Y} \to [K]^d$（不随校准数据变化）
- 校准集需分成 $S_{\text{opt}}$（解 Psem）和 $S_{\text{ecal}}$（找 $\hat{\lambda}_{\text{sem}}$）
- 推理时必须使用与校准时相同的分割模型
- 分割模型的质量影响结果，但其校准不在本方法范围内

## 直觉解释

不同患者的器官大小、形状、位置差异很大。固定分组（K-CRC）会让一些本不需要大区间的像素承担过多不确定性。sem-CRC 用分割模型识别每个患者的解剖结构，为每个器官单独调整不确定性参数，从而产生更紧的区间。同时 $\hat{\lambda}_{\text{sem}}$ 直接揭示哪些器官的不确定性更高，具有临床可解释性。

## 与其他知识的关系

← meth-k-crc（sem-CRC 扩展 K-CRC 到语义分组）
→ thm-sem-crc-validity（Proposition 1 保证 sem-CRC 的风险控制）
→ meth-sem-crc-per-organ（sem-CRC 可特化为逐器官风险控制）
applies_to → exp-ct-denoising-reconstruction（应用于 CT 去噪和重建）
depends_on → def-semantic-uq（理解 sem-CRC 需先理解语义不确定性的概念）

## 来源引用

- Teneggi et al. 2025, Section 3, Equations (7)-(9), (Psem)
- Code: https://github.com/Sulam-Group/semantic_uq
