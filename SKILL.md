---
name: domain-knowledge-builder
description: 构建/生成领域知识库 skill 的 meta-skill——给 N 篇学术论文（PDF/EPUB/DOCX）+ 领域名，自动产出一个结构等价于共形预测实例的 A 级领域知识库（DAG 知识节点 + 心智模型 + 查询协议 + 诚实边界）。触发词：「给 X 领域建知识库」「把这些论文变成 skill」「蒸馏领域」「论文→skill」「DAG 知识库」「domain knowledge builder」。区别于查询型知识库（只读），本 skill 是生成器（generator-skill），会 fan-out 提取 + 受控写入 + darwin 质量门。
---

# Domain Knowledge Builder — 领域知识库生成器

> **给我 N 篇论文 + 领域名 → 产出一个可查询的 A 级领域知识库 skill。**
> 知识库结构：DAG（5 类型节点 + 10 关系）+ 心智模型 + Query 协议 + 诚实边界。
> 质量门：darwin 2.0 的 9 维评分，≥B+ (80) 才算生成成功。

---

## 核心心智模型

### 1. 知识 ≠ 定义堆砌

一个能用的领域知识库不是把定义/定理逐条搬进来，而是提炼**这个领域用什么镜片看世界**（心智模型），再用知识节点支撑镜片。问"我的数据流非交换，CP 会怎么帮我"——纯定义堆砌答不出，心智模型驱动的知识库能推断立场。所以 ingest 流程必须有心智模型提炼步骤（S5），不是只提取节点。

### 2. Karpathy 生命周期 × DAG 结构

- **Karpathy LLM Wiki 提供「生命周期」**：raw（不可变源）→ wiki（LLM 维护）→ SCHEMA（规范）三层 + Ingest/Query/Lint 三工作流。知识库是会成长的有机体，不是一次提取的快照。
- **DAG 提供「结构」**：节点间不只是分类，是关系——`guarantees`/`generalizes`/`contradicts`/`depends_on`。定理 A 推出定理 B、方法 C 与方法 D 矛盾，这些关系是领域知识的核心，扁平目录承载不了。
- **融合**：Karpathy 管"知识怎么长"（生命周期），DAG 管"知识怎么连"（结构）。

### 3. 生成器必须可控（D7）

meta-skill ≠ 普通 skill 的本质是**生成其他 skill**——大量 FS 写、subagent spawn、网络。这必须可控：每次 ingest 可 checkpoint 恢复、darwin 不过门可 git revert、每个节点可追溯（provenance）、同论文重跑产生同 node ID（determinism）。否则 6 个月后不可维护。这四支柱（可回滚/可审计/确定性/预检）是 generator-skill 合规的标准（darwin 第 9 维 generator 子类）。

---

## 何时用 / 何时不用

**用**：
- "把这几篇论文变成可查询的知识库"
- "给 X 领域建一个 DAG 知识库"
- "我有 N 篇 PDF，想要一个能推断立场的领域助手"

**不用**（路由到其他 skill）：
- "什么是 Split CP？" → 查询已存在的 CP 知识库（`examples/conformal-prediction`）
- "总结这本书" → 用 book-to-skill 直接生成单本书 skill
- "蒸馏一个人怎么想" → 用 nuwa-skill

---

## 架构（5 层）

```
domain-knowledge-skill/
├── SKILL.md                       # 本文件（meta-skill 入口）
├── schema/schema.md               # 知识规范（5 类型 + 10 关系 + D7 可控性）
├── pipeline/                      # Ingest/Query/Lint 工作流
│   ├── ingest.md                  # 7 步流水线契约（S1-S7）
│   ├── query.md                   # 5 步 DAG 遍历查询
│   ├── lint.md                    # 结构 + Generator 合规检查
│   ├── run-dag-pipeline.js        # workflow 编排脚本
│   └── state/                     # D7 运行时
│       ├── init_run.py            # UUID + git + run-manifest + preflight
│       └── lint_d7.py             # 四支柱 Lint
├── engines/                       # 复用的引擎
│   ├── book_to_skill/             # virgiliojr94 提取引擎（technical 模式）
│   ├── darwin-rubric.md           # 9 维质量评分（第 9 维双子类）
│   └── nuwa-validation.md         # 领域化三重验证
├── references/                    # 模板（规划中）
└── examples/
    └── conformal-prediction/      # 黄金参照（88 分 A-，懒加载）
```

---

## 7 步 Ingest 流水线（D3 阶段性质拆分）

```
确定性（workflow fan-out）         交互/判断（subagent chain）
─────────────────────            ─────────────────────
S1 提取 ──┬─▶ S2×N 并行 ──┐
          └─▶ ...        ├─▶ S3 合并 ──▶ S4 导航 ──▶ S5 心智模型 ──▶ S6 验证 ──▶ S7 组装 ──▶ darwin 门
                          │   (contradicts    (并行 3)   (三重验证)    (fresh)    (<4K)     (≥B+)
                          │    人工确认)
```

**详细契约见 `pipeline/ingest.md`**。关键约束：
- S1 必做 docling preflight（schema §12.4，technical 模式硬依赖）
- S2 节点 ID 遵 `<type>-<source>-<canonical-term>`（schema §10 Determinism）
- S3遇 `contradicts`/`does_not_guarantee` 边必须 `contact_supervisor` 人工确认
- S5 加载 `engines/nuwa-validation.md` 做三重验证
- S6/S7 用 fresh-context 子 agent（独立验证/评分，禁自评）
- 全程每节点写 provenance（generated_by_step/run_id/source_span）

---

## 质量门（darwin 2.0，9 维）

加载 `engines/darwin-rubric.md`，fresh-context 子 agent 评分：

| 维度 | 权重 | 关注点 |
|------|------|--------|
| ①结构完整性 ②清晰度 ③内容完整性 ④可操作性 | 15%×4 | frontmatter/工作流/覆盖/可执行 |
| ⑤准确性 ⑥一致性 | 10%×2 | 定理原文精确/无断裂引用 |
| ⑦执行效率 ⑧鲁棒性 | 8%/7% | token 预算/诚实边界 |
| ⑨元技能合规 | 5% | **generator-skill 子类**：四支柱 |

**第 9 维双子类**（oracle 洞察）：query-skill（CP 型，只读）vs generator-skill（本 skill 型，允许受控写入但须满足四支柱：可回滚/可审计/确定性/预检）。这让生成器能公平过质量门。

**棘轮机制**：darwin <B+ → `git revert` 最后 stage → 诊断低分维度 → 修复重评。连续 3 轮无改进 → 提议探索性重写。

---

## 5 个参考源的去向

| 源 | 去向 | 复用方式 |
|----|------|---------|
| **Karpathy LLM Wiki** | `schema/` + `pipeline/` | 干净继承：3 层架构 + Ingest/Query/Lint 生命周期 |
| **book-to-skill** | `engines/book_to_skill/` | 干净 vendor：提取引擎（technical 模式保留公式） |
| **nuwa-skill** | `engines/nuwa-validation.md` | 方法论提炼：三重验证（去 expression DNA） |
| **darwin-skill** | `engines/darwin-rubric.md` | 双源重构：validation-report 的 9 维 + 旧版 8 维对照 |
| **dag-executor** | 仅哲学参考 | wave-based 并行 + 文件锁（实现用 pi workflow/subagent） |

---

## examples/conformal-prediction（黄金参照）

懒加载——不参与默认 skill 路由，显式请求时激活：
- v1.1.0 / 50 节点 / 138 边 / 0 断裂 / darwin 88 分（A-）
- 3 篇来源（Angelopoulos 2022 / Teneggi 2025 / Min 2026）
- 用法：(1) 新领域 ingest 时作为质量基准；(2) 用户显式查"共形预测"时加载

---

## 约束与诚实边界

**硬约束**：
- docling 是 technical 模式硬依赖（学术论文没公式=没价值，不可牺牲）
- SKILL.md body <4K tokens（compaction 从末尾截断）
- 所有节点 provenance 必填（新 ingest）
- generated skill 路径只用 skill-root-relative（防链接断裂）

**做不到**：
- 蒸馏不了直觉——框架能提取，灵感不能
- 覆盖不了领域所有论文——只覆盖用户提供的来源
- 自动判断不了来源质量——garbage in garbage out（低质量论文 → 低质量知识库）
- 替代不了专家判断——contradicts 边必须人工确认

**已知局限**：
- docling 版本漂移可能静默降质提取（无测试捕获）
- canonical-term 的 LLM 抽取非完全确定性（同论文两次抽取可能差 hash，Lint 会报告）
- 大论文（>50K tokens）提取成本高（建议分批 ingest）

---

## 快速上手

```
用户: 给我建一个 diffusion-models 领域知识库，论文在 ~/papers/ddpm.pdf, ~/papers/score-sde.pdf

→ 本 skill:
  1. 确认领域 + 来源 + preflight docling
  2. 跑 7 步 pipeline（pipeline/ingest.md）
  3. darwin 评分，≥B+ 则交付生成的 skill 到 ~/.pi/agent/skills/diffusion-models/
  4. 用户可后续查询该生成的 skill
```

详见 `pipeline/ingest.md` 的完整契约。

---

_本 meta-skill 版本：v0.1 | 5 源复用 + D7 可控性 + darwin 2.0 质量门 | 黄金参照：examples/conformal-prediction (88/A-)_
