# 专家心智元素 Schema — Expert Mind Elements

> 本文件定义专家顾问生成器中**专家心智元素的建模规范**。心智元素 = 专家心智的核心实体（mental_model/heuristic/anti_pattern），带三重验证 + 知识依据（grounded_in），是 expert-mind/ 目录的数据契约。

---

## 0. 定位与职责

| 维度 | 说明 |
|------|------|
| **目的** | 为专家心智元素（心智模型、启发式、反模式）提供统一建模，建立心智与知识的紧耦合关联 |
| **时机** | S5b（专家心智提炼）+ S5c（紧耦合融合） |
| **产物** | `expert-mind/mental-models.md`（每个心智元素一个 frontmatter 块） |
| **关键作用** | 三重验证确保心智可靠性；grounded_in 建立心智→知识的引用关系，为 judgment 提供依据 |

---

## 1. Frontmatter 字段定义

每个心智元素包含以下 YAML frontmatter：

### 必填字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 唯一标识，格式前缀 + slug（如 `mm-lecun-energy-based-worldview`） |
| `type` | enum | ✅ | 心智元素类型：`mental_model` \| `heuristic` \| `anti_pattern` |
| `label` | string | ✅ | 中文标签（简短概括） |
| `statement` | string | ✅ | 核心陈述（一句话概括该心智元素） |
| `status` | enum | ✅ | 验证状态：`verified` \| `demoted` \| `inferred` \| `contradicted` |
| `verification` | object | ✅ | 三重验证结果（cross_scene/generative/exclusive） |
| `grounded_in` | array | ✅ | 知识依据（对象数组，每项 `{node, role, quote}`） |
| `confidence` | enum | ✅ | 置信度：`high` \| `medium` \| `low` |
| `provenance` | object | ✅ | 来源溯源 `{sources: [src-*.md id 列表]}` |

### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `demote_reason` | string | 降级原因（仅 `status: demoted` 时使用） |

---

## 2. 字段枚举值说明

### type（心智元素类型）

| 值 | 含义 | 三重验证要求 | grounded_in 要求 | 典型示例 |
|------|------|-------------|-----------------|----------|
| `mental_model` | 心智模型（专家的核心信念体系） | **3 重全过**（cross_scene + generative + exclusive） | **必须** `≥1` 节点（强耦合，有硬依据） | LeCun 能量世界观、Hinton 知识先验观 |
| `heuristic` | 启发式（经验法则/决策捷径） | **1-2 重**（至少 cross_scene 或 generative） | 可选（可能只有经验依据，无明确知识节点） | Karpathy「先看官方实现再读论文」 |
| `anti_pattern` | 反模式（明确反对的方法/观点） | **排他性必过**（exclusive 验证） | **必须** 用 `role: refutes` 指向反对的方法节点 | LeCun 反对「纯自回归做推理」 |

### status（验证状态）

| 值 | 含义 | 出现场景 |
|------|------|----------|
| `verified` | 已验证（三重验证全过） | S5b 三重验证通过的心智元素 |
| `demoted` | 已降级（原为 mental_model，但 grounded_in 不足） | §4.4 降级规则：3 重过但语义不匹配 |
| `inferred` | 已推断（基于心智镜片外推，非专家原话） | §6.2 推断落盘机制 |
| `contradicted` | 已矛盾（专家前后观点矛盾） | S3 合并发现矛盾时标注 |

### grounded_in 对象数组结构

**统一为对象数组**（与 judgment schema 一致），每项包含：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `node` | string | ✅ | 知识节点 ID（引用 `dag/knowledge/` 中节点） |
| `role` | enum | ✅ | 关系角色：`supports` \| `refutes` \| `context` |
| `quote` | string | ✅ | 引用原文（证明该关系的专家原话） |

**role 枚举说明**：
- `supports`：该知识节点支撑此心智元素（如定理支撑观点）
- `refutes`：该知识节点与此心智元素矛盾（主要用于 `anti_pattern`）
- `context`：提供上下文，但不直接支撑或反驳（如反例说明）

### verification 对象结构（三重验证）

继承 nuwa 三重验证方法论：

```yaml
verification:
  cross_scene: { pass: true/false, evidence: [场景1, 场景2] }
  generative: { pass: true/false, predicts: "可预测的行为/判断" }
  exclusive:  { pass: true/false, vs: "对立观点/替代方案" }
```

| 验证维度 | 说明 | 通过标准 |
|---------|------|---------|
| `cross_scene` | 跨场景一致性 | 在≥3 个不同场景/话题下出现该心智模式 |
| `generative` | 生成性（可预测性） | 能预测专家对新问题的判断/选择 |
| `exclusive` | 排他性 | 与对立观点区分清晰（非平庸陈述） |

---

## 3. 完整示例

### 示例 1：心智模型（mental_model）

```yaml
---
id: mm-lecun-energy-based-worldview
type: mental_model
label: 能量模型世界观
statement: "智能 = 在能量函数上做优化/约束满足，而非自回归预测下一token"
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "在 JEPA 架构中强调 latent space 预测"
      - "多次批评 LLM 缺乏世界模型"
      - "提出 LatentEBM 作为统一框架"
  generative:
    pass: true
    predicts: "对任何新架构先问其能量函数/目标函数是什么"
  exclusive:
    pass: true
    vs: "贝叶斯派靠先验、生成式派靠似然"
grounded_in:
  - node: thm-ebm-as-energy-minimization
    role: supports
    quote: "能量模型的核心是将学习问题转化为能量函数最小化"
  - node: meth-jepa-latent-predictive
    role: supports
    quote: "JEPA 在潜在空间做预测，避免自回归的逐 token 生成"
  - node: thm-planning-needs-world-model
    role: supports
    quote: "真正的规划需要在世界模型上做 forward 模拟"
confidence: high
provenance:
  sources:
    - src-lecun-jepa-2022
    - src-lecun-lex-2023
    - src-lecun-latent-ebm-2023
---

## 核心思想

LeCun 的根本信念是「智能本质 = 在适当定义的能量函数上做优化」，而非当前主流的「纯自回归续写」。

### 跨场景证据

1. **架构选择**：JEPA 不做逐 token 生成，而是在 latent space 预测未来表征
2. **对 LLM 批评**：多次公开表示「LLM 缺乏世界模型，无法真正推理」
3. **统一框架**：提出 LatentEBM 作为兼容判别式和生成式的统一范式

### 局限

- 能量函数设计仍需人工归纳（非完全端到端）
- 推理速度受能量优化过程约束

### 支撑节点

- `thm-ebm-as-energy-minimization`：能量基础模型理论基础
- `meth-jepa-latent-predictive`：架构实现
- `thm-planning-needs-world-model`：规划理论依据
```

### 示例 2：启发式（heuristic）

```yaml
---
id: heur-karpathy-official-impl-first
type: heuristic
label: 官方实现优先原则
statement: "学新算法时先跑官方实现，再读论文，而非直接从论文啃"
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "多次推荐在 GitHub 上找官方实现"
      - "自己教学时先让学生跑代码再看理论"
  generative:
    pass: false
    predicts: null  # 无法预测具体技术选择，只是学习策略
  exclusive:
    pass: true
    vs: "学院派'先读论文再实现'"
grounded_in: []  # 启发式允许无知识节点依据
confidence: medium
provenance:
  sources:
    - src-karpathy-twitter-2023
    - src-karpathy-blog-let-s-build-gpt
---

## 适用场景

- 快速上手新领域（避免陷入论文细节先迷失）
- 验证论文宣称（跑不动的官方实现可能说明论文有问题）

## 局限

- 无官方实现时失效（需降级为直接读论文）
- 官方实现可能有 bug（需批判性使用）
```

### 示例 3：反模式（anti_pattern）

```yaml
---
id: ap-lecun-autoregressive-reasoning
type: anti_pattern
label: 反对自回归做推理
statement: "纯自回归 LLM 不能做真正的推理和规划"
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "在访谈中多次强调"
      - "在 IEEE Spectrum 专访中详述"
  generative:
    pass: true
    predicts: "对任何声称'LLM 会推理'的论文持怀疑态度"
  exclusive:
    pass: true
    vs: " Scaling camp 相信'LLM 通过 scale 突现推理'"
grounded_in:
  - node: meth-autoregressive-generation
    role: refutes
    quote: "自回归只是逐 token 概率续写，没有世界模型的 forward 模拟能力"
  - node: thm-planning-needs-world-model
    role: supports
    quote: "真正的规划需要预测后果，这需要世界模型"
  - node: exp-gpt4-planning-benchmarks
    role: context
    quote: "虽然 CoT 下部分规划任务可通过，但这不是真正的推理"
confidence: high
provenance:
  sources:
    - src-lecun-lex-2023
    - src-lecun-ieee-spectrum-2022
---

## 反对理由

1. **缺乏世界模型**：自回归只做局部 token 预测，无全局状态表征
2. **无法做后果预测**：规划需要在抽象空间模拟不同行动的后果
3. **外推能力差**：训练分布外的任务容易失效

## 诚实边界

- CoT 和 Scratchpad 可以**部分缓解**（显式展开推理步骤）
- GPT-4 在部分规划基准上表现良好（但仍有失败案例）
- 这是开放争论，非共识
```

### 示例 4：降级心智模型（demoted）

```yaml
---
id: mm-lecun-ebm-universal
type: mental_model
label: 能量模型统一论
statement: "所有 AI 问题都可以能量模型框架统一"
status: demoted
demote_reason: "semantic_mismatch"  # §4.4 降级规则
verification:
  cross_scene:
    pass: true
    evidence:
      - "在 LatentEBM 论文中提出统一框架"
  generative:
    pass: true
    predicts: "倾向于用能量模型解释新方法"
  exclusive:
    pass: true
    vs: "扩散模型派、自回归派"
grounded_in:
  - node: thm-ebm-as-energy-minimization
    role: supports
    quote: "能量模型理论基础扎实"
  # 注意：找不到更多支撑节点（如「扩散模型可归约为 EBM」之类）
confidence: high
provenance:
  sources:
    - src-lecun-latent-ebm-2023
---

## 核心思想

LeCun 认为 EBM 可以作为判别式和生成式学习的统一框架。

## 降级原因

S6 校验发现：虽然 3 重验证通过，但 `grounded_in` 只有理论节点（`thm-ebm-as-energy-minimization`），缺少实证支撑（如「扩散模型可归约为 EBM」之类节点）。语义匹配不足，降级为 `heuristic`。

## 保留价值

虽然降级，但仍保留为启发式：体现 LeCun 的理论偏好，只是不作为强心智模型。
```

---

## 4. 降级规则（引用 §4.4）

S5c 紧耦合融合执行以下降级规则（处理"3 重过但依据不足"的边界）：

| 情况 | 处理 | status |
|------|------|--------|
| 3 重全过，但 `grounded_in` **完全找不到**任何相关节点 | **丢弃**（纯口嗨，无任何知识锚点）| dropped（不入库）|
| 3 重全过，找到候选节点但 S6 判定**语义不匹配** | **降级为 heuristic**，保留原 verification + 标注降级原因 | demoted（`demote_reason: semantic_mismatch`）|
| 降级后的 heuristic | `grounded_in` 变可选，但 `provenance` 必须保留；不重跑验证 | demoted |

**关键约束**：没有 `grounded_in` 依据的判断，**不能冒充心智模型**——这是"有依据"的硬闸，由 S6 + darwin 门强制。

---

## 5. 字段必填矩阵

| type | 必填字段 | 条件字段 |
|------|---------|---------|
| `mental_model` | `id`, `type`, `label`, `statement`, `status`, `verification`, `grounded_in` (≥1项), `confidence`, `provenance` | — |
| `heuristic` | `id`, `type`, `label`, `statement`, `status`, `verification`, `confidence`, `provenance` | `grounded_in` (可选) |
| `anti_pattern` | `id`, `type`, `label`, `statement`, `status`, `verification`, `grounded_in` (≥1项，含 `role: refutes`), `confidence`, `provenance` | — |

**核心逻辑**：
- `mental_model` 和 `anti_pattern` 必须有知识依据（强耦合）
- `heuristic` 允许无知识节点（仅经验依据）

---

## 6. 质量保证

### 三重验证（S5b 执行）

- 由 `engines/nuwa-validation.md` 提供的方法论执行
- 两个独立 subagent 跑验证（避免单一视角）
- 结果落盘为 `verification` 对象

### 紧耦合校验（S6 执行）

- **程序化检查**（`lint_d7.py`）：`grounded_in` 节点 ID 存在于 dag-index（硬门③ 无孤儿判断）
- **语义抽查**（fresh subagent）：`grounded_in` 的 `role` 与 `quote` 是否真的匹配（硬门① 紧耦合完整性）

---

## 7. 与其他 Schema 的关系

| Schema | 关系 |
|--------|------|
| `schema.md` | 知识节点 schema（不变），本 schema 的 `grounded_in` 引用 `dag/knowledge/` 节点 |
| `source.md` | 来源打标 schema，本 schema 的 `provenance.sources` 引用 `src-*.md` 的 `id` |
| `coupling.md` | 紧耦合关联 schema（§4.3），judgment 的 `derived_from` 引用本 schema 的心智元素 ID |

**数据流**：
```
S5b → expert-mind/mental-models.md（本 schema）
         ↓
S5c → expert-mind/judgments.md（judgment.derived_from 引用本 schema）
```

---

## 8. 命名规范

| 对象 | 命名格式 | 示例 |
|------|---------|------|
| 文件名 | `mental-models.md`（固定） | `expert-mind/mental-models.md` |
| 心智模型 ID | `mm-<slug>` | `mm-lecun-energy-based-worldview` |
| 启发式 ID | `heur-<slug>` | `heur-karpathy-official-impl-first` |
| 反模式 ID | `ap-<slug>` | `ap-lecun-autoregressive-reasoning` |

**slug 生成规则**：
- 格式：`<专家名>-<核心概念>-<关键词>`
- 示例：`lecun-energy-based-worldview`、`karpathy-official-impl-first`

---

_本 schema 版本：expert-advisor-builder v0.1 | 维护：domain-knowledge-builder 扩展为 meta-skill_
