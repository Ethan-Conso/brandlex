"""BrandLex V3 indexing and bounded grounding regressions."""

from copy import deepcopy
import json
import unicodedata
import unittest
from unittest.mock import patch

from core.ai_rewriter import _system_prompt
from core.rewrite_grounding import apply_constraints, retrieve_constraints
from core.search_engine import SearchEngine, match_glossary_terms


def term(identifier, expression, *, hk=None, cn=None, aliases=(), tip="说明适用对象。"):
    return {
        "id": identifier, "term_en": expression, "term_hk": hk or f"{expression}香港",
        "term_cn": cn or f"{expression}内地", "aliases": list(aliases),
        "category": "电商与转化", "meaning": "条件与参与方式", "usage_tip": tip,
    }


def grounding_prompt(matched, constraints):
    prompt = _system_prompt("hk", "standard", matched, constraints)
    encoded = prompt.split("Mandatory Brand Glossary Constraints (JSON data): ", 1)[1].split("\n", 1)[0]
    return encoded, json.loads(encoded)


class IndexedSnapshotTests(unittest.TestCase):
    def test_page_preserves_search_rank_and_only_copies_requested_records(self):
        engine = SearchEngine([
            term(1, "Offer Details"), term(2, "Offer"), term(3, "Welcome Offer"),
            {**term(4, "Offer"), "category": "投放与增长"},
        ])
        with patch("core.search_engine.deepcopy", wraps=deepcopy) as copy:
            page, count = engine.search_page("offer", "电商与转化", offset=1, limit=1)
        self.assertEqual((page[0]["id"], count, copy.call_count), (1, 3, 1))
        self.assertEqual(engine.search_page("offer", offset=60, limit=60), ([], 4))
        self.assertEqual(len(engine), 4)
        self.assertEqual(engine.category_counts(), {"电商与转化": 3, "投放与增长": 1})
        page[0]["term_en"] = "Changed"
        self.assertEqual(engine.get_term(1)["term_en"], "Offer Details")

    def test_candidates_respect_boundaries_and_preserve_across_script_matches(self):
        engine = SearchEngine([
            term(1, "ROAS"), term(2, "Free Shipping", hk="免運費", cn="包邮"),
            term(3, "Best-Seller", hk="皇牌產品", cn="爆款", aliases=("熱賣",)),
            term(4, "A/B Test"), term(5, "博", hk="博", cn="博"),
        ])
        self.assertEqual([row["id"] for row in match_glossary_terms(
            "roast ROAS_；包郵。热卖，Ａ／Ｂ test，微博。", engine
        )], [2, 3, 4, 5])

    def test_reused_engine_does_not_rebuild_or_convert_all_aliases(self):
        engine = SearchEngine([term(1, "Free Shipping", hk="免運費", cn="包邮")])
        with patch("core.search_engine.SearchEngine.__init__", side_effect=AssertionError("rebuilt")):
            matched, constraints = retrieve_constraints("香港包郵。", "hk", engine)
        self.assertEqual([row["id"] for row in matched], [1])
        self.assertEqual([(rule["original"], rule["adapted"]) for rule in constraints],
                         [("包郵", "免運費")])

    def test_prefix_index_keeps_suffix_hits_and_recovers_after_misses(self):
        engine = SearchEngine([
            term(1, "Cold Brew", hk="冷萃咖啡", cn="冷萃咖啡"),
            term(2, "Coffee", hk="咖啡", cn="咖啡"),
            term(3, "Coffee Beans", hk="咖啡豆", cn="咖啡豆"),
        ])
        self.assertEqual([row["id"] for row in engine.draft_matches("試飲冷萃咖啡，選購咖啡豆。")], [1, 2, 3])
        self.assertEqual([row["id"] for row in engine.draft_matches("Coffee beaned. Coffee beans.")], [2, 3])


class GroundingBudgetTests(unittest.TestCase):
    def test_retrieval_ranks_specificity_then_frequency_then_id(self):
        rows = [term(8, "Promotions", aliases=("red",)), term(4, "Promotion", aliases=("red",)),
                term(3, "Regional Offers", aliases=("pop",)), term(1, "Longer Offer")]
        engine = SearchEngine(rows)
        matched, _ = retrieve_constraints("red red pop. Longer Offer", "hk", engine)
        self.assertEqual([row["id"] for row in matched], [1, 4, 8, 3])

    def test_nested_aliases_do_not_inflate_occurrence_frequency(self):
        engine = SearchEngine([term(1, "Long soak"), term(2, "Cold brew", aliases=("brew",))])
        matched, _ = retrieve_constraints("Long soak. Cold brew.", "hk", engine)
        self.assertEqual([row["id"] for row in matched], [1, 2])
        matched, _ = retrieve_constraints("Long soak. Cold brew. Brew.", "hk", engine)
        self.assertEqual([row["id"] for row in matched], [2, 1])

    def test_top_term_and_unique_rule_caps_on_dense_inputs(self):
        rows = [term(identifier, f"Offer name {identifier}",
                     aliases=(f"campaign offer {identifier}", f"member offer {identifier}"))
                for identifier in range(1, 41)]
        text = " · ".join(f"campaign offer {i} / member offer {i}" for i in range(1, 41))
        matched, constraints = retrieve_constraints(text, "hk", SearchEngine(rows))
        self.assertEqual(len(matched), 18)
        self.assertEqual(len(constraints), 24)
        self.assertEqual(len({row["original"].casefold() for row in constraints}), 24)
        long_copy = ("。".join((text,) * 20))[:20_000]
        long_matches, long_constraints = retrieve_constraints(long_copy, "hk", SearchEngine(rows))
        encoded, payload = grounding_prompt(long_matches, long_constraints)
        self.assertLessEqual(len(encoded.encode()), 700)
        self.assertGreater(len(payload["terms"]), 0)
        self.assertGreater(len(payload["matched_rules"]), 0)

    def test_budget_bounds_serialized_json_even_with_long_or_escaped_fields(self):
        tip = "港" * 80 + "unique-tail"
        matched = [term(1, "Gift", hk="禮品", cn="礼品", tip=tip),
                   term(2, "鉅" * 6000, tip="*" * 6000),
                   *[term(i, "Gift \\" + '"\\' * 100) for i in range(3, 20)]]
        constraints = [
            {"original": "包邮", "adapted": "免運費", "reason": "香港用語", "term_id": None},
            {"original": "。" * 6000, "adapted": "！" * 6000, "reason": "str" * 5000,
             "term_id": None},
        ]
        encoded, data = grounding_prompt(matched, constraints)
        self.assertLessEqual(len(encoded.encode()), 700)
        self.assertEqual(data["terms"][0]["term_id"], 1)
        self.assertEqual(data["terms"][0]["usage_tip"], tip[:80])
        self.assertEqual(data["matched_rules"], constraints[:1])
        self.assertNotIn("unique-tail", encoded)
        self.assertNotIn("鉅", encoded)

    def test_budget_accounts_for_unicode_expansion_and_omitted_term_ids(self):
        rows = [term(1, "Gift", hk="禮品", cn="礼品", tip="㍿" * 80),
                term(2, "Gift Wrap", hk="禮品包裝", cn="礼品包装")]
        rules = (
            {"original": "礼品", "adapted": "禮品", "reason": "香港用語", "term_id": 1},
            {"original": "礼品包装", "adapted": "禮品包裝", "reason": "香港用語", "term_id": 2},
        )
        encoded, payload = grounding_prompt(rows, rules)
        self.assertLessEqual(len(unicodedata.normalize("NFKD", encoded).encode()), 700)
        self.assertEqual([entry["term_id"] for entry in payload["terms"]], [2])
        self.assertEqual(payload["matched_rules"], [{**rules[0], "term_id": None}, rules[1]])

    def test_url_contents_do_not_affect_term_selection_or_rank(self):
        rows = [term(1, "Free Shipping", hk="免運費", cn="包邮"),
                term(2, "Cashback", hk="現金回贈", cn="消费返现")]
        matched, constraints = retrieve_constraints(
            "詳情 https://example.com/Cashback/消费返现 ，香港包邮。", "hk", SearchEngine(rows)
        )
        self.assertEqual([row["id"] for row in matched], [1])
        self.assertEqual([rule["original"] for rule in constraints], ["包邮"])

    def test_protects_actual_canonical_spans_without_merging_overlaps(self):
        constraints = (
            {"original": "乙丙丁", "adapted": "轉化"},
            {"original": "其他甲", "adapted": "甲乙丙"},
            {"original": "其他乙", "adapted": "丙丁戊"},
            {"original": "乙", "adapted": "錯誤"},
        )
        self.assertEqual(apply_constraints("甲乙丙丁戊", constraints, "hk"), "甲轉化戊")
        self.assertEqual(apply_constraints("甲乙丙", constraints, "hk"), "甲乙丙")


if __name__ == "__main__":
    unittest.main()
