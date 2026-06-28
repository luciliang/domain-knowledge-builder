# Query 工作流 — 三模式查询协议（专家顾问版）

> 本文件是 **expert-advisor-builder 生成的专家顾问 skill** 被查询时遵循的流程。
> 对应 spec §6。生成的每个专家顾问 skill 的 SKILL.md 会内嵌此协议的精简版。

---

## 0. 何时触发

用户在已生成的专家顾问 skill 上下文中提问：
- "什么是 X？" / "X 的定义/定理"
- "专家怎么看 X / 会怎么选 / 怎么办"
- "专家为什么认为 X / X 的依据"
- "比较 A 和 B" / "如何评估 / 设计 / 选择 X"

**不触发**（应路由到 builder meta-skill）：
- "给 X 领域建知识库" / "把这些论文变成 skill"
- "生成 X 专家的顾问 skill"

---

## 1. 意图路由（第 0 步）

根据用户问题类型，路由到三种查询模式：

```
用户问题
   ↓ 判断问题类型
   ├─ "什么是X / X的定义/定理"        ─▶ 【知识模式】(Step 1a)
   ├─ "专家怎么看X / 会怎么选 / 怎么办" ─▶ 【心智模式】(Step 1b)
   ├─ "专家为什么认为X / X的依据"       ─▶ 【融合模式】(Step 1c) ⭐
   └─ 模糊                              ─▶ 【融合模式】(默认，最全)
```

**路由规则**：
- **明确知识查询**（定义/定理/方法）→ 知识模式
- **明确心智查询**（专家判断/决策）→ 心智模式
- **融合查询**（判断+依据）或意图模糊 → 融合模式（默认）

---

## 2. 三模式查询流程

### Step 1a: 知识模式（继承 DKB DAG 遍历）

**适用场景**：「什么是 X」「X 的定理/方法」「X 和 Y 的区别」

#### 流程

1. **问题分析**：判断涉及的概念/知识类型（def/thm/meth/exp/ins）
2. **DAG 遍历**：从问题概念出发，沿关系边扩展
   - 剪枝规则：控制在 3-5 个节点（每个 ~1K tokens → 总共 ~3-5K tokens）
   - 优先级：theorem > definition > method > experiment > insight
   - 冲突加载：`contradicts` / `does_not_guarantee` 命中 → 同时加载双方
3. **按需加载**：
   - 只读取选中的 `dag/knowledge/*.md`
   - 必要时从 `sources/*.md` 补充（需要来源上下文 / 节点信息不足）
4. **返回**：定理/方法原文（LaTeX）+ 来源 provenance

#### 诚实边界（知识模式）

- 知识不足的子领域 → 明说「本库未覆盖此方向」
- 定理/方法的局限 → 主动标注适用边界
- 矛盾/争议 → 同时呈现双方 + 各自证据

---

### Step 1b: 心智模式（专家判断 + 推理链）

**适用场景**：「专家怎么看 X」「专家会怎么选」「专家怎么办」

#### 流程

1. **加载专家心智镜片**：读取 `expert-mind/mental-models.md`（心智模型/启发式/反模式）
2. **匹配 judgment**：在 `expert-mind/judgments.md` 中查找匹配的判断（通过 `trigger` 字段）
3. **返回判断 + 推理 + 依据**：
   - **专家立场**（`judgment` 字段）
   - **推理链**（`reasoning` 字段）
   - **依据节点 ID**（`grounded_in` 引用的知识节点）
   - **置信度**（`confidence` 字段）
4. **推断机制**（无现成 judgment 时）：
   - 用心智镜片（mental_models/heuristic）推断答案
   - **构建期/测试期**：推断结果落盘为新 judgment（`status: inferred`），供 S6 复审与测试复现
   - **运行期**：推断结果只读不写（不持久化，避免违背 skill 只读惯例 + 并发写冲突），标注「推断·非原话」

#### 诚实边界（心智模式）

- **专家没说过**：标注「推断·基于其心智镜片外推，非原话」（落盘 status: inferred）
- **知识不足子领域**：明说「专家未明确表述此方向，基于镜片推断」
- **观点演化**：标注「早期/近期」判断（通过 `provenance.sources` 时间线）
- **判断矛盾**：并列双方 + 各自适用边界（status: contradicted）
- **落在反模式**：直接说「专家会反对，因为…」+ 反模式依据

---

### Step 1c: 融合模式（判断 + 理论依据 + 替代方案）⭐

**适用场景**：「专家为什么认为 X」「X 的依据」；或意图模糊时的默认模式（最全）

#### 流程

1. **镜片理解**：加载 `expert-mind/mental-models.md`，理解专家心智框架
2. **找 judgment**：匹配 `expert-mind/judgments.md` 中相关判断（通过 `trigger` 或语义匹配）
3. **加载依据节点**：根据 judgment 的 `grounded_in` 字段，加载对应知识节点（`dag/knowledge/*.md`）
4. **综合回答**（四要素）：
   - **[立场]** 专家判断（`judgment` 字段 + judgment ID）
   - **[理论依据]** 支撑该判断的知识节点（`grounded_in` 引用的定理/方法，含节点 ID）
   - **[替代方案]** 专家提出的其他方法（`grounded_in` 中 `role: supports` 的 method 节点）
   - **[局限/诚实边界]** 反方证据/适用边界（`counter_evidence` 或 `grounded_in` 中 `role: context`）
5. **推断机制**（同心智模式）：
   - **构建期/测试期**：推断落盘为 `status: inferred` judgment
   - **运行期**：推断只读不写，标注「推断·非原话」

#### 融合模式回答示例

> **问**：LeCun 会怎么看「用 LLM 做世界模型」？
>
> **答**：
> - **[立场]** 大概率反对——自回归 LLM 缺乏世界模型的 forward 模拟 *(judg-lecun-llm-cant-reason)*
> - **[理论依据]** 规划/推理需在抽象空间预测后果 *(thm-planning-needs-world-model)*，而自回归只做 token 续写
> - **[他的替代方案]** JEPA 在 latent 空间做预测式学习 *(meth-jepa-latent-predictive)*
> - **[诚实边界]** 但 CoT 下部分规划任务 GPT-4 可通过 *(exp-gpt4-planning-benchmarks)*，此为开放争论

#### 诚实边界（融合模式）

融合模式**必须包含诚实边界**，规则同心智模式：
- **推断标注**：非专家原话 → 「推断·基于心智镜片外推，非原话」
- **知识缺口**：未覆盖方向 → 「本库未覆盖此子领域」
- **观点演化**：早期/近期观点标注时间线
- **矛盾并列**：双方判断 + 适用边界（不强行调和）
- **反模式直说**：落在反模式 → 「专家会反对，因为…」+ 依据

---

## 3. 推断落盘机制（构建期 vs 运行期）

### 落盘规则

| 阶段 | 行为 | 原因 |
|------|------|------|
| **构建期/测试期** | 推断结果落盘为新 judgment（`status: inferred`）| 测试可复现 + S6 复审 + 积累专家判断库 |
| **运行期** | 推断结果只读不写（不持久化）| 避免违背 skill 只读惯例 + 防止并发写冲突 |

### status: inferred 的落盘格式

```yaml
---
id: judg-<专家>-<推断问题>-<推断>
type: judgment
label: <推断判断标签>
status: inferred              # 标注为推断
trigger: "<触发问题>"
derived_from: mm-<心智镜片-id>  # 标注推断来源
judgment: "<推断立场>"
reasoning: "<推断推理链>"
grounded_in:
  - node: <支撑节点-id>
    role: supports
    quote: "专家原话支撑此推断"
confidence: medium           # 推断置信度通常为 medium
provenance:
  sources:
    - src-<原始来源>-<id>
  note: "推断基于心智镜片（<心智镜片-label>），非专家直接表述"
---
```

### 运行期推断返回格式（不落盘）

```
[立场] <推断答案>
**[推断说明]** 此答案基于专家的心智镜片（<心智镜片名>）推断，非专家原话。
[理论依据] <引用的知识节点 ID>
```

---

## 4. 加载效率提示（token 预算）

| 查询模式 | 加载内容 | tokens |
|---------|---------|--------|
| **知识模式** | SKILL.md + dag-index.json + 3-5 个知识节点 | ~8-11K |
| **心智模式** | SKILL.md + expert-mind/mental-models.md + expert-mind/judgments.md | ~6-9K |
| **融合模式**（全）| SKILL.md + mental-models.md + judgments.md + 3-5 个知识节点 | ~12-16K |
| **Ingest/Lint** | 额外加 schema/*.md | +3-6K |

**原则**：
- schema 细节（节点模板、命名规范）仅在创建/修改节点时加载，查询时不读
- 查询优先读索引（dag-index.json / judgments.md），按需加载节点全文
- 融合模式最全，token 最高，适合「判断 + 依据」的深度查询

---

## 5. 查询质量自检（三模式通用）

### 通用自检

回答前自问：
- [ ] 每个论点引用了具体节点 ID / judgment ID？
- [ ] 知识模式：定理/方法原文 + 来源 provenance？
- [ ] 心智模式：判断 + 推理链 + 依据节点 ID？
- [ ] 融合模式：四要素完整（立场 + 理论依据 + 替代方案 + 局限）？

### 诚实边界自检

- [ ] 推断判断是否标注「推断·非原话」或 `status: inferred`？
- [ ] 知识缺口是否明说「未覆盖」，不补脑？
- [ ] 观点演化是否标注「早期/近期」？
- [ ] 矛盾判断是否并列双方 + 适用边界？
- [ ] 落在反模式是否直接说「专家会反对，因为…」？

### 引用完整性

- [ ] 知识模式：每个论点引用知识节点 ID（如 `thm-xxx`）
- [ ] 心智模式：每个判断引用 judgment ID（如 `judg-xxx`）
- [ ] 融合模式：每个论点同时引用 judgment ID + 知识节点 ID

---

## 6. 可选——回答存档

有长期价值的回答（如跨源综合、复杂对比）→ 写入 `wiki/syntheses/<topic>.md`（DKB 原有机制）

存档规则：
- 只创建新文件，不合入现有 knowledge 节点（synthesis 是综合答案，非原始知识）
- 融合模式的四要素回答优先存档（立场 + 依据 + 替代 + 局限）
- 存档时保留引用关系（judgment ID + 知识节点 ID）

---

## 7. Schema 引用（扩展说明）

### 相关 schema 文件

| 查询要素 | 来源 schema | 关键字段 |
|---------|------------|----------|
| **知识节点** | `schema/schema.md` | 节点类型（def/thm/meth/exp/ins）+ 关系（uses/generalizes/contradicts） |
| **专家心智元素** | `schema/expert-mind.md` | mental_model / heuristic / anti_pattern + verification |
| **判断（judgment）** | `schema/coupling.md` | judgment + reasoning + grounded_in + status |
| **来源打标** | `schema/source.md` | value（knowledge/mind/both）+ channel + provenance |

### 查询时不读 schema 细节

- 知识类型和关系 → 直接读 `dag-index.json` 的 edges 字段
- judgment 结构 → 直接读 `expert-mind/judgments.md` 的 frontmatter
- schema 细节（模板、命名规范）仅在创建/修改节点时加载

---

_本查询协议对应 spec §6 | 生成专家顾问 skill 的 SKILL.md 内嵌精简版_
_扩展自 domain-knowledge-builder 原有 query.md，增加三模式路由 + 推断落盘 + 诚实边界_
