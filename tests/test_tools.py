"""Offline tests for the notebook's tools and helpers: no API key, no LLM calls.

Covers the tools (Stage 5), safe_execute (Stage 6), the keyword router and parse_label (Stage 7),
the Gradio history converter (Stage 8) and the reflection JSON parser (Stage 10).
Run from the repo root: python tests/test_tools.py
"""
import inspect
import json

from nb_loader import ROOT, load_cells

nb = load_cells("def record_feedback", "TOOL_SCHEMAS = [", "def safe_execute",
                "def keyword_route", "def gradio_to_api", "def _parse_reflection")


def lines(path):
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def test_valid_lead_writes_one_json_line():
    before = len(lines(nb["LEADS_LOG"]))
    r = nb["record_customer_interest"]("Sara@Example.com ", "Sara", "Memory Capsule for my graduation")
    assert r["status"] == "ok" and r["lead_id"].startswith("lead_"), r
    rows = lines(nb["LEADS_LOG"])
    assert len(rows) == before + 1
    row = json.loads(rows[-1])
    assert row["email"] == "sara@example.com" and row["name"] == "Sara"
    assert set(row) == {"timestamp", "lead_id", "email", "name", "message"}


def test_invalid_email_is_rejected_and_not_written():
    before = len(lines(nb["LEADS_LOG"]))
    for bad in ["sara.example.com", "sara@", "sara@example", "", None, "sara @example.com"]:
        assert nb["record_customer_interest"](bad, "Sara") == {"status": "error", "error": "invalid email"}, bad
    assert nb["record_customer_interest"]("sara@example.com", "  ")["status"] == "error"
    assert len(lines(nb["LEADS_LOG"])) == before


def test_feedback_ok_and_empty():
    before = len(lines(nb["FEEDBACK_LOG"]))
    assert nb["record_feedback"]("Do you sell gift cards?")["status"] == "ok"
    assert nb["record_feedback"]("   ") == {"status": "error", "error": "empty question"}
    assert len(lines(nb["FEEDBACK_LOG"])) == before + 1


def test_arabic_name_saved_as_readable_utf8():
    nb["record_customer_interest"]("mustafa@example.com", "مصطفى", "Life Timeline")
    raw = nb["LEADS_LOG"].read_text(encoding="utf-8")
    assert "مصطفى" in raw and "\\u0645" not in raw


def test_schemas_match_function_signatures():
    for schema in nb["TOOL_SCHEMAS"]:
        params = inspect.signature(nb["TOOL_REGISTRY"][schema["name"]]).parameters
        assert list(schema["inputSchema"]["properties"]) == list(params)
        required = [p for p, v in params.items() if v.default is inspect.Parameter.empty]
        assert schema["inputSchema"]["required"] == required
        assert {"name", "description", "inputSchema", "outputSchema"} <= set(schema)
    tool = nb["mcp_to_openai"](nb["TOOL_SCHEMAS"][0])
    assert tool["type"] == "function" and set(tool["function"]) == {"name", "description", "parameters"}


def test_safe_execute_never_raises():
    cases = [("delete_everything", "{}", "unknown tool"),
             ("record_feedback", "{question: oops", "not valid JSON"),
             ("record_feedback", "[1, 2]", "must be a JSON object"),
             ("record_customer_interest", '{"email": "a@b.co"}', "wrong arguments"),
             ("record_feedback", '{"question": "hi", "phone": "1"}', "wrong arguments"),
             ("record_feedback", None, "wrong arguments")]
    with __import__("contextlib").redirect_stdout(__import__("io").StringIO()):
        for name, raw, expected in cases:
            r = nb["safe_execute"](name, raw)
            assert r["status"] == "error" and expected in r["error"], (name, raw, r)


def test_parse_label():
    for raw, expected in [("Intent: Lead.", "lead"), ("LEAD", "lead"), ("feedback\n", "feedback"),
                          ("I think general", "general"), ("", None), (None, None), ("unknown", None)]:
        assert nb["parse_label"](raw) == expected, raw


def test_keyword_router_accuracy():
    cases = json.loads((ROOT / "tests" / "router_cases.json").read_text(encoding="utf-8"))
    every = cases["tuning"] + cases["held_out"]
    correct = sum(nb["keyword_route"](c["message"], c.get("history")) == c["label"] for c in every)
    assert correct / len(every) >= 0.85, f"{correct}/{len(every)}"
    lead_to_feedback = [c["message"] for c in every
                        if c["label"] == "lead" and nb["keyword_route"](c["message"], c.get("history")) == "feedback"]
    assert not lead_to_feedback, lead_to_feedback


def test_gradio_history_converter():
    gr = lambda role, text: {"role": role, "content": [{"type": "text", "text": text}], "metadata": None, "options": None}
    history = [gr("user", "Hi, I'm Karim."), gr("assistant", "Hello Karim!"),
               {"role": "user", "content": [{"type": "file", "file": {"path": "/tmp/a.jpg"}}]},
               {"role": "system", "content": "x"}, ["hello", "hi there"], {"role": "user", "content": "plain"}]
    assert nb["gradio_to_api"](history) == [
        {"role": "user", "content": "Hi, I'm Karim."}, {"role": "assistant", "content": "Hello Karim!"},
        {"role": "user", "content": "hello"}, {"role": "assistant", "content": "hi there"},
        {"role": "user", "content": "plain"}]
    assert nb["gradio_to_api"](None) == []


def test_reflection_parser():
    parse = nb["_parse_reflection"]
    assert parse('```json\n{"ok": false, "issues": "too long", "revised": " Short. "}\n```') == {
        "ok": False, "issues": ["too long"], "revised": "Short."}
    for bad in ["", None, "not json", '{"issues": []}', '{"ok": "yes"}', "[1, 2]"]:
        assert parse(bad) is None, bad


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
    print(f"\n(test logs written to {nb['LOGS_DIR']}, not to logs/)")
    raise SystemExit(failed)
