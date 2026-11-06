# BrandLex V3.2

BrandLex is a marketing copy localization workspace with a shared brand library of more than 3,200 terms across 12 categories. The homepage introduces the workflow with a curated three-market preview and 12 category shortcuts. Navigation opens 文案改写 and 学习 at `/#studio` and `/#library`. Visitors can rewrite, search, inspect, copy, and export. Only an authenticated maintenance session can modify the library.

Homepage preview tabs switch locally between illustrative examples without submitting a draft or calling the model. Its explicit edit-and-rewrite action loads the displayed campaign and selected market into the studio and submits one real rewrite request. Three feature surfaces offer isolated market/tone previews, expression copying, and direct exports. Ordinary navigation preserves studio drafts and results. Scenario shortcuts clear the library search and apply their category. Browser Back and Forward restore the selected view.

The homepage particle canvas respects reduced-motion preferences and pauses while its hero, the homepage, or the browser document is hidden. Homepage styles and interactions are scoped separately from both functional workspaces.

学习 opens with six regional copywriting cases drawn across different categories. Cards show three expressions, a switchable example, and one short takeaway. The shared detail drawer contains the full notes and pitfalls. Search can load more ranked cases, and 试改 sends a case's pitfall to the studio for rewriting.

## Launch and configuration

From the application directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open `http://127.0.0.1:5062`. `PORT` changes the port. `wsgi.py` exposes `application` for a WSGI host. The development server binds to `127.0.0.1` and does not enable debug mode.

Startup reads the application directory's existing `.env` without modifying it. Environment variables already set by the host take precedence. Configure these values privately:

| Variable | Purpose |
| --- | --- |
| `DEEPSEEK_API_KEY` | Enables DeepSeek rewriting; an absent key or the documented placeholder selects a local preview. |
| `DEEPSEEK_BASE_URL` | Chat Completions service base URL; normally `https://api.deepseek.com`. |
| `BRANDLEX_ADMIN_PASSWORD` | Maintenance password; never returned to the browser. |
| `BRANDLEX_SECRET_KEY` | Persistent, unpredictable session-signing secret. Use the same secret across workers. |
| `BRANDLEX_HTTPS` | Set to `1` when serving over HTTPS to require secure cookies. |
| `BRANDLEX_DATA_DIR` | Optional separately initialized library directory. |

Do not commit `.env`. Configure production secrets outside source control. Missing, short, or publicly documented sample session secrets are replaced with a random process-local secret; use a private persistent secret of at least 32 characters for multiple workers or sessions that survive restarts. No browser-side API key or password is required for public reading and rewriting.

## HTTP API and maintenance access

Responses use `{ "success": true, "data": ... }`; errors use `{ "success": false, "error": "..." }`. `GET /api/bootstrap` returns six random cases, category labels and counts, four sample drafts, a CSRF token, and `is_admin`. Send that token in `X-CSRF-Token` for every POST, PATCH, or DELETE request. Browser sessions use an HttpOnly, SameSite cookie. Cross-origin writes are rejected, and API requests are rate limited.

| Route | Access and result |
| --- | --- |
| `GET /api/bootstrap` | Public workspace data and current maintenance state. |
| `GET /api/terms?mode=feed&category=...&exclude=1,2` | Public random case feed. Defaults to six and avoids previous IDs when the pool allows. |
| `GET /api/terms?q=...&category=...&offset=0&limit=12` | Public ranked case search and pagination. The limit is capped at 200. |
| `GET /api/terms/<id>` | Public complete term record. |
| `GET /api/export/csv`, `/tbx`, `/json` | Public library downloads. |
| `POST /api/rewrite` | Public complete-draft rewrite; JSON body: `text`, `target_market`, `tone`. |
| `POST /api/check` | Compatible local editorial check; JSON body: `text`, `target_market`. |
| `POST /api/admin/login` | JSON body: `password`; authenticates the current session. |
| `POST /api/admin/logout` | JSON body: `{}`; ends maintenance access for the current session. |
| `POST /api/terms` | Maintenance only; complete editable term fields. |
| `PATCH /api/terms/<id>` | Maintenance only; partial editable fields. |
| `DELETE /api/terms/<id>` | Maintenance only. |
| `POST /api/library/reset` | Maintenance only; JSON body must be exactly `{ "confirm": true }`. |

Each library response includes `terms`, `total` for the whole library, `matched_total` for the active query or category, `offset`, `limit`, `has_more`, and `category_counts` for the whole library. Case records include a display-only `learning_tip` of at most 22 characters alongside the full `usage_tip`. Random responses use `offset: 0` and `has_more: false`. An empty query defaults to the random feed. An explicit offset or limit retains ordered pagination when feed mode and exclusions are omitted.

Unauthenticated library mutations return HTTP 403 with `请先解锁维护模式后再修改词库。`. Hiding maintenance controls is only a convenience: the server independently checks authorization. Login and logout rotate the session and return its maintenance state and current CSRF token; use the returned token for subsequent requests. Maintenance access expires and is invalidated when the configured maintenance password changes. An absent maintenance password leaves library writes locked. Never log passwords, keys, or draft bodies.

## Complete-draft rewriting

```python
from core.ai_rewriter import rewrite_copy
from core.db_manager import DBManager

library = DBManager()
result = rewrite_copy(
    "新品早鸟福利限时上线，满299包邮。",
    "hk",
    "standard",
    library.get_search_engine(),
)
print(result["primary_copy"])
```

Targets are `hk`, `cn`, and `en`; tones are `standard`, `social`, and `concise`. Input is limited to 20,000 characters. Retrieval matches glossary expressions, aliases, and relevant regional rules before composing the rewriting instruction. Each of the nine market and tone combinations has its own editorial guidance for voice, structure, and regional phrasing. Both versions preserve the facts, prices, dates, offers, and applicable brand terminology.

Retrieval ranks glossary hits by the longest matched expression, then occurrence count, then term ID. It retains up to 18 terms and 24 phrase rules. The model prompt further packs those results into a 690-byte UTF-8 JSON budget, a conservative token bound for byte-level tokenizers. It sends usage tips of at most 80 characters and omits examples and other metadata. This budget covers the grounding block. Draft length and model output have separate limits.

With a configured key, the service posts to `{DEEPSEEK_BASE_URL}/chat/completions` using `deepseek-flash`, `urllib.request`, a 25-second timeout, and JSON object output. Requests disable thinking and use temperatures 0.5 for `standard`, 0.75 for `social`, and 0.35 for `concise`. The submitted draft and relevant library constraints are sent to DeepSeek. Drafts are not added to the library or persisted by BrandLex.

The result contains:

- `primary_copy` and `alt_copy`: recommended and shorter versions.
- `adaptations`: exact source and output quotes for glossary, style, and translation edits, with a short Chinese reason and a verified `term_id` when applicable.
- `cta_options`: two optional ending suggestions.
- `matched_glossary_terms`: complete reference records for the shared detail drawer.
- `counts` and `source_counts`: output and input length/read-time estimates.
- `engine`: `deepseek` or `fallback`, with a truthful `notice` when a local preview is returned.

Fallback notices distinguish configuration, authentication, balance, rate limits, timeouts, connection/certificate problems, and unusable model output. The returned `error_code` is a stable category and is `null` after a successful model rewrite. No provider response body, credentials, or draft text is included in a diagnostic. A successful HTTP response can still require a local preview if its content is incomplete or fails validation; this does not imply that the API credentials are invalid.

An absent or placeholder key, network failure, timeout, or unusable model response produces a local preview instead. Complete Traditional/Simplified conversion and regional wording rules maintain Chinese script consistency. This local preview does not have the semantic rewriting or general translation abilities of a language model; the UI identifies it explicitly. Review all generated marketing copy before publishing, especially names and factual claims.

## Library persistence and export

```python
library = DBManager()
terms = library.search_terms("early bird")
term = library.get_term(terms[0]["id"])
library.update_term(term["id"], {"usage_tip": "Your team's regional guidance."})
csv_bytes = library.export_csv()
library.export("tbx", "/tmp/brandlex.tbx")
```

`add_term(record)` accepts every seed field except `id`, which is assigned automatically. `update_term(id, changes)` accepts a partial record. Both validate the complete resulting record and return a fresh dictionary with an `updated_at` timestamp. `delete_term(id)` returns whether a record was removed. `reset_to_defaults()` returns the restored records. Missing lookups return `None`; edits to a missing ID raise `KeyError`; invalid input raises `ValueError`. These Python methods are internal persistence operations; HTTP maintenance authorization is enforced separately.

`data/digilex.db` is authoritative. `data/glossary.json` mirrors the current library; `data/glossary_seed.json` contains defaults. A new database loads its defaults automatically; an existing empty library stays empty. On opening an older library, the five previous category labels migrate to V2 labels without replacing terms, custom wording, IDs, or timestamps. Older default JSON labels are normalized in memory without modifying the source file.

Every mutation commits a transaction and publishes a complete JSON snapshot. Publication is serialized across writers and uses an atomic file replacement. If publication fails after the database commit, `SnapshotSyncError` explicitly reports that the library was saved; call `sync_json()` or reopen the manager to repair the snapshot.

`export_csv()`, `export_tbx()`, and `export_json()` return bytes. CSV uses UTF-8-SIG and protects spreadsheet formula cells. TBX exports `en`, `zh-Hant-HK`, and `zh-Hans-CN` sections with definitions, examples, and notes; an empty library must have a term added before TBX export. JSON retains every field. `export(format, path=None)` returns bytes or atomically saves a separate file; exports cannot overwrite the library or default files.

To generate the clean default library:

```sh
.venv/bin/python data/init_seed_data.py
```

This command **restores the full V3 default library and replaces local term edits**. Use `--data-dir /path/to/directory` for a disposable library. The original 100 terms retain IDs 1 through 100. The additional terms are built deterministically from category-specific editorial matrices. All bundled terms and samples are emoji-free.

## Search and compatible Copy Check

```python
from core.copy_checker import analyze_copy

search = library.get_search_engine()
results = search.search("种草", category="社媒与种草")
report = analyze_copy("亲，爆款精华包邮，快来种草！", "hk", search)
```

Search includes English, both Chinese expressions, aliases, meanings, category names, and copywriting examples. It ignores case and normalizes full-width characters and dash variants. Multiple query words must all occur in the record. Exact expressions rank before prefixes, partial expressions, definitions, and matches in the case text. Category filters match complete labels. `SearchEngine` is an independent snapshot. `DBManager` reuses the index for search, pagination, and draft matching until the database version changes. Read requests reuse the snapshot in memory and leave the JSON backup untouched.

The compatible checker returns readiness scores, exact-span suggestions, CTA strength and suggestions, counts, readability, warnings, and matched records. It stays local and does not perform complete-draft translation. Its editorial scores estimate wording readiness, not conversion performance.

Replacement positions use Python Unicode code points in the exact submitted draft. In JavaScript, slice `Array.from(text)` to handle supplementary characters correctly. Recheck after edits; `apply_suggestion()` rejects stale spans. Character counts exclude whitespace; Chinese characters and English words each count as one reading unit. Reading time is an estimate.

## Verification

```sh
.venv/bin/python -m unittest discover -v
BRANDLEX_TEST_PYTHON=.venv/bin/python node --test tests/test_*.cjs
```

Tests exercise dataset quality, multilingual search, persistence and migrations, concurrent writers, snapshot recovery, malformed inputs, exports, local checking, rewrite service responses, maintenance isolation, same-origin protection, request limits, and complete backend workflows. Browser verification instructions live in `tests/browser/README.md`.

With the optional `coverage` development tool:

```sh
python3 -m coverage run --branch --source=core,data,app,web_security,admin_auth -m unittest discover -q
python3 -m coverage report -m --fail-under=80
```

TBX follows the [TBX-Basic data category rules](https://github.com/LTAC-Global/TBX-Basic_dialect/blob/master/DCA/TBX-Basic_DCA.sch) and [TBX core structure](https://github.com/LTAC-Global/TBX_Core_RNG/blob/master/TBXcoreStructV03.rng).
