# 紧耦合关联 Schema — Coupling Layer (Judgment)

> 本文件定义专家顾问生成器中**紧耦合关联的建模规范**。judgment = 紧耦合的"枢纽"：一条专家判断 = 立场 + 推理链 + 依据节点。回答「专家怎么看 X」的核心载体，独立成层避免污染知识 DAG。

---

## 0. 定位与职责

| 维度 | 说明 |
|------|------|
| **目的** | 为专家判断（judgment）提供统一建模，建立专家心智与知识节点的紧耦合关联 |
| **时机** | S5c（紧耦合融合）：judgment 通过 `derived_from` 继承心智元素的验证，挂载 `grounded_in` 依据节点 |
| **产物** | `expert-mind/judgments.md`（每个判断一个 frontmatter 块） |
| **关键作用** | 回答「专家怎么看 X」= 判断 + 推理 + 依据节点；紧耦合确保判断有知识锚点 |

---

## 1. Frontmatter 字段定义

每个 judgment 包含以下 YAML frontmatter：

### 必填字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 唯一标识，格式前缀 + slug（如 `judg-lecun-llm-cant-reason`） |
| `type` | string | ✅ | 固定值 `judgment`（与心智元素 type 区分） |
| `label` | string | ✅ | 中文标签（简短概括判断） |
| `status` | enum | ✅ | 验证状态：`verified` \| `inferred` \| `contradicted` |
| `trigger` | string | ✅ | 触发问题（用户可能问的问题） |
| `derived_from` | string | ✅ | 所属心智元素 ID（引用 `expert-mind/mental-models.md` 中心智元素） |
| `judgment` | string | ✅ | 判断立场（一句话回答"专家怎么看 X"） |
| `reasoning` | string | ✅ | 推理链（判断的推导过程） |
| `grounded_in` | array | ✅ | 知识依据（对象数组，每项 `{node, role, quote}`） |
| `confidence` | enum | ✅ | 置信度：`high` \| `medium` \| `low` |
| `provenance` | object | ✅ | 来源溯源 `{sources: [src-*.md id 列表]}` |

### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `counter_evidence` | array | 反方证据（对象数组，结构与 `grounded_in` 相同，role 用 `context`） |

---

## 2. 字段枚举值说明

### type（类型）

- **固定值** `judgment`：标识本文件为判断实体，与心智元素（`mental_model`/`heuristic`/`anti_pattern`）区分

### status（验证状态）

| 值 | 含义 | 出现场景 |
|------|------|----------|
| `verified` | 已验证（继承自心智元素的 verification） | S5c 中，judgment 通过 `derived_from` 继承所属心智元素的三重验证结果 |
| `inferred` | 已推断（基于心智镜片外推，非专家原话） | §6.2 推断落盘机制：对未明确表述的问题，用心智镜片推断并落盘 |
| `contradicted` | 已矛盾（专家前后观点矛盾） | S3 合并发现矛盾时标注 |

**重要**：judgment **无 `demoted` 状态**，不参与 §4.4 降级。降级只作用于心智元素（§4.2），judgment 通过 `derived_from` 继承其所属心智元素的最终 status。

### grounded_in 对象数组结构

**统一为对象数组**（与心智元素 schema 同结构），每项包含：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `node` | string | ✅ | 知识节点 ID（引用 `dag/knowledge/` 中节点） |
| `role` | enum | ✅ | 关系角色：`supports` \| `refutes` \| `context` |
| `quote` | string | ✅ | 引用原文（证明该关系的专家原话） |

**role 枚举说明**：
- `supports`：该知识节点支撑此判断（如定理支撑推理）
- `refutes`：该知识节点与此判断矛盾（反例说明）
- `context`：提供上下文，但不直接支撑或反驳（如边界条件说明）

### derived_from（继承机制）

judgment 通过 `derived_from` **继承**所属心智元素的三重验证结果：

- judgment **不独立跑三重验证**（避免重复计算）
- quality 由 `provenance`（忠实度，硬门②）+ `grounded_in`（紧耦合，硬门①）保证
- 若所属心智元素被降级（`status: demoted`），其下的 judgment 继承降级后的心智模型状态

### counter_evidence（反方证据）

**诚实列反方**（避免误导），结构与 `grounded_in` 相同：

- **role 固定用 `context`**（非直接反驳，而是提供边界说明）
- 典型场景：专家判断「LLM 不能做推理」，但 GPT-4 在部分规划基准上表现良好 → 列为 `counter_evidence`，role 用 `context`

---

## 3. 完整示例

### 示例 1：verified judgment（继承验证）

```yaml
---
id: judg-lecun-llm-cant-reason
type: judgment
label: LLM不能真正推理
status: verified
trigger: "LLM 能做真正的推理吗 / 为什么 LLM 不会规划"
derived_from: mm-lecun-energy-based-worldview
judgment: "不能。纯自回归续写缺乏世界模型，无法预测后果做规划"
reasoning: "推理 = 在抽象空间预测后果+规划路径；自回归只做token级概率续写，
           没有世界模型的 forward 模拟能力，故外推时暴露"
grounded_in:
  - node: thm-planning-needs-world-model
    role: supports
    quote: "真正的规划需要预测后果，这需要世界模型"
  - node: meth-jepa-latent-predictive
    role: supports
    quote: "JEPA 在潜在空间做预测，避免自回归的逐 token 生成"
  - node: meth-autoregressive-generation
    role: refutes
    quote: "自回归只是逐 token 概率续写，没有世界模型的 forward 模拟能力"
counter_evidence:
  - node: exp-gpt4-planning-benchmarks
    role: context
    quote: "虽然 CoT 下部分规划任务可通过，但这不是真正的推理"
    note: "Chain-of-Thought 可以部分缓解，但仍不是真正的世界模型"
confidence: high
provenance:
  sources:
    - src-lecun-lex-2023
    - src-lecun-ieee-spectrum-2022
---

## 判断背景

用户常问「LLM 能做真正的推理和规划吗」，这是 LeCun 被反复问到的问题。

## 判断立场

**不能**。纯自回归续写缺乏世界模型，无法预测后果做规划。

## 推理链

1. **推理的定义**：在抽象空间预测不同行动的后果 + 规划最优路径
2. **自回归的本质**：逐 token 概率续写，无全局状态表征
3. **缺乏世界模型**：没有 forward 模拟能力，无法预测后果
4. **外推暴露**：训练分布外的任务容易失效

## 支撑节点

- `thm-planning-needs-world-model`：规划理论依据（真正的规划需要世界模型）
- `meth-jepa-latent-predictive`：架构实现（JEPA 在潜在空间做预测）
- `meth-autoregressive-generation`：反驳对象（自回归的局限性）

## 诚实边界

- CoT 和 Scratchpad 可以**部分缓解**（显式展开推理步骤）
- GPT-4 在部分规划基准上表现良好（但仍非真正的推理）
- 这是开放争论，非共识
```

### 示例 2：inferred judgment（推断落盘）

```yaml
---
id: judg-lecun-transformer-cant-reason
type: judgment
label: Transformer架构无法实现真正推理
status: inferred
trigger: "Transformer 架构能实现真正的推理吗"
derived_from: mm-lecun-energy-based-worldview
judgment: "不能。Transformer 的自回归本质仍缺乏世界模型的 forward 模拟能力"
reasoning: "虽然 Transformer 可以通过 attention 捕获长距离依赖，但其核心仍是
           token 级续写，无法在抽象空间做后果预测"
grounded_in:
  - node: thm-planning-needs-world-model
    role: supports
    quote: "规划需要世界模型，这是架构无关的约束"
  - node: meth-transformer-attention
    role: context
    quote: "Attention 机制改善长距离依赖，但不改变自回归本质"
confidence: medium
provenance:
  sources:
    - src-lecun-lex-2023
  note: "推断基于心智镜片（能量世界观），非专家直接表述"
---

## 推断依据

此判断基于 `mm-lecun-energy-based-worldview` 的心智镜片推断：
- 虽然专家未明确表述「Transformer 不能推理」，但其对「自回归续写」的批评隐含此判断
- 推断逻辑：Transformer 的自回归本质与 LLM 相同，故同样缺乏世界模型

## 推断置信度

`medium`（非专家原话，仅为心智镜片的外推）
```

### 示例 3：contradicted judgment（矛盾标注）

```yaml
---
id: judg-lecun-llm-reasoning-progress
type: judgment
label: LLM推理能力有进展但不充分
status: contradicted
trigger: "LLM 的推理能力是否有进步"
derived_from: mm-lecun-energy-based-worldview
judgment: "有进展（CoT、Scratchpad），但仍不是真正的推理"
reasoning: "虽然显式展开推理步骤可改善表现，但核心问题（缺乏世界模型）未解决"
grounded_in:
  - node: meth-chain-of-thought
    role: context
    quote: "CoT 通过显式展开步骤缓解，但不改变本质"
  - node: thm-planning-needs-world-model
    role: supports
    quote: "真正的推理需要世界模型，这是硬约束"
confidence: low
provenance:
  sources:
    - src-lecun-lex-2023
    - src-lecun-ieee-spectrum-2022
contradiction:
  detected_at: "S3-merge"
  conflicting_statements:
    - "在 2022 年 IEEE Spectrum 采访中表示「LLM 毫无推理能力」"
    - "在 2023 年 Lex Fridman 访谈中承认「CoT 下有部分推理表现」"
  resolution: "标注为 contradicted，保留两个时间点的判断，由用户自行判断"
---

## 矛盾说明

LeCun 在不同时间点的表述存在演化：
- 2022 年：强硬反对「LLM 能推理」
- 2023 年：承认进展但坚持「非真正推理」

## 标注处理

S3 合并时检测到矛盾，标注为 `contradicted`，保留两个时间点的判断，供用户参考演化轨迹。
```

---

## 4. 两条边界澄清（§4.4 修订，round-2 spec）

### 边界 1：judgment 无 demoted status

**降级只作用于心智元素（§4.2），不作用于 judgment**：
- judgment 的 status 枚举为 `verified | inferred | contradicted`（**无 `demoted`**）
- 降级/丢弃由 S5c 在心智元素层面执行
- judgment 通过 `derived_from` 继承其所属心智元素的最终 status，自身不参与 §4.4 降级

**原因**：judgment 是心智元素的具体应用实例，降级应作用在心智模型层（源），而非每个判断实例（汇）。

### 边界 2：§4.4 降级/丢弃规则优先于 §6.2 推断落盘

**优先级**：§4.4 > §6.2
- 若一条判断同时落在「3 重过但 grounded_in 完全找不到」情形又被推断机制触及
- 以 §4.4 为准——即无依据的推断判断**不落盘 `inferred`**，而是按 §4.4 丢弃或降级为 heuristic

**原因**：避免推断机制绕过紧耦合闸门（无依据的判断不应通过推断通道落盘）。

---

## 5. 为什么独立成层、不污染知识 DAG

### DKB 的 DAG 边是「知识↔知识」

- DAG 节点 = 定理/方法/实验/定义/洞察（知识实体）
- DAG 边 = 知识节点之间的逻辑关系（`uses`/`generalizes`/`contradicts` 等）

### 如果把 judgment 塞进 DAG

**污染问题**：
- DAG 节点混入「专家判断」（主观判断 vs 客观知识）
- query 时难剪枝（用户问「什么是 X」时，不应返回专家的观点）
- 图谱膨胀（每个专家的每个判断都成为节点，不可控）

### 独立关联层的设计

**judgment 作为独立层**（`expert-mind/judgments.md`）：
- 通过 `grounded_in` 引用知识节点 ID（引用关系，非 DAG 边）
- 知识图谱保持干净（纯知识）
- 紧耦合关系单独可查、可验证

**查询分离**：
- 问「什么是 X」→ 查 DAG（知识节点）
- 问「专家怎么看 X」→ 查 judgment（判断 + grounded_in 节点 ID）
- 问「专家为什么认为 X」→ 融合查询（judgment + grounded_in 节点全文）

---

## 6. 字段必填矩阵

| judgment 类型 | 必填字段 | 条件字段 |
|-------------|---------|---------|
| 所有 judgment | `id`, `type`, `label`, `status`, `trigger`, `derived_from`, `judgment`, `reasoning`, `grounded_in` (≥1项), `confidence`, `provenance` | `counter_evidence`（建议列反方） |

**核心逻辑**：
- 所有 judgment **必须有 `grounded_in` ≥1 项**（紧耦合硬约束）
- `counter_evidence` 不强制，但强烈建议（诚实列反方，提高可信度）

---

## 7. 质量保证

### 紧耦合完整性（S6 执行）

- **程序化检查**（`lint_d7.py`）：`grounded_in` 节点 ID 存在于 dag-index（硬门③ 无孤儿判断）
- **语义抽查**（fresh subagent）：`grounded_in` 的 `role` 与 `quote` 是否真的匹配（硬门① 紧耦合完整性）

### 忠实度验证（硬门②）

- judgment 的 `provenance.sources` 必须能追溯到具体 `src-*.md`
- 网采源：HTTP 验证 URL 可达
- 用户材料源：`locator.{page, section}` 可 grep 核对

完整校验流程（fresh subagent 抽查、darwin 门判定）见 **spec §7 与 pipeline §5.4**，本 schema 不重复定义，避免分叉。

---

## 8. 与其他 Schema 的关系

| Schema | 关系 |
|--------|------|
| `schema.md` | 知识节点 schema（不变），本 schema 的 `grounded_in` 引用 `dag/knowledge/` 节点 |
| `source.md` | 来源打标 schema，本 schema 的 `provenance.sources` 引用 `src-*.md` 的 `id` |
| `expert-mind.md` | 专家心智 schema（§4.2），本 schema 的 `derived_from` 引用心智元素 ID |

**数据流**：
```
S5b → expert-mind/mental-models.md（expert-mind.md schema）
         ↓
S5c → expert-mind/judgments.md（本 schema）
         ├─ derived_from → 心智元素 ID
         └─ grounded_in → 知识节点 ID
```

---

## 9. 命名规范

| 对象 | 命名格式 | 示例 |
|------|---------|------|
| 文件名 | `judgments.md`（固定） | `expert-mind/judgments.md` |
| judgment ID | `judg-<slug>` | `judg-lecun-llm-cant-reason` |

**slug 生成规则**：
- 格式：`<专家名>-<核心问题>-<关键概念>`
- 示例：`lecun-llm-cant-reason`、`karpathy-official-impl-first`

---

_本 schema 版本：expert-advisor-builder v0.1 | 维护：domain-knowledge-builder 扩展为 meta-skill_
