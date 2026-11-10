"""The GitHub Pages artifact must work as a project site and exclude local state."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urljoin, urlsplit

from core.search_engine import SearchEngine
from tests.test_homepage import PageElements


ROOT = Path(__file__).resolve().parents[1]
PROJECT_URL = "https://example.github.io/brandlex/"
GATEWAY = "https://rewrite.example.net:8443/api/pages/rewrite"


class GitHubPagesBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temporary.cleanup)
        cls.project = Path(temporary.name) / "brandlex"
        shutil.copytree(ROOT, cls.project, ignore=shutil.ignore_patterns(
            ".git", ".env*", ".venv", "__pycache__", ".pytest_cache", ".coverage*",
            ".playwright*", "*.db*", "glossary.json", "docs", "visual_assets",
        ))
        (cls.project / ".env").write_text("DEEPSEEK_API_KEY=fixture-not-for-publication\n", encoding="utf-8")
        (cls.project / "data" / "digilex.db").write_bytes(b"private runtime database fixture")
        result = subprocess.run(
            [sys.executable, str(cls.project / "scripts" / "build_github_pages.py")],
            cwd=cls.project, capture_output=True, text=True, timeout=60,
            env={**os.environ, "BRANDLEX_PUBLIC_REWRITE_URL": ""},
        )
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.output = cls.project / "docs"

    def test_local_assets_resolve_inside_the_project_site(self):
        html = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertNotRegex(html, r"\{[{%]")
        page = PageElements(html)
        assets = [attrs["src"] for tag, attrs in page.elements if tag == "script" and "src" in attrs]
        assets += [attrs["href"] for tag, attrs in page.elements if tag == "link" and attrs.get("rel") == "stylesheet"]
        self.assertTrue(any(path.endswith("static/js/static_engine.js") for path in assets))
        for asset in assets:
            with self.subTest(asset=asset):
                url = urljoin(PROJECT_URL, asset)
                self.assertTrue(url.startswith(PROJECT_URL), url)
                self.assertTrue((self.output / urlsplit(url.removeprefix(PROJECT_URL)).path).is_file())

    def test_all_seed_terms_and_samples_ship_without_runtime_files(self):
        seed = json.loads((self.project / "data" / "glossary_seed.json").read_text(encoding="utf-8"))
        output = json.loads((self.output / "data" / "glossary_seed.json").read_text(encoding="utf-8"))
        self.assertEqual(len(output), 3208)
        self.assertEqual(len({record["category"] for record in output}), 12)
        self.assertEqual([{field: record[field] for field in seed[0]} for record in output], seed)
        self.assertEqual(
            json.loads((self.output / "data" / "sample_drafts.json").read_text(encoding="utf-8")),
            json.loads((self.project / "data" / "sample_drafts.json").read_text(encoding="utf-8")),
        )
        for path in self.output.rglob("*"):
            with self.subTest(path=path.relative_to(self.output)):
                self.assertNotIn(path.name, {".env", ".venv", "__pycache__", ".pytest_cache", "app.py"})
                self.assertNotIn(path.suffix, {".db", ".pyc"})
                if path.is_file():
                    self.assertNotIn(b"fixture-not-for-publication", path.read_bytes())

    def test_pages_gateway_build_config_and_csp(self):
        from scripts.build_github_pages import static_head

        without_gateway = static_head("")
        self.assertNotIn("brandlex-public-rewrite-url", without_gateway)
        html = static_head(GATEWAY)
        self.assertIn(f'<meta name="brandlex-public-rewrite-url" content="{GATEWAY}">', html)
        self.assertIn("connect-src 'self' https://api.deepseek.com https://rewrite.example.net:8443;", html)
        for invalid in (
            "http://rewrite.example.net/api/pages/rewrite",
            "https://user:pass@rewrite.example.net/api/pages/rewrite",
            "https://rewrite.example.net/api/pages/rewrite?token=fixture",
            "https://rewrite.example.net/api/pages/rewrite#",
            "https://rewrite.example.net/api/rewrite",
            "https://rewrite.example.net:65536/api/pages/rewrite",
            'https://rewrite.example.net"; script-src *;/api/pages/rewrite',
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                static_head(invalid)

    @unittest.skipUnless(shutil.which("node"), "Node.js is required for the public rewrite check")
    def test_static_public_rewrite_uses_cache_or_a_credential_free_gateway(self):
        result = subprocess.run(
            ["node", str(ROOT / "tests" / "github_pages_rewrite.cjs"), str(self.output), GATEWAY],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(shutil.which("node"), "Node.js is required for the search parity check")
    def test_static_search_returns_the_flask_ranking_and_counts(self):
        engine = SearchEngine(json.loads((self.output / "data" / "glossary_seed.json").read_text(encoding="utf-8")))
        queries = [
            ("ROAS", "", 0), ("ＲＯＡＳ", "", 0), ("CTR", "", 0), ("ROAS date", "", 0),
            ("PPC", "", 0), ("Pay-Per-Click", "", 0), ("CPC", "", 0),
            ("Conversion Rate (CVR)", "", 0), ("Landing Page", "", 0),
            ("early–bird", "", 0), ("Product Seeding", "", 0), ("A/B Testing", "", 0),
            ("香港 包邮", "电商与转化", 0), ("防晒", "", 12), ("—", "", 0),
            ("免運費", "", 0), ("限时", "", 0), ("", "文旅与酒店", 36),
            ("no-match-brandlex-test", "", 0),
        ]
        result = subprocess.run(
            ["node", str(ROOT / "tests" / "github_pages_search.cjs"), str(self.output)],
            input=json.dumps(queries, ensure_ascii=False), capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for (query, category, offset), page in zip(queries, json.loads(result.stdout), strict=True):
            with self.subTest(query=query, category=category, offset=offset):
                expected, total = engine.search_page(query, category or None, offset=offset, limit=12)
                self.assertEqual(page["ids"], [record["id"] for record in expected])
                self.assertEqual(page["matched_total"], total)
                self.assertEqual(page["has_more"], offset + len(expected) < total)
                if query in {"ROAS", "ＲＯＡＳ", "CTR"}:
                    self.assertEqual(page["ids"], [42 if query == "CTR" else 41])
                    self.assertEqual(page["matched_total"], 1)
