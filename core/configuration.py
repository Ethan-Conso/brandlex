"""Small, non-executing local configuration loader. Never writes .env."""

import os
import re
import secrets
from pathlib import Path

ENV_KEYS = frozenset({
    "DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL",
    "BRANDLEX_ADMIN_PASSWORD", "BRANDLEX_SECRET_KEY", "BRANDLEX_DATA_DIR", "BRANDLEX_HTTPS", "PORT",
})
UNSAFE_SESSION_KEYS = frozenset({"brandlex-production-secret-key-2026", "your_secret_key_here"})


def _value(raw):
    raw = raw.strip()
    if raw.startswith(("'", '"')):
        quote = raw[0]
        match = re.fullmatch(r"(['\"])((?:\\.|[^\\])*?)\1\s*(?:#.*)?", raw)
        if not match:
            return None
        value = match[2]
        if quote == '"':
            replacements = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}
            value = re.sub(r'\\([nrt"\\])', lambda item: replacements[item[1]], value)
        return value
    return re.split(r"\s+#", raw, maxsplit=1)[0].strip()


def load_environment(path):
    """Allowlisted dotenv assignments; process environment always takes priority."""
    path = Path(path)
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[7:].lstrip()
        name, separator, raw = line.partition("=")
        name = name.strip()
        if separator and name in ENV_KEYS:
            value = _value(raw)
            if value is not None:
                os.environ.setdefault(name, value)


def session_secret(value):
    """Publicly documented sample signing keys cannot protect admin cookies."""
    if not value or len(value) < 32 or value in UNSAFE_SESSION_KEYS:
        return secrets.token_hex(32)
    return value
