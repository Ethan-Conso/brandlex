const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const { resolve } = require('node:path');
const test = require('node:test');
const { rewrite, verifyFactualFidelity } = require('../static/js/static_rewrite.js');
const bundledCache = require('../data/pages_rewrites.json');
const marketingFacts = require('./rewrite_marketing_facts.json');

const MARKETS = ['hk', 'cn', 'en'];
const TONES = ['standard', 'social', 'concise'];
const DRAFT = '周末有一场读书会。';
const TRANSLATION = {
  primary_copy: 'Join the weekend book club.', alt_copy: 'Make time for the weekend reading circle.',
  adaptations: [], cta_options: ['Explore the book club.', 'See what we are reading this weekend.'],
};

const FIDELITY_CASES = [
  { name: 'rewritten price and date', region: 'hk', draft: '禮盒售價 HK$280，11月30日發售。',
    primary: '禮盒售價 HK$820，12月31日發售。', alt: '禮盒售價 HK$820，12月31日發售。', expected: 'local' },
  { name: 'required price omitted from the alternate', region: 'en', draft: '禮盒售價 HK$280，11月30日發售。',
    primary: 'The gift set launches on November 30 for HK$280.', alt: 'Shop the gift set on 30 November.', expected: 'local' },
  { name: 'conflicting price in a call to action', region: 'en', draft: '禮盒售價 HK$280，11月30日發售。',
    primary: 'The gift set launches on November 30 for HK$280.', alt: 'Shop the gift set on 30 November for HK$280.',
    cta: 'Order the gift set for HK$820.', expected: 'local' },
  { name: 'a three-day offer described as two days', region: 'hk', draft: '11月15至17日預訂享早鳥禮遇 HK$280。',
    primary: '11月15至17日預訂享早鳥禮遇 HK$280。記低呢兩日！',
    alt: '早鳥禮遇 HK$280，11月15至17日預訂。', expected: 'local' },
  { name: 'the inclusive date window and currency are translated', region: 'en', draft: '11月15至17日預訂享早鳥禮遇 HK$280。',
    primary: 'Order between 15 and 17 November for HK$280. The offer lasts three days.',
    alt: 'Book for HK$280 from November 15 to 17.', cta: 'Book between November 15 and 17.', expected: 'live' },
  { name: 'Chinese discount converts to percent off', region: 'en', draft: '本週會員享85折。',
    primary: 'Get 15% off with your membership.', alt: 'Members save 15% this week.', expected: 'live' },
  { name: 'English discount converts to Chinese', region: 'cn', draft: 'Save 20% this week.',
    primary: '本周享8折。', alt: '本周活动八折。', expected: 'live' },
  { name: 'Chinese written numbers convert to Arabic digits', region: 'en', draft: '每盒二十件。满299包邮。',
    primary: 'Each set contains 20 pieces. Free shipping on orders of 299 or more.',
    alt: 'Get 20 items per box with free shipping from 299.', expected: 'live' },
  { name: 'a minimum-spend amount cannot become an unconditional price', region: 'en', draft: '满299包邮。',
    primary: 'The set costs 299 and ships free.', alt: 'Free shipping on orders of 299 or more.', expected: 'local' },
  { name: 'amount and date may use localized words', region: 'en', draft: '禮盒售價 HK$280，11月30日發售。',
    primary: 'The gift set launches on November the thirtieth for 280 Hong Kong dollars.',
    alt: 'Discover the gift set on November 30 for HKD 280.', expected: 'live' },
  { name: 'monthless date and bare labelled price are preserved', region: 'en', draft: '禮盒30日發售，售價：280。',
    primary: 'The gift set launches on the 30th. Price: 280.', alt: 'Shop the gift set on the 30th. It costs 280.', expected: 'live' },
  { name: '24-hour and 12-hour time windows are equivalent', region: 'en', draft: '活動時間 11:00–18:00。',
    primary: 'Join us from 11 am to 6 pm.', alt: 'Come by between 11:00 and 18:00.',
    cta: 'We open at 11 am.', expected: 'live' },
  { name: 'one day in ordinary prose is not a timed claim', region: 'en', draft: '用新的方式开启平凡的一天。',
    primary: 'Start your day a little differently.', alt: 'Try something fresh in your routine.', expected: 'live' },
  { name: 'a booking URL is preserved verbatim including its path case', region: 'en',
    draft: 'Book at https://example.test/Events?slot=12&code=VIP.',
    primary: 'Book now at https://example.test/events?slot=12&code=VIP.',
    alt: 'Book at https://example.test/Events?slot=12&code=VIP.', expected: 'local' },
  { name: 'an alternate cannot omit a source URL', region: 'en', draft: 'Book at https://example.test/Book.',
    primary: 'Book now at https://example.test/Book.', alt: 'Get your booking in today.', expected: 'local' },
  { name: 'a call to action cannot invent a URL', region: 'en', draft: 'Book at https://example.test/Book.',
    primary: 'Book now at https://example.test/Book.', alt: 'Reserve at https://example.test/Book.',
    cta: 'Reserve at https://example.test/Offer.', expected: 'local' },
  { name: 'the source URL may be followed by localized punctuation', region: 'en',
    draft: '请到 https://example.test/Book?code=VIP 预订。',
    primary: 'Book now at https://example.test/Book?code=VIP.',
    alt: 'Reserve at https://example.test/Book?code=VIP.', expected: 'live' },
  { name: 'a rewrite cannot drop a limited quantity', region: 'en', draft: '限量 50 套。',
    primary: 'Available for a limited time.', alt: 'Only 50 sets are available.', expected: 'local' },
  { name: 'a rewrite must keep scarcity bound to the quantity', region: 'en', draft: '礼盒限量 50 套。',
    primary: 'Explore our 50 gift sets.', alt: 'Only 50 sets are available.', expected: 'local' },
  { name: 'a rewrite cannot replace bottles with boxes', region: 'en', draft: '礼盒内含 2 瓶。',
    primary: 'The gift set contains 2 bottles.', alt: 'Each gift set comes with 2 boxes.', expected: 'local' },
  { name: 'localized quantities preserve compatible units', region: 'en',
    draft: '限量 50 套，每套 2 瓶，每瓶 100ml，礼盒宽 20厘米。',
    primary: 'Only 50 sets are available, with two bottles per set. Each bottle holds 100 mL and the box is 20 cm wide.',
    alt: 'Limited to fifty sets. Each 20 cm gift box includes 2 bottles of 100 milliliters each.', expected: 'live' },
  { name: 'the same two prices cannot be swapped between named items', region: 'en',
    draft: 'LUMA is HK$280 and NOVA is HK$350.',
    primary: 'Get LUMA for HK$350 and NOVA for HK$280.',
    alt: 'Shop NOVA for HK$350 or LUMA for HK$280.', expected: 'local' },
  { name: 'two named items and their prices can change order', region: 'en',
    draft: 'LUMA 售价 HK$280，NOVA 售价 HK$350。',
    primary: 'Shop NOVA for HK$350 or LUMA for HK$280.',
    alt: 'Get LUMA for HK$280 and NOVA for HK$350.', expected: 'live' },
  { name: 'the offer membership qualifier is required in both versions', region: 'en', draft: '会员专享 HK$280。',
    primary: 'Members pay HK$280.', alt: 'Everyone can shop for HK$280.', expected: 'local' },
  { name: 'membership copy can use VIP eligibility', region: 'en', draft: '会员专享 HK$280。',
    primary: 'Pay HK$280 with your membership.', alt: 'Shop for HK$280 at the VIP rate.', expected: 'live' },
  { name: 'shipping scope cannot become order eligibility', region: 'hk', draft: '禮盒售價 HK$280，香港免運費。',
    primary: '禮盒售價 HK$280，香港免運費。', alt: '禮盒售價 HK$280，訂單僅限香港地區。', expected: 'local' },
  { name: 'free shipping may be limited geographically', region: 'en', draft: '禮盒售價 HK$280，香港免運費。',
    primary: 'Shop the gift set for HK$280 with free Hong Kong shipping.',
    alt: 'Get the gift set for HK$280. Free shipping is available in Hong Kong only.', expected: 'live' },
  { name: 'shipping negation in the alternate triggers the local fallback', region: 'hk',
    draft: '香港免運費。', primary: '香港免運費。', alt: '香港不免運費。', expected: 'local' },
  { name: 'shipping negation without a region still conflicts', region: 'en',
    draft: '包邮。', primary: 'Enjoy free shipping.', alt: 'Shipping is not free.', expected: 'local' },
  { name: 'a deadline cannot turn into an opening date', region: 'en',
    draft: '報名截止至11月30日。', primary: 'Registration closes on November 30.',
    alt: 'Registration starts on November 30.', expected: 'local' },
  { name: 'both versions keep membership on the same named product', region: 'en',
    draft: 'Members only: LUMA. NOVA is open to everyone.',
    primary: 'LUMA is for members only. Everyone can shop NOVA.',
    alt: 'Everyone can shop LUMA. NOVA is for members only.', expected: 'local' },
  { name: 'distinct quantities cannot move between products', region: 'en',
    draft: 'LUMA contains 2 bottles. NOVA contains 3 bottles.',
    primary: 'LUMA includes two bottles and NOVA includes three bottles.',
    alt: 'LUMA includes three bottles and NOVA includes two bottles.', expected: 'local' },
  { name: 'unchanged URLs cannot be attached to the wrong products', region: 'en',
    draft: 'LUMA: https://example.test/Offer1. NOVA: https://example.test/Offer2.',
    primary: 'Visit LUMA at https://example.test/Offer1 and NOVA at https://example.test/Offer2.',
    alt: 'Visit LUMA at https://example.test/Offer2 and NOVA at https://example.test/Offer1.', expected: 'local' },
  { name: 'named products can change order when their quantities and links follow them', region: 'en',
    draft: 'LUMA contains 2 bottles: https://example.test/Offer1. NOVA contains 3 bottles: https://example.test/Offer2.',
    primary: 'NOVA includes three bottles: https://example.test/Offer2. LUMA includes two bottles: https://example.test/Offer1.',
    alt: 'LUMA includes two bottles: https://example.test/Offer1. NOVA includes three bottles: https://example.test/Offer2.', expected: 'live' },
];

function deepSeekResponse(result) {
  return new Response(JSON.stringify({ choices: [{ finish_reason: 'stop', message: { content: JSON.stringify(result) } }] }));
}

test('direct rewrites verify the source facts in both versions and calls to action', async t => {
  const original = globalThis.fetch;
  t.after(() => { globalThis.fetch = original; });
  for (const entry of FIDELITY_CASES) {
    globalThis.fetch = async () => deepSeekResponse({
      primary_copy: entry.primary, alt_copy: entry.alt, adaptations: [],
      cta_options: entry.region === 'en' ? [entry.cta ?? 'Learn more.', 'See the details.'] : ['了解详情。', '查看更多。'],
    });
    const result = await rewrite({ draft: entry.draft, region: entry.region, tone: 'standard' }, { key: 'test' });
    assert.equal(result.engine_source, entry.expected, entry.name);
    assert.equal(result.error_code, entry.expected === 'local' ? 'factual_mismatch' : null, entry.name);
  }
});

test('all 45 bundled rewrites pass the browser fact checker', () => {
  let checked = 0;
  for (const draft of bundledCache.drafts) {
    for (const [key, result] of Object.entries(draft.rewrites)) {
      assert.doesNotThrow(() => verifyFactualFidelity(draft.text, result.primary_copy, result.alt_copy, result.cta_options),
        draft.id + ' ' + key);
      checked += 1;
    }
  }
  assert.equal(checked, 45);
});

test('the browser passes the shared Python and JavaScript marketing fact cases', () => {
  for (const { name, source, primary, alt, cta, valid } of marketingFacts) {
    const check = () => verifyFactualFidelity(source, primary, alt, cta ? [cta] : []);
    if (valid) assert.doesNotThrow(check, name);
    else assert.throws(check, /Factual mismatch in DeepSeek rewrite/, name);
  }
});

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
    return deepSeekResponse({ ...TRANSLATION, primary_copy: `Weekend book club. Version ${'ABCDEFGHI'[requests.length - 1]}.` });
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
