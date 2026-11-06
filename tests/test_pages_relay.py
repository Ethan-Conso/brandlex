"""GitHub Pages can rewrite uncached drafts without a session or provider key."""

import json
import tempfile
import unittest
from unittest.mock import patch

from app import create_pages_app
from tests import write_flagship_fixture


ORIGIN = "https://ethan-conso.github.io"
PATH = "/api/pages/rewrite"
DRAFT = {"text": "今晚一起出门散步。", "target_market": "en", "tone": "social"}


class PagesRelayTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        write_flagship_fixture(self.temporary.name)
        self.client = self.relay()

    def relay(self, **config):
        return create_pages_app({
            "TESTING": True, "LIBRARY_DIR": self.temporary.name,
            "PAGES_ORIGIN": ORIGIN, "PAGES_TRUST_CLOUDFLARE": False, **config,
        }).test_client(use_cookies=False)

    def post(self, client=None, **options):
        return (client or self.client).post(PATH, **{
            "json": DRAFT, "headers": {"Origin": ORIGIN}, **options,
        })

    def test_preflight_and_rewrite_are_cookie_free_and_use_server_glossary(self):
        client = self.relay(PAGES_IP_RATE_LIMIT=1, PAGES_DAILY_LIMIT=1)
        preflight = client.options(PATH, headers={
            "Origin": ORIGIN, "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type, accept",
        })
        self.assertEqual(preflight.status_code, 204)
        self.assertEqual(preflight.headers["Access-Control-Allow-Origin"], ORIGIN)
        self.assertEqual(preflight.headers["Access-Control-Allow-Methods"], "POST")
        self.assertIn("Content-Type", preflight.headers["Access-Control-Allow-Headers"])
        self.assertIn("Origin", preflight.vary)
        with patch("app.rewrite_copy", return_value={"engine": "deepseek"}) as rewrite:
            result = self.post(client)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.headers["Access-Control-Allow-Origin"], ORIGIN)
        self.assertEqual(result.headers["Cache-Control"], "no-store")
        self.assertIsNone(result.headers.get("Access-Control-Allow-Credentials"))
        self.assertIsNone(result.headers.get("Set-Cookie"))
        self.assertEqual(result.json, {"success": True, "data": {"engine": "deepseek"}})
        self.assertEqual(rewrite.call_args.args[:3], (DRAFT["text"], "en", "social"))
        self.assertEqual(len(rewrite.call_args.args[3]), 100)

    def test_unapproved_origin_or_preflight_never_reaches_provider(self):
        with patch("app.rewrite_copy") as rewrite:
            for headers in ({}, {"Origin": "null"}, {"Origin": ORIGIN + ".example"},
                            {"Origin": ORIGIN + "/brandlex/"}):
                result = self.post(headers=headers)
                self.assertEqual(result.status_code, 403)
                self.assertNotIn("Access-Control-Allow-Origin", result.headers)
            for method, header in (("GET", "content-type"), ("POST", "authorization")):
                result = self.client.options(PATH, headers={
                    "Origin": ORIGIN, "Access-Control-Request-Method": method,
                    "Access-Control-Request-Headers": header,
                })
                self.assertEqual(result.status_code, 403)
            rewrite.assert_not_called()

    def test_relay_is_opt_in_and_does_not_expose_local_api(self):
        self.assertEqual(self.post(self.relay(PAGES_ORIGIN="")).status_code, 503)
        with self.assertRaises(ValueError):
            self.relay(PAGES_ORIGIN="http://example.com")
        with self.assertRaises(ValueError):
            self.relay(PAGES_ORIGIN="https://example.com:bad")
        for path in ("/", "/api/bootstrap", "/api/terms", "/api/rewrite", "/api/admin/login"):
            self.assertEqual(self.client.get(path).status_code, 404)
            self.assertEqual(self.client.post(path, json=DRAFT).status_code, 404)

    def test_health_check_does_not_use_origin_cookie_or_provider(self):
        client = self.relay(PAGES_ORIGIN="")
        with patch("app.rewrite_copy") as rewrite:
            result = client.get("/healthz")
            rewrite.assert_not_called()
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.get_data(), b"")
        self.assertEqual(result.headers["Cache-Control"], "no-store")
        self.assertNotIn("Set-Cookie", result.headers)
        self.assertNotIn("Access-Control-Allow-Origin", result.headers)

    def test_payload_rejections_are_readable_by_pages(self):
        with patch("app.rewrite_copy") as rewrite:
            for payload in ({**DRAFT, "model": "other"}, {**DRAFT, "tone": []},
                            {**DRAFT, "text": "x" * 4001}):
                result = self.post(json=payload)
                self.assertEqual(result.status_code, 400)
                self.assertEqual(result.headers["Access-Control-Allow-Origin"], ORIGIN)
            malformed = self.client.post(PATH, data=json.dumps({**DRAFT, "text": "\ud800"}),
                                         headers={"Origin": ORIGIN}, content_type="application/json")
            self.assertEqual(malformed.status_code, 400)
            result = self.client.post(PATH, data="x" * 65537, headers={"Origin": ORIGIN},
                                      content_type="application/json")
            self.assertEqual(result.status_code, 413)
            rewrite.assert_not_called()

    def test_per_ip_and_global_quotas_do_not_trust_forwarded_ip(self):
        client = self.relay(PAGES_IP_RATE_LIMIT=1, PAGES_DAILY_LIMIT=2)
        with patch("app.rewrite_copy", return_value={"engine": "deepseek"}) as rewrite:
            self.assertEqual(self.post(client).status_code, 200)
            self.assertEqual(self.post(client, headers={
                "Origin": ORIGIN, "X-Forwarded-For": "198.51.100.3", "CF-Connecting-IP": "198.51.100.4",
            }).status_code, 429)
            self.assertEqual(self.post(client, environ_overrides={"REMOTE_ADDR": "198.51.100.4"}).status_code, 200)
            limited = self.post(client, environ_overrides={"REMOTE_ADDR": "198.51.100.5"})
        self.assertEqual(limited.status_code, 429)
        self.assertEqual(limited.headers["Access-Control-Allow-Origin"], ORIGIN)
        self.assertEqual(limited.headers["Retry-After"], "86400")
        self.assertEqual(rewrite.call_count, 2)

    def test_opt_in_edge_uses_only_one_valid_cloudflare_address(self):
        client = self.relay(PAGES_IP_RATE_LIMIT=1, PAGES_TRUST_CLOUDFLARE=True)
        with patch("app.rewrite_copy", return_value={"engine": "deepseek"}):
            for ip, expected in (("2001:db8::1", 200), ("2001:0db8:0:0:0:0:0:1", 429),
                                 ("198.51.100.2", 200), ("192.0.2.1, 192.0.2.2", 200),
                                 ("not-an-ip", 429), ("", 429)):
                with self.subTest(ip=ip):
                    result = self.post(client, headers={"Origin": ORIGIN, "CF-Connecting-IP": ip})
                    self.assertEqual(result.status_code, expected)


if __name__ == "__main__":
    unittest.main()
