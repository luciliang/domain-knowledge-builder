# 心智模型：统计校准与共形预测

> 从 Vovk 的校准哲学出发，基于 Angelopoulos et al. (2022)、Teneggi et al. (2025)、Min et al. (2026) 三篇核心论文提炼。

---

## 核心心智模型

### 1. 可交换性即合法性（Exchangeability as the Only License）

**一句话：** 共形预测的全部力量来自可交换性假设——只要交换性成立，覆盖率保证无条件成立，无需任何分布假设。

**核心思想：** Vovk 的奠基定理（`thm-split-cp-coverage`）表明，覆盖率保证 $\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}})) \geq 1-\alpha$ 仅依赖校准分数与测试分数的可交换性，而非对 $P(X,Y)$ 的参数化假设。这是整个领域的合法性根基：不假设模型正确，不假设数据分布，只假设"测试样本和校准样本来自同一个不可区分的池子"。

**三重验证：**
- **跨域复现：** 在频域信号处理（`thm-distribution-drift-coverage`）、图结构数据（`thm-symmpi-structured`）中同样成立——只要存在对称性结构，可交换性就能被构造出来。
- **生成力：** 直接指导协变量漂移场景的适应性设计——若漂移的似然比已知，加权共形分位数恢复边际覆盖（`thm-covariate-shift-coverage`）。
- **排他性：** 这是共形预测独有的哲学。贝叶斯方法需要先验正确，频率方法需要大样本渐近，只有 CP 的保证是有限样本且分布自由的。

**相关节点：** `thm-split-cp-coverage`, `thm-covariate-shift-coverage`, `thm-distribution-drift-coverage`, `thm-symmpi-structured`, `thm-beta-coverage-distribution`

---

### 2. 边际保证与条件追求的张力（Marginal-Conditional Tension）

**一句话：** 边际覆盖廉价且可达，条件覆盖昂贵且不可达——整个领域的发展史就是围绕这条不可能边界的攀登史。

**核心思想：** 边际覆盖（`def-marginal-coverage`）是全局平均，允许多数错误集中在少数样本上；条件覆盖（`def-conditional-coverage`）要求每个输入都得到保护。Vovk (2012) 证明条件覆盖在一般情况下不可能（`thm-conditional-coverage-impossible`），但 Min et al. (2026) 的三误差分解（`thm-three-term-decomposition`）给出了精确诊断：结构瓶颈是"内在条件失配误差"——它不随样本量增大而消失，必须通过方法设计（选择合适的分数函数和加权方案）使其趋于零。

**三重验证：**
- **跨域复现：** 类似张力存在于鲁棒统计（全局最优 vs. 逐点最优）和公平性机器学习（群体公平 vs. 个体公平）。
- **生成力：** 指导实际选择——CQR/GLCP 通过分数设计使内在误差为零；RLCP 通过加权使分数估计误差为零；二者的权衡由具体场景驱动（`ins-method-comparison-table`）。
- **排他性：** "三条误差路径"的分解结构是 CP 条件覆盖理论特有的，其他领域没有类似的精确分解。

**相关节点：** `def-marginal-coverage`, `def-conditional-coverage`, `thm-conditional-coverage-impossible`, `thm-three-term-decomposition`, `def-three-errors`, `ins-intrinsic-error-necessity`, `ins-method-comparison-table`

---

### 3. 风险泛化器思维（The Risk Generalizer Mindset）

**一句话：** 从覆盖率到任意有界损失——CRC 把共形预测从"是否覆盖"的二元判断提升为"控制任意风险"的通用框架。

**核心思想：** `thm-conformal-risk-control` 证明，只要损失函数关于参数 $\lambda$ 单调，且损失有界，就能通过经验风险的 $B/n$ 校正找到满足 $\mathbb{E}[\ell] \leq \alpha$ 的参数。这把共形预测从覆盖率保证推广到风险控制保证。Teneggi 的 sem-CRC（`meth-sem-crc`）进一步展示，即使在实例依赖分组下，只要分割模型固定（保持可交换性），风险控制保证依然成立（`thm-sem-crc-validity`）。

**三重验证：**
- **跨域复现：** 在在线学习（对偶平均法的止损保证）和强化学习（约束策略优化）中有类似的风险控制范式。
- **生成力：** 直接生成 sem-CRC 等新方法——将像素级风险重构为器官级风险，只需替换分组方式和损失定义。
- **排他性：** $B/n$ 校正项是共形框架特有的——它精确控制有限样本的"最坏情况"越界概率，与 VC 维或其他泛化界有本质区别。

**相关节点：** `thm-conformal-risk-control`, `def-teneggi2025-crc`, `meth-sem-crc`, `thm-sem-crc-validity`, `def-semantic-uq`, `meth-k-crc`

---

### 4. 不确定性要有语义锚点（Anchoring Uncertainty to Semantics）

**一句话：** 不确定性估计的价值不在于精度，而在于能否与终端用户的决策语言对接。

**核心思想：** Teneggi et al. (2025) 的核心论证：像素级不确定性无法直接用于临床决策（`def-semantic-uq`），而语义分组（器官级不确定性）不仅产生更紧的区间，还直接揭示哪些器官的模型行为更不可靠（`ins-semantic-uq-clinical`）。关键洞察是：标准方法通过过度覆盖背景来补偿器官的欠覆盖，掩盖了真实的安全风险（`meth-sem-crc-per-organ` vs `meth-sem-crc`）。

**三重验证：**
- **跨域复现：** 可解释 AI 领域（LIME/SHAP 将模型行为映射到特征空间）、自然语言处理（将不确定性映射到可验证的事实单元）。
- **生成力：** 指导新应用设计——任何需要不确定性量化的领域，都应先问"终端用户的语义单位是什么"，而非直接套用像素级或样本级方法。
- **排他性：** "固定分割模型 + 实例依赖分组"的组合是 sem-CRC 的特定技术选择，利用了医学影像的先验结构。

**相关节点：** `def-semantic-uq`, `meth-sem-crc`, `meth-sem-crc-per-organ`, `meth-k-crc`, `ins-semantic-uq-clinical`, `exp-ct-denoising-reconstruction`

---

## 决策启发式

1. **如果只需要有限样本保证，用 Split CP；如果需要更好的条件覆盖近似，用 APS。** 因为 Split CP 保证了不可突破的底线（`thm-split-cp-coverage`），而 APS 在分类任务中自适应调整集合大小，更好地近似条件覆盖（`e-aps-conditional`）。

2. **如果协变量分布漂移且似然比已知，用加权共形分位数恢复边际覆盖。** 因为密度比 $r_X(x)$ 直接校准到测试分布（`thm-covariate-shift-marginal`），但注意这只是边际恢复，不是条件覆盖（`ins-wcp-limitation`）。

3. **如果追求条件覆盖，先问"内在失配误差能否设计为零"。** 因为这是三误差分解中唯一不随数据量消失的项（`ins-intrinsic-error-necessity`），CQR/GLCP 通过分数设计使其为零，RLCP 保留非零失配但消除了分数估计误差（`ins-method-comparison-table`）。

4. **如果损失函数有界且关于参数单调，用 CRC 而非标准 CP。** 因为 CRC 是标准 CP 到任意有界损失的推广（`thm-conformal-risk-control`），退化的特殊情况下与标准覆盖保证一致。

5. **如果在高维图像中量化不确定性，不要用固定像素分组——用语义分组。** 因为不同患者的解剖结构差异大，固定分组会过度覆盖简单区域（`def-semantic-uq`, `meth-sem-crc`）。

6. **如果需要器官级风险控制（如监管审批），用 per-organ 变体而非全局控制。** 因为全局风险控制可能掩盖特定器官的系统性失效（`ins-semantic-uq-clinical`），代价是平均区间更长（`meth-sem-crc-per-organ`）。

7. **如果分数估计误差和内在失配误差都非零，优先消减内在失配。** 因为内在失配是结构性瓶颈，不随数据增加而消失；分数估计是机械性误差，多数据自然解决（`def-three-errors`）。

---

## 诚实边界

### 已覆盖
- Split/full/conformalized 量化回归的基础理论（Angelopoulos 2022）
- 条件覆盖的三误差统一分解（Min 2026）
- 协变量漂移下的边际与条件覆盖分析（Min 2026, Angelopoulos 2022）
- 语义风险控制方法及其临床应用（Teneggi 2025）
- 图结构数据上的共形预测（Min 2026 GraphCP）
- Beta 分布的有限样本覆盖率波动刻画（Vovk 2012, Angelopoulos 2022）

### 未覆盖
- **交叉共形预测（Cross-conformal prediction）**：仅简单提及，未深入
- **时序/流数据的 conformal 方法**：完全未涉及
- **非 exchangeable 场景**（如 adversarial data、因果推断中的 CP）
- **多任务/多标签联合校准**的覆盖保证
- **计算效率**：高维场景下的分位数计算复杂度未分析

### 有争议/未完全解决
- **条件覆盖近似度量**的选择（FSC vs SSC）尚无统一标准（`def-fsc-metric`, `def-ssc-metric`）
- **最佳分数函数**的理论选择与实际选择之间有鸿沟——理论建议用 oracle 分数，实践中必须用估计分数
- **协变量漂移下密度比估计**的实用性：Min 2026 假设密度比已知，但实际中需要估计，估计误差的传播未被完全分析
- **sem-CRC 的分割模型敏感性**：Teneggi 2025 明确指出分割模型质量影响结果，但该依赖未被纳入理论保证

---

_生成日期：2026-06-24 | 基于 3 篇论文 49 个知识节点 135 条边的 DAG_
