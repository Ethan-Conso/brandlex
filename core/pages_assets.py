"""Shared, public data projections for the browser-only BrandLex engine."""

import json
import sys
from dataclasses import asdict
from functools import lru_cache
from pathlib import Path

from core.copy_rules import RULES
from core.schema import CATEGORIES
from core.search_engine import _FEATURED_EXPRESSIONS
from data.lexicon_domains import learning_tip

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SNAPSHOTS = ("glossary_seed.json", "sample_drafts.json", "pages_rewrites.json", "brandlex_tbx.xcs")
OPENCC = ROOT / "core" / "opencc_data"


@lru_cache(maxsize=1)
def library_metadata():
    seed = json.loads((ROOT / "data" / "glossary_seed.json").read_text(encoding="utf-8"))
    casefold = {}
    for point in range(sys.maxunicode + 1):
        char = chr(point)
        folded = char.casefold()
        if folded != char.lower() or char == "Σ":
            casefold[char] = folded
    return {
        "categories": CATEGORIES,
        "learning_tips": {term["id"]: learning_tip(term) for term in seed},
        "casefold": casefold,
        "featured_terms": sorted(_FEATURED_EXPRESSIONS),
    }


@lru_cache(maxsize=1)
def rewrite_resources():
    names = ("HKVariants", "HKVariantsRev", "HKVariantsRevPhrases", "STCharacters", "STPhrases", "TSCharacters", "TSPhrases")
    return {
        "rules": [asdict(rule) for rule in RULES],
        "dictionaries": {name: (OPENCC / f"{name}.txt").read_text(encoding="utf-8") for name in names},
    }


GENERATED_ASSETS = {
    "pages_library.json": library_metadata,
    "pages_rewrite_resources.json": rewrite_resources,
}
