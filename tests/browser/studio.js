async (page) => {
  const assert = (value, message) => { if (!value) throw new Error(message); };
  const base = page.url().split('/').slice(0, 3).join('/');
  const bootstrapRequest = page.waitForResponse(response => response.url() === base + '/api/bootstrap' && response.ok());
  await page.goto(base + '/');
  const bootstrap = (await (await bootstrapRequest).json()).data;
  await page.waitForFunction(() => document.querySelectorAll('[data-sample]').length === 4);
  await page.context().grantPermissions(['clipboard-read', 'clipboard-write']);
  assert(await page.locator('.main-nav [role="tab"]').count() === 3, 'Three main views');
  assert(await page.locator('#view-home').isVisible(), 'Product home is landing view');
  await page.locator('#tab-studio').click();
  assert(await page.locator('#view-studio').isVisible(), 'Studio remains one click away');
  assert(await page.locator('.app-header').evaluate(node => node.getBoundingClientRect().height) === 52, '52px header');
  assert(await page.locator('.admin-only:visible').count() === 0, 'Public write actions hidden');
  assert(bootstrap.is_admin === false, 'Public session locked');
  const denied = await page.evaluate(async token => {
    const results = [];
    for (const [method, path] of [['POST', '/api/terms'], ['PATCH', '/api/terms/1'], ['DELETE', '/api/terms/1'], ['POST', '/api/library/reset']]) {
      const response = await fetch(path, {method, headers: {'Content-Type': 'application/json', 'X-CSRF-Token': token}, body: '{}'});
      results.push({status: response.status, payload: await response.json()});
    }
    return results;
  }, bootstrap.csrf_token);
  assert(denied.every(item => item.status === 403 && item.payload.error === '请先解锁维护模式后再修改词库。'), 'Public writes denied by backend');
  const term = await page.evaluate(async () => {
    const terms = (await (await fetch('/api/terms?q=Free+Shipping')).json()).data.terms;
    return terms.find(item => item.term_cn === '包邮');
  });
  assert(Boolean(term), 'Real glossary fixture');
  const laterTerm = await page.evaluate(async loaded => {
    const terms = (await (await fetch('/api/terms?offset=60&limit=12')).json()).data.terms;
    const later = terms.find(item => !loaded.includes(item.id));
    return later && {id: later.id, term_en: later.term_en, term_hk: later.term_hk, term_cn: later.term_cn};
  }, bootstrap.terms.map(item => item.id));
  assert(Boolean(laterTerm), 'Off-feed glossary fixture');
  const requests = [];
  let stale = false;
  let pendingRoute;
  const handler = async route => {
    const input = route.request().postDataJSON();
    requests.push(input);
    if (stale) { pendingRoute = route; return; }
    const copies = {hk: ['春日禮盒現已登場，免運費送到府上。', '春日好禮，免運費送上。'], cn: ['春日礼盒上新，包邮到家。', '把春日心意，送给自己。'], en: ['Meet the spring gift set, delivered with free shipping.', 'A little spring joy, delivered.']}[input.target_market];
    const data = {primary_copy: copies[0], alt_copy: copies[1], adaptations: [{original: '包邮', adapted: input.target_market === 'hk' ? '免運費' : input.target_market === 'cn' ? '包邮' : 'Free Shipping', reason: '遵循品牌词库表达', term_id: term.id}], cta_options: input.target_market === 'en' ? ['Explore the collection.', 'Find your fit.'] : input.target_market === 'hk' ? ['了解禮盒詳情。', '私訊查詢。'] : ['了解礼盒详情。', '私信咨询。'], matched_glossary_terms: [term, laterTerm], counts: {character_count: copies[0].length, word_count: 15, reading_time_seconds: 4}, engine: 'deepseek', notice: ''};
    await route.fulfill({json: {success: true, data}});
  };
  await page.route('**/api/rewrite', handler);
  try {
    for (let index = 0; index < 4; index += 1) {
      await page.locator('[data-sample]').nth(index).click();
      assert((await page.locator('#copy-text').inputValue()).length > 40, 'Sample ' + index);
      assert(await page.locator('#rewrite-copy').isEnabled(), 'Loaded draft actionable');
    }
    await page.locator('#copy-text').fill('春日礼盒上新，包邮到家。');
    for (const market of ['hk', 'cn', 'en']) {
      for (const tone of ['standard', 'social', 'concise']) {
        await page.locator(`[data-market="${market}"]`).click();
        await page.locator(`[data-tone="${tone}"]`).click();
        await page.locator('#rewrite-copy').click();
        await page.waitForFunction(() => !document.querySelector('#output-content').hidden && document.querySelector('#copy-results').getAttribute('aria-busy') === 'false');
        const latest = requests[requests.length - 1];
        assert(latest.target_market === market && latest.tone === tone, 'Market/tone ' + market + '/' + tone);
      }
    }
    await page.locator('#version-alt').click();
    const alternate = await page.locator('#rewritten-copy').innerText();
    await page.locator('#copy-output').click();
    assert(await page.evaluate(() => navigator.clipboard.readText()) === alternate, 'Copies alternate version');
    await page.locator('#version-primary').click();
    assert(await page.locator('#rewritten-copy').innerText() !== alternate, 'Version switch');
    const before = await page.locator('#rewritten-copy').innerText();
    const cta = await page.locator('[data-cta="0"] span').first().innerText();
    await page.locator('[data-cta="0"]').click();
    const appended = await page.locator('#rewritten-copy').innerText();
    assert(appended === before + '\n\n' + cta, 'CTA append');
    await page.locator('[data-cta="0"]').click();
    assert(await page.locator('#rewritten-copy').innerText() === appended, 'CTA deduplicated');
    const detailUrl = base + '/api/terms/' + laterTerm.id;
    const laterTermButton = page.locator(`#matched-terms [data-open-term="${laterTerm.id}"]`);
    let delayedDetail;
    const delayedDetailHandler = route => { delayedDetail = route; };
    await page.route(detailUrl, delayedDetailHandler);
    try {
      const started = page.waitForRequest(request => request.url() === detailUrl);
      await laterTermButton.click();
      await started;
      assert(await page.locator('#drawer-content').getAttribute('aria-busy') === 'true', 'Drawer shows loading state');
      await page.keyboard.press('Escape');
      if (delayedDetail) await delayedDetail.abort().catch(() => {});
      assert(!await page.locator('#term-drawer').isVisible(), 'Closing pending detail leaves drawer closed');
    } finally {
      await page.unroute(detailUrl, delayedDetailHandler);
    }
    const detail = page.waitForResponse(response => response.url() === detailUrl && response.ok());
    await laterTermButton.click();
    await detail;
    await page.locator('.drawer-good').waitFor();
    assert(await page.locator('#term-drawer').isVisible(), 'Studio opens shared drawer for an unloaded term');
    assert(await page.locator('#drawer-title').innerText() === laterTerm.term_en, 'Correct referenced term');
    await page.keyboard.press('Escape');
    await page.locator('#use-output').click();
    assert(await page.locator('#copy-text').inputValue() === appended, 'Use output');
    assert(await page.locator('#output-empty').isVisible(), 'Source edit invalidates result');
    await page.locator('#copy-text').press('Control+Enter');
    await page.waitForFunction(() => !document.querySelector('#output-content').hidden);
    await page.locator('[data-tone="social"]').click();
    assert(await page.locator('#output-empty').isVisible(), 'Tone edit invalidates result');
    stale = true;
    await page.locator('#rewrite-copy').click();
    await page.waitForFunction(() => document.querySelector('#copy-results').getAttribute('aria-busy') === 'true');
    await page.locator('#copy-text').fill('An edited source that must not receive an old result.');
    if (pendingRoute) await pendingRoute.abort().catch(() => {});
    assert(await page.locator('#output-empty').isVisible(), 'Stale request discarded');
    assert(await page.locator('#rewrite-copy').isEnabled(), 'Recovers after abort');
    await page.locator('#clear-copy').click();
    assert(await page.locator('#copy-text').inputValue() === '' && await page.locator('#rewrite-copy').isDisabled(), 'Clear resets editor');
    await page.locator('#admin-toggle').click();
    await page.locator('#admin-password').fill('incorrect-browser-test');
    await page.locator('#admin-submit').click();
    await page.locator('#admin-error').waitFor();
    assert(await page.locator('#admin-error').innerText() === '维护口令不正确。', 'Wrong password rejected');
    await page.keyboard.press('Escape');
    await page.waitForFunction(() => !document.querySelector('#admin-dialog').open && document.querySelector('#admin-password').value === '');
    assert(await page.locator('#admin-password').inputValue() === '', 'Password cleared');
    const text = await page.locator('body').innerText();
    assert(!/\p{Extended_Pictographic}|[\u{1F1E6}-\u{1F1FF}]|\uFE0F/u.test(text), 'Emoji-free workspace');
    assert(!/TRA6202|Dr\. Siu|Member [1-4]|Section 3|CRUD|SQLite|4D Index|Tokenization|Stop Words|ABSA|11-Step Pipeline|CPU|GPU|Tacotron|WaveGlow|ONE IDEA|每个市场，都说得地道|好文案，也要入乡随俗|把好表达，留在品牌里/.test(text), 'No obsolete clutter or slogans');
    return {passed: true, mocked_rewrites: requests.length, checks: ['public API isolation', 'three-view navigation', 'four samples', 'nine market/tone combinations', 'versions/clipboard/CTA', 'shared drawer with out-of-page detail', 'source replacement', 'keyboard rewrite', 'stale requests', 'maintenance rejection']};
  } finally {
    if (pendingRoute) await pendingRoute.abort().catch(() => {});
    await page.unroute('**/api/rewrite', handler);
  }
}
