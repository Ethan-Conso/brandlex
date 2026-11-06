const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { webcrypto } = require('node:crypto');

const [output, gateway] = process.argv.slice(2);
const site = 'https://example.github.io/brandlex/';
const provider = 'https://api.deepseek.com/chat/completions';
const draft = '用新的方式开启平凡的一天。';
const mockedKey = 'fixture-personal-key';
const cache = JSON.parse(readFileSync(join(output, 'data/pages_rewrites.json'), 'utf8'));
const editedSample = `${cache.drafts[0].text}\n文案补充说明。`;
const enginePath = require.resolve(join(output, 'static/js/static_engine.js'));
const calls = [];
let gatewayStatus = 200;
let gatewayOverrides = {};

globalThis.window = globalThis;
globalThis.crypto ??= webcrypto;
globalThis.BrandLexHelpers = require(join(output, 'static/js/helpers.js'));
globalThis.BrandLexStaticRewrite = require(join(output, 'static/js/static_rewrite.js'));
globalThis.fetch = async (input, options) => {
  const url = new URL(input, site);
  if (url.href.startsWith(`${site}data/`)) {
    const file = join(output, url.pathname.slice('/brandlex/'.length));
    return new Response(readFileSync(file));
  }
  const headers = new Headers(options.headers);
  const payload = JSON.parse(options.body);
  calls.push(url.href);
  assert.equal(options.method, 'POST');
  assert.equal(options.credentials, 'omit');
  assert.equal(options.cache, 'no-store');
  assert(!headers.has('X-CSRF-Token'));
  if (url.href === gateway) {
    assert.deepEqual(Object.keys(payload).sort(), ['target_market', 'text', 'tone']);
    assert([draft, editedSample].includes(payload.text));
    assert(!headers.has('Authorization'));
    if (gatewayStatus !== 200) return Response.json({ success: false }, { status: gatewayStatus });
    return Response.json({ success: true, data: {
      engine: 'deepseek', primary_copy: `Edited ${payload.target_market} ${payload.tone}`, alt_copy: 'A brighter start.',
      target_market: payload.target_market, tone: payload.tone, cta_options: ['See more.', 'Learn more.'],
      adaptations: [], matched_glossary_terms: [],
      ...gatewayOverrides,
    } });
  }
  assert.equal(url.href, provider);
  assert.equal(headers.get('Authorization'), `Bearer ${mockedKey}`);
  assert.equal(payload.model, 'deepseek-flash');
  return Response.json({ choices: [{ finish_reason: 'stop', message: { content: JSON.stringify({
    primary_copy: 'Bring a brighter note to your morning.', alt_copy: 'A brighter start.',
    cta_options: ['See what’s new.', 'Explore more.'], adaptations: [],
  }) } }] });
};

async function browser(endpoint = '', key = '') {
  const stored = new Map(key ? [['brandlex_deepseek_key', key]] : []);
  const storage = map => ({ getItem: name => map.get(name) ?? null, setItem: (name, value) => map.set(name, value),
    removeItem: name => map.delete(name) });
  globalThis.localStorage = storage(new Map());
  globalThis.sessionStorage = storage(stored);
  globalThis.document = { baseURI: site, querySelector: () => endpoint && { content: endpoint } };
  delete require.cache[enginePath];
  require(enginePath);
  const engine = globalThis.BrandLexStaticEngine;
  let { data } = await engine.request('/api/bootstrap');
  assert.equal(data.is_admin, false);
  const post = async (path, body) => {
    const result = await engine.request(path, {
      method: 'POST', headers: { 'X-CSRF-Token': data.csrf_token }, body: JSON.stringify(body),
    });
    if (result.data.csrf_token) data = result.data;
    return result.data;
  };
  return {
    rewrite: (text, target_market, tone) => post('/api/rewrite', { text, target_market, tone }),
    logout: () => post('/api/admin/logout', {}),
  };
}

(async () => {
  const publicUser = await browser(gateway);
  const outputs = new Set();
  for (const region of ['hk', 'cn', 'en']) {
    for (const tone of ['standard', 'social', 'concise']) {
      const report = await publicUser.rewrite(draft, region, tone);
      assert.equal(report.engine, 'deepseek');
      assert.equal(report.engine_source, 'live');
      outputs.add(report.primary_copy);
    }
  }
  assert.equal(outputs.size, 9);
  assert.deepEqual(calls.splice(0), Array(9).fill(gateway));
  assert.equal((await publicUser.rewrite(cache.drafts[0].text, 'en', 'standard')).engine_source, 'cache');
  assert.deepEqual(calls, []);
  assert.equal((await publicUser.rewrite(editedSample, 'en', 'standard')).engine_source, 'live');
  assert.deepEqual(calls.splice(0), [gateway]);

  for (const overrides of [
    { matched_glossary_terms: [{ id: '1" data-fixture="unsafe' }] },
    { adaptations: [{ original: draft, adapted: 'Edited', reason: '精炼表达', term_id: '1' }] },
  ]) {
    gatewayOverrides = overrides;
    const invalid = await publicUser.rewrite(draft, 'en', 'standard');
    assert.equal(invalid.engine, 'local');
    assert.deepEqual(calls.splice(0), [gateway]);
  }
  gatewayOverrides = {};

  const oversized = await publicUser.rewrite('字'.repeat(4001), 'hk', 'standard');
  assert.equal(oversized.engine, 'local');
  assert.match(oversized.notice, /4,000 字/);
  assert.deepEqual(calls, []);

  gatewayStatus = 429;
  const limited = await publicUser.rewrite(draft, 'en', 'standard');
  assert.equal(limited.engine, 'local');
  assert.match(limited.notice, /稍后重试/);
  assert.deepEqual(calls.splice(0), [gateway]);

  const byok = await browser(gateway, mockedKey);
  assert.equal((await byok.rewrite(cache.drafts[0].text, 'en', 'standard')).engine_source, 'cache');
  assert.deepEqual(calls, []);
  await byok.logout();
  const direct = await byok.rewrite(draft, 'en', 'standard');
  assert.equal(direct.engine, 'deepseek');
  assert(!/\p{Script=Han}/u.test(direct.primary_copy));
  assert.deepEqual(calls.splice(0), [provider]);

  const offline = await browser();
  const local = await offline.rewrite(draft, 'en', 'standard');
  assert.equal(local.engine, 'local');
  assert.match(local.notice, /全文改写/);
  assert.deepEqual(calls, []);
})().catch(error => { process.stderr.write(`${error.stack}\n`); process.exitCode = 1; });
