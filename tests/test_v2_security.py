"""Permission isolation and rewrite HTTP contracts, with no external calls."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import create_app
from tests import write_flagship_fixture


class V2SecurityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        write_flagship_fixture(self.temporary.name)
        self.app = create_app({
            "TESTING": True, "LIBRARY_DIR": self.temporary.name,
            "SECRET_KEY": "isolated-session-test-key", "ADMIN_PASSWORD": "private-test-password",
            "RATELIMIT_ENABLED": False,
        })
        self.client = self.app.test_client()
        self.headers = self.token(self.client)

    def tearDown(self):
        self.temporary.cleanup()

    def token(self, client):
        return {"X-CSRF-Token": client.get("/api/bootstrap").json["data"]["csrf_token"]}

    def login(self):
        response = self.client.post("/api/admin/login", json={"password": "private-test-password"}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.headers = {"X-CSRF-Token": response.json["data"]["csrf_token"]}
        return response

    def test_public_writes_are_denied_before_validation_and_never_touch_library(self):
        self.assertIs(self.client.get("/api/bootstrap").json["data"].get("is_admin"), False)
        for method, path in (("post", "/api/terms"), ("patch", "/api/terms/1"),
                             ("delete", "/api/terms/1"), ("post", "/api/library/reset")):
            for headers in ({}, self.headers):
                response = getattr(self.client, method)(path, json={}, headers=headers)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(response.json["error"], "请先解锁维护模式后再修改词库。")
        self.assertEqual(len(self.app.extensions["library"].get_all_terms()), 100)

    def test_login_is_session_scoped_rotates_csrf_and_logout_revokes(self):
        old_headers = self.headers
        self.assertIs(self.login().json["data"]["is_admin"], True)
        self.assertNotEqual(old_headers, self.headers)
        self.assertIs(self.client.get("/api/bootstrap").json["data"]["is_admin"], True)
        visitor = self.app.test_client()
        self.assertIs(visitor.get("/api/bootstrap").json["data"]["is_admin"], False)
        denied = visitor.delete("/api/terms/1", headers=self.token(visitor))
        self.assertEqual(denied.status_code, 403)
        edited = self.client.patch("/api/terms/1", json={"usage_tip": "维护用词提示"}, headers=self.headers)
        self.assertEqual(edited.status_code, 200)
        logged_out = self.client.post("/api/admin/logout", json={}, headers=self.headers)
        self.assertEqual(logged_out.status_code, 200)
        self.assertIs(logged_out.json["data"]["is_admin"], False)
        self.assertEqual(self.client.delete("/api/terms/1", headers=self.headers).status_code, 403)

    def test_bad_password_types_wrong_password_and_missing_configuration_fail_closed(self):
        for password in ("wrong", [], {}, 1, True, "", "x" * 1025):
            response = self.client.post("/api/admin/login", json={"password": password}, headers=self.headers)
            self.assertIn(response.status_code, {400, 401})
            self.assertIs(self.client.get("/api/bootstrap").json["data"]["is_admin"], False)
        self.app.config["ADMIN_PASSWORD"] = ""
        response = self.client.post("/api/admin/login", json={"password": "private-test-password"}, headers=self.headers)
        self.assertEqual(response.status_code, 503)

    def test_password_change_expiry_and_failed_relogin_revoke_admin(self):
        self.login()
        self.app.config["ADMIN_PASSWORD"] = "changed-password"
        self.assertIs(self.client.get("/api/bootstrap").json["data"]["is_admin"], False)
        self.app.config["ADMIN_PASSWORD"] = "private-test-password"
        self.login()
        with self.client.session_transaction() as session:
            session["admin_issued"] = 1
        self.assertIs(self.client.get("/api/bootstrap").json["data"]["is_admin"], False)
        self.login()
        self.client.post("/api/admin/login", json={"password": "wrong"}, headers=self.headers)
        self.assertIs(self.client.get("/api/bootstrap").json["data"]["is_admin"], False)

    def test_login_rewrite_and_logout_require_csrf_and_same_origin(self):
        for path, payload in (("/api/admin/login", {"password": "private-test-password"}),
                              ("/api/admin/logout", {}),
                              ("/api/rewrite", {"text": "包邮", "target_market": "hk", "tone": "standard"})):
            self.assertEqual(self.client.post(path, json=payload).status_code, 403)
            response = self.client.post(path, json=payload, headers={**self.headers, "Origin": "https://foreign.example"})
            self.assertEqual(response.status_code, 403)

    def test_login_has_own_rate_limit(self):
        self.app.config.update(RATELIMIT_ENABLED=True, LOGIN_RATE_LIMIT=2)
        for _ in range(2):
            self.assertEqual(self.client.post("/api/admin/login", json={"password": "wrong"}, headers=self.headers).status_code, 401)
        response = self.client.post("/api/admin/login", json={"password": "wrong"}, headers=self.headers)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.headers["Retry-After"], "60")

    def test_rewrite_validates_contract_and_uses_live_glossary(self):
        payload = {"text": "包邮", "target_market": "hk", "tone": "social"}
        result = {"primary_copy": "免運費", "alt_copy": "免運費", "engine": "fallback"}
        with patch("app.rewrite_copy", return_value=result) as rewrite:
            response = self.client.post("/api/rewrite", json=payload, headers=self.headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["data"], result)
            self.assertEqual(rewrite.call_args.args[:3], ("包邮", "hk", "social"))
            self.assertEqual(len(rewrite.call_args.args[3]), 100)
        for bad in ({**payload, "text": ""}, {**payload, "tone": []}, {**payload, "target_market": {}},
                    {**payload, "text": "x" * 20001}, {**payload, "text": "hello\x00world"},
                    {**payload, "unexpected": True}, {"text": "a", "target_market": "hk"}):
            self.assertEqual(self.client.post("/api/rewrite", json=bad, headers=self.headers).status_code, 400)
        malformed = json.dumps({**payload, "text": "\ud800"})
        self.assertEqual(self.client.post("/api/rewrite", data=malformed, content_type="application/json", headers=self.headers).status_code, 400)
        legacy = self.client.post("/api/check", json={"text": "", "target_market": "hk"}, headers=self.headers)
        self.assertEqual(legacy.status_code, 200)


if __name__ == "__main__":
    unittest.main()
