async (page) => {
  const assert = (value, message) => { if (!value) throw new Error(message); };
  const base = page.url().split('/').slice(0, 3).join('/');
  const requests = [];
  const pageErrors = [];
  const onPageError = error => pageErrors.push(error.message);
  page.on('pageerror', onPageError);
  await page.addInitScript(() => {
    window.__brandlexAnimationFrames = 0;
    const requestFrame = window.requestAnimationFrame.bind(window);
    window.requestAnimationFrame = callback => requestFrame(time => {
      window.__brandlexAnimationFrames += 1;
      callback(time);
    });
  });
  const frameDelta = () => page.evaluate(async () => {
    const initial = window.__brandlexAnimationFrames;
    await new Promise(resolve => setTimeout(resolve, 180));
    return window.__brandlexAnimationFrames - initial;
  });
  async function waitMotion(expected) {
    try {
      await page.waitForFunction(value => document.querySelector('#antigravity-canvas').dataset.motion === value, expected, {timeout: 8000});
    } catch {
      const actual = await page.evaluate(() => ({motion: document.querySelector('#antigravity-canvas').dataset.motion,
        hidden: document.hidden, reduced: matchMedia('(prefers-reduced-motion: reduce)').matches, scrollY}));
      throw new Error('Expected motion ' + expected + ': ' + JSON.stringify(actual));
    }
  }
  async function verifyMotion() {
    await page.bringToFront();
    await page.evaluate(() => window.scrollTo(0, 0));
    await waitMotion('running');
    assert(await page.locator('#antigravity-canvas').getAttribute('data-particle-count') === '45', 'Exactly 45 subtle particles');
    assert(await frameDelta() > 0, 'Visible hero animates');
    const hero = await page.locator('.home-hero').boundingBox();
    assert(hero.height >= await page.evaluate(() => innerHeight * .82) - 1, 'Hero retains 82vh breathing room');
    await page.mouse.move(hero.x + hero.width * .55, hero.y + hero.height * .45);
    const canvas = await page.locator('#antigravity-canvas').evaluate(node => ({width: node.width, height: node.height}));
    assert(canvas.width > 0 && canvas.height > 0, 'Canvas has a real drawing surface');
    await page.emulateMedia({reducedMotion: 'reduce'});
    await waitMotion('reduced');
    assert(await frameDelta() <= 1, 'Reduced motion draws a still surface without a frame loop');
    await page.emulateMedia({reducedMotion: 'no-preference'});
    await waitMotion('running');
    await page.locator('#tab-studio').click();
    await waitMotion('paused');
    assert(await frameDelta() <= 1, 'Hidden home stops the animation loop');
    await page.locator('#tab-home').click();
    await waitMotion('running');
  }
  async function verifySurfaces() {
    const names = ['rewrite', 'glossary', 'export'];
    for (const name of names) {
      await page.locator(`[data-home-surface="${name}"]`).click();
      assert(await page.locator(`[data-home-surface-panel="${name}"]`).isVisible(), 'Visual surface ' + name);
      assert(await page.locator(`[data-home-surface="${name}"]`).getAttribute('aria-selected') === 'true', 'Selected surface ' + name);
      assert(await page.locator('[data-home-surface-panel]:visible').count() === 1, 'One visible surface at a time');
    }
    await page.locator('[data-home-surface="export"]').press('Home');
    assert(await page.locator('[data-home-surface="rewrite"]').getAttribute('aria-selected') === 'true', 'Surface Home selects rewrite');
    const miniCopies = [];
    for (const market of ['hk', 'cn', 'en']) {
      for (const tone of ['standard', 'social', 'concise']) {
        await page.locator(`[data-mini-market="${market}"]`).click();
        await page.locator(`[data-mini-tone="${tone}"]`).click();
        const copy = await page.locator('#home-mini-copy').innerText();
        assert(copy.length > 8, 'Useful mini preview ' + market + '/' + tone);
        miniCopies.push(copy);
      }
    }
    assert(new Set(miniCopies).size === 9, 'Nine distinct tone and market previews');
    assert(requests.length === 0, 'Mini controls stay local');
    await page.locator('[data-home-surface="rewrite"]').press('ArrowDown');
    assert(await page.locator('[data-home-surface="glossary"]').getAttribute('aria-selected') === 'true', 'Surface arrows select glossary');
    await page.context().grantPermissions(['clipboard-read', 'clipboard-write']);
    const expressions = page.locator('#home-surface-panel-glossary [data-copy]');
    assert(await expressions.count() === 12, 'Four tri-regional glossary rows');
    for (let index = 0; index < 12; index += 1) {
      const text = await expressions.nth(index).getAttribute('data-copy');
      await expressions.nth(index).click();
      assert(await page.evaluate(() => navigator.clipboard.readText()) === text, 'Mini expression copies ' + text);
    }
    const learningCta = page.locator('#home-surface-panel-glossary [data-go-view="library"]');
    assert((await learningCta.innerText()).trim().startsWith('探索三语学习'), 'Surface uses learning CTA');
    await learningCta.click();
    assert(await page.locator('#view-library').isVisible(), 'Learning surface opens learning');
    await page.locator('.brand').click();
    await page.locator('[data-home-surface="export"]').click();
    for (const format of ['csv', 'tbx', 'json']) {
      const response = await page.request.get(base + '/api/export/' + format);
      assert(response.status() === 200, 'Homepage export endpoint ' + format);
      if (format === 'csv') assert([...((await response.body()).subarray(0, 3))].join(',') === '239,187,191', 'CSV has Excel-friendly BOM');
      const [download] = await Promise.all([page.waitForEvent('download'), page.locator(`[data-home-export="${format}"]`).click()]);
      await download.saveAs('/private/tmp/BrandLex-antigravity-home-export.' + format);
      assert(await download.failure() === null, 'Homepage download ' + format);
      assert(await page.locator('#view-home').isVisible(), 'Export retains home');
    }
    await page.locator('[data-home-surface="export"]').press('Home');
    assert(requests.length === 0, 'Surfaces and exports make no rewrite call');
  }
  const handler = async route => {
    const input = route.request().postDataJSON();
    requests.push(input);
    const copy = {hk: '跨界聯乘禮盒，早鳥禮遇及免運費。', cn: '联名礼盒，早鸟福利及包邮。', en: 'Discover the collaboration gift set with early-bird pricing and free shipping.'}[input.target_market];
    await route.fulfill({json: {success: true, data: {
      primary_copy: copy, alt_copy: copy, adaptations: [], cta_options: [],
      matched_glossary_terms: [], counts: {character_count: copy.length, word_count: 12, reading_time_seconds: 4},
      engine: 'deepseek', notice: '', error_code: null
    }}});
  };
  await page.route('**/api/rewrite', handler);
  try {
    await page.goto(base + '/');
    await page.waitForFunction(() => document.querySelectorAll('[data-sample]').length === 4);
    assert(await page.locator('#view-home').isVisible(), 'Root defaults to product home');
    assert(await page.locator('.main-nav [role="tab"]').count() === 3, 'Exactly three main views');
    assert((await page.locator('.main-nav [role="tab"]').allTextContents()).map(text => text.trim()).join('|') === '首页|文案改写|学习',
      'Navigation uses the learning name');
    assert((await page.locator('.home-hero [data-go-view="library"]').innerText()).trim() === '进入学习',
      'Hero uses the learning CTA');
    assert(await page.locator('#home-surface-glossary strong').innerText() === '三语表达学习', 'Surface uses the learning title');
    assert(await page.locator('#tab-home').getAttribute('aria-selected') === 'true', 'Home tab selected');
    assert(await page.locator('.app-header').evaluate(node => node.getBoundingClientRect().height) === 52, 'Compact header retained');
    assert(await page.locator('.admin-only:visible').count() === 0, 'Home does not expose public writes');
    const captions = await page.locator('#view-home [data-home-caption]').evaluateAll(nodes => nodes.map(node => ({
      text: node.textContent.trim(), limit: Number(node.dataset.captionLimit || 28)
    })));
    assert(captions.length >= 5, 'Home captions are explicitly identifiable');
    for (const caption of captions) assert((caption.text.match(/[\u3400-\u9fff]/g) || []).length <= caption.limit, 'Short single-sentence caption: ' + caption.text);
    await verifyMotion();
    await verifySurfaces();
    const outputs = {};
    for (const market of ['hk', 'cn', 'en']) {
      await page.locator(`[data-home-market="${market}"]`).click();
      outputs[market] = await page.locator('#home-preview-copy').innerText();
      assert(outputs[market].length > 30, 'Substantive localized sample ' + market);
      const adaptations = await page.locator('#home-preview-adaptations').innerText();
      assert(adaptations.length > 10, 'Adaptations update with output ' + market);
      const selected = await page.locator(`[data-home-market="${market}"]`).getAttribute('aria-selected')
        || await page.locator(`[data-home-market="${market}"]`).getAttribute('aria-pressed');
      assert(selected === 'true', 'Accessible market selection ' + market);
    }
    assert(new Set(Object.values(outputs)).size === 3, 'Three distinct market previews');
    assert(/免運費/.test(outputs.hk) && /包邮/.test(outputs.cn) && /free shipping/i.test(outputs.en), 'Market-specific terminology');
    assert(!/[\u3400-\u9fff]/.test(outputs.en), 'English output is English');
    assert(requests.length === 0, 'Browsing curated previews makes no model request');
    await page.locator('[data-home-market="en"]').press('Home');
    assert(await page.locator('[data-home-market="hk"]').getAttribute('aria-selected') === 'true', 'Preview Home selects HK');
    await page.locator('[data-home-market="hk"]').press('ArrowRight');
    assert(await page.locator('[data-home-market="cn"]').getAttribute('aria-selected') === 'true', 'Preview arrow selects CN');
    assert(await page.locator('#home-preview-copy').getAttribute('lang') === 'zh-CN', 'Preview updates content language');
    await page.locator('[data-home-market="cn"]').press('End');
    assert(await page.locator('[data-home-market="en"]').getAttribute('aria-selected') === 'true', 'Preview End selects EN');
    assert(await page.locator('#home-preview-copy').getAttribute('lang') === 'en', 'English preview language');
    const panelLabel = await page.locator('#home-preview-panel').getAttribute('aria-labelledby');
    assert(panelLabel === await page.locator('[data-home-market="en"]').getAttribute('id'), 'Preview panel points to selected tab');
    await page.locator('#admin-toggle').click();
    await page.keyboard.press('Escape');
    assert(await page.locator('#view-home').isVisible(), 'Closing maintenance retains home');
    assert(await page.locator('#admin-toggle').evaluate(node => node === document.activeElement), 'Maintenance returns focus to visible trigger');
    const source = (await page.locator('#home-source-copy').innerText()).trim();
    for (const market of ['en', 'hk', 'cn']) {
      await page.locator(`[data-home-market="${market}"]`).click();
      await page.locator('#home-edit-draft').click();
      await page.waitForFunction(() => !document.querySelector('#output-content').hidden
        && document.querySelector('#copy-results').getAttribute('aria-busy') === 'false');
      assert(await page.locator('#view-studio').isVisible(), 'Preview opens studio');
      const latest = requests[requests.length - 1];
      assert(latest.text === source && latest.target_market === market && latest.tone === 'standard', 'Preview draft/market forwarded ' + market);
      assert((await page.locator('#copy-text').inputValue()).trim() === source, 'Studio source is exact preview brief');
      await page.locator('.brand').click();
      assert(await page.locator('#view-home').isVisible(), 'Brand returns to home');
    }
    assert(requests.length === 3, 'One rewrite per explicit preview action');

    const destinations = await page.locator('#view-home [data-go-view]:visible').evaluateAll(nodes => nodes.map(node => node.dataset.goView));
    assert(destinations.includes('studio') && destinations.includes('library'), 'Direct workspace CTAs present');
    for (let index = 0; index < destinations.length; index += 1) {
      await page.locator('#view-home [data-go-view]:visible').nth(index).click();
      assert(await page.locator('#view-' + destinations[index]).isVisible(), 'CTA destination ' + index);
      await page.locator('.brand').click();
    }
    assert(requests.length === 3, 'Ordinary CTA navigation does not rewrite');

    await page.locator('#tab-studio').click();
    await page.locator('#copy-text').fill('A working draft stays here while exploring the product.');
    await page.locator('.brand').click();
    await page.locator('#tab-studio').click();
    assert(await page.locator('#copy-text').inputValue() === 'A working draft stays here while exploring the product.', 'Navigation preserves working draft');

    const categories = ['社媒与种草', '电商与转化', '投放与增长', '公关与线下', '文案与修辞',
      '美妆与个护', '时尚与奢品', '数码与科技', '餐饮与酒水', '文旅与酒店', '金融与支付', '合规与风控'];
    assert(await page.locator('#home-library-count').innerText().then(text => /3,2\d\d 条三语词条 · 12 个营销场景/.test(text)), 'Homepage shows current glossary scale');
    assert(await page.locator('[data-home-category]').count() === 12, 'Homepage lists all scenarios');
    for (const category of categories) {
      await page.locator('#tab-library').click();
      await page.locator('#library-search').fill('a prior search that should clear');
      await page.locator('.brand').click();
      await page.locator(`[data-home-category="${category}"]`).click();
      await page.waitForFunction(name => {
        const grid = document.querySelector('#case-feed-grid');
        const cards = [...grid.querySelectorAll('[data-term-id]')];
        return cards.length === 6 && cards.every(card => card.dataset.categoryName === name)
          && grid.getAttribute('aria-busy') === 'false';
      }, category);
      assert(await page.locator('#view-library').isVisible(), 'Scenario opens library');
      assert(await page.locator('#library-search').inputValue() === '', 'Scenario clears prior query');
      assert(await page.locator(`[data-category="${category}"]`).getAttribute('aria-pressed') === 'true', 'Scenario selects filter');
    }

    await page.goto(base + '/');
    await page.waitForFunction(() => document.querySelectorAll('[data-sample]').length === 4);
    await page.locator('#tab-studio').click();
    await page.locator('#tab-library').click();
    await page.goBack();
    assert(await page.locator('#view-studio').isVisible(), 'Back restores studio');
    await page.goBack();
    assert(await page.locator('#view-home').isVisible(), 'Back restores home');
    await page.goForward();
    assert(await page.locator('#view-studio').isVisible(), 'Forward restores studio');
    for (const view of ['studio', 'library', 'home']) {
      await page.goto(base + '/#' + view);
      await page.waitForFunction(name => !document.querySelector('#view-' + name).hidden, view);
      assert(await page.locator('#tab-' + view).getAttribute('aria-selected') === 'true', 'Direct hash ' + view);
    }
    for (const view of ['studio', 'library']) {
      await page.locator('#tab-' + view).click();
      await page.locator('.skip-link').focus();
      await page.locator('.skip-link').press('Enter');
      assert(await page.locator('#view-' + view).isVisible(), 'Skip link preserves ' + view);
      assert(page.url().endsWith('#' + view), 'Skip link preserves workspace URL');
      assert(await page.locator('#main-content').evaluate(node => node === document.activeElement), 'Skip link focuses current content');
    }
    await page.goto(base + '/#unknown');
    await page.waitForFunction(() => !document.querySelector('#view-home').hidden);
    await page.locator('#tab-home').press('ArrowRight');
    assert(await page.locator('#view-studio').isVisible(), 'Arrow selects next main tab');
    await page.locator('#tab-studio').press('End');
    assert(await page.locator('#view-library').isVisible(), 'End selects final main tab');
    await page.locator('#tab-library').press('Home');
    assert(await page.locator('#view-home').isVisible(), 'Home selects first main tab');
    const text = await page.locator('body').innerText();
    assert(!/\p{Extended_Pictographic}|[\u{1F1E6}-\u{1F1FF}]|\uFE0F/u.test(text), 'Emoji-free home');
    assert(pageErrors.length === 0, 'No browser errors: ' + pageErrors.join('; '));
    return {passed: true, mocked_rewrites: requests.length, checks: ['default home and three tabs', '45 particles and paused/reduced motion', 'three interactive surfaces', 'nine mini previews', '12 copyable expressions', 'three export downloads', 'three instant previews', 'no unsolicited rewrite', 'selected-market handoff', 'all workspace CTA links', 'preserved working draft', 'twelve category jumps and query reset', 'browser history', 'direct hashes', 'keyboard navigation', 'skip-link focus', 'zero emojis']};
  } finally {
    await page.unroute('**/api/rewrite', handler);
    await page.emulateMedia({reducedMotion: 'no-preference'});
    page.off('pageerror', onPageError);
  }
}
