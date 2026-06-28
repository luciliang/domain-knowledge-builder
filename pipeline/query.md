# Query 工作流 — 心智模型引导的 DAG 遍历查询

> 本文件是 domain-knowledge-builder **生成的知识库 skill**被查询时遵循的流程。
> 对应 schema §7。生成的每个知识库 skill 的 SKILL.md 会内嵌此协议的精简版。

---

## 0. 何时触发

用户在已生成的领域知识库 skill 上下文中提问：
- "什么是 X？" / "X 和 Y 有什么区别？"
- "如何评估 / 设计 / 选择 X？"
- "比较 A 和 B"

**不触发**（应路由到 builder meta-skill）：
- "给 X 领域建知识库" / "把这些论文变成 skill"

---

## 1. 5 步查询协议

### Step 1: 问题分析
- 判断问题涉及哪些概念/知识类型（def/thm/meth/exp/ins）
- 关系类型定义见 `schema/schema.md` §3（仅首次或遗忘时查阅；日常查询不读 schema.md，直接按 dag-index.json 的 edges 字段遍历）

### Step 2: DAG 遍历（读 dag-index.json）
- 从问题中的概念出发，沿关系边扩展
- **剪枝规则**：控制在 3-5 个节点（每个 ~1K tokens → 总共 ~3-5K tokens）
- **优先级**：theorem > definition > method > experiment > insight
- **冲突加载**：`contradicts` / `does_not_guarantee` 命中 → 同时加载双方

### Step 3: 按需加载
- 只读取选中的 `wiki/knowledge/*.md`
- 必要时从 `wiki/sources/*.md` 补充（触发条件：需要来源上下文 / 节点信息不足 / 用户问"哪篇论文提出的"）

### Step 4: 心智模型综合分析
- 用心智模型（`wiki/mental-models.md`）+ 加载的知识节点 → 有理有据的回答
- **每个论点必须引用具体节点 ID**（如"据 `thm-split-cp-coverage`..."）
- 知识不足以完整回答 → 明确说明缺什么（诚实优先于编造）

### Step 5: 可选——回答存档
- 有长期价值的回答（如跨源综合、复杂对比）→ 写入 `wiki/syntheses/<topic>.md`
- 存档规则：只创建新文件，不合入现有 knowledge 节点（archive 是综合答案，非原始知识）

---

## 2. 加载效率提示（token 预算）

| 查询类型 | 加载内容 | tokens |
|---------|---------|--------|
| **核心查询** | 只 SKILL.md（心智模型 + 查询协议 + 节点索引） | ~3K |
| **标准查询** | SKILL.md + dag-index.json + 3-5 个知识节点 | ~8-11K |
| **Ingest/Lint** | 额外加 schema/schema.md | +3K |

**原则**：schema 细节（节点模板、命名规范）仅在创建/修改节点时加载，查询时不读。

---

## 3. 查询质量自检

回答前自问：
- [ ] 每个论点引用了具体节点 ID？
- [ ] 用了心智模型组织答案（而非照搬节点内容）？
- [ ] 矛盾/争议是否同时呈现双方？
- [ ] 知识缺口是否诚实标注？

---

_本工作流对应 schema §7 | 生成 skill 的 SKILL.md 内嵌精简版_
