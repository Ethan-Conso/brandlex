"""Full-table Chinese script conversion using locally vendored OpenCC data.

This is orthographic normalization, not semantic translation. Ambiguous Han
characters depend on phrase context; the complete phrase tables are applied
before individual characters. See opencc_data/NOTICE.txt for provenance/license.
"""

from functools import lru_cache
from pathlib import Path
import re
from types import MappingProxyType

_DATA_DIR = Path(__file__).resolve().parent / "opencc_data"


@lru_cache(maxsize=7)
def _dictionary(name):
    with (_DATA_DIR / f"{name}.txt").open(encoding="utf-8") as source:
        entries = tuple(line.rstrip().split("\t", 1) for line in source if line.strip())
    values = {key: candidates.split(" ")[0] for key, candidates in entries}
    return MappingProxyType(values), tuple(sorted({len(key) for key in values}, reverse=True))


def _replace_longest(text, names):
    dictionaries = tuple(_dictionary(name) for name in names)
    chunks = []
    position = 0
    while position < len(text):
        match = None
        for dictionary, lengths in dictionaries:
            for length in lengths:
                key = text[position:position + length]
                if len(key) == length and key in dictionary:
                    match = (length, dictionary[key])
                    break
            if match:
                break
        length, value = match or (1, text[position])
        chunks.append(value)
        position += length
    return "".join(chunks)


def _convert_segment(text, market):
    """Convert prose; callers protect URLs before entering this function."""
    if market == "hk":
        traditional = _replace_longest(text, ("STPhrases", "STCharacters"))
        return _replace_longest(traditional, ("HKVariants",))
    if market == "cn":
        standard = _replace_longest(text, ("HKVariantsRevPhrases", "HKVariantsRev"))
        return _replace_longest(standard, ("TSPhrases", "TSCharacters"))
    return text


def convert_script(text, market):
    """Normalize prose scripts while preserving exact source URL destinations."""
    parts = re.split(r"(https?://[^\s<>\"，。！？；]+)", text, flags=re.IGNORECASE)
    return "".join(part if index % 2 else _convert_segment(part, market)
                   for index, part in enumerate(parts))
