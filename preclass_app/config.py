from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


class AppError(Exception):
    """A safe, one-line error that never contains a credential-bearing URL."""


@dataclass(frozen=True)
class Settings:
    api_key: str
    proxy: str = ""
    ollama_url: str = "http://localhost:11434"
    model: str = "gemma3:4b"

    @classmethod
    def load(cls, root: Path):
        try:
            text = (root / ".env").read_text(encoding="utf-8-sig")
        except OSError:
            raise AppError("找不到或无法读取项目的 .env，请复制 .env.example 后填写密钥。") from None
        values = {}
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip("\"'")
        key = values.get("SERPAPI_API_KEY", "")
        if not key or any(c.isspace() for c in key):
            raise AppError(".env 中的 SERPAPI_API_KEY 为空或含空白，请重新填写。")
        url = values.get("OLLAMA_URL") or "http://localhost:11434"
        parsed = urlsplit(url)
        if parsed.hostname not in ("localhost", "127.0.0.1", "::1") or parsed.scheme != "http":
            raise AppError("OLLAMA_URL 必须是本机 HTTP 地址，避免把资料发送给远程模型。")
        return cls(key, values.get("SERPAPI_PROXY", ""), url.rstrip("/"),
                   values.get("OLLAMA_MODEL") or "gemma3:4b")
