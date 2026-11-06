"""Local, deterministic copy feedback for BrandLex.

``analyze_copy(text, target_market, glossary=None)`` returns JSON-ready feedback:
score/readiness_score (0–100), suggestions, cta_suggestions, cta_strength,
word_count, character_count, paragraph_count, reading_time_seconds, readability,
warnings and matched_glossary_terms. Counts are also grouped under ``counts``.
Chinese characters count as individual reading units; English words count as
words. Character count excludes whitespace. Reading time is an estimate.

Every replacement has original_span, suggested_replacement, start/end, reason,
category and id. Offsets are Python Unicode code points into the exact input,
not UTF-16 positions. A browser can slice ``Array.from(text)`` or use
``apply_suggestion`` server-side. CTA insertions use start=end=len(text).
Re-run analysis after every edit: offsets belong to that version of the draft.
Suggestions are editorial guidance, not a complete translation or a guarantee
of marketing performance. Drafts are never sent to an external service.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence

from core.copy_rules import RULES
from core.search_engine import SearchEngine, match_glossary_terms

MAX_COPY_LENGTH = 20_000
_COMPILED_RULES = tuple((rule, re.compile(rule.pattern, re.IGNORECASE)) for rule in RULES)
_CJK = re.compile(r"[\u3400-\u9fff]")
_WORDS = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")
# Deliberately excludes shared characters such as 后, 里, 台 and 干. This is a
# conservative warning, not script conversion or a complete writing-system test.
_SIMPLIFIED_DISTINCTIVE = frozenset("这为与发选购预订优运费肤亲温适湿润质实测联赠减满开关广务户号礼鸟场现")
_TRADITIONAL_DISTINCTIVE = frozenset("這為與發選購預訂優運費膚親溫適濕潤質實測聯贈減滿開關廣務戶號禮鳥場現")
_STRONG_CTA = {
    "hk": r"立即(?:入手|選購|購買|登記|預訂|報名)|按(?:此|連結)(?:選購|購買|登記|了解)|私訊(?:我們|查詢)|了解更多|即刻(?:選購|登記)",
    "cn": r"立即(?:购买|选购|下单|报名|预约|预订)|点击(?:链接|这里)[，,\s]*(?:购买|下单|报名|了解|查看)|私信(?:我们|咨询)|了解更多|马上(?:购买|下单)",
    "en": r"\b(?:shop now|shop via the link|buy now|order now|sign up|register now|book now|pre-order now|discover more|learn more|get started|subscribe now|reserve your (?:place|spot)|send us a message)\b",
}
_WEAK_CTA = {
    "hk": r"[點点][擊击]這[裡里]|[點点]此|歡迎[選选][購购]|快[來来]看看|不容錯過",
    "cn": r"点这里|点此|欢迎选购|快来看看|不容错过",
    "en": r"\b(?:click here|check it out|welcome to buy|don't miss out)\b",
}
_CTA_ENDINGS = {
    "hk": ("按連結選購，查看產品詳情。", "私訊我們，了解適合你的選擇。", "立即登記，接收最新活動消息。"),
    "cn": ("点击链接，查看产品详情并选购。", "私信我们，了解适合你的选择。", "立即报名，获取最新活动消息。"),
    "en": ("Shop now and find your favourite.", "Discover more via the link.", "Send us a message to find out more."),
}


def _validate_input(text: str, target_market: str) -> None:
    if not isinstance(text, str):
        raise TypeError("文案必须是文字。")
    if target_market not in ("hk", "cn", "en"):
        raise ValueError("请选择香港、内地或英语市场。")
    if len(text) > MAX_COPY_LENGTH:
        raise ValueError(f"文案过长，请缩短至 {MAX_COPY_LENGTH:,} 字以内后重试。")


def _replacement_suggestions(text: str, target_market: str) -> list[dict]:
    candidates = [
        {"id": f"{rule.id}-{match.start()}-{match.end()}",
         "start": match.start(), "end": match.end(),
         "original_span": match.group(), "suggested_replacement": rule.replacement,
         "reason": rule.reason, "category": rule.category}
        for rule, pattern in _COMPILED_RULES if rule.market == target_market
        for match in pattern.finditer(text)
        if match.group() != rule.replacement
    ]
    # Keep the longest expression at a position; one click must never partially
    # overwrite another suggestion. Literal phrases win ties over shorter words.
    ordered = sorted(candidates, key=lambda item: (
        item["start"], -(item["end"] - item["start"]), item["id"]))
    selected = []
    previous_end = -1
    for item in ordered:
        if item["start"] >= previous_end:
            selected.append(item)
            previous_end = item["end"]
    return selected


def _not_negated(text: str, start: int) -> bool:
    prefix = text[max(0, start - 40):start]
    negative = (
        r"(?:don['’]t|(?:do|does|did|should|would|could|must|can|may|might|need)\s+not|"
        r"(?:should|would|could|must|can|does|did)n['’]t|cannot|never|no need to|not ready to|"
        r"(?:不要|请勿|請勿|勿|不必)(?:现在|現在|马上|馬上)?)\s*$"
    )
    return not re.search(negative, prefix, re.IGNORECASE)


def _cta_feedback(text: str, market: str) -> tuple[str, list[dict]]:
    # A trailing URL, hashtag or punctuation should not hide the actual ending.
    content = re.sub(r"https?://\S+|#[\w\u3400-\u9fff]+", "", text).rstrip()
    meaningful_parts = [part for part in re.finditer(r"[^.!?。！？\n]+", content)
                        if _CJK.search(part.group()) or _WORDS.search(part.group())]
    end_start = meaningful_parts[-1].start() if meaningful_parts else len(content)
    actions = [match for match in re.finditer(_STRONG_CTA[market], content, re.IGNORECASE)
               if _not_negated(content, match.start())]
    if any(match.start() >= end_start for match in actions):
        return "strong", []
    weak_actions = [match for match in re.finditer(_WEAK_CTA[market], content, re.IGNORECASE)
                    if _not_negated(content, match.start())]
    strength = "weak" if actions or weak_actions else "missing"
    reason = ("结尾可加一句清楚的行动引导，请按实际购买或报名入口选用。"
              if strength == "missing" else
              "把明确的行动引导放到结尾，并确认入口可用。")
    suggestions = [
        {"id": f"cta-{market}-{index}", "start": len(text), "end": len(text),
         "original_span": "", "suggested_replacement": ("\n\n" if text.strip() else "") + ending,
         "reason": reason, "category": "行动号召"}
        for index, ending in enumerate(_CTA_ENDINGS[market], 1)
    ]
    return strength, suggestions


def _counts(text: str) -> dict:
    cjk_count = len(_CJK.findall(text))
    latin_count = len(_WORDS.findall(text))
    reading_seconds = cjk_count * 60 / 400 + latin_count * 60 / 220
    return {
        "word_count": cjk_count + latin_count,
        "character_count": sum(not char.isspace() for char in text),
        "paragraph_count": len([part for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]),
        "reading_time_seconds": math.ceil(reading_seconds),
    }


def _readability(text: str, market: str) -> dict:
    sentences = re.split(r"[.!?。！？\n]+", text)
    long_count = sum((len(_WORDS.findall(sentence)) > 30 if market == "en"
                      else len(_CJK.findall(sentence)) + len(_WORDS.findall(sentence)) > 55)
                     for sentence in sentences)
    return {
        "label": "建议拆短句" if long_count else "易于浏览",
        "long_sentence_count": long_count,
        "tips": ["把长句拆成两句，优先展示一个卖点，再交代优惠或下一步。"] if long_count else [],
    }


def _language_feedback(text: str, market: str) -> tuple[list[str], int]:
    cjk_count = len(_CJK.findall(text))
    letter_count = len(re.findall(r"[A-Za-z]", text))
    if market == "en" and cjk_count >= 4:
        dominant_chinese = cjk_count > letter_count
        return (["正文仍有中文，请先改写成自然英文；当前建议仅覆盖已识别的表达。"],
                50 if dominant_chinese else 15)
    characters = frozenset(text)
    if market == "hk" and len(characters & _SIMPLIFIED_DISTINCTIVE) >= 2:
        return ["正文仍有简体字，发往香港前请核对繁体写法和当地表达；当前建议未覆盖全文转换。"], 10
    if market == "cn" and len(characters & _TRADITIONAL_DISTINCTIVE) >= 2:
        return ["正文仍有繁体字，发往内地前请核对简体写法和平台语气；当前建议未覆盖全文转换。"], 10
    return [], 0


def analyze_copy(text: str, target_market: str, glossary: Sequence[Mapping] | SearchEngine | None = None) -> dict:
    """Check an exact draft without changing it or storing its contents.

    ``glossary=None`` reads the current library on each call, so user edits and
    deletions are reflected immediately. Pass a sequence or a cached index.
    """
    _validate_input(text, target_market)
    if glossary is None:
        from core.db_manager import DBManager
        glossary = DBManager().get_search_engine()
    suggestions = _replacement_suggestions(text, target_market)
    cta_strength, cta_suggestions = _cta_feedback(text, target_market)
    counts = _counts(text)
    readability = _readability(text, target_market)
    warnings, language_penalty = _language_feedback(text, target_market)
    distinct_issues = len({item["id"].rsplit("-", 2)[0] for item in suggestions})
    penalty = (min(60, distinct_issues * 7) + {"strong": 0, "weak": 9, "missing": 18}[cta_strength]
               + min(12, readability["long_sentence_count"] * 4) + language_penalty)
    score = max(0, 100 - penalty) if counts["word_count"] else 0
    return {
        "target_market": target_market, "score": score, "readiness_score": score,
        "suggestions": suggestions, "cta_suggestions": cta_suggestions,
        "cta_strength": cta_strength, "counts": counts, **counts,
        "readability": readability, "warnings": warnings,
        "matched_glossary_terms": match_glossary_terms(text, glossary),
    }


def apply_suggestion(text: str, suggestion: Mapping) -> str:
    """Apply one exact suggestion, rejecting stale offsets instead of corrupting copy."""
    if not isinstance(text, str) or not isinstance(suggestion, Mapping):
        raise TypeError("请提供文案和有效的修改建议。")
    start, end = suggestion.get("start"), suggestion.get("end")
    original = suggestion.get("original_span")
    replacement = suggestion.get("suggested_replacement")
    if (type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(text)
            or not isinstance(original, str) or not isinstance(replacement, str)):
        raise ValueError("修改建议无效，请重新检查文案。")
    if text[start:end] != original:
        raise ValueError("文案已更改，请重新检查后再应用建议。")
    return text[:start] + replacement + text[end:]
