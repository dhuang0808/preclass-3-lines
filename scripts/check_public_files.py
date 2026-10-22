"""Fail before commit if staged content contains local keys/private artifacts."""
from pathlib import Path, PurePosixPath
import subprocess
import sys
from urllib.parse import quote, quote_plus

ROOT = Path(__file__).resolve().parents[1]
names = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"], cwd=ROOT).decode().split("\0")
secrets = []
env = ROOT / ".env"
if env.exists():
    for line in env.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and any(x in line.split("=", 1)[0].upper() for x in ("KEY", "TOKEN", "PASSWORD")):
            value = line.split("=", 1)[1].strip().strip("\"'")
            if value:
                secrets.extend(x.encode() for x in (value, quote(value), quote_plus(value)))
issues = []
for name in filter(None, names):
    path = PurePosixPath(name)
    if (any(p in (".venv", "private", ".models", ".cache", ".tmp", "__pycache__", "data") for p in path.parts)
            or (path.name.startswith(".env") and name != ".env.example")):
        issues.append(name + ": private path")
    blob = subprocess.check_output(["git", "show", ":" + name], cwd=ROOT)
    if any(value in blob for value in secrets):
        issues.append(name + ": credential detected")
if issues:
    print("Public-file check FAILED; values redacted:", *issues, sep="\n")
    sys.exit(1)
print(f"Public-file check PASS: {sum(bool(n) for n in names)} staged files; no local secrets/private paths.")
