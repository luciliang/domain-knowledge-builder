# 专家心智元素索引 — 滕佳烨（Jiaye Teng）

> 本文件是**导航文件**，心智元素实体存储在独立 `mm-*.md` / `ap-*.md` 文件中（顶部裸 frontmatter，供 lint 解析）。
> 对应 schema `expert-mind.md`。

## 心智模型（mental_model，3 重全过 + grounded_in ≥1）

| ID | 标签 | 核心陈述 | 文件 |
|----|------|----------|------|
| `mm-teng-feature-space-superior` | 特征/语义空间优于输出空间 | CP 应在语义特征空间而非输出空间做，深度表示归纳偏置让 prediction set provably 更短 | [`mm-teng-feature-space-superior.md`](mm-teng-feature-space-superior.md) |
| `mm-teng-coverage-as-floor` | Coverage 是底线 | P(Y_test ∈ C) ≥ 1-α 是不可妥协的底线，困难场景也要先恢复 | [`mm-teng-coverage-as-floor.md`](mm-teng-coverage-as-floor.md) |
| `mm-teng-balance-efficiency-interpretability` | 平衡效率与可解释性 | interval length 不是唯一目标，connectivity 同样重要 | [`mm-teng-balance-efficiency-interpretability.md`](mm-teng-balance-efficiency-interpretability.md) |
| `mm-teng-question-standard-metric` | 质疑标准度量充分性 | coverage-length 不足以评判 CP，更短≠更好，需 stability 度量 | [`mm-teng-question-standard-metric.md`](mm-teng-question-standard-metric.md) |

## 反模式（anti_pattern，exclusive 必过 + role:refutes）

| ID | 标签 | 核心陈述 | 文件 |
|----|------|----------|------|
| `ap-teng-blind-shorter-better` | 反对盲目追求更短区间 | 仅凭 length 更短声称更优而不审 coverage/碎片化/stability，滕佳烨根本怀疑 | [`ap-teng-blind-shorter-better.md`](ap-teng-blind-shorter-better.md) |

## 心智演化时间线

1. **2021（T-SCI）**：确立 `mm-teng-coverage-as-floor`——困难场景守底线
2. **2023（Feature CP）**：确立 `mm-teng-feature-space-superior`——研究主线奠基
3. **2025（SCD-split）**：演化出 `mm-teng-balance-efficiency-interpretability`——质疑 length 唯一论
4. **2026（Prejudicial Trick）**：确立 `mm-teng-question-standard-metric` + `ap-teng-blind-shorter-better`——批判性成熟

## 三重验证锚点说明

滕佳烨心智的锚点是**专家个人镜片**（非领域共识）：
- "feature space 优于 output space" 非所有 CP 研究者共识（经典派仍坚持黑盒 output-space CP）
- "质疑 coverage-length 度量" 是滕佳烨课题组的独特视角（Min/Lu 等为其学生/合作者）

换一位 CP 专家（如 Angelopoulos）这些心智不一定成立——这是 expert-advisor 与领域 knowledge-base 的本质区别。
