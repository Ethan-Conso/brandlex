"""Behavior checks for market adaptation and actionable copy feedback."""

import unittest
from unittest.mock import patch

from core.copy_checker import analyze_copy, apply_suggestion
from core.copy_rules import RULES


class CopyCheckerTests(unittest.TestCase):
    def check_copy(self, text, market="hk", glossary=None):
        return analyze_copy(text, market, glossary=glossary or [])

    def test_cross_regional_rules_cover_three_markets(self):
        self.assertGreaterEqual(len(RULES), 35)
        self.assertEqual({rule.market for rule in RULES}, {"hk", "cn", "en"})

    def test_hk_conversion_including_traditional_mainland_slang(self):
        result = self.check_copy("亲，早鸟福利到！包邮爆款值得种草。聯名款也包郵，立即入手。")
        replacements = {item["original_span"]: item["suggested_replacement"]
                        for item in result["suggestions"]}
        self.assertEqual(replacements["包邮"], "免運費")
        self.assertEqual(replacements["包郵"], "免運費")
        self.assertEqual(replacements["亲"], "各位")
        self.assertEqual(replacements["早鸟福利"], "早鳥禮遇")
        self.assertEqual(replacements["聯名"], "聯乘")

    def test_mainland_conversion(self):
        result = self.check_copy("期間限定店有聯乘皇牌產品，免運費。立即购买。", "cn")
        replacements = {item["suggested_replacement"] for item in result["suggestions"]}
        self.assertTrue({"快闪店", "联名", "爆款单品", "包邮"} <= replacements)

    def test_english_literal_copy(self):
        result = self.check_copy("Welcome to buy our new headphones with high cost performance.", "en")
        self.assertTrue(any(item["original_span"].lower() == "welcome to buy"
                            for item in result["suggestions"]))
        self.assertTrue(any(item["suggested_replacement"] == "great value"
                            for item in result["suggestions"]))

    def test_literal_chinese_pattern_and_no_nested_duplicates(self):
        text = "解锁你皮肤的潜能，给你带来前所未有的体验。"
        result = self.check_copy(text)
        spans = [(item["start"], item["end"]) for item in result["suggestions"]]
        self.assertTrue(any(item["category"] == "生硬直译" for item in result["suggestions"]))
        self.assertTrue(all(left[1] <= right[0] for left, right in zip(spans, spans[1:])))

    def test_repeated_occurrences_preserve_exact_unicode_offsets(self):
        text = "✨包邮！包邮！立即入手。"
        suggestions = self.check_copy(text)["suggestions"]
        shipping = [item for item in suggestions if item["original_span"] == "包邮"]
        self.assertEqual(len(shipping), 2)
        for item in suggestions:
            self.assertEqual(text[item["start"]:item["end"]], item["original_span"])
        self.assertNotEqual(shipping[0]["id"], shipping[1]["id"])

    def test_salutation_does_not_flag_skin_friendly_or_family(self):
        result = self.check_copy("親膚面料，亲肤柔软，亲子出游。立即入手。")
        self.assertFalse(any(item["original_span"] in {"亲", "親"}
                             for item in result["suggestions"]))

    def test_missing_cta_gives_three_safe_insertions(self):
        text = "輕盈面霜，為日常補水。"
        result = self.check_copy(text)
        self.assertEqual(result["cta_strength"], "missing")
        self.assertEqual(len(result["cta_suggestions"]), 3)
        for item in result["cta_suggestions"]:
            self.assertEqual(item["start"], len(text))
            self.assertEqual(item["end"], len(text))
            self.assertEqual(item["original_span"], "")
            self.assertTrue(apply_suggestion(text, item).startswith(text))

    def test_strong_ending_cta_and_weak_earlier_cta(self):
        for market, text in [("hk", "柔潤面霜現已登場。立即入手。"),
                             ("cn", "补水面霜上新。立即购买。"),
                             ("en", "Meet your everyday moisturiser. Shop now.")]:
            with self.subTest(market=market):
                result = self.check_copy(text, market)
                self.assertEqual(result["cta_strength"], "strong")
                self.assertEqual(result["cta_suggestions"], [])
        result = self.check_copy("Shop now. Our new moisturiser is light and comfortable.", "en")
        self.assertEqual(result["cta_strength"], "weak")

    def test_every_generated_cta_is_recognised_after_insertion(self):
        for market, text in [("hk", "柔潤面霜現已登場。"),
                             ("cn", "补水面霜上新。"), ("en", "Meet your everyday moisturiser.")]:
            for item in self.check_copy(text, market)["cta_suggestions"]:
                with self.subTest(market=market, ending=item["suggested_replacement"]):
                    updated = apply_suggestion(text, item)
                    self.assertEqual(self.check_copy(updated, market)["cta_strength"], "strong")

    def test_ending_cta_remains_strong_with_emoji_hashtag_or_link(self):
        for text in ["Shop now. 🎁", "Shop now. #skincare", "Shop now. https://example.com/shop"]:
            with self.subTest(text=text):
                self.assertEqual(self.check_copy(text, "en")["cta_strength"], "strong")

    def test_replacement_cta_is_recognised(self):
        text = "Please click the link to purchase."
        item = self.check_copy(text, "en")["suggestions"][0]
        self.assertEqual(self.check_copy(apply_suggestion(text, item), "en")["cta_strength"], "strong")

    def test_glossary_matches_full_records_and_avoids_latin_substrings(self):
        glossary = [{"id": 1, "term_en": "ROAS", "term_hk": "廣告投資回報", "term_cn": "广告支出回报", "aliases": []},
                    {"id": 2, "term_en": "IG", "term_hk": "Instagram", "term_cn": "照片社交平台", "aliases": []}]
        result = self.check_copy("Review ROAS for this big campaign. Shop now.", "en", glossary)
        self.assertEqual(result["matched_glossary_terms"], [glossary[0]])
        self.assertIsNot(result["matched_glossary_terms"][0], glossary[0])

    def test_default_analysis_reads_current_library_each_time(self):
        term = {"id": 1, "term_en": "ROAS", "term_hk": "廣告投資回報", "term_cn": "广告支出回报", "aliases": []}
        with patch("core.db_manager.DBManager") as manager:
            manager.return_value.get_search_engine.side_effect = [[term], []]
            self.assertEqual(analyze_copy("ROAS", "en")["matched_glossary_terms"], [term])
            self.assertEqual(analyze_copy("ROAS", "en")["matched_glossary_terms"], [])
            self.assertEqual(manager.call_count, 2)

    def test_mixed_english_body_can_report_chinese_without_zeroing_score(self):
        result = self.check_copy("Our new daily moisturiser is gentle and light. 春日限定新品 Shop now.", "en")
        self.assertTrue(result["warnings"])
        self.assertGreater(result["score"], 50)

    def test_invalid_suggestion_is_rejected(self):
        for suggestion in [None, {"start": True, "end": 1, "original_span": "x", "suggested_replacement": "y"},
                           {"start": 0, "end": 99, "original_span": "x", "suggested_replacement": "y"}]:
            with self.subTest(suggestion=suggestion):
                with self.assertRaises((TypeError, ValueError)):
                    apply_suggestion("x", suggestion)

    def test_negated_cta_does_not_count_as_strong(self):
        self.assertNotEqual(self.check_copy("Don't shop now.", "en")["cta_strength"], "strong")
        self.assertNotEqual(self.check_copy("不要立即购买。", "cn")["cta_strength"], "strong")

    def test_other_negative_endings_do_not_count_as_strong(self):
        for market, text in [("en", "You should not shop now."),
                             ("en", "There is no need to shop now."),
                             ("en", "Not ready to shop now."),
                             ("cn", "不要现在立即购买。"),
                             ("hk", "請勿現在立即入手。")]:
            with self.subTest(text=text):
                self.assertNotEqual(self.check_copy(text, market)["cta_strength"], "strong")

    def test_distinctive_wrong_script_warns_without_full_conversion(self):
        for market, text in [("hk", "新品上市，温和亲肤，清爽保湿，适合每日使用。立即入手。"),
                             ("cn", "全新面霜現已登場，清爽質感滋潤肌膚。立即购买。")]:
            with self.subTest(market=market):
                result = self.check_copy(text, market)
                self.assertTrue(result["warnings"])
                self.assertLess(result["score"], 100)
        self.assertEqual(self.check_copy("台灣品牌，親膚面霜。立即入手。", "hk")["warnings"], [])

    def test_counts_and_empty_copy_are_honest(self):
        result = self.check_copy("  \n  ", "en")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["word_count"], 0)
        self.assertEqual(result["character_count"], 0)
        self.assertEqual(result["reading_time_seconds"], 0)
        self.assertEqual(result["paragraph_count"], 0)
        mixed = self.check_copy("Shop now!\n\n新品上市。", "hk")
        self.assertEqual(mixed["paragraph_count"], 2)
        self.assertEqual(mixed["word_count"], 6)
        self.assertGreater(mixed["reading_time_seconds"], 0)

    def test_chinese_draft_for_english_gets_language_warning_and_low_score(self):
        result = self.check_copy("新品上市，温和亲肤，清爽保湿，适合每日使用。", "en")
        self.assertTrue(result["warnings"])
        self.assertLessEqual(result["score"], 50)

    def test_long_sentence_gives_reading_feedback(self):
        result = self.check_copy("这款面霜" * 30 + "。", "cn")
        self.assertEqual(result["readability"]["long_sentence_count"], 1)
        self.assertTrue(result["readability"]["tips"])

    def test_apply_suggestion_rejects_stale_span(self):
        item = self.check_copy("包邮。立即入手。")["suggestions"][0]
        self.assertEqual(apply_suggestion("包邮。立即入手。", item), "免運費。立即入手。")
        with self.assertRaises(ValueError):
            apply_suggestion("免運費。立即入手。", item)

    def test_input_validation(self):
        for text, market, error in [(None, "hk", TypeError), ("draft", "tw", ValueError),
                                    ("x" * 20001, "en", ValueError)]:
            with self.subTest(market=market, error=error):
                with self.assertRaises(error):
                    self.check_copy(text, market)

    def test_scores_bounded_and_improve_after_adaptation(self):
        bad = self.check_copy("亲，包邮爆款快来种草。")
        good = self.check_copy("各位，皇牌產品免運費，誠意推介。立即入手。")
        self.assertGreater(good["score"], bad["score"])
        self.assertTrue(0 <= bad["score"] <= good["score"] <= 100)


if __name__ == "__main__":
    unittest.main()
