"""app.py must be exactly what scripts/export_app.py generates from the notebook (no drift). No API key needed.
Run from the repo root: python tests/test_app_export.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from export_app import build_app_source  # noqa: E402


def test_app_py_matches_notebook():
    current = (ROOT / "app.py").read_text(encoding="utf-8")
    assert current == build_app_source(), "app.py is out of date: run  python scripts/export_app.py"


def test_app_py_compiles_and_has_no_tests():
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    compile(source, "app.py", "exec")
    for leftover in ["PROMPT_TESTS", "AGENT_TESTS", "REFLECTION_TESTS", "ROUTER_CASES", "temporary_logs", "tests/"]:
        assert leftover not in source, f"test code leaked into app.py: {leftover}"
    assert source.rstrip().endswith("demo.launch(theme=gr.themes.Soft())")


def test_key_only_from_environment():
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'os.getenv("GEMINI_API_KEY")' in source
    for prefix in ["AIza", "sk-", "AQ."]:
        assert prefix not in source, f"something that looks like a key ({prefix}) is in app.py"


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except AssertionError as e:
                failed += 1
                print("FAIL", name, "-", e)
    raise SystemExit(failed)
