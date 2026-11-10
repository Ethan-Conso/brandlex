"""HTTP and security contracts for BrandLex, using disposable team libraries."""

import codecs
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

from app import create_app
from core.db_manager import DBManager, TBX_NAMESPACE
from core.schema import TERM_FIELDS
from tests import write_flagship_fixture
from data.seed_terms import build_seed_terms


class WebAppTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        write_flagship_fixture(self.root)
        self.application = create_app({
            "TESTING": True, "LIBRARY_DIR": self.root,
            "RATELIMIT_ENABLED": False, "SECRET_KEY": "test-session-key-only",
            "ADMIN_PASSWORD": "isolated-test-password",
        })
        self.client = self.application.test_client()
        self.bootstrap = self.client.get("/api/bootstrap").get_json()["data"]
        self.headers = {"X-CSRF-Token": self.bootstrap["csrf_token"]}
        login = self.client.post("/api/admin/login", json={"password": "isolated-test-password"}, headers=self.headers)
        self.headers = {"X-CSRF-Token": login.json["data"]["csrf_token"]}

    def tearDown(self):
        self.temporary.cleanup()

    def term_payload(self):
        source = build_seed_terms()[0]
        return {**{key: value for key, value in source.items() if key != "id"},
                "term_en": "Signature Ritual", "term_hk": "品牌日常儀式",
                "term_cn": "品牌日常仪式", "aliases": ["daily ritual"]}

    def assert_error(self, response, status):
        self.assertEqual(response.status_code, status)
        payload = response.get_json()
        self.assertIs(payload["success"], False)
        self.assertIsInstance(payload["error"], str)
        self.assertRegex(payload["error"], r"[\u3400-\u9fff]")
        self.assertNotRegex(payload["error"], r"Traceback|sqlite3|term_en|updated_at|SELECT|INSERT")
        return payload

    def test_paginated_library_and_full_detail(self):
        first = self.client.get("/api/terms?offset=0").json["data"]
        self.assertEqual((first["offset"], first["limit"]), (0, 60))
        self.assertEqual(first["total"], first["matched_total"])
        self.assertEqual(sum(first["category_counts"].values()), first["total"])
        self.assertTrue(first["has_more"])
        self.assertEqual(len(first["terms"]), 60)
        self.assertEqual(set(first["terms"][0]), set(TERM_FIELDS) | {"learning_tip"})
        next_page = self.client.get("/api/terms?offset=60&limit=500").json["data"]
        self.assertEqual(next_page["limit"], 200)
        self.assertEqual(next_page["terms"][0]["id"], 61)
        detail = self.client.get("/api/terms/61").json["data"]
        self.assertIn("good_example_en", detail)
        filtered = self.client.get("/api/terms?category=公关与线下&offset=1&limit=1").json["data"]
        self.assertEqual(filtered["total"], first["total"])
        self.assertEqual(filtered["matched_total"], 20)
        self.assertEqual(filtered["category_counts"], first["category_counts"])
        self.assertEqual(len(filtered["terms"]), 1)
        self.assertTrue(filtered["has_more"])
        empty = self.client.get("/api/terms?offset=10000").json["data"]
        self.assertEqual(empty["terms"], [])
        self.assertFalse(empty["has_more"])
        self.assertLess(len(self.client.get("/api/bootstrap").data), 40_000)

    def test_rejects_malformed_pagination(self):
        for query in ("offset=-1", "offset=1.2", "offset=", "limit=0", "limit=Infinity",
                      "limit=NaN", "offset=99999999999999999999999999999999"):
            with self.subTest(query=query):
                self.assert_error(self.client.get(f"/api/terms?{query}"), 400)

    def test_feed_returns_complete_cases_and_excludes_previous_batch(self):
        category = "社媒与种草"
        response = self.client.get("/api/terms", query_string={"category": category})
        self.assertIn("no-store", response.headers.get("Cache-Control", ""))
        first = response.json["data"]
        self.assertEqual(first["total"], 100)
        self.assertEqual(first["matched_total"], 20)
        self.assertEqual((first["offset"], first["limit"], first["has_more"]), (0, 6, False))
        self.assertEqual(len(first["terms"]), 6)
        self.assertTrue(all(row["category"] == category and set(row) == set(TERM_FIELDS) | {"learning_tip"}
                            for row in first["terms"]))
        previous = {row["id"] for row in first["terms"]}
        second = self.client.get("/api/terms", query_string={
            "mode": "feed", "category": category, "exclude": ",".join(map(str, previous)), "limit": 8,
        }).json["data"]
        current = {row["id"] for row in second["terms"]}
        self.assertEqual(len(current), 8)
        self.assertTrue(previous.isdisjoint(current))
        self.assertEqual(second["matched_total"], 20)

    def test_feed_rejects_malformed_or_excessive_exclusions(self):
        for exclude in ("0", "-2", "1,,2", "1,2,", "1e9", "２", str(2**63),
                        ",".join(["1"] * 201), "9" * 4001):
            with self.subTest(exclude=exclude):
                response = self.client.get("/api/terms", query_string={"mode": "feed", "exclude": exclude})
                self.assert_error(response, 400)

    def test_home_and_bootstrap_provide_clean_working_app(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("BrandLex", html)
        self.assertIn('name="csrf-token"', html)
        self.assertIn("static/css/style.css", html)
        self.assertIn("static/js/main.js", html)
        for forbidden in ("TRA6202", "Dr. Siu", "Member 1", "Section 3", "CRUD",
                          "SQLite Dual-Sync", "4D Index", "Tokenization", "ABSA"):
            self.assertNotIn(forbidden, html)
        self.assertEqual(len(self.bootstrap["terms"]), 6)
        self.assertEqual(len(self.bootstrap["categories"]), 12)
        self.assertEqual(len(self.bootstrap["samples"]), 4)
        self.assertTrue(self.bootstrap["csrf_token"])

    def test_response_headers_protect_app_and_user_content(self):
        response = self.client.get("/")
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertIn("default-src", response.headers.get("Content-Security-Policy", ""))
        self.assertIn(response.headers.get("X-Frame-Options"), {"DENY", "SAMEORIGIN"})
        self.assertTrue(response.headers.get("Referrer-Policy"))
        self.assertIn("no-store", response.headers.get("Cache-Control", ""))

    def test_search_category_and_term_lookup(self):
        category = "电商与转化"
        response = self.client.get("/api/terms", query_string={"q": "EARLY BIRD", "category": category})
        self.assertEqual(response.status_code, 200)
        result = response.get_json()["data"]
        self.assertEqual(result["matched_total"], 1)
        self.assertEqual(result["terms"][0]["term_cn"], "早鸟福利")
        identifier = result["terms"][0]["id"]
        term = self.client.get(f"/api/terms/{identifier}").get_json()["data"]
        self.assertEqual(term["id"], identifier)
        self.assertEqual(self.client.get("/api/terms", query_string={"category": category}).get_json()["data"]["matched_total"], 20)
        self.assertEqual(self.client.get("/api/terms", query_string={"q": "no-such-term"}).get_json()["data"]["terms"], [])
        self.assertEqual(self.client.get("/api/terms", query_string={"q": "--"}).get_json()["data"]["matched_total"], 0)

    def test_add_edit_delete_survive_app_reopen_and_snapshot(self):
        created = self.client.post("/api/terms", json=self.term_payload(), headers=self.headers)
        self.assertEqual(created.status_code, 201)
        saved = created.get_json()["data"]
        identifier = saved["id"]
        self.assertGreater(identifier, 100)
        case = self.client.get("/api/terms?q=Signature%20Ritual").json["data"]["terms"][0]
        self.assertTrue(0 < len(case["learning_tip"]) <= 22)
        self.assertEqual(case["usage_tip"], saved["usage_tip"])
        edited = self.client.patch(f"/api/terms/{identifier}", json={"term_hk": "品牌晨間儀式"}, headers=self.headers)
        self.assertEqual(edited.status_code, 200)
        self.assertEqual(edited.get_json()["data"]["term_hk"], "品牌晨間儀式")
        reopened = DBManager(db_path=self.root / "digilex.db", json_path=self.root / "glossary.json", seed_path=self.root / "glossary_seed.json")
        self.assertEqual(reopened.get_term(identifier)["term_hk"], "品牌晨間儀式")
        self.assertEqual(json.loads((self.root / "glossary.json").read_text()), reopened.get_all_terms())
        deleted = self.client.delete(f"/api/terms/{identifier}", headers=self.headers)
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(deleted.get_json()["data"]["id"], identifier)
        self.assert_error(self.client.get(f"/api/terms/{identifier}"), 404)

    def test_validation_rejects_partial_new_term_and_unknown_fields(self):
        for payload in ({"term_en": "Incomplete"}, {**self.term_payload(), "unexpected": "value"},
                        {**self.term_payload(), "platforms": "IG"}, {**self.term_payload(), "category": "Unknown"}):
            with self.subTest(payload=payload):
                self.assert_error(self.client.post("/api/terms", json=payload, headers=self.headers), 400)
        self.assert_error(self.client.patch("/api/terms/1", json={"id": 3}, headers=self.headers), 400)
        self.assertEqual(self.client.get("/api/terms").get_json()["data"]["total"], 100)

    def test_create_and_update_require_chinese_and_english_definitions(self):
        original = self.client.get("/api/terms/1").json["data"]["meaning"]
        payload = self.term_payload()
        for meaning in ("只提供中文释义。", "EN: English only.", "Only English. EN: Still English.",
                        "中文释义。 EN:", "中文释义。 EN: EN:", "中文释义。 EN: 仅中文。", ""):
            with self.subTest(meaning=meaning):
                created = self.client.post("/api/terms", json={**payload, "meaning": meaning}, headers=self.headers)
                updated = self.client.patch("/api/terms/1", json={"meaning": meaning}, headers=self.headers)
                for response in (created, updated):
                    self.assertIn("EN:", self.assert_error(response, 400)["error"])
        no_meaning = {key: value for key, value in payload.items() if key != "meaning"}
        response = self.client.post("/api/terms", json=no_meaning, headers=self.headers)
        self.assertIn("EN:", self.assert_error(response, 400)["error"])
        self.assertEqual(self.client.get("/api/terms/1").json["data"]["meaning"], original)
        self.assertEqual(self.client.get("/api/terms").json["data"]["total"], 100)
        accepted = self.client.post("/api/terms", json={
            **payload, "meaning": "品牌日常仪式。\nEN: A recurring brand ritual.",
        }, headers=self.headers)
        self.assertEqual(accepted.status_code, 201)
        self.assertEqual(accepted.json["data"]["meaning"], "品牌日常仪式。 EN: A recurring brand ritual.")

    def test_mutations_and_copy_check_require_valid_csrf(self):
        operations = (
            ("post", "/api/terms", self.term_payload()),
            ("patch", "/api/terms/1", {"term_cn": "改写"}),
            ("delete", "/api/terms/1", None),
            ("post", "/api/library/reset", {"confirm": True}),
            ("post", "/api/check", {"text": "包邮", "target_market": "hk"}),
        )
        for method, url, payload in operations:
            for headers in ({}, {"X-CSRF-Token": "wrong-token"}):
                with self.subTest(method=method, url=url, headers=headers):
                    response = getattr(self.client, method)(url, json=payload, headers=headers)
                    self.assert_error(response, 403)
        self.assertEqual(self.client.get("/api/terms").get_json()["data"]["total"], 100)

    def test_session_token_is_not_shared_between_visitors(self):
        other_client = self.application.test_client()
        token = other_client.get("/api/bootstrap").get_json()["data"]["csrf_token"]
        self.assertNotEqual(token, self.headers["X-CSRF-Token"])
        self.assert_error(other_client.post("/api/check", json={"text": "Shop now.", "target_market": "en"}, headers=self.headers), 403)

    def test_wrong_origin_cannot_write_even_with_token(self):
        response = self.client.post("/api/terms", json=self.term_payload(),
                                    headers={**self.headers, "Origin": "https://unrelated.example"})
        self.assert_error(response, 403)

    def test_malformed_json_and_nonobject_payloads_get_plain_errors(self):
        response = self.client.post("/api/check", data="{bad", content_type="application/json", headers=self.headers)
        self.assert_error(response, 400)
        for payload in ([], "text", 5, None):
            with self.subTest(payload=payload):
                response = self.client.post("/api/check", data=json.dumps(payload), content_type="application/json", headers=self.headers)
                self.assert_error(response, 400)

    def test_copy_check_uses_current_library_and_precise_unicode_positions(self):
        created = self.client.post("/api/terms", json=self.term_payload(), headers=self.headers).get_json()["data"]
        text = "✨包邮！包邮！daily ritual。立即入手。"
        report = self.client.post("/api/check", json={"text": text, "target_market": "hk"}, headers=self.headers).get_json()["data"]
        self.assertTrue(0 <= report["readiness_score"] <= 100)
        self.assertEqual(len([s for s in report["suggestions"] if s["original_span"] == "包邮"]), 2)
        for suggestion in report["suggestions"]:
            self.assertEqual(text[suggestion["start"]:suggestion["end"]], suggestion["original_span"])
        self.assertIn(created["id"], [record["id"] for record in report["matched_glossary_terms"]])
        self.client.delete(f"/api/terms/{created['id']}", headers=self.headers)
        report = self.client.post("/api/check", json={"text": text, "target_market": "hk"}, headers=self.headers).get_json()["data"]
        self.assertNotIn(created["id"], [record["id"] for record in report["matched_glossary_terms"]])

    def test_copy_input_validation_and_empty_draft(self):
        for payload in ({"text": "copy", "target_market": "unknown"}, {"text": 3, "target_market": "hk"},
                        {"text": "copy"}, {"target_market": "hk"}, {"text": "x" * 20_001, "target_market": "en"}):
            with self.subTest(payload=str(payload)[:100]):
                self.assert_error(self.client.post("/api/check", json=payload, headers=self.headers), 400)
        empty = self.client.post("/api/check", json={"text": "", "target_market": "en"}, headers=self.headers).get_json()["data"]
        self.assertEqual(empty["score"], 0)
        self.assertEqual(empty["word_count"], 0)

    def test_structured_or_numeric_market_values_are_invalid_input(self):
        for market in ([], {}, ["hk"], 1, True):
            with self.subTest(market=market):
                response = self.client.post("/api/check", json={"text": "Draft", "target_market": market}, headers=self.headers)
                self.assert_error(response, 400)

    def test_invalid_identifier_ranges_are_client_errors(self):
        for identifier in (0, 2**63, 10**50):
            for method, payload in (("get", None), ("patch", {"term_cn": "测试词条"}), ("delete", None)):
                with self.subTest(identifier=identifier, method=method):
                    response = getattr(self.client, method)(f"/api/terms/{identifier}", json=payload, headers=self.headers)
                    self.assertIn(response.status_code, {400, 404})
                    self.assert_error(response, response.status_code)

    def test_malformed_origin_and_nonascii_token_do_not_cause_server_errors(self):
        payload = {"text": "Shop now.", "target_market": "en"}
        response = self.client.post("/api/check", json=payload, headers={**self.headers, "Origin": "http://[invalid]"})
        self.assert_error(response, 403)
        response = self.client.post("/api/check", json=payload, headers={"X-CSRF-Token": "é"})
        self.assert_error(response, 403)

    def test_large_request_is_rejected_before_processing(self):
        response = self.client.post("/api/check", data="x" * 1_100_000, content_type="application/json", headers=self.headers)
        self.assert_error(response, 413)

    def test_all_sample_drafts_can_be_checked(self):
        for draft in self.bootstrap["samples"]:
            with self.subTest(draft=draft["id"]):
                response = self.client.post("/api/check", json={"text": draft["text"], "target_market": draft["target_market"]}, headers=self.headers)
                self.assertEqual(response.status_code, 200)
                report = response.get_json()["data"]
                self.assertGreater(report["character_count"], 0)
                self.assertGreater(report["reading_time_seconds"], 0)
                self.assertEqual(report["target_market"], draft["target_market"])

    def test_downloads_are_attachments_with_safe_trilingual_content(self):
        for format in ("csv", "tbx", "json"):
            with self.subTest(format=format):
                response = self.client.get(f"/api/export/{format}")
                self.assertEqual(response.status_code, 200)
                self.assertIn("attachment", response.headers.get("Content-Disposition", ""))
                self.assertIn(f".{format}", response.headers["Content-Disposition"])
                if format == "csv":
                    self.assertTrue(response.data.startswith(codecs.BOM_UTF8))
                elif format == "json":
                    self.assertEqual(len(json.loads(response.data)), 100)
                else:
                    document = ET.fromstring(response.data)
                    self.assertEqual(len(document.findall(f".//{{{TBX_NAMESPACE}}}conceptEntry")), 100)
        self.assert_error(self.client.get("/api/export/html"), 400)

    def test_reset_requires_explicit_intent_and_restores_defaults(self):
        for payload in ({}, {"confirm": False}, {"confirm": "true"}, {"confirm": 1}):
            self.assert_error(self.client.post("/api/library/reset", json=payload, headers=self.headers), 400)
        self.client.delete("/api/terms/1", headers=self.headers)
        self.client.post("/api/terms", json=self.term_payload(), headers=self.headers)
        restored = self.client.post("/api/library/reset", json={"confirm": True}, headers=self.headers)
        self.assertEqual(restored.status_code, 200)
        result = restored.get_json()["data"]
        self.assertEqual(result["total"], 100)
        self.assertEqual(result["terms"][0]["term_en"], "Product Seeding")

    def test_missing_routes_and_terms_have_json_api_errors(self):
        for url in ("/api/missing", "/api/terms/999", "/api/terms/not-a-number"):
            with self.subTest(url=url):
                self.assert_error(self.client.get(url), 404)
        self.assert_error(self.client.patch("/api/terms/999", json={"term_cn": "词语"}, headers=self.headers), 404)
        self.assert_error(self.client.delete("/api/terms/999", headers=self.headers), 404)

    def test_stored_html_is_returned_as_data_and_not_inserted_into_page(self):
        injection = '<img src=x onerror="alert(1)">'
        payload = {**self.term_payload(), "term_en": injection}
        response = self.client.post("/api/terms", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["data"]["term_en"], injection)
        self.assertNotIn(injection, self.client.get("/").get_data(as_text=True))
        self.assertTrue(response.content_type.startswith("application/json"))

    def test_unexpected_backend_error_does_not_disclose_internal_details(self):
        with self.assertLogs(self.application.logger, level="ERROR"), patch.object(self.application.extensions["library"], "get_search_engine", side_effect=RuntimeError("SELECT * FROM secret_table")):
            response = self.client.get("/api/terms")
        self.assert_error(response, 500)

    def test_unavailable_storage_returns_retryable_localized_error(self):
        with self.assertLogs(self.application.logger, level="ERROR"), patch.object(self.application.extensions["library"], "get_search_engine", side_effect=sqlite3.OperationalError("database secret_path unavailable")):
            response = self.client.get("/api/bootstrap")
        self.assert_error(response, 503)
        self.assertNotIn("secret_path", response.get_json()["error"])

    def test_saved_but_failed_snapshot_is_reported_and_recoverable(self):
        with self.assertLogs(self.application.logger, level="ERROR"), patch("core.db_manager.os.replace", side_effect=OSError("disk unavailable")):
            response = self.client.post("/api/terms", json=self.term_payload(), headers=self.headers)
        payload = self.assert_error(response, 503)
        self.assertIs(payload["saved"], True)
        result = self.client.get("/api/terms", query_string={"q": "Signature Ritual"}).get_json()["data"]
        self.assertEqual(result["matched_total"], 1)
        library = self.application.extensions["library"]
        library.sync_json()
        self.assertEqual(json.loads((self.root / "glossary.json").read_text()), library.get_all_terms())

    def test_rate_limit_returns_json_after_configured_budget(self):
        application = create_app({"TESTING": True, "LIBRARY_DIR": self.root,
                                  "RATELIMIT_ENABLED": True, "API_RATE_LIMIT": 2})
        client = application.test_client()
        self.assertEqual(client.get("/api/bootstrap").status_code, 200)
        self.assertEqual(client.get("/api/bootstrap").status_code, 200)
        response = client.get("/api/bootstrap")
        self.assert_error(response, 429)
        self.assertTrue(response.headers.get("Retry-After"))


if __name__ == "__main__":
    unittest.main()
