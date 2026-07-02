# T-SCI Coverage 定理（两阶段共形推断恢复 Cox-MLP 的 guaranteed coverage）

> 节点 ID: `thm-teng2021-tsci-coverage` | type: theorem | 来源: `src-teng2021-tsci`

## 问题

生存分析中，**censoring（删失）** 意味着只能观测 $Y = \min\{T, C\}$（生存时间 $T$ 与删失时间 $C$ 的最小值），而非真实生存时间 $T$。这导致：
1. **covariate shift**：删失与未删失数据的协变量分布不同，$(X|\Delta=1) \neq (X|\Delta=0)$，破坏 exchangeability
2. Cox-MLP（神经网络版 Cox 回归）放松线性假设后失去 guaranteed coverage

## 假设：strong ignorability

$$
T \perp \Delta \mid X
$$

（生存时间与删失指示变量在协变量条件下独立）——weighted conformal inference 的标准假设。

## 方法：两阶段共形推断（T-SCI）

### 阶段 1：WCCI（Weighted Conformal Censoring Inference）

- 基于偏似然（partial likelihood）设计 non-conformity score（不需显式估计生存时间）
- 用 **weighted conformal inference**（Tibshirani-Foygel 2019）处理 covariate shift

### 阶段 2：Quantile conformal inference 校准

- 用 quantile conformal inference（Romano et al. 2019）校准 WCCI 结果
- 返回 **"nearly perfect" coverage**：既有 lower bound 也有 upper bound 保证

## 理论保证

- **WCCI**：在 strong ignorability 下返回 guaranteed coverage（恢复 `thm-split-cp-coverage` 在删失场景的保证）
- **T-SCI**：在 **milder 假设** 下返回 nearly perfect guaranteed coverage——不仅保证 $\ge 1-\alpha$（lower bound），还保证不超过 $1-\alpha+\epsilon$（upper bound），即"接近精确"

## 在滕佳烨工作中的地位

这是滕佳烨 CP 研究的**起点**（第一作者，清华 IIIS）：
- 确立"**coverage 是底线**"——即使在困难的删失/covariate shift 场景，也要恢复 guaranteed coverage
- 引入"**两阶段校准逼近精确**"的范式——WCCI 先保证，T-SCI 再校准收紧
- 与后续工作的对比：Feature CP 追求"更短"，T-SCI 追求"更精确（区间不空但也不太宽）"

## 局限

- strong ignorability 假设（若 $T \not\perp \Delta | X$ 则失效）
- 依赖偏似然框架（Cox 系），非任意删失机制
- 与 Candès et al. (2021) 的删失 CP 是不同假设下的平行工作（后者放松 strong ignorability 但要求删失时间信息完全）
