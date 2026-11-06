async (page) => {
  const base = page.url().split('/').slice(0, 3).join('/');
  const home = 'visual_assets/brandlex_v2_home.png';
  const library = 'visual_assets/brandlex_v2_library.png';
  async function capture(path) {
    await page.mouse.move(6, 90);
    await page.evaluate(async () => {
      await document.fonts.ready;
      document.activeElement.blur();
      window.scrollTo({top: 0, behavior: 'instant'});
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    });
    await page.screenshot({path, fullPage: true, scale: 'css', animations: 'disabled'});
  }
  try {
    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.setViewportSize({width: 1440, height: 1000});
    await page.bringToFront();
    await page.goto(base + '/');
    await page.waitForFunction(() => document.querySelectorAll('[data-home-category]').length === 12
      && document.querySelector('.home-hero [data-go-view="library"]').textContent.trim() === '进入学习'
      && document.querySelector('#tab-home').getAttribute('aria-selected') === 'true'
      && document.querySelector('#antigravity-canvas').dataset.motion === 'reduced');
    await capture(home);

    await page.locator('#tab-library').click();
    await page.waitForFunction(() => {
      const grid = document.querySelector('#case-feed-grid');
      const cards = [...grid.querySelectorAll('[data-term-id]')];
      return cards.length === 6 && new Set(cards.map(card => card.dataset.categoryName)).size === 6
        && grid.getAttribute('aria-busy') === 'false'
        && document.querySelector('#tab-library').textContent.trim() === '学习'
        && document.querySelector('#tab-library').getAttribute('aria-selected') === 'true';
    });
    await capture(library);
    return {screenshots: [home, library]};
  } finally {
    await page.emulateMedia({reducedMotion: 'no-preference'});
  }
}
