"""BrandLex persistence. The database is authoritative; glossary.json is a snapshot.

Search uses a process-local index of the current database. Default terms live
in glossary_seed.json and are never overwritten by edits. A failed JSON backup
raises SnapshotSyncError after the database commit; sync_json() can repair it.
"""

import csv
import io
import json
import os
import sqlite3
import tempfile
from collections.abc import Mapping
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from xml.etree import ElementTree as ET

from core.schema import LIST_FIELDS, TERM_FIELDS, TEXT_FIELDS, validate_identifier, validate_term
from core.search_engine import SearchEngine

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TBX_NAMESPACE = "urn:iso:std:iso:30042:ed-2"
DATABASE_FIELDS = (*TERM_FIELDS, "updated_at")
_COLUMNS = ", ".join(DATABASE_FIELDS)
_INSERT = f"INSERT INTO terms ({_COLUMNS}) VALUES ({', '.join('?' for _ in DATABASE_FIELDS)})"
# Previous releases used decorative category prefixes. Only these exact labels
# are migrated; user wording, timestamps, IDs and unrelated categories stay intact.
_LEGACY_CATEGORIES = (
    ("\U0001F4F1 社媒与内容种草", "社媒与种草"),
    ("\U0001F6CD\uFE0F 电商与大促转化", "电商与转化"),
    ("\U0001F4C8 广告投放与增长指标", "投放与增长"),
    ("\U0001F48E 品牌公关与线下体验", "公关与线下"),
    ("\u270D\uFE0F 广告文案与视觉修辞", "文案与修辞"),
)


class SnapshotSyncError(RuntimeError):
    """The library was saved, but its JSON backup needs to be retried."""


def _atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _json_bytes(records):
    return (json.dumps(records, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _from_row(row):
    return {key: json.loads(row[key]) if key in LIST_FIELDS else row[key] for key in DATABASE_FIELDS}


def _values(record):
    return tuple(json.dumps(record[key], ensure_ascii=False) if key in LIST_FIELDS else record[key] for key in DATABASE_FIELDS)


def _current_category(record):
    if not isinstance(record, Mapping):
        return record
    category = record.get("category")
    for legacy, current in _LEGACY_CATEGORIES:
        if category == legacy:
            return {**record, "category": current}
    return record


def _timestamp():
    return datetime.now(timezone.utc).isoformat()


class DBManager:
    """Manage one local library, with explicit paths for isolated deployments/tests."""

    def __init__(self, db_path=None, json_path=None, seed_path=None):
        self.db_path = Path(db_path or DATA_DIR / "digilex.db").resolve()
        self.json_path = Path(json_path or self.db_path.with_name("glossary.json")).resolve()
        self.seed_path = Path(seed_path or self.db_path.with_name("glossary_seed.json")).resolve()
        if len({self.db_path, self.json_path, self.seed_path}) != 3:
            raise ValueError("The library, backup, and default terms must use different files.")
        self._cache_lock = Lock()
        self._cache = None
        self._wal_path = self.db_path.with_name(self.db_path.name + "-wal")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()
        self._repair_json_if_needed()

    @contextmanager
    def _connection(self):
        connection = sqlite3.connect(self.db_path, timeout=15)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _load_defaults(self):
        try:
            records = json.loads(self.seed_path.read_text(encoding="utf-8"))
        except FileNotFoundError as error:
            raise FileNotFoundError("Default terms are missing. Run data/init_seed_data.py first.") from error
        except json.JSONDecodeError as error:
            raise ValueError("The default term file is not valid JSON.") from error
        if not isinstance(records, list) or not records:
            raise ValueError("The default term file must contain a nonempty list.")
        validated = [validate_term(_current_category(record), require_id=True) for record in records]
        if len({record["id"] for record in validated}) != len(validated):
            raise ValueError("Every default term must have a unique ID.")
        return validated

    def _initialize(self):
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            table = connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='terms'").fetchone()
            if table:
                columns = {row["name"] for row in connection.execute("PRAGMA table_info(terms)")}
                if not set(DATABASE_FIELDS) <= columns:
                    raise ValueError("This library uses an older format. Use a new library path to preserve it.")
                connection.executemany("UPDATE terms SET category = ? WHERE category = ?",
                                       [(current, legacy) for legacy, current in _LEGACY_CATEGORIES])
                return
            defaults = self._load_defaults()
            strings = ", ".join(f"{field} TEXT NOT NULL" for field in (*TEXT_FIELDS, *LIST_FIELDS, "updated_at"))
            connection.execute(f"CREATE TABLE terms (id INTEGER PRIMARY KEY AUTOINCREMENT, {strings})")
            connection.execute("CREATE INDEX terms_category ON terms(category)")
            self._insert_defaults(connection, defaults)

    @staticmethod
    def _insert_defaults(connection, defaults):
        timestamp = _timestamp()
        connection.executemany(_INSERT, [_values({**record, "updated_at": timestamp}) for record in defaults])

    def _read_all_terms(self):
        with self._connection() as connection:
            return [_from_row(row) for row in connection.execute(f"SELECT {_COLUMNS} FROM terms ORDER BY id")]

    def _database_version(self):
        database = self.db_path.stat()
        try:
            wal = self._wal_path.stat()
            wal_version = (wal.st_ino, wal.st_mtime_ns, wal.st_size)
        except FileNotFoundError:
            wal_version = None
        return (database.st_ino, database.st_mtime_ns, database.st_size, wal_version)

    def get_search_engine(self):
        """Reuse an independent index until a committed library version changes."""
        with self._cache_lock:
            version = self._database_version()
            if self._cache is not None and self._cache[0] == version:
                return self._cache[1]
            records = self._read_all_terms()
            engine = SearchEngine(records)
            if self._database_version() == version:
                self._cache = (version, engine)
            return engine

    def get_all_terms(self):
        return self.get_search_engine().all_terms()

    def get_term(self, term_id):
        validate_identifier(term_id)
        return self.get_search_engine().get_term(term_id)

    def search_terms(self, query="", category=None):
        return self.get_search_engine().search(query, category)

    def _publish_mutation(self):
        with self._cache_lock:
            self._cache = None
        self.sync_json()

    def _repair_json_if_needed(self):
        try:
            database_mtime = self.db_path.stat().st_mtime_ns
            if self._wal_path.exists():
                database_mtime = max(database_mtime, self._wal_path.stat().st_mtime_ns)
            if self.json_path.stat().st_mtime_ns >= database_mtime:
                with self.json_path.open(encoding="utf-8") as snapshot:
                    if isinstance(json.load(snapshot), list):
                        return
        except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
            pass
        self.sync_json()

    def add_term(self, term):
        record = validate_term(term)
        if "id" in record:
            raise ValueError("New term IDs are assigned automatically.")
        record = {**record, "updated_at": _timestamp()}
        fields = tuple(field for field in DATABASE_FIELDS if field != "id")
        with self._connection() as connection:
            values = tuple(json.dumps(record[field], ensure_ascii=False) if field in LIST_FIELDS else record[field] for field in fields)
            cursor = connection.execute(f"INSERT INTO terms ({', '.join(fields)}) VALUES ({', '.join('?' for _ in fields)})", values)
            saved = {**record, "id": cursor.lastrowid}
        self._publish_mutation()
        return saved

    def update_term(self, term_id, changes):
        validate_identifier(term_id)
        if not isinstance(changes, Mapping) or not changes or set(changes) - (set(TERM_FIELDS) - {"id"}):
            raise ValueError("Provide editable term fields only.")
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(f"SELECT {_COLUMNS} FROM terms WHERE id = ?", (term_id,)).fetchone()
            if row is None:
                raise KeyError("This term could not be found.")
            current = _from_row(row)
            saved = validate_term({**current, **changes}, require_id=True, allow_metadata=True)
            saved = {**saved, "updated_at": _timestamp()}
            fields = tuple(field for field in DATABASE_FIELDS if field != "id")
            values = tuple(json.dumps(saved[field], ensure_ascii=False) if field in LIST_FIELDS else saved[field] for field in fields)
            connection.execute(f"UPDATE terms SET {', '.join(field + ' = ?' for field in fields)} WHERE id = ?", (*values, term_id))
        self._publish_mutation()
        return saved

    def delete_term(self, term_id):
        validate_identifier(term_id)
        with self._connection() as connection:
            deleted = connection.execute("DELETE FROM terms WHERE id = ?", (term_id,)).rowcount > 0
        if deleted:
            self._publish_mutation()
        return deleted

    def reset_to_defaults(self):
        defaults = self._load_defaults()
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("DELETE FROM terms")
            connection.execute("DELETE FROM sqlite_sequence WHERE name = 'terms'")
            self._insert_defaults(connection, defaults)
        self._publish_mutation()
        return self.get_all_terms()

    def sync_json(self):
        """Publish the latest database state, serializing writers across processes."""
        try:
            with self._connection() as connection:
                connection.execute("BEGIN IMMEDIATE")
                records = [_from_row(row) for row in connection.execute(f"SELECT {_COLUMNS} FROM terms ORDER BY id")]
                _atomic_write(self.json_path, _json_bytes(records))
        except OSError as error:
            raise SnapshotSyncError("The library was saved, but its backup could not be updated. Retry syncing the library.") from error
        return self.json_path

    def export_json(self):
        """Return UTF-8 JSON bytes, including every field."""
        return _json_bytes(self.get_all_terms())

    def export_csv(self):
        """Return Excel-compatible bytes; protect cells from formula execution."""
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=DATABASE_FIELDS)
        writer.writeheader()
        for record in self.get_all_terms():
            writer.writerow({field: _csv_cell(record[field]) for field in DATABASE_FIELDS})
        return output.getvalue().encode("utf-8-sig")

    def export_tbx(self):
        """Return an escaped three-language TBX document."""
        records = self.get_all_terms()
        if not records:
            raise ValueError("Add at least one term before exporting a TBX library.")
        root = ET.Element("tbx", {"xmlns": TBX_NAMESPACE, "type": "TBX-Basic", "style": "dca", "{http://www.w3.org/XML/1998/namespace}lang": "en"})
        header = ET.SubElement(root, "tbxHeader")
        description = ET.SubElement(header, "fileDesc")
        ET.SubElement(ET.SubElement(description, "titleStmt"), "title").text = "BrandLex Marketing Library"
        ET.SubElement(ET.SubElement(description, "sourceDesc"), "p").text = "BrandLex team library export."
        body = ET.SubElement(ET.SubElement(root, "text"), "body")
        for record in records:
            _tbx_entry(body, record)
        ET.indent(root, space="  ")
        return ET.tostring(root, encoding="utf-8", xml_declaration=True)

    def export(self, format, path=None):
        """Return export bytes, or atomically write them to an explicit destination."""
        exporters = {"csv": self.export_csv, "json": self.export_json, "tbx": self.export_tbx}
        if not isinstance(format, str) or format.lower().lstrip(".") not in exporters:
            raise ValueError("Choose CSV, TBX, or JSON to export the library.")
        content = exporters[format.lower().lstrip(".")]()
        if path is None:
            return content
        destination = Path(path).resolve()
        if destination in {self.db_path, self.json_path, self.seed_path}:
            raise ValueError("Choose a separate export file to preserve the library.")
        _atomic_write(destination, content)
        return destination


def _csv_cell(value):
    value = json.dumps(value, ensure_ascii=False) if isinstance(value, list) else str(value)
    if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r")):
        return "'" + value
    return value


def _tbx_entry(body, record):
    entry = ET.SubElement(body, "conceptEntry", {"id": f"brandlex-{record['id']}"})
    ET.SubElement(entry, "descrip", {"type": "subjectField"}).text = record["category"]
    ET.SubElement(entry, "descrip", {"type": "definition"}).text = record["meaning"]
    ET.SubElement(entry, "note").text = record["usage_tip"]
    ET.SubElement(entry, "note").text = "Avoid: " + record["bad_example"]
    ET.SubElement(entry, "note").text = "Search aliases: " + ", ".join(record["aliases"])
    ET.SubElement(entry, "note").text = "Platforms: " + ", ".join(record["platforms"])
    for language, field, example in (("en", "term_en", "good_example_en"), ("zh-Hant-HK", "term_hk", "good_example_hk"), ("zh-Hans-CN", "term_cn", "good_example_cn")):
        section = ET.SubElement(entry, "langSec", {"{http://www.w3.org/XML/1998/namespace}lang": language})
        term_section = ET.SubElement(section, "termSec")
        ET.SubElement(term_section, "term").text = record[field]
        ET.SubElement(term_section, "descrip", {"type": "context"}).text = record[example]
