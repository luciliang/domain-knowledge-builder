# Domain Knowledge Skill — 项目计划

> 创建时间：2026-06-27  
> 项目：统计校准与共形预测领域知识库 Skill  
> 当前版本：v1.1.0  
> 打包文件：`domain-knowledge-skill.tar.gz`（8.8 MB）

---

## 📊 项目概况

| 指标 | 数值 |
|------|------|
| 知识来源 | 3 篇核心论文 |
| 知识节点 | 50 个 |
| 关系边 | 138 条 |
| 断裂引用 | 0（首轮进化已修复） |
| Darwin MVP 评分 | 87/100（A-） |
| 文件总数 | 74 |
| 目录大小 | 11 MB |

### 来源论文
1. **Angelopoulos & Bates 2022** — *A Gentle Introduction to Conformal Prediction*（51页, 34K tokens）
2. **Teneggi et al. 2025** — *Conformal Risk Control for Semantic UQ in CT*（12页, 5.8K tokens）
3. **Min et al. 2026** — *A Unified Theory of Conditional Coverage in CP*（157页, 67K tokens）

---

## ✅ 已完成

### Phase 1：知识蒸馏（6/24，女娲 7 步 DAG 流水线）
- [x] S1：3 篇 PDF 文本提取（pdftotext，共 220 页 / 107K tokens）
- [x] S2：逐篇知识结构化提取（extraction-p1/p3/p4.json）
- [x] S3：跨论文 DAG 合并（49 节点 / 135 边，含 9 条跨论文连接边）
- [x] S4：schema 验证（schema.md 节点模板 + 边类型定义）
- [x] S5：SKILL.md 撰写（4 个心智模型 + 查询协议 + 节点索引 + 术语映射 + 诚实边界）
- [x] S6：wiki 知识节点写入（50 个 .md 文件，100% schema 合规）
- [x] S7：dag-index.json 生成 + 验证报告

### Phase 2：Darwin MVP 评估（6/24）
- [x] 9 维评分：87/100（A-）
  - 结构完整性 9 | 清晰度 9 | 内容完整性 8 | 可操作性 9 | 准确性 9
  - 一致性 8 | 执行效率 8 | 鲁棒性 8 | 元技能合规 10
- [x] 端到端查询测试：38/40（准确性 10 + 引用完整性 10 + 知识缺口处理 10 + token 效率 8）
- [x] 改进建议 Top 5 已记录

### Phase 3：首轮进化 v1.1（6/25）
- [x] 修复断裂引用（`thm-full-cp-coverage` 节点补充）
- [x] 节点数 49 → 50，边数 135 → 138
- [x] 断裂引用 1 → 0
- [x] 版本号升至 v1.1.0

### 工程基础设施
- [x] dag/merge.py & merge.js（跨论文合并脚本）
- [x] dag/validation-report.md（完整评估报告）
- [x] wiki/index.md（知识节点索引）
- [x] wiki/mental-models.md（心智模型详情）
- [x] wiki/log.md（变更日志）
- [x] raw/sources/（3 份原始 PDF 保留）

---

## ⏳ 未完成

### Priority 1：Darwin 第二轮复评（judge-r1）
- [ ] 使用 darwin-judge-r1 对 v1.1 版本重新评分
- [ ] 目标：维持 ≥87 分（棘齿机制，不降级）
- [ ] 若通过，v1.1 确认为稳定版本
- **阻塞原因**：需触发 Darwin skill 的 judge 模式

### Priority 2：改进建议（来自 MVP 评估报告）
- [ ] **#2 优化 token 加载效率**（中优先级）
  - schema.md 细节移到按需加载路径
  - 基础加载从 6K → ~2K tokens
- [ ] **#3 增加 Getting Started 示例查询**（中优先级）
  - SKILL.md 中补充 2-3 个完整查询路径示例
- [ ] **#4 条件覆盖评估对比表**（低优先级）
  - 新建 `ins-coverage-metrics-comparison` 节点
  - FSC/SSC/ECE 适用场景 + 优劣势对比
- [ ] **#5 扩展来源覆盖**（低优先级）
  - Barber et al. 2020 — Cross-conformal prediction
  - Gibbs & Candes 2021 — Adaptive conformal inference（online setting）
  - Calibrated LLM / Semantic entropy

### Priority 3：Meta-skill 重组（独立大任务）
- [ ] 盘点女娲 skill 核心能力（多源并行采集、三重验证、Agentic Protocol）
- [ ] 盘点 book-to-skill 核心能力（文本提取 pipeline、REPL 大文档探测、增量更新）
- [ ] 盘点 Darwin skill 核心能力（独立子 agent 评估、棘轮机制）
- [ ] 盘点 DAG Executor 核心能力（多步骤编排）
- [ ] 设计 meta-skill 架构，整合上述能力为统一接口

### Priority 4：领域知识扩展（持续迭代）
- [ ] Ingest 更多 CP/UQ 文献（按 Ingest 工作流逐步纳入）
- [ ] 每篇新来源触发 Step 5 验证 + DAG 更新
- [ ] 长期目标：覆盖 10+ 篇核心文献，节点数 100+

---

## 📁 打包内容

```
domain-knowledge-skill.tar.gz (8.8 MB)
├── SKILL.md              # 入口文件：心智模型 + 查询协议 + 节点索引
├── plan.md               # 本文件
├── metadata.json         # 元数据（来源、token 统计）
├── mvp-plan.yaml         # MVP 阶段计划（归档）
├── README.md             # 项目说明
├── full_text.txt         # 三篇论文合并全文（归档）
├── extraction-p{1,3,4}.json  # 逐篇知识提取结果
├── schema/
│   └── schema.md         # 节点模板 + DAG 边类型定义
├── dag/
│   ├── dag-index.json    # DAG 索引（50 节点 / 138 边）
│   ├── validation-report.md  # Darwin MVP 评估报告（87/100）
│   ├── merge-report.md   # 合并报告
│   ├── merge.py / merge.js  # 合并脚本
├── wiki/
│   ├── overview.md       # 知识库概览
│   ├── index.md          # 节点索引
│   ├── mental-models.md  # 心智模型详情
│   ├── log.md            # 变更日志
│   ├── sources/          # 来源论文摘要 (3 篇)
│   ├── knowledge/        # 知识节点 (50 个 .md)
│   └── syntheses/        # 综合分析（待填充）
├── raw/
│   └── sources/          # 原始 PDF (3 份)
└── .dreams/              # Darwin 进化历史快照
```

---

## 🕐 时间线

| 日期 | 事件 |
|------|------|
| 2026-06-24 | Phase 1 完成：知识蒸馏（49节点/135边） |
| 2026-06-24 | Phase 2 完成：Darwin MVP 评估 87/100 |
| 2026-06-25 | Phase 3 完成：首轮进化 v1.1（50节点/138边/0断裂） |
| 2026-06-27 | 打包 + plan.md 撰写 |
| 待定 | Darwin Round 2 复评 |
| 待定 | 改进建议 #2-#5 实施 |
| 待定 | Meta-skill 重组 |

---

_最后更新：2026-06-27 11:42 CST_
