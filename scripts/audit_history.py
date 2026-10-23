"""Audit B history without displaying secret values or ledger identities."""
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path, PurePosixPath
import subprocess
from urllib.parse import quote, quote_plus

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ledger", type=Path, required=True)
    args = parser.parse_args()
    secrets = []
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and any(s in line.split("=", 1)[0].upper() for s in ("KEY", "TOKEN", "PASSWORD")):
            value = line.split("=", 1)[1].strip().strip("\"'")
            if value:
                secrets.extend(s.encode() for s in (value, quote(value), quote_plus(value)))
    with args.private_ledger.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    identities = [r["transaction_id"].encode() for r in rows if r.get("transaction_id")]
    # Match exact CSV data rows too, not only original file paths.
    ledger_lines = [s.strip() for s in args.private_ledger.read_bytes().splitlines()[1:] if s.strip()]
    issues = set()
    blobs = set()
    for entry in git("rev-list", "--objects", "--all", "--reflog").decode().splitlines():
        oid, _, name = entry.partition(" ")
        if not name:
            continue
        path = PurePosixPath(name)
        if (path.name.startswith(".env") and path.name != ".env.example") or any(p in {"data", "private"} for p in path.parts):
            issues.add("private path found")
        if git("cat-file", "-t", oid).strip() != b"blob":
            continue
        blobs.add(oid)
        content = git("cat-file", "blob", oid)
        if any(v in content for v in secrets):
            issues.add("credential found")
        if any(v in content for v in identities + ledger_lines):
            issues.add("known ledger content found")
    result = {"checked_at": datetime.now().astimezone().isoformat(),
              "commit": git("rev-parse", "HEAD").decode().strip(),
              "scope": "B local refs, fetched origin refs and reflog-reachable history",
              "historical_blobs_checked": len(blobs), "ledger_identity_count": len(identities),
              "checks": ["private paths", "local credential literals and URL encodings", "known real ledger transaction IDs and exact CSV rows"],
              "status": "FAIL" if issues else "PASS", "findings_redacted": sorted(issues),
              "limits": "Cannot prove absence of unknown rewritten/aggregated financial content or inaccessible remote objects; no private values included in this report."}
    (ROOT / "notes/day3-security-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
