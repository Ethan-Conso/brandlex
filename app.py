"""BrandLex's local Flask workspace and JSON API. Run with python app.py."""

import io
import json
import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_file, send_from_directory
from werkzeug.exceptions import HTTPException

from admin_auth import install_admin, is_admin
from core.ai_rewriter import rewrite_copy
from core.configuration import load_environment, session_secret
from core.copy_checker import MAX_COPY_LENGTH, analyze_copy
from core.db_manager import DBManager, SnapshotSyncError
from core.pages_assets import GENERATED_ASSETS, PUBLIC_SNAPSHOTS
from core.schema import CATEGORIES, TERM_FIELDS
from core.search_engine import FEED_BATCH_SIZE
from data.lexicon_domains import learning_tip
from web_security import csrf_token, install_safeguards

ROOT = Path(__file__).resolve().parent
DEFAULT_PAGE_SIZE = 60
SEARCH_PAGE_SIZE = 12
MAX_PAGE_SIZE = 200
MESSAGES = {
    400: "请检查填写的内容后重试。",
    403: "页面连接已更新，请刷新页面后重试。",
    404: "没有找到这条内容，请刷新词库后重试。",
    405: "暂时无法完成此操作，请刷新页面后重试。",
    413: "内容太长，请缩短后重试。",
    415: "请检查提交内容的格式后重试。",
    500: "暂时无法完成操作，请稍后重试。",
}
LABELS = {
    "term_en": "英文表达", "term_hk": "香港表达", "term_cn": "内地表达",
    "aliases": "别名", "category": "业务分类", "platforms": "适用平台",
    "meaning": "一句话解析", "bad_example": "踩坑写法",
    "good_example_en": "英文例句", "good_example_hk": "香港例句",
    "good_example_cn": "内地例句", "usage_tip": "跨区用词贴士",
}


def _payload():
    if not request.is_json:
        abort(400, description="请提交完整的填写内容后重试。")
    value = request.get_json()
    if not isinstance(value, dict):
        abort(400, description="请提交完整的填写内容后重试。")
    return value


def _term_error(error):
    """Translate validation details without exposing implementation field names."""
    message = str(error)
    labels = [label for field, label in LABELS.items() if field in message]
    if labels:
        return "请检查" + "、".join(f"「{label}」" for label in labels) + "，填写有效且完整的内容。"
    return "请填写完整的三语表达、分类、例句和用词贴士，并检查别名与适用平台。"


def _valid_term_id(term_id):
    if not 0 < term_id < 2**63:
        abort(404)


def _page_number(name, default, minimum):
    value = request.args.get(name, str(default))
    if len(value) > 19 or not value.isascii() or not value.isdecimal() or int(value) < minimum:
        abort(400, description="请选择有效的词库分页范围。")
    return int(value)


def _excluded_term_ids():
    raw = request.args.get("exclude", "")
    if not raw:
        return ()
    if len(raw) > MAX_PAGE_SIZE * 20 - 1:
        abort(400, description="请选择有效的案例编号。")
    values = raw.split(",")
    if len(values) > MAX_PAGE_SIZE or any(
        len(value) > 19 or not value.isascii() or not value.isdecimal() or not 0 < int(value) < 2**63
        for value in values
    ):
        abort(400, description="请选择有效的案例编号。")
    return tuple(map(int, values))


def _term_page(library, query="", category=None, offset=0, limit=DEFAULT_PAGE_SIZE, *, feed=False, exclude_ids=()):
    engine = library.get_search_engine()
    counts = engine.category_counts()
    if feed:
        records = engine.sample_feed(category, limit, exclude_ids)
        matched_total = counts.get(category, 0) if category else len(engine)
        offset = 0
    else:
        records, matched_total = engine.search_page(query, category, offset=offset, limit=limit)
    return {
        "terms": [
            {**{field: record[field] for field in TERM_FIELDS}, "learning_tip": learning_tip(record)}
            for record in records
        ],
        "total": len(engine), "matched_total": matched_total,
        "offset": offset, "limit": limit, "has_more": not feed and offset + len(records) < matched_total,
        "category_counts": {name: counts.get(name, 0) for name in CATEGORIES},
    }


def create_app(config=None):
    """Create an app for one library; tests may supply an isolated LIBRARY_DIR."""
    load_environment(ROOT / ".env")
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=session_secret(os.environ.get("BRANDLEX_SECRET_KEY")),
        ADMIN_PASSWORD=os.environ.get("BRANDLEX_ADMIN_PASSWORD") or "",
        ADMIN_SESSION_SECONDS=8 * 60 * 60,
        LIBRARY_DIR=os.environ.get("BRANDLEX_DATA_DIR") or ROOT / "data",
        MAX_CONTENT_LENGTH=192 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_COOKIE_SECURE=os.environ.get("BRANDLEX_HTTPS") == "1",
        RATELIMIT_ENABLED=True, API_RATE_LIMIT=300, CHECK_RATE_LIMIT=90,
        WRITE_RATE_LIMIT=60, LOGIN_RATE_LIMIT=5, REWRITE_RATE_LIMIT=10,
    )
    if config:
        app.config.update(config)
    app.json.ensure_ascii = False
    directory = Path(app.config["LIBRARY_DIR"]).resolve()
    library = DBManager(db_path=directory / "digilex.db", json_path=directory / "glossary.json", seed_path=directory / "glossary_seed.json")
    library.get_search_engine()
    app.extensions["library"] = library
    samples = json.loads((directory / "sample_drafts.json").read_text(encoding="utf-8"))
    install_admin(app)
    install_safeguards(app)
    _register_errors(app)
    _register_routes(app, library, samples)
    return app


def _register_errors(app):
    @app.errorhandler(HTTPException)
    def http_error(error):
        message = error.description if any("\u3400" <= char <= "\u9fff" for char in error.description) else MESSAGES.get(error.code, MESSAGES[500])
        return jsonify(success=False, error=message), error.code

    @app.errorhandler(SnapshotSyncError)
    def snapshot_error(error):
        app.logger.exception("Library saved but snapshot publication failed")
        return jsonify(success=False, saved=True, error="更改已保存，但词库备份暂时未能更新。请刷新页面确认更改。"), 503

    @app.errorhandler(sqlite3.Error)
    @app.errorhandler(OSError)
    def storage_error(error):
        app.logger.exception("Library operation failed")
        return jsonify(success=False, error="词库暂时无法读取或保存，请稍后重试。"), 503

    @app.errorhandler(Exception)
    def unexpected_error(error):
        app.logger.exception("Unexpected BrandLex request failure")
        return jsonify(success=False, error=MESSAGES[500]), 500


def _register_routes(app, library, samples):
    @app.get("/")
    def index():
        return render_template("index.html", csrf_token=csrf_token())

    @app.get("/favicon.ico")
    def favicon():
        return "", 204

    @app.get("/data/<filename>")
    def browser_engine_asset(filename):
        if filename in GENERATED_ASSETS:
            return jsonify(GENERATED_ASSETS[filename]())
        if filename in PUBLIC_SNAPSHOTS:
            return send_from_directory(ROOT / "data", filename)
        abort(404)

    @app.get("/api/bootstrap")
    def bootstrap():
        return jsonify(success=True, data={
            **_term_page(library, limit=FEED_BATCH_SIZE, feed=True), "categories": list(CATEGORIES), "samples": samples,
            "csrf_token": csrf_token(), "is_admin": is_admin(),
        })

    @app.get("/api/terms")
    def terms():
        query, category = request.args.get("q", ""), request.args.get("category") or None
        if len(query) > 500 or (category is not None and category not in CATEGORIES):
            abort(400, description="请缩短搜索内容或选择有效的业务分类。")
        query = query.strip()
        mode = request.args.get("mode")
        if mode not in (None, "feed"):
            abort(400, description="请选择有效的案例浏览方式。")
        pagination = "offset" in request.args or "limit" in request.args
        feed = not query and (mode == "feed" or "exclude" in request.args or not pagination)
        default_limit = FEED_BATCH_SIZE if feed else SEARCH_PAGE_SIZE if query else DEFAULT_PAGE_SIZE
        offset = _page_number("offset", 0, 0)
        limit = min(_page_number("limit", default_limit, 1), MAX_PAGE_SIZE)
        exclude_ids = _excluded_term_ids() if feed else ()
        return jsonify(success=True, data=_term_page(
            library, query, category, offset, limit, feed=feed, exclude_ids=exclude_ids,
        ))

    @app.get("/api/terms/<int:term_id>")
    def get_term(term_id):
        _valid_term_id(term_id)
        record = library.get_term(term_id)
        if record is None:
            abort(404)
        return jsonify(success=True, data=record)

    @app.post("/api/terms")
    def add_term():
        payload = _payload()
        try:
            record = library.add_term(payload)
        except ValueError as error:
            abort(400, description=_term_error(error))
        return jsonify(success=True, data=record), 201

    @app.patch("/api/terms/<int:term_id>")
    def edit_term(term_id):
        _valid_term_id(term_id)
        payload = _payload()
        try:
            record = library.update_term(term_id, payload)
        except ValueError as error:
            abort(400, description=_term_error(error))
        except KeyError:
            abort(404)
        return jsonify(success=True, data=record)

    @app.delete("/api/terms/<int:term_id>")
    def delete_term(term_id):
        _valid_term_id(term_id)
        if not library.delete_term(term_id):
            abort(404)
        return jsonify(success=True, data={"id": term_id})

    @app.post("/api/library/reset")
    def reset_library():
        payload = _payload()
        if set(payload) != {"confirm"} or payload["confirm"] is not True:
            abort(400, description="请确认恢复默认词库后再继续。")
        library.reset_to_defaults()
        return jsonify(success=True, data=_term_page(library))

    @app.post("/api/check")
    def check_copy():
        payload = _payload()
        text, market = payload.get("text"), payload.get("target_market")
        if set(payload) != {"text", "target_market"} or not isinstance(text, str):
            abort(400, description="请填写文案并选择目标市场。")
        if not isinstance(market, str) or market not in {"hk", "cn", "en"}:
            abort(400, description="请选择香港、内地或英语市场。")
        if len(text) > MAX_COPY_LENGTH:
            abort(400, description="文案太长，请缩短至 20,000 字以内后重试。")
        try:
            text.encode("utf-8")
        except UnicodeError:
            abort(400, description="文案含有无法识别的字符，请重新粘贴后重试。")
        report = analyze_copy(text, market, library.get_search_engine())
        return jsonify(success=True, data=report)

    @app.get("/api/export/<format>")
    def export_library(format):
        formats = {"csv": "text/csv", "tbx": "application/xml", "json": "application/json"}
        if format not in formats:
            abort(400, description="请选择 Excel CSV、TBX 或 JSON 导出格式。")
        try:
            content = library.export(format)
        except ValueError:
            abort(400, description="请先添加至少一条词条，再导出词库。")
        return send_file(io.BytesIO(content), mimetype=formats[format], as_attachment=True, download_name=f"BrandLex-Library.{format}")

    @app.post("/api/rewrite")
    def rewrite_draft():
        payload = _payload()
        text, market, tone = payload.get("text"), payload.get("target_market"), payload.get("tone")
        if set(payload) != {"text", "target_market", "tone"} or not isinstance(text, str) or not text.strip():
            abort(400, description="请输入原稿并选择市场和风格。")
        if not isinstance(market, str) or market not in {"hk", "cn", "en"}:
            abort(400, description="请选择香港、内地或英语市场。")
        if not isinstance(tone, str) or tone not in {"standard", "social", "concise"}:
            abort(400, description="请选择品牌标准、社媒种草或精炼转化。")
        if len(text) > MAX_COPY_LENGTH:
            abort(400, description="文案太长，请缩短至 20,000 字以内后重试。")
        try:
            text.encode("utf-8")
        except UnicodeError:
            abort(400, description="文案含有无法识别的字符，请重新粘贴后重试。")
        try:
            report = rewrite_copy(text, market, tone, library.get_search_engine())
        except (ValueError, TypeError):
            abort(400, description="请检查原稿中的字符，并重新选择市场和风格。")
        return jsonify(success=True, data=report)


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=int(os.environ.get("PORT", "5062")), debug=False, load_dotenv=False)
