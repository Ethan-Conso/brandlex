"""Persistence and export contracts, exercised against disposable libraries."""

import codecs
import csv
import io
import json
import sqlite3
from contextlib import closing
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

from core.db_manager import DBManager, SnapshotSyncError, TBX_NAMESPACE


def term(identifier=1, name="Product Seeding"):
    return {
        "id": identifier, "term_en": name, "term_hk": "好物推介",
        "term_cn": "种草", "aliases": ["seeding", "安利"],
        "category": "社媒与种草", "platforms": ["IG", "小红书"],
        "meaning": "通过真实体验分享，让更多人认识产品。",
        "bad_example": "亲，一起种草吧。", "good_example_en": "Meet your new everyday favourite.",
        "good_example_hk": "今次私心推介呢款隨身香水。",
        "good_example_cn": "这款随身香水值得加入你的通勤包。",
        "usage_tip": "香港品牌帖文可写好物推介，内地社媒常写种草。",
    }


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.seed = self.root / "glossary_seed.json"
        self.seed.write_text(json.dumps([term()], ensure_ascii=False), encoding="utf-8")
        self.options = dict(db_path=self.root / "digilex.db", json_path=self.root / "glossary.json", seed_path=self.seed)
        self.db = DBManager(**self.options)

    def tearDown(self):
        self.temporary.cleanup()

    def assert_snapshot(self):
        self.assertEqual(json.loads(self.options["json_path"].read_text(encoding="utf-8")), self.db.get_all_terms())

    def test_bootstrap_and_round_trip_mutations(self):
        self.assertEqual(len(self.db.get_all_terms()), 1)
        payload = {k: v for k, v in term(name="Community Pick").items() if k != "id"}
        added = self.db.add_term(payload)
        self.assertEqual(added["id"], 2)
        self.assertIn("updated_at", added)
        self.assertNotIn("id", payload)
        updated = self.db.update_term(added["id"], {"term_cn": "社群推荐", "aliases": ["community"]})
        self.assertEqual(updated["term_cn"], "社群推荐")
        reopened = DBManager(**self.options)
        self.assertEqual(reopened.get_term(added["id"]), updated)
        self.assert_snapshot()
        self.assertTrue(reopened.delete_term(added["id"]))
        self.assertFalse(reopened.delete_term(added["id"]))
        self.assertIsNone(reopened.get_term(added["id"]))
        self.assert_snapshot()

    def test_legacy_categories_migrate_without_replacing_custom_terms(self):
        labels = (
            ("\U0001F4F1 社媒与内容种草", "社媒与种草"),
            ("\U0001F6CD\uFE0F 电商与大促转化", "电商与转化"),
            ("\U0001F4C8 广告投放与增长指标", "投放与增长"),
            ("\U0001F48E 品牌公关与线下体验", "公关与线下"),
            ("\u270D\uFE0F 广告文案与视觉修辞", "文案与修辞"),
        )
        for index, (_, current) in enumerate(labels[1:], start=2):
            self.db.add_term({key: value for key, value in {
                **term(name=f"Custom Expression {index}"), "category": current,
                "usage_tip": "团队自订指引，迁移后须完整保留。",
            }.items() if key != "id"})
        before = self.db.get_all_terms()
        with closing(sqlite3.connect(self.db.db_path)) as connection, connection:
            for legacy, current in labels:
                connection.execute("UPDATE terms SET category = ? WHERE category = ?", (legacy, current))
        reopened = DBManager(**self.options)
        self.assertEqual(reopened.get_all_terms(), before)
        self.assertEqual(DBManager(**self.options).get_all_terms(), before)
        self.assert_snapshot()

    def test_legacy_default_categories_load_without_overwriting_source(self):
        legacy = {**term(), "category": "\U0001F4F1 社媒与内容种草"}
        self.seed.write_text(json.dumps([legacy], ensure_ascii=False), encoding="utf-8")
        original = self.seed.read_bytes()
        restored = self.db.reset_to_defaults()
        self.assertEqual(restored[0]["category"], "社媒与种草")
        fresh = DBManager(db_path=self.root / "new.db", json_path=self.root / "new.json", seed_path=self.seed)
        self.assertEqual(fresh.get_term(1)["category"], "社媒与种草")
        self.assertEqual(self.seed.read_bytes(), original)

    def test_delete_last_does_not_reseed_on_reopen(self):
        self.db.delete_term(1)
        self.assertEqual(DBManager(**self.options).get_all_terms(), [])
        self.assert_snapshot()

    def test_reset_restores_seed_without_editing_it(self):
        original = self.seed.read_bytes()
        self.db.update_term(1, {"term_cn": "自订词语"})
        self.db.add_term({k: v for k, v in term(name="Other").items() if k != "id"})
        restored = self.db.reset_to_defaults()
        self.assertEqual(len(restored), 1)
        self.assertEqual(self.db.get_term(1)["term_cn"], "种草")
        self.assertEqual(self.seed.read_bytes(), original)
        self.assert_snapshot()

    def test_validation_failure_does_not_write(self):
        before = self.db.get_all_terms()
        for invalid in ({"term_cn": ""}, {"platforms": "IG"}, {"aliases": [2]}, {"category": "Unknown"}, {"id": 200}, {"extra": "value"}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.db.update_term(1, invalid)
        with self.assertRaises(ValueError):
            self.db.add_term({"term_en": "Incomplete"})
        self.assertEqual(self.db.get_all_terms(), before)
        self.assert_snapshot()

    def test_missing_identifiers_and_invalid_types(self):
        with self.assertRaises(KeyError):
            self.db.update_term(999, {"term_cn": "词语"})
        for identifier in (True, -1, "1 OR 1=1"):
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                self.db.delete_term(identifier)

    def test_sql_strings_and_search_are_literal(self):
        unusual = "Brand's <gift> & \"); DROP TABLE terms; --"
        self.db.update_term(1, {"term_en": unusual})
        self.assertEqual(self.db.get_term(1)["term_en"], unusual)
        self.assertEqual(len(self.db.search_terms("安利")), 1)
        self.assertEqual(self.db.search_terms("' OR 1=1 --"), [])
        self.assertEqual(self.db.search_terms("", category="电商与转化"), [])

    def test_reads_are_fresh_and_input_not_mutated(self):
        original = self.db.get_term(1)
        original["aliases"].append("temporary")
        self.assertNotIn("temporary", self.db.get_term(1)["aliases"])
        self.db.update_term(1, {"aliases": ["new"]})
        self.assertEqual(DBManager(**self.options).get_term(1)["aliases"], ["new"])

    def test_reuses_one_index_and_does_not_publish_on_reads(self):
        snapshot = self.options["json_path"].stat().st_mtime_ns
        engine = self.db.get_search_engine()
        with patch.object(self.db, "_connection", side_effect=AssertionError("database read")):
            self.assertIs(self.db.get_search_engine(), engine)
            self.assertEqual(self.db.search_terms("安利")[0]["id"], 1)
            self.assertEqual(self.db.get_term(1)["id"], 1)
            self.assertEqual(self.db.get_all_terms()[0]["id"], 1)
            self.db.export_json()
        DBManager(**self.options)
        self.assertEqual(self.options["json_path"].stat().st_mtime_ns, snapshot)

    def test_indexes_track_mutations_across_managers(self):
        other = DBManager(**self.options)
        original = self.db.get_search_engine()
        other.update_term(1, {"aliases": ["new campaign phrase"], "category": "公关与线下"})
        current = self.db.get_search_engine()
        self.assertIsNot(original, current)
        self.assertEqual(original.search("安利")[0]["id"], 1)
        self.assertEqual(current.search("new campaign phrase")[0]["id"], 1)
        self.assertEqual(self.db.search_terms("安利"), [])
        other.delete_term(1)
        self.assertEqual(self.db.get_all_terms(), [])
        other.reset_to_defaults()
        self.assertEqual(self.db.get_term(1)["term_en"], "Product Seeding")

    def test_failed_reset_preserves_current_library(self):
        before = self.db.get_all_terms()
        self.seed.write_text('[{"id": 1}]', encoding="utf-8")
        with self.assertRaises(ValueError):
            self.db.reset_to_defaults()
        self.assertEqual(self.db.get_all_terms(), before)

    def test_snapshot_repaired_from_database_on_reopen(self):
        self.options["json_path"].write_text("damaged", encoding="utf-8")
        DBManager(**self.options)
        self.assert_snapshot()

    def test_snapshot_failure_reports_saved_state_and_can_retry(self):
        with patch("core.db_manager.os.replace", side_effect=OSError("disk unavailable")):
            with self.assertRaises(SnapshotSyncError):
                self.db.update_term(1, {"term_cn": "新品推荐"})
        self.assertEqual(self.db.get_term(1)["term_cn"], "新品推荐")
        self.db.sync_json()
        self.assert_snapshot()
        self.assertEqual(list(self.root.glob("*.tmp")), [])

    def test_exports_are_unicode_safe_and_parseable(self):
        special = "Brand's <gift> & café\nlaunch"
        self.db.update_term(1, {"term_en": special, "good_example_en": '=HYPERLINK("bad")'})
        content = self.db.export_json()
        self.assertEqual(json.loads(content), self.db.get_all_terms())
        csv_data = self.db.export_csv()
        self.assertTrue(csv_data.startswith(codecs.BOM_UTF8))
        row = next(csv.DictReader(io.StringIO(csv_data.decode("utf-8-sig"))))
        self.assertEqual(row["term_en"], special)
        self.assertTrue(row["good_example_en"].startswith("'="))
        self.assertEqual(json.loads(row["aliases"]), ["seeding", "安利"])
        tbx = ET.fromstring(self.db.export_tbx())
        self.assertEqual(tbx.tag, f"{{{TBX_NAMESPACE}}}tbx")
        namespace = {"t": TBX_NAMESPACE}
        languages = {node.attrib["{http://www.w3.org/XML/1998/namespace}lang"] for node in tbx.findall(".//t:langSec", namespace)}
        self.assertEqual(languages, {"en", "zh-Hant-HK", "zh-Hans-CN"})
        self.assertEqual(tbx.find(".//t:term", namespace).text, special)
        for extension in ("csv", "json", "tbx"):
            destination = self.root / f"export.{extension}"
            self.assertEqual(self.db.export(extension, destination), destination.resolve())
            self.assertTrue(destination.exists())
        with self.assertRaises(ValueError):
            self.db.export("html")

    def test_paths_must_be_distinct(self):
        with self.assertRaises(ValueError):
            DBManager(db_path=self.seed, json_path=self.root / "other.json", seed_path=self.seed)

    def test_export_refuses_to_replace_library_or_defaults(self):
        for protected in (self.db.db_path, self.db.json_path, self.db.seed_path):
            with self.subTest(protected=protected), self.assertRaises(ValueError):
                self.db.export("json", protected)

    def test_rejects_characters_that_cannot_be_exported_to_xml(self):
        for invalid in ("bad\x00", "bad\ud800", "bad\ufffe", "bad\uffff", "x" * 6001):
            with self.subTest(invalid=repr(invalid)), self.assertRaises(ValueError):
                self.db.update_term(1, {"term_en": invalid})
        self.assertEqual(self.db.get_term(1)["term_en"], "Product Seeding")

    def test_empty_library_exports_and_missing_defaults(self):
        self.db.delete_term(1)
        self.assertEqual(json.loads(self.db.export_json()), [])
        self.assertEqual(list(csv.DictReader(io.StringIO(self.db.export_csv().decode("utf-8-sig")))), [])
        with self.assertRaises(ValueError):
            self.db.export_tbx()
        self.seed.unlink()
        with self.assertRaises(FileNotFoundError):
            self.db.reset_to_defaults()

    def test_invalid_and_duplicate_seed_never_replace_saved_terms(self):
        for invalid in ("not JSON", "{}", "[]", json.dumps([term(), term()])):
            self.seed.write_text(invalid, encoding="utf-8")
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.db.reset_to_defaults()
            self.assertEqual(len(self.db.get_all_terms()), 1)

    def test_concurrent_managers_preserve_all_updates_and_latest_snapshot(self):
        other = DBManager(**self.options)
        def add(index):
            manager = self.db if index % 2 else other
            return manager.add_term({k: v for k, v in term(name=f"Community Pick {index}").items() if k != "id"})
        with ThreadPoolExecutor(max_workers=4) as pool:
            records = list(pool.map(add, range(16)))
        self.assertEqual(len({record["id"] for record in records}), 16)
        self.assertEqual(len(self.db.get_all_terms()), 17)
        self.assert_snapshot()


if __name__ == "__main__":
    unittest.main()
