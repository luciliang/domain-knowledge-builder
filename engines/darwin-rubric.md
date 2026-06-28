# Darwin 2.0 Rubric — 领域知识库 Skill 质量评分规范

> 本文件是 domain-knowledge-builder meta-skill 的**质量门规范**。所有生成的知识库 skill 都须过此门——加权总分 ≥ B+（80/100）才算生成成功。
> 评估基准：darwin 2.0 的 9 维评估体系。第 9 维按被评 skill 的类型选双子类（见 §2）。

---

## 1. 9 维评分体系

### 评分公式

```
总分(百分制) = Σ 维度分(1-10) × 权重 × 10
```

- 每个维度打 **1-10 分**，附一句扣分理由。
- 权重合计 **100%**：①②③④ 各 15%、⑤⑥ 各 10%、⑦ 8%、⑧ 7%、⑨ 5%。
- 满分 = 10 × 1.0 × 10 = **100**。

> 示例（CP 实例）：9×0.15+9×0.15+8×0.15+9×0.15+9×0.10+8×0.10+8×0.08+8×0.07+10×0.05 = 8.65 → **86.5 ≈ 87（A-）**

### 评分锚点（通用 1-10 锚）

评分子 agent 逐维度打分时，参照以下通用锚点（维度特定标准见下表「满分要点」）：

| 分 | 含义 |
|----|------|
| 10 | 满分——该维度所有要点全部满足，无可扣之处 |
| 8-9 | 优秀——仅 1 个微小扣分点（不影响核心可用性） |
| 6-7 | 合格——存在 1-2 个明显短板，但核心功能成立 |
| 4-5 | 及格——有结构性缺陷，影响部分功能 |
| 1-3 | 不及格——该维度基本不满足要求 |

> 原则：优先按「满分要点」表对照，扣分点表给出常见问题。若被评 skill 表现介于两档，取中间分（如 8.5）。每个扣分必须附一句理由。

### 维度定义表

| # | 维度 | 权重 | 10 分要点（满分标准） | 常见扣分点 |
|---|------|------|----------------------|-----------|
| ① | **结构完整性** | 15% | YAML frontmatter 规范完整（name/description/domain/sources/nodes/edges/version）；章节划分清晰，层次从高层心智模型到底层节点 ID 层次分明；导航结构合理 | 缺 CHANGELOG；缺快速上手示例（Getting Started）；frontmatter 字段缺失 |
| ② | **清晰度** | 15% | 查询/工作流步骤具体且有序（分析→遍历→加载→综合→存档）；剪枝规则（如 3-5 节点）和优先级排序（theorem > definition > …）操作性强；心智模型用「一句话开头」再展开；术语映射提供中英对照 | 触发条件模糊（如"必要时补充"未给具体判定条件）；步骤无序号或无明确输入/输出 |
| ③ | **内容完整性** | 15% | 覆盖领域核心理论 + 高级主题 + 应用扩展；知识节点密度高（无空壳节点）；诚实边界准确列出已覆盖/未覆盖/有争议 | 遗漏领域当前热点（如 LLM 应用方向）；核心概念仅提及无深入节点；来源数不足 |
| ④ | **可操作性** | 15% | 工作流每步有具体约束（节点 500-2000 tokens、定理必须原文精确表述）；schema 提供完整节点模板 + DAG 边类型定义；外部依赖有路径验证或 fallback | 依赖脚本无路径验证；无 fallback；步骤可执行性差（缺参数/格式/示例） |
| ⑤ | **准确性** | 10% | 心智模型与领域经典理论一致；定理节点保留原文精确表述（含 LaTeX）；来源引用标注到章节/公式/页码；边方向抽查正确 | 概念描述方向正确但不精确对应原文定义；心智模型表述与定理原条件有偏差 |
| ⑥ | **一致性** | 10% | 术语全文统一（如选定 nonconformity score 则不混用 conformal score）；节点 ID 命名遵循 schema 规范（type前缀-slug）；来源合并后无重复 ID；**无断裂引用**（关系表引用的节点均存在于索引） | 断裂引用（引用了不存在的节点 ID）；来源归属不够精确；术语混用 |
| ⑦ | **执行效率** | 8% | 查询 token 预算设计合理（如 3-5K/查询）；剪枝策略避免全图遍历；心智模型放顶部避免每次重载；基础加载成本可控 | 基础加载成本偏高（SKILL.md + schema 合计 >6K）；schema 细节未走按需加载路径 |
| ⑧ | **鲁棒性** | 7% | 诚实边界明确（已覆盖/未覆盖/有争议三段）；查询协议要求"知识不足则明确说明缺什么"；Lint 覆盖孤立节点/矛盾关系/重复节点/缺失引用 | 缺环路检测说明；版本冲突无严重性等级和升级路径；矛盾关系类型选择不精确 |
| ⑨ | **元技能合规** | 5% | **按被评 skill 类型选双子类**（query-skill / generator-skill，见 §2） | 见 §2 各子类扣分细则 |

---

## 2. 第 9 维双子类详解

### 2.1 为什么拆分（核心洞察）

darwin 2.0 原「元技能合规」维度奖励**不做外部操作**（无网络、无 API、无 FS 写）——这对纯查询型 skill（如 CP 知识库）天然得 10/10。

但 **meta-skill（generator-skill）的本质是生成其他 skill**：它必然做大量 FS 写（生成知识节点）、spawn 子 agent（fan-out 抽取）、发起网络请求（docling 拉取文献）。直接套原标准，meta-skill 在这维会**系统性输给** CP（CP 得 10/10，meta-skill 只能得 0-4），导致不公平的质量门。

**解法**：第 9 维拆成两个并列子类。评分时按**被评 skill 的类型**选其一，满分仍为 10，权重不变（5%）。这样 query-skill 与 generator-skill 各自在符合自身职责的标准下被公平评估。

> 判定规则：被评 skill 是否在 frontmatter 或工作流中声明「生成/修改其他 skill 或知识库」？是 → generator-skill 子类；否（只读知识库、只回答查询）→ query-skill 子类。

### 2.2 query-skill 合规（CP 型，原标准）

**职责**：读取知识库、遍历 DAG、综合回答、可选写入存档。

| 满分标准 | 说明 |
|---------|------|
| 无网络请求 | 不发起任何外部 HTTP/API 调用 |
| 无外部 FS 写 | 唯一允许的写：`wiki/syntheses/` 存档；不修改知识节点本体 |
| 不修改外部状态 | 不依赖运行时环境、不改变系统配置 |
| 操作可枚举 | 所有操作限于：读节点、遍历 DAG、综合回答、写存档 |

**扣分**：每引入一项不合规外部操作扣 3 分；写入超出存档范围扣 4 分。

### 2.3 generator-skill 合规（meta-skill 型，新增设计）

**职责**：生成/更新知识库 skill（受控写入 + 子 agent spawn + 网络）。**允许外部操作**，但必须满足以下**四支柱**——「做得安全」替代「不做」。

#### 四支柱

| 支柱 | 要求 | 验证方法 |
|------|------|---------|
| **① 可回滚 (Reversible)** | 每个 pipeline 阶段产出独立 git commit；任何阶段退步可 `git revert`（非 `reset --hard`）；棘轮机制保证只保留改进（见 §3） | 检查 git log 是否 commit-per-stage；revert 后能否恢复前一阶段 |
| **② 可审计 (Auditable)** | 每个知识节点标注 provenance（来源论文/章节/公式/页码）；**expert-advisor 扩展**：judgment provenance 可追溯到具体来源（网采 URL 或用户材料 file+locator）；results.tsv 记录每次评分变化；可追溯到生成时刻的输入与 commit | 抽查节点 frontmatter 的 sources 字段；节点是否可溯源到具体论文段落；**抽查 judgment 的 provenance 字段，网采 URL HTTP 可达，用户材料 locator{page,section} 可定位** |
| **③ 确定性 (Deterministic)** | 节点 ID 遵循 schema 命名规范（`type前缀-slug`）；同一来源重跑生成相同 ID；无随机/时间戳命名；可重现 | 同一来源二次抽取，节点 ID 是否一致；ID 是否符合 schema |
| **④ 预检 (Preflight)** | 执行前检查所有依赖（脚本路径可达、docling 端点可用、schema 版本匹配）；缺失依赖有 fallback 或明确报错，**不静默失败** | 触发依赖缺失场景，观察是否报错而非产出残缺结果 |

#### generator-skill 评分细则

- **10/10**：四支柱全部满足。
- 每缺一项支柱扣 **1.5 分**（缺可回滚 −1.5，缺可审计 −1.5，缺确定性 −1.5，缺预检 −1.5）。
- **严重违规**（独立扣分，可叠加支柱扣分）：
  - 有外部写入但**无 provenance**（不可审计）→ 直接 ≤ **4**（不可审计等于不可信任）。
  - 缺预检导致**静默失败**（产出残缺结果无报错）→ 该维度 ≤ **6**。
  - 写入**不可回滚**（无 git commit，或用 reset 覆盖历史）→ 该维度 ≤ **5**。

> 公平性说明：generator-skill 满足四支柱即可得 10/10，与 query-skill 满分标准等价。这样 meta-skill 与 CP 在第 9 维处于同一起跑线——衡量的是「是否安全合规地履行职责」，而非「是否不做外部操作」。

### 2.4 评分实例：meta-skill 如何公平过门

以本 meta-skill（domain-knowledge-builder）自身为例，演示 generator-skill 子类评分：

| 维度 | 分 | 说明 |
|------|----|------|
| ①-⑧ | （按通用标准） | 结构/清晰度/内容/可操作性/准确性/一致性/效率/鲁棒性——与 query-skill 同标准 |
| ⑨ 元技能合规 | 9/10 | 按四支柱评：可回滚 ✓（commit-per-stage + 棘轮）、可审计 ✓（每节点标注 provenance）、确定性 ✓（节点 ID 遵 schema 规范）、预检 ✓（检查脚本/docling/schema 版本）。扣 1 分：若某阶段 fallback 不够明确 |

对比：若强行套 query-skill 原标准，meta-skill 第 9 维因「做 FS 写 + spawn + 网络」只得 **0-4**，直接被压低总分。双子类拆分后，meta-skill 凭安全合规履行职责即可得 9-10，与 CP 的 10/10 同档——质量门恢复公平。

> 评分锚点：generator-skill 第 9 维 | 10=四支柱全 ✓ | 8-9=缺一项弱项 | 6-7=缺一项核心支柱 | ≤5=有严重违规（不可审计/不可回滚/静默失败） |

---

## 3. 棘轮机制（Ratchet）

> 借鉴 Karpathy autoresearch：只保留改进，自动回滚退步。

### 核心规则

1. **只保留改进** —— 改进后总分必须**严格高于**改进前才 `keep`。
2. **每轮只改一个维度** —— 避免多个变更混杂导致无法归因提升/退步来源。
3. **退步即回滚** —— 用 `git revert HEAD`（创建新 commit 回滚），**不用** `reset --hard`。保留退步尝试的历史，便于复盘。
4. **commit-per-stage** —— generator-skill 的每个 pipeline 阶段（提取/结构化/DAG 合并/导航更新/验证）各自一个 commit，任一阶段退步可独立 revert，不影响已验证的前置阶段。
5. **瓶颈即停** —— 连续 N 轮（默认 3 轮）在某 skill 上无改进（涨不动），跳到下一个，避免局部最优。

### 探索性重写（可选，突破局部最优）

当 hill-climbing 连续多个 skill 都在首轮 break，提议一次「探索性重写」：

1. 选一个瓶颈 skill，`git stash` 保存当前最优版本。
2. 从头重组结构（不是微调，是重写）。
3. 重新评估：重写版 > stash 版 → 采用；否则 `git stash pop` 恢复。
4. **必须征得用户同意**后才执行。

---

## 4. 独立评分流程

> 关键原则：**评分必须用 fresh-context 子 agent，禁止自评。** 不能在生成/改进的同一上下文里「改完直接评」——这是避免「自己改自己评」偏差的硬约束。

### 4.1 评分执行步骤

```
for each 待评 skill:
  1. 结构评分（①-⑧ + ⑨双子类选择）
     - spawn fresh-context 子 agent（无生成过程记忆）
     - 读取 skill 全文 + 索引文件，逐维度打分（1-10），附扣分理由
     - 第 9 维：先判定 skill 类型，选对应子类标准评分

  2. 效果评分（实测，对 query-skill 适用）
     - 为 skill 设计 2-3 个典型测试 prompt（覆盖 happy path + 一个复杂/歧义场景）
     - spawn 子 agent：with_skill（带 skill 跑）vs baseline（不带 skill 跑）
     - 对比输出质量：是否完成用户意图 / 相比 baseline 是否提升 / 有无 skill 引入的负面影响
     - 效果反馈影响 ②④⑤ 维度（清晰度/可操作性/准确性）的校准

  3. 加权汇总 → 百分制总分 → 等级（见 §6）
  4. 记录到 results.tsv（见 §5）
```

### 4.2 eval_mode（评估模式）

| 模式 | 说明 | 适用 |
|------|------|------|
| `full_test` | spawn 子 agent 跑了测试 prompt（with vs baseline） | query-skill 默认 |
| `dry_run` | 无法 spawn 子 agent 时，读完 skill 模拟一个典型 prompt 的执行思路 | 时间/资源受限时退化 |

> 不要因为跑不了测试就跳过效果维度——`dry_run` 也比完全不看效果好，但必须在 results.tsv 标注。

### 4.3 generator-skill 的特殊处理

generator-skill 的「效果」是**生成的知识库质量**，而非单次查询。其效果验证 = 对生成产物跑一次完整 darwin 评估（即本文件 §1-§4）。因此 generator-skill 的评分是**两级递归**：

- **一级**：评估生成的知识库 skill（query-skill 类型）的 9 维分数 → 这是 meta-skill 的「实测表现」证据。
- **二级**：评估 meta-skill 本身（generator-skill 类型）的第 9 维合规性 + 结构维度。

---

## 5. results.tsv 格式

> 每次评分/改进追加一行。文件位置：skill 仓库根目录的 `darwin-results.tsv`。

```tsv
timestamp	commit	skill	old_score	new_score	status	dimension	note	eval_mode
2026-06-24T21:50	baseline	cp-kb	-	87	baseline	-	初始评估	full_test
2026-06-24T22:10	a1b2c3d	cp-kb	87	91	keep	⑥一致性	修复断裂引用 full-conformal-coverage	full_test
2026-06-24T22:25	b2c3d4e	cp-kb	91	89	revert	⑦执行效率	拆分 schema 导致导航断裂	dry_run
```

### 字段说明

| 字段 | 取值 | 说明 |
|------|------|------|
| `timestamp` | ISO 8601 | 评分时刻 |
| `commit` | git SHA / `baseline` | 对应的 commit；首次基线写 `baseline` |
| `skill` | skill 名 | 被评 skill 标识 |
| `old_score` | 数字 / `-` | 改进前分数；首次基线写 `-` |
| `new_score` | 数字 | 改进后分数 |
| `status` | `baseline` / `keep` / `revert` | 保留改进 / 回滚退步 / 基线 |
| `dimension` | 维度编号或名称 | 本轮改动针对的维度；基线写 `-` |
| `note` | 简述 | 改动摘要或扣分理由 |
| `eval_mode` | `full_test` / `dry_run` | 是否 spawn 子 agent 实测 |

---

## 6. 等级映射与质量门

| 等级 | 分数区间 | 含义 |
|------|---------|------|
| **A+** | ≥ 95 | 卓越——可作范例 |
| **A** | ≥ 90 | 优秀——仅小幅工程改进空间 |
| **A-** | ≥ 85 | 良好——核心能力达标，工程完善度可优化 |
| **B+** | ≥ 80 | **合格（质量门）**——生成成功，可交付 |
| **B** | ≥ 75 | 及格——需改进后再交付 |
| < B | < 75 | 不合格——棘轮回滚，重做 |

### 质量门（Quality Gate）

- **生成成功阈值：B+（≥ 80/100）。** 未达标的知识库 skill 视为生成失败，触发棘轮回滚或重做。
- 质量门对 query-skill 与 generator-skill **同等适用**：meta-skill 自身也须 ≥ B+（按 generator-skill 子类评第 9 维）。

---

## 7. 何时触发

| 触发场景 | 说明 | 是否必跑 |
|---------|------|---------|
| **初始化必跑** | 新知识库 skill 生成完成后，立刻跑一次完整 darwin 评估，确认是否过质量门 | ✅ 强制 |
| **schema 变化重评** | `schema/schema.md` 的节点模板/边类型/命名规范变更后，已有 skill 须重评（结构一致性可能受影响） | ✅ 强制 |
| **用户显式请求** | 用户执行 `lint --score` 或说「skill 评分」「质量检查」 | ✅ 按需 |
| **Ingest 新文献后** | 纳入新来源触发 DAG 变更，建议重评（影响 ③内容完整性/⑥一致性） | ⚠️ 建议 |
| **优化循环** | darwin 优化器主动调用本 rubric 做基线→改进→重评循环 | ⚠️ 按需 |

### 触发后的动作链

```
触发 darwin 评估
  → spawn fresh-context 子 agent（§4）
  → 9 维评分（第 9 维选双子类）
  → 加权汇总 → 等级判定（§6）
  → 写 results.tsv（§5）
  → 是否 ≥ B+？
     是 → 生成成功，交付
     否 → 棘轮回滚 / 探索性重写（§3）→ 重评，直到过门或用户叫停
```

---

## 附：与 darwin 1.0（8 维）的差异

darwin 2.0 相对花叔 darwin 1.0 的主要演进：

| 项 | darwin 1.0（8 维） | darwin 2.0（9 维） |
|----|-------------------|-------------------|
| 维度数 | 8（结构 6 + 效果 2） | 9（含元技能合规） |
| 权重 | 8/15/10/7/15/5/15/25 | 15/15/15/15/10/10/8/7/5 |
| 第 9 维 | 无 | 新增，**拆双子类**适配 meta-skill |
| 评分独立性 | 子 agent（继承） | fresh-context 子 agent（强化） |
| 棘轮机制 | git revert（继承） | + commit-per-stage 适配 pipeline |
| results.tsv | 8 列 | 9 列（+ eval_mode） |

darwin 2.0 保留了 1.0 的棘轮机制、独立子 agent 评分、results.tsv 追踪，新增了元技能合规维度并针对 meta-skill 做了双子类改造，使质量门能公平评估「生成其他 skill 的 skill」。

---

## 8. 专家顾问 Builder 三硬门（Expert Advisor Hard Gates）

> 本节适用于 `expert-advisor-builder`（DKB 扩展分支）。三硬门是**致命问题**（非扣分项），不过即判 <B+ 回滚。硬门检查紧耦合完整性与专家忠实度，确保生成的专家顾问 skill 既"有依据"又"真来自专家"。

### 8.1 三硬门总览

| 硬门 | 检查项 | 判定方式 |
|------|--------|----------|
| **① 紧耦合完整性** | 每个 3 重过的心智模型 `grounded_in ≥1` 节点，且**语义匹配**（节点真支撑该判断）；**含 anti_pattern 的 `role: refutes` 约束**（反模式必须用 refutes 指向反对的方法节点） | **fresh subagent 抽查语义**（非 lint 程序化，需理解力） |
| **② judgment 忠实度** | 每条 judgment 有真实 provenance（网采 URL HTTP 可达 / 用户材料 `locator{page,section}` 可定位），非模型编造；**含 judgment 的 `derived_from` 继承正确性**（judgment 继承的心智元素 verification 是否真实） | **fresh subagent 抽查 provenance**（验证来源真实性） |
| **③ 无孤儿判断** | judgment 的 `grounded_in` 节点都在 dag-index 里（无断裂引用） | **lint 程序化**（`pipeline/state/lint_d7.py` 扫 dag-index） |

**判定方式核心差异**：
- 存在性（硬门③）= **程序化 lint**（快、确定）
- 语义匹配 + 忠实度（硬门①②）= **fresh subagent 抽查**（慢、需判断力，合并为一次 fresh 校验）

### 8.2 硬门①：紧耦合完整性（语义匹配）

**目标**：确保每个 3 重过的心智模型真的"有依据"，且依据节点在语义上真支撑该判断（非机械挂靠）。

**检查项**：
- 心智模型（`type: mental_model`）必须有 `grounded_in ≥1` 节点
- `grounded_in` 每个节点的 `role` 与判断语义一致（`role: supports` 时节点真支撑判断，`role: refutes` 时节点真反对方观点）
- **anti_pattern 的 `role: refutes` 约束**：反模式判断的 `grounded_in` 节点必须用 `role: refutes` 明确标注反对关系（非遗漏或误标）
- 启发式（`type: heuristic`）允许 `grounded_in` 为空，但若有则必须语义匹配

**判定方式**：**fresh subagent 抽查语义**
- 每条验证：读取心智模型/判断全文 + 加载其 `grounded_in` 节点定义 → 判断节点内容是否真支撑该判断
- 失败示例：一条关于"LLM 不能推理"的判断，挂靠节点是"Transformer 架构"（语义不相关）或挂靠节点是"CoT 可提升规划能力"（语义矛盾）

**spec §4.4 降级规则的衔接**：
- 3 重全过但 `grounded_in` 完全找不到任何节点 → **丢弃**（不入库）
- 3 重全过但找到节点且 S6 判定语义不匹配 → **降级为 heuristic**（`status: demoted`，`demote_reason: semantic_mismatch`）
- 硬门① 即 S6 语义匹配判定

### 8.3 硬门②：judgment 忠实度（provenance 追溯）

**目标**：确保每条 judgment 真来自专家材料，非模型编造。忠实度是"可信度"的底线。

**检查项**：
- 网采源 judgment：`provenance.sources` 必须包含 HTTP 可达的 URL（fresh subagent 可访问验证）
- 用户材料源 judgment：`provenance.sources` 对应的 `sources/src-*.md` 必须有 `locator: {page, section}` 且可定位到具体页码/章节
- **judgment 的 `derived_from` 继承正确性**：judgment 必须正确继承其所属心智元素的 `verification` 结果（derived_from 指向的节点必须存在且确实通过三重验证）

**判定方式**：**fresh subagent 抽查**
- 网采 URL：尝试 HTTP 访问，验证 404/403/权限问题 → 失败即违反硬门②
- 用户材料：核对 PDF 第 N 页第 M 节是否真包含该判断 → 失败即违反硬门②
- **derived_from 继承**：检查 judgment 的 `derived_from` 字段指向的心智元素是否存在，且其 `verification` 确实通过（避免继承失败/误导）

**与第 9 维可审计支柱的衔接**（见 §2.3）：
- 第 9 维的"可审计"支柱要求"每个知识节点标注 provenance"
- 硬门② 是其**执行层验证**：确保标注的 provenance 真实可达、非伪造 URL/空 locator

### 8.4 硬门③：无孤儿判断（程序化 lint）

**目标**：确保 judgment 的 `grounded_in` 节点都在 dag-index 里，无断裂引用。

**检查项**：
- judgment 的 `grounded_in` 每个节点的 `node` ID 都存在于 `dag/dag-index.json`
- 心智元素的 `grounded_in` 每个节点的 `node` ID 都存在于 `dag/dag-index.json`
- 无"挂了节点 ID 但节点不存在"的孤儿判断

**判定方式**：**lint 程序化**（`pipeline/state/lint_d7.py`）
- 调用 `lint_d7.py` 的 `check_grounding_existence` 函数（已实现 Task 4.1/4.3）
- 扫描所有 judgment/心智元素的 `grounded_in` 节点 ID，逐一核对 `dag-index.json`
- 发现孤儿节点 → 报错并返回具体 judgment ID + 缺失节点 ID
- **这是唯一可程序化判定的硬门**（存在性检查无需语义理解）

**与 D7 可控性的衔接**：
- D7（可控性）要求"每个节点可追溯到来源"
- 硬门③ 确保"每个判断可追溯到存在的节点"——是 D7 在紧耦合层的强制执行

### 8.5 执行时机

三硬门在 S6 验证阶段执行（详见 `pipeline/ingest.md` §5.4），不过即触发棘轮机制（§3）。

### 8.6 与 darwin 9 维关系

三硬门是门槛（不过即 <B+），darwin 9 维是质量评分（≥80 才成功）。硬门② 与第 9维『可审计』支柱衔接：darwin 要求标注 provenance，硬门② 验证其真实性。

---

_规范版本：darwin 2.0 | 适配项目：domain-knowledge-builder meta-skill + expert-advisor-builder 扩展 | 质量门：B+ (80/100) | 三硬门：不过即回滚_
