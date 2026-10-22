import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import time

from .config import AppError, Settings
from .search import fetch_results, format_sources
from .summary import summarize_sources

ROOT = Path(__file__).resolve().parents[1]


def run_preview(topic: str, root: Path = ROOT) -> dict:
    topic = topic.strip()
    if not topic or len(topic) > 200:
        raise AppError("请输入 1—200 个字符的主题。")
    started = time.perf_counter()
    settings = Settings.load(root)
    results = fetch_results(topic, settings)
    searched = time.perf_counter()
    output, attempts = summarize_sources(topic, format_sources(results), settings)
    return {"topic": topic, "live": True, "source_count": len(results), "sources": results,
            "captured_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
            "model": settings.model, "stdout": output, "attempts": attempts,
            "line_count": len(output.splitlines()), "line_lengths": [len(s) for s in output.splitlines()],
            "search_seconds": round(searched - started, 2), "total_seconds": round(time.perf_counter() - started, 2)}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise AppError('参数不正确，请使用 python preclass.py "主题"；帮助见 --help。')


def main(argv=None) -> int:
    try:
        parser = Parser(description="用实时搜索与本地 Gemma，生成恰好三行中文课前速览。")
        parser.add_argument("topic", nargs="+", help="想在课前搞懂的主题")
        parser.add_argument("--save-evidence", type=Path, help="可选：保存公开搜索来源及运行证据为 JSON")
        args = parser.parse_args(argv)
        receipt = run_preview(" ".join(args.topic))
        if args.save_evidence:
            args.save_evidence.parent.mkdir(parents=True, exist_ok=True)
            args.save_evidence.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
        print(receipt["stdout"])
        return 0
    except AppError as error:
        print(str(error), file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError):
        print("读取配置、处理接口数据或保存证据失败，请检查文件与服务状态。", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("已取消本次查询。", file=sys.stderr)
        return 130
