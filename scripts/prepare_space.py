"""Assemble exactly the files a Hugging Face Space needs into dist/hf_space/ (git-ignored).

Run from the repo root:  python scripts/prepare_space.py
Then upload the CONTENTS of dist/hf_space/ to the Space (web UI or git). Never upload .env:
the key goes in the Space's Settings → Variables and secrets as a *secret* named GEMINI_API_KEY.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "hf_space"
FILES = {
    "app.py": ROOT / "app.py",
    "requirements.txt": ROOT / "requirements.txt",
    "README.md": ROOT / "deploy" / "hf_space" / "README.md",  # Space card with the sdk/sdk_version YAML header
    "me/about_business.pdf": ROOT / "me" / "about_business.pdf",
    "me/business_summary.txt": ROOT / "me" / "business_summary.txt",
}

sys.path.insert(0, str(ROOT / "scripts"))
from export_app import build_app_source  # noqa: E402

if (ROOT / "app.py").read_text(encoding="utf-8") != build_app_source():
    raise SystemExit("app.py is out of date: run  python scripts/export_app.py  first")

if OUT.exists():
    shutil.rmtree(OUT)
for target, source in FILES.items():
    dest = OUT / target
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    print(f"  {target:<26} ← {source.relative_to(ROOT)}")

leaked = [p for p in OUT.rglob("*") if p.name == ".env"]
assert not leaked, f".env must never be uploaded: {leaked}"
print(f"\nReady: upload the contents of {OUT.relative_to(ROOT)}/ to your Space ({len(FILES)} files, no .env).")
