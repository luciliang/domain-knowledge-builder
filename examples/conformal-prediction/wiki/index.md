# 知识节点索引

> 领域：统计校准与共形预测 | 节点数：50 | 边数：138 | 来源数：3
> 生成日期：2026-06-24 | 更新：2026-06-25

---

## Definition（定义 · 10 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| def-conditional-coverage | Conditional Coverage | 共形预测覆盖率的理想目标：对所有输入条件的均匀覆盖保证 |
| def-conformal-coverage | Conformal Risk Control Guarantee | CRC 框架的基本覆盖率保证定义 |
| def-crc | Conformal Risk Control (CRC) | 通过有序保序性统计量控制任意风险函数的共形方法 |
| def-fsc-metric | Feature-Stratified Coverage (FSC) Metric | 按特征分组度量的覆盖率指标，评估条件覆盖近似程度 |
| def-marginal-coverage | Marginal Coverage | 共形预测的基本保证：整体样本集上至少 1−α 的覆盖率 |
| def-semantic-uq | Semantic Uncertainty Quantification | 在医学影像等语义空间中量化像素级预测不确定性的方法 |
| def-split-conformal-prediction | Split Conformal Prediction (Inductive) | 将数据拆分为拟合集和校准集的归纳式共形预测方法 |
| def-ssc-metric | Size-Stratified Coverage (SSC) Metric | 按预测集大小分层的覆盖率指标，衡量集合大小自适应性 |
| def-three-errors | Three Components of Conditional Miscoverage | 条件误覆盖分解为三个误差分量：WCP 误差、校准误差、内在条件失配误差 |
| def-unified-cp-framework | Unified CP Framework via Weighted Conformal Quantiles | 通过加权共形分位数统一各类共形预测方法的理论框架 |

---

## Method（方法 · 13 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| meth-aps | Adaptive Prediction Sets (APS) | 分类任务中自适应大小的预测集方法，近似条件覆盖 |
| meth-class-conditional-cp | Class-Conditional Conformal Prediction | 按类别分别设定覆盖阈值的条件共形预测方法 |
| meth-conformalize-bayes | Conformalizing Bayes | 将贝叶斯后验与共形预测结合以获得有效覆盖率保证 |
| meth-conformalize-uncertainty | Conformalizing Scalar Uncertainty Estimates | 利用标量不确定性估计构建共形集的通用方法 |
| meth-covariate-shift-conditional | Conditional Methods under Covariate Shift | 协变量漂移下通过密度比加权和局部化恢复条件覆盖的方法 |
| meth-cqr | Conformalized Quantile Regression (CQR) | 将分位数回归与共形预测结合的回归区间方法 |
| meth-graphcp | GraphCP: Community-Conditional Conformal Prediction on Graphs | 在图数据上实现社区条件覆盖的共形预测方法 |
| meth-group-balanced-cp | Group-Balanced Conformal Prediction | 为已知分组提供均衡覆盖率保证的方法 |
| meth-k-crc | K-CRC (High-Dimensional Risk Control via K Groups) | 通过 K 组划分实现高维空间风险控制的 CRC 扩展 |
| meth-model-selection-cc | Conditional-Coverage-Oriented Model Selection | 以条件覆盖为导向的模型选择方法，基于内在误差分量 |
| meth-outlier-detection-cp | Conformal Outlier Detection | 将共形预测框架应用于无监督异常检测的方法 |
| meth-sem-crc | sem-CRC (Semantic Conformal Risk Control) | 基于语义分组实现实例级风险控制的 CRC 变体 |
| meth-sem-crc-per-organ | sem-CRC̄ (Per-Organ Risk Control) | 逐器官风险控制的 sem-CRC 变体，提供更细粒度保证 |

---

## Theorem（定理 · 19 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| thm-averaged-miscoverage | Theorem 3: Averaged Conditional Miscoverage under Weak Conditions | 弱条件下的平均条件误覆盖上界定理 |
| thm-beta-coverage-distribution | Beta Distribution of Coverage (Vovk 2012) | 覆盖率在有限样本下服从 Beta 分布，刻画随机波动 |
| thm-cc-averaged | Corollary 1: Averaged Conditional Miscoverage of CC | CC 方法的平均条件误覆盖推论 |
| thm-class-conditional-coverage | Proposition 2: Class-Conditional CP Validity | 类别条件共形预测的有效性命题 |
| thm-community-conditional | Theorem 7: Community-Conditional Miscoverage Convergence | 社区条件误覆盖收敛性定理 |
| thm-conditional-coverage-impossible | Conditional Coverage Impossibility | 一般意义下精确条件覆盖率不可达的不可能定理 |
| thm-conformal-risk-control | Theorem 2: Conformal Risk Control | 任意损失函数下风险控制的基本定理 |
| thm-covariate-shift-coverage | Theorem 3: Conformal Prediction Under Covariate Shift | 协变量漂移下通过似然比加权保持覆盖率的定理 |
| thm-covariate-shift-marginal | Theorem 4: Marginal Coverage under Covariate Shift | 加权校准在协变量漂移下恢复边际覆盖的定理 |
| thm-distribution-drift-coverage | Theorem 4: Conformal Prediction Under Distribution Drift | 分布漂移下通过加权分位数提供近似覆盖的定理 |
| thm-full-cp-coverage | Full Conformal Prediction Coverage Guarantee | 全量共形预测的覆盖率保证，计算昂贵但统计效率最优 |
| thm-group-balanced-coverage | Proposition 1: Group-Balanced CP Validity | 组均衡共形预测的有效性命题 |
| thm-marginal-coverage-weighted | Theorem 1: Marginal Coverage of Weighted CP | 加权共形分位数的边际覆盖率定理 |
| thm-outlier-detection-guarantee | Proposition 3: Outlier Detection Error Control | 异常检测错误率的共形控制命题 |
| thm-sem-crc-validity | Proposition 1: Validity of sem-CRC | 语义共形风险控制方法在 ε 水平上控制风险的有效性 |
| thm-split-cp-coverage | Theorem 1: Conformal Coverage Guarantee (Split CP) | Split CP 的基本覆盖率保证定理 |
| thm-symmpi-conditional | Theorem 6: Conditional Miscoverage Decomposition under SymmPI | SymmPI 下的条件误覆盖分解定理 |
| thm-symmpi-structured | Theorem 5: Marginal Coverage under SymmPI (Structured Data) | 结构化数据下对称排列不变性(SymmPI)的边际覆盖率定理 |
| thm-three-term-decomposition | Theorem 2: Three-Term Conditional Miscoverage Decomposition | 条件误覆盖三分量分解的核心定理 |

---

## Insight（洞见 · 4 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| ins-intrinsic-error-necessity | Intrinsic Conditional-Mismatch Error is the Key Bottleneck | 内在条件失配误差是条件覆盖的真正瓶颈，不可通过后处理消除 |
| ins-method-comparison-table | Unified Error Decomposition Across Methods (Table 1) | 基于三误差分解的统一方法对比表，揭示各类方法得失 |
| ins-semantic-uq-clinical | Clinical Value of Semantic Uncertainty in Medical Imaging | 医学影像中语义不确定性的临床价值：辅助器官特异性错误识别 |
| ins-wcp-limitation | WCP Restores Marginal but Not Conditional Coverage under Covariate Shift | 加权共形预测(WCP)在协变量漂移下恢复边际覆盖但无法恢复条件覆盖 |

---

## Experiment（实验 · 4 个）

| 节点 ID | 名称 | 一句话摘要 |
|---------|------|-----------|
| exp-covariate-shift | Conditional Methods under Covariate Shift (Synthetic) | 合成数据上验证协变量漂移条件覆盖方法有效性的实验 |
| exp-ct-denoising-reconstruction | CT Denoising and FBP-UNet Reconstruction Experiments | CT 去噪和 FBP-UNet 重建任务上评估 CRC 系列方法的实验 |
| exp-model-selection | Conditional-Coverage-Oriented Model Selection Experiments | 验证条件覆盖导向模型选择准则有效性的实验 |
| exp-toloker-graph | GraphCP on Toloker Dataset (Real Graph Data) | 真实图数据集 Toloker 上验证 GraphCP 社区条件覆盖的实验 |
