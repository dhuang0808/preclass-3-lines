import contextlib
import io
import json
from http.client import IncompleteRead
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from preclass_app.cli import main
from preclass_app.config import AppError, Settings
from preclass_app.search import fetch_results
from preclass_app.summary import summarize_sources, validate_answer

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = Settings("test-only-placeholder")
ANSWER = {"what": "一种学习方法。", "why": "帮助理解课堂内容。", "example": "假设需要预测明天的销量。"}


def response(value):
    return io.BytesIO(json.dumps(value, ensure_ascii=False).encode())


class PreviewTests(unittest.TestCase):
    def test_three_short_chinese_lines(self):
        text = validate_answer(ANSWER)
        self.assertEqual(len(text.splitlines()), 3)
        self.assertTrue(all(len(line) <= 64 for line in text.splitlines()))

    def test_long_answer_is_rejected_instead_of_silently_truncated(self):
        with self.assertRaises(ValueError):
            validate_answer(dict(ANSWER, what="很" * 80))

    def test_blank_or_missing_field_is_rejected(self):
        for answer in ({"what": "内容"}, dict(ANSWER, why=" "), dict(ANSWER, example=1)):
            with self.assertRaises(ValueError):
                validate_answer(answer)

    def test_english_only_output_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_answer(dict(ANSWER, what="hello"))

    def test_marketing_placeholder_is_not_a_real_case(self):
        with self.assertRaises(ValueError):
            validate_answer(dict(ANSWER, example="Jane Doe 使用了这个模型。"))

    def test_observed_editing_instruction_leak_is_rejected(self):
        observed = '假设：客户服务机器人使用RAG，能提供更准确的产品信息。”} 替换为： 替换为：{'
        with self.assertRaisesRegex(ValueError, "编辑说明"):
            validate_answer(dict(ANSWER, example=observed))

    def test_embedded_line_breaks_cannot_add_a_fourth_line(self):
        self.assertEqual(len(validate_answer(dict(ANSWER, why="一句\n补充")).splitlines()), 3)

    @patch("preclass_app.search.build_opener")
    def test_search_uses_first_five_not_sixth_result(self, builder):
        items = [{"title": str(i), "snippet": "真实摘要", "link": "https://example.org"} for i in range(6)]
        builder.return_value.open.return_value = response({"organic_results": items})
        self.assertEqual([item["title"] for item in fetch_results("主题", SETTINGS)], [str(i) for i in range(5)])

    @patch("preclass_app.search.build_opener")
    def test_empty_search_does_not_fabricate_mock_results(self, builder):
        builder.return_value.open.return_value = response({"organic_results": []})
        with self.assertRaisesRegex(AppError, "没有搜到"):
            fetch_results("主题", SETTINGS)

    @patch("preclass_app.search.build_opener")
    def test_incomplete_snippets_fail_clearly(self, builder):
        builder.return_value.open.return_value = response({"organic_results": [{"title": "标题"}] * 5})
        with self.assertRaisesRegex(AppError, "摘要缺失"):
            fetch_results("主题", SETTINGS)

    @patch("preclass_app.search.build_opener")
    def test_credential_bearing_error_url_is_not_displayed(self, builder):
        builder.return_value.open.side_effect = HTTPError("https://example.org?api_key=SECRET-CANARY", 401, "SECRET-CANARY", {}, None)
        with self.assertRaises(AppError) as caught:
            fetch_results("主题", SETTINGS)
        self.assertNotIn("SECRET-CANARY", str(caught.exception))

    @patch("preclass_app.summary.build_opener")
    def test_invalid_generation_retries_then_passes(self, builder):
        builder.return_value.open.side_effect = [response({"done": True, "response": "{}"}),
                                                response({"done": True, "response": json.dumps(ANSWER)})]
        text, attempts = summarize_sources("主题", "来源", SETTINGS)
        self.assertEqual(attempts, 2)
        self.assertEqual(len(text.splitlines()), 3)

    @patch("preclass_app.summary.build_opener")
    def test_retry_budget_is_finite(self, builder):
        builder.return_value.open.side_effect = [response({"done": True, "response": "{}"}) for _ in range(2)]
        with self.assertRaisesRegex(AppError, "连续两次"):
            summarize_sources("主题", "来源", SETTINGS)
        self.assertEqual(builder.return_value.open.call_count, 2)

    def test_config_reads_only_local_dotenv_and_rejects_remote_model(self):
        (ROOT / ".tmp").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / ".tmp") as path:
            root = Path(path)
            (root / ".env").write_text("\ufeffSERPAPI_API_KEY=local-test-key\n", encoding="utf-8")
            self.assertEqual(Settings.load(root).api_key, "local-test-key")
            (root / ".env").write_text("SERPAPI_API_KEY=local-test-key\nOLLAMA_URL=https://example.org\n", encoding="utf-8")
            with self.assertRaises(AppError):
                Settings.load(root)

    @patch("preclass_app.cli.run_preview", side_effect=AppError("没有搜到可用资料。"))
    def test_cli_errors_are_one_line_without_traceback(self, _):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(["主题"])
        self.assertEqual(code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue().splitlines(), ["没有搜到可用资料。"])

    def test_missing_topic_is_one_safe_line(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(main([]), 1)
        self.assertEqual(len(err.getvalue().splitlines()), 1)

    @patch("preclass_app.cli.run_preview", side_effect=IncompleteRead(b"PRIVATE-PARTIAL-CANARY", 20))
    def test_partial_http_response_does_not_expose_body_or_traceback(self, _):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(main(["主题"]), 1)
        self.assertEqual(len(err.getvalue().splitlines()), 1)
        self.assertNotIn("PRIVATE-PARTIAL-CANARY", err.getvalue())


if __name__ == "__main__":
    unittest.main()
