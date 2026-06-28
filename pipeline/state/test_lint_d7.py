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
