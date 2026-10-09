"""Generate app.py (the Hugging Face Space entry point) from business_agent.ipynb.

The notebook stays the single source of truth: this copies its definition cells (setup, persona, instructions, tools,
router, agent loop, orchestrator, reflection, Gradio) in order and leaves out every test and demo cell.
Run from the repo root after changing the notebook:  python scripts/export_app.py
tests/test_app_export.py fails if app.py is out of date.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (section label, marker that identifies the code cell, optional text that ends the part to keep)
CELLS = [
    ("1.1 Imports and configuration", "ME_DIR = Path(", None),
    ("1.2 Load the API key", "GEMINI_API_KEY = os.getenv", None),
    ("1.3 LLM client and call_llm()", "def call_llm(", None),
    ("2. Business context", "def load_business_context(", None),
    ("2. Business context (load)", "summary_text, pdf_text = load_business_context()", None),
    ("3. PERSONA", 'PERSONA = """', None),
    ("4. INSTRUCTIONS", 'INSTRUCTIONS = """', None),
    ("5. System prompt", "def build_system_prompt(", "\nsystem_prompt = build_system_prompt()"),
    ("6. Tools", "def record_feedback(", None),
    ("6.1 Tool schemas (MCP style)", "TOOL_SCHEMAS = [", '\nprint("=== MCP-style'),
    ("7. Router", "def keyword_route(", None),
    ("7. Routes", "ROUTES = {", "\nassert set(ROUTES)"),
    ("8. Agent loop", "def safe_execute(", None),
    ("9. Orchestrator", "def gradio_to_api(", None),
    ("10. Reflection", "def reflect_with_verdict(", None),
    ("12. Gradio interface", "demo = gr.ChatInterface(", None),
]

HEADER = '''"""EchoNest business agent: Milo, the Memory Concierge (Hugging Face Space entry point).

GENERATED from business_agent.ipynb by scripts/export_app.py. Do not edit by hand: change the notebook, then run
    python scripts/export_app.py
The API key is read only from the environment (GEMINI_API_KEY): a Space secret on Hugging Face, or .env locally.
Tests and demos live in the notebook; this file contains only the application code.
"""
'''


def build_app_source():
    nb = json.loads((ROOT / "business_agent.ipynb").read_text(encoding="utf-8"))
    code = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    parts = [HEADER]
    for label, marker, cut in CELLS:
        matches = [src for src in code if marker in src]
        assert len(matches) == 1, f"expected one notebook cell containing {marker!r}, found {len(matches)}"
        src = matches[0]
        if cut:
            assert cut in src, f"cut text {cut!r} not found in the {label} cell"
            src = src[:src.index(cut)]
        parts.append(f"\n# {'=' * 100}\n# {label}\n# {'=' * 100}\n{src.strip()}\n")
    return "".join(parts)


if __name__ == "__main__":
    source = build_app_source()
    compile(source, "app.py", "exec")
    (ROOT / "app.py").write_text(source, encoding="utf-8")
    print(f"Wrote app.py ({len(source.splitlines())} lines, {len(CELLS)} notebook cells)")
