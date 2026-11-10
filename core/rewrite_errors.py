"""Safe rewrite failure categories; never expose provider bodies or exceptions."""

import ssl
from urllib.error import HTTPError, URLError

_NOTICES = {
    "missing_key": "未配置 DeepSeek 密钥。",
    "invalid_config": "DeepSeek 服务配置有误，请检查服务地址与模型设置。",
    "auth_failed": "DeepSeek 密钥验证未通过，请检查密钥与访问权限。",
    "insufficient_balance": "DeepSeek 账户余额不足，请充值后重试。",
    "rate_limited": "DeepSeek 请求较多，请稍后重试。",
    "timeout": "DeepSeek 改写等待超过 25 秒，请稍后重试。",
    "tls_error": "无法与 DeepSeek 建立安全连接，请检查服务证书配置。",
    "network_error": "DeepSeek 连接失败，请检查网络后重试。",
    "service_unavailable": "DeepSeek 服务暂不可用，请稍后重试。",
    "invalid_response": "DeepSeek 改写结果格式异常，请重试。",
    "incomplete_response": "DeepSeek 改写结果未完成，请重试。",
    "incomplete_translation": "DeepSeek 英文改写尚未完整，请重试。",
    "factual_mismatch": "DeepSeek 改写中的价格、日期或其他数字与原稿不一致，请重试。",
}


class RewriteFailure(ValueError):
    """A failure already attributed to a safe, allowlisted category."""

    def __init__(self, code):
        self.code = code if code in _NOTICES else "invalid_response"
        super().__init__(self.code)


def failure_code(error):
    """Classify by exception/status without returning any raw error details."""
    if isinstance(error, RewriteFailure):
        return error.code
    if isinstance(error, HTTPError):
        if error.code in (401, 403):
            return "auth_failed"
        if error.code == 402:
            return "insufficient_balance"
        if error.code == 429:
            return "rate_limited"
        return "service_unavailable" if error.code >= 500 else "invalid_config"
    reason = error.reason if isinstance(error, URLError) else error
    # urllib commonly wraps the actual socket/TLS failure in URLError.reason.
    # Inspect only for classification; never render or log the string itself.
    detail = str(reason).casefold()
    if isinstance(reason, TimeoutError) or "timed out" in detail or "timeout" in detail:
        return "timeout"
    if (isinstance(reason, ssl.SSLError) or "certificate_verify_failed" in detail
            or "certificate verify failed" in detail or "[ssl:" in detail):
        return "tls_error"
    if isinstance(error, (URLError, OSError)):
        return "network_error"
    return "invalid_response"


def failure_notice(code):
    """Render only product copy associated with an allowlisted category."""
    return _NOTICES.get(code, _NOTICES["invalid_response"])
