# Surrogate Feature（Feature CP 的 non-conformity score 机制）

> 节点 ID: `meth-teng2023-surrogate-feature` | type: method | 来源: `src-teng2023-feature-cp`

## 问题

标准 non-conformity score 形如 $s(X_i, Y_i, \hat{\mu}) = \|Y_i - \hat{\mu}(X_i)\|$，需要 ground truth $Y_i$。但在**特征空间**做 CP 时，特征空间没有 ground truth（特征的"真值"未定义）。

## 滕佳烨的解法：surrogate feature

用 **surrogate feature（代理特征）** 替代 ground truth 项。给定输出 $Y_i$，定义其特征空间的代理为：

$$
\hat{v}_i^{\text{surrogate}} \in \arg\min_{v} \|v - \hat{f}(X_i)\| \quad \text{s.t.} \quad \hat{g}(v) = Y_i
$$

即在满足 $\hat{g}(v) = Y_i$ 的特征中，选最接近 $\hat{f}(X_i)$ 的——作为 ground truth 在特征空间的代理。

Feature-space non-conformity score：

$$
s^{\text{feat}}(X_i, Y_i, \hat{\mu}) = \|\hat{v}_i^{\text{surrogate}} - \hat{f}(X_i)\|
$$

## Band Estimation / Band Detection（特征 band 转输出 band）

- **Band Estimation**：计算 feature-space confidence band 映射到 output space 的上界
- **Band Detection**：判定给定 output 响应是否落在 band 内（无需显式构造整个 band）

## 为何有效

surrogate feature 让 Feature CP 在"无 feature ground truth"的困难下仍能计算 score，且：
- coverage 仍由 exchangeability 保证（`thm-split-cp-coverage`）
- 在 cubic conditions 下 band 更短（`thm-teng2023-feature-cp-advantage`）

## 局限（被 FFCP 解决）

求解 surrogate feature 涉及 LiPRA（非线性反向映射）操作，**计算昂贵**。FFCP（`meth-teng2025-ffcp-score`）用 Taylor 展开近似，50x 加速。

## 在滕佳烨工作中的地位

这是 Feature CP 的**技术核心**——把"在 feature space 做 CP"从理念变为可实现算法。体现了滕佳烨"理论 + 工程并重"——不仅有定理，更有可用的 score。
