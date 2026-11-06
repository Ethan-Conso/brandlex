async (page) => {
  const base = page.url().split('/').slice(0, 3).join('/');
  let rewrites = 0;
  const watchRequest = request => { if (request.url().endsWith('/api/rewrite')) rewrites += 1; };
  page.on('request', watchRequest);
  try {
    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.setViewportSize({width: 1440, height: 1000});
    await page.goto(base + '/');
    await page.waitForFunction(() => document.querySelectorAll('[data-sample]').length === 4
      && document.querySelector('#antigravity-canvas').dataset.motion === 'reduced');
    await page.evaluate(() => { document.activeElement.blur(); window.scrollTo(0, 0); });
    await page.screenshot({path: 'visual_assets/brandlex_v2_home.png', fullPage: true, scale: 'css', animations: 'disabled'});
    await page.setViewportSize({width: 390, height: 900});
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({path: 'visual_assets/brandlex_v2_home_mobile.png', fullPage: true, scale: 'css', animations: 'disabled'});
    if (rewrites) throw new Error('Homepage capture unexpectedly submitted a draft.');
    return {passed: true, rewrites, screenshots: ['visual_assets/brandlex_v2_home.png', 'visual_assets/brandlex_v2_home_mobile.png']};
  } finally {
    await page.emulateMedia({reducedMotion: 'no-preference'});
    await page.setViewportSize({width: 1440, height: 1000});
    page.off('request', watchRequest);
  }
}
