# pipeline/state/test_lint_d7.py
import importlib.util
from pathlib import Path

def _load_lint(path):
    spec = importlib.util.spec_from_file_location("lint_d7", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def test_check_grounding_existence_passes_when_node_exists():
    lint = _load_lint(str(Path(__file__).parent / "lint_d7.py"))
    dag = {"nodes": [{"id": "thm-foo"}, {"id": "meth-bar"}]}
    judgments = [{"id": "judg-1", "grounded_in": [{"node": "thm-foo", "role": "supports"}]}]
    assert lint.check_grounding_existence(dag, judgments) == []

def test_check_grounding_existence_flags_orphan():
    lint = _load_lint(str(Path(__file__).parent / "lint_d7.py"))
    dag = {"nodes": [{"id": "thm-foo"}]}
    judgments = [{"id": "judg-1", "grounded_in": [{"node": "thm-NONEXISTENT", "role": "supports"}]}]
    issues = lint.check_grounding_existence(dag, judgments)
    assert len(issues) == 1 and "thm-NONEXISTENT" in issues[0]

def test_check_mental_model_requires_grounding():
    lint = _load_lint(str(Path(__file__).parent / "lint_d7.py"))
    elements = [{"id": "mm-1", "type": "mental_model",
                 "verification": {"cross_scene":{"pass":True},"generative":{"pass":True},"exclusive":{"pass":True}},
                 "grounded_in": []}]
    assert any("mm-1" in i for i in lint.check_mind_element_grounding(elements))

def test_check_heuristic_grounding_optional():
    lint = _load_lint(str(Path(__file__).parent / "lint_d7.py"))
    assert lint.check_mind_element_grounding([{"id": "heur-1", "type": "heuristic", "grounded_in": []}]) == []

# ===== Task 4.3: load_mind_artifacts + 接入 main() =====
import json

def _lint():
    return _load_lint(str(Path(__file__).parent / "lint_d7.py"))

def test_load_mind_artifacts_parses_judgments_and_elements(tmp_path):
    lint = _lint()
    em = tmp_path / "expert-mind"; em.mkdir()
    (em / "judgments.md").write_text(
        "---\nid: judg-1\ntype: judgment\ngrounded_in:\n  - {node: thm-bar, role: supports}\n---\nbody")
    (em / "mental-models.md").write_text(
        "---\nid: mm-1\ntype: mental_model\ngrounded_in: []\n---\nbody")
    art = lint.load_mind_artifacts(tmp_path)
    assert len(art["judgments"]) == 1 and art["judgments"][0]["id"] == "judg-1"
    assert len(art["elements"]) == 1 and art["elements"][0]["id"] == "mm-1"

def test_end_to_end_lint_flags_orphan_in_temp_skill(tmp_path):
    lint = _lint()
    dag_dir = tmp_path / "dag"; dag_dir.mkdir()
    (dag_dir / "dag-index.json").write_text(json.dumps({"nodes": [{"id": "thm-foo"}]}))
    em = tmp_path / "expert-mind"; em.mkdir()
    (em / "judgments.md").write_text(
        "---\nid: judg-1\ntype: judgment\ngrounded_in:\n  - {node: thm-bar, role: supports}\n---\nbody")
    art = lint.load_mind_artifacts(tmp_path)
    dag = json.loads((dag_dir / "dag-index.json").read_text())
    issues = lint.check_grounding_existence(dag, art["judgments"])
    assert any("thm-bar" in i for i in issues)

def test_end_to_end_lint_flags_mental_model_no_grounding(tmp_path):
    lint = _lint()
    em = tmp_path / "expert-mind"; em.mkdir()
    (em / "mental-models.md").write_text(
        "---\nid: mm-1\ntype: mental_model\nverification:\n  cross_scene: {pass: true}\n  generative: {pass: true}\n  exclusive: {pass: true}\ngrounded_in: []\n---\nbody")
    art = lint.load_mind_artifacts(tmp_path)
    issues = lint.check_mind_element_grounding(art["elements"])
    assert any("mm-1" in i for i in issues)
