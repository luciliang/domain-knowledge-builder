---
name: conformal-prediction
description: 查询型知识库——共形预测(Conformal Prediction)领域的心智模型 + DAG 知识节点 + 查询协议。用于回答"什么是 CQR / Split CP vs Full CP / 条件覆盖"等领域问题。此为 domain-knowledge-builder meta-skill 的黄金参照实例（懒加载，仅显式请求时激活，不参与默认 skill 路由）。
domain: 统计校准与共形预测
sources: 3 (Angelopoulos & Bates 2022, Teneggi et al. 2025, Min et al. 2026)
nodes: 50
edges: 138
created: 2026-06-24
version: 1.1.0
golden_baseline: true
baseline_score: 88
classification: query-skill
---

# 统计校准与共形预测 — 领域知识 Skill

## 核心心智模型

### 1. 可交换性即合法性

共形预测的全部力量来自可交换性假设——只要校准分数与测试分数可交换，覆盖率 $\geq 1-\alpha$ 无条件成立，无需分布假设。这是 CP 独有的哲学：贝叶斯需要先验正确，频率方法需要大样本渐近，CP 的保证是有限样本且分布自由的。关键节点：`thm-split-cp-coverage`, `thm-covariate-shift-coverage`, `thm-symmpi-structured`。

### 2. 边际保证与条件追求的张力

边际覆盖廉价可达（全局平均），条件覆盖昂贵不可达（逐点保护）。Vovk 证明条件覆盖在一般情况下不可能（`thm-conditional-coverage-impossible`），但 Min et al. 的三误差分解（`thm-three-term-decomposition`）给出了精确诊断：结构性瓶颈是"内在条件失配误差"——不随样本量增大消失，必须通过方法设计使其趋于零。CQR/GLCP 通过分数设计消除，RLCP 通过加权消除。

### 3. 风险泛化器思维

`thm-conformal-risk-control` 将 CP 从"是否覆盖"推广到"控制任意有界风险"：只要损失关于参数单调且损失有界，通过经验风险的 $B/n$ 校正即可满足 $\mathbb{E}[\ell] \leq \alpha$。sem-CRC（`meth-sem-crc`）进一步展示，实例依赖语义分组下风险控制保证依然成立。

### 4. 不确定性要有语义锚点

像素级不确定性无法直接用于临床决策。语义分组（器官级）不仅产生更紧区间，还直接揭示哪些器官模型行为更不可靠。标准方法通过过度覆盖背景来补偿器官欠覆盖，掩盖了真实安全风险。关键节点：`def-semantic-uq`, `meth-sem-crc`, `meth-sem-crc-per-organ`。

---

## 查询协议

当用户提出领域相关问题时，按以下步骤执行：

1. **问题分析** — 判断涉及的概念和知识类型（定义/定理/方法/实验/洞察）
2. **DAG 遍历** — 读取 `dag/dag-index.json`，从相关概念出发沿关系边扩展
   - 剪枝：控制在 3-5 个节点（每个 ~1K tokens → 总共 ~3-5K tokens）
   - 优先级：theorem > definition > method > experiment > insight
   - 命中 `contradicts` 边 → 同时加载矛盾双方
3. **按需加载** — 只读取选中的 `wiki/knowledge/*.md`，必要时从 `wiki/sources/*.md` 补充
4. **综合回答** — 用心智模型 + 加载的知识给出有理有据的回答，每个论点引用具体节点 ID
5. **存档**（可选）— 有长期价值的回答写入 `wiki/syntheses/`

### 加载效率提示
- **核心查询**：只需 SKILL.md（心智模型 + 查询协议 + 节点索引）≈ 3K tokens
- **完整查询**：SKILL.md + dag-index.json + 3-5个知识节点 ≈ 8-11K tokens
- **Ingest/Lint**：需要额外加载 `schema/schema.md` ≈ +3K tokens
- **原则**：schema 细节（节点模板、命名规范）仅在创建/修改节点时加载，查询时不读

### 示例查询

**示例 1：概念查询** — "什么是 CQR？它与标准 CP 有什么区别？"
- Step 1: 涉及 method(meth-angelopoulos2022-cqr) + definition(def-split-conformal-prediction)
- Step 2: 从 meth-angelopoulos2022-cqr 出发 → guarantees→thm-split-cp-coverage, compares_with→meth-angelopoulos2022-aps
- Step 3: 加载 meth-angelopoulos2022-cqr.md + thm-split-cp-coverage.md（~2.2K tokens）
- Step 4: 综合回答，引用节点 ID

**示例 2：跨论文比较** — "Split CP 和 Full CP 有什么区别？什么时候用哪个？"
- Step 1: 涉及 theorem(thm-split-cp-coverage, thm-full-cp-coverage) + definition(def-split-conformal-prediction)
- Step 2: thm-full-cp-coverage → generalizes→thm-split-cp-coverage, specializes→def-split-conformal-prediction
- Step 3: 加载 thm-full-cp-coverage.md + thm-split-cp-coverage.md（~2.2K tokens）
- Step 4: 对比计算成本（O(n) refits vs O(1)）和统计效率

**示例 3：实验设计** — "如何评估我的 sCT 模型的条件覆盖是否充分？"
- Step 1: 涉及 definition(def-fsc-metric, def-ssc-metric, def-conditional-coverage) + insight(ins-intrinsic-error-necessity)
- Step 2: def-conditional-coverage → evaluates→def-fsc-metric, evaluates→def-ssc-metric; def-fsc-metric → compares_with→def-ssc-metric
- Step 3: 加载 4 个节点（~3.3K tokens）
- Step 4: 推荐 FSC+SSC 双指标，引用三误差分解指出内在失配误差是瓶颈

---

## 知识节点索引

### Definition（10）

| ID | 名称 |
|----|------|
| def-conditional-coverage | Conditional Coverage |
| def-conformal-coverage | Conformal Risk Control Guarantee |
| def-teneggi2025-crc | Conformal Risk Control (CRC) |
| def-fsc-metric | Feature-Stratified Coverage (FSC) Metric |
| def-marginal-coverage | Marginal Coverage |
| def-semantic-uq | Semantic Uncertainty Quantification |
| def-split-conformal-prediction | Split Conformal Prediction |
| def-ssc-metric | Size-Stratified Coverage (SSC) Metric |
| def-three-errors | Three Components of Conditional Miscoverage |
| def-unified-cp-framework | Unified CP Framework via Weighted Conformal Quantiles |

### Method（13）

| ID | 名称 |
|----|------|
| meth-angelopoulos2022-aps | Adaptive Prediction Sets (APS) |
| meth-class-conditional-cp | Class-Conditional Conformal Prediction |
| meth-conformalize-bayes | Conformalizing Bayes |
| meth-conformalize-uncertainty | Conformalizing Scalar Uncertainty Estimates |
| meth-covariate-shift-conditional | Conditional Methods under Covariate Shift |
| meth-angelopoulos2022-cqr | Conformalized Quantile Regression (CQR) |
| meth-min2026-graphcp | GraphCP: Community-Conditional CP on Graphs |
| meth-group-balanced-cp | Group-Balanced Conformal Prediction |
| meth-k-crc | K-CRC (High-Dimensional Risk Control via K Groups) |
| meth-model-selection-cc | Conditional-Coverage-Oriented Model Selection |
| meth-outlier-detection-cp | Conformal Outlier Detection |
| meth-sem-crc | sem-CRC (Semantic Conformal Risk Control) |
| meth-sem-crc-per-organ | sem-CRC̄ (Per-Organ Risk Control) |

### Theorem（19）

| ID | 名称 |
|----|------|
| thm-averaged-miscoverage | Theorem 3: Averaged Conditional Miscoverage |
| thm-beta-coverage-distribution | Beta Distribution of Coverage (Vovk 2012) |
| thm-cc-averaged | Corollary 1: Averaged Miscoverage of CC |
| thm-class-conditional-coverage | Proposition 2: Class-Conditional CP Validity |
| thm-community-conditional | Theorem 7: Community-Conditional Miscoverage Convergence |
| thm-conditional-coverage-impossible | Conditional Coverage Impossibility |
| thm-conformal-risk-control | Theorem 2: Conformal Risk Control |
| thm-covariate-shift-coverage | Theorem 3: CP Under Covariate Shift |
| thm-covariate-shift-marginal | Theorem 4: Marginal Coverage under Covariate Shift |
| thm-distribution-drift-coverage | Theorem 4: CP Under Distribution Drift |
| thm-full-cp-coverage | Full Conformal Prediction Coverage Guarantee |
| thm-group-balanced-coverage | Proposition 1: Group-Balanced CP Validity |
| thm-marginal-coverage-weighted | Theorem 1: Marginal Coverage of Weighted CP |
| thm-outlier-detection-guarantee | Proposition 3: Outlier Detection Error Control |
| thm-sem-crc-validity | Proposition 1: Validity of sem-CRC |
| thm-split-cp-coverage | Theorem 1: Conformal Coverage Guarantee (Split CP) |
| thm-symmpi-conditional | Theorem 6: Conditional Miscoverage under SymmPI |
| thm-symmpi-structured | Theorem 5: Marginal Coverage under SymmPI |
| thm-three-term-decomposition | Theorem 2: Three-Term Conditional Miscoverage Decomposition |

### Insight（4）

| ID | 名称 |
|----|------|
| ins-intrinsic-error-necessity | Intrinsic Conditional-Mismatch Error is the Key Bottleneck |
| ins-method-comparison-table | Unified Error Decomposition Across Methods (Table 1) |
| ins-semantic-uq-clinical | Clinical Value of Semantic Uncertainty in Medical Imaging |
| ins-wcp-limitation | WCP Restores Marginal but Not Conditional Coverage |

### Experiment（4）

| ID | 名称 |
|----|------|
| exp-covariate-shift | Conditional Methods under Covariate Shift (Synthetic) |
| exp-ct-denoising-reconstruction | CT Denoising and FBP-UNet Reconstruction |
| exp-model-selection | Conditional-Coverage-Oriented Model Selection |
| exp-toloker-graph | GraphCP on Toloker Dataset (Real Graph Data) |

---

## 术语映射

| 英文 | 中文 |
|------|------|
| Conformal Prediction (CP) | 共形预测 |
| Marginal Coverage | 边际覆盖 |
| Conditional Coverage | 条件覆盖 |
| Split Conformal Prediction | 分割共形预测 |
| Exchangeability | 可交换性 |
| Conformal Risk Control (CRC) | 共形风险控制 |
| Conformalized Quantile Regression (CQR) | 共形化分位数回归 |
| Adaptive Prediction Sets (APS) | 自适应预测集 |
| Covariate Shift | 协变量漂移 |
| Semantic Uncertainty Quantification | 语义不确定性量化 |
| Intrinsic Conditional-Mismatch Error | 内在条件失配误差 |
| Feature-Stratified Coverage (FSC) | 特征分层覆盖 |
| Size-Stratified Coverage (SSC) | 大小分层覆盖 |
| SymmPI (Symmetric Permutation Invariance) | 对称排列不变性 |
| GraphCP | 图共形预测 |

---

## 诚实边界

**已覆盖：** Split/full/conformalized 量化回归基础理论、条件覆盖三误差统一分解、协变量漂移下边际与条件覆盖、语义风险控制及临床应用、图结构数据 CP、Beta 分布有限样本波动。

**未覆盖：** 交叉共形预测（仅提及）、时序/流数据 CP、非可交换场景（对抗数据、因果推断 CP）、多任务/多标签联合校准、高维分位数计算复杂度。

**有争议/未解决：** 条件覆盖近似度量（FSC vs SSC）尚无统一标准；理论 oracle 分数 vs 实践估计分数存在鸿沟；协变量漂移下密度比估计的误差传播未被完全分析；sem-CRC 对分割模型质量的依赖未纳入理论保证。

---

## 维护说明

- **Ingest 新文献：** 读取 `schema/schema.md` → 按 Ingest 工作流执行（提取 → DAG 合并 → 更新导航 → 验证）
- **Query：** 读 `dag/dag-index.json` → 遍历边 → 按需加载 `wiki/knowledge/*.md` → 用心智模型综合回答
- **Lint：** 检查孤立节点、矛盾关系、重复节点、缺失引用、来源覆盖完整性
- **知识路径：** `wiki/knowledge/` 存节点，`wiki/sources/` 存来源摘要，`dag/dag-index.json` 存关系图，`wiki/index.md` 存导航
