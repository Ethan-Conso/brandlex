const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { webcrypto } = require('node:crypto');

const [output, gateway] = process.argv.slice(2);
const site = 'https://example.github.io/brandlex/';
const provider = 'https://api.deepseek.com/chat/completions';
const draft = '让平凡的日常多点新意。';
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

async function browser(endpoint = '', key = '', edits) {
  const stored = new Map(key ? [['brandlex_deepseek_key', key]] : []);
  const storage = map => ({ getItem: name => map.get(name) ?? null, setItem: (name, value) => map.set(name, value),
    removeItem: name => map.delete(name) });
  globalThis.localStorage = storage(new Map(edits ? [['brandlex_static_edits', JSON.stringify(edits)]] : []));
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
    engine,
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
  gatewayOverrides = { engine: 'fallback', error_code: 'factual_mismatch' };
  const mismatch = await publicUser.rewrite(draft, 'en', 'standard');
  assert.equal(mismatch.engine, 'local');
  assert.match(mismatch.notice, /与原稿不一致/);
  assert.deepEqual(calls.splice(0), [gateway]);
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

  const firstTerm = (await offline.engine.request('/api/terms/1')).data;
  const localName = 'Saved Draft Overlay';
  const updated = await browser('', '', { records: {
    3204: { ...firstTerm, id: 3204, term_en: localName },
    3205: null,
    3208: { ...firstTerm, id: 3208, term_en: 'Another Saved Overlay' },
  } });
  const newDefaults = await Promise.all([3204, 3205].map(id => updated.engine.request(`/api/terms/${id}`)));
  assert(newDefaults.every(({ data }) => data.term_en !== localName && data.meaning.includes(' EN: ')));
  const relocated = (await updated.engine.request('/api/terms?q=Saved+Draft+Overlay')).data.terms[0];
  assert.equal(relocated.term_en, localName);
  assert(relocated.id > 3208);
  assert.equal((await updated.engine.request('/api/terms/3208')).data.term_en, 'Pay-Per-Click (PPC)');
  const another = (await updated.engine.request('/api/terms?q=Another+Saved+Overlay')).data.terms[0];
  assert.equal(another.term_en, 'Another Saved Overlay');
  assert(another.id > 3208 && another.id !== relocated.id);

  const previous = await browser('', '', { seedMaxId: 3207, records: { 3205: null, 3208: null } });
  await assert.rejects(previous.engine.request('/api/terms/3205'), { status: 404 });
  assert.equal((await previous.engine.request('/api/terms/3208')).data.term_en, 'Pay-Per-Click (PPC)');
})().catch(error => { process.stderr.write(`${error.stack}\n`); process.exitCode = 1; });
