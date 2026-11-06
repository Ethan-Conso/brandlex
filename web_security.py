"""Small same-origin safeguards for the local BrandLex application."""

import secrets
import threading
import time
from collections import OrderedDict, deque
from ipaddress import ip_address
from urllib.parse import urlsplit

from flask import abort, jsonify, request, session


def csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


class RequestLimiter:
    """Bound memory and serialize concurrent quota checks."""

    def __init__(self, window_seconds=60):
        self._window_seconds = window_seconds
        self._buckets = OrderedDict()
        self._lock = threading.Lock()

    def allow(self, key, limit):
        now = time.monotonic()
        with self._lock:
            bucket = self._buckets.pop(key, deque())
            while bucket and bucket[0] <= now - self._window_seconds:
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
                return _rate_limit_response(60, "操作有点频繁，请稍等一分钟后再试。")
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

    _install_response_headers(app)


def _rate_limit_response(seconds, message):
    response = jsonify(success=False, error=message)
    response.status_code = 429
    response.headers["Retry-After"] = str(seconds)
    return response


def _relay_client_address(trust_cloudflare):
    if trust_cloudflare:
        # Only enable where the public edge overwrites this header (e.g. Render).
        try:
            return str(ip_address(request.headers.get("CF-Connecting-IP", "")))
        except ValueError:
            pass
    return request.remote_addr


def install_pages_safeguards(app):
    """Isolate the public, cookie-free route and bound paid calls per process."""
    per_ip = RequestLimiter()
    daily_window = 24 * 60 * 60
    daily = RequestLimiter(window_seconds=daily_window)
    origin = app.config["PAGES_ORIGIN"]
    _install_response_headers(app)

    @app.before_request
    def protect_relay():
        if request.endpoint != "pages_rewrite":
            return None
        if not origin:
            abort(503, description="在线改写尚未配置。")
        if request.headers.get("Origin") != origin:
            abort(403)
        if request.method == "OPTIONS":
            headers = request.headers.get("Access-Control-Request-Headers", "")
            requested = {header.strip().lower() for header in headers.split(",") if header.strip()}
            if request.headers.get("Access-Control-Request-Method") != "POST" or requested - {"content-type", "accept"}:
                abort(403)
            return None
        address = _relay_client_address(app.config["PAGES_TRUST_CLOUDFLARE"])
        if not per_ip.allow(address, app.config["PAGES_IP_RATE_LIMIT"]):
            return _rate_limit_response(60, "改写有点频繁，请稍等一分钟后再试。")
        return None

    @app.after_request
    def allow_pages_origin(response):
        if request.endpoint == "pages_rewrite":
            response.vary.add("Origin")
            if origin and request.headers.get("Origin") == origin:
                response.headers["Access-Control-Allow-Origin"] = origin
            if request.method == "OPTIONS":
                response.vary.update(("Access-Control-Request-Method", "Access-Control-Request-Headers"))
                if response.status_code == 204:
                    response.headers["Access-Control-Allow-Methods"] = "POST"
                    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
        return response

    def reserve_call():
        # Keep one independent global bucket, so rotating IPs cannot evict it.
        if not daily.allow("global", app.config["PAGES_DAILY_LIMIT"]):
            return _rate_limit_response(daily_window, "今日公共改写额度已用完，请稍后再试。")
        return None

    return reserve_call


def _install_response_headers(app):
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
