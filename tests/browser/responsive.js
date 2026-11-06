async (page) => {
  const assert = (value, message) => { if (!value) throw new Error(message); };
  const base = page.url().split('/').slice(0, 3).join('/');
  await page.goto(base + '/');
  await page.waitForFunction(() => document.querySelectorAll('[data-sample]').length === 4);
  await page.locator('#tab-home').press('ArrowRight');
  assert(await page.locator('#view-studio').isVisible(), 'Keyboard selects studio');
  await page.locator('#tab-studio').press('ArrowRight');
  assert(await page.locator('#view-library').isVisible(), 'Keyboard selects library');
  await page.locator('#tab-library').press('Home');
  assert(await page.locator('#view-home').isVisible(), 'Home navigates first tab');
  const homeSizes = [];
  for (const width of [320, 390, 768, 1440]) {
    await page.setViewportSize({width, height: 1000});
    const metrics = await page.evaluate(() => ({
      width: innerWidth, scroll: document.documentElement.scrollWidth,
      heroHeight: document.querySelector('.home-hero').getBoundingClientRect().height,
      titleSize: parseFloat(getComputedStyle(document.querySelector('#home-title')).fontSize),
      headerHeight: document.querySelector('.app-header').getBoundingClientRect().height
    }));
    assert(metrics.scroll <= width + 1, 'Home fits width ' + width);
    assert(metrics.heroHeight >= 819 && metrics.headerHeight === 52, 'Hero rhythm and compact header ' + width);
    assert(metrics.titleSize >= 44 && metrics.titleSize <= 76, 'Monumental responsive type ' + width);
    homeSizes.push(metrics);
  }
  await page.locator('.brand').focus();
  await page.keyboard.press('/');
  assert(await page.locator('#library-search').evaluate(node => node === document.activeElement), 'Slash opens library search');
  await page.setViewportSize({width: 390, height: 900});
  const dimensions = [];
  for (const view of ['home', 'studio', 'library']) {
    await page.locator(`[data-view="${view}"]`).click();
    await page.evaluate(() => window.scrollTo(0, 0));
    const size = await page.evaluate(() => ({width: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth}));
    assert(size.scroll <= size.width + 1, 'No page overflow ' + view + ' ' + JSON.stringify(size));
    dimensions.push({view, ...size});
  }
  const cardSelector = '#case-feed-grid > [data-term-id]';
  const waitCases = () => page.waitForFunction(() => document.querySelectorAll('#case-feed-grid > [data-term-id]').length === 6
    && document.querySelector('#case-feed-grid').getAttribute('aria-busy') === 'false');
  const cardPositions = () => page.locator(cardSelector).evaluateAll(items => items.map(item => {
    const {x, y, width} = item.getBoundingClientRect();
    return {x, y, width};
  }));
  await waitCases();
  const mobileCards = await cardPositions();
  assert(mobileCards.every(card => Math.abs(card.x - mobileCards[0].x) < 1 && card.width < 390), 'Mobile uses one column');
  assert(mobileCards[1].y > mobileCards[0].y, 'Mobile cards flow vertically');
  const tipLines = await page.locator(cardSelector + ' [data-case-tip]:visible').evaluateAll(tips => tips.map(tip => {
    const text = document.createRange();
    text.selectNodeContents(tip);
    return new Set([...text.getClientRects()].map(rect => Math.round(rect.top))).size;
  }));
  assert(tipLines.length === 6 && tipLines.every(lines => lines === 1), 'Mobile takeaways fit on one line');
  const rail = page.locator('#category-filters');
  const railMetrics = await rail.evaluate(node => {
    const {clientWidth, scrollWidth} = node;
    const initial = node.scrollLeft;
    node.scrollLeft = scrollWidth;
    const end = node.scrollLeft;
    node.scrollLeft = initial;
    return {clientWidth, scrollWidth, initial, end};
  });
  assert(railMetrics.scrollWidth > railMetrics.clientWidth && railMetrics.end > railMetrics.initial,
    'Mobile category pills scroll inside the rail');
  const afterCards = await page.evaluate(() => ({width: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth}));
  assert(afterCards.scroll <= afterCards.width + 1, 'Loaded cards and scrolling category rail stay within the viewport');
  await page.locator(cardSelector).first().locator('[data-open-term]').press('Enter');
  await page.locator('.drawer-good').waitFor();
  await page.waitForFunction(() => getComputedStyle(document.querySelector('#term-drawer')).transform === 'none');
  const drawer = await page.locator('#term-drawer').boundingBox();
  assert(drawer.width <= 390 && drawer.x >= 0, 'Drawer fits mobile ' + JSON.stringify(drawer));
  assert(await page.locator('.drawer-expression').count() === 3, 'All regional expressions available');
  await page.locator('.drawer-tip').scrollIntoViewIfNeeded();
  assert(await page.locator('.drawer-tip').isVisible(), 'Mobile detail can scroll to usage tip');
  await page.keyboard.press('Escape');
  await page.locator('#admin-toggle').click();
  const modal = await page.locator('#admin-dialog').boundingBox();
  assert(modal.width <= 390 && modal.x >= 0, 'Password dialog fits mobile');
  await page.keyboard.press('Escape');
  await page.locator('[data-view="studio"]').click();
  await page.locator('[data-sample]').first().click();
  await page.locator('#rewrite-copy').scrollIntoViewIfNeeded();
  assert(await page.locator('#rewrite-copy').isVisible(), 'Mobile rewrite action reachable');
  await page.locator('#copy-text').fill('Typing / keeps the slash in the source.');
  await page.locator('#copy-text').press('/');
  assert(await page.locator('#view-studio').isVisible(), 'Slash does not hijack typing');
  assert((await page.locator('#copy-text').inputValue()).includes('/'), 'Slash remains draft content');
  await page.setViewportSize({width: 1440, height: 1000});
  const panels = await page.locator('.studio-workspace').evaluate(node => [...node.children].map(item => item.getBoundingClientRect().width));
  assert(Math.abs(panels[0] - panels[1]) < 1, 'Desktop editor panes are equal');
  await page.goto(base + '/#library');
  await waitCases();
  const desktopControls = await Promise.all(['#library-search', '#category-filters', '#shuffle-feed'].map(selector => page.locator(selector).boundingBox()));
  const [searchBox, categories, shuffle] = desktopControls;
  const centers = desktopControls.map(box => box.y + box.height / 2);
  assert(searchBox.x < categories.x && categories.x < shuffle.x && Math.max(...centers) - Math.min(...centers) <= 5,
    'Desktop toolbar places search, categories, and shuffle on one row');
  const desktopCards = await cardPositions();
  assert(desktopCards[1].x > desktopCards[0].x && Math.abs(desktopCards[0].y - desktopCards[1].y) < 1
    && Math.abs(desktopCards[0].width - desktopCards[1].width) < 1, 'Desktop feed uses two equal columns');
  const body = await page.locator('body').innerText();
  assert(!/\p{Extended_Pictographic}|[\u{1F1E6}-\u{1F1FF}]|\uFE0F/u.test(body), 'Emoji-free live interface');
  return {passed: true, checks: ['keyboard view navigation', 'home layout at four widths', 'slash shortcut and typing isolation', 'three mobile views', 'mobile category rail', 'mobile drawer and password dialog', 'reachable controls', 'equal desktop panes', 'single-row desktop toolbar', 'responsive editorial cards', 'direct links', 'emoji-free content'], homeSizes, dimensions};
}
