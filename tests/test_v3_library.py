"""Pagination, payload and warm-path performance on the complete V3 corpus."""

import json
import statistics
import tempfile
import unittest
from time import perf_counter
from unittest.mock import patch

from app import create_app
from core.ai_rewriter import _system_prompt
from core.rewrite_grounding import MAX_RAG_CONSTRAINTS, MAX_RAG_TERMS, retrieve_constraints
from core.schema import CATEGORIES, TERM_FIELDS
from data.init_seed_data import initialize_data

CASE_FIELDS = set(TERM_FIELDS) | {"learning_tip"}


class ExpandedLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(directory.cleanup)
        cls.total = initialize_data(directory.name)["term_count"]
        cls.application = create_app({
            "TESTING": True, "LIBRARY_DIR": directory.name,
            "RATELIMIT_ENABLED": False, "SECRET_KEY": "v3-integration-test-key",
        })
        cls.client = cls.application.test_client()
        cls.library = cls.application.extensions["library"]

    def test_bootstrap_returns_a_small_batch_of_complete_cases(self):
        response = self.client.get("/api/bootstrap")
        self.assertLess(len(response.data), 40_000)
        self.assertIn("no-store", response.headers.get("Cache-Control", ""))
        bootstrap = response.json["data"]
        self.assertEqual(bootstrap["total"], self.total)
        self.assertEqual(bootstrap["categories"], list(CATEGORIES))
        self.assertEqual(sum(bootstrap["category_counts"].values()), self.total)
        self.assertEqual(len({term["id"] for term in bootstrap["terms"]}), 6)
        self.assertFalse(bootstrap["has_more"])
        self.assertEqual(len({term["category"] for term in bootstrap["terms"]}), 6)
        self.assertTrue(all(set(term) == CASE_FIELDS for term in bootstrap["terms"]))
        for case in bootstrap["terms"]:
            detail = self.client.get(f"/api/terms/{case['id']}").json["data"]
            self.assertTrue(0 < len(case["learning_tip"]) <= 22)
            self.assertEqual(case["usage_tip"], detail["usage_tip"])

    def test_category_pages_are_deterministic_with_explicit_pagination(self):
        counts = self.library.get_search_engine().category_counts()
        for category in CATEGORIES:
            with self.subTest(category=category):
                identifiers = []
                while True:
                    page = self.client.get("/api/terms", query_string={
                        "category": category, "limit": 200, "offset": len(identifiers),
                    }).json["data"]
                    self.assertEqual(page["matched_total"], counts[category])
                    self.assertEqual(page["total"], self.total)
                    self.assertTrue(all(term["category"] == category for term in page["terms"]))
                    identifiers.extend(term["id"] for term in page["terms"])
                    if not page["has_more"]:
                        break
                    self.assertTrue(page["terms"])
                self.assertEqual(identifiers, sorted(set(identifiers)))
                self.assertEqual(len(identifiers), counts[category])
        detail = self.client.get(f"/api/terms/{self.total}").json["data"]
        self.assertEqual(detail["id"], self.total)
        self.assertTrue(detail["good_example_hk"])
        self.assertTrue(detail["usage_tip"])

    def test_ranked_search_defaults_to_twelve_and_keeps_explicit_pagination(self):
        query = {"q": "精华", "category": "美妆与个护"}
        search = self.client.get("/api/terms", query_string={**query, "mode": "feed"}).json["data"]
        legacy_search = self.client.get("/api/terms", query_string=query).json["data"]
        self.assertEqual(search, legacy_search)
        self.assertEqual((search["offset"], search["limit"], len(search["terms"])), (0, 12, 12))
        self.assertTrue(search["has_more"])
        later = self.client.get("/api/terms", query_string={
            **query, "mode": "feed", "offset": 12, "limit": 3,
        }).json["data"]
        reference, matched_total = self.library.get_search_engine().search_page(
            query["q"], query["category"], limit=15,
        )
        actual = search["terms"] + later["terms"]
        self.assertEqual([{key: term[key] for key in TERM_FIELDS} for term in actual],
                         [{key: term[key] for key in TERM_FIELDS} for term in reference])
        self.assertTrue(all(0 < len(term["learning_tip"]) <= 22 for term in actual))
        self.assertEqual(search["matched_total"], matched_total)
        self.assertEqual(later["matched_total"], matched_total)

    def test_feed_includes_curated_flagship_and_industry_cases(self):
        engine = self.library.get_search_engine()
        for category, names in (
            ("社媒与种草", {term["term_en"] for term in engine.search_page(category="社媒与种草", limit=20)[0]}),
            ("美妆与个护", {"Niacinamide", "Retinol", "Pro-Xylane", "Skin Barrier Care"}),
        ):
            with self.subTest(category=category):
                feed = engine.sample_feed(category)
                self.assertGreaterEqual(sum(term["term_en"] in names for term in feed), 2)

    def test_long_cross_industry_draft_keeps_model_grounding_bounded(self):
        engine = self.library.get_search_engine()
        terms, _ = engine.search_page(offset=1700, limit=200)
        terms_text = "。".join(term["term_cn"] for term in terms)
        draft = ((terms_text + "。内地包邮，早鸟福利。") * 30)[:20_000]
        matched, constraints = retrieve_constraints(draft, "hk", engine)
        self.assertEqual(len(matched), MAX_RAG_TERMS)
        self.assertLessEqual(len(constraints), MAX_RAG_CONSTRAINTS)
        prompt = _system_prompt("hk", "standard", matched, constraints)
        block = prompt.split("Mandatory Brand Glossary Constraints (JSON data): ", 1)[1].split("\n", 1)[0]
        self.assertLess(len(block.encode("utf-8")), 700)
        payload = json.loads(block)
        self.assertTrue(payload["terms"])
        self.assertTrue(all(len(term["usage_tip"]) <= 80 for term in payload["terms"]))

    def test_warm_search_feed_and_grounding_reuse_index_in_milliseconds(self):
        engine = self.library.get_search_engine()
        draft = "LUMA 联名香氛礼盒上线。预订享早鸟福利，香港包邮。新品亮相期間限定店。"
        timings = {"search": [], "feed": [], "grounding": []}
        with patch.object(self.library, "_connection", side_effect=AssertionError("warm database read")):
            for _ in range(30):
                start = perf_counter()
                page = self.client.get("/api/terms", query_string={"q": "早鸟", "limit": 60})
                timings["search"].append(1000 * (perf_counter() - start))
                self.assertEqual(page.status_code, 200)
                start = perf_counter()
                feed = self.client.get("/api/terms", query_string={"mode": "feed", "exclude": "1,2,3,4,5,6"})
                timings["feed"].append(1000 * (perf_counter() - start))
                self.assertTrue({row["id"] for row in feed.json["data"]["terms"]}.isdisjoint(range(1, 7)))
                start = perf_counter()
                matched, _ = retrieve_constraints(draft, "hk", self.library.get_search_engine())
                timings["grounding"].append(1000 * (perf_counter() - start))
                self.assertIn("Early-Bird Offer", {term["term_en"] for term in matched})
        self.assertIs(self.library.get_search_engine(), engine)
        for operation, elapsed in timings.items():
            with self.subTest(operation=operation):
                self.assertLess(statistics.median(elapsed), 5.0, elapsed)
                self.assertLess(statistics.quantiles(elapsed, n=20)[18], 10.0, elapsed)
