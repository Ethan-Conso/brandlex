"""Editorial seed transformations and compact cross-market takeaways."""

from copy import deepcopy
from itertools import chain
import unittest

from core.chinese_converter import convert_script
from core.schema import validate_term
from data.lexicon_domains import learning_tip, polish_generated_terms
from data.seed_beauty_fashion_tech import build_beauty_fashion_tech_terms
from data.seed_core_definitions import ADDITIONAL_CORE_TERMS
from data.seed_finance_compliance import build_finance_compliance_terms
from data.seed_food_travel import build_food_travel_terms
from data.seed_marketing import build_marketing_terms
from data.seed_terms import build_seed_terms


def generated_source():
    additions = chain(
        build_marketing_terms(), build_beauty_fashion_tech_terms(),
        build_food_travel_terms(), build_finance_compliance_terms(),
        ADDITIONAL_CORE_TERMS,
    )
    return [{**term, "id": index} for index, term in enumerate(additions, 101)]


class LearningCopyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = generated_source()
        cls.flagships = build_seed_terms()
        cls.polished = polish_generated_terms(cls.raw, cls.flagships)
        cls.records = {term["term_en"]: term for term in cls.polished}

    def test_shortens_headwords_with_previous_expression_as_alias(self):
        title = self.records["Blood Oxygen Smart Ring"]
        self.assertIn("Blood-Oxygen-Tracking Smart Ring", title["aliases"])
        self.assertEqual(title["term_hk"], "血氧追蹤智能戒指")
        self.assertIn("Product Detail Page Frequently Asked Questions",
                      self.records["Product Page FAQ"]["aliases"])

    def test_leaves_long_title_when_shortened_title_is_already_reserved(self):
        raw = next(term for term in self.raw if term["term_en"] == "Blood-Oxygen-Tracking Smart Ring")
        before = deepcopy(raw)
        result, = polish_generated_terms([raw], [{"term_en": "Blood Oxygen Smart Ring"}])
        self.assertEqual(result["term_en"], before["term_en"])
        self.assertEqual(raw, before)

    def test_examples_keep_their_point_in_plain_language(self):
        ring = self.records["Blood Oxygen Smart Ring"]
        self.assertEqual(ring["good_example_en"],
                         "Use the sizing kit before ordering, then pair your blood oxygen smart ring with the app.")
        self.assertEqual(ring["good_example_hk"], "先用量度套裝揀啱尺寸，血氧追蹤智能戒指到手再配對應用程式。")
        self.assertEqual(ring["good_example_cn"], "先用量圈工具选好尺码，血氧监测智能戒指到手后再连接应用。")
        tasting = self.records["Tasting Menu"]
        self.assertIn("sweet peas", tasting["good_example_en"])
        dish = self.records["Wok-Fried Beef Ho Fun"]
        self.assertEqual(dish["good_example_en"], "Try our wok-fried beef ho fun this week.")
        self.assertEqual(dish["good_example_hk"], "本週餐單有乾炒牛河。")

    def test_takeaways_name_a_useful_difference_and_treat_script_only_honestly(self):
        early_bird = next(term for term in self.flagships if term["term_en"] == "Early-Bird Offer")
        self.assertEqual(learning_tip(early_bird), "港用「禮遇」，内地用「福利」。")
        tech = self.records["Blood Oxygen Smart Ring"]
        self.assertEqual(learning_tip(tech), "港用「追蹤」，内地用「监测」。")
        self.assertEqual(learning_tip({"term_hk": "示意圖", "term_cn": "示意图"}), "港繁内简，用词相同。")
        self.assertEqual(learning_tip({"term_hk": "網店自取", "term_cn": "网店自提"}),
                         "港用「自取」，内地用「自提」。")
        excluded = self.records["Birthday Excluded Items"]
        self.assertIn("「不適用貨品」", learning_tip(excluded))
        self.assertIn("「不参加活动商品」", learning_tip(excluded))

    def test_unknown_long_terms_do_not_lose_a_shared_negative_prefix(self):
        term = {"term_hk": "型格耳機系列未開通音效", "term_cn": "型格耳机系列未启用声音功能"}
        tip = learning_tip(term)
        self.assertNotIn("「開通音效」", tip)
        self.assertNotIn("「启用声音功能」", tip)

    def test_entire_corpus_is_valid_ordered_distinct_and_has_compact_takeaways(self):
        full = self.flagships + self.polished
        self.assertEqual([term["id"] for term in full], list(range(1, 3208)))
        self.assertGreater(sum(raw["term_en"] != new["term_en"] for raw, new in zip(self.raw, self.polished)), 200)
        for field in ("term_en", "term_hk", "term_cn"):
            self.assertEqual(len({term[field].casefold() for term in full}), len(full))
        for term in full:
            self.assertEqual(validate_term(term, require_id=True), term)
            self.assertEqual(convert_script(term["good_example_cn"], "cn"), term["good_example_cn"])
            tip = learning_tip(term)
            self.assertTrue(0 < len(tip) <= 22, (term["id"], tip))
            self.assertNotRegex(tip, r"[\r\n…]")
