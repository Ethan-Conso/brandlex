from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from core.copy_checker import _counts
from scripts import cache_github_pages_rewrites as cache


class PagesCacheTests(unittest.TestCase):
    def test_home_hk_social_respects_the_inclusive_booking_window(self):
        snapshot = cache.read_data("pages_rewrites.json")
        home = next(draft for draft in snapshot["drafts"] if draft["id"] == "home")
        result = home["rewrites"]["hk:social"]
        for field in ("primary_copy", "alt_copy"):
            self.assertIn("呢三日", result[field])
            self.assertNotIn("呢兩日", result[field])

    def test_cache_generation_retries_a_factual_mismatch(self):
        draft = cache.read_data("pages_rewrites.json")["drafts"][0]
        result = draft["rewrites"]["hk:social"]
        live = {**result, "matched_glossary_terms": [{"id": term_id} for term_id in result["matched_term_ids"]]}
        fallback = {"engine": "fallback", "error_code": "factual_mismatch"}
        with patch.object(cache, "rewrite_copy", side_effect=[fallback, live]) as rewrite, patch.object(cache.time, "sleep"):
            self.assertEqual(cache.cache_case((draft, "hk", "social"), ()), result)
        self.assertEqual(rewrite.call_count, 2)

    def test_cache_write_preserves_existing_snapshot_on_factual_mismatch(self):
        snapshot = cache.read_data("pages_rewrites.json")
        result = snapshot["drafts"][0]["rewrites"]["hk:social"]
        result["primary_copy"] = result["primary_copy"].replace("HK$280", "HK$820")
        with TemporaryDirectory() as directory, patch.object(cache, "DATA", Path(directory)):
            target = Path(directory) / "pages_rewrites.json"
            target.write_text("existing snapshot", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, r"home hk:social.*factual_mismatch"):
                cache.write_cache(snapshot, "temporary-test-key")
            self.assertEqual(target.read_text(encoding="utf-8"), "existing snapshot")

    def test_cache_contains_distinct_verified_styles_for_all_demo_drafts(self):
        snapshot = cache.read_data("pages_rewrites.json")
        cache.validate_fidelity(snapshot)
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
                        self.assertEqual(result["counts"], _counts(result["primary_copy"]))
                        self.assertEqual(result["source_counts"], _counts(draft["text"]))
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
