# Split CP Coverage 定理

> 节点 ID: `thm-split-cp-coverage` | type: theorem | 来源: `src-angelopoulos-bates-2022`（CP 基础，复用 conformal-prediction 示例）

## 定理表述

设数据对 $(X_i, Y_i)_{i=1}^{n}$ 与测试点 $(X_{n+1}, Y_{n+1})$ 满足 **exchangeability**（可交换性，弱于 i.i.d.）。将数据分为训练折 $\mathcal{D}_{tr}$ 与校准折 $\mathcal{D}_{ca}$，在训练折上训练模型 $\hat{\mu}$，在校准折上计算 non-conformity score $V_i = s(X_i, Y_i, \hat{\mu})$。

取分位数

$$
\hat{q} = \text{Quantile}\left(\left\{V_i\right\}_{i \in \mathcal{D}_{ca}};\; \lceil (1-\alpha)(n_{ca}+1) \rceil / (n_{ca}+1)\;\text{level}\right)
$$

则 split conformal prediction set

$$
\mathcal{C}_{1-\alpha}(X_{n+1}) = \left\{Y : s(X_{n+1}, Y, \hat{\mu}) \le \hat{q}\right\}
$$

满足 **finite-sample, distribution-free marginal coverage**：

$$
\boxed{\;\;P\left(Y_{n+1} \in \mathcal{C}_{1-\alpha}(X_{n+1})\right) \ge 1 - \alpha\;\;}
$$

## 关键性质

- **finite-sample**：不依赖渐近理论，任意样本量成立
- **distribution-free**：不假设数据分布形式
- **marginal（非 conditional）**：保证的是对 $X$ 平均意义下的 coverage，**不**保证对每个条件组 $X \in G$ 都成立（conditional coverage 在一般情况下不可达，见 `def-conditional-coverage` / `thm-conditional-coverage-impossible`）
- **post-hoc / model-agnostic**：不重训模型，是包裹在任意黑盒预测器外的校准层

## 在滕佳烨工作中的地位

这是滕佳烨**所有工作的理论底盘**——他的每一篇论文都以这条 coverage 保证为底线：

- T-SCI：在 censoring/covariate shift 下恢复这条保证（`thm-teng2021-tsci-coverage`）
- Feature CP：在特征空间做 CP，coverage 仍由 exchangeability 保证，额外证明更短（`thm-teng2023-feature-cp-advantage`）
- SCD-split：smoothing 不破坏这条保证（Theorem 4.1）
- Prejudicial Trick：PT 在这条保证上玩花招——coverage valid 但 length 欺骗（`thm-teng2026-prejudicial-trick`）

## 局限

- marginal coverage 不等于 conditional coverage（对子群可能欠覆盖）
- exchangeability 假设（分布漂移下失效）
- 效率（interval length）不由定理保证，依赖 non-conformity score 的选择——这正是滕佳烨改进的方向
