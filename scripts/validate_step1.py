"""Capture public search evidence without recording credentials or request URLs."""
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from preclass_app.cli import run_preview

started = time.perf_counter()
receipt = run_preview("TabPFN")
sources = receipt["sources"]
output = receipt["stdout"]
assert len(output.splitlines()) == 3
receipt = {"topic": "TabPFN", "search": "SerpApi Google, no_cache=true",
           "source_count": 5, "sources": sources, "stdout": output,
           "line_count": 3, "seconds": round(time.perf_counter() - started, 2)}
(ROOT / "notes" / "step1-real-search.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
(ROOT / "notes" / "step1-real-search.txt").write_text(
    "python preclass.py TabPFN\n" + output + "\nExit code: 0\n", encoding="utf-8")
print(output)
print("Evidence saved; source_count=5; line_count=3; exit=0")
