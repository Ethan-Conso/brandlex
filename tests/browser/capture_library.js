async (page) => {
  const base = new URL(page.url()).origin;
  const screenshot = 'visual_assets/brandlex_v2_library.png';
  try {
    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.setViewportSize({width: 1440, height: 1000});
    await page.goto(base + '/?capture=library#library');
    await page.waitForFunction(() => document.querySelectorAll('#case-feed-grid > [data-term-id]').length === 6
      && document.querySelector('#case-feed-grid').getAttribute('aria-busy') === 'false');
    await page.evaluate(async () => {
      await document.fonts.ready;
      document.activeElement.blur();
      window.scrollTo(0, 0);
    });
    await page.screenshot({path: screenshot, fullPage: true, scale: 'css', animations: 'disabled'});
    return {screenshot, cases: 6};
  } finally {
    await page.emulateMedia({reducedMotion: 'no-preference'});
  }
}
