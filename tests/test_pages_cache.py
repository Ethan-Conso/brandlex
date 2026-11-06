import json
from itertools import product
import unittest

from scripts import cache_github_pages_rewrites as cache


class PagesCacheTests(unittest.TestCase):
    def test_cache_contains_distinct_verified_styles_for_all_demo_drafts(self):
        snapshot = json.loads((cache.DATA / "pages_rewrites.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["model"], "deepseek-flash")
        self.assertEqual(
            [{"id": draft["id"], "text": draft["text"]} for draft in snapshot["drafts"]],
            cache.load_drafts(),
        )
        for draft in snapshot["drafts"]:
            self.assertEqual(
                set(draft["rewrites"]),
                {f"{market}:{tone}" for market, tone in product(cache.MARKETS, cache.TONES)},
            )
            for market in cache.MARKETS:
                primary = set()
                for tone in cache.TONES:
                    with self.subTest(draft=draft["id"], market=market, tone=tone):
                        result = draft["rewrites"][f"{market}:{tone}"]
                        self.assertEqual(result["engine"], "deepseek")
                        self.assertNotEqual(result["primary_copy"], result["alt_copy"])
                        self.assertEqual(len(set(result["cta_options"])), 2)
                        self.assertNotIn(result["primary_copy"], primary)
                        primary.add(result["primary_copy"])
                        self.assertIn(len(result["adaptations"]), range(3, 7))
                        for change in result["adaptations"]:
                            self.assertIn(change["original"], draft["text"])
                            self.assertTrue(
                                any(change["adapted"] in result[field] for field in ("primary_copy", "alt_copy"))
                            )
                            self.assertLessEqual(len(change["reason"]), 15)
