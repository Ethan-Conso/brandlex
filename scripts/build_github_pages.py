#!/usr/bin/env python3
"""Build the GitHub Pages artifact from the shared template and public snapshots."""

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.pages_assets import GENERATED_ASSETS, OPENCC, PUBLIC_SNAPSHOTS

ASSET = re.compile(r"\{\{ url_for\('static', filename='((?:css|js)/[\w.\-]+)'\) \}\}")
CSRF = '<meta name="csrf-token" content="{{ csrf_token }}">'
STATIC_HEAD = """<meta name="csrf-token" content="">
  <meta name="brandlex-mode" content="static">
  <meta name="referrer" content="same-origin">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self' https://api.deepseek.com; object-src 'none'; base-uri 'none'; form-action 'self'">"""


def copy_asset(source, destination):
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"Expected a regular asset file: {source.relative_to(ROOT)}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def stage_site(stage):
    template = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    if template.count(CSRF) != 1:
        raise ValueError("Expected one Flask CSRF meta tag in index.html")
    html = ASSET.sub(r"./static/\1", template.replace(CSRF, STATIC_HEAD))
    html = html.replace('href="/api/export/', 'href="./api/export/')
    if re.search(r"\{[{%]", html):
        raise ValueError("The static index contains unsupported Flask template syntax")
    (stage / "index.html").write_text(html, encoding="utf-8")
    (stage / ".nojekyll").touch()
    for name in set(ASSET.findall(template)):
        copy_asset(ROOT / "static" / name, stage / "static" / name)
    for name in PUBLIC_SNAPSHOTS:
        copy_asset(ROOT / "data" / name, stage / "data" / name)
    for name, generate in GENERATED_ASSETS.items():
        data = json.dumps(generate(), ensure_ascii=False, separators=(",", ":"))
        (stage / "data" / name).write_text(data, encoding="utf-8")
    for name in ("LICENSE.txt", "NOTICE.txt"):
        copy_asset(OPENCC / name, stage / "data" / "opencc_data" / name)


def build():
    output = ROOT / "docs"
    if output.is_symlink() or (output.exists() and not (output / ".nojekyll").is_file()):
        raise ValueError("docs already exists and is not a generated Pages artifact")
    with tempfile.TemporaryDirectory(prefix=".brandlex-pages-", dir=ROOT) as temporary:
        stage = Path(temporary) / "site"
        stage.mkdir()
        stage_site(stage)
        if output.exists():
            output.rename(Path(temporary) / "previous")
        stage.rename(output)
    print("Built GitHub Pages site in docs/")


if __name__ == "__main__":
    build()
