/* BrandLex workspace. Untrusted copy and glossary content are always escaped. */
(() => {
  'use strict';
  const { escapeHtml: esc, parseList, countDraft, appendCta, resultText, cleanCaseDraft } = window.BrandLexHelpers;
  const { createCard, setLanguage: setCaseLanguage, renderTermDetail } = window.BrandLexCaseFeed;
  const api = window.BrandLexAPI;
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const HOME_DRAFT = 'LUMA 联名香氛礼盒上线，11月15至17日预订享早鸟福利 HK$280，香港包邮。';
  const HOME_PREVIEWS = Object.freeze({
    hk: Object.freeze({
      label: 'HK · 香港繁中', lang: 'zh-HK',
      copy: 'LUMA 跨界聯乘香氛禮盒，為日常添一縷香氣。\n11 月 15 至 17 日預訂，享早鳥禮遇 HK$280，香港免運費。',
      adaptations: Object.freeze(['联名 → 跨界聯乘', '早鸟福利 → 早鳥禮遇', '包邮 → 免運費']),
    }),
    cn: Object.freeze({
      label: 'CN · 内地简中', lang: 'zh-CN',
      copy: 'LUMA 跨界联名香氛礼盒上新，把灵感装进日常。\n11 月 15—17 日预订，早鸟福利 HK$280，香港地区包邮。',
      adaptations: Object.freeze(['联名 → 跨界联名', '上线 → 上新', '香港包邮 → 香港地区包邮']),
    }),
    en: Object.freeze({
      label: 'EN · English', lang: 'en',
      copy: 'A new scent for your everyday.\nDiscover the LUMA fragrance gift set, created in collaboration.\nPre-order 15–17 November for the early-bird price of HK$280. Free shipping in Hong Kong.',
      adaptations: Object.freeze(['联名 → Collaboration', '早鸟福利 → Early-bird price', '包邮 → Free shipping']),
    }),
  });
  const CATEGORY_LABELS = Object.freeze({
    '社媒与种草': '社媒', '电商与转化': '电商', '投放与增长': '投放', '公关与线下': '公关',
    '文案与修辞': '修辞', '美妆与个护': '美妆', '时尚与奢品': '奢品', '数码与科技': '数码',
    '餐饮与酒水': '餐饮', '文旅与酒店': '文旅', '金融与支付': '金融', '合规与风控': '合规',
  });
  const LOCAL_EDIT_NOTICE = '词条已保存在本浏览器';
  const formatCount = new Intl.NumberFormat('zh-CN').format;
  let state = {
    view: 'home', homeMarket: 'hk', terms: [], categories: [], samples: [], category: '',
    total: 0, matchedTotal: 0, nextOffset: 0, hasMore: false, categoryCounts: {},
    loading: true, libraryBusy: false, libraryError: '', libraryQuery: '', lastFeedIds: [], isAdmin: false,
    market: 'hk', tone: 'standard', report: null, version: 'primary', rewriting: false,
    editingId: null, drawerId: null, drawerLanguage: 'hk', drawerError: '', pendingAction: null,
  };
  let termDetails = new Map();
  let csrfToken = $('meta[name="csrf-token"]').content;
  let searchController;
  let detailController;
  let rewriteVersion = 0;
  let searchTimer;
  let toastTimer;
  let rewriteController;
  let busyDialog = null;
  const dialogFocus = new WeakMap();
  function errorMessage(selector, message = '') {
    $(selector).textContent = message;
    $(selector).hidden = !message;
  }

  async function request(path, options = {}) {
    try {
      const result = await api.request(path, { ...options, headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': csrfToken, ...options.headers } });
      if (result.data?.csrf_token) csrfToken = result.data.csrf_token;
      return result.data;
    } catch (error) {
      if (error.status === 403 && error.message.includes('解锁维护模式')) {
        state = { ...state, isAdmin: false };
        renderAdmin();
      }
      throw error;
    }
  }

  function toast(message) {
    clearTimeout(toastTimer);
    $('#toast').textContent = message;
    $('#toast').classList.add('is-visible');
    toastTimer = setTimeout(() => $('#toast').classList.remove('is-visible'), 2500);
  }

  async function copyText(text) {
    if (!text) return;
    try {
      if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(text);
      else {
        const input = document.createElement('textarea');
        input.value = text;
        input.className = 'clipboard-fallback';
        document.body.append(input);
        input.select();
        const copied = document.execCommand('copy');
        input.remove();
        if (!copied) throw new Error();
      }
      toast(`已复制：${text.length > 23 ? text.slice(0, 23) + '…' : text}`);
    } catch { toast('复制暂未完成，请选中文字后复制。'); }
  }

  function switchView(view, focusTab = false, writeHistory = true) {
    const next = ['home', 'library', 'studio'].includes(view) ? view : 'home';
    const changed = next !== state.view;
    if (changed) {
      detailController?.abort();
      if ($('#term-drawer').open) closeDialog('term-drawer');
      if (state.view === 'library') {
        clearTimeout(searchTimer);
        searchController?.abort();
        state = { ...state, libraryBusy: false };
      }
    }
    state = { ...state, view: next };
    $$('.workspace-view').forEach(panel => { panel.hidden = panel.id !== `view-${next}`; });
    $('#main-content').classList.toggle('is-home', next === 'home');
    window.BrandLexHome?.setVisible(next === 'home');
    $$('.nav-tab').forEach(tab => {
      const active = tab.dataset.view === next;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
    });
    if (writeHistory && location.hash !== `#${next}`) history.pushState(null, '', `#${next}`);
    if (changed) window.scrollTo(0, 0);
    if (focusTab) $(`#tab-${next}`).focus();
    if (changed && next === 'library') {
      $('#library-search').value = '';
      $('#category-filters .is-active')?.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      filterTerms();
    }
  }

  function renderHomePreview(market = state.homeMarket, focus = false) {
    const next = Object.hasOwn(HOME_PREVIEWS, market) ? market : 'hk';
    const preview = HOME_PREVIEWS[next];
    state = { ...state, homeMarket: next };
    $('#home-source-copy').textContent = HOME_DRAFT;
    $('#home-preview-copy').textContent = preview.copy;
    $('#home-preview-copy').lang = preview.lang;
    $('#home-preview-market').textContent = preview.label;
    $('#home-preview-panel').setAttribute('aria-labelledby', `home-market-${next}`);
    $('#home-preview-adaptations').innerHTML = preview.adaptations.map(item => `<span>${esc(item)}</span>`).join('');
    $$('[data-home-market]').forEach(tab => {
      const active = tab.dataset.homeMarket === next;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
    });
    if (focus) $(`[data-home-market="${next}"]`).focus();
  }

  function openHomeScenario(category) {
    state = { ...state, category };
    markCategorySelection();
    switchView('library', true);
  }

  function editHomeDraft() {
    if (state.loading) return;
    $('#copy-text').value = HOME_DRAFT;
    setOption('market', state.homeMarket);
    setOption('tone', 'standard');
    invalidateResult();
    errorMessage('#copy-error');
    switchView('studio', true);
    rewriteCopy();
  }

  function renderCategories() {
    const categoryCount = name => formatCount(state.categoryCounts[name] || 0);
    const filters = [['', '全部'], ...state.categories.map(name => [name, CATEGORY_LABELS[name] || name])];
    $('#category-filters').innerHTML = filters.map(([value, label]) => (
      `<button type="button" class="category-pill" data-category="${esc(value)}" aria-label="${esc(value || label)}" title="${esc(value || label)}">${esc(label)}</button>`
    )).join('');
    markCategorySelection();

    const current = $('#field-category').value;
    $('#field-category').innerHTML = state.categories.map(name => `<option value="${esc(name)}">${esc(name)}</option>`).join('');
    if (state.categories.includes(current)) $('#field-category').value = current;

    $('#home-scenario-pills').innerHTML = state.categories.map(name => (
      `<button type="button" data-home-category="${esc(name)}" title="${categoryCount(name)} 条词条">${esc(name)}</button>`
    )).join('');
    const homeCount = $('#home-library-count');
    homeCount.textContent = `${formatCount(state.total)} 条三语词条 · ${state.categories.length} 个营销场景`;
    homeCount.hidden = false;
  }

  function markCategorySelection() {
    $$('#category-filters [data-category]').forEach(button => {
      const active = button.dataset.category === state.category;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  }

  function selectCategory(category) {
    state = { ...state, category };
    markCategorySelection();
    filterTerms();
  }

  function renderAdmin() {
    $$('.admin-only').forEach(element => { element.hidden = !state.isAdmin; });
    $('#admin-label').textContent = state.isAdmin ? '已解锁' : '维护模式';
    $('#admin-toggle').classList.toggle('is-admin', state.isAdmin);
    $('#admin-toggle').setAttribute('aria-label', state.isAdmin ? '维护模式已解锁，点击退出' : '解锁维护模式');
    if ($('#term-drawer').open) renderDrawer();
  }

  function renderRewriteSettings() {
    if (!api.isStatic()) return;
    $('#deepseek-key-toggle').hidden = false;
    $('#rewrite-privacy-note').textContent = api.getDeepSeekKey()
      ? '原稿与命中词条将直接发送至 DeepSeek，个人密钥仅在本次浏览器会话有效。'
      : api.hasPublicRewrite()
        ? '在线改写支持 4,000 字，经 BrandLex 服务将原稿与命中词条发送至 DeepSeek。'
        : '当前可使用示例或本地预览。设置个人密钥后可连接 DeepSeek 进行全文改写。';
  }

  function renderLibrary(terms = state.terms, append = false) {
    const grid = $('#case-feed-grid');
    const cards = terms.map(term => createCard(term, state.isAdmin, CATEGORY_LABELS[term.category] || term.category));
    if (append) grid.append(...cards);
    else grid.replaceChildren(...cards);
  }

  function renderPager() {
    const count = $('#library-count');
    const more = $('#load-more-terms');
    const shuffle = $('#shuffle-feed');
    const bottomShuffle = $('[data-action="shuffle-feed"]');
    const query = $('#library-search').value.trim();
    const busy = (state.loading && !state.libraryError) || state.libraryBusy;
    const scope = state.category ? state.matchedTotal : state.total;
    const summary = state.libraryQuery ? `匹配 ${formatCount(state.matchedTotal)} 组` : `随机推荐 ${formatCount(state.terms.length)} 组 · 共 ${formatCount(scope)} 组`;
    count.textContent = busy ? (query ? '正在搜索案例…' : '正在加载案例…') : state.libraryError ? '案例加载失败' : summary;
    $('#case-feed-grid').setAttribute('aria-busy', String(busy));
    const message = $('#case-feed-message');
    message.textContent = state.libraryError || (busy ? '正在加载案例…' : '暂无匹配案例，试试其他关键词或分类。');
    message.hidden = state.terms.length > 0;
    shuffle.disabled = state.loading;
    for (const button of [shuffle, bottomShuffle, more]) button.setAttribute('aria-disabled', String(busy));
    const active = document.activeElement;
    bottomShuffle.hidden = state.loading || Boolean(query) || (!state.terms.length && !state.libraryError);
    more.hidden = !query || !state.hasMore || query !== state.libraryQuery;
    if ((active === more && more.hidden) || (active === bottomShuffle && bottomShuffle.hidden)) count.focus({ preventScroll: true });
  }

  function acceptPage(data, query = '', append = false) {
    const countsChanged = data.total !== state.total ||
      state.categories.some(name => state.categoryCounts[name] !== data.category_counts[name]);
    const loaded = append ? new Set(state.terms.map(term => term.id)) : null;
    const additions = loaded ? data.terms.filter(term => !loaded.has(term.id)) : data.terms;
    state = {
      ...state, terms: append ? [...state.terms, ...additions] : additions,
      total: data.total, matchedTotal: data.matched_total, nextOffset: data.offset + data.terms.length,
      hasMore: data.has_more, categoryCounts: data.category_counts, libraryError: '', libraryQuery: query,
      lastFeedIds: query ? state.lastFeedIds : data.terms.map(term => term.id),
    };
    if (countsChanged) renderCategories();
    renderLibrary(additions, append);
  }

  async function fetchLibraryPage(append = false) {
    if (state.loading || state.view !== 'library' || (append && (state.libraryBusy || !state.hasMore))) return;
    const controller = new AbortController();
    searchController = controller;
    state = { ...state, libraryBusy: true };
    renderPager();
    const query = $('#library-search').value.trim();
    const params = new URLSearchParams({ mode: 'feed', category: state.category });
    if (query) params.set('q', query);
    if (query && append) params.set('offset', state.nextOffset);
    if (!query && state.lastFeedIds.length) params.set('exclude', state.lastFeedIds.join(','));
    try {
      const data = await request(`/api/terms?${params}`, { signal: controller.signal });
      if (controller.signal.aborted) return;
      acceptPage(data, query, append);
      errorMessage('#app-error');
    } catch (error) {
      if (controller.signal.aborted) return;
      if (!append) {
        state = { ...state, terms: [], matchedTotal: 0, hasMore: false, nextOffset: 0, libraryError: '案例暂未加载，请重试。' };
        renderLibrary();
      }
      errorMessage('#app-error', error.message);
    } finally {
      if (searchController === controller) searchController = null;
      if (!controller.signal.aborted) {
        state = { ...state, libraryBusy: false };
        renderPager();
      }
    }
  }

  function filterTerms(delay = 0) {
    clearTimeout(searchTimer);
    searchController?.abort();
    if (state.loading || state.view !== 'library') return;
    state = { ...state, libraryBusy: true };
    renderPager();
    if (delay) searchTimer = setTimeout(fetchLibraryPage, delay);
    else return fetchLibraryPage();
  }

  function shuffleFeed(bottom) {
    if (state.loading || state.libraryBusy) return;
    $('#library-search').value = '';
    if (bottom) {
      $('#library-count').focus({ preventScroll: true });
      window.scrollTo(0, 0);
    }
    filterTerms();
  }

  function caseRecord(id) {
    return state.terms.find(term => term.id === id) || termDetails.get(id);
  }

  function tryCase(button) {
    const term = caseRecord(Number(button.dataset.tryCase));
    const draft = cleanCaseDraft(term?.bad_example);
    if (!draft) return;
    const market = button.closest('.case-card').querySelector('[data-case-language][aria-pressed="true"]').dataset.caseLanguage;
    $('#copy-text').value = draft;
    setOption('market', market);
    setOption('tone', 'standard');
    invalidateResult();
    errorMessage('#copy-error');
    switchView('studio', true);
    rewriteCopy();
  }

  function renderSamples() {
    const titles = ['美妆种草', '数码发布', '节日礼盒', '快闪活动'];
    $('#sample-drafts').innerHTML = state.samples.map((sample, index) => `<button class="sample-button" data-sample="${esc(sample.id)}" title="${esc(sample.title)}">${esc(titles[index] || sample.title)}</button>`).join('');
  }

  function setOption(type, value) {
    state = { ...state, [type]: value };
    $$(`[data-${type}]`).forEach(button => {
      const active = button.dataset[type] === value;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    if (type === 'market') $('#market-hint').textContent = { hk: 'Instagram / Facebook', cn: '小红书 / 微信', en: 'Global marketing' }[value];
  }

  function updateCounts() {
    const text = $('#copy-text').value;
    const counts = countDraft(text);
    $('#draft-stats').innerHTML = `<span>${counts.character_count.toLocaleString()} 字符 · ${counts.word_count.toLocaleString()} 字词</span><span>约 ${counts.reading_time_seconds} 秒阅读</span>`;
    $('#rewrite-copy').disabled = !text.trim() || state.rewriting || state.loading;
    $('#clear-copy').disabled = !text;
  }

  function invalidateResult() {
    rewriteVersion += 1;
    rewriteController?.abort();
    state = { ...state, report: null, rewriting: false, version: 'primary' };
    $('#output-content').hidden = true;
    $('#output-loading').hidden = true;
    $('#output-empty').hidden = false;
    $('#copy-results').setAttribute('aria-busy', 'false');
    $('#engine-label').textContent = '待改写';
    $('#engine-label').classList.remove('is-live');
    $('#rewrite-copy span').textContent = '智能改写';
    setVersion('primary');
    updateCounts();
  }

  function setVersion(version, focus = false) {
    state = { ...state, version: version === 'alt' ? 'alt' : 'primary' };
    $$('[data-version]').forEach(tab => {
      const active = tab.dataset.version === state.version;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
    });
    $('#rewritten-copy').setAttribute('aria-labelledby', `version-${state.version}`);
    if (state.report) {
      const copy = resultText(state.report, state.version);
      $('#rewritten-copy').textContent = copy;
      $('#rewritten-copy').lang = { hk: 'zh-HK', cn: 'zh-CN', en: 'en' }[state.market];
      const counts = countDraft(copy);
      $('#output-stats').textContent = `${counts.character_count.toLocaleString()} 字符 · ${counts.word_count.toLocaleString()} 字词`;
    }
    if (focus) $(`#version-${state.version}`).focus();
  }

  function renderResult(report) {
    const matched = report.matched_glossary_terms || [];
    const known = new Set(matched.map(term => term.id));
    const adaptations = report.adaptations || [];
    $('#adaptation-count').textContent = String(adaptations.length);
    $('#adaptations-list').innerHTML = adaptations.length ? adaptations.map(item => `<div class="adaptation-row"><div><div class="adaptation-line"><span class="adaptation-original">${esc(item.original)}</span><span class="adaptation-arrow" aria-hidden="true">→</span><span class="adaptation-adapted">${esc(item.adapted)}</span></div><p>${esc(item.reason)}</p></div>${known.has(item.term_id) ? `<button class="glossary-link" data-open-term="${esc(item.term_id)}">词库标准</button>` : ''}</div>`).join('') : '<p class="no-adaptations">本次暂无可核对的改动。</p>';
    $('#matched-terms').innerHTML = matched.map(term => `<button class="matched-term" data-open-term="${esc(term.id)}"><small>词条</small>${esc(term[`term_${state.market}`] || term.term_en)}</button>`).join('');
    $('#cta-list').innerHTML = (report.cta_options || []).map((cta, index) => `<button class="cta-button" data-cta="${index}"><span>${esc(cta)}</span><span aria-hidden="true">+</span></button>`).join('');
    $('.cta-section').hidden = !(report.cta_options || []).length;
    $('#engine-label').textContent = api.engineLabel(report);
    $('#engine-label').classList.toggle('is-live', report.engine === 'deepseek');
    const notice = report.notice || report.message || (report.engine === 'fallback' ? '当前为本地预览，已调整常见用词与繁简字形。完整语境改写需连接 DeepSeek。' : '');
    $('#engine-notice').textContent = notice;
    $('#engine-notice').hidden = !notice;
    $('#output-empty').hidden = true;
    $('#output-loading').hidden = true;
    $('#output-content').hidden = false;
    setVersion(state.version);
  }

  async function rewriteCopy() {
    const text = $('#copy-text').value;
    if (!text.trim() || state.rewriting || state.loading) return;
    const { market, tone } = state;
    const version = ++rewriteVersion;
    rewriteController?.abort();
    rewriteController = new AbortController();
    state = { ...state, rewriting: true, report: null, version: 'primary' };
    $('#output-content').hidden = true;
    $('#output-empty').hidden = true;
    $('#output-loading').hidden = false;
    $('#copy-results').setAttribute('aria-busy', 'true');
    $('#engine-label').textContent = '改写中';
    $('#rewrite-copy span').textContent = '正在改写…';
    errorMessage('#copy-error');
    updateCounts();
    try {
      const report = await request('/api/rewrite', { method: 'POST', signal: rewriteController.signal, body: JSON.stringify({ text, target_market: market, tone }) });
      if (version !== rewriteVersion || text !== $('#copy-text').value || market !== state.market || tone !== state.tone) return;
      state = { ...state, report };
      renderResult(report);
    } catch (error) {
      if (version === rewriteVersion && error.name !== 'AbortError') {
        errorMessage('#copy-error', error.message);
        $('#output-empty').hidden = false;
        $('#engine-label').textContent = '待改写';
      }
    } finally {
      if (version === rewriteVersion) {
        state = { ...state, rewriting: false };
        $('#output-loading').hidden = true;
        $('#copy-results').setAttribute('aria-busy', 'false');
        $('#rewrite-copy span').textContent = '智能改写';
        updateCounts();
      }
    }
  }

  function insertCta(index) {
    if (!state.report) return;
    const cta = state.report.cta_options?.[index];
    if (typeof cta !== 'string') return;
    const field = state.version === 'alt' ? 'alt_copy' : 'primary_copy';
    const copy = appendCta(resultText(state.report, state.version), cta);
    state = { ...state, report: { ...state.report, [field]: copy } };
    setVersion(state.version);
    toast('已加入当前版本');
  }

  function showDialog(id, trigger = document.activeElement) {
    if (busyDialog) return;
    const dialog = $(`#${id}`);
    if (dialog.open) return;
    if (id !== 'term-drawer') detailController?.abort();
    dialogFocus.set(dialog, trigger);
    dialog.showModal();
  }

  function closeDialog(id, force = false) {
    if (busyDialog === id && !force) return;
    if (id === 'term-drawer') detailController?.abort();
    $(`#${id}`).close();
  }

  function renderDrawer() {
    const { drawerId: id, drawerError: error, drawerLanguage: language, isAdmin } = state;
    renderTermDetail($('#drawer-content'), { term: caseRecord(id), id, error, language, isAdmin });
  }

  async function readTermDetail(id) {
    detailController?.abort();
    const cached = caseRecord(id);
    if (cached) return cached;
    const controller = new AbortController();
    detailController = controller;
    try {
      const term = await request(`/api/terms/${id}`, { signal: controller.signal });
      controller.signal.throwIfAborted();
      termDetails = new Map(termDetails).set(id, term);
      return term;
    } finally {
      if (detailController === controller) detailController = null;
    }
  }

  async function openDrawer(id, trigger) {
    if (!Number.isSafeInteger(id) || id < 1 || busyDialog || $('dialog[open]:not(#term-drawer)')) return;
    const drawer = $('#term-drawer');
    state = { ...state, drawerId: id, drawerLanguage: state.market, drawerError: '' };
    renderDrawer();
    showDialog('term-drawer', trigger);
    drawer.scrollTop = 0;
    try {
      await readTermDetail(id);
      if (state.drawerId === id && drawer.open) renderDrawer();
    } catch (error) {
      if (error.name === 'AbortError' || state.drawerId !== id || !drawer.open) return;
      state = { ...state, drawerError: error.message };
      renderDrawer();
    }
  }

  function fillTermForm(record) {
    for (const field of $('#term-form').elements) {
      if (field.name) field.value = Array.isArray(record[field.name]) ? record[field.name].join(', ') : record[field.name] || '';
    }
  }

  async function openTerm(id = null) {
    if (!state.isAdmin || busyDialog || $('dialog[open]:not(#term-drawer)')) return;
    let term;
    try {
      if (id) term = await readTermDetail(id);
    } catch (error) {
      if (error.name !== 'AbortError') toast(error.message);
      return;
    }
    if (!state.isAdmin || busyDialog || $('dialog[open]:not(#term-drawer)')) return;
    if ($('#term-drawer').open) closeDialog('term-drawer');
    state = { ...state, editingId: id };
    $('#term-form').reset();
    if (term) fillTermForm(term);
    $('#term-dialog-title').textContent = id ? '编辑词条' : '新增词条';
    $('#fill-example').hidden = Boolean(id);
    errorMessage('#term-error');
    showDialog('term-dialog');
  }

  function exampleTerm() {
    fillTermForm({ term_en: 'Brand Newsletter', term_hk: '品牌電子通訊', term_cn: '品牌订阅邮件', aliases: ['newsletter', '品牌邮件', '電子報'], category: state.categories[0], platforms: ['EDM', 'Shopify'], meaning: '定期把新品、品牌故事或实用内容发给主动订阅的读者，让品牌与受众保持联系。', bad_example: '欢迎接收我们的新闻信。——机械照搬 newsletter 的字面意思，读者难以理解。', good_example_en: 'A little inspiration for your inbox. Subscribe for new arrivals and stories worth sharing.', good_example_hk: '訂閱品牌電子通訊，率先接收新品消息，發掘日常生活的小靈感。', good_example_cn: '订阅品牌邮件，第一时间获取上新消息，也收获一点日常灵感。', usage_tip: '香港可用「電子通訊」，内地可写「订阅邮件」；清楚说明内容与频率，并提供取消订阅方式。' });
    $('#field-term-en').focus();
  }

  async function loadBootstrap() {
    const data = await request('/api/bootstrap');
    renderRewriteSettings();
    state = {
      ...state, categories: data.categories, samples: data.samples,
      isAdmin: data.is_admin === true, loading: false,
    };
    acceptPage(data);
    renderPager();
    renderSamples();
    renderAdmin();
    $('#home-edit-draft').disabled = false;
    if (state.category || $('#library-search').value.trim()) filterTerms();
    updateCounts();
  }

  function refreshLibrary() {
    detailController?.abort();
    termDetails = new Map();
    return state.view === 'library' ? filterTerms() : loadBootstrap();
  }

  async function saveTerm(event) {
    event.preventDefault();
    if (!state.isAdmin || busyDialog || !$('#term-form').reportValidity()) return;
    const values = Object.fromEntries(new FormData($('#term-form')));
    const record = { ...values, aliases: parseList(values.aliases), platforms: parseList(values.platforms) };
    if (!record.aliases.length || !record.platforms.length) { errorMessage('#term-error', '请填写至少一个别称和适用平台。'); return; }
    const id = state.editingId;
    busyDialog = 'term-dialog';
    $('#save-term').disabled = true;
    errorMessage('#term-error');
    try {
      await request(id ? `/api/terms/${id}` : '/api/terms', { method: id ? 'PATCH' : 'POST', body: JSON.stringify(record) });
      closeDialog('term-dialog', true);
      await refreshLibrary();
      invalidateResult();
      toast(api.isStatic() ? LOCAL_EDIT_NOTICE : id ? '词条已更新' : '词条已新增');
      if (state.view === 'library') $('#library-search').focus();
    } catch (error) { errorMessage($('#term-dialog').open ? '#term-error' : '#app-error', error.message); }
    finally { busyDialog = null; $('#save-term').disabled = false; }
  }

  function askAction(type, id = null) {
    if (!state.isAdmin || busyDialog) return;
    const term = caseRecord(id);
    if (type === 'delete' && !term) return;
    if ($('#term-drawer').open) closeDialog('term-drawer');
    state = { ...state, pendingAction: { type, id } };
    $('#confirm-title').textContent = { delete: '删除词条？', reset: '重置词库？', logout: '退出维护？' }[type];
    $('#confirm-description').textContent = type === 'delete' ? `「${term.term_en}」将从词库移除。` : type === 'reset' ? '将恢复默认词库，当前新增与修改会被替换。需要保留时，请先导出词库。' : '退出后，词库恢复为只读模式。';
    $('#confirm-action').textContent = { delete: '删除', reset: '重置', logout: '退出' }[type];
    errorMessage('#confirm-error');
    showDialog('confirm-dialog');
  }

  async function confirmAction() {
    const action = state.pendingAction;
    if (!state.isAdmin || !action || busyDialog) return;
    busyDialog = 'confirm-dialog';
    $('#confirm-action').disabled = true;
    try {
      if (action.type === 'logout') await logoutAdmin();
      else if (action.type === 'reset') await request('/api/library/reset', { method: 'POST', body: JSON.stringify({ confirm: true }) });
      else await request(`/api/terms/${action.id}`, { method: 'DELETE' });
      closeDialog('confirm-dialog', true);
      state = { ...state, pendingAction: null };
      if (action.type !== 'logout') {
        await refreshLibrary();
        invalidateResult();
        const deletionNotice = api.isStatic() ? LOCAL_EDIT_NOTICE : '词条已删除';
        toast(action.type === 'reset' ? '已恢复默认词库' : deletionNotice);
      }
      if (state.view === 'library') $('#library-search').focus();
    } catch (error) { errorMessage($('#confirm-dialog').open ? '#confirm-error' : '#app-error', error.message); }
    finally { busyDialog = null; $('#confirm-action').disabled = false; }
  }

  async function loginAdmin(event) {
    event.preventDefault();
    if (busyDialog || !$('#admin-form').reportValidity()) return;
    busyDialog = 'admin-dialog';
    $('#admin-submit').disabled = true;
    errorMessage('#admin-error');
    try {
      const data = await request('/api/admin/login', { method: 'POST', body: JSON.stringify({ password: $('#admin-password').value }) });
      state = { ...state, isAdmin: data.is_admin === true };
      $('#admin-password').value = '';
      closeDialog('admin-dialog', true);
      renderAdmin();
      toast(api.isStatic() ? '维护模式已解锁（当前演示修改保存在本浏览器）' : '维护模式已解锁');
    } catch (error) { errorMessage('#admin-error', error.message); }
    finally { busyDialog = null; $('#admin-submit').disabled = false; }
  }

  async function logoutAdmin() {
    const data = await request('/api/admin/logout', { method: 'POST', body: JSON.stringify({}) });
    state = { ...state, isAdmin: data.is_admin === true };
    renderAdmin();
    $('#admin-password').value = '';
    toast('已退出维护模式');
  }

  async function downloadLibrary(link) {
    link.closest('details')?.removeAttribute('open');
    try {
      await api.downloadExport(new URL(link.href).pathname.split('/').pop());
      toast('词库已导出');
    } catch (error) { errorMessage('#app-error', error.message); }
  }

  function saveDeepSeekKey(event) {
    event.preventDefault();
    if (!api.isStatic()) return;
    const key = $('#deepseek-key-input').value;
    try {
      api.setDeepSeekKey(key);
      closeDialog('deepseek-key-dialog');
      renderRewriteSettings();
      invalidateResult();
      toast(key.trim() ? '本次会话已启用 DeepSeek' : '已清除 DeepSeek API Key');
    } catch (error) { errorMessage('#deepseek-key-error', error.message); }
  }

  function onClick(event) {
    const button = event.target.closest('button, a');
    if (button?.matches('.skip-link')) {
      event.preventDefault();
      $('#main-content').tabIndex = -1;
      $('#main-content').focus({ preventScroll: true });
      window.scrollTo(0, 0);
    } else if (button?.matches('.brand')) { event.preventDefault(); switchView('home', true); }
    else if (button?.matches('[data-view]')) switchView(button.dataset.view);
    else if (button?.matches('[data-go-view]')) { event.preventDefault(); switchView(button.dataset.goView, true); }
    else if (button?.matches('[data-home-market]')) renderHomePreview(button.dataset.homeMarket);
    else if (button?.matches('[data-home-category]')) openHomeScenario(button.dataset.homeCategory);
    else if (button?.id === 'home-edit-draft') editHomeDraft();
    else if (button?.id === 'shuffle-feed' || button?.matches('[data-action="shuffle-feed"]')) shuffleFeed(button.id !== 'shuffle-feed');
    else if (button?.matches('[data-try-case]')) tryCase(button);
    else if (button?.matches('[data-case-language]')) {
      const card = button.closest('.case-card');
      const term = caseRecord(Number(card.dataset.termId));
      if (term) setCaseLanguage(card, term, button.dataset.caseLanguage);
    } else if (button?.matches('[data-copy]')) copyText(button.dataset.copy);
    else if (button?.matches('[data-close]')) closeDialog(button.dataset.close);
    else if (button?.matches('[data-open-term]')) openDrawer(Number(button.dataset.openTerm), button);
    else if (button?.matches('[data-category]')) selectCategory(button.dataset.category);
    else if (button?.matches('[data-market], [data-tone]')) {
      const type = button.dataset.market ? 'market' : 'tone';
      setOption(type, button.dataset[type]);
      invalidateResult();
      errorMessage('#copy-error');
    } else if (button?.matches('[data-sample]')) {
      const sample = state.samples.find(item => item.id === button.dataset.sample);
      if (!sample) return;
      $('#copy-text').value = sample.text;
      setOption('market', sample.target_market);
      invalidateResult();
      errorMessage('#copy-error');
      $('#copy-text').focus();
    } else if (button?.matches('[data-version]')) setVersion(button.dataset.version);
    else if (button?.matches('[data-cta]')) insertCta(Number(button.dataset.cta));
    else if (button?.matches('[data-language]')) {
      state = { ...state, drawerLanguage: button.dataset.language };
      renderDrawer();
      $(`[data-language="${state.drawerLanguage}"]`)?.focus();
    } else if (button?.matches('[data-action="add-term"]')) openTerm();
    else if (button?.matches('[data-edit]')) openTerm(Number(button.dataset.edit));
    else if (button?.matches('[data-delete]')) askAction('delete', Number(button.dataset.delete));
    else if (button?.matches('.export-options a, [data-home-export]')) { event.preventDefault(); downloadLibrary(button); }
    else if (!button && window.getSelection()?.isCollapsed !== false) {
      const card = event.target.closest('.case-card');
      if (card) openDrawer(Number(card.dataset.termId), card.querySelector('[data-open-term]'));
    }
  }

  function onKeydown(event) {
    const dialogOpen = document.querySelector('dialog[open]');
    if ((event.metaKey || event.ctrlKey) && event.key === 'Enter' && state.view === 'studio' && !dialogOpen) { event.preventDefault(); rewriteCopy(); }
    if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !dialogOpen && !event.target.closest('input,textarea,select,[contenteditable="true"]')) {
      event.preventDefault(); switchView('library'); $('#library-search').focus();
    }
    if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) {
      const navigation = event.target.matches('.nav-tab');
      const versions = event.target.matches('[data-version]');
      const preview = event.target.matches('[data-home-market]');
      if (!navigation && !versions && !preview) return;
      event.preventDefault();
      const tabs = $$(navigation ? '.nav-tab' : preview ? '[data-home-market]' : '[data-version]');
      const current = tabs.indexOf(event.target);
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (current + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      if (navigation) switchView(tabs[next].dataset.view, true);
      else if (preview) renderHomePreview(tabs[next].dataset.homeMarket, true);
      else setVersion(tabs[next].dataset.version, true);
    }
  }

  function bindEvents() {
    document.addEventListener('click', onClick);
    document.addEventListener('keydown', onKeydown);
    const restoreView = () => switchView(location.hash.slice(1), false, false);
    window.addEventListener('hashchange', restoreView);
    window.addEventListener('popstate', restoreView);
    $('#library-search').addEventListener('input', () => filterTerms(140));
    $('#load-more-terms').addEventListener('click', () => fetchLibraryPage(true));
    $('#copy-text').addEventListener('input', () => { invalidateResult(); errorMessage('#copy-error'); });
    $('#rewrite-copy').addEventListener('click', rewriteCopy);
    $('#clear-copy').addEventListener('click', () => { $('#copy-text').value = ''; invalidateResult(); errorMessage('#copy-error'); $('#copy-text').focus(); });
    $('#copy-output').addEventListener('click', () => copyText(resultText(state.report, state.version)));
    $('#use-output').addEventListener('click', () => { const copy = resultText(state.report, state.version); if (!copy) return; $('#copy-text').value = copy; invalidateResult(); toast('已替换原稿'); $('#copy-text').focus(); });
    $('#term-form').addEventListener('submit', saveTerm);
    $('#fill-example').addEventListener('click', exampleTerm);
    $('#reset-library').addEventListener('click', () => askAction('reset'));
    $('#confirm-action').addEventListener('click', confirmAction);
    $('#admin-form').addEventListener('submit', loginAdmin);
    $('#admin-toggle').addEventListener('click', () => {
      if (state.isAdmin) askAction('logout');
      else { $('#admin-form').reset(); errorMessage('#admin-error'); showDialog('admin-dialog'); }
    });
    $('#admin-logout').addEventListener('click', () => askAction('logout'));
    $('#deepseek-key-form').addEventListener('submit', saveDeepSeekKey);
    $('#deepseek-key-toggle').addEventListener('click', () => {
      $('#deepseek-key-input').placeholder = api.getDeepSeekKey() ? '会话已设置密钥，留空保存可清除' : '输入 DeepSeek API Key';
      showDialog('deepseek-key-dialog');
    });
    $$('dialog').forEach(dialog => {
      dialog.addEventListener('close', () => {
        if (dialog.id === 'admin-dialog') $('#admin-password').value = '';
        if (dialog.id === 'deepseek-key-dialog') { $('#deepseek-key-form').reset(); errorMessage('#deepseek-key-error'); }
        if (dialog.id === 'term-drawer' && !dialog.open) {
          state = { ...state, drawerId: null, drawerError: '' };
        }
        const target = dialogFocus.get(dialog);
        if (target?.isConnected && !target.closest('[hidden]')) target.focus();
        else $({ home: '#tab-home', library: '#library-search', studio: '#copy-text' }[state.view]).focus();
      });
      dialog.addEventListener('cancel', event => {
        if (busyDialog === dialog.id) event.preventDefault();
        else if (dialog.id === 'term-drawer') detailController?.abort();
      });
      dialog.addEventListener('click', event => {
        if (event.target !== dialog || busyDialog === dialog.id) return;
        const rect = dialog.getBoundingClientRect();
        if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDialog(dialog.id);
      });
    });
    document.addEventListener('click', event => $$('.export-menu[open]').forEach(menu => { if (!menu.contains(event.target)) menu.open = false; }));
  }

  async function initialize() {
    bindEvents();
    window.BrandLexHome?.initialize();
    switchView(location.hash.slice(1), false, false);
    renderHomePreview();
    updateCounts();
    try { await loadBootstrap(); }
    catch (error) {
      errorMessage('#app-error', `${error.message} 请刷新页面重试。`);
      state = { ...state, libraryError: '案例暂未加载，请刷新重试。' };
      renderPager();
    }
  }
  initialize();
})();
