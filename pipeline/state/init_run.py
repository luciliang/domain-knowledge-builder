#!/usr/bin/env python3
"""
D7 Checkpoint 初始化脚本 — pipeline 开始前调用。

功能：
1. 生成本次 run_id（UUID）
2. 在 target_skill_root 初始化 git（若未有）+ 创建 ingest/<run_id> 分支
3. 创建 pipeline/state/run-manifest.json（空 stages）
4. 运行 docling preflight 并记录

用法：
  python3 pipeline/state/init_run.py \\
    --target-skill-root /path/to/generated-skill \\
    --domain "diffusion-models" \\
    --sources p1.pdf p2.pdf

输出：run_id（stdout）+ run-manifest.json（文件）
"""

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def run(cmd, cwd=None, check=True):
    """运行命令，返回 (returncode, stdout, stderr)。"""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"命令失败: {' '.join(cmd)}\nstderr: {r.stderr}")
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def git_init(target_root: Path, run_id: str):
    """初始化 git + 创建 ingest/<run_id> 分支。"""
    if not (target_root / ".git").exists():
        run(["git", "init"], cwd=target_root)
        # 配置 commit message 规范 hook（可选，先跳过）

    # 确保有初始 commit（git checkout -b 需要）
    rc, _, _ = run(["git", "rev-parse", "--verify", "HEAD"], cwd=target_root, check=False)
    if rc != 0:
        # 空 repo，先做初始 commit
        run(["git", "add", "-A"], cwd=target_root)
        run(["git", "commit", "-m", "initial: empty skill scaffold", "--allow-empty"], cwd=target_root)

    # 创建并切到 ingest 分支
    run(["git", "checkout", "-b", f"ingest/{run_id}"], cwd=target_root)


def docling_preflight(meta_skill_root: Path) -> dict:
    """运行 book_to_skill --check，返回 per-format 提取器可用性。
    
    schema §12.4 要求：technical 模式（学术论文必需）下 docling 不可用 → 报错。
    book_to_skill --check 的退出码 0 表示"有 fallback"，但我们要 docling 本身可用。
    """
    engines_dir = meta_skill_root / "engines"
    rc, stdout, stderr = run(
        [sys.executable, "-m", "book_to_skill", "--check"],
        cwd=engines_dir, check=False
    )
    # 解析输出，检查 docling 是否真的可用（不只是有 fallback）
    docling_ok = rc == 0 and '✓ python: docling' in stdout
    return {
        "ok": docling_ok,
        "book_to_skill_runs": rc == 0,  # book_to_skill 本身能跑
        "docling_available": docling_ok,
        "stdout": stdout[:2000],  # 截断防超大
        "stderr": stderr[:500],
        "checked_at": datetime.now(timezone.utc).isoformat()
    }


def init_run(target_skill_root: Path, meta_skill_root: Path, domain: str, sources: list) -> str:
    """主入口：初始化 run-manifest + git，返回 run_id。"""
    run_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc).isoformat()

    # 创建 pipeline/state/ 目录
    state_dir = target_skill_root / "pipeline" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    # git 初始化
    git_init(target_skill_root, run_id)

    # docling preflight
    preflight = docling_preflight(meta_skill_root)
    if not preflight["ok"]:
        # docling 不可用 → 报错（schema §12.4 不静默退化）
        # 但仍创建 run-manifest 记录失败，便于审计
        print(f"⚠️  docling preflight 失败（technical 模式必需）：", file=sys.stderr)
        print(preflight["stderr"], file=sys.stderr)
        print(f"   安装指引：pip install docling", file=sys.stderr)

    # 创建 run-manifest.json
    manifest = {
        "run_id": run_id,
        "started_at": started_at,
        "domain": domain,
        "sources": sources,
        "meta_skill_root": str(meta_skill_root),
        "preflight": preflight,
        "stages": [],
        "darwin_score": None,
        "accepted": False
    }
    manifest_path = state_dir / "run-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    # 首个 commit：记录 run 启动
    run(["git", "add", "pipeline/state/run-manifest.json"], cwd=target_skill_root)
    run(["git", "commit", "-m", f"run-init: {run_id} domain={domain}"], cwd=target_skill_root)

    if not preflight["ok"]:
        print(f"\n❌ run 已初始化但 preflight 失败：{manifest_path}", file=sys.stderr)
        print(f"   run_id={run_id}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ run 初始化完成", file=sys.stdout)
    print(f"   run_id: {run_id}", file=sys.stdout)
    print(f"   manifest: {manifest_path}", file=sys.stdout)
    print(f"   git branch: ingest/{run_id}", file=sys.stdout)
    return run_id


def main():
    p = argparse.ArgumentParser(description="D7 Checkpoint 初始化")
    p.add_argument("--target-skill-root", required=True, type=Path)
    p.add_argument("--meta-skill-root", required=True, type=Path,
                   help="本 meta-skill 根目录（读 engines）")
    p.add_argument("--domain", required=True)
    p.add_argument("--sources", required=True, nargs="+",
                   help="来源论文路径列表")
    args = p.parse_args()

    run_id = init_run(args.target_skill_root, args.meta_skill_root,
                      args.domain, args.sources)
    # stdout 只输出 run_id，便于脚本捕获
    sys.stdout.write(run_id)


if __name__ == "__main__":
    main()
