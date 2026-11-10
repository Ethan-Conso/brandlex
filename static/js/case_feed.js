/* Rendering for the learning cards and shared detail drawer. */
(() => {
  'use strict';
  const { escapeHtml: esc } = window.BrandLexHelpers;
  const COPY = '<svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="7" y="7" width="9" height="10" rx="1.5" stroke="currentColor" stroke-width="1.5"/><path d="M12 7V3H3v9h4" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>';
  const languages = Object.freeze({ hk: 'zh-HK', cn: 'zh-CN', en: 'en' });

  function setLanguage(card, term, market) {
    if (!Object.hasOwn(languages, market)) return;
    const example = term[`good_example_${market}`];
    const button = card.querySelector('[data-case-copy]');
    const copy = button.querySelector('.case-copy-text');
    copy.textContent = example;
    copy.lang = languages[market];
    button.dataset.copy = example;
    button.setAttribute('aria-label', `复制 ${market.toUpperCase()} 例句：${example}`);
    card.querySelectorAll('[data-case-language]').forEach(tab => {
      const active = tab.dataset.caseLanguage === market;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-pressed', String(active));
    });
  }

  function createCard(term, isAdmin, categoryName = term.category) {
    const card = document.querySelector('#case-card-template').content.firstElementChild.cloneNode(true);
    const find = selector => card.querySelector(selector);
    card.dataset.termId = term.id;
    card.dataset.categoryName = term.category;
    card.setAttribute('aria-label', term.term_en);
    const category = find('[data-case-category]');
    category.textContent = categoryName;
    category.title = term.category;
    find('[data-try-case]').dataset.tryCase = term.id;
    card.querySelectorAll('[data-case-expression]').forEach(button => {
      const market = button.dataset.caseExpression;
      const text = term[`term_${market}`];
      const label = button.querySelector('.case-expression-text');
      label.textContent = text;
      label.lang = languages[market];
      button.dataset.copy = text;
      button.title = `复制 ${text}`;
      button.setAttribute('aria-label', `复制 ${market.toUpperCase()}：${text}`);
    });
    setLanguage(card, term, 'hk');

    const tip = find('[data-case-tip]');
    tip.textContent = term.learning_tip || '';
    tip.hidden = !tip.textContent;
    const detail = find('[data-open-term]');
    detail.dataset.openTerm = term.id;
    detail.setAttribute('aria-label', `查看 ${term.term_en} 详情`);
    for (const [action, label] of [['edit', '编辑'], ['delete', '删除']]) {
      const button = find(`[data-${action}]`);
      button.dataset[action] = term.id;
      button.setAttribute('aria-label', `${label} ${term.term_en}`);
    }
    card.querySelectorAll('.admin-only').forEach(element => { element.hidden = !isAdmin; });
    return card;
  }

  function drawerDefinitions(meaning, language) {
    const marker = meaning.indexOf(' EN: ');
    const chinese = marker > 0 ? meaning.slice(0, marker).trim() : '';
    const english = marker > 0 ? meaning.slice(marker + 5).trim() : '';
    if (!chinese || !english) return `<p>${esc(meaning)}</p>`;
    const chineseLine = `<p lang="zh-CN">${esc(chinese)}</p>`;
    const englishLine = `<p lang="en">${esc(english)}</p>`;
    return `<div class="drawer-definitions">${language === 'en' ? englishLine + chineseLine : chineseLine + englishLine}</div>`;
  }

  function renderTermDetail(content, { term, id, error, language, isAdmin }) {
    content.setAttribute('aria-busy', String(!term && !error));
    if (!term) {
      const status = error
        ? `<p class="drawer-status" role="alert">${esc(error)}</p><button class="button button-secondary" data-open-term="${esc(id)}">重试</button>`
        : '<p class="drawer-status" role="status">正在加载完整释义与例句…</p>';
      content.innerHTML = `<div class="drawer-body"><h2 id="drawer-title">词条详情</h2>${status}</div>`;
      return;
    }
    content.innerHTML = `<div class="drawer-body">
      <p class="drawer-category">${esc(term.category)}</p><h2 id="drawer-title">${esc(term.term_en)}</h2>
      <div class="drawer-expressions">${[['en', 'EN'], ['hk', 'HK'], ['cn', 'CN']].map(([key, label]) => `<button class="drawer-expression" data-copy="${esc(term[`term_${key}`])}" aria-label="复制 ${label}：${esc(term[`term_${key}`])}"><small>${label}</small><span lang="${languages[key]}">${esc(term[`term_${key}`])}</span>${COPY}</button>`).join('')}</div>
      <section class="drawer-section"><h3>简明释义</h3>${drawerDefinitions(term.meaning, language)}<div class="drawer-platforms">${term.platforms.map(platform => `<span class="platform-tag">${esc(platform)}</span>`).join('')}</div></section>
      <section class="drawer-section drawer-bad"><h3>避免写法</h3><p>${esc(term.bad_example)}</p></section>
      <section class="drawer-section"><div class="example-heading"><h3>地道例句</h3><div class="example-tabs" role="group" aria-label="例句语言">${['en', 'hk', 'cn'].map(key => `<button class="example-tab ${language === key ? 'is-active' : ''}" data-language="${key}" aria-pressed="${language === key}">${key.toUpperCase()}</button>`).join('')}</div></div><button class="drawer-good" data-copy="${esc(term[`good_example_${language}`])}" aria-label="复制当前例句"><span>${esc(term[`good_example_${language}`])}</span>${COPY}</button></section>
      <section class="drawer-section drawer-tip"><h3>跨区贴士</h3><p>${esc(term.usage_tip)}</p></section>${isAdmin ? `<div class="drawer-footer"><button class="button button-secondary" data-edit="${esc(term.id)}">编辑词条</button><button class="button button-danger" data-delete="${esc(term.id)}">删除词条</button></div>` : ''}</div>`;
  }

  window.BrandLexCaseFeed = Object.freeze({ createCard, setLanguage, renderTermDetail });
})();
