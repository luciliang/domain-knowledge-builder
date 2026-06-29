# 设计：节点 ID 格式严格化 + tengjiaye 边 id 修复

> 状态：已批准（2026-06-29）｜规模：中（lint 代码 + 1 节点迁移 + 17 边数据修复）
> 前序：`2026-06-29-deterministic-edge-id-design.md`（确定性边 ID 公式，已实现）

---

## 1. 动机

继确定性边 ID 公式落地后，本次解决两个遗留：

1. **节点 ID 格式校验形同虚设** —— `_check_deterministic_data` 节点循环从未调用 `NODE_ID_RE`（lint_d7.py 原空操作 `pass`），§10 节点 ID 规范无程序化保证。
2. **tengjiaye-advisor 数据缺陷** —— 17 条边缺 `id` 字段（被 lint 的 `e.get('id','')` 读成空串）；1 个节点 `def-exchangeability` 是 2 段短 id（不符 3 段规范）。

## 2. 决策（已与用户确认）

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 节点格式严格化策略 | 启用 NODE_ID_RE + legacy_ok 宽容 | 与边 ID 公式完全对称；新生成强制 3 段，历史宽容 |
| 迁移范围 | **只迁移 tengjiaye 的 1 个**（`def-exchangeability`） | 配合边 id 修复让 tengjiaye 自洽毕业；conformal 4 个短 id 引用面 10–20 文件/id，全迁移是跨 50+ 文件大重构，收益低 → legacy 宽容 |
| 边 id 修复 | 统一公式覆盖 17 条 | 一致性；from/relation/to 已确认全完整 |
| source-slug 规范化 | `angelopoulosbates2022` | source `src-angelopoulos-bates-2022` 含 `-` 不符正则第二段，去 `src-` 前缀 + 去 `-` |

## 3. 改动清单

### 3.1 `pipeline/state/lint_d7.py` + `test_lint_d7.py`（TDD）
- `_check_deterministic_data` 节点循环新增 NODE_ID_RE 检查：不符 → `legacy_ok` 时 `legacy_node_ids`，否则 `bad_node_format`
- 返回结构新增 `bad_node_format` / `legacy_node_ids`
- 测试：`test_..._flags_non_formula_node_id`（严格报错）/ `test_..._legacy_ok_tolerates_node_id`（宽容）

### 3.2 迁移 `def-exchangeability`（脚本化）
- 新 id：`def-angelopoulosbates2022-exchangeability`
- 机制：建 `old→new` 映射 → 全局词边界精确替换（防子串误匹配）→ 重命名 `dag/knowledge/def-exchangeability.md` → 更新 dag-index.json（node.id / edges.from-to / file）
- 验证：迁移后 `grep -rw def-exchangeability`（旧 id 作完整 token）应为 0 残留

### 3.3 tengjiaye 17 条边 id 覆盖
- `dag-index.json` 每条边：`edge["id"] = compute_edge_id(edge)`
- 单文件改动

## 4. Legacy 策略

- `--legacy-ok` 统一宽容历史旧格式：缺 provenance 节点 + 旧 slug 边 ID + **短节点 id**（本次新增）
- conformal-prediction 的 4 个短节点 id（`def-crc`/`meth-aps`/`meth-cqr`/`meth-graphcp`）走宽容，不迁移

## 5. 验收标准

- [ ] 新增节点格式测试全绿，全量测试无回归
- [ ] tengjiaye **不带 `--legacy-ok`** 确定性维度全过（边 id 符公式 + 节点 id 符 NODE_ID_RE + 无重复）→ **毕业自洽**
- [ ] 迁移后 grep `def-exchangeability` 旧 id 零残留
- [ ] conformal `--legacy-ok` 过；hinton / diffusion **严格模式**全过

## 6. 不做（YAGNI）

- 不迁移 conformal 的 4 个短节点 id（legacy 宽容）
- 不统一 source 字段格式（conformal 用 `author+year`，tengjiaye 用 `src-author-year`）—— 独立议题
- 不改其他 examples 的边 id（上次决策已定）
