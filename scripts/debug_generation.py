"""Local-only troubleshooting against already captured public snippets."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from preclass_app.config import Settings
from preclass_app.search import format_sources
from preclass_app.summary import summarize_sources

receipt = json.loads((ROOT / "notes" / "live-concept-2.json").read_text(encoding="utf-8"))
diagnostics = []
try:
    print(summarize_sources(receipt["topic"], format_sources(receipt["sources"]), Settings.load(ROOT), diagnostics))
finally:
    (ROOT / ".tmp").mkdir(exist_ok=True)
    (ROOT / ".tmp" / "debug-generation.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
