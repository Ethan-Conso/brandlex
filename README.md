# BrandLex

BrandLex is a trilingual marketing copy workspace and learning library for Hong Kong, mainland China, and English-speaking markets. [Open the public demo](https://ethan-conso.github.io/brandlex/).

## GitHub Pages and local static preview

```sh
python3 scripts/build_github_pages.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory docs
```

Open `http://127.0.0.1:8000/`. The Pages workflow rebuilds and publishes `docs/` from `main`. The generated directory is ignored by Git.

The static demo ships 3,203 terms and 45 cached DeepSeek results for the homepage and four sample drafts. Other drafts use the browser’s glossary and language rules. For unrestricted translation or a live rewrite, unlock 维护模式 and enter your own DeepSeek key in 文案改写. The key stays in browser session storage and is sent only to the official DeepSeek endpoint when you request a live rewrite.

The public maintenance demo uses `brandlex2026`. Its SHA-256 check unlocks edits in that browser, and edits persist in local storage. Exports include those edits. Reset clears them and restores the shipped library.

## Flask workspace

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open `http://127.0.0.1:5062/`. Flask uses SQLite and generates the local database and JSON snapshot from the seed. Configure `DEEPSEEK_API_KEY`, `BRANDLEX_ADMIN_PASSWORD`, and `BRANDLEX_SECRET_KEY` in your local `.env` or shell environment. To preview the browser engine through Flask, add `?mode=static` to the homepage URL.

The bundled cache can be regenerated with `.venv/bin/python scripts/cache_github_pages_rewrites.py` and a local DeepSeek key. The build and deployment workflow use the resulting JSON without credentials.

Run the [browser acceptance checks](tests/browser/README.md) alongside the Python suite with `.venv/bin/python -m unittest discover -s tests`.
