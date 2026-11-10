# BrandLex

BrandLex is a trilingual marketing copy workspace and learning library for Hong Kong, mainland China, and English-speaking markets. [Open the public demo](https://ethan-conso.github.io/brandlex/).

## GitHub Pages and local static preview

```sh
python3 scripts/build_github_pages.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory docs
```

Open `http://127.0.0.1:8000/`. The Pages workflow rebuilds and publishes `docs/` from `main`. The generated directory is ignored by Git.

The static demo ships 3,208 terms with Chinese and English definitions and 45 cached DeepSeek results for the homepage and four sample drafts. When a public relay is configured, new drafts, edited samples, and `试改` cases can call `deepseek-flash` without a sign-in. 文案改写 also accepts an optional personal DeepSeek key. It stays in the current browser session and is sent directly to DeepSeek when a draft needs live rewriting. Without either connection, the browser offers a labeled local glossary preview.

The public maintenance demo uses `brandlex2026`. Its SHA-256 check unlocks edits in that browser, and edits persist in local storage. Exports include those edits. Reset clears them and restores the shipped library.

### Enable public live rewrites on GitHub Pages

1. Open the [Render deployment for BrandLex](https://render.com/deploy?repo=https://github.com/Ethan-Conso/brandlex), sign in, and deploy the relay described in `render.yaml`. Enter a dedicated `DEEPSEEK_API_KEY` in Render when prompted. The free service can take about a minute to wake after 15 minutes idle. [Render free service limits](https://render.com/docs/free)
2. Once the service is live, open `/healthz` on its public URL to check that it returns HTTP 200. In the [BrandLex Actions variables](https://github.com/Ethan-Conso/brandlex/settings/variables/actions), set `BRANDLEX_PUBLIC_REWRITE_URL` to the full endpoint, for example `https://brandlex-rewrite.onrender.com/api/pages/rewrite`. Only the endpoint URL goes into GitHub.
3. Run the [Pages workflow](https://github.com/Ethan-Conso/brandlex/actions/workflows/pages.yml). Open 文案改写 in a fresh browser session, paste a new draft, and verify that the result is labeled `DeepSeek`.

The relay accepts drafts of up to 4,000 characters and uses the shipped glossary. Browser-only glossary edits remain local. The service limits requests to six per minute per IP and 120 per 24 hours per process. Those counters reset with the process. The allowed browser origin controls CORS. For a public demo, use a dedicated key and bound its available provider balance or quota.

On another HTTPS host, install `requirements-relay.txt`, serve `pages_wsgi:application` with one Gunicorn worker, and set `BRANDLEX_PAGES_ORIGIN=https://ethan-conso.github.io` and `DEEPSEEK_API_KEY` in the hosting environment. The Render blueprint enables `BRANDLEX_PAGES_TRUST_CLOUDFLARE` for its managed edge, which overwrites the client IP header. Leave it disabled for direct access or if the proxy can forward client-supplied values.

## Flask workspace

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open `http://127.0.0.1:5062/`. Flask uses SQLite and generates the local database and JSON snapshot from the seed. Configure `DEEPSEEK_API_KEY`, `BRANDLEX_ADMIN_PASSWORD`, and `BRANDLEX_SECRET_KEY` in your local `.env` or shell environment. To preview the browser engine through Flask, add `?mode=static` to the homepage URL.

The bundled cache can be regenerated with `.venv/bin/python scripts/cache_github_pages_rewrites.py` and a local DeepSeek key. The build and deployment workflow use the resulting JSON without credentials.

Run the [browser acceptance checks](tests/browser/README.md) alongside the Python suite with `.venv/bin/python -m unittest discover -s tests`.
