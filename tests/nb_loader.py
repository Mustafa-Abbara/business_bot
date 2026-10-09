"""Load selected code cells from business_agent.ipynb, so the tests run the notebook's own code (no second copy).

Only cells that define functions are loaded: no API key, no LLM calls, and logs go to a temporary folder.
"""
import contextlib
import io
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PRELUDE = f"""
import json, os, re, sys
from pathlib import Path
ME_DIR = Path({str(ROOT / "me")!r})
LOGS_DIR = Path({tempfile.mkdtemp(prefix="business_bot_test_logs_")!r})
"""


def load_cells(*markers):
    """Exec the code cells containing each marker (in the given order) and return their namespace."""
    nb = json.loads((ROOT / "business_agent.ipynb").read_text(encoding="utf-8"))
    code_cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    ns = {"__name__": "business_agent"}
    exec(PRELUDE, ns)
    for marker in markers:
        matches = [src for src in code_cells if marker in src]
        assert len(matches) == 1, f"expected exactly one notebook cell containing {marker!r}, found {len(matches)}"
        with contextlib.redirect_stdout(io.StringIO()):  # some cells print documentation
            exec(compile(matches[0], f"<notebook: {marker}>", "exec"), ns)
    return ns
