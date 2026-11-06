async (page) => {
  const assert = (value, message) => { if (!value) throw new Error(message); };
  const base = new URL(page.url()).origin;
  assert(base === 'http://127.0.0.1:5063', 'Mutation tests require disposable loopback server port 5063.');
  await page.goto(base + '/?test=library&run=' + Date.now() + '#library');
  const pageSize = 12;
  const feedSize = 6;
  const gridSelector = '#case-feed-grid';
  const cards = page.locator(gridSelector + ' > [data-term-id]');
  const status = page.locator('#library-count');
  const shuffle = page.locator('#shuffle-feed');
  const bottomShuffle = page.locator('[data-action="shuffle-feed"]');
  const more = page.locator('#load-more-terms');
  const input = page.locator('#library-search');
  const bootstrap = await page.evaluate(async () => (await (await fetch('/api/bootstrap')).json()).data);
  const format = new Intl.NumberFormat('zh-CN').format;
  const waitStatus = value => page.waitForFunction(text =>
    document.querySelector('#library-count').textContent.includes(text), value);
  const waitTotal = total => waitStatus('共 ' + format(total) + ' 组');
  const waitCards = (count, category = '') => page.waitForFunction(({count, category}) => {
    const grid = document.querySelector('#case-feed-grid');
    const records = [...grid.querySelectorAll('[data-term-id]')];
    return grid.getAttribute('aria-busy') === 'false' && records.length === count
      && (!category || records.every(card => card.dataset.categoryName === category));
  }, {count, category});
  const cardIds = () => cards.evaluateAll(items => items.map(card => Number(card.dataset.termId)));
  const cardCategories = () => cards.evaluateAll(items => items.map(card => card.dataset.categoryName));
  async function checkDiversity() {
    const categories = await cardCategories();
    assert(categories.every(name => bootstrap.categories.includes(name)), 'Each card has a known category');
    assert(new Set(categories).size === feedSize, 'Unfiltered recommendations span six different categories');
  }
  const matchResponse = filters => response => {
    const url = new URL(response.url());
    return url.origin === base && url.pathname === '/api/terms' && response.ok()
      && Object.entries(filters).every(([key, value]) => (url.searchParams.get(key) ?? '') === value);
  };
  const checkDifferent = (before, after) => {
    assert(before.slice().sort().join(',') !== after.slice().sort().join(','), 'Random draw changes the set');
  };
  async function shuffleCards(button, category = '') {
    const previous = await cardIds();
    const pending = page.waitForResponse(matchResponse({mode: 'feed', q: '', category}));
    await button.click();
    const response = await pending;
    await waitCards(feedSize, category);
    const excluded = new URL(response.url()).searchParams.get('exclude')?.split(',').map(Number);
    assert(previous.every(id => excluded?.includes(id)), 'Shuffle requests exclusion of the previous draw');
    const fresh = await cardIds();
    assert(fresh.every(id => !previous.includes(id)), 'Shuffle avoids all prior cases when enough cases exist');
    assert(new Set(fresh).size === feedSize, 'No duplicate cards in one batch');
    if (!category) await checkDiversity();
    return fresh;
  }
  async function search(value) {
    const pending = page.waitForResponse(matchResponse({q: value}));
    await input.fill(value);
    const response = await pending;
    const payload = (await response.json()).data;
    await waitCards(payload.terms.length);
    const summary = value ? '匹配 ' + format(payload.matched_total) + ' 组' : '随机推荐 ' + feedSize + ' 组';
    await waitStatus(summary);
    if (value) assert(await status.innerText() === summary, 'Search status shows only its result count');
    return payload;
  }

  await page.context().grantPermissions(['clipboard-read', 'clipboard-write']);
  await waitCards(feedSize);
  await waitTotal(bootstrap.total);
  assert(bootstrap.total >= 3200 && bootstrap.categories.length === 12, 'Scaled fixture');
  assert(bootstrap.terms.length === feedSize
    && bootstrap.terms.every(term => term.good_example_hk && term.usage_tip
      && typeof term.learning_tip === 'string' && [...term.learning_tip].length <= 22),
  'Bootstrap carries complete case records and short takeaways');
  assert(await page.locator('#tab-library').innerText() === '学习', 'Learning navigation label');
  assert(await input.getAttribute('placeholder') === '搜索三语表达或场景…', 'Concise learning search prompt');
  assert(await shuffle.innerText() === '换一换', 'Concise shuffle label');
  assert(await page.locator('#view-library .library-heading').count() === 0, 'Toolbar replaces the old heading stack');
  assert(await page.locator('#view-library table').count() === 0, 'Editorial feed replaces the table');
  assert(await page.locator('.admin-only:visible').count() === 0, 'Starts read-only');
  assert(!await more.isVisible() && await bottomShuffle.isVisible(), 'Random browse offers shuffle instead of pagination');
  assert(await status.innerText() === '随机推荐 6 组 · 共 ' + format(bootstrap.total) + ' 组', 'Browse status shows only sample and corpus size');
  await checkDiversity();
  const shuffled = await shuffleCards(shuffle);
  await shuffleCards(bottomShuffle);
  const previousReload = await cardIds();
  await page.reload();
  await waitCards(feedSize);
  await checkDiversity();
  checkDifferent(previousReload, await cardIds());
  const previousEntry = await cardIds();
  await page.locator('#tab-home').click();
  const entry = page.waitForResponse(matchResponse({mode: 'feed', q: ''}));
  await page.locator('#tab-library').click();
  await entry;
  await waitCards(feedSize);
  await checkDiversity();
  checkDifferent(previousEntry, await cardIds());

  assert(await page.locator('#category-filters [data-category]').count() === 13, 'All 12 filters plus All');
  assert((await page.locator('#category-filters [data-category]').allTextContents()).map(text => text.trim()).join('|')
    === '全部|社媒|电商|投放|公关|修辞|美妆|奢品|数码|餐饮|文旅|金融|合规', 'Short category labels without numeric counters');
  for (const name of bootstrap.categories) {
    const filter = page.locator('[data-category="' + name + '"]');
    await filter.click();
    await waitCards(feedSize, name);
    await waitTotal(bootstrap.category_counts[name]);
    const filterName = await filter.innerText();
    assert((await cards.locator('[data-case-category]').allTextContents()).every(label => label.trim() === filterName),
      'Cards show the same short scene name as their filter');
  }
  await shuffleCards(shuffle, bootstrap.categories.at(-1));
  await page.locator('[data-category=""]').click();
  await waitCards(feedSize);
  await waitTotal(bootstrap.total);

  const ranked = await search('防晒');
  assert(ranked.terms.length === pageSize && ranked.matched_total > pageSize && ranked.has_more, 'Search initially shows twelve ranked cards');
  assert(await more.isVisible() && !await bottomShuffle.isVisible(), 'Only search offers additional pages');
  assert((await cardIds()).join(',') === ranked.terms.map(term => term.id).join(','), 'Cards retain server ranking');
  await cards.first().evaluate(card => { card.dataset.paginationMarker = 'original'; });
  for (let offset = pageSize; offset < ranked.matched_total; offset += pageSize) {
    const pending = page.waitForResponse(matchResponse({q: '防晒', offset: String(offset)}));
    await more.click();
    await pending;
    await waitCards(Math.min(ranked.matched_total, offset + pageSize));
  }
  assert(!await more.isVisible(), 'Load more hides after final partial search page');
  assert(await cards.first().getAttribute('data-pagination-marker') === 'original', 'Page append preserves previous cards');
  const ids = await cardIds();
  assert(new Set(ids).size === ids.length, 'Search pages do not duplicate cards');

  let stale;
  const staleUrl = url => url.pathname === '/api/terms' && url.searchParams.get('q') === 'stale-search-test';
  const staleHandler = route => { stale = route; };
  await page.route(staleUrl, staleHandler);
  try {
    const started = page.waitForRequest(request => staleUrl(new URL(request.url())));
    await input.fill('stale-search-test');
    await started;
    const newest = await search('ROAS');
    assert(newest.terms.length > 0, 'New search resolves while older search is pending');
    if (stale) await stale.fulfill({json: {success: true, data: {...newest, terms: [], matched_total: 0, has_more: false}}}).catch(() => {});
    assert((await cardIds()).join(',') === newest.terms.map(term => term.id).join(','), 'Stale search cannot replace current results');
  } finally {
    if (stale) await stale.abort().catch(() => {});
    await page.unroute(staleUrl, staleHandler);
  }
  for (const query of ['早鸟福利', '免運費', 'early bird', '玻色因']) {
    assert((await search(query)).terms.length > 0, 'Search finds ' + query);
  }

  const record = (await search('Product Seeding')).terms[0];
  assert(record.term_en === 'Product Seeding', 'Known cross-market case ranks first');
  const first = cards.first();
  const example = first.locator('[data-case-copy]');
  const text = first.locator('.case-copy-text');
  const marketButton = market => first.locator('[data-case-language="' + market + '"]');
  const detailRequests = [];
  const onRequest = request => {
    if (new URL(request.url()).pathname === '/api/terms/' + record.id) detailRequests.push(request.url());
  };
  page.on('request', onRequest);
  try {
    assert(await marketButton('hk').getAttribute('aria-pressed') === 'true', 'Each card defaults to Hong Kong');
    assert(await first.locator('.case-header [data-case-language]').count() === 3, 'Market controls live in the card meta row');
    assert((await first.locator('[data-try-case]').innerText()).trim().startsWith('试改'), 'Concise rewrite action');
    assert(await first.locator('[data-case-bad], .case-before, .case-platforms, .platform-tag').count() === 0,
      'Pitfall and platform tags stay out of the card face');
    assert(!/避免写法|地道实战例句/.test(await first.innerText()), 'The card has no field-label headers');
    const tip = await first.locator('[data-case-tip]').innerText();
    assert(tip === record.learning_tip && [...tip].length > 0 && [...tip].length <= 22, 'Shows a short standalone takeaway');
    const surfaces = await first.evaluate(card => ({
      background: getComputedStyle(card).backgroundColor,
      radius: getComputedStyle(card).borderTopLeftRadius,
      padding: getComputedStyle(card).paddingTop,
      inner: ['.case-expressions', '[data-case-copy]'].map(selector => getComputedStyle(card.querySelector(selector)).backgroundColor),
      hairline: getComputedStyle(card.querySelector('[data-case-copy]')).borderTopColor,
    }));
    assert(surfaces.background === 'rgb(255, 255, 255)' && surfaces.radius === '20px' && surfaces.padding === '28px',
      'Desktop card is a white rounded editorial surface');
    assert(surfaces.inner.every(color => color === 'rgba(0, 0, 0, 0)') && surfaces.hairline === 'rgb(241, 241, 244)',
      'Headwords and example are unboxed with only a light hairline');
    assert(await text.innerText() === record.good_example_hk, 'Hong Kong example is visible without opening the drawer');
    for (const key of ['en', 'hk', 'cn']) {
      const expression = first.locator('[data-case-expression="' + key + '"]');
      await expression.click();
      assert(await page.evaluate(() => navigator.clipboard.readText()) === record['term_' + key], 'Copies ' + key + ' expression');
      assert((await page.locator('#toast').innerText()).includes('已复制'), 'Copy displays confirmation');
      await marketButton(key).click();
      assert(await marketButton(key).getAttribute('aria-pressed') === 'true', 'Example market selection for ' + key);
      assert(await text.innerText() === record['good_example_' + key], 'Displays ' + key + ' in-context copy');
      await example.click();
      assert(await page.evaluate(() => navigator.clipboard.readText()) === record['good_example_' + key], 'Copies entire ' + key + ' sentence');
      assert(!await page.locator('#term-drawer').isVisible(), 'Copying does not open drawer');
    }
    await first.locator('[data-open-term]').press('Enter');
    await page.locator('.drawer-good').waitFor();
    assert(await page.locator('#drawer-title').innerText() === record.term_en, 'Details open for the selected card');
    assert(await page.locator('.drawer-section').count() >= 4, 'Shared drawer shows complete detail');
    assert((await page.locator('#term-drawer').innerText()).includes(record.bad_example), 'Drawer retains the full pitfall');
    assert((await page.locator('#term-drawer').innerText()).includes(record.usage_tip), 'Drawer retains the full usage tip');
    assert(await page.locator('#term-drawer [data-edit]').count() === 0, 'Public drawer hides edit actions');
    assert(detailRequests.length === 0, 'Full case payload supports examples and details without extra requests');
    await page.keyboard.press('Escape');
    await page.locator('#term-drawer').waitFor({state: 'hidden'});
    await first.click({position: {x: 8, y: 32}});
    await page.locator('.drawer-good').waitFor();
    assert(await page.locator('#drawer-title').innerText() === record.term_en, 'Clicking the card whitespace opens the same drawer');
    await page.keyboard.press('Escape');
    await first.locator('[data-open-term]:focus').waitFor({timeout: 5000});
  } finally {
    page.off('request', onRequest);
  }

  const rewrites = [];
  const mockRewrite = async route => {
    rewrites.push(route.request().postDataJSON());
    await route.fulfill({json: {success: true, data: {
      primary_copy: record.good_example_cn, alt_copy: record.good_example_hk,
      adaptations: [], cta_options: [], matched_glossary_terms: [record],
      counts: {character_count: record.good_example_cn.length, word_count: 0, reading_time_seconds: 4},
      engine: 'deepseek', notice: '',
    }}});
  };
  await page.route('**/api/rewrite', mockRewrite);
  try {
    await first.locator('[data-try-case]').click();
    await page.locator('#rewritten-copy').waitFor();
    const expectedDraft = '亲，这支精华必须种草！';
    assert(await page.locator('#view-studio').isVisible(), 'Case action opens Studio');
    assert(await page.locator('#copy-text').inputValue() === expectedDraft, 'Handoff strips editorial notes and quote wrappers');
    assert(rewrites.length === 1 && rewrites[0].text === expectedDraft, 'Handoff starts one rewrite with cleaned draft');
    assert(rewrites[0].target_market === 'cn' && rewrites[0].tone === 'standard', 'Handoff uses selected market and brand tone');
    assert(await page.locator('#rewritten-copy').innerText() === record.good_example_cn, 'Rewrite result renders in Studio');
  } finally {
    await page.unroute('**/api/rewrite', mockRewrite);
  }

  await page.locator('#tab-library').click();
  await search('no-match-brandlex-test');
  assert(await cards.count() === 0 && await page.locator('#case-feed-message').isVisible(), 'Empty search state');
  await search('');
  await waitTotal(bootstrap.total);
  await page.locator('#admin-toggle').click();
  await page.locator('#admin-password').fill('browser-test-only');
  await page.locator('#admin-submit').click();
  await page.waitForFunction(() => document.querySelector('#admin-label').textContent === '已解锁');
  assert(await page.locator('#admin-password').inputValue() === '', 'Clears successful password');
  const add = page.locator('#view-library [data-action="add-term"]');
  const desktopViewport = page.viewportSize() || {width: 1440, height: 1000};
  await page.setViewportSize({...desktopViewport, width: 390});
  try {
    assert((await input.boundingBox()).width >= 170, 'Mobile admin controls leave room for search');
    assert(await add.isVisible() && await page.locator('#reset-library').isVisible(), 'Mobile admin controls remain reachable');
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Mobile admin toolbar fits the page');
  } finally {
    await page.setViewportSize(desktopViewport);
  }
  await add.click();
  await page.keyboard.press('Escape');
  await page.waitForFunction(() => !document.querySelector('#term-dialog').open
    && document.activeElement === document.querySelector('#view-library [data-action="add-term"]'));
  const testName = 'BrandLex Browser Fixture Newsletter';
  async function addFixture() {
    await add.click();
    await page.locator('#fill-example').click();
    assert(await page.locator('#field-term-en').inputValue() === 'Brand Newsletter', 'Fills example');
    await page.locator('#field-term-en').fill(testName);
    await page.locator('#save-term').click();
    await page.locator('#term-dialog').waitFor({state: 'hidden'});
    await waitTotal(bootstrap.total + 1);
  }
  await addFixture();
  const fixture = (await search(testName)).terms[0];
  const edit = first.locator('[data-edit="' + fixture.id + '"]');
  const remove = first.locator('[data-delete="' + fixture.id + '"]');
  await edit.click();
  await page.locator('#field-term-hk').fill('品牌週末電子通訊');
  await page.locator('#save-term').click();
  await page.waitForFunction(() => !document.querySelector('#term-dialog').open
    && document.querySelector('#case-feed-grid').textContent.includes('品牌週末電子通訊'));
  await page.reload();
  await waitTotal(bootstrap.total + 1);
  assert(await page.locator('#admin-label').innerText() === '已解锁', 'Admin survives reload');
  assert((await search(testName)).terms[0].term_hk === '品牌週末電子通訊', 'Edit survives reload');
  await remove.click();
  await page.keyboard.press('Escape');
  assert(await remove.isVisible(), 'Cancel preserves case');
  await remove.click();
  await page.locator('#confirm-action').click();
  await page.locator('#confirm-dialog').waitFor({state: 'hidden'});
  await waitCards(0);
  await search('');
  await waitTotal(bootstrap.total);
  await addFixture();
  await page.locator('#reset-library').click();
  await page.keyboard.press('Escape');
  assert((await status.innerText()).includes(format(bootstrap.total + 1)), 'Cancel reset');
  await page.locator('#reset-library').click();
  await page.locator('#confirm-action').click();
  await page.locator('#confirm-dialog').waitFor({state: 'hidden'});
  await waitTotal(bootstrap.total);
  await waitCards(feedSize);
  await first.locator('[data-open-term]').click();
  await page.locator('#term-drawer [data-edit]').waitFor();
  assert(await page.locator('#term-drawer [data-delete]').count() === 1, 'Admin drawer actions');
  await page.keyboard.press('Escape');
  const downloads = [];
  for (const filetype of ['csv', 'tbx', 'json']) {
    await page.locator('.app-header .export-menu summary').click();
    const event = page.waitForEvent('download');
    await page.locator('.export-menu a[href="/api/export/' + filetype + '"]').click();
    const download = await event;
    const destination = '/private/tmp/BrandLex-v3-2-ui-export.' + filetype;
    await download.saveAs(destination);
    assert(await download.failure() === null, 'Export ' + filetype);
    downloads.push(destination);
  }
  await page.locator('#admin-logout').click();
  await page.locator('#confirm-action').click();
  await page.waitForFunction(() => document.querySelector('#admin-label').textContent === '维护模式'
    && !document.querySelector('#confirm-dialog').open);
  assert(await page.locator('.admin-only:visible').count() === 0
    && await cards.locator('[data-edit]:visible, [data-delete]:visible').count() === 0, 'Logout hides actions');
  const denied = await page.evaluate(async () => {
    const data = (await (await fetch('/api/bootstrap')).json()).data;
    const response = await fetch('/api/terms/1', {method: 'DELETE', headers: {'X-CSRF-Token': data.csrf_token}});
    return {admin: data.is_admin, status: response.status};
  });
  assert(denied.admin === false && denied.status === 403, 'Logout revokes backend permission');
  return {passed: true, shuffled, checks: [
    'six distinct categories and no table', 'two shuffle controls and exclusion', 'fresh re-entry and reload',
    'twelve category filters', 'ranked search and stable append', 'stale and empty search',
    'unboxed learning cards and short takeaways', 'inline examples and clipboard', 'drawer via details and card whitespace', 'case handoff and auto rewrite',
    'admin mutations and confirmations', 'exports and logout',
  ], downloads};
}
