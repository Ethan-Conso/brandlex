# BrandLex browser acceptance

The application has no JavaScript package dependency. These functions execute through Playwright CLI against the running Flask interface. Model responses are mocked for UI checks. HTTP authentication, public write rejection, search, persistence, and downloads use the actual server. The Python suite validates DeepSeek request construction, structured responses, failures, script conversion, and glossary enforcement.

Run the unit and HTTP suites before browser acceptance:

```sh
.venv/bin/python -W error::ResourceWarning -m unittest discover -q
node --test tests/test_frontend_helpers.cjs tests/test_home_motion.cjs
```

Create a disposable library and launch it on **5063**. The password below is a test fixture, never a production credential. Existing `.env` is retained; these process variables take precedence.

```sh
.venv/bin/python data/init_seed_data.py --data-dir /private/tmp/brandlex-v3-2-browser-data
BRANDLEX_DATA_DIR=/private/tmp/brandlex-v3-2-browser-data BRANDLEX_ADMIN_PASSWORD=browser-test-only DEEPSEEK_API_KEY=your_deepseek_api_key_here PORT=5063 .venv/bin/python app.py
```

Run from the application directory, in a second terminal:

```sh
npx @playwright/cli -s=brandlex-v32-test open http://127.0.0.1:5063 --browser chrome
npx @playwright/cli -s=brandlex-v32-test resize 1440 1000
npx @playwright/cli -s=brandlex-v32-test run-code --filename=tests/browser/home.js
npx @playwright/cli -s=brandlex-v32-test run-code --filename=tests/browser/studio.js
npx @playwright/cli -s=brandlex-v32-test run-code --filename=tests/browser/library.js
npx @playwright/cli -s=brandlex-v32-test run-code --filename=tests/browser/responsive.js
npx @playwright/cli -s=brandlex-v32-test close
```

`library.js` requires the disposable loopback server on port 5063. It checks batches spanning six different categories, both shuffle controls, the 12 short category filters, stable search pagination, stale search isolation, unboxed cards, short takeaways, and in-card examples and copy. Both card whitespace and `详情` open the shared drawer, which retains the pitfall and full usage tip. `试改` triggers a rewrite with the cleaned draft. The suite also tests admin add, edit, delete, reset, confirmations, and session persistence. The Studio workflow opens a glossary reference outside the loaded feed. Downloaded exports are saved under `/private/tmp/BrandLex-v3-2-ui-export.*`. Start each workflow with a public session. `library.js` logs out at the end.

To capture the updated homepage and learning feed after launching `.venv/bin/python app.py` on 5062:

```sh
npx @playwright/cli -s=brandlex-v32-capture open http://127.0.0.1:5062 --browser chrome
npx @playwright/cli -s=brandlex-v32-capture run-code --filename=tests/browser/capture_v3.js
npx @playwright/cli -s=brandlex-v32-capture close
```

`home.js` tests the root landing view, learning CTA and tab names, 45 particles, animation pause and reduced motion, interactive feature surfaces, campaign previews, exports, selected-market rewrite handoffs, workspace links, preserved editor contents, all 12 scenario filters, browser history, direct links, and keyboard navigation. `responsive.js` checks the homepage at 320, 390, 768, and 1440px, all three views at a 390px viewport, the mobile scrolling category rail, and the single-row toolbar and two-column learning feed on desktop. `tests/test_homepage.py` and the Node helper suite scan the shipped HTML, CSS, and JS assets for emojis. The homepage suite also enforces short descriptive copy.

`capture_library.js` writes only `visual_assets/brandlex_v2_library.png` and makes no rewrite request. `capture_v3.js` updates the desktop home and library, and `capture_home.js` updates both home sizes. The broader `capture_screenshots.js` also captures Studio and the drawer and can make one live rewrite request when a valid key is configured.

## GitHub Pages acceptance

From the application directory, build the site and serve it under a project subpath with a disposable HTTP server.

```sh
python3 scripts/build_github_pages.py
preview_dir=$(mktemp -d "${TMPDIR:-/tmp}/brandlex-pages.XXXXXX")
ln -s "$PWD/docs" "$preview_dir/brandlex"
python3 -m http.server 5067 --bind 127.0.0.1 --directory "$preview_dir"
```

Run Playwright CLI from the application directory in a second terminal.

```sh
npx @playwright/cli -s=brandlex-pages open http://127.0.0.1:5067/brandlex/ --browser=chrome
npx @playwright/cli -s=brandlex-pages resize 1440 1000
npx @playwright/cli -s=brandlex-pages run-code --filename=tests/browser/github_pages.js
npx @playwright/cli -s=brandlex-pages close
```

This suite clears browser storage on the disposable origin. It checks the homepage, all 45 cached DeepSeek outputs, a mocked optional-key request and fallback, case browsing, local term edits across reloads, and three browser-generated exports. It also reports warm browser timings for search, feed, and term detail.
