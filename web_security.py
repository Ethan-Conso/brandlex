"""Small same-origin safeguards for the local BrandLex application."""

import secrets
import threading
import time
from collections import OrderedDict, deque
from urllib.parse import urlsplit

from flask import abort, jsonify, request, session


def csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


class RequestLimiter:
    """Bound memory and serialize concurrent requests; never trust forwarded IPs."""

    def __init__(self):
        self._buckets = OrderedDict()
        self._lock = threading.Lock()

    def allow(self, key, limit):
        now = time.monotonic()
        with self._lock:
            bucket = self._buckets.pop(key, deque())
            while bucket and bucket[0] <= now - 60:
                bucket.popleft()
            allowed = len(bucket) < limit
            if allowed:
                bucket.append(now)
            self._buckets[key] = bucket
            while len(self._buckets) > 4096:
                self._buckets.popitem(last=False)
            return allowed


def install_safeguards(app):
    limiter = RequestLimiter()
    app.extensions["request_limiter"] = limiter

    @app.before_request
    def protect_api():
        if not request.path.startswith("/api/"):
            return None
        if request.content_length and request.content_length > app.config["MAX_CONTENT_LENGTH"]:
            abort(413)
        if app.config["RATELIMIT_ENABLED"]:
            limit = app.config["API_RATE_LIMIT"]
            if request.endpoint == "admin_login":
                limit = min(limit, app.config["LOGIN_RATE_LIMIT"])
            elif request.endpoint == "rewrite_draft":
                limit = min(limit, app.config["REWRITE_RATE_LIMIT"])
            elif request.endpoint == "check_copy":
                limit = min(limit, app.config["CHECK_RATE_LIMIT"])
            elif request.method in {"POST", "PATCH", "DELETE"}:
                limit = min(limit, app.config["WRITE_RATE_LIMIT"])
            if not limiter.allow((request.remote_addr, request.endpoint), limit):
                response = jsonify(success=False, error="操作有点频繁，请稍等一分钟后再试。")
                response.status_code = 429
                response.headers["Retry-After"] = "60"
                return response
        if request.method not in {"POST", "PATCH", "DELETE"}:
            return None
        origin = request.headers.get("Origin")
        if origin:
            try:
                parsed = urlsplit(origin)
            except ValueError:
                abort(403)
            if (parsed.scheme, parsed.netloc) != (request.scheme, request.host):
                abort(403)
        if request.headers.get("Sec-Fetch-Site") == "cross-site":
            abort(403)
        expected = session.get("csrf_token")
        received = request.headers.get("X-CSRF-Token", "")
        if not expected or not secrets.compare_digest(expected.encode("utf-8"), received.encode("utf-8")):
            abort(403)
        return None

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "same-origin"
        connect_src = "'self' https://api.deepseek.com" if request.path == "/" else "'self'"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            f"img-src 'self' data:; font-src 'self'; connect-src {connect_src}; "
            "object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'self'"
        )
        if request.path.startswith("/api/") or request.path == "/":
            response.headers["Cache-Control"] = "no-store"
        return response
