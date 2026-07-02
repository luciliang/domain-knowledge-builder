# SCD-split（Smoothing-based Conformal Prediction）

> 节点 ID: `meth-teng2025-scd-split` | type: method | 来源: `src-teng2025-smoothing-cp`

## 问题

CD-split（conditional density split CP）用条件密度估计作 conformity score，效率高（区间短）。但**在多模态分布下，生成的预测集由大量断开子区间组成**，难以解释（医生/投资者面对 10 个断开区间无法决策）。

## 新度量：connectivity（断开子区间数量）

滕佳烨引入 **断开子区间数量** 作为 CP 的新度量，与 interval length 共同刻画 **interpretability**（可解释性）：

| 维度 | 含义 | 越___越好 |
|------|------|----------|
| interval length | 预测集总长度 | 短 |
| **number of disjoint intervals** | 断开子区间数 | **少** |

## SCD-split 方法

1. 用户指定期望的子区间数 $k$
2. 对估计的条件密度函数做 **Fourier smoothing**（傅里叶平滑）
3. smoothing 减少密度函数不必要的峰（peaks）
4. validation 过程调 smoothing 参数，使最终预测集子区间数逼近 $k$

## 理论三保证

- **Theorem 4.1（validity）**：smoothing 保持 marginal coverage $\ge 1-\alpha$（不破坏 CP 底线）
- **Theorem 4.2（connectivity 不增）**：smoothing 后断开子区间数不增
- **Theorem 4.3（narrow-valley double peaks 下严格减少）**：在"窄谷双峰"等结构假设下，子区间数严格减少
- **Theorem 4.4（length upper bound）**：smoothing 后区间长度有可证明的上界（不会为减子区间而爆炸式增长）

## 应用动机

- **医疗**：疾病预后可能"快速恶化"或"长期康复"两条轨迹，医生需要 2 个清晰区间而非 1 个宽区间或 10 个碎片
- **金融**：股价"大涨"或"大跌"两种场景，投资者需要 2 个区间区分上下行风险

## 在滕佳烨工作中的地位

这是滕佳烨「**coverage 是底线，但要平衡效率与可解释性**」心智的直接体现——不盲目追求更短区间，而是把可解释性纳入度量。与 questioning-metric（`thm-teng2026-prejudicial-trick`）一脉相承：质疑"interval length 唯一论"。

## 局限

- smoothing 引入超参（smoothing 强度），需 validation 调参
- connectivity 度量是回归任务导向（分类任务预测集结构不同）
