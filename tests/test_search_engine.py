"""Search behavior shared by the glossary and Copy Check tools."""

import unittest

from core.search_engine import SearchEngine, match_glossary_terms, search_terms


def records():
    return [
        {
            "id": 1, "term_en": "Product Seeding", "term_hk": "好物推介 / 誠意推介",
            "term_cn": "种草", "aliases": ["seeding", "安利"], "category": "social",
            "meaning": "邀请真实用户分享试用体验，帮助消费者认识新产品。", "platforms": ["IG"],
        },
        {
            "id": 2, "term_en": "Early-Bird Offer", "term_hk": "早鳥禮遇",
            "term_cn": "早鸟福利", "aliases": ["early bird"], "category": "commerce",
            "meaning": "提前预订可享优惠。", "platforms": ["Shopify"],
        },
        {
            "id": 3, "term_en": "Return on Ad Spend", "term_hk": "廣告投資回報",
            "term_cn": "广告支出回报", "aliases": ["ROAS"], "category": "growth",
            "meaning": "每花一元广告费带来多少销售额。", "platforms": ["Meta Ads"],
        },
        {
            "id": 4, "term_en": "A/B Testing", "term_hk": "A/B 測試",
            "term_cn": "A/B 测试", "aliases": ["split testing"], "category": "growth",
            "meaning": "比较两个版本的表现。", "platforms": ["IG"],
        },
    ]


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.terms = records()

    def ids(self, query="", category=None):
        return [term["id"] for term in search_terms(self.terms, query, category)]

    def test_all_fields_and_case_insensitive_aliases(self):
        for query, expected in [("seeding", 1), ("好物推介", 1), ("种草", 1),
                                ("安利", 1), ("roas", 3), ("广告费", 3)]:
            with self.subTest(query=query):
                self.assertEqual(self.ids(query), [expected])

    def test_multiword_and_unicode_punctuation(self):
        self.assertEqual(self.ids("ＥＡＲＬＹ—ＢＩＲＤ"), [2])
        self.assertEqual(self.ids("early bird offer"), [2])
        self.assertEqual(self.ids("product 体验"), [1])
        self.assertEqual(self.ids("a/b testing"), [4])

    def test_short_ascii_queries_match_whole_words_in_each_field(self):
        engine = SearchEngine([
            {"id": 1, "term_en": "ROAS"},
            {"id": 2, "term_en": "ROAS Trend"},
            {"id": 3, "term_en": "Track ROAS Today"},
            {"id": 4, "meaning": "跟踪广告表现。 EN: Use ROAS to measure return."},
            {"id": 5, "good_example_hk": "每週查看ROAS。"},
            {"id": 6, "term_en": "Roast Date"},
            {"id": 7, "meaning": "A slow-roasted main course."},
            {"id": 8, "good_example_en": "With a side of roast potatoes."},
            {"id": 9, "term_en": "Macroas Dashboard", "aliases": ["ROAS2"]},
        ])
        for query in ("ROAS", "ＲＯＡＳ"):
            with self.subTest(query=query):
                self.assertEqual([row["id"] for row in engine.search(query)], [1, 2, 3, 4, 5])
        self.assertEqual([row["id"] for row in engine.search("roast")], [6, 8])

    def test_short_ascii_tokens_cannot_match_inside_a_phrase(self):
        engine = SearchEngine([
            {"id": 1, "term_en": "ROAS Date"},
            {"id": 2, "term_en": "Roast Date"},
            {"id": 3, "term_en": "Track Macroas Date"},
            {"id": 4, "term_en": "ROAS Dateline"},
            {"id": 5, "term_en": "ROAS", "meaning": "Results by date."},
            {"id": 6, "term_en": "ROAS", "good_example_en": "Pick a date."},
            {"id": 7, "term_en": "ROAS", "good_example_en": "Pick a dateline."},
        ])
        self.assertEqual([row["id"] for row in engine.search("roas date")], [1, 5, 6])

    def test_category_is_exact_and_composes_with_query(self):
        self.assertEqual(self.ids(category="growth"), [3, 4])
        self.assertEqual(self.ids("ROAS", "growth"), [3])
        self.assertEqual(self.ids("ROAS", "commerce"), [])
        self.assertEqual(self.ids(category="grow"), [])

    def test_empty_and_missing_query(self):
        self.assertEqual(self.ids("   "), [1, 2, 3, 4])
        self.assertEqual(search_terms([], "种草"), [])
        self.assertEqual(self.ids("unknown"), [])
        self.assertEqual(self.ids(" — -- "), [])

    def test_rank_prefers_exact_then_prefix_then_substring_then_meaning(self):
        terms = [
            {"id": 4, "term_en": "Brand", "meaning": "seeding"},
            {"id": 3, "term_en": "Product Seeding"},
            {"id": 2, "term_en": "Seeding campaign"},
            {"id": 1, "term_en": "Seeding"},
        ]
        self.assertEqual([row["id"] for row in search_terms(terms, "seeding")], [1, 2, 3, 4])

    def test_case_context_is_searchable_below_expressions_and_meanings(self):
        engine = SearchEngine([
            {"id": 3, "category": "文旅与酒店", "bad_example": "花園景觀套房一律面海",
             "good_example_en": "Ask about the balcony.",
             "good_example_hk": "可同前台預約行李寄存。",
             "good_example_cn": "今晚可领取欢迎饮品。"},
            {"id": 2, "meaning": "等待行李寄存"},
            {"id": 1, "term_cn": "行李寄存"},
        ])
        self.assertEqual([row["id"] for row in engine.search("行李寄存")], [1, 2, 3])
        for phrase in ("文旅与酒店", "一律面海", "balcony", "欢迎饮品", "文旅与酒店 balcony"):
            with self.subTest(phrase=phrase):
                self.assertEqual([row["id"] for row in engine.search(phrase)], [3])
                self.assertEqual(engine.draft_matches(phrase), [])

    def test_index_and_results_are_immutable_snapshots(self):
        engine = SearchEngine(self.terms)
        self.terms[0]["aliases"].append("mutation")
        self.assertEqual(engine.search("mutation"), [])
        result = engine.search("种草")
        result[0]["aliases"].append("leak")
        result[0]["term_hk"] = "bad"
        self.assertEqual(engine.search("leak"), [])
        self.assertEqual(engine.search("种草")[0]["term_hk"], "好物推介 / 誠意推介")

    def test_feed_prefers_new_cases_and_refills_when_the_pool_is_small(self):
        engine = SearchEngine(self.terms)
        fresh = engine.sample_feed("growth", limit=1, exclude_ids=(3,))
        self.assertEqual([row["id"] for row in fresh], [4])
        fresh[0]["aliases"].append("private mutation")
        refilled = engine.sample_feed("growth", limit=6, exclude_ids=(3,))
        self.assertEqual({row["id"] for row in refilled}, {3, 4})
        self.assertEqual(len(refilled), 2)
        self.assertEqual(engine.get_term(4)["aliases"], ["split testing"])
        self.assertEqual(engine.sample_feed("missing"), [])
        self.assertEqual(engine.sample_feed(limit=0), [])

    def test_default_feed_covers_six_categories_before_repeating_one(self):
        terms = [{"id": index, "term_en": "Offer", "category": "commerce"} for index in range(1, 15)]
        terms += [{"id": 100 + index, "term_en": "Editorial", "category": str(index)} for index in range(7)]
        engine = SearchEngine(terms)
        batch = engine.sample_feed()
        self.assertEqual(len(batch), 6)
        self.assertEqual(len({row["category"] for row in batch}), 6)
        following = engine.sample_feed(limit=10, exclude_ids=(row["id"] for row in batch))
        self.assertTrue({row["id"] for row in following}.isdisjoint(row["id"] for row in batch))
        available = {row["category"] for row in terms if row not in batch}
        self.assertEqual({row["category"] for row in following}, available)

    def test_feed_prioritizes_freshness_then_category_coverage_when_sparse(self):
        terms = [{"id": index, "term_en": "Offer", "category": "commerce"} for index in range(1, 8)]
        terms += [
            {"id": 8, "term_en": "Hashtag", "category": "social"},
            {"id": 9, "term_en": "KPI", "category": "growth"},
        ]
        engine = SearchEngine(terms)
        batch = engine.sample_feed(limit=2, exclude_ids=range(3, 10))
        self.assertEqual({row["id"] for row in batch}, {1, 2})
        batch = engine.sample_feed(limit=4, exclude_ids=range(3, 10))
        self.assertEqual({row["id"] for row in batch}, {1, 2, 8, 9})

    def test_feed_prefers_concise_flagships_and_discovery_cases(self):
        terms = [
            {"id": index, "term_en": "Long Multi-Feature Noise-Cancelling Flagship Offer", "category": "test"}
            for index in range(1, 7)
        ] + [
            {"id": index, "term_en": "Trade-In Credit" if index <= 103 else "Cash Rebate", "category": "test"}
            for index in range(101, 109)
        ]
        engine = SearchEngine(terms)
        feed = engine.sample_feed("test")
        self.assertEqual(len(feed), 6)
        self.assertTrue(all(row["id"] > 100 for row in feed))
        self.assertEqual(sum(row["id"] <= 103 for row in feed), 3)
        self.assertEqual(len(engine.search("noise-cancelling")), 6)

    def test_rejects_invalid_inputs(self):
        for query in [None, 3, ["种草"]]:
            with self.subTest(query=query), self.assertRaises(TypeError):
                search_terms(self.terms, query)
        with self.assertRaises(TypeError):
            search_terms(self.terms, category=3)
        with self.assertRaises(TypeError):
            SearchEngine("not records")


class GlossaryMatchTests(unittest.TestCase):
    def setUp(self):
        self.terms = records() + [
            {"id": 5, "term_en": "IG", "aliases": [], "meaning": "摄影"},
            {"id": 6, "term_en": "CTA", "aliases": ["call to action"]},
        ]

    def ids(self, text):
        return [row["id"] for row in match_glossary_terms(text, self.terms)]

    def test_matches_terms_and_aliases_but_not_meaning_or_platform(self):
        self.assertEqual(self.ids("种草文案中加入 ROAS 和誠意推介。"), [1, 3])
        self.assertEqual(self.ids("摄影体验好，提前预订。"), [])

    def test_latin_word_boundaries_prevent_acronym_substrings(self):
        self.assertEqual(self.ids("A big roast has no CTAish IGloo."), [])
        self.assertEqual(self.ids("IG / ROAS / cta!"), [3, 5, 6])
        self.assertEqual(self.ids("_ROAS ROAS_ 1ROAS ROAS2"), [])

    def test_matches_normalized_phrases_and_deduplicates(self):
        self.assertEqual(self.ids("EARLY—BIRD offer: early bird offer"), [2])
        self.assertEqual(self.ids("好物推介，种草，seeding，再来种草。"), [1])
        self.assertEqual(self.ids("用 A/B Testing 比较两个版本"), [4])
        self.assertEqual(self.ids("B Testing"), [])

    def test_empty_copy_and_no_input_mutation(self):
        self.assertEqual(self.ids(""), [])
        self.assertEqual(match_glossary_terms("ROAS", []), [])
        result = match_glossary_terms("ROAS", self.terms)
        result[0]["aliases"].append("changed")
        self.assertNotIn("changed", self.terms[2]["aliases"])

    def test_slash_separated_chinese_expressions(self):
        terms = [{"id": 1, "term_cn": "爆款/热卖单品", "aliases": []}]
        self.assertEqual(len(match_glossary_terms("我们的热卖单品", terms)), 1)

    def test_rejects_nontext_copy(self):
        with self.assertRaises(TypeError):
            match_glossary_terms(None, self.terms)


if __name__ == "__main__":
    unittest.main()
