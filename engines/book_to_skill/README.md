# book_to_skill — Vendored Extraction Engine

> **来源**：[virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (MIT)
> **vendored commit**：`6ee737d` (2026-06-26)
> **用途**：domain-knowledge-builder meta-skill 的 PDF/EPUB/DOCX/HTML/RTF/TXT/Calibre 文本提取引擎，`--mode technical`（Docling）保留学术论文公式/表格。

## 为什么 vendor 整个包

`book_to_skill/` 内部有紧耦合依赖（`utils.py` 和所有 parser 都 import `dependencies.py` + `exceptions.py` + `config.py`）。摘选 `parsers/` 会断依赖，import 直接失败。所以 vendor **完整集合**：`parsers/` + `utils.py` + `config.py` + `dependencies.py` + `exceptions.py` + `__init__.py` + **`cli.py` + `__main__.py`**（后两者是 `python -m book_to_skill` 调用链必需，最初误弃已修正）。

## 已弃用的文件（相对源 repo）

- `scripts/extract.py` — 旧版独立脚本（被 `python -m book_to_skill` 替代）。注：源 repo 的 `scripts/` 不在 `book_to_skill/` 包内，本就不 vendor。

## 修改点

**零修改**。保持 vendor 代码原样，便于未来从上游拉取更新。

调用方式：`python -m book_to_skill <paths> --mode technical`（subprocess，保持 vendor 隔离）。

## 硬依赖：docling

`technical` 模式（保留公式/表格的核心价值）依赖 [docling](https://github.com/DS4SD/docling)——重型 ML 库（几百 MB + 模型下载）。`dependencies.py` 已内置 `--check` preflight 和 `--install-missing` 机制。

domain-knowledge-builder 的 pipeline S1 会先跑 preflight：缺 docling 则报错指引安装。学术论文场景下 docling 不可牺牲（没公式=没价值）。

## 升级流程

```bash
# 从上游拉新版本
cd ~/projects/domain-skill-research/book-to-skill && git pull
# 对比差异
diff -r book_to_skill/ ~/.pi/agent/skills/domain-knowledge-skill/engines/book_to_skill/ --exclude='__pycache__' --exclude='LICENSE.md' --exclude='README.md'
# 确认后覆盖，更新本文件的 vendored commit
```

## 许可证

见 `LICENSE.md`（MIT）。原作者 virgiliojr94。
