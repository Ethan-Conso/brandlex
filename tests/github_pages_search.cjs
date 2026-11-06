// Exercise the browser search adapter against the built Pages assets in Node.
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { webcrypto } = require('node:crypto');

const output = process.argv[2];
const origin = 'https://example.github.io/brandlex/';
globalThis.window = globalThis;
globalThis.document = { baseURI: origin };
globalThis.localStorage = globalThis.sessionStorage = { getItem: () => null };
globalThis.crypto ??= webcrypto;
globalThis.fetch = async input => {
  const url = new URL(input, origin);
  assert(url.href.startsWith(`${origin}data/`), `Unexpected request: ${url}`);
  return new Response(readFileSync(join(output, url.pathname.slice('/brandlex/'.length))), {
    headers: { 'Content-Type': 'application/json' },
  });
};
require(join(output, 'static/js/static_engine.js'));

(async () => {
  const queries = JSON.parse(readFileSync(0, 'utf8'));
  const pages = await Promise.all(queries.map(async ([q, category, offset]) => {
    const params = new URLSearchParams({ q, category, offset, limit: 12 });
    const { success, data } = await BrandLexStaticEngine.request(`/api/terms?${params}`);
    assert.equal(success, true);
    const { terms, matched_total, has_more } = data;
    return { ids: terms.map(term => term.id), matched_total, has_more };
  }));
  process.stdout.write(JSON.stringify(pages));
})().catch(error => { process.stderr.write(`${error.stack}\n`); process.exitCode = 1; });
