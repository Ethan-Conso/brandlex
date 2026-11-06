"""Assemble the original flagship terms and the V3 editorial matrices."""

import re
from collections import Counter
from itertools import chain
from unicodedata import normalize

from core.schema import CATEGORIES, validate_term
from data.learning_anchor_copy import ANCHOR_EXAMPLES
from data.lexicon_domains import polish_generated_terms
from data.seed_beauty_fashion_tech import build_beauty_fashion_tech_terms
from data.seed_finance_compliance import build_finance_compliance_terms
from data.seed_food_travel import build_food_travel_terms
from data.seed_marketing import build_marketing_terms
from data.seed_terms import build_seed_terms


def _with_anchor_examples(record):
    examples = ANCHOR_EXAMPLES.get(record["term_en"])
    if examples is None:
        return record
    fields = ("good_example_en", "good_example_hk", "good_example_cn")
    if len(examples) != len(fields):
        raise ValueError("Mismatched anchor examples.")
    return {**record, **dict(zip(fields, examples))}


def build_default_library():
    flagships = build_seed_terms()
    additions = chain(
        build_marketing_terms(), build_beauty_fashion_tech_terms(),
        build_food_travel_terms(), build_finance_compliance_terms(),
    )
    polished = polish_generated_terms(additions, reserved=flagships)
    terms = [*flagships, *(
        validate_term({**_with_anchor_examples(record), "id": identifier}, require_id=True)
        for identifier, record in enumerate(polished, len(flagships) + 1)
    )]
    counts = Counter(term["category"] for term in terms)
    if len(terms) < 3200 or any(not 260 <= counts[category] <= 280 for category in CATEGORIES):
        raise ValueError(f"The default library is incomplete: {counts}")
    english = Counter(normalize("NFKC", term["term_en"]).casefold() for term in terms)
    duplicates = [name for name, count in english.items() if count > 1]
    if duplicates:
        raise ValueError("Duplicate English expressions: " + ", ".join(duplicates))
    for term in terms[len(flagships):]:
        if any(re.search(r"\d", term[field]) for field in ("term_en", "term_hk", "term_cn")):
            raise ValueError(f"Numbered expression in generated library: {term['term_en']}")
    return terms
