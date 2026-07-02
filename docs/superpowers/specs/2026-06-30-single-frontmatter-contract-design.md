# 设计：硬门⑤ — 元素文件单 frontmatter 契约

> 状态：已批准（2026-06-30）｜规模：小（1 lint 函数 + 测试）
> 前序：本次会话 lint 硬门系列（①③④）

---

## 1. 动机

backlog：「每元素一个独立 .md 文件（顶部裸 frontmatter）」契约未被 lint 强制（load_mind_artifacts 正则只解析顶部块）。

**现状厘清**（探索）：
- examples 已采用「每元素独立文件」模式：`judg-*.md` / `mm-*.md` / `ap-*.md` / `heur-*.md`，每个顶部一个 frontmatter 块（数据定义）
- `judgments.md` / `mental-models.md` / `index.md` = **纯导航层**（链接到独立文件，不存元素数据）
- 风险：若未来生成时把多个元素塞进一个文件（多 frontmatter 块），`load_mind_artifacts` 只解析顶部块 → **漏元素**，且 lint 不报警

## 2. 设计（硬门⑤）

### `check_single_frontmatter(skill_root) -> list[str]`
- 遍历 `expert-mind/*.md`
- **只检查元素文件**（文件名前缀 `judg-` / `mm-` / `ap-` / `heur-`），跳过导航文件（`index` / `judgments` / `mental-models`）
- 每个元素文件：`---` 分隔符（`^---\s*$` 行）计数须 **恰好 2**（= 单 frontmatter 块：开 + 结）
- ≠ 2 → 报 issue：「含 N 个 '---'，应为 2（单 frontmatter 块），多元素须拆独立文件」

### 接入 main()
- 新增检查项「硬门⑤ 元素文件单 frontmatter」

## 3. 决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 检查范围 | 元素文件（前缀），排除导航 | 导航文件正文含 `---` 分割线，非元素；按前缀精确识别 |
| 判定 | `---` 行数 == 2 | 元素文件正文不用 `---` 分割线（frontmatter + ## 正文）；简单可靠 |
| legacy | 无 | examples 元素文件全合规（探索确认），零误报 |

## 4. 测试（TDD）

- `test_check_single_frontmatter_passes`：正常元素文件（2 个 `---`）→ 无 issue
- `test_check_single_frontmatter_flags_multi_block`：元素文件含 4 个 `---`（2 块）→ 报 issue
- `test_check_single_frontmatter_skips_nav_files`：导航文件（index.md，多 `---`）→ 不报

## 5. 验收

- [ ] 3 测试绿，全量无回归
- [ ] 4 examples 硬门⑤全 ✓（元素文件全合规）
- [ ] schema/lint.md 同步硬门⑤

## 6. 不做（YAGNI）

- 不检查导航文件结构（它们是链接层，灵活）
- 不验证 frontmatter 内容（由硬门①③④覆盖）
