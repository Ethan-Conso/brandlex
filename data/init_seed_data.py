"""Build BrandLex's default library and restore the local working library.

Run from any directory: python /path/to/data/init_seed_data.py
The --data-dir option supports isolated previews and automated verification.
Running this command explicitly restores defaults, replacing local term edits.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.db_manager import DBManager
from data.seed_terms import build_sample_drafts


def _write_json(path, value):
    """Publish a complete file, without leaving a partly written default set."""
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, delete=False) as handle:
            temporary_path = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def initialize_data(data_dir=None):
    """Generate editorial JSON files and restore the full default library."""
    from data.seed_library import build_default_library

    destination = Path(data_dir) if data_dir is not None else Path(__file__).resolve().parent
    destination.mkdir(parents=True, exist_ok=True)
    terms = build_default_library()
    drafts = build_sample_drafts()
    database = destination / "digilex.db"
    existing = database.exists()
    _write_json(destination / "glossary_seed.json", terms)
    _write_json(destination / "sample_drafts.json", drafts)
    manager = DBManager(db_path=database,
                        json_path=destination / "glossary.json",
                        seed_path=destination / "glossary_seed.json")
    if existing:
        manager.reset_to_defaults()
    return {"term_count": len(terms), "sample_count": len(drafts)}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Restore BrandLex's full default library.")
    parser.add_argument("--data-dir", type=Path, default=None,
                        help="Write generated data to this directory instead of the bundled data directory.")
    args = parser.parse_args(argv)
    result = initialize_data(args.data_dir)
    print(f"BrandLex: {result['term_count']} default terms and {result['sample_count']} sample drafts ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
