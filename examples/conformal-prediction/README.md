# Domain Knowledge Skill — 领域知识库

> Karpathy 三层架构 + DAG 知识结构化 + 心智模型引导查询

## 三个组件复用映射

| 组件 | 来源 | 用途 |
|------|------|------|
| 三层架构 + Ingest/Query/Lint | Karpathy LLM Wiki | 整体框架 |
| extract.py (technical 模式) | book-to-skill | PDF → 文本提取 |
| 三重验证 | 女娲 Skill | 心智模型提炼 |
| DAG Executor | dag-executor skill | 多文献并行构建流水线 |
| DAG 知识结构 + 按需加载 | 新设计 | 知识关系表达和查询导航 |

## 目录结构

```
domain-knowledge-skill/
├── schema/
│   └── schema.md              # 知识提取规范（LLM 的规则手册）
├── raw/
│   └── sources/               # PDF 原件（不可变）
│       ├── p1.pdf
│       ├── p2.pdf
│       └── p3.pdf
├── wiki/
│   ├── index.md               # 知识目录导航
│   ├── log.md                 # 变更记录（append-only）
│   ├── overview.md            # 领域全局概览
│   ├── mental-models.md       # 心智模型 + 决策启发式
│   ├── knowledge/             # 段落级知识节点（按需加载）
│   │   ├── def-coverage.md
│   │   ├── thm-glivenko-cantelli.md
│   │   └── ...
│   ├── sources/               # 每篇来源的摘要
│   │   ├── src-p1.md
│   │   └── ...
│   ├── entities/              # 人物、机构
│   ├── concepts/              # 高层概念聚合
│   └── syntheses/             # 查询回答存档
├── dag/
│   └── dag-index.json         # 知识关系 DAG（核心索引）
├── mvp-plan.yaml              # MVP DAG 流水线计划
└── SKILL.md                   # 最终产物（<4K tokens 索引）
```

## 核心设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 知识关系 | 多维 DAG | 支持依赖、引用、概念关联等多种关系 |
| 交互模式 | 抛问题 → 系统自动找知识 + 专家分析 | 用户不需要知道知识在哪里 |
| 知识粒度 | 段节级（500-2000 tokens） | 精确不冗余，按需加载 |
| DAG 构建 | LLM 自动（schema 驱动） | 人类只审核，不做 bookkeeping |
| 心智模型 | 女娲三重验证提炼 | 从论文中提炼，非泛泛思维框架 |
| 验证 | 独立子 agent 抽查 | 定理表述 vs 原文比对 |

## 当前状态

- [x] schema/schema.md 写完
- [x] mvp-plan.yaml 写完
- [ ] 确认 3 篇论文并放入 raw/sources/
- [ ] 运行 DAG 流水线
- [ ] 验证 Query 效果
- [ ] 迭代 schema 规范
