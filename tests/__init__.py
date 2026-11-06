"""Shared test fixture for legacy HTTP and permission contracts."""

import json
from pathlib import Path

from data.seed_terms import build_sample_drafts, build_seed_terms


def write_flagship_fixture(directory):
    """Let the app initialize SQLite from the original 100 defaults."""
    root = Path(directory)
    for name, records in (("glossary_seed.json", build_seed_terms()),
                          ("sample_drafts.json", build_sample_drafts())):
        (root / name).write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
