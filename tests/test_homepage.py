"""Homepage contracts for the airy, interactive product showcase."""

import re
from html import unescape
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from app import create_app
from data.init_seed_data import initialize_data


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("社媒与种草", "电商与转化", "投放与增长", "公关与线下", "文案与修辞",
              "美妆与个护", "时尚与奢品", "数码与科技", "餐饮与酒水", "文旅与酒店",
              "金融与支付", "合规与风控")
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u20E3\u200D]")


class PageElements(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        self.elements.append((tag, dict(attributes)))

    def with_attribute(self, name):
        return [attributes for _, attributes in self.elements if name in attributes]

    def by_id(self, identifier):
        return next((attributes for _, attributes in self.elements
                     if attributes.get("id") == identifier), {})


class HomepageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        root = Path(cls.temporary.name)
        initialize_data(root)
        cls.app = create_app({"TESTING": True, "LIBRARY_DIR": root,
                              "SECRET_KEY": "homepage-test-session", "RATELIMIT_ENABLED": False})

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def setUp(self):
        self.client = self.app.test_client()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.html = response.get_data(as_text=True)
        self.page = PageElements(self.html)
        self.home_html = self.html[self.html.index('id="view-home"'):self.html.index('id="view-studio"')]

    def test_default_page_has_three_accessible_views_with_home_selected(self):
        tabs = [item for item in self.page.with_attribute("data-view")
                if item.get("role") == "tab"]
        self.assertEqual([item["data-view"] for item in tabs], ["home", "studio", "library"])
        for view in ("home", "studio", "library"):
            with self.subTest(view=view):
                tab = self.page.by_id("tab-" + view)
                panel = self.page.by_id("view-" + view)
                self.assertEqual(tab.get("aria-controls"), "view-" + view)
                self.assertEqual(tab.get("aria-selected"), str(view == "home").lower())
                self.assertEqual(panel.get("role"), "tabpanel")
                self.assertEqual(panel.get("aria-labelledby"), "tab-" + view)
                self.assertEqual("hidden" in panel, view != "home")
        brand = next(attributes for _, attributes in self.page.elements
                     if "brand" in attributes.get("class", "").split())
        self.assertEqual(brand.get("href"), "#home")

    def test_home_has_preview_controls_and_real_workspace_destinations(self):
        text = re.sub(r"<[^>]*>", "", self.home_html)
        self.assertIn("一处词库基准，三地原生表达。", re.sub(r"\s+", "", text))
        self.assertIn("让每一次跨市场发声，自然着陆。", text)
        self.assertEqual([item["data-home-market"] for item in
                          self.page.with_attribute("data-home-market")], ["hk", "cn", "en"])
        for identifier in ("home-preview-copy", "home-preview-adaptations", "home-preview-market",
                           "home-source-copy", "home-edit-draft", "antigravity-canvas"):
            self.assertTrue(self.page.by_id(identifier), identifier)
        self.assertEqual(self.page.by_id("antigravity-canvas").get("aria-hidden"), "true")
        destinations = {item["data-go-view"] for item in self.page.with_attribute("data-go-view")}
        self.assertTrue({"studio", "library"}.issubset(destinations))

    def test_scenarios_have_a_dynamic_category_group_and_counter(self):
        bootstrap = self.client.get("/api/bootstrap").get_json()["data"]
        self.assertEqual(bootstrap["categories"], list(CATEGORIES))
        self.assertIn("aria-label", self.page.by_id("home-scenario-pills"))
        self.assertIn("hidden", self.page.by_id("home-library-count"))
        self.assertIn("hidden", self.page.by_id("load-more-terms"))
        self.assertNotIn("home-scenario-terms", self.home_html)
        self.assertNotIn("home-comparison", self.home_html)
        self.assertNotIn("传统机翻与字面转换的局限", self.home_html)

    def test_learning_uses_short_labels_and_keeps_pitfalls_out_of_card_template(self):
        self.assertRegex(self.html, r'id="tab-library"[^>]*>学习</button>')
        self.assertIn('data-go-view="library">进入学习', self.home_html)
        self.assertIn('data-go-view="library">探索三语学习', self.home_html)
        self.assertIn('三语表达学习', self.home_html)
        self.assertNotRegex(self.home_html, r"浏览品牌词库|查阅完整词库")
        self.assertEqual(self.page.by_id("library-search").get("placeholder"), "搜索三语表达或场景…")
        library_html = self.html[self.html.index('id="view-library"'):self.html.index('id="term-drawer"')]
        for removed in ("library-heading", "BRANDLEX CASEBOOK", "三语实战案例",
                        "地道实战例句", "避免写法", "case-before", "data-case-platforms"):
            self.assertNotIn(removed, library_html)
        self.assertTrue(self.page.with_attribute("data-try-case"))
        self.assertTrue(self.page.with_attribute("data-open-term"))

    def test_three_interactive_surfaces_have_accessible_controls_and_real_exports(self):
        names = [item["data-home-surface"] for item in self.page.with_attribute("data-home-surface")]
        self.assertEqual(names, ["rewrite", "glossary", "export"])
        for name in names:
            tab = self.page.by_id("home-surface-" + name)
            panel = self.page.by_id("home-surface-panel-" + name)
            self.assertEqual(tab.get("role"), "tab")
            self.assertEqual(tab.get("aria-controls"), "home-surface-panel-" + name)
            self.assertEqual(panel.get("role"), "tabpanel")
            self.assertEqual(panel.get("aria-labelledby"), "home-surface-" + name)
        self.assertEqual([item["data-mini-market"] for item in self.page.with_attribute("data-mini-market")], ["hk", "cn", "en"])
        self.assertEqual([item["data-mini-tone"] for item in self.page.with_attribute("data-mini-tone")], ["standard", "social", "concise"])
        exports = self.page.with_attribute("data-home-export")
        self.assertEqual([item["data-home-export"] for item in exports], ["csv", "tbx", "json"])
        for item in exports:
            self.assertEqual(item["href"], "/api/export/" + item["data-home-export"])
            self.assertIn("download", item)

    def test_descriptions_are_short_and_examples_remain_distinct(self):
        examples = ("home-source-copy", "home-preview-copy", "home-mini-copy")
        for paragraph in re.finditer(r"<p\b(?P<attrs>[^>]*)>(?P<text>.*?)</p>", self.home_html, re.S):
            if any(identifier in paragraph["attrs"] for identifier in examples):
                continue
            text = unescape(re.sub(r"<[^>]*>", "", paragraph["text"]))
            chinese = re.findall(r"[\u3400-\u9fff]", text)
            self.assertLessEqual(len(chinese), 28, text)

    def test_shipped_html_css_and_javascript_have_no_emoji(self):
        files = [ROOT / "templates/index.html", *sorted((ROOT / "static/css").glob("*.css")),
                 *sorted((ROOT / "static/js").glob("*.js"))]
        for path in files:
            with self.subTest(file=path.relative_to(ROOT)):
                self.assertIsNone(EMOJI.search(path.read_text(encoding="utf-8")))

    def test_studio_always_displays_human_verification_reminder(self):
        studio = self.html[self.html.index('id="view-studio"'):self.html.index('id="view-library"')]
        self.assertRegex(
            studio,
            r'(?s)class="workspace-note"[^>]*>\s*<span>.*?'
            r'<span id="rewrite-verification-note">请人工复核成稿中的适用地区、资格条件、优惠对象、起止时间与链接用途。</span>',
        )

    def test_home_remains_public_and_does_not_relax_write_permissions(self):
        bootstrap = self.client.get("/api/bootstrap").get_json()["data"]
        self.assertIs(bootstrap["is_admin"], False)
        self.assertEqual(len(bootstrap["terms"]), 6)
        self.assertGreaterEqual(bootstrap["total"], 3200)
        response = self.client.post("/api/terms", json={},
                                    headers={"X-CSRF-Token": bootstrap["csrf_token"]})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()["error"], "请先解锁维护模式后再修改词库。")


if __name__ == "__main__":
    unittest.main()
