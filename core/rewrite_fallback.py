"""Honest local previews when the external rewriting service is unavailable."""

import re

from core.chinese_converter import convert_script
from core.rewrite_grounding import apply_constraints

_CTA = {
    "hk": ("了解產品詳情，選擇適合你的款式。", "私訊查詢，了解更多。"),
    "cn": ("了解产品详情，找到适合自己的选择。", "欢迎私信咨询更多详情。"),
    "en": ("Explore the details and find your fit.", "Get in touch to learn more."),
}
_EVENT_CTA = {
    "hk": ("查看活動詳情，安排你的行程。", "私訊查詢活動安排。"),
    "cn": ("查看活动详情，安排你的行程。", "私信了解活动安排。"),
    "en": ("Explore the event details and plan your visit.", "Get in touch for event information."),
}
# Conservative phrase edits only: no prices, dates, benefits or offers are added.
_EN_PHRASES = (
    (r"新品(?:即将)?上市|全新产品(?:即将)?推出", "A new product is on the way"),
    (r"欢迎选购|立即选购|立即购买|立即入手", "Explore the collection"),
    (r"了解更多|了解详情|了解詳情", "Learn more"),
)


def cta_options(text, market):
    event = re.search(r"活動|活动|快閃|快闪|限定店|pop.up|event|café|咖啡", text, re.IGNORECASE)
    return list((_EVENT_CTA if event else _CTA)[market])


def _style_segment(text, market, tone):
    cleaned = re.sub(r"[ \t]+", " ", text)
    if tone == "social":
        # Line breaks make an existing draft easier to scan without new claims.
        chinese = re.sub(r"([。！？])\s*(?=[^\s。！？])", r"\1\n\n", cleaned)
        return re.sub(r"([!?]|\.(?!\d))\s+(?=[A-Za-z])", r"\1\n\n", chinese)
    if tone == "concise":
        return re.sub(r"(?:，|(?<!\d),|,(?!\d))\s*", "\n", cleaned)
    return cleaned


def _preview_style(text, market, tone):
    parts = re.split(r"(https?://[^\s<>\"，。！？；]+)", text, flags=re.IGNORECASE)
    return "".join(part if index % 2 else _style_segment(part, market, tone)
                   for index, part in enumerate(parts)).strip()


def _english_preview(text):
    parts = re.split(r"(https?://[^\s<>\"，。！？；]+)", text, flags=re.IGNORECASE)
    def translate_prose(value):
        for pattern, replacement in _EN_PHRASES:
            value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
        return value
    return "".join(part if index % 2 else translate_prose(part)
                   for index, part in enumerate(parts))


def local_preview(text, market, tone, constraints):
    adapted = apply_constraints(text, constraints, market)
    if market == "en":
        adapted = _english_preview(adapted)
    normalized = convert_script(adapted, market)
    primary = _preview_style(normalized, market, tone)
    # The alternative is a conservative first-paragraph version, never a claim
    # that local rules can recreate a native speaker's complete creative rewrite.
    alt = _preview_style(normalized, market, "concise" if tone != "concise" else "social")
    notice = "当前为本地预览：已应用词库与繁简转换，完整改写需连接改写服务。"
    if market == "en" and re.search(r"[\u3400-\u9fff]", primary):
        notice = "当前为本地预览：仅调整已识别的英文表达，余下中文尚未翻译；完整英文改写需连接改写服务。"
    return {"primary_copy": primary, "alt_copy": alt, "adaptations": [],
            "cta_options": cta_options(text, market), "notice": notice}
