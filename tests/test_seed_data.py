"""The default library must be complete, useful and safe to restore."""

import collections
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from core.schema import CATEGORIES as ALL_CATEGORIES, validate_term
from data.seed_terms import build_sample_drafts, build_seed_terms


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = (
    "社媒与种草",
    "电商与转化",
    "投放与增长",
    "公关与线下",
    "文案与修辞",
)
FIELDS = {
    "id", "term_en", "term_hk", "term_cn", "aliases", "category",
    "platforms", "meaning", "bad_example", "good_example_en",
    "good_example_hk", "good_example_cn", "usage_tip",
}


class SeedContentTests(unittest.TestCase):
    def test_seed_english_copy_has_no_accidental_repetitions_or_package_prepositions(self):
        from data.seed_library import build_default_library

        terms = build_default_library()
        errors = re.compile(r"\b([A-Za-z]+)\s+\1\b|\bincluded at the\b", re.IGNORECASE)
        defects = [
            (term["id"], field, match.group())
            for term in terms
            for field, value in term.items()
            for text in (value if isinstance(value, list) else [value])
            if isinstance(text, str) and (match := errors.search(text))
        ]
        self.assertEqual(defects, [])
        by_id = {term["id"]: term for term in terms}
        self.assertEqual(by_id[2936]["term_en"], "Joint Account Closure")
        self.assertEqual(by_id[2669]["good_example_en"],
                         "See what's included in the residential meeting package and how to get there.")

    def test_all_published_terms_have_bilingual_definitions(self):
        from data.seed_library import build_default_library

        terms = build_default_library()
        self.assertEqual(terms, json.loads((ROOT / "data/glossary_seed.json").read_text(encoding="utf-8")))
        required = {
            "CTR", "ROAS", "KOL", "KOC", "UGC", "CTA", "EDM", "GMV", "SEO", "SEM",
            "Dewy Lip Tint", "Absolute Advertising Claim", "Joint Account Closure",
            "Residential Meeting Package", "Pop-up Store",
        }
        self.assertEqual(len(terms), 3208)
        expressions = {value for term in terms for value in (term["term_en"], *term["aliases"])}
        self.assertEqual(required - expressions, set())
        for term in terms:
            with self.subTest(term=term["term_en"]):
                chinese, _, english = term["meaning"].partition(" EN: ")
                self.assertRegex(chinese, r"[\u4e00-\u9fff].*。$")
                self.assertRegex(english, r"^[A-Z].*\.$")
                self.assertNotIn(" EN: ", english)

    def test_growth_headwords_distinguish_ppc_model_from_cpc_cost(self):
        from core.search_engine import SearchEngine
        from data.seed_library import build_default_library

        engine = SearchEngine(build_default_library())
        ppc = engine.search("PPC")[0]
        self.assertEqual(ppc["id"], 3208)
        self.assertEqual(ppc["term_en"], "Pay-Per-Click (PPC)")
        self.assertEqual(ppc["term_hk"], "按點擊付費廣告")
        self.assertEqual(ppc["term_cn"], "按点击付费广告")
        self.assertEqual(ppc["category"], "投放与增长")
        self.assertEqual(ppc["aliases"], ["PPC", "Pay-Per-Click", "点击付费模式"])
        self.assertEqual(engine.search("Pay-Per-Click")[0]["id"], 3208)
        cpc = engine.search("CPC")[0]
        self.assertEqual(cpc["id"], 51)
        self.assertNotIn("pay per click", cpc["aliases"])
        self.assertIn("advertising model", ppc["meaning"])
        self.assertIn("average", cpc["meaning"])
        for query, identifier in (("Conversion Rate (CVR)", 54), ("Landing Page", 55)):
            with self.subTest(query=query):
                term = engine.search(query)[0]
                self.assertEqual(term["id"], identifier)
                self.assertIn(" EN: ", term["meaning"])

    def test_exactly_one_hundred_terms_twenty_per_category(self):
        terms = build_seed_terms()
        self.assertEqual(len(terms), 100)
        self.assertEqual({term["id"] for term in terms}, set(range(1, 101)))
        self.assertEqual(collections.Counter(t["category"] for t in terms),
                         {category: 20 for category in CATEGORIES})
        for key in ("term_en", "term_hk", "term_cn"):
            self.assertEqual(len({t[key].casefold() for t in terms}), 100)

    def test_expanded_defaults_preserve_flagships_and_fill_every_category(self):
        from data.seed_library import build_default_library

        terms = build_default_library()
        self.assertEqual(terms, build_default_library())
        self.assertGreaterEqual(len(terms), 3200)
        self.assertEqual(terms[:100], build_seed_terms())
        self.assertEqual([term["id"] for term in terms], list(range(1, len(terms) + 1)))
        counts = collections.Counter(term["category"] for term in terms)
        self.assertEqual(set(counts), set(ALL_CATEGORIES))
        self.assertTrue(all(260 <= count <= 280 for count in counts.values()), counts)
        self.assertEqual(len({term["term_en"].casefold() for term in terms}), len(terms))
        for term in terms[100:]:
            with self.subTest(term=term["term_en"]):
                self.assertEqual(validate_term(term, require_id=True), term)
                for key in ("term_en", "term_hk", "term_cn"):
                    self.assertNotRegex(term[key], r"\d")
                self.assertNotEqual(term["good_example_hk"], term["good_example_cn"])
        content = json.dumps(terms, ensure_ascii=False)
        self.assertNotRegex(content, r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]")

    def test_every_record_has_complete_practical_content(self):
        for term in build_seed_terms():
            with self.subTest(term=term["term_en"]):
                self.assertEqual(set(term), FIELDS)
                self.assertIs(type(term["id"]), int)
                for field in FIELDS - {"id", "aliases", "platforms"}:
                    self.assertIsInstance(term[field], str)
                    self.assertTrue(term[field].strip())
                for field in ("aliases", "platforms"):
                    self.assertIsInstance(term[field], list)
                    self.assertTrue(term[field])
                    self.assertTrue(all(isinstance(v, str) and v.strip()
                                        for v in term[field]))
                self.assertGreaterEqual(len(term["meaning"]), 15)
                self.assertGreaterEqual(len(term["usage_tip"]), 15)
                self.assertNotEqual(term["good_example_hk"], term["good_example_cn"])

    def test_examples_are_bespoke_and_library_has_no_legacy_clutter(self):
        terms = build_seed_terms()
        for field in ("meaning", "bad_example", "good_example_en",
                      "good_example_hk", "good_example_cn", "usage_tip"):
            self.assertEqual(len({t[field] for t in terms}), 100, field)
        content = json.dumps(terms + build_sample_drafts(), ensure_ascii=False).casefold()
        for forbidden in ("tra6202", "dr. siu", "member 1", "member 2", "section 3",
                          "cpu", "gpu", "tacotron", "waveglow", "crud", "absa",
                          "tokenization", "stop words", "11-step pipeline", "4d index"):
            self.assertNotIn(forbidden, content)

    def test_all_default_content_is_emoji_free(self):
        content = json.dumps(build_seed_terms() + build_sample_drafts(), ensure_ascii=False)
        self.assertNotRegex(content, r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]")

    def test_regional_marketing_anchor_terms(self):
        by_en = {term["term_en"]: term for term in build_seed_terms()}
        expected = {
            "Product Seeding": ("好物推介", "种草"),
            "Free Shipping": ("免運費", "包邮"),
            "Early-Bird Offer": ("早鳥禮遇", "早鸟福利"),
            "Pop-up Store": ("期間限定店", "快闪店"),
            "Crossover Collaboration": ("跨界聯乘", "跨界联名"),
        }
        for key, (hk, cn) in expected.items():
            self.assertIn(hk, by_en[key]["term_hk"])
            self.assertIn(cn, by_en[key]["term_cn"])

    def test_builders_return_independent_copies(self):
        first = build_seed_terms()
        first[0]["aliases"].append("test mutation")
        first[0]["term_hk"] = "changed"
        self.assertNotEqual(first, build_seed_terms())
        self.assertNotIn("test mutation", build_seed_terms()[0]["aliases"])
        drafts = build_sample_drafts()
        drafts[0]["text"] = "changed"
        self.assertNotEqual(drafts, build_sample_drafts())

    def test_four_realistic_drafts(self):
        drafts = build_sample_drafts()
        self.assertEqual(len(drafts), 4)
        self.assertEqual(len({draft["id"] for draft in drafts}), 4)
        self.assertEqual({draft["target_market"] for draft in drafts}, {"hk", "cn", "en"})
        for draft in drafts:
            self.assertTrue({"id", "title", "text", "target_market"} <= set(draft))
            self.assertGreaterEqual(len(draft["text"]), 60)


class SeedScriptTests(unittest.TestCase):
    def test_command_runs_from_any_directory_and_restores_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "brandlex-data"
            command = [sys.executable, str(ROOT / "data/init_seed_data.py"),
                       "--data-dir", str(destination)]
            completed = subprocess.run(command, cwd=directory, capture_output=True,
                                       text=True, check=True)
            expected = {"glossary_seed.json", "glossary.json", "sample_drafts.json", "digilex.db"}
            self.assertTrue(expected <= {p.name for p in destination.iterdir()})
            terms = json.loads((destination / "glossary_seed.json").read_text(encoding="utf-8"))
            self.assertIn(f"{len(terms)} default terms", completed.stdout)
            self.assertGreaterEqual(len(terms), 3200)
            self.assertEqual(terms[:100], build_seed_terms())
            with closing(sqlite3.connect(destination / "digilex.db")) as connection, connection:
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM terms").fetchone()[0], len(terms))
                connection.execute("DELETE FROM terms WHERE id = 1")
            subprocess.run(command, cwd=directory, capture_output=True, check=True)
            with closing(sqlite3.connect(destination / "digilex.db")) as connection, connection:
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM terms").fetchone()[0], len(terms))


if __name__ == "__main__":
    unittest.main()
