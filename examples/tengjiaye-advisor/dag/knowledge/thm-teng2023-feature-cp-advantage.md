# Feature CP 优势定理（Feature Conformal Prediction）

> 节点 ID: `thm-teng2023-feature-cp-advantage` | type: theorem | 来源: `src-teng2023-feature-cp`（滕佳烨代表作，ICLR 2023）

## 核心命题

把 conformal prediction 从**输出空间**（output space）迁移到**语义特征空间**（feature space），在深度学习的归纳偏置下，可 provably 返回更短的 confidence band，同时 coverage 有效。

## Feature CP 框架

将模型拆分为 $\hat{\mu} = \hat{g} \circ \hat{f}$：
- $\hat{f}$：feature function（前几层，提取语义特征）
- $\hat{g}$：prediction head（后几层，特征 → 输出）

在 feature space 而非 output space 计算 non-conformity score，再通过 Band Estimation / Band Detection 把 feature space 的 band 转回 output space。

### surrogate feature（解决 feature space 无 ground truth）

特征空间没有 ground truth，滕佳烨提出 **surrogate feature** 替代 non-conformity score 中的 ground truth 项（`meth-teng2023-surrogate-feature`）。

## 关键定理（Theorem 6：cubic conditions 下 Feature CP 更优）

**cubic conditions** 从三方面刻画特征空间性质：

1. **length preserving**：映射不显著拉伸/压缩距离
2. **expansion**：特征空间有利的几何展开
3. **quantile stability**：个体 non-conformity score 与其分位数的距离更小

**结论**：在 cubic conditions 下，Feature CP 返回的 confidence band **provably 比 vanilla CP 更短**，且

$$
P\left(Y_{n+1} \in \mathcal{C}_{1-\alpha}^{\text{Feature}}(X_{n+1})\right) \ge 1 - \alpha
$$

仍由 exchangeability 保证（coverage 有效）。

## 直觉

- **output-space CP 的局限**：对图像分割，所有像素返回相同不确定性，无视语义区域
- **feature-space CP 的优势**：在语义特征空间，不同区域的不确定性可区分；经非线性变换 `ĝ` 映回 output space 后，像素级不确定性自然分化（信息量区域确定，边界区域不确定）

## 实证（SOTA）

- ImageNet 分类、Cityscapes 像素级分割：Feature CP 优于 vanilla，达 SOTA
- 可插入 CQR 等 adaptive CP（feature-level 技术通用）

## 在滕佳烨工作中的地位（研究主线奠基）

这是滕佳烨**最核心的贡献**——确立"CP 应在特征/语义空间做"这一研究范式：
- Fast Feature CP（`meth-teng2025-ffcp-score`）：加速 Feature CP 的工程兑现
- Feature CP 的"利用归纳偏置"思想贯穿他后续所有工作

## 局限

- cubic conditions 是温和假设，实证满足，但非对所有 feature space 成立
- Band Estimation 依赖 LiPRA 非线性操作，耗时长（FFCP 解决此问题）
