"""Record machine timings, never substitute them for a human reading study.

Uses three live SerpApi requests. Page retrieval is a fixed five-link protocol,
not a claim that every learner must read five pages. No full pages are saved.
"""
from contextlib import contextmanager
from datetime import datetime
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import socket
import statistics
import sys
import time
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from preclass_app.cli import run_preview
from preclass_app.config import AppError, Settings
from preclass_app.search import format_sources
from preclass_app.summary import summarize_sources

OUT = ROOT / "notes" / "article-measurements.json"
TOPIC = "检索增强生成 RAG 是什么"


def save(value):
    OUT.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


@contextmanager
def client_loopback_only():
    """Guard this Python client only; not an OS/server network sandbox."""
    original = socket.socket.connect
    calls = []

    def connect(sock, address):
        host = address[0]
        try:
            allowed = ipaddress.ip_address(host).is_loopback
        except ValueError:
            allowed = False
        calls.append({"host": host, "port": address[1], "allowed": allowed})
        if not allowed:
            raise OSError("Benchmark client rejects non-loopback connections")
        return original(sock, address)

    with patch.object(socket.socket, "connect", connect):
        yield calls


class TextCounter(HTMLParser):
    """Rough HTML text count; not a verified article body or reading load."""
    IGNORED = {"script", "style", "head", "nav", "footer", "header", "noscript"}

    def __init__(self):
        super().__init__()
        self.hidden = []
        self.chars = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.IGNORED:
            self.hidden.append(tag)

    def handle_endtag(self, tag):
        if tag in self.hidden:
            index = len(self.hidden) - 1 - self.hidden[::-1].index(tag)
            del self.hidden[index:]

    def handle_data(self, value):
        if not self.hidden:
            self.chars += len("".join(value.split()))


def retrieve_metadata(source):
    row = {"title": source["title"], "url": source["link"]}
    started = time.perf_counter()
    try:
        request = Request(source["link"], headers={"User-Agent": "PreclassEvidence/1.0"})
        with build_opener(ProxyHandler({})).open(request, timeout=8) as response:
            content_type = response.headers.get_content_type()
            raw = response.read(1_000_001)
            row.update(status=response.status, content_type=content_type,
                       bytes_read=len(raw), capped=len(raw) > 1_000_000)
            if content_type in {"text/html", "application/xhtml+xml"}:
                parser = TextCounter()
                parser.feed(raw.decode(response.headers.get_content_charset() or "utf-8", errors="replace"))
                row["rough_html_text_chars"] = parser.chars
    except HTTPError as error:
        row["error"] = "HTTP " + str(error.code)
    except Exception as error:
        row["error"] = type(error).__name__  # no credential-bearing exception URL
    row["seconds"] = round(time.perf_counter() - started, 3)
    return row


def main():
    receipt = {
        "measured_at": datetime.now().astimezone().isoformat(), "topic": TOPIC,
        "protocol": "3 sequential fresh live runs; fetch first run's 5 links once; 3 cached-source local runs",
        "human_lookup_seconds": None, "human_pages_read": None, "human_three_line_read_seconds": None,
        "human_measurement_status": "not measured; machine timings cannot establish human time saved",
        "live_runs": [], "page_retrieval": [], "cached_local_runs": [],
    }
    save(receipt)
    for index in range(3):
        started = time.perf_counter()
        try:
            run = run_preview(TOPIC)
            run["input_title_snippet_chars"] = sum(len(s["title"]) + len(s["snippet"]) for s in run["sources"])
            run["output_chars_excluding_linebreaks"] = sum(run["line_lengths"])
            receipt["live_runs"].append(run)
        except AppError as error:
            receipt["live_runs"].append({"error": str(error), "failure_seconds": round(time.perf_counter() - started, 3)})
        save(receipt)
        print(f"live {index + 1}/3 recorded", flush=True)
    successful = [r for r in receipt["live_runs"] if "error" not in r]
    if not successful:
        raise SystemExit("No successful live run; inspect safe receipt")
    for source in successful[0]["sources"]:
        receipt["page_retrieval"].append(retrieve_metadata(source))
        save(receipt)
        print(f"page {len(receipt['page_retrieval'])}/5 recorded", flush=True)
    local = Settings(api_key="", model="gemma3:4b")
    with client_loopback_only() as connections:
        # Documentation-only external address. Guard must reject before any packet.
        try:
            with socket.socket() as sock:
                sock.connect(("203.0.113.1", 443))
        except OSError:
            receipt["guard_self_test"] = "external address rejected before connect"
        else:
            raise RuntimeError("Client guard self-test failed")
        for index in range(3):
            started = time.perf_counter()
            row = {"api_key_present": False}
            try:
                output, attempts = summarize_sources(TOPIC, format_sources(successful[0]["sources"]), local)
                row.update(stdout=output, attempts=attempts, line_count=len(output.splitlines()))
            except AppError as error:
                row["error"] = str(error)
            row["seconds"] = round(time.perf_counter() - started, 3)
            receipt["cached_local_runs"].append(row)
            save(receipt)
            print(f"cached local {index + 1}/3 recorded", flush=True)
        receipt["client_socket_connect_calls"] = connections
    receipt["guard_scope"] = "Only this Python client's socket.connect; not the Ollama process, OS, DNS, or a physical disconnection test"
    durations = [r["total_seconds"] for r in successful]
    receipt["summary"] = {
        "live_successes": len(successful), "live_attempts": 3,
        "live_seconds_median": statistics.median(durations),
        "live_seconds_min": min(durations), "live_seconds_max": max(durations),
        "page_requests_attempted": len(receipt["page_retrieval"]),
        "page_http_successes": sum(200 <= r.get("status", 0) < 300 for r in receipt["page_retrieval"]),
        "page_retrieval_seconds_sum": round(sum(r["seconds"] for r in receipt["page_retrieval"]), 3),
        "cached_local_successes": sum("error" not in r for r in receipt["cached_local_runs"]),
    }
    save(receipt)
    print(json.dumps(receipt["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
