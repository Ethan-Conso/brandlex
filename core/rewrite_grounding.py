"""Retrieve glossary constraints and verified regional phrases for one draft."""

from bisect import bisect_right
from functools import lru_cache
from itertools import accumulate, product
import re

from core.copy_rules import RULES
from core.search_engine import SearchEngine, expressions
from core.chinese_converter import convert_script

MAX_RAG_TERMS = 18
MAX_RAG_CONSTRAINTS = 24

_FIELDS = {"hk": "term_hk", "cn": "term_cn", "en": "term_en"}
_URL = r"https?://[^\s<>\"，。！？；]+"
_SCAN_URL = re.compile(_URL, re.IGNORECASE)
_SPLIT_URL = re.compile(f"({_URL})", re.IGNORECASE)
_HAN_RULE_ATOM = r"[\u3400-\u9fff]|\[[\u3400-\u9fff]+\]"
_HAN_RULE_ATOMS = re.compile(_HAN_RULE_ATOM)
_HAN_RULE_BRANCH = re.compile(f"(?:{_HAN_RULE_ATOM})+")


def _rule_prefixes(pattern):
    """Derive literal anchors only for plain Han alternatives and classes."""
    branches = pattern.split("|")
    if any(not _HAN_RULE_BRANCH.fullmatch(branch) for branch in branches):
        return ()
    return tuple(dict.fromkeys(
        "".join(chars)
        for branch in branches
        for chars in product(*(atom.strip("[]") for atom in _HAN_RULE_ATOMS.findall(branch)[:2]))
    ))


_REGIONAL_RULES = {
    market: tuple((rule, re.compile(rule.pattern, re.IGNORECASE), _rule_prefixes(rule.pattern))
                  for rule in RULES if rule.market == market)
    for market in _FIELDS
}


@lru_cache(maxsize=4096)
def phrase_pattern(value):
    left = r"(?<![A-Za-z0-9_])" if value[0].isascii() and value[0].isalnum() else ""
    right = r"(?![A-Za-z0-9_])" if value[-1].isascii() and value[-1].isalnum() else ""
    return re.compile(left + re.escape(value) + right, re.IGNORECASE)


def canonical_expression(term, market):
    value = term[_FIELDS[market]]
    # Explicit editorial alternatives are allowed; use the first, never print a
    # slash-separated shopping/marketing instruction into the finished draft.
    return re.split(r"\s+/\s+|／", value)[0].strip()


def _find_rules(text, market):
    found = []
    for rule, pattern, prefixes in _REGIONAL_RULES[market]:
        if prefixes and not any(prefix in text for prefix in prefixes):
            continue
        originals = tuple(dict.fromkeys(match.group() for match in pattern.finditer(text)))
        if originals:
            found.append((rule, originals))
    return found


def _casefold(value):
    # Python's IGNORECASE also treats dotted/dotless I as ASCII I.
    return value.replace("İ", "i").replace("ı", "i").casefold()


def _source_matches(value, source, folded_source):
    folded = _casefold(value)
    if folded not in folded_source:
        return
    pattern = phrase_pattern(value)
    if len(folded_source) != len(source):
        yield from pattern.finditer(source)
        return
    position = folded_source.find(folded)
    while position >= 0:
        match = pattern.match(source, position)
        if match:
            yield match
            position = folded_source.find(folded, match.end())
            continue
        position = folded_source.find(folded, position + 1)


def _source_expressions(value, source, folded_source):
    matches = _source_matches(value, source, folded_source)
    if value.lower() == value.upper():
        # Caseless phrases cannot produce a different original later in the draft.
        match = next(matches, None)
        return (match.group(),) if match else ()
    return dict.fromkeys(match.group() for match in matches)


def _ranked_terms(engine, text, rules):
    direct = engine.draft_matches(text, ranked=True, limit=MAX_RAG_TERMS)
    if not rules or len(direct) == MAX_RAG_TERMS:
        return direct
    # Rule-derived terms are relevant even when no glossary surface appears in
    # the draft. Place them after literal matches and keep rules independent.
    expanded = "\0".join(rule.replacement for rule, _ in rules)
    indirect = engine.draft_matches(expanded, ranked=True, limit=MAX_RAG_TERMS)
    identities = {term.get("id") for term in direct}
    return [*direct, *(term for term in indirect if term.get("id") not in identities)][:MAX_RAG_TERMS]


def retrieve_constraints(text, market, glossary):
    """Return bounded, ranked glossary rows and exact-source phrase rules."""
    scan_text = _SCAN_URL.sub(" ", text)
    engine = glossary if isinstance(glossary, SearchEngine) else SearchEngine(glossary)
    rules = _find_rules(scan_text, market)
    matched = _ranked_terms(engine, scan_text, rules)
    folded_source = _casefold(scan_text)
    constraints, targets = {}, {}
    for term in matched:
        target = convert_script(canonical_expression(term, market), market)
        identifier = term.get("id")
        for value in expressions(term):
            targets.setdefault(value, (target, identifier))
            for original in _source_expressions(value, scan_text, folded_source):
                if original != target:
                    constraints.setdefault(original.casefold(), {
                        "original": original, "adapted": target, "reason": "遵循品牌词库表达", "term_id": identifier,
                    })
    for rule, originals in rules:
        adapted, identifier = targets.get(rule.replacement, (rule.replacement, None))
        for original in originals:
            if original != rule.replacement:
                constraints.setdefault(original.casefold(), {
                    "original": original, "adapted": adapted, "reason": rule.reason[:15], "term_id": identifier,
                })
    # Longest expressions win; glossary entries precede generic rules on ties.
    ordered = sorted(constraints.values(), key=lambda item: -len(item["original"]))
    return matched, tuple(ordered[:MAX_RAG_CONSTRAINTS])


def output_constraints(matched, market):
    """Canonicalize every known alias in generated prose, including unseen aliases."""
    rows = []
    for term in matched:
        target = convert_script(canonical_expression(term, market), market)
        rows.extend({"original": value, "adapted": target}
                    for value in expressions(term) if value != target)
    return tuple(sorted(rows, key=lambda item: -len(item["original"])))


def _apply_segment(text, constraints, market):
    """Apply all known surface variants simultaneously, avoiding replacement loops."""
    folded_text = _casefold(text)
    canonical_spans = sorted((match.start(), match.end())
                             for target in {item["adapted"] for item in constraints}
                             for match in _source_matches(target, text, folded_text))
    canonical_starts = [start for start, _ in canonical_spans]
    # Track the maximum end among spans that start before a candidate. Merging
    # overlapping spans would wrongly protect a match not inside any one term.
    canonical_ends = list(accumulate((end for _, end in canonical_spans), max))
    matches = []
    for index, item in enumerate(constraints):
        for original in dict.fromkeys((item["original"], convert_script(item["original"], market))):
            for match in _source_matches(original, text, folded_text):
                previous = bisect_right(canonical_starts, match.start()) - 1
                if previous < 0 or match.end() > canonical_ends[previous]:
                    matches.append((match.start(), match.end(), index))
    selected = []
    end = -1
    for start, stop, index in sorted(set(matches), key=lambda row: (row[0], -row[1], row[2])):
        if start >= end:
            selected.append((start, stop, constraints[index]["adapted"]))
            end = stop
    chunks = []
    position = 0
    for start, end, replacement in selected:
        chunks.extend((text[position:start], replacement))
        position = end
    return "".join((*chunks, text[position:]))


def apply_constraints(text, constraints, market):
    """Normalize expressions in prose without changing live link destinations."""
    parts = _SPLIT_URL.split(text)
    return "".join(part if index % 2 else _apply_segment(part, constraints, market)
                   for index, part in enumerate(parts))
