"""Immutable multilingual search and draft indexes for a library snapshot."""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from random import choice, shuffle
import re
import unicodedata

from core.chinese_converter import convert_script


_TERM_FIELDS = ("term_en", "term_hk", "term_cn")
_CASE_SEARCH_FIELDS = ("category", "bad_example", "good_example_en", "good_example_hk", "good_example_cn")
_DASHES = re.compile(r"[-\u2010-\u2015\u2212]+")
_SPACES = re.compile(r"\s+")
_ALTERNATIVES = re.compile(
    r"\s+/\s+|[／|]|(?<=[\u3400-\u9fff])\s*/\s*|\s*/\s*(?=[\u3400-\u9fff])"
)
_ASCII_WORD = re.compile(r"[a-z0-9_]+")
_HAN = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U000323af]")
FEED_BATCH_SIZE = 6
_FEATURED_EXPRESSIONS = frozenset({
    "Niacinamide", "Retinol", "Pro-Xylane", "Skin Barrier Care",
    "Capsule Collection", "Haute Couture", "Bespoke Tailoring", "Private Viewing Appointment",
    "On-Device AI", "Active Noise Cancellation", "Foldable Display", "Trade-In Credit",
    "Tasting Menu", "Chef's Table", "Free-Flow Brunch", "Wine Pairing",
    "Family Suite", "Harbour View Room", "Room Upgrade", "Airport Transfer",
    "Faster Payment System", "Cashback", "Interest-Free Instalments", "Cross-Border Remittance",
    "Misleading Omission", "Absolute Advertising Claim", "Comparative Advertising", "From Price",
})


def _normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = _DASHES.sub(" ", normalized)
    return _SPACES.sub(" ", normalized).strip()


def _raw_expressions(term: Mapping) -> tuple[str, ...]:
    aliases = term.get("aliases", ())
    if isinstance(aliases, str):
        aliases = (aliases,)
    values = [term.get(field, "") for field in _TERM_FIELDS]
    values.extend(aliases if isinstance(aliases, (list, tuple)) else ())
    return tuple(dict.fromkeys(
        part.strip()
        for value in values if isinstance(value, str)
        for part in (value, *_ALTERNATIVES.split(value)) if part.strip()
    ))


def _normalized_expressions(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(filter(None, dict.fromkeys(map(_normalize, values))))


@lru_cache(maxsize=32_768)
def _script_variants(value: str) -> tuple[str, ...]:
    if not _HAN.search(value):
        return (value,)
    return tuple(dict.fromkeys((value, convert_script(value, "hk"), convert_script(value, "cn"))))


def expressions(term: Mapping) -> tuple[str, ...]:
    """Return editorial aliases and script variants without changing the records."""
    return tuple(dict.fromkeys(
        variant for value in _raw_expressions(term) for variant in _script_variants(value)
    ))


def _validate_records(terms: Iterable[Mapping]) -> tuple[dict, ...]:
    if isinstance(terms, (str, bytes, Mapping)) or not isinstance(terms, Iterable):
        raise TypeError("Terms must be a collection of term records.")
    records = tuple(terms)
    if any(not isinstance(term, Mapping) for term in records):
        raise TypeError("Each term must be a record.")
    return tuple(deepcopy(dict(term)) for term in records)


def _bigrams(value: str) -> Iterable[str]:
    return map("".join, zip(value, value[1:]))


def _is_featured(record: Mapping) -> bool:
    identifier, english = record.get("id"), record.get("term_en")
    return ((isinstance(identifier, int) and 1 <= identifier <= 100)
            or (isinstance(english, str) and english in _FEATURED_EXPRESSIONS))


def _has_concise_headwords(record: Mapping) -> bool:
    english, hong_kong, mainland = (str(record.get(field, "")) for field in _TERM_FIELDS)
    return (0 < len(english) <= 32 and len(_normalize(english).split()) <= 4
            and max(len(hong_kong), len(mainland)) <= 13)


def _occurrences(matches):
    if len(matches) == 1:
        return len(matches[0][1])
    spans = sorted((start, -length) for length, positions in matches for start in positions)
    count, end = 0, 0
    for start, negative_length in spans:
        if start >= end:
            count += 1
            end = start - negative_length
    return count


class _DraftIndex:
    """A prefix automaton finds candidate phrases in one pass over a draft."""

    def __init__(self, owners):
        children, outputs, suffixes, phrases = [{}], [[]], [0], []
        for expression, indices in owners.items():
            node = 0
            for char in expression:
                if char not in children[node]:
                    children[node][char] = len(children)
                    children.append({})
                    outputs.append([])
                    suffixes.append(0)
                node = children[node][char]
            outputs[node].append(len(phrases))
            phrases.append((len(expression), bool(_ASCII_WORD.match(expression[0])),
                            bool(_ASCII_WORD.match(expression[-1])), tuple(indices)))

        # Failing to extend one prefix may still extend a shorter suffix.
        queue = deque(children[0].values())
        while queue:
            parent = queue.popleft()
            for char, node in children[parent].items():
                suffix = suffixes[parent]
                while suffix and char not in children[suffix]:
                    suffix = suffixes[suffix]
                suffixes[node] = children[suffix].get(char, 0)
                outputs[node].extend(outputs[suffixes[node]])
                queue.append(node)
        self._children, self._outputs, self._suffixes, self._phrases = children, outputs, suffixes, phrases

    def find(self, text):
        node, matches = 0, defaultdict(list)
        children, suffixes, outputs, phrases = self._children, self._suffixes, self._outputs, self._phrases
        for end, char in enumerate(text, 1):
            successor = children[node].get(char)
            while successor is None and node:
                node = suffixes[node]
                successor = children[node].get(char)
            node = successor or 0
            for index in outputs[node]:
                length, left, right, _ = phrases[index]
                start = end - length
                if ((not left or not start or not _ASCII_WORD.match(text, start - 1))
                        and (not right or not _ASCII_WORD.match(text, end))):
                    positions = matches[index]
                    if not positions or start >= positions[-1] + length:
                        positions.append(start)
        hits = defaultdict(list)
        for index, positions in matches.items():
            length, _, _, owners = phrases[index]
            for owner in owners:
                hits[owner].append((length, positions))
        return hits


@dataclass(frozen=True)
class _IndexedTerm:
    record: dict
    expressions: tuple[str, ...]
    meaning: str
    case_context: tuple[str, ...]

    def rank(self, query: str, tokens: tuple[str, ...]) -> int | None:
        if query in self.expressions:
            return 0
        if any(value.startswith(query) for value in self.expressions):
            return 1
        if any(query in value for value in self.expressions):
            return 2
        if len(tokens) == 1:
            if query in self.meaning:
                return 4
            return 5 if any(query in value for value in self.case_context) else None
        if all(any(token in value for value in self.expressions) for token in tokens):
            return 3
        primary_fields = (*self.expressions, self.meaning)
        if all(any(token in value for value in primary_fields) for token in tokens):
            return 4
        fields = (*primary_fields, *self.case_context)
        if all(any(token in value for value in fields) for token in tokens):
            return 5
        return None


class SearchEngine:
    """Pre-index a copied library for repeated instant searches.

    Multiple query words must all appear somewhere in the expressions, aliases,
    meaning, category, or examples. A category filter matches the complete
    category label exactly. Equal-ranked results retain the library's order.
    """

    def __init__(self, terms: Iterable[Mapping]):
        self._index = tuple(
            _IndexedTerm(term, _normalized_expressions(_raw_expressions(term)),
                         _normalize(str(term.get("meaning", ""))),
                         _normalized_expressions(
                             value for field in _CASE_SEARCH_FIELDS if isinstance(value := term.get(field), str)
                         ))
            for term in _validate_records(terms)
        )
        self._positions = {
            entry.record["id"]: position for position, entry in enumerate(self._index) if "id" in entry.record
        }
        self._search_postings, self._categories, self._draft_index = self._build_postings()
        self._concise_indices = frozenset(
            index for index, entry in enumerate(self._index) if _has_concise_headwords(entry.record)
        )
        self._featured_indices = frozenset(
            index for index in self._concise_indices if _is_featured(self._index[index].record)
        )

    def _build_postings(self):
        postings, categories, draft_owners = defaultdict(set), defaultdict(set), defaultdict(list)
        for index, entry in enumerate(self._index):
            categories[entry.record.get("category", "")].add(index)
            for value in (*entry.expressions, entry.meaning, *entry.case_context):
                for gram in set(value).union(_bigrams(value)):
                    postings[gram].add(index)
            for value in _normalized_expressions(expressions(entry.record)):
                draft_owners[value].append(index)
        return dict(postings), dict(categories), _DraftIndex(draft_owners)

    def __len__(self):
        return len(self._index)

    def all_terms(self) -> list[dict]:
        return [deepcopy(entry.record) for entry in self._index]

    def get_term(self, term_id: int) -> dict | None:
        position = self._positions.get(term_id)
        return deepcopy(self._index[position].record) if position is not None else None

    def category_counts(self) -> dict[str, int]:
        return {category: len(indices) for category, indices in self._categories.items()}

    def _ordered_matches(self, query: str, category: str | None) -> range | list[int]:
        if not isinstance(query, str):
            raise TypeError("Search text must be a string.")
        if category is not None and not isinstance(category, str):
            raise TypeError("Category must be a string or None.")
        normalized = _normalize(query)
        if not normalized:
            if query.strip():
                return []
            return sorted(self._categories.get(category, ())) if category else range(len(self))
        tokens = tuple(normalized.split())
        grams = {gram for token in tokens for gram in (_bigrams(token) if len(token) > 1 else (token,))}
        postings = [self._search_postings.get(gram, set()) for gram in grams]
        if category:
            postings.append(self._categories.get(category, set()))
        candidates = set.intersection(*sorted(postings, key=len))
        ranked = []
        for index in candidates:
            rank = self._index[index].rank(normalized, tokens)
            if rank is not None:
                ranked.append((rank, index))
        return [index for _, index in sorted(ranked)]

    def search(self, query: str = "", category: str | None = None) -> list[dict]:
        return [deepcopy(self._index[index].record) for index in self._ordered_matches(query, category)]

    def search_page(
        self, query: str = "", category: str | None = None, *, offset: int = 0, limit: int = 60,
    ) -> tuple[list[dict], int]:
        indices = self._ordered_matches(query, category)
        return [deepcopy(self._index[index].record) for index in indices[offset:offset + limit]], len(indices)

    def sample_feed(
        self, category: str | None = None, limit: int = FEED_BATCH_SIZE, exclude_ids: Iterable[int] = (),
    ) -> list[dict]:
        """Favor fresh cases and spread each batch across the available categories."""
        if limit <= 0:
            return []
        if category is not None and not isinstance(category, str):
            raise TypeError("Category must be a string or None.")
        categories = {category: self._categories.get(category, set())} if category else self._categories
        excluded = {self._positions[term_id] for term_id in exclude_ids if term_id in self._positions}
        target = min(limit, sum(map(len, categories.values())))
        selected, counts = [], Counter()
        fresh = {name: pool - excluded for name, pool in categories.items()}
        self._draw_feed(fresh, target, selected, counts)
        if len(selected) < target:
            repeat = {name: pool & excluded for name, pool in categories.items()}
            self._draw_feed(repeat, target, selected, counts)
        shuffle(selected)
        return [deepcopy(self._index[index].record) for index in selected]

    def _draw_feed(self, categories, limit, selected, counts):
        available = {name: pool for name, pool in categories.items() if pool}
        while available and len(selected) < limit:
            # Randomize ties so choosing for diversity doesn't favor the index order.
            names = list(available)
            shuffle(names)
            names.sort(key=counts.__getitem__)
            for name in names[:limit - len(selected)]:
                pool = available[name]
                featured = self._featured_indices & pool
                concise = self._concise_indices & pool
                preferred = featured if len(selected) < (limit + 1) // 2 else concise - featured
                index = choice(tuple(preferred or concise or pool))
                selected.append(index)
                counts[name] += 1
                pool.remove(index)
                if not pool:
                    del available[name]

    def draft_matches(self, text: str, *, ranked=False, limit: int | None = None) -> list[dict]:
        """Match expression boundaries, optionally ordering by length, frequency and ID."""
        if not isinstance(text, str):
            raise TypeError("Copy must be a string.")
        hits = self._draft_index.find(_normalize(text))

        def sort_key(index):
            matches = hits[index]
            length = max(length for length, _ in matches)
            identifier = self._index[index].record.get("id")
            return -length, -_occurrences(matches), identifier if isinstance(identifier, int) else index

        matches = []
        seen = set()
        for index in sorted(hits, key=sort_key if ranked else None):
            entry = self._index[index]
            identity = entry.record.get("id", entry.expressions)
            if identity in seen:
                continue
            matches.append(deepcopy(entry.record))
            if len(matches) == limit:
                break
            seen.add(identity)
        return matches


def search_terms(
    terms: Iterable[Mapping], query: str = "", category: str | None = None,
) -> list[dict]:
    """Search the current library; return independent copies of matching terms."""
    return SearchEngine(terms).search(query, category)


def match_glossary_terms(text: str, terms: Iterable[Mapping] | SearchEngine) -> list[dict]:
    """Find expressions in library order without matching definitions or platform tags."""
    engine = terms if isinstance(terms, SearchEngine) else SearchEngine(terms)
    return engine.draft_matches(text)
