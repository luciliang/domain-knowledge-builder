# FFCP Non-conformity Score（Fast Feature CP）

> 节点 ID: `meth-teng2025-ffcp-score` | type: method | 来源: `src-teng2025-fast-feature-cp`

## 问题

Feature CP（`meth-teng2023-surrogate-feature`）的 Band Estimation 依赖 LiPRA 非线性操作，**计算昂贵**，限制实用性。

## FFCP 的核心思想

用 **Taylor 展开**近似 FCP 的非线性 band 变换，得到一个简单可算的 non-conformity score。

## FFCP non-conformity score

设 $\hat{\mu} = \hat{g} \circ \hat{h}$（$\hat{h}$ 特征层，$\hat{g}$ 预测头），$\hat{v}_i = \hat{h}(X_i)$ 为特征，则

$$
\boxed{\;\;s_{\text{ff}}(X, Y, \hat{g} \circ \hat{h}) = \frac{|Y - \hat{g} \circ \hat{h}(X)|}{\|\nabla \hat{g}(\hat{v})\|}\;\;}
$$

其中 $\nabla \hat{g}(\hat{v})$ 是预测头 $\hat{g}$ 在特征 $\hat{v} = \hat{h}(X)$ 处的梯度：

$$
\nabla \hat{g}(\hat{v}_i) = \left.\frac{d\hat{g} \circ \hat{h}(X)}{d\hat{h}(X)}\right|_{X=X_i}
$$

## 直觉

- 分子 $|Y - \hat{g}\circ\hat{h}(X)|$：output space 的残差
- 分母 $\|\nabla \hat{g}(\hat{v})\|$：预测头在特征点的局部"放大率"——梯度大处，output 小残差对应 feature 大偏差，需缩小（除以梯度）
- 等价于对预测头做一阶 Taylor 展开，把 feature-space 的 band 线性映回 output space

## 理论保证（Theorem 4 + 5）

- **Theorem 4（有效性）**：FFCP 返回的 band 满足 empirical coverage $\ge 1-\alpha$
- **Theorem 5（效率性，square conditions）**：在 **square conditions**（expansion + quantile stability，比 cubic conditions 少一项）下，FFCP 返回比 vanilla CP 更短的 band

## 实证

- FFCP ≈ FCP 精度（都优于 vanilla），**~50x 加速**
- 通用性：扩展到 CQR（FFCQR）、LCP（FFLCP）、RAPS（FFRAPS）

## 在滕佳烨工作中的地位

Feature CP 主线的**工程兑现**——把"特征空间更优"的理念变成可部署的高效算法。体现滕佳烨"理论 + 工程并重"：Theorem 5 保证效率，50x 加速保证实用。

## 局限

- Taylor 展开是一阶近似，feature space 严重非线性时近似误差累积
- square conditions 是温和假设，实证满足，但理论上是 sufficient 而非 necessary
