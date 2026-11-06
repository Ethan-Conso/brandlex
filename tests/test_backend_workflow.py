"""End-to-end backend workflows, isolated from the bundled working library."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

from core.copy_checker import analyze_copy, apply_suggestion
from core.db_manager import DBManager, TBX_NAMESPACE
from data.init_seed_data import initialize_data
from data.seed_terms import build_sample_drafts, build_seed_terms


class BackendWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        initialize_data(self.root)
        self.options = dict(db_path=self.root / "digilex.db", json_path=self.root / "glossary.json", seed_path=self.root / "glossary_seed.json")
        self.manager = DBManager(**self.options)

    def tearDown(self):
        self.temporary.cleanup()

    def test_team_library_lifecycle_and_live_copy_references(self):
        total = len(self.manager.get_all_terms())
        self.assertGreaterEqual(total, 3200)
        self.assertEqual(self.manager.search_terms("ROAS")[0]["term_en"], "ROAS")
        category = "电商与转化"
        self.assertGreaterEqual(len(self.manager.search_terms(category=category)), 260)
        original_seed = self.options["seed_path"].read_bytes()
        template = build_seed_terms()[0]
        payload = {key: value for key, value in template.items() if key != "id"}
        added = self.manager.add_term({**payload, "term_en": "Signature Ritual", "term_hk": "品牌日常儀式", "term_cn": "品牌日常仪式", "aliases": ["morning ritual"]})
        self.manager.update_term(added["id"], {"aliases": ["daily ritual"]})
        with patch("core.db_manager.DATA_DIR", self.root):
            report = analyze_copy("Discover our daily ritual. Shop now.", "en")
            self.assertIn(added["id"], [term["id"] for term in report["matched_glossary_terms"]])
            self.manager.delete_term(added["id"])
            report = analyze_copy("Discover our daily ritual. Shop now.", "en")
            self.assertNotIn(added["id"], [term["id"] for term in report["matched_glossary_terms"]])
        self.manager.delete_term(1)
        self.assertEqual(len(self.manager.reset_to_defaults()), total)
        self.assertEqual(self.options["seed_path"].read_bytes(), original_seed)
        self.assertEqual(json.loads(self.manager.export_json()), self.manager.get_all_terms())
        exported = ET.fromstring(self.manager.export_tbx())
        self.assertEqual(len(exported.findall(f".//{{{TBX_NAMESPACE}}}conceptEntry")), total)
        self.assertEqual(json.loads(self.options["json_path"].read_text(encoding="utf-8")), DBManager(**self.options).get_all_terms())

    def test_sample_drafts_replacements_counts_and_cta_insertion(self):
        glossary = self.manager.get_all_terms()
        for draft in build_sample_drafts():
            with self.subTest(draft=draft["title"]):
                text, market = draft["text"], draft["target_market"]
                report = analyze_copy(text, market, glossary)
                self.assertTrue(0 <= report["readiness_score"] <= 100)
                self.assertGreater(report["word_count"], 0)
                self.assertGreater(report["reading_time_seconds"], 0)
                for suggestion in report["suggestions"]:
                    self.assertEqual(text[suggestion["start"]:suggestion["end"]], suggestion["original_span"])
                # Reverse order keeps earlier offsets valid when lengths change.
                rewritten = text
                for suggestion in reversed(report["suggestions"]):
                    rewritten = apply_suggestion(rewritten, suggestion)
                after = analyze_copy(rewritten, market, glossary)
                if after["cta_suggestions"]:
                    rewritten = apply_suggestion(rewritten, after["cta_suggestions"][0])
                    after = analyze_copy(rewritten, market, glossary)
                self.assertEqual(after["cta_strength"], "strong")
                self.assertGreaterEqual(after["readiness_score"], report["readiness_score"])
        self.assertNotIn("text", json.loads(self.manager.export_json())[0])


if __name__ == "__main__":
    unittest.main()
