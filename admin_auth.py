"""Session-scoped maintenance permissions for a shared brand library."""

import hashlib
import hmac
import time

from flask import abort, current_app, jsonify, request, session

from web_security import csrf_token

LOCKED_MESSAGE = "请先解锁维护模式后再修改词库。"
LIBRARY_WRITES = frozenset({"add_term", "edit_term", "delete_term", "reset_library"})


def _fingerprint():
    password = current_app.config.get("ADMIN_PASSWORD") or ""
    secret = current_app.secret_key
    key = secret.encode("utf-8") if isinstance(secret, str) else secret
    return hmac.new(key, password.encode("utf-8"), hashlib.sha256).hexdigest()


def is_admin():
    issued = session.get("admin_issued")
    signature = session.get("admin_signature")
    if not current_app.config.get("ADMIN_PASSWORD") or not isinstance(issued, (int, float)):
        return False
    if not 0 <= time.time() - issued < current_app.config["ADMIN_SESSION_SECONDS"]:
        return False
    return isinstance(signature, str) and hmac.compare_digest(signature, _fingerprint())


def install_admin(app):
    @app.before_request
    def require_maintenance():
        if request.endpoint in LIBRARY_WRITES and not is_admin():
            abort(403, description=LOCKED_MESSAGE)

    @app.post("/api/admin/login")
    def admin_login():
        session.pop("admin_signature", None)
        session.pop("admin_issued", None)
        payload = request.get_json(silent=True) if request.is_json else None
        if not isinstance(payload, dict) or set(payload) != {"password"}:
            abort(400, description="请输入维护口令。")
        password = payload["password"]
        if not isinstance(password, str) or not password or len(password) > 1024:
            abort(400, description="请输入有效的维护口令。")
        try:
            candidate = hashlib.sha256(password.encode("utf-8")).digest()
        except UnicodeError:
            abort(400, description="请输入有效的维护口令。")
        expected = app.config.get("ADMIN_PASSWORD")
        if not expected:
            abort(503, description="维护口令尚未配置，请联系词库维护者。")
        if not hmac.compare_digest(candidate, hashlib.sha256(expected.encode("utf-8")).digest()):
            abort(401, description="维护口令不正确。")
        session.clear()
        session.update(admin_issued=time.time(), admin_signature=_fingerprint())
        return jsonify(success=True, data={"is_admin": True, "csrf_token": csrf_token()})

    @app.post("/api/admin/logout")
    def admin_logout():
        payload = request.get_json(silent=True) if request.is_json else None
        if payload != {}:
            abort(400, description="请刷新页面后退出维护模式。")
        session.clear()
        return jsonify(success=True, data={"is_admin": False, "csrf_token": csrf_token()})
