"""Editorial matrices for payment copy and evidence-led marketing disclosures."""

from data.seed_compliance_examples import COMPLIANCE_ANCHORS, COMPLIANCE_MATRICES
from data.seed_finance_examples import FINANCE_ANCHORS, FINANCE_MATRICES

_FIELDS = ("term_en", "term_hk", "term_cn", "meaning", "bad_example",
           "good_example_en", "good_example_hk", "good_example_cn", "usage_tip")


def _rows(source):
    for line in source.strip().splitlines():
        if line.strip():
            yield tuple(field.strip() for field in line.split("|"))


def _record(category, platforms, fields, aliases):
    values = tuple(fields)
    if len(values) != len(_FIELDS):
        raise ValueError("Mismatched seed fields.")
    return {
        **dict(zip(_FIELDS, values)),
        "category": category,
        "platforms": list(platforms),
        "aliases": aliases.split(";"),
    }


def _matrix_terms(category, contexts, facets, platforms):
    for en, hk, cn, scope in _rows(contexts):
        substitutions = {"en": en, "english": en.lower(), "hk": hk, "cn": cn, "scope": scope}
        for *fields, aliases in _rows(facets):
            yield _record(category, platforms,
                          (field.format_map(substitutions) for field in fields),
                          aliases.format_map(substitutions))


def build_finance_compliance_terms():
    """Yield new records in source order, with IDs assigned by the seed builder."""
    for category, anchors, matrices, platforms in (
        ("金融与支付", FINANCE_ANCHORS, FINANCE_MATRICES, ("银行 App", "官網")),
        ("合规与风控", COMPLIANCE_ANCHORS, COMPLIANCE_MATRICES, ("官网", "微信")),
    ):
        for *fields, aliases in _rows(anchors):
            yield _record(category, platforms, fields, aliases)
        for contexts, facets, matrix_platforms in matrices:
            yield from _matrix_terms(category, contexts, facets, matrix_platforms)
