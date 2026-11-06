const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const { resolve } = require('node:path');
const test = require('node:test');
const { rewrite } = require('../static/js/static_rewrite.js');

const MARKETS = ['hk', 'cn', 'en'];
const TONES = ['standard', 'social', 'concise'];
const DRAFT = '周末有一场读书会。';
const TRANSLATION = {
  primary_copy: 'Join the weekend book club.', alt_copy: 'Make time for the weekend reading circle.',
  adaptations: [], cta_options: ['Explore the book club.', 'See what we are reading this weekend.'],
};

function deepSeekResponse(result) {
  return new Response(JSON.stringify({ choices: [{ finish_reason: 'stop', message: { content: JSON.stringify(result) } }] }));
}

test('direct personal-key requests use the same nine prompts as Flask', async t => {
  const python = process.env.BRANDLEX_TEST_PYTHON || 'python3';
  const backendPrompts = JSON.parse(execFileSync(python, ['-c', `
import json
from core.ai_rewriter import _system_prompt
print(json.dumps({f"{market}:{tone}": _system_prompt(market, tone, [], [])
                  for market in ("hk", "cn", "en") for tone in ("standard", "social", "concise")}))
`], { cwd: resolve(__dirname, '..'), encoding: 'utf8' }));
  const original = globalThis.fetch;
  t.after(() => { globalThis.fetch = original; });
  const resultTexts = new Set();
  const requests = [];
  globalThis.fetch = async (url, options) => {
    requests.push({ url, options, payload: JSON.parse(options.body) });
    return deepSeekResponse({ ...TRANSLATION, primary_copy: `Weekend book club. Version ${requests.length}.` });
  };
  for (const region of MARKETS) {
    for (const tone of TONES) {
      const result = await rewrite({ draft: DRAFT, region, tone }, { key: 'test-personal-key' });
      assert.equal(result.engine_source, 'live');
      resultTexts.add(result.primary_copy);
      const { url, options, payload } = requests.at(-1);
      assert.equal(url, 'https://api.deepseek.com/chat/completions');
      assert.equal(options.credentials, 'omit');
      assert.equal(options.redirect, undefined);
      assert.equal(options.cache, 'no-store');
      assert.equal(options.headers.Accept, 'application/json');
      assert.equal(payload.model, 'deepseek-flash');
      assert.equal(payload.temperature, { standard: 0.5, social: 0.75, concise: 0.35 }[tone]);
      assert.deepEqual(payload.thinking, { type: 'disabled' });
      assert.equal(payload.messages[0].content, backendPrompts[`${region}:${tone}`]);
      assert.deepEqual(JSON.parse(payload.messages[1].content), { source_draft: DRAFT });
    }
  }
  assert.equal(requests.length, 9);
  assert.equal(resultTexts.size, 9);
});

test('direct rewrite verifies exact output quotes despite casing and surrounding spaces', async t => {
  const original = globalThis.fetch;
  t.after(() => { globalThis.fetch = original; });
  globalThis.fetch = async () => deepSeekResponse({ ...TRANSLATION, adaptations: [
    { original: '  WEEKEND BOOK CLUB ', adapted: ' the WEEKEND READING CIRCLE ', reason: '英文社群语感', term_id: 999 },
    { original: 'Weekend Book Club', adapted: 'the weekend reading circle', reason: '重复', term_id: null },
    { original: 'Weekend Book Club', adapted: 'club.\nMake time', reason: '跨版本', term_id: null },
    { original: 'Fictional offer', adapted: 'Join the weekend book club', reason: '虚构', term_id: null },
  ] });
  const result = await rewrite({ draft: 'Join our Weekend Book Club.', region: 'en', tone: 'social' }, { key: 'test' });
  assert.deepEqual(result.adaptations, [{ original: 'Weekend Book Club', adapted: 'the weekend reading circle',
    reason: '英文社群语感', term_id: null }]);
});

test('a known Flash demo stays available without a personal-key call', async t => {
  const original = globalThis.fetch;
  t.after(() => { globalThis.fetch = original; });
  const requests = [];
  globalThis.fetch = async (...args) => { requests.push(args); return deepSeekResponse(TRANSLATION); };
  const cache = { version: 1, model: 'deepseek-flash', drafts: [{ text: DRAFT,
    rewrites: { 'en:social': { ...TRANSLATION, engine: 'deepseek', matched_term_ids: [] } } }] };
  const result = await rewrite({ draft: DRAFT, region: 'en', tone: 'social' }, { cache, key: 'test' });
  assert.equal(result.engine_source, 'cache');
  assert.equal(requests.length, 0);
});

test('live result preserves target-market grammar and caps confirmed changes', async t => {
  const original = globalThis.fetch;
  t.after(() => { globalThis.fetch = original; });
  const terms = [{ id: 29, term_en: 'Value for Money', term_hk: '抵買', term_cn: '高性价比', aliases: ['性价比'] },
    { id: 26, term_en: 'Gift with Purchase', term_hk: '買滿即送', term_cn: '满赠礼遇', aliases: ['买满即送'] }];
  const sourceBits = Array.from({ length: 8 }, (_, i) => `原詞${i}`);
  const outputBits = Array.from({ length: 8 }, (_, i) => `改写${i}`);
  const primary = `性价比挺高，买满即送明信片。${outputBits.join('，')}。`;
  globalThis.fetch = async () => deepSeekResponse({
    primary_copy: primary, alt_copy: '领取明信片前，请查看满赠礼遇。', cta_options: ['查看详情。', '了解活动规则。'],
    adaptations: sourceBits.map((original, i) => ({ original, adapted: outputBits[i], reason: '小红书表达' })),
  });
  const result = await rewrite({ draft: `性价比高，買滿即送。${sourceBits.join('，')}。`, region: 'cn', tone: 'social' },
    { key: 'test', terms });
  assert.equal(result.primary_copy, primary);
  assert.equal(result.adaptations.length, 6);
  assert.equal(result.adaptations[0].term_id, 26);
  assert.deepEqual(result.adaptations.slice(1).map(row => row.original), sourceBits.slice(0, 5));
});
