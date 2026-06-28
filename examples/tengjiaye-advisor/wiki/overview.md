# 共形预测领域概览 — 滕佳烨视角

## 什么是共形预测（Conformal Prediction, CP）

共形预测是一种 **distribution-free、finite-sample** 的不确定性量化框架。给定任意黑盒预测器（包括神经网络），CP 通过一个校准步骤包裹它，输出 **prediction set / confidence band** $\mathcal{C}_{1-\alpha}(X)$，保证：

$$
P\left(Y_{\text{test}} \in \mathcal{C}_{1-\alpha}(X_{\text{test}})\right) \ge 1 - \alpha
$$

这条保证只需 **exchangeability**（可交换性，弱于 i.i.d.），不需假设数据分布形式，任意样本量成立。详见 `thm-split-cp-coverage`。

## CP 的核心张力

CP 研究围绕一对永恒张力展开：

| 目标 | 要求 | 难点 |
|------|------|------|
| **Coverage（有效性）** | P(Y∈C) ≥ 1-α | 底线，不可妥协 |
| **Efficiency（效率）** | interval length 尽量短 | 与 coverage 冲突（C=∞ 恒满足 coverage） |

滕佳烨的研究正是在这对张力上展开，并**扩展了评估维度**——除 length 外，引入 connectivity（可解释性）和 stability（可靠性）。

## 滕佳烨的研究版图（5 大贡献）

### 1. 特征空间 CP（研究主线）
- **Feature CP (ICLR 2023)**：把 CP 从 output space 迁移到语义 feature space，利用深度表示归纳偏置，cubic conditions 下 provably 更短
- **Fast Feature CP (2025)**：Taylor 展开近似，50x 加速，工程兑现

### 2. 可解释性 CP
- **SCD-split (2025)**：CD-split 在多模态下生成大量断开子区间，用 Fourier smoothing 合并；引入 connectivity 度量

### 3. 批判性度量研究
- **Prejudicial Trick (ICML 2026)**：证明 coverage-length 可被欺骗，更短≠更好；引入 interval stability 度量

### 4. 生存分析 CP
- **T-SCI (2021)**：删失/covariate shift 下用 weighted conformal + 两阶段校准恢复 Cox-MLP 的 guaranteed coverage

### 5. CP 基础理论应用
- 所有工作都建立在 split CP coverage 定理 + exchangeability 之上（`thm-split-cp-coverage` / `def-exchangeability`）

## 滕佳烨心智的演化轨迹

```
2021 T-SCI          → 确立 "coverage 是底线"（困难场景守底线）
       ↓
2023 Feature CP     → 确立 "特征空间优于输出空间"（研究主线奠基）
       ↓
2025 SCD-split      → 演化 "平衡效率与可解释性"（质疑 length 唯一论）
       ↓
2026 Prejudicial    → 确立 "质疑标准度量" + 反模式（批判性成熟）
       Trick
```

这条轨迹清晰展现一位研究者从「守住底线 → 找到主线 → 深化批判」的成熟过程。

## 与 CP 经典文献的关系

| 经典工作 | 与滕佳烨的关系 |
|----------|----------------|
| Vovk et al. (2005) — CP 奠基 | 滕佳烨所有工作的理论源头 |
| Angelopoulos-Bates (2022) — CP 综述 | 滕佳烨理论底盘 + 质疑对象（质疑其 coverage-length 评估范式） |
| Tibshirani-Foygel (2019) — weighted CP | T-SCI 的 covariate shift 处理工具 |
| Romano et al. (2019) — quantile CP | T-SCI 第二阶段校准工具 |
| Romano et al. (2020) — APS | Feature CP 的对比基准 |
| Izbicki et al. (2021) — CD-split | SCD-split 的改进对象 |

## 诚实边界

- 本库聚焦滕佳烨个人贡献 + CP 基础，非 CP 全景（如 online CP、time series CP、NLP 应用等子领域未深入）
- conditional coverage 理论（Min 2026）作为参照来源，未展开为独立节点
- 滕佳烨心智是**专家个人镜片**，非 CP 共识——经典派（Angelopoulos 等）对 feature space / 度量质疑的看法可能不同
