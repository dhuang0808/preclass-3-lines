"""Four new live student topics plus non-sensitive account quota receipts."""
from datetime import datetime
import json
from pathlib import Path
import sys
import time
from urllib.parse import urlencode
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from preclass_app.cli import run_preview
from preclass_app.config import AppError, Settings


def quota():
    try:
        settings = Settings.load(ROOT)
        proxy = settings.proxy
        opener = build_opener(ProxyHandler({"http": proxy, "https": proxy} if proxy else {}))
        with opener.open("https://serpapi.com/account.json?" + urlencode({"api_key": settings.api_key}), timeout=25) as response:
            raw = json.load(response)
        return {"checked_at": datetime.now().astimezone().isoformat(),
                **{k: raw.get(k) for k in ("plan_name", "searches_per_month", "this_month_usage", "total_searches_left")}}
    except Exception as error:
        return {"checked_at": datetime.now().astimezone().isoformat(), "error_type": type(error).__name__}


def main():
    result = {"quota_before": quota(), "runs": []}
    output = ROOT / "notes/day3-live-evidence.json"
    topics = ["函数极限的直观含义", "导数的几何意义", "机器学习中的过拟合", "线性代数中的矩阵乘法"]
    for topic in topics:
        started = time.perf_counter()
        try:
            row = run_preview(topic)
            before = sum(len(s["title"]) + len(s["snippet"]) for s in row["sources"])
            after = sum(row["line_lengths"])
            row.update(input_title_snippet_chars=before, output_chars_including_labels=after,
                       displayed_text_reduction_percent=round((1 - after / before) * 100, 2))
            print(topic + "\n" + row["stdout"] + "\nseconds: " + str(row["total_seconds"]), flush=True)
        except AppError as error:
            row = {"topic": topic, "error": str(error), "failure_seconds": round(time.perf_counter() - started, 2)}
            print(topic + ": " + str(error), flush=True)
        result["runs"].append(row)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    result["quota_after"] = quota()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Quota after:", json.dumps(result["quota_after"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
