"""AI rewriting contracts: trusted grounding, scripts, safe transport and fallback."""

from copy import deepcopy
import io
import json
import os
import socket
import ssl
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from core.ai_rewriter import _RejectRedirects, _tls_context, rewrite_copy, urlopen
from core.chinese_converter import convert_script


TERMS = [
    {"id": 1, "term_en": "Product Seeding", "term_hk": "好物推介", "term_cn": "种草",
     "aliases": ["seeding", "種草", "安利"], "meaning": "分享真实用家体验。"},
    {"id": 2, "term_en": "Free Shipping", "term_hk": "免運費", "term_cn": "包邮",
     "aliases": ["包郵", "free delivery"], "meaning": "免收运费。"},
]


def response(content=None, *, finish="stop"):
    value = content if content is not None else {
        "primary_copy": "全新面霜，清爽保湿。包邮。立即选购。",
        "alt_copy": "清爽面霜现已登场，包邮。",
        "adaptations": [{"original": "包邮", "adapted": "免運費", "reason": "符合香港用语", "term_id": 999}],
        "cta_options": ["按连结了解详情。", "私讯我们，了解更多。"],
    }
    body = {"choices": [{"finish_reason": finish, "message": {
        "content": value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)}}]}
    return io.BytesIO(json.dumps(body, ensure_ascii=False).encode())


class RewriterTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {
            "DEEPSEEK_API_KEY": "", "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
            "DEEPSEEK_MODEL": ""})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_missing_key_fallback_never_calls_network(self):
        with patch("core.ai_rewriter.urlopen") as call:
            result = rewrite_copy("新品面霜，亲肤保湿，包邮。", "hk", "standard", TERMS)
        call.assert_not_called()
        self.assertEqual(result["engine"], "fallback")
        self.assertIn("本地", result["notice"])
        self.assertIn("免運費", result["primary_copy"])
        self.assertIn("親膚保濕", result["primary_copy"])
        self.assertEqual(result["primary_copy"], convert_script(result["primary_copy"], "hk"))
        self.assertEqual(len(result["cta_options"]), 2)
        self.assertGreater(result["counts"]["character_count"], 0)
        self.assertEqual(result["source_counts"]["character_count"], 13)

    def test_placeholder_key_and_empty_glossary(self):
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "your_deepseek_api_key_here"}), \
                patch("core.ai_rewriter.urlopen") as call:
            result = rewrite_copy("亲，包邮！", "hk", "social", [])
        call.assert_not_called()
        self.assertIn("免運費", result["primary_copy"])
        self.assertEqual(result["matched_glossary_terms"], [])

    def test_hk_all_character_and_ambiguous_phrase_conversion(self):
        text = "头发干燥，后台发货，面向顾客开发设计。轻盈亲肤，清爽保湿，适合日常使用。"
        output = convert_script(text, "hk")
        self.assertEqual(output, "頭髮乾燥，後台發貨，面向顧客開發設計。輕盈親膚，清爽保濕，適合日常使用。")
        self.assertEqual(convert_script("閱讀體驗與獨家聯乘，質感細緻，香港免運費。", "cn"),
                         "阅读体验与独家联乘，质感细致，香港免运费。")

    def test_fallback_tones_are_distinct_but_keep_facts(self):
        text = "品牌联名面霜将于11月12日推出，售价HK$280，香港包邮。请关注。"
        outputs = [rewrite_copy(text, "hk", tone, TERMS)["primary_copy"]
                   for tone in ("standard", "social", "concise")]
        self.assertGreater(len(set(outputs)), 1)
        for output in outputs:
            for fact in ("11月12日", "HK$280", "香港", "免運費"):
                self.assertIn(fact, output)
            self.assertNotIn("限量", output)

    def test_mainland_fallback_localizes_complete_script(self):
        result = rewrite_copy("全新聯乘面霜，親膚質感，香港免運費。", "cn", "standard", TERMS)
        self.assertIn("包邮", result["primary_copy"])
        self.assertNotIn("親膚", result["primary_copy"])
        self.assertEqual(result["primary_copy"], convert_script(result["primary_copy"], "cn"))

    def test_english_fallback_is_honest_about_untranslated_source(self):
        result = rewrite_copy("全新面霜，包邮。", "en", "standard", TERMS)
        self.assertEqual(result["engine"], "fallback")
        self.assertIn("英文", result["notice"])
        self.assertNotIn("award-winning", result["primary_copy"])

    def test_live_request_uses_grounding_format_timeout_and_normalizes_output(self):
        os.environ["DEEPSEEK_API_KEY"] = "test-key-never-real"
        with patch("core.ai_rewriter.urlopen", return_value=response()) as call:
            result = rewrite_copy("全新面霜，清爽保湿，包邮。", "hk", "standard", TERMS)
        request = call.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(request.full_url, "https://api.deepseek.com/chat/completions")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(call.call_args.kwargs["timeout"], 25)
        self.assertEqual(payload["response_format"], {"type": "json_object"})
        self.assertEqual(payload["thinking"], {"type": "disabled"})
        self.assertIsNone(result["error_code"])
        self.assertEqual(payload["model"], "deepseek-flash")
        prompt = payload["messages"][0]["content"]
        self.assertIn("Mandatory Brand Glossary Constraints", prompt)
        self.assertIn("免運費", prompt)
        self.assertIn("Do not invent", prompt)
        self.assertIn("source_draft", payload["messages"][1]["content"])
        self.assertEqual(result["engine"], "deepseek")
        for key in ("primary_copy", "alt_copy"):
            self.assertIn("免運費", result[key])
            self.assertEqual(result[key], convert_script(result[key], "hk"))
        self.assertEqual(result["adaptations"][0]["term_id"], 2)
        self.assertTrue(all(item["term_id"] != 999 for item in result["adaptations"]))
        self.assertEqual(result["cta_options"][0], "按連結了解詳情。")

    def test_configured_base_uses_flash_even_if_model_setting_is_stale(self):
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test", "DEEPSEEK_BASE_URL": "https://gateway.example/v1/",
                                     "DEEPSEEK_MODEL": "configured-model"}), \
                patch("core.ai_rewriter.urlopen", return_value=response()) as call:
            rewrite_copy("包邮", "hk", "concise", TERMS)
        self.assertEqual(call.call_args.args[0].full_url, "https://gateway.example/v1/chat/completions")
        self.assertEqual(json.loads(call.call_args.args[0].data)["model"], "deepseek-flash")

    def test_media_styles_and_temperatures_for_out_of_glossary_drafts(self):
        style_names = {
            "hk": ["Lane Crawford", "香港 Instagram / Threads", "WhatsApp"],
            "cn": ["微信公众号", "小红书", "抖音"],
            "en": ["Luxury & DTC", "TikTok", "Shopify"],
        }
        draft = "周末有一场读书会。"
        prompts = set()
        for market, names in style_names.items():
            for (tone, temperature), name in zip((("standard", 0.5), ("social", 0.75), ("concise", 0.35)), names):
                with self.subTest(market=market, tone=tone), \
                        patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                        patch("core.ai_rewriter.urlopen", return_value=response()) as call:
                    result = rewrite_copy(draft, market, tone, [])
                self.assertEqual(result["matched_glossary_terms"], [])
                payload = json.loads(call.call_args.args[0].data)
                self.assertEqual(payload["model"], "deepseek-flash")
                self.assertEqual(payload["temperature"], temperature)
                self.assertEqual(json.loads(payload["messages"][1]["content"]), {"source_draft": draft})
                prompt = payload["messages"][0]["content"]
                self.assertIn(name, prompt)
                self.assertIn('{"terms":[],"matched_rules":[]}', prompt)
                self.assertIn("3 to 6 concrete adaptations", prompt)
                self.assertIn("even when the glossary and matched rules are empty", prompt)
                self.assertIn("满299 means at least 299", prompt)
                self.assertIn("including account follows, in both versions", prompt)
                self.assertIn("Never infer a product feature", prompt)
                self.assertIn("source_draft is the sole factual authority", prompt)
                self.assertNotIn(draft, prompt)
                prompts.add(prompt)
        self.assertEqual(len(prompts), 9)

    def test_adaptations_quote_actual_text_without_case_or_edge_whitespace_mismatches(self):
        content = {
            "primary_copy": "Discover our morning gathering.",
            "alt_copy": "Make room for the Sunday reading circle.",
            "cta_options": ["Explore the reading circle.", "See what's planned for Sunday."],
            "adaptations": [
                {"original": "  sunday book club  ", "adapted": " THE SUNDAY READING CIRCLE ",
                 "reason": "英文社群语感", "term_id": 999},
                {"original": "Sunday book club", "adapted": "the Sunday reading circle", "reason": "重复", "term_id": None},
                {"original": "Sunday book club", "adapted": "gathering.\nMake room", "reason": "跨版本", "term_id": None},
                {"original": "Fictional offer", "adapted": "our morning gathering", "reason": "虚构", "term_id": None},
            ],
        }
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(content)):
            result = rewrite_copy("Join our Sunday Book Club.", "en", "social", [])
        self.assertEqual(result["engine"], "deepseek")
        self.assertEqual(result["adaptations"], [{"original": "Sunday Book Club", "adapted": "the Sunday reading circle",
                                                   "reason": "英文社群语感", "term_id": None}])

    def test_important_glossary_and_model_changes_share_a_six_edit_cap(self):
        draft = "香港包邮。" + " ".join(f"source {index}" for index in range(10))
        content = {
            "primary_copy": "香港免運費。" + " ".join(f"output {index}" for index in range(10)),
            "alt_copy": "了解香港免運費安排。",
            "cta_options": ["查看詳情。", "查閱送貨安排。"],
            "adaptations": [
                {"original": f"source {index}", "adapted": f"output {index}", "reason": "改為港式語感"}
                for index in range(10)
            ],
        }
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(content)):
            result = rewrite_copy(draft, "hk", "standard", TERMS)
        self.assertEqual(len(result["adaptations"]), 6)
        self.assertEqual(result["adaptations"][0]["term_id"], 2)
        self.assertEqual([row["original"] for row in result["adaptations"][1:]],
                         [f"source {index}" for index in range(5)])

    def test_network_failures_return_clear_safe_fallback(self):
        for error in (URLError("private internals"), socket.timeout(),
                      HTTPError("https://api.deepseek.com", 401, "sensitive-token", {}, None)):
            with self.subTest(error=type(error).__name__), \
                    patch.dict(os.environ, {"DEEPSEEK_API_KEY": "secret-key"}), \
                    patch("core.ai_rewriter.urlopen", side_effect=error):
                result = rewrite_copy("清爽保湿，包邮。", "hk", "standard", TERMS)
                self.assertEqual(result["engine"], "fallback")
                self.assertNotIn("secret-key", result["notice"])
                self.assertNotIn("private internals", result["notice"])
                self.assertIn("免運費", result["primary_copy"])

    def test_malformed_truncated_and_oversized_responses_fallback(self):
        values = [io.BytesIO(b"not json"), response("   "), response({}),
                  response(finish="length"), io.BytesIO(b" " * 300_001),
                  response({"primary_copy": "x", "alt_copy": "x", "adaptations": [], "cta_options": "wrong"})]
        for value in values:
            with self.subTest(value=value), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                    patch("core.ai_rewriter.urlopen", return_value=value):
                self.assertEqual(rewrite_copy("包邮", "hk", "standard", TERMS)["engine"], "fallback")

    def test_model_cannot_assign_unmatched_term_or_fake_adaptation(self):
        content = {"primary_copy": "免運費，親膚面霜。", "alt_copy": "親膚面霜，免運費。",
                   "cta_options": ["了解詳情。", "私訊查詢。"], "adaptations": [
                       {"original": "not in source", "adapted": "親膚", "reason": "fake", "term_id": 1},
                       {"original": "包邮", "adapted": "免運費", "reason": "香港配送用语", "term_id": 1}]}
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(content)):
            result = rewrite_copy("亲肤面霜，包邮。", "hk", "standard", TERMS)
        self.assertEqual({term["id"] for term in result["matched_glossary_terms"]}, {2})
        self.assertTrue(all(item["original"] != "not in source" for item in result["adaptations"]))
        self.assertTrue(all(item["term_id"] in (None, 2) for item in result["adaptations"]))

    def test_glossary_source_and_results_are_independent(self):
        original = deepcopy(TERMS)
        result = rewrite_copy("包邮，值得种草。", "hk", "social", TERMS)
        self.assertEqual(TERMS, original)
        result["matched_glossary_terms"][0]["term_hk"] = "changed"
        self.assertEqual(TERMS, original)

    def test_invalid_inputs_fail_before_network(self):
        for args in [(None, "hk", "standard"), ("", "hk", "standard"),
                     ("draft", [], "standard"), ("draft", "xx", "standard"),
                     ("draft", "hk", {}), ("draft", "hk", "urgent"),
                     ("x" * 20_001, "hk", "standard"), ("\ud800", "hk", "standard"),
                     ("draft\x00", "hk", "standard")]:
            with self.subTest(args=args), patch("core.ai_rewriter.urlopen") as call:
                with self.assertRaises((TypeError, ValueError)):
                    rewrite_copy(*args, glossary=TERMS)
                call.assert_not_called()

    def test_insecure_or_malformed_endpoint_does_not_send_key(self):
        for base in ("http://api.deepseek.com", "file:///etc/passwd", "https://user:pass@example.com", "https://example.com/#frag"):
            with self.subTest(base=base), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "secret", "DEEPSEEK_BASE_URL": base}), \
                    patch("core.ai_rewriter.urlopen") as call:
                result = rewrite_copy("包邮", "hk", "standard", TERMS)
                self.assertEqual(result["engine"], "fallback")
                call.assert_not_called()

    def test_fallback_preserves_decimal_prices_thousands_and_urls_all_tones(self):
        source = "面霜 HK$280.50，礼盒 HK$1,299。详情：https://shop.example.com/购买?优惠=免运费"
        url = "https://shop.example.com/购买?优惠=免运费"
        for tone in ("standard", "social", "concise"):
            result = rewrite_copy(source, "hk", tone, TERMS)
            for key in ("primary_copy", "alt_copy"):
                self.assertIn("HK$280.50", result[key])
                self.assertIn("HK$1,299", result[key])
                self.assertIn(url, result[key])
        self.assertEqual(convert_script(url, "hk"), url)

    def test_fallback_preserves_whitespace_around_urls(self):
        source = "Learn more at https://example.com/立即选购 now."
        for market in ("hk", "cn", "en"):
            for tone in ("standard", "social", "concise"):
                result = rewrite_copy(source, market, tone, [])
                self.assertEqual(result["primary_copy"], source)
                self.assertEqual(result["alt_copy"], source)

    def test_invalid_envelope_shapes_all_return_fallback(self):
        for value in ({"choices": [None]}, {"choices": ["x"]}, {"choices": []},
                      {"choices": [{"finish_reason": "stop", "message": None}]},
                      {"choices": [{"finish_reason": "stop", "message": {"content": []}}]}, []):
            with self.subTest(value=value), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                    patch("core.ai_rewriter.urlopen", return_value=io.BytesIO(json.dumps(value).encode())):
                self.assertEqual(rewrite_copy("包邮", "hk", "standard", TERMS)["engine"], "fallback")
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=io.BytesIO(b"[" * 2000 + b"]" * 2000)):
            self.assertEqual(rewrite_copy("包邮", "hk", "standard", TERMS)["engine"], "fallback")

    def test_transport_disables_redirects_and_preserves_timeout(self):
        from urllib.request import Request
        request = Request("https://api.deepseek.com/chat/completions")
        with self.assertRaises(HTTPError) as caught:
            _RejectRedirects().redirect_request(request, None, 302, "Moved", {}, "https://attacker.example")
        caught.exception.close()
        with patch("core.ai_rewriter.build_opener") as build:
            urlopen(request, timeout=25)
        self.assertIsInstance(build.call_args.args[0], _RejectRedirects)
        build.return_value.open.assert_called_once_with(request, timeout=25)

    def test_default_library_is_loaded_at_call_time(self):
        from core.search_engine import SearchEngine
        with patch("core.db_manager.DBManager") as manager:
            manager.return_value.get_search_engine.return_value = SearchEngine(TERMS)
            result = rewrite_copy("包邮", "hk")
        self.assertEqual([term["id"] for term in result["matched_glossary_terms"]], [2])
        manager.return_value.get_search_engine.assert_called_once_with()

    def test_invalid_english_body_or_cta_returns_explicit_preview(self):
        for body, ctas in [("面霜", ["Learn more.", "Get in touch."]),
                           ("A daily moisturiser.", ["了解详情。", "Get in touch."])]:
            content = {"primary_copy": body, "alt_copy": "Your daily ritual.", "adaptations": [], "cta_options": ctas}
            with self.subTest(body=body), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                    patch("core.ai_rewriter.urlopen", return_value=response(content)):
                result = rewrite_copy("面霜", "en", "standard", TERMS)
            self.assertEqual(result["engine"], "fallback")

    def test_output_all_aliases_canonicalized_even_when_source_is_already_correct(self):
        content = {"primary_copy": "新品包邮。", "alt_copy": "新品 free delivery。", "adaptations": [],
                   "cta_options": ["包郵詳情請查詢。", "了解更多。"]}
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(content)):
            result = rewrite_copy("新品免運費。", "hk", "standard", TERMS)
        self.assertEqual(result["engine"], "deepseek")
        self.assertEqual(result["primary_copy"], "新品免運費。")
        self.assertIn("免運費", result["alt_copy"])
        self.assertIn("免運費", result["cta_options"][0])
        self.assertEqual(result["adaptations"], [])

    def test_custom_brand_terms_override_generic_rules_and_match_latin_case(self):
        glossary = [{"id": 10, "term_en": "Star Shipping", "term_hk": "星瀾送貨禮遇",
                     "term_cn": "星澜配送福利", "aliases": ["包邮", "free delivery"]}]
        content = {"primary_copy": "FREE DELIVERY。", "alt_copy": "包郵。", "adaptations": [],
                   "cta_options": ["了解詳情。", "私訊查詢。"]}
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(content)):
            result = rewrite_copy("包邮。", "hk", "standard", glossary)
        self.assertEqual(result["primary_copy"], "星瀾送貨禮遇。")
        self.assertEqual(result["alt_copy"], "星瀾送貨禮遇。")
        self.assertEqual(result["adaptations"][0]["term_id"], 10)

    def test_canonical_prefix_alias_never_duplicates_suffix_and_is_idempotent(self):
        from core.rewrite_grounding import apply_constraints, output_constraints
        glossary = [{**TERMS[1], "aliases": [*TERMS[1]["aliases"], "免運", "免运"]}]
        constraints = output_constraints(glossary, "hk")
        exact = "早鳥禮遇至3月20日；禮盒免運費。"
        self.assertEqual(apply_constraints(exact, constraints, "hk"), exact)
        self.assertEqual(apply_constraints(apply_constraints("禮盒免運。", constraints, "hk"),
                                           constraints, "hk"), "禮盒免運費。")
        content = {"primary_copy": exact, "alt_copy": "禮盒免運費。", "adaptations": [],
                   "cta_options": ["免運費詳情請查詢。", "了解更多。"]}
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(content)):
            result = rewrite_copy("禮盒包邮。", "hk", "standard", glossary)
        self.assertEqual(result["primary_copy"], exact)
        self.assertEqual(result["alt_copy"], "禮盒免運費。")
        self.assertEqual(result["cta_options"][0], "免運費詳情請查詢。")
        self.assertEqual(rewrite_copy("禮盒免運費。", "hk", "standard", glossary)["primary_copy"], "禮盒免運費。")

    def test_flagship_canonical_terms_survive_repeated_enforcement(self):
        from core.rewrite_grounding import apply_constraints, canonical_expression, output_constraints
        from data.seed_terms import build_seed_terms
        glossary = build_seed_terms()
        for market in ("hk", "cn", "en"):
            constraints = output_constraints(glossary, market)
            for term in glossary:
                target = convert_script(canonical_expression(term, market), market)
                with self.subTest(market=market, term_id=term["id"]):
                    first = apply_constraints(target, constraints, market)
                    self.assertEqual(first, target)
                    self.assertEqual(apply_constraints(first, constraints, market), target)

    def test_cross_script_alias_retrieval_retains_exact_source_phrase(self):
        from core.rewrite_grounding import retrieve_constraints
        from data.seed_terms import build_seed_terms
        glossary = build_seed_terms()
        source = "春日联名礼盒，早鸟福利至3月20日，包邮。"
        matched, constraints = retrieve_constraints(source, "hk", glossary)
        self.assertIn(62, {term["id"] for term in matched})
        crossover = next(item for item in constraints if item["original"] == "联名")
        self.assertEqual(crossover["adapted"], "跨界聯乘")
        self.assertEqual(crossover["term_id"], 62)
        self.assertTrue(all(item["original"] in source for item in constraints))
        self.assertLess(len(matched), 6)
        # A definition mentioning collaboration must not expand into a match.
        neutral, _ = retrieve_constraints("温和面霜，滋润双手。", "hk", glossary)
        self.assertEqual(neutral, [])

    def test_tls_context_adds_os_bundle_only_for_missing_default(self):
        from types import SimpleNamespace
        with patch("core.ai_rewriter.ssl.create_default_context") as create, \
                patch("core.ai_rewriter.ssl.get_default_verify_paths", return_value=SimpleNamespace(cafile=None)), \
                patch("core.ai_rewriter.Path.is_file", return_value=True), \
                patch.dict(os.environ, {"SSL_CERT_FILE": ""}):
            context = _tls_context()
        self.assertIs(context, create.return_value)
        context.load_verify_locations.assert_called_once_with(cafile="/etc/ssl/cert.pem")
        with patch("core.ai_rewriter.ssl.create_default_context") as create, \
                patch("core.ai_rewriter.ssl.get_default_verify_paths", return_value=SimpleNamespace(cafile="/valid/default.pem")):
            _tls_context()
        create.return_value.load_verify_locations.assert_not_called()
        with patch("core.ai_rewriter.ssl.create_default_context") as create, \
                patch("core.ai_rewriter.ssl.get_default_verify_paths", return_value=SimpleNamespace(cafile=None)), \
                patch.dict(os.environ, {"SSL_CERT_FILE": "/custom/trust.pem"}):
            _tls_context()
        create.return_value.load_verify_locations.assert_not_called()

    def test_missing_or_placeholder_key_identifies_configuration(self):
        for key in ("", "your_deepseek_api_key_here"):
            with self.subTest(key=key), patch.dict(os.environ, {"DEEPSEEK_API_KEY": key}), \
                    patch("core.ai_rewriter.urlopen") as call:
                result = rewrite_copy("包邮", "hk", "standard", TERMS)
            self.assertEqual(result["error_code"], "missing_key")
            self.assertIn("未配置 DeepSeek 密钥", result["notice"])
            call.assert_not_called()

    def test_configuration_error_is_distinct_from_invalid_result(self):
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test", "DEEPSEEK_BASE_URL": "http://api.deepseek.com"}), \
                patch("core.ai_rewriter.urlopen") as call:
            result = rewrite_copy("包邮", "hk", "standard", TERMS)
        self.assertEqual(result["error_code"], "invalid_config")
        self.assertIn("配置", result["notice"])
        call.assert_not_called()
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=io.BytesIO(b"not json")):
            result = rewrite_copy("包邮", "hk", "standard", TERMS)
        self.assertEqual(result["error_code"], "invalid_response")
        self.assertIn("格式", result["notice"])
        self.assertNotIn("暂不可用", result["notice"])

    def test_http_failures_have_safe_specific_codes_and_notices(self):
        cases = [(401, "auth_failed", "验证"), (403, "auth_failed", "验证"),
                 (402, "insufficient_balance", "余额不足"), (429, "rate_limited", "稍后"),
                 (500, "service_unavailable", "暂不可用"), (503, "service_unavailable", "暂不可用"),
                 (400, "invalid_config", "配置"), (404, "invalid_config", "配置")]
        for status, code, notice in cases:
            with self.subTest(status=status), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "private-key"}), \
                    patch("core.ai_rewriter.urlopen", side_effect=HTTPError(
                        "https://private-endpoint.example", status, "private-error-body", {}, io.BytesIO(b"sensitive"))):
                result = rewrite_copy("private-source 包邮", "hk", "standard", TERMS)
            self.assertEqual(result["engine"], "fallback")
            self.assertEqual(result["error_code"], code)
            self.assertIn(notice, result["notice"])
            for secret in ("private-key", "private-endpoint", "private-error-body", "sensitive", "private-source"):
                self.assertNotIn(secret, result["notice"])
                self.assertNotIn(secret, result["error_code"])

    def test_timeout_tls_and_network_are_separate_including_wrapped_reasons(self):
        cases = [(socket.timeout("private-details"), "timeout", "25 秒"),
                 (URLError(socket.timeout("private-details")), "timeout", "25 秒"),
                 (URLError("request timed out: private-details"), "timeout", "25 秒"),
                 (ssl.SSLCertVerificationError("private-cert"), "tls_error", "安全连接"),
                 (URLError(ssl.SSLError("private-cert")), "tls_error", "安全连接"),
                 (URLError("[SSL: CERTIFICATE_VERIFY_FAILED] private-cert"), "tls_error", "安全连接"),
                 (URLError("private-host"), "network_error", "连接失败"),
                 (ConnectionResetError("private-host"), "network_error", "连接失败")]
        for error, code, notice in cases:
            with self.subTest(code=code, kind=type(error).__name__), \
                    patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                    patch("core.ai_rewriter.urlopen", side_effect=error):
                result = rewrite_copy("包邮", "hk", "standard", TERMS)
            self.assertEqual(result["error_code"], code)
            self.assertIn(notice, result["notice"])
            for secret in ("private-details", "private-cert", "private-host"):
                self.assertNotIn(secret, result["notice"])

    def test_local_certificate_setup_failure_is_not_reported_as_network(self):
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.ssl.create_default_context", side_effect=FileNotFoundError("private-cert-path")):
            result = rewrite_copy("包邮", "hk", "standard", TERMS)
        self.assertEqual(result["error_code"], "tls_error")
        self.assertIn("安全连接", result["notice"])
        self.assertNotIn("private-cert-path", result["notice"])

    def test_live_english_prose_may_preserve_han_in_url_but_not_in_sentences(self):
        url = "https://example.com/活動"
        ctas = [f"Learn more at {url}", "Explore this weekend's event."]
        content = {"primary_copy": f"Join our weekend reading circle. {url}", "alt_copy": "Make time for the book club.",
                   "adaptations": [], "cta_options": ctas}
        source = f"周末有读书会。查看详情 {url}"
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(content)):
            result = rewrite_copy(source, "en", "standard", [])
        self.assertEqual(result["engine"], "deepseek")
        self.assertEqual(result["primary_copy"], content["primary_copy"])
        self.assertEqual(result["cta_options"], ctas)
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response({**content, "alt_copy": "𠀀 book club"})):
            result = rewrite_copy(source, "en", "standard", [])
        self.assertEqual(result["error_code"], "incomplete_translation")

    def test_native_phrase_inflection_survives_glossary_post_processing(self):
        from data.seed_terms import build_seed_terms
        glossary = build_seed_terms()
        cases = (
            ("性價比高，買滿即送明信片。", "cn", "性价比挺高，买满即送明信片。"),
            ("性价比高。", "hk", "性價比幾高。"),
            ("性价比高。", "en", "It offers good value for money."),
        )
        for source, market, primary in cases:
            with self.subTest(market=market), patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                    patch("core.ai_rewriter.urlopen", return_value=response({
                        "primary_copy": primary, "alt_copy": primary, "adaptations": [],
                        "cta_options": ["Find out more.", "Explore the details."],
                    })):
                result = rewrite_copy(source, market, "standard", glossary)
            self.assertEqual(result["engine"], "deepseek")
            self.assertEqual(result["primary_copy"], primary)

    def test_incomplete_translation_and_truncated_response_are_distinct(self):
        chinese = {"primary_copy": "新品面霜。", "alt_copy": "A daily ritual.",
                   "adaptations": [], "cta_options": ["Learn more.", "Explore the details."]}
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(chinese)):
            result = rewrite_copy("新品面霜。", "en", "standard", TERMS)
        self.assertEqual(result["error_code"], "incomplete_translation")
        self.assertIn("英文", result["notice"])
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), \
                patch("core.ai_rewriter.urlopen", return_value=response(finish="length")):
            result = rewrite_copy("包邮", "hk", "standard", TERMS)
        self.assertEqual(result["error_code"], "incomplete_response")
        self.assertIn("未完成", result["notice"])

    def test_enforcement_uses_word_boundaries(self):
        glossary = [{"id": 8, "term_en": "Return on Ad Spend", "term_hk": "廣告投資回報", "term_cn": "广告支出回报", "aliases": ["ROAS"]}]
        result = rewrite_copy("Fresh roast coffee.", "en", "standard", glossary)
        self.assertEqual(result["matched_glossary_terms"], [])
        self.assertIn("roast", result["primary_copy"])


if __name__ == "__main__":
    unittest.main()
