"""Assemble the beauty, fashion, and technology seed catalogues."""

from data.seed_vertical_beauty import build_beauty_terms
from data.seed_vertical_fashion import build_fashion_terms
from data.seed_vertical_tech import build_tech_terms


def build_beauty_fashion_tech_terms():
    yield from build_beauty_terms()
    yield from build_fashion_terms()
    yield from build_tech_terms()
