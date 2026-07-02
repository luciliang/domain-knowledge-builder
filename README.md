# Domain Knowledge Builder — 领域知识库生成器（Meta-Skill）

> **给我 N 篇学术论文 + 领域名 → 自动产出一个可查询的 A 级领域知识库 skill。**
>
> 知识库结构：DAG（5 类型节点 + 10 关系）+ 心智模型 + Query 协议 + 诚实边界。
> 质量门：darwin 2.0 的 9 维评分，≥B+ (80) 才算生成成功。

这是一个 **meta-skill**——它的职责不是回答领域问题，而是**生成其他可回答领域问题的知识库 skill**。

## 它解决什么问题

读论文有三种深度：
1. **检索（RAG）**：每次问都从原文找——重复劳动，无累积
2. **总结**：一次性摘要——丢失结构，无法推理
3. **蒸馏成知识库**：把论文的定理/方法/实验/洞察提炼成相互关联的 DAG 节点 + 领域心智模型——**可累积、可推理、可查询**

本 meta-skill 做第三件事。它的产物是一个**结构等价于 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) + DAG 关系图**的 skill，可用作该领域的思维顾问。

## 架构（5 层）

```
domain-knowledge-builder/
├── SKILL.md                       # 入口（生成器，<4K tokens）
├── schema/schema.md               # 知识规范（5 类型 + 10 关系 + D7 可控性）
├── pipeline/                      # Ingest/Query/Lint 工作流
│   ├── ingest.md                  # 7 步流水线契约（S1-S7）
│   ├── query.md                   # 5 步 DAG 遍历查询
│   ├── lint.md                    # 结构 + Generator 合规检查
│   ├── run-dag-pipeline.js        # workflow 编排脚本
│   └── state/
│       ├── init_run.py            # UUID + git + run-manifest + preflight
│       └── lint_d7.py             # 四支柱 Lint
├── engines/                       # 复用的引擎
│   ├── book_to_skill/             # vendored 自 virgiliojr94 (MIT)，提取引擎
│   ├── darwin-rubric.md           # 9 维质量评分（第 9 维双子类）
│   └── nuwa-validation.md         # 领域化三重验证
├── references/                    # 模板（待补）
└── examples/
    ├── conformal-prediction/      # 黄金参照（darwin 88/A-，领域知识库模式）
    ├── tengjiaye-advisor/       # Expert Advisor：滕佳烨心模+判断+知识（v1.0）
    └── hinton-advisor/          # Expert Advisor：Hinton 模式验证（示例级）
    └── diffusion-models/          # 首个生成实例（darwin 84.70/B+，领域知识库模式）
```

## 7 步 Ingest 流水线

```
确定性（workflow fan-out）         交互/判断（subagent chain）
─────────────────────            ─────────────────────
S1 提取 ──┬─▶ S2×N 并行 ──┐
          └─▶ ...        ├─▶ S3 合并 ──▶ S4 导航 ──▶ S5 心智模型 ──▶ S6 验证 ──▶ S7 组装 ──▶ darwin 门
                          │   (contradicts    (并行 3)   (三重验证)    (fresh)    (<4K)     (≥B+)
                          │    人工确认)
```

| Stage | 类型 | 职责 |
|-------|------|------|
| S1 提取 | workflow | pdftotext/docling 提取 PDF → full-text.txt |
| S2 知识提取 | workflow fan-out | 并行提取每篇论文的知识节点（含 D7 provenance）|
| S3 DAG 合并 | subagent | 跨源合并 + `contradicts` 边人工确认 |
| S4 导航 | workflow | index/log/overview 三文件 |
| S5 心智模型 | subagent | 三重验证提炼 3-7 个领域镜片 |
| S6 验证 | fresh subagent | 独立验证（不继承构建过程）|
| S7 组装 | subagent | SKILL.md（<4K tokens）|
| darwin | fresh subagent | 9 维评分，<B+ 则 git revert |

## D7 生成器可控性层

meta-skill 与普通 skill 的本质区别是**生成其他 skill**——大量 FS 写、subagent spawn、网络。这必须可控。本 meta-skill 实现了 5 项机制（对应 darwin 第 9 维 generator-skill 子类的四支柱）：

| 机制 | 实现 |
|------|------|
| **Checkpoint** | `pipeline/state/run-manifest.json` 记录每个 stage，失败可从最后 done 的 stage 恢复 |
| **Rollback** | 生成的 skill 目录 `git init` + commit-per-stage；darwin <B+ 则 `git revert` |
| **Determinism** | 节点 ID 遵 `<type>-<source>-<canonical-term>`，同论文重 ingest 产生同 ID（幂等）|
| **Provenance** | 每节点 frontmatter 含 `generated_by_step`/`run_id`/`source_span`，6 个月后可追溯 |
| **路径确定性** | 节点 .md 只用 skill-root-relative 路径，禁绝对/meta-relative（防链接断裂）|

`pipeline/state/lint_d7.py` 是这 5 项的可执行检查器。

## 质量门：darwin 2.0（9 维，第 9 维双子类）

| 维度 | 权重 | 关注点 |
|------|------|--------|
| ①结构完整性 ②清晰度 ③内容完整性 ④可操作性 | 15%×4 | frontmatter/工作流/覆盖/可执行 |
| ⑤准确性 ⑥一致性 | 10%×2 | 定理原文精确/无断裂引用 |
| ⑦执行效率 ⑧鲁棒性 | 8%/7% | token 预算/诚实边界 |
| ⑨元技能合规 | 5% | **generator-skill 子类**：四支柱 |

**第 9 维双子类**（关键设计）：
- `query-skill` 子类（CP 型，只读）：奖励"不做外部操作"
- `generator-skill` 子类（本 meta-skill 型）：允许受控写入 + spawn + 网络，但须满足四支柱

这让生成器能公平过质量门（否则按 query-skill 标准，meta-skill 必然因"做外部操作"在这维得 0 分）。

## 5 个参考源的去向

| 源 | 去向 | 复用方式 |
|----|------|---------|
| [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | schema + pipeline | 干净继承：3 层架构 + Ingest/Query/Lint 生命周期 |
| [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) | engines/book_to_skill/ | 干净 vendor (MIT)：提取引擎（technical 模式保留公式）|
| [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) | engines/nuwa-validation.md | 方法论提炼：三重验证（去 expression DNA）|
| [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill) | engines/darwin-rubric.md | 双源重构：9 维 + 第 9 维双子类 |
| dag-executor | 仅哲学参考 | wave-based 并行（实现用 pi workflow/subagent）|

## 安装

### 前置依赖

- **pi**（coding agent harness，提供 workflow + subagent 编排）
- **docling**（technical 模式硬依赖，保留论文公式）：
  ```bash
  pip install docling
  # 国内经代理若 curl 18 失败，可降级 pdftotext（pdftotext 已含于 poppler）
  ```

### 安装步骤

```bash
# 1. clone
git clone https://github.com/luciliang/domain-knowledge-builder.git
# 2. 放到 pi 的 skills 目录
cp -R domain-knowledge-builder ~/.pi/agent/skills/
# 3. 装好后告诉 pi agent
#    "给 X 领域建知识库，论文在 ~/papers/xxx.pdf"
```

### 从 example 恢复黄金参照（可选）

`examples/conformal-prediction/raw/sources/` 因版权不含 PDF。若要完整复现 CP 黄金参照：
- 从 [arxiv 2107.07511](https://arxiv.org/abs/2107.07511) 下 Angelopoulos & Bates 2022
- 其他两篇见 `examples/conformal-prediction/wiki/sources/*.md` 的引用

## 使用示例

```
用户: 给我建一个 graph-neural-networks 领域知识库，论文在 ~/papers/gcn.pdf, ~/papers/gat.pdf

→ meta-skill:
  1. preflight docling + 初始化 run-manifest
  2. 跑 7 步 pipeline（S1-S7）
  3. darwin 评分，≥B+ 则交付到 ~/.pi/agent/skills/graph-neural-networks/
  4. 用户可后续查询该 skill
```

## 已验证的实例

| 实例 | 类型 | 来源 | 节点/边 | darwin | 说明 |
|------|------|------|---------|--------|------|
| `examples/conformal-prediction` | 领域知识库 | 3 篇 CP 论文 | 50/138 | **88 A-** | 黄金参照（人工策展 v1.1.0）|
| `examples/diffusion-models` | 领域知识库 | DDPM + Score-SDE | 30/53 | **84.70 B+** | 自动生成（双源，含 11 跨源关系）|
| `examples/tengjiaye-advisor` | 专家顾问 | 8 篇 CP 论文 | 9 节点 | N/A | Expert Advisor：4 心模+6 判断+9 知识节点 |
| `examples/hinton-advisor` | 专家顾问 | Hinton 论文 + 访谈 | — | N/A | Expert Advisor 模式验证（示例级）|

## 已知局限

- **docling 安装可能受阻**：国内经代理装 docling 时 `docling-parse` 需编译 4 个 C 库（lcms2/openjpeg/jpeg/json），github clone 可能 curl 18。降级 pdftotext 可跑通流程但丢公式格式。
- **ar5iv HTML 是更优提取源**：实测对 arxiv 论文，`ar5iv.labs.arxiv.org/html/<id>` 的 HTML 把 LaTeX 存于 `<annotation>`，提取后 663 公式完整保留，质量优于 pdftotext 且经代理下载更稳定。
- **canonical-term 非完全确定**：LLM 抽取节点命名实体两次可能差 hash，lint 会报告。
- **大论文提取成本高**：>50K tokens 的论文需 REPL 探测（grep+sed），不能全读。

## 进化 v1.0（2026-07-02）

根据达尔文.skill 2.0 流程对 meta-skill 进行一轮进化，针对三种蒸馏系统的实际对比测试暴露的缺陷：

### 核心改进

**① S5 心模抽象层级检验**
- 新增方法论/原则/结论三级判定标准
- 追问提升协议 + 跨域迁移测试
- Generative 验证升级（未见领域问题的推理链测试）
- 确保产出的是可迁移的思维操作，而非领域具体的结论

**② 模式0 元批判（Meta-Critique）**
- 所有用户问题先经：问题假设检查 → 裂缝检查 → 指标检查
- 问题本身隐含不合理假设 → 先重新定义再进入知识查询
- 防止"直接开干"而不质疑问题本身的合理性

**③ 生成式判断引擎**
- 预制立场（静态结论）→ 生成规则（trigger_pattern + inference_steps + fallback）
- 跨域迁移从"匹配已有判断"提升至"按推理规则生成新判断"

### 进化评分
- 进化前：67.36/100（C+）
- 进化后：88.00/100（B+）
- Judge 盲评 PASS，用户确认 ✅

### 提交历史
详见 PR #3：心模抽象层级检验 + 元批判模式 + 生成式判断引擎

## 许可证

MIT（见 `LICENSE`），但 `engines/book_to_skill/` 遵循其原 [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) 的 MIT 许可。

## 致谢

本 meta-skill 站在以下工作的肩膀上：
- **Andrej Karpathy** — [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式
- **virgiliojr94** — [book-to-skill](https://github.com/virgiliojr94/book-to-skill) 提取引擎
- **花叔 (alchaincyf)** — [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) 三重验证方法论 + [darwin-skill](https://github.com/alchaincyf/darwin-skill) 质量评分

_本 meta-skill 在 [pi coding agent](https://github.com/earendil-works/pi-coding-agent) 环境下设计与验证。_
