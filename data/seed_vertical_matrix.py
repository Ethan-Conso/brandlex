"""Render explicitly selected attribute and product combinations.

Each family supplies edited expressions and claim guidance, plus examples
written for its specific product forms. A row opts in to named forms so the
catalogue never invents an attribute/product pairing to fill a quota.
"""

import re


_EN_WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")
_LATIN_CJK = re.compile(r"(?<=[A-Za-z])(?=[\u3400-\u9fff])|(?<=[\u3400-\u9fff])(?=[A-Za-z])")
_PROPER_NAMES = frozenset({"Asscher", "Bluetooth", "Matter", "Wi", "Fi"})


def _in_sentence(value):
    def lowercase(match):
        word = match[0]
        return word if word in _PROPER_NAMES or word.isupper() else word.lower()

    return _EN_WORD.sub(lowercase, value)


def _rows(source):
    for line in source.strip().splitlines():
        if line.strip():
            yield tuple(field.strip() for field in line.split("|"))


def _record(category, platforms, en, hk, cn, aliases, meaning, bad, examples, tip):
    return {
        "term_en": en,
        "term_hk": hk,
        "term_cn": cn,
        "aliases": list(dict.fromkeys(aliases)),
        "category": category,
        "platforms": list(platforms),
        "meaning": meaning,
        "bad_example": bad,
        "good_example_en": examples[0],
        "good_example_hk": examples[1],
        "good_example_cn": examples[2],
        "usage_tip": tip,
    }


def editorial_terms(category, platforms, source):
    for en, hk, cn, aliases, meaning, bad, ex_en, ex_hk, ex_cn, tip in _rows(source):
        yield _record(category, platforms, en, hk, cn, aliases.split(";"),
                      meaning, bad, (ex_en, ex_hk, ex_cn), tip)


def matrix_terms(category, platforms, attributes, forms):
    variants = {key: values for key, *values in _rows(forms)}
    for en, hk, cn, alternate, meaning, bad, tip, available in _rows(attributes):
        for key in available.split():
            yield _combination(category, platforms, (en, hk, cn, alternate, meaning, bad, tip),
                               variants[key])


def _combination(category, platforms, attribute, form):
    en, hk, cn, alternate, meaning, bad, tip = attribute
    name_en, name_hk, name_cn, context, ex_en, ex_hk, ex_cn, product_tip = form
    term_en = name_en.format(en)
    term_hk = _LATIN_CJK.sub(" ", name_hk.format(hk))
    term_cn = _LATIN_CJK.sub(" ", name_cn.format(cn))
    alias = name_en.format(alternate).replace("-", " ")
    return _record(category, platforms, term_en, term_hk, term_cn, [alias],
                   f"「{term_cn}」常见于{context}的介绍。{meaning}", bad.format(term_cn),
                   (ex_en.format(_in_sentence(term_en)),
                    _LATIN_CJK.sub(" ", ex_hk.format(term_hk)),
                    _LATIN_CJK.sub(" ", ex_cn.format(term_cn))),
                   f"写「{term_cn}」时，{tip}{product_tip}")
