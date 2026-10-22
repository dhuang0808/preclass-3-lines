"""Live acceptance runs, separate from mocked unit tests."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from preclass_app.cli import run_preview

cases = [("concept-1", "梯度下降"), ("concept-2", "梯度下降"), ("concept-3", "梯度下降"),
         ("current-event", "Hacktoberfest 2026 Week 3 Slow and Steady"), ("daily-life", "大学生如何整理电脑下载文件夹")]
report = []
for name, topic in cases:
    print(f"Running live case: {name}", flush=True)
    receipt = run_preview(topic)
    receipt["case"] = name
    assert receipt["source_count"] == 5 and receipt["line_count"] == 3
    assert max(receipt["line_lengths"]) <= 64
    path = ROOT / "notes" / f"live-{name}.json"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    report.append({key: receipt[key] for key in ("case", "topic", "line_count", "line_lengths", "attempts", "total_seconds")})
    print(receipt["stdout"], flush=True)
(ROOT / "notes" / "live-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
outputs = [json.loads((ROOT / "notes" / f"live-concept-{i}.json").read_text(encoding="utf-8"))["stdout"] for i in (1, 2, 3)]
print("Repeated topic: format PASS for all 3 runs; distinct texts:", len(set(outputs)), flush=True)
print("LIVE ACCEPTANCE PASS: 5 runs, 3 real topics; not a semantic-accuracy benchmark.")
