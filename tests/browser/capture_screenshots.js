async (page) => {
  const base = page.url().split('/').slice(0, 3).join('/');
  const root = 'visual_assets/';
  await page.setViewportSize({width: 1440, height: 1000});
  await page.goto(base + '/');
  await page.waitForFunction(() => document.querySelectorAll('[data-sample]').length === 4);
  await page.evaluate(() => { document.activeElement.blur(); window.scrollTo(0, 0); });
  await page.screenshot({path: root + 'brandlex_v2_home.png', fullPage: true, scale: 'css', animations: 'disabled'});
  await page.locator('#tab-studio').click();
  await page.locator('[data-market="hk"]').click();
  await page.locator('[data-tone="standard"]').click();
  await page.locator('#copy-text').fill('春日联名礼盒现已上新，早鸟福利至3月20日，包邮。\n\n礼盒包含玫瑰护手霜与香氛蜡烛，适合送给朋友，也为自己的日常添一点仪式感。欢迎到店了解详情。');
  await page.locator('#rewrite-copy').click();
  await page.waitForFunction(() => !document.querySelector('#output-content').hidden && document.querySelector('#copy-results').getAttribute('aria-busy') === 'false', undefined, {timeout: 35000});
  const engine = await page.locator('#engine-label').innerText();
  await page.evaluate(() => { document.activeElement.blur(); window.scrollTo(0, 0); });
  await page.screenshot({path: root + 'brandlex_v2_studio.png', scale: 'css', animations: 'disabled'});
  await page.locator('[data-view="library"]').click();
  await page.waitForFunction(() => document.querySelectorAll('#case-feed-grid > [data-term-id]').length === 6
    && document.querySelector('#case-feed-grid').getAttribute('aria-busy') === 'false');
  await page.evaluate(() => { document.activeElement.blur(); window.scrollTo(0, 0); });
  await page.screenshot({path: root + 'brandlex_v2_library.png', fullPage: true, scale: 'css', animations: 'disabled'});
  await page.locator('#case-feed-grid > [data-term-id]').first().locator('[data-open-term]').press('Enter');
  await page.locator('#term-drawer').waitFor();
  await page.evaluate(() => document.activeElement.blur());
  await page.screenshot({path: root + 'brandlex_v2_drawer.png', scale: 'css', animations: 'disabled'});
  await page.keyboard.press('Escape');
  await page.locator('[data-view="studio"]').click();
  await page.setViewportSize({width: 390, height: 900});
  await page.evaluate(() => { document.activeElement.blur(); window.scrollTo(0, 0); });
  await page.screenshot({path: root + 'brandlex_v2_mobile.png', fullPage: true, scale: 'css', animations: 'disabled'});
  await page.locator('.brand').click();
  await page.evaluate(() => { document.activeElement.blur(); window.scrollTo(0, 0); });
  await page.screenshot({path: root + 'brandlex_v2_home_mobile.png', fullPage: true, scale: 'css', animations: 'disabled'});
  await page.setViewportSize({width: 1440, height: 1000});
  return {engine, screenshots: ['brandlex_v2_home.png', 'brandlex_v2_studio.png', 'brandlex_v2_library.png', 'brandlex_v2_drawer.png', 'brandlex_v2_mobile.png', 'brandlex_v2_home_mobile.png'].map(name => root + name)};
}
