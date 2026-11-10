async (page) => {
  const assert = (condition, message) => { if (!condition) throw new Error(message); };
  const base = new URL(page.url());
  assert(base.hostname === '127.0.0.1' && base.pathname === '/brandlex/',
    'Open the disposable static site at http://127.0.0.1:<port>/brandlex/.');

  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => {
    const url = new URL(request.url());
    if (url.origin === base.origin && /\/api\//.test(url.pathname)) errors.push(`Unexpected server request: ${url}`);
  });
  page.on('response', response => {
    const url = new URL(response.url());
    if (url.origin === base.origin && !response.ok() && response.status() !== 304) {
      errors.push(`Failed asset: ${url} (${response.status()})`);
    }
  });

  await page.evaluate(() => { localStorage.clear(); sessionStorage.clear(); });
  await page.reload();
  const $ = selector => page.locator(selector);
  const gateway = await $('meta[name="brandlex-public-rewrite-url"]').getAttribute('content', { timeout: 1000 }).catch(() => null);
  const gatewayCalls = [];
  if (gateway) await page.route(gateway, async route => {
    const headers = { 'access-control-allow-origin': base.origin, 'access-control-allow-methods': 'POST, OPTIONS',
      'access-control-allow-headers': 'content-type, accept' };
    if (route.request().method() === 'OPTIONS') return route.fulfill({ status: 204, headers });
    const body = route.request().postDataJSON();
    gatewayCalls.push({ body, authorization: await route.request().headerValue('authorization') });
    const copy = {
      hk: ['春日禮盒現已推出，香港免運費。', '選購春日禮盒。'],
      cn: ['春日礼盒现已推出，香港包邮。', '选购春日礼盒。'],
      en: ['Meet the spring gift set, with free shipping in Hong Kong.', 'Shop the spring gift set.'],
    }[body.target_market];
    return route.fulfill({ headers, json: { success: true, data: {
      primary_copy: copy[0], alt_copy: copy[1], cta_options: [copy[1], copy[1]], adaptations: [], matched_glossary_terms: [],
      engine: 'deepseek', target_market: body.target_market, tone: body.tone,
    } } });
  });
  const api = (path, options = {}) => page.evaluate(async ({ path, options }) => {
    const engine = window.BrandLexStaticEngine;
    if (options.method) {
      const { data } = await engine.request('/api/bootstrap');
      return engine.request(path, { ...options, headers: { 'X-CSRF-Token': data.csrf_token } });
    }
    return engine.request(path, options);
  }, { path, options });
  const cards = $('#case-feed-grid > [data-term-id]');
  const waitCards = (count, category = '') => page.waitForFunction(({ count, category }) => {
    const grid = document.querySelector('#case-feed-grid');
    const items = [...grid.querySelectorAll('[data-term-id]')];
    return grid.getAttribute('aria-busy') === 'false' && items.length === count
      && (!category || items.every(item => item.dataset.categoryName === category));
  }, { count, category });
  const ids = () => cards.evaluateAll(items => items.map(item => Number(item.dataset.termId)));
  const result = () => $('#output-content').waitFor({ state: 'visible' });
  const search = async value => {
    await $('#library-search').fill(value);
    await page.waitForFunction(() => document.querySelector('#library-count').textContent.includes('匹配')
      && document.querySelector('#case-feed-grid').getAttribute('aria-busy') === 'false');
  };

  await page.waitForFunction(() => document.querySelectorAll('[data-sample]').length === 4);
  assert(await $('#view-home').isVisible(), 'Homepage opens by default');
  const { data: bootstrap } = await api('/api/bootstrap');
  assert(bootstrap.total === 3208 && bootstrap.categories.length === 12 && !bootstrap.is_admin,
    'Complete seed and public startup');
  const publicStatus = await page.evaluate(async token => {
    try {
      await window.BrandLexStaticEngine.request('/api/terms/1', { method: 'DELETE', headers: { 'X-CSRF-Token': token } });
    } catch (error) { return error.status; }
    return 200;
  }, bootstrap.csrf_token);
  assert(publicStatus === 403, 'Public sessions cannot delete terms');
  await $('#home-edit-draft').click();
  await result();
  assert(await $('#view-studio').isVisible(), 'Homepage draft opens Studio and runs a rewrite');
  assert((await $('#rewritten-copy').innerText()).includes('HK$280'), 'Rewrite keeps the homepage offer');
  assert(await $('.adaptation-row').count() > 0, 'Displays homepage terminology adaptations');
  const homeDraft = await $('#copy-text').inputValue();
  const primary = await $('#rewritten-copy').innerText();
  await $('#version-alt').click();
  assert((await $('#rewritten-copy').innerText()) !== primary, 'Alternate rewrite is distinct');
  const rewriteMatrix = await page.evaluate(async drafts => {
    const results = [];
    const engine = window.BrandLexStaticEngine;
    const { data: { csrf_token } } = await engine.request('/api/bootstrap');
    for (const text of drafts) {
      for (const target_market of ['hk', 'cn', 'en']) {
        for (const tone of ['standard', 'social', 'concise']) {
          const { data } = await engine.request('/api/rewrite', {
            method: 'POST', headers: { 'X-CSRF-Token': csrf_token }, body: JSON.stringify({ text, target_market, tone }),
          });
          if (!data.primary_copy?.trim() || !data.alt_copy?.trim() || data.primary_copy === data.alt_copy
            || !Array.isArray(data.adaptations) || !data.cta_options?.length
            || data.notice?.includes('未配置 DeepSeek 密钥')) {
            throw new Error(`Invalid rewrite for ${target_market}/${tone}: ${text.slice(0, 20)}`);
          }
          results.push(data.engine_source);
        }
      }
    }
    return results;
  }, [homeDraft, ...bootstrap.samples.map(sample => sample.text)]);
  assert(rewriteMatrix.length === 45 && rewriteMatrix.every(source => source === 'cache'),
    'Homepage plus four samples have cached DeepSeek outputs for every market and tone');
  assert(!gatewayCalls.length, 'Exact examples never send a live request');
  assert(!(await $('#engine-notice').innerText()).includes('未配置 DeepSeek 密钥'), 'No missing-key warning');

  await $('#tab-library').click();
  await waitCards(6);
  assert(await $('#category-filters [data-category]').count() === 13, 'Twelve category pills and All');
  assert(new Set(await cards.evaluateAll(items => items.map(item => item.dataset.categoryName))).size === 6,
    'Unfiltered feed samples six distinct categories');
  const previous = await ids();
  await $('#shuffle-feed').click();
  await waitCards(6);
  assert((await ids()).every(id => !previous.includes(id)), 'Shuffle excludes the prior batch');
  const category = bootstrap.categories[1];
  await $(`#category-filters [data-category="${category}"]`).click();
  await waitCards(6, category);
  await $('#category-filters [data-category=""]').click();
  await waitCards(6);
  await search('Ｐｒｏｄｕｃｔ Ｓｅｅｄｉｎｇ');
  const seedCard = cards.filter({ hasText: 'Product Seeding' }).first();
  const seedId = await seedCard.getAttribute('data-term-id');
  await seedCard.locator('[data-open-term]').click();
  await $('#term-drawer .drawer-good').waitFor();
  assert(await $('#drawer-title').innerText() === 'Product Seeding', 'NFKC lookup and complete drawer');
  const definitions = $('#term-drawer .drawer-definitions p');
  assert(await definitions.count() === 2 && await definitions.first().getAttribute('lang') === 'zh-CN'
    && await definitions.last().getAttribute('lang') === 'en'
    && (await definitions.last().innerText()).startsWith('EN: '), 'Both definitions are visible, Chinese first for HK');
  await $('#term-drawer [data-language="en"]').click();
  assert(await definitions.first().getAttribute('lang') === 'en'
    && await definitions.last().getAttribute('lang') === 'zh-CN', 'English selection shows the English definition first');
  await page.keyboard.press('Escape');
  await seedCard.locator('[data-try-case]').click();
  await result();
  assert(await $('#view-studio').isVisible(), '试改 starts a custom draft rewrite');
  if (gateway) {
    assert(gatewayCalls.length === 1 && gatewayCalls[0].authorization === null
      && gatewayCalls[0].body.text === await $('#copy-text').inputValue(), 'Public 试改 sends the case to the relay without a key');
    assert(await $('#engine-label').innerText() === 'DeepSeek', 'The case result is live');
  }
  await $('#copy-text').fill('春日礼盒上线，香港包邮。');
  await $('[data-market="hk"]').click();
  await $('#rewrite-copy').click();
  await result();
  assert((await $('#rewritten-copy').innerText()).includes('免運費'), 'A custom draft uses the HK term');
  if (gateway) {
    await $('[data-market="en"]').click();
    await $('[data-tone="social"]').click();
    await $('#rewrite-copy').click();
    await result();
    assert(gatewayCalls.length === 3 && gatewayCalls[2].authorization === null
      && gatewayCalls[2].body.target_market === 'en' && gatewayCalls[2].body.tone === 'social',
    'Public custom draft goes to the relay with the selected market and tone');
    assert(await $('#engine-label').innerText() === 'DeepSeek'
      && !/\p{Script=Han}/u.test(await $('#rewritten-copy').innerText()), 'Public custom draft returns translated live copy');
  }

  const deepSeek = 'https://api.deepseek.com/chat/completions';
  const mockKey = 'brandlex-playwright-fixture-key';
  const liveCalls = [];
  let failLive = false;
  const mockModel = async route => {
    const headers = {
      'access-control-allow-origin': base.origin, 'access-control-allow-methods': 'POST, OPTIONS',
      'access-control-allow-headers': 'authorization, content-type',
    };
    if (route.request().method() === 'OPTIONS') return route.fulfill({ status: 204, headers });
    liveCalls.push({ key: await route.request().headerValue('authorization'), payload: route.request().postDataJSON() });
    if (failLive) return route.fulfill({ status: 401, headers, json: { error: 'fixture failure' } });
    const output = { primary_copy: '春日礼盒现已上线，香港包邮。', alt_copy: '春日礼盒，香港包邮。',
      adaptations: [], cta_options: ['选购礼盒。', '了解礼盒详情。'] };
    return route.fulfill({ headers, json: { choices: [{ finish_reason: 'stop', message: { content: JSON.stringify(output) } }] } });
  };
  await page.route(deepSeek, mockModel);
  try {
    assert(await $('#admin-label').innerText() === '维护模式', 'Personal DeepSeek settings are available without maintenance');
    await $('#deepseek-key-toggle').click();
    await $('#deepseek-key-input').fill(mockKey);
    await $('#deepseek-key-form [type="submit"]').click();
    await $('#deepseek-key-dialog').waitFor({ state: 'hidden' });
    const liveDraft = '春日礼盒上线，香港包邮。';
    await $('#copy-text').fill(liveDraft);
    await $('[data-market="hk"]').click();
    await $('#rewrite-copy').click();
    await result();
    assert(liveCalls.length === 1 && liveCalls[0].key === `Bearer ${mockKey}`, 'Uses the optional session key in the browser');
    assert(liveCalls[0].payload.model === 'deepseek-flash', 'Direct browser calls use deepseek-flash');
    const [system, user] = liveCalls[0].payload.messages;
    const grounding = system.content.match(/^Mandatory Brand Glossary Constraints \(JSON data\): (.*)$/m)?.[1];
    assert(grounding && Buffer.byteLength(grounding) <= 690 && JSON.parse(grounding).terms.length <= 18
      && JSON.parse(user.content).source_draft === liveDraft, 'Live request includes bounded, separated grounding');
    assert(await $('#engine-label').innerText() === 'DeepSeek'
      && (await $('#rewritten-copy').innerText()).includes('香港免運費'), 'Live output is post-normalized and labeled');
    failLive = true;
    const cached = await api('/api/rewrite', {
      method: 'POST', body: JSON.stringify({ text: homeDraft, target_market: 'hk', tone: 'standard' }),
    });
    assert(cached.data.engine_source === 'cache' && liveCalls.length === 1, 'Exact sample cache is used before a personal key');
    await $('#rewrite-copy').click();
    await result();
    assert(liveCalls.length === 2 && (await $('#engine-notice').innerText()).includes('核对密钥'),
      'A rejected personal key produces a labeled local preview');
    await $('#deepseek-key-toggle').click();
    await $('#deepseek-key-form [type="submit"]').click();
    await $('#deepseek-key-dialog').waitFor({ state: 'hidden' });
    assert(await page.evaluate(() => window.BrandLexAPI.getDeepSeekKey() === ''), 'Clearing removes the session key');
  } finally { await page.unroute(deepSeek, mockModel); }

  await $('#tab-library').click();
  await $('#admin-toggle').click();
  await $('#admin-password').fill('incorrect-fixture');
  await $('#admin-submit').click();
  await $('#admin-error').waitFor();
  await $('#admin-password').fill('brandlex2026');
  await $('#admin-submit').click();
  await $('#admin-dialog').waitFor({ state: 'hidden' });
  const waitToast = message => page.waitForFunction(text => {
    const toast = document.querySelector('#toast');
    return toast.classList.contains('is-visible') && toast.textContent === text;
  }, message);
  await waitToast('维护模式已解锁（当前演示修改保存在本浏览器）');
  const fixtureName = 'BrandLex Pages Browser Fixture';
  await $('#view-library [data-action="add-term"]').click();
  await $('#fill-example').click();
  await $('#field-term-en').fill(fixtureName);
  await $('#save-term').click();
  await $('#term-dialog').waitFor({ state: 'hidden' });
  await waitToast('词条已保存在本浏览器');
  await search(fixtureName);
  const fixture = cards.filter({ hasText: fixtureName });
  await fixture.locator('[data-edit]').click();
  const updated = '品牌週末電子通訊 & <校驗>';
  await $('#field-term-hk').fill(updated);
  await $('#save-term').click();
  await fixture.filter({ hasText: updated }).waitFor();
  await waitToast('词条已保存在本浏览器');
  await page.reload();
  await $('#admin-logout').waitFor({ state: 'visible' });
  await search(fixtureName);
  await fixture.filter({ hasText: updated }).waitFor();
  assert(await page.evaluate(() => Boolean(localStorage.getItem('brandlex_static_edits'))), 'Edits are stored locally');

  for (const format of ['csv', 'tbx', 'json']) {
    await $('.app-header .export-menu summary').click();
    const pending = page.waitForEvent('download');
    await $(`.app-header .export-menu a[href$="/export/${format}"]`).click();
    const download = await pending;
    assert(download.suggestedFilename().endsWith(`.${format}`) && await download.failure() === null, `Download ${format}`);
  }
  const exportChecks = await page.evaluate(async ({ fixtureName, updated, seedTotal }) => {
    const output = format => window.BrandLexStaticEngine.request(`/api/export/${format}`);
    const csv = (await output('csv')).blob;
    const bom = [...new Uint8Array(await csv.slice(0, 3).arrayBuffer())].join(',');
    const tbx = await (await output('tbx')).blob.text();
    const xml = new DOMParser().parseFromString(tbx, 'application/xml');
    const data = JSON.parse(await (await output('json')).blob.text());
    return {
      csv: bom === '239,187,191' && (await csv.text()).includes(updated),
      tbx: xml.documentElement.localName === 'martif' && xml.documentElement.getAttribute('type') === 'TBX-Basic'
        && !xml.querySelector('parsererror') && xml.documentElement.textContent.includes(updated),
      json: data.length === seedTotal + 1 && data.some(record => record.term_en === fixtureName && record.term_hk === updated),
    };
  }, { fixtureName, updated, seedTotal: bootstrap.total });
  assert(Object.values(exportChecks).every(Boolean), `Export content: ${JSON.stringify(exportChecks)}`);

  await fixture.locator('[data-delete]').click();
  await $('#confirm-action').click();
  await waitCards(0);
  await waitToast('词条已保存在本浏览器');
  await search('Product Seeding');
  const seeded = $(`#case-feed-grid > [data-term-id="${seedId}"]`);
  await seeded.locator('[data-delete]').click();
  await $('#confirm-action').click();
  await seeded.waitFor({ state: 'detached' });
  assert((await api('/api/bootstrap')).data.total === bootstrap.total - 1, 'Deleting a seed term persists as a local override');
  await $('#library-search').fill('');
  await waitCards(6);
  await $('#reset-library').click();
  await $('#confirm-action').click();
  await $('#confirm-dialog').waitFor({ state: 'hidden' });
  assert((await api('/api/bootstrap')).data.total === bootstrap.total, 'Reset restores the seed corpus');
  await $('#admin-logout').click();
  await $('#confirm-action').click();
  await $('#admin-logout').waitFor({ state: 'hidden' });
  assert(!await $('#view-library [data-action="add-term"]').isVisible(), 'Logout closes maintenance actions');
  assert(!errors.length, errors.join('\n'));
  const warmP95Milliseconds = await page.evaluate(async id => {
    const engine = window.BrandLexStaticEngine;
    const paths = {
      search: '/api/terms?q=防晒', category: '/api/terms?category=合规与风控&mode=feed',
      shuffle: `/api/terms?mode=feed&exclude=${id}`, detail: `/api/terms/${id}`,
    };
    const timings = {};
    for (const [name, path] of Object.entries(paths)) {
      await engine.request(path);
      const samples = [];
      for (let run = 0; run < 100; run += 1) {
        const start = performance.now();
        await engine.request(path);
        samples.push(performance.now() - start);
      }
      samples.sort((left, right) => left - right);
      timings[name] = Number(samples[94].toFixed(3));
    }
    return timings;
  }, seedId);
  return { passed: true, rewrites: rewriteMatrix.length, cached: rewriteMatrix.filter(source => source === 'cache').length,
    gatewayCalls: gatewayCalls.length,
    exportChecks, warmP95Milliseconds };
}
