/* Rendering for the learning cards. Term text is inserted as text nodes. */
(() => {
  'use strict';
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

  window.BrandLexCaseFeed = Object.freeze({ createCard, setLanguage });
})();
