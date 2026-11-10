"""Shared, dependency-free validation for the BrandLex term format."""

import re
import unicodedata
from collections.abc import Mapping

CATEGORIES = (
    "社媒与种草", "电商与转化", "投放与增长",
    "公关与线下", "文案与修辞",
    "美妆与个护", "时尚与奢品", "数码与科技",
    "餐饮与酒水", "文旅与酒店", "金融与支付", "合规与风控",
)
TEXT_FIELDS = (
    "term_en", "term_hk", "term_cn", "category", "meaning", "bad_example",
    "good_example_en", "good_example_hk", "good_example_cn", "usage_tip",
)
LIST_FIELDS = ("aliases", "platforms")
TERM_FIELDS = ("id", *TEXT_FIELDS[:3], "aliases", "category", "platforms", *TEXT_FIELDS[4:])
_HAN = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U000323af]")


class BilingualMeaningError(ValueError):
    """A term is missing one or both languages in its definition."""

    def __init__(self):
        super().__init__("请按「中文释义 EN: English definition」格式填写中英文释义。")


def validate_identifier(value):
    """Require a positive integer, excluding bool and SQL-like text."""
    if isinstance(value, bool) or not isinstance(value, int) or not 0 < value < 2**63:
        raise ValueError("Term ID must be a positive whole number.")
    return value


def _text(value, field, limit=6000):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{field} must contain between 1 and {limit} characters.")
    if any((unicodedata.category(char) in ("Cc", "Cs") and char not in "\n\r\t")
           or char in "\ufffe\uffff" for char in value):
        raise ValueError(f"{field} contains unsupported characters.")
    return value.strip()


def _bilingual_meaning(value):
    if not isinstance(value, str) or not value.strip():
        raise BilingualMeaningError()
    parts = re.split(r"(?<=\s)EN:", _text(value, "meaning"), maxsplit=1)
    if len(parts) != 2 or not _HAN.search(parts[0]) or not re.search(r"\b(?!EN:)[A-Za-z]{2,}\b", parts[1], re.ASCII):
        raise BilingualMeaningError()
    return _text(f"{parts[0].strip()} EN: {parts[1].strip()}", "meaning")


def validate_term(record, *, require_id=False, allow_metadata=False, require_bilingual=True):
    """Return a validated copy; never change caller-owned objects."""
    if not isinstance(record, Mapping):
        raise ValueError("A term must be an object containing the required fields.")
    allowed = set(TERM_FIELDS) | ({"updated_at"} if allow_metadata else set())
    unknown = set(record) - allowed
    if unknown:
        raise ValueError("Unknown term fields: " + ", ".join(sorted(map(str, unknown))))
    required = set(TEXT_FIELDS) | set(LIST_FIELDS) | ({"id"} if require_id else set())
    missing = required - set(record)
    if missing:
        if require_bilingual and missing == {"meaning"}:
            raise BilingualMeaningError()
        raise ValueError("Missing term fields: " + ", ".join(sorted(missing)))
    result = {field: _bilingual_meaning(record[field]) if require_bilingual and field == "meaning"
              else _text(record[field], field) for field in TEXT_FIELDS}
    if result["category"] not in CATEGORIES:
        raise ValueError("Choose a valid category.")
    for field in LIST_FIELDS:
        values = record[field]
        if not isinstance(values, list) or not values or len(values) > 50:
            raise ValueError(f"{field} must contain between 1 and 50 text items.")
        result[field] = list(dict.fromkeys(_text(value, field, 200) for value in values))
    if "id" in record:
        result["id"] = validate_identifier(record["id"])
    if "updated_at" in record and allow_metadata:
        result["updated_at"] = _text(record["updated_at"], "updated_at", 80)
    return result
