"""Editorial matrices for the five original marketing categories.

The source files pair real channel, audience, and task labels with expressions
used in campaign briefs. Each recipe supplies its own editorial use case,
localized examples and a common mistake. A recipe only applies to a group
whose members support it.
"""

from data import (
    seed_marketing_commerce,
    seed_marketing_copy,
    seed_marketing_growth,
    seed_marketing_pr,
    seed_marketing_social,
)


def _rows(source, width):
    for line in source.strip().splitlines():
        if not line.strip():
            continue
        fields = tuple(value.strip() for value in line.split("|"))
        if len(fields) != width or not all(fields):
            raise ValueError(f"Invalid marketing editorial source row: {line!r}")
        yield fields


def matrix(category, topics, recipes):
    """Render a localized set of copy-ready term records from editorial rows."""
    for en, hk, cn, platform_tags, context_en, context_hk, context_cn, note in _rows(topics, 8):
        context = {
            "en": en,
            "hk": hk,
            "cn": cn,
            "context_en": context_en,
            "context_hk": context_hk,
            "context_cn": context_cn,
            "recap_en": en.removesuffix(" Event"),
            "recap_hk": hk.removesuffix("活動"),
            "recap_cn": cn.removesuffix("活动"),
        }
        for recipe in _rows(recipes, 10):
            term_en, term_hk, term_cn, alias, meaning, bad, good_en, good_hk, good_cn, tip = (
                field.format_map(context) for field in recipe
            )
            yield {
                "term_en": term_en, "term_hk": term_hk, "term_cn": term_cn,
                "aliases": [alias], "platforms": platform_tags.split(","),
                "category": category, "meaning": meaning, "bad_example": bad,
                "good_example_en": good_en, "good_example_hk": good_hk,
                "good_example_cn": good_cn, "usage_tip": f"{tip}{note}",
            }


def build_marketing_terms():
    """Return the additional marketing records in stable editorial order."""
    sources = (
        ("社媒与种草", seed_marketing_social),
        ("电商与转化", seed_marketing_commerce),
        ("投放与增长", seed_marketing_growth),
        ("公关与线下", seed_marketing_pr),
        ("文案与修辞", seed_marketing_copy),
    )
    return [
        term
        for category, source in sources
        for topics, recipes in source.BLOCKS
        for term in matrix(category, topics, recipes)
    ]
