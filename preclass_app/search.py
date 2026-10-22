import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener

from .config import AppError, Settings


def fetch_results(topic: str, settings: Settings) -> list[dict]:
    params = urlencode({"engine": "google", "q": topic, "hl": "zh-cn",
                        "no_cache": "true", "api_key": settings.api_key})
    proxy = settings.proxy
    opener = build_opener(ProxyHandler({"http": proxy, "https": proxy} if proxy else {}))
    request = Request("https://serpapi.com/search.json?" + params,
                      headers={"User-Agent": "preclass-3-lines/1.0"})
    try:
        with opener.open(request, timeout=60) as response:
            data = json.load(response)
    except HTTPError as error:
        detail = {401: "密钥无效", 403: "账号或访问受限", 429: "额度或请求频率受限"}.get(error.code, "服务请求失败")
        raise AppError(f"SerpApi {detail}（HTTP {error.code}）。") from None
    except (URLError, TimeoutError, OSError):
        raise AppError("SerpApi 连接失败或超时，请检查网络及 .env 中的代理端口。") from None
    except (ValueError, UnicodeError):
        raise AppError("SerpApi 没有返回有效 JSON，请稍后重试。") from None
    if not isinstance(data, dict) or data.get("error"):
        raise AppError("SerpApi 返回搜索错误，请检查账号配额或换一个主题。")
    items = data.get("organic_results")
    if not isinstance(items, list) or not items:
        raise AppError("没有搜到可用资料，请换一个更明确的主题。")
    items = items[:5]
    if len(items) < 5:
        raise AppError("搜索结果不足 5 条，请换一个更明确的主题。")
    results = []
    for item in items:
        if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k].strip() for k in ("title", "snippet")):
            raise AppError("前 5 条结果存在标题或摘要缺失，请换一个主题。")
        results.append({"title": item["title"].strip(), "snippet": item["snippet"].strip(),
                        "link": item.get("link", "")})
    return results


def format_sources(results: list[dict]) -> str:
    return "\n".join(f"{i}. 标题：{item['title']}\n摘要：{item['snippet']}" for i, item in enumerate(results, 1))
