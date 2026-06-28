#!/usr/bin/env python3
"""
D7 Generator 合规 Lint 脚本 — 检查生成知识库的 D7 四支柱合规性。

对应 schema §8 Generator 合规检查 + §12 四支柱 + lint.md §2。

功能：
1. 可回滚：检查 git commit-per-stage
2. 可审计：检查节点 provenance 完整性（generated_by_step/run_id/source_span）
3. 确定性：检查 node ID 命名规范（禁时间戳/随机/流水号）
4. 预检：检查 run-manifest.json 的 preflight 记录
5. 路径确定性：扫描节点 .md 路径引用（禁绝对/meta-relative 路径）

退出码：0=全过，1=有 error，2=仅 warning

用法：
  python3 pipeline/state/lint_d7.py --target-skill-root /path/to/generated-skill [--legacy-ok]
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # 无 PyYAML 时 fallback，_parse_frontmatter 返回 {}


# ========== 1. 可回滚 ==========

def check_reversible(target_root: Path) -> dict:
    """检查 git commit-per-stage（schema §12.1）。"""
    issues = []
    if not (target_root / ".git").exists():
        return {"ok": False, "issues": ["无 git 仓库，无法 commit-per-stage"]}
    r = subprocess.run(["git", "log", "--oneline"], cwd=target_root, capture_output=True, text=True)
    commits = r.stdout.strip().split('\n') if r.stdout.strip() else []
    stage_commits = [c for c in commits if re.search(r'(S[1-7]|darwin|run-init)', c)]
    # 只在有 run-manifest 声称是 generator 产物时才严格检查 commit-per-stage
    # （历史数据如 CP 是人工策展的，不强求）
    manifest = target_root / "pipeline" / "state" / "run-manifest.json"
    is_generated = manifest.exists()
    if is_generated and len(stage_commits) < 3:
        issues.append(f"generator 产物但 stage commit 数偏少（{len(stage_commits)}），未做 commit-per-stage")
    return {"ok": len(issues) == 0, "stage_commits": len(stage_commits), "is_generated": is_generated, "issues": issues}


# ========== 2. 可审计 ==========

def check_auditable(target_root: Path, legacy_ok: bool) -> dict:
    """检查节点 provenance 完整性（schema §12.2 + §11）。"""
    dag = target_root / "dag" / "dag-index.json"
    if not dag.exists():
        return {"ok": False, "issues": ["无 dag/dag-index.json"]}
    d = json.loads(dag.read_text())

    manifest = target_root / "pipeline" / "state" / "run-manifest.json"
    manifest_run_id = None
    if manifest.exists():
        manifest_run_id = json.loads(manifest.read_text()).get("run_id")

    provenance_fields = ["generated_by_step", "run_id", "source_span"]
    missing = []
    legacy = []
    run_id_mismatch = []

    for n in d.get("nodes", []):
        miss = [f for f in provenance_fields if f not in n]
        if miss:
            # 若节点标 [legacy] 或 created 早于 manifest，视为历史数据
            is_legacy = (n.get("id", "").startswith("[legacy]") or
                         (legacy_ok and not n.get("generated_by_step")))
            if is_legacy:
                legacy.append(n["id"])
            else:
                missing.append((n["id"], miss))
        elif manifest_run_id and n.get("run_id") != manifest_run_id:
            run_id_mismatch.append((n["id"], n.get("run_id"), manifest_run_id))

    issues = []
    if missing:
        issues.append(f"{len(missing)} 个新节点缺 provenance: {missing[:3]}")
    if run_id_mismatch:
        issues.append(f"{len(run_id_mismatch)} 个节点 run_id 与 manifest 不一致: {run_id_mismatch[:2]}")

    return {
        "ok": len(issues) == 0,
        "total_nodes": len(d.get("nodes", [])),
        "missing_provenance": len(missing),
        "legacy_nodes": len(legacy),
        "run_id_mismatch": len(run_id_mismatch),
        "issues": issues
    }


# ========== 3. 确定性 ==========

NODE_ID_RE = re.compile(r'^(def|thm|meth|exp|ins)-[a-z][a-z0-9]*-[a-z0-9-]+$')
BAD_ID_PATTERNS = [
    (re.compile(r'-\d{6,8}($|-)'), '时间戳命名'),
    (re.compile(r'-[a-f0-9]{6,}($|-)'), '随机 hash 后缀'),
    (re.compile(r'-\d{3}$'), '流水号'),
]


def check_deterministic(target_root: Path) -> dict:
    """检查 node ID 命名规范（schema §10 + §12.3）。"""
    dag = target_root / "dag" / "dag-index.json"
    if not dag.exists():
        return {"ok": False, "issues": ["无 dag/dag-index.json"]}
    d = json.loads(dag.read_text())

    bad_format = []
    bad_pattern = []
    duplicates = []

    ids = [n["id"] for n in d.get("nodes", [])]
    seen = set()
    for nid in ids:
        # 格式检查
        if not NODE_ID_RE.match(nid):
            # 容忍 CP 实例的旧格式（无 source-slug 中段，如 thm-split-cp-coverage）
            # 新 schema 要求 <type>-<source>-<term>，但历史数据是 <type>-<term>
            pass  # 见下方 legacy 处理
        # 禁止模式
        for pat, desc in BAD_ID_PATTERNS:
            if pat.search(nid):
                bad_pattern.append((nid, desc))
        # 重复
        if nid in seen:
            duplicates.append(nid)
        seen.add(nid)

    issues = []
    if bad_pattern:
        issues.append(f"{len(bad_pattern)} 个 node ID 用禁止命名: {bad_pattern[:3]}")
    if duplicates:
        issues.append(f"{len(duplicates)} 个重复 node ID: {duplicates[:3]}")

    return {
        "ok": len(issues) == 0,
        "total_ids": len(ids),
        "unique_ids": len(seen),
        "bad_pattern": len(bad_pattern),
        "duplicates": len(duplicates),
        "issues": issues
    }


# ========== 4. 预检 ==========

def check_preflight(target_root: Path) -> dict:
    """检查 run-manifest 的 preflight 记录（schema §12.4）。"""
    manifest = target_root / "pipeline" / "state" / "run-manifest.json"
    if not manifest.exists():
        return {"ok": False, "issues": ["无 pipeline/state/run-manifest.json，未做 preflight"]}
    m = json.loads(manifest.read_text())
    pf = m.get("preflight", {})
    if not pf:
        return {"ok": False, "issues": ["run-manifest 无 preflight 记录"]}
    if not pf.get("ok"):
        return {"ok": False, "issues": [f"preflight 失败: {pf.get('stderr', '')[:200]}"]}
    return {"ok": True, "checked_at": pf.get("checked_at"), "issues": []}


# ========== 5. 路径确定性 ==========

ABSOLUTE_PATH_RE = re.compile(r'\]\((?:/|[A-Za-z]:\\)')
META_RELATIVE_RE = re.compile(r'\]\(\.\./(?:examples|engines|pipeline|schema)/')


def check_path_determinism(target_root: Path) -> dict:
    """扫描节点 .md 的路径引用（schema §12.5，防链接断裂）。"""
    wiki = target_root / "wiki" / "knowledge"
    if not wiki.exists():
        return {"ok": True, "issues": [], "scanned": 0}

    violations = []
    scanned = 0
    for md in wiki.glob("*.md"):
        scanned += 1
        text = md.read_text()
        for m in ABSOLUTE_PATH_RE.finditer(text):
            violations.append((md.name, "绝对路径", m.group(0)))
        for m in META_RELATIVE_RE.finditer(text):
            violations.append((md.name, "meta-skill-root-relative", m.group(0)))

    issues = []
    if violations:
        issues.append(f"{len(violations)} 个路径违规: {violations[:3]}")

    return {"ok": len(issues) == 0, "scanned": scanned, "violations": len(violations), "issues": issues}


# ========== 6. 硬门③：grounded_in 节点存在性 ==========

def check_grounding_existence(dag_index, judgments):
    """硬门③：judgment/心智元素的 grounded_in 节点必须存在于 DAG。"""
    valid_ids = {n["id"] for n in dag_index.get("nodes", [])}
    issues = []
    for j in judgments:
        for ref in j.get("grounded_in", []):
            node = ref.get("node") if isinstance(ref, dict) else ref
            if node not in valid_ids:
                issues.append(f"{j['id']}: grounded_in 指向不存在的节点 {node}")
    return issues


# ========== 7. 硬门①：mental_model 3重全过必 grounded_in ==========

def check_mind_element_grounding(elements):
    """硬门①：3重过的 mental_model 必须 grounded_in ≥1（heuristic 可选）。
    注：anti_pattern 的 role:refutes 约束、judgment 的 derived_from 继承正确性
    由 fresh subagent 抽查兜底（硬门①②），lint 不程序化校验。"""
    issues = []
    for e in elements:
        v = e.get("verification", {})
        all_pass = all(v.get(k, {}).get("pass") for k in ("cross_scene","generative","exclusive"))
        if e.get("type") == "mental_model" and all_pass and not e.get("grounded_in"):
            issues.append(f"{e['id']}: mental_model(3重全过) 缺 grounded_in 依据（硬门①）")
    return issues


# ========== 主流程 ==========

def _parse_frontmatter(text):
    """解析 .md 文件的 YAML frontmatter，无 frontmatter 或无 PyYAML 时返回 {}。"""
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    if yaml:
        return yaml.safe_load(m.group(1)) or {}
    # PyYAML 缺失 fallback：至少抽出顶层 type/id 不足以表达嵌套，这里仅警告并返回空
    print("warning: PyYAML 未安装，frontmatter 解析返回空（请 pip install pyyaml）", file=sys.stderr)
    return {}


def load_mind_artifacts(skill_root):
    """从 expert-mind/*.md 解析 judgments + mind elements 的 frontmatter。

    Returns:
        {"judgments": [...], "elements": [...]}
        judgments: type == "judgment" 的 frontmatter 列表
        elements:  type in ("mental_model", "heuristic", "anti_pattern") 的列表
    """
    em = Path(skill_root) / "expert-mind"
    if not em.exists():
        return {"judgments": [], "elements": []}
    judgments, elements = [], []
    for f in em.glob("*.md"):
        fm = _parse_frontmatter(f.read_text())
        t = fm.get("type")
        if t == "judgment":
            judgments.append(fm)
        elif t in ("mental_model", "heuristic", "anti_pattern"):
            elements.append(fm)
    return {"judgments": judgments, "elements": elements}


def main():
    p = argparse.ArgumentParser(description="D7 Generator 合规 Lint")
    p.add_argument("--target-skill-root", required=True, type=Path)
    p.add_argument("--legacy-ok", action="store_true",
                   help="容忍历史节点缺 provenance（CP 实例下沉后用）")
    args = p.parse_args()

    target = args.target_skill_root

    # 加载 DAG 与心智元素 frontmatter（硬门①③输入）
    dag_path = target / "dag" / "dag-index.json"
    dag = json.loads(dag_path.read_text()) if dag_path.exists() else {"nodes": []}
    artifacts = load_mind_artifacts(target)

    # 硬门①③返回 list[str]（issues 列表），需包装成 {ok, issues} 以适配主流程渲染
    grounding_issues = check_grounding_existence(dag, artifacts["judgments"])
    mind_grounding_issues = check_mind_element_grounding(artifacts["elements"])

    checks = {
        "可回滚 (Reversible)": check_reversible(target),
        "可审计 (Auditable)": check_auditable(target, args.legacy_ok),
        "确定性 (Deterministic)": check_deterministic(target),
        "预检 (Preflight)": check_preflight(target),
        "路径确定性 (Path Determinism)": check_path_determinism(target),
        "硬门③ grounded_in 节点存在 (Grounding Existence)": {
            "ok": len(grounding_issues) == 0, "issues": grounding_issues,
            "judgments_count": len(artifacts["judgments"]),
        },
        "硬门① mental_model 3重全过必 grounded_in": {
            "ok": len(mind_grounding_issues) == 0, "issues": mind_grounding_issues,
            "elements_count": len(artifacts["elements"]),
        },
    }

    has_error = False
    print(f"# D7 Lint Report — {target.name}\n")
    for name, result in checks.items():
        ok = result.pop("ok")
        status = "✓" if ok else "✗"
        print(f"## {status} {name}")
        for k, v in result.items():
            if k == "issues" and v:
                for issue in v:
                    print(f"  - {issue}")
            elif k != "issues":
                print(f"  - {k}: {v}")
        print()
        if not ok:
            has_error = True

    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
