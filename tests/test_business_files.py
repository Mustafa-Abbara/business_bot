"""Stage 1 gate checks (no API calls). Run from the repo root: python tests/test_business_files.py"""
import json
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
ME_DIR = ROOT / "me"
CHECKS = json.loads((ROOT / "tests" / "knowledge_checks.json").read_text(encoding="utf-8"))


def norm(text):
    """Collapse whitespace so phrases split across PDF lines still match."""
    return re.sub(r"\s+", " ", text)


def load():
    pdf_text = "\n\n".join((p.extract_text() or "") for p in PdfReader(ME_DIR / "about_business.pdf").pages)
    summary_text = (ME_DIR / "business_summary.txt").read_text(encoding="utf-8")
    return norm(pdf_text), norm(summary_text)


PDF, SUMMARY = load()


def test_pdf_text_is_selectable():
    assert len(PDF) > 500, f"PDF text too short ({len(PDF)} chars) - is it a scanned image?"
    assert CHECKS["business_name"] in PDF


def test_summary_length():
    assert len(SUMMARY) > 200
    assert CHECKS["business_name"] in SUMMARY
    paragraphs = [p for p in (ME_DIR / "business_summary.txt").read_text(encoding="utf-8").split("\n\n") if p.strip()]
    assert 3 <= len(paragraphs) <= 5, f"summary has {len(paragraphs)} paragraphs, expected 3-5"


def test_shared_facts_match():
    for fact in CHECKS["shared_facts"] + [CHECKS["unpriced_service"]["name"]]:
        assert fact in PDF, f"{fact!r} missing from PDF"
        assert fact in SUMMARY, f"{fact!r} missing from summary"


def test_prices_agree():
    pdf_prices = set(re.findall(r"\$\d+", PDF))
    summary_prices = set(re.findall(r"\$\d+", SUMMARY))
    assert pdf_prices == summary_prices, f"PDF {pdf_prices} vs summary {summary_prices}"


def test_pdf_only_facts():
    for item in CHECKS["pdf_only"]:
        assert item["phrase"] in PDF, f"{item['phrase']!r} missing from PDF"
        assert item["phrase"] not in SUMMARY, f"{item['phrase']!r} should be PDF-only"


def test_summary_only_facts():
    for item in CHECKS["summary_only"]:
        assert item["phrase"] in SUMMARY, f"{item['phrase']!r} missing from summary"
        assert item["phrase"] not in PDF, f"{item['phrase']!r} should be summary-only"


def test_not_offered_services_are_listed():
    """Declined services: the docs give a grounded 'no' (the agent still logs the demand)."""
    for item in CHECKS["not_offered"]:
        phrase = item["phrase"].lower()
        assert phrase in PDF.lower(), f"{phrase!r} missing from the PDF not-offered list"
        assert phrase in SUMMARY.lower(), f"{phrase!r} missing from the summary not-offered list"


def test_unknown_questions_are_really_unknown():
    """Hallucination traps: these topics must not appear anywhere in the docs."""
    for item in CHECKS["unknown"]:
        pattern = r"\b" + re.escape(item["keyword"])
        for name, text in [("PDF", PDF), ("summary", SUMMARY)]:
            assert not re.search(pattern, text, re.I), f"{item['keyword']!r} is mentioned in the {name}"


if __name__ == "__main__":
    print(f"PDF: {len(PDF)} chars | summary: {len(SUMMARY)} chars")
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
