/* Browser API adapter for the published BrandLex workspace. */
(() => {
  'use strict';
  const EDITS_KEY = 'brandlex_static_edits';
  const LEGACY_SEED_MAX_ID = 3203;
  const ADMIN_KEY = 'brandlex_static_admin_until';
  const DEEPSEEK_KEY = 'brandlex_deepseek_key';
  const ADMIN_DIGEST = '27f9a8244ebd8b37a73ab917581ff97435e4bd623e2489125bba781bed8fc49c';
  const ADMIN_DURATION = 8 * 60 * 60 * 1000;
  const rewriteGateway = document.querySelector('meta[name="brandlex-public-rewrite-url"]')?.content || '';
  const TERM_FIELDS = ['id', 'term_en', 'term_hk', 'term_cn', 'aliases', 'category', 'platforms', 'meaning', 'bad_example', 'good_example_en', 'good_example_hk', 'good_example_cn', 'usage_tip'];
  const EXPRESSIONS = ['term_en', 'term_hk', 'term_cn'];
  const CONTEXT_FIELDS = ['category', 'bad_example', 'good_example_en', 'good_example_hk', 'good_example_cn'];
  const LIST_FIELDS = ['aliases', 'platforms'];
  const EDITABLE_FIELDS = TERM_FIELDS.slice(1);
  const LABELS = {
    term_en: '英文表达', term_hk: '香港表达', term_cn: '内地表达', aliases: '别名', category: '业务分类',
    platforms: '适用平台', meaning: '一句话解析', bad_example: '踩坑写法', good_example_en: '英文例句',
    good_example_hk: '香港例句', good_example_cn: '内地例句', usage_tip: '跨区用词贴士',
  };
  const FEED_BATCH = 6;
  const MAX_PAGE = 200;
  const MAX_DRAFT = 20000;
  const MAX_RELAY_DRAFT = 4000;
  const MAX_REQUEST = 192 * 1024;
  const MARKETS = ['hk', 'cn', 'en'];
  const TONES = ['standard', 'social', 'concise'];
  const MISSING = '没有找到这条内容，请刷新词库后重试。';
  const STORAGE_ERROR = '词库暂时无法读取或保存，请稍后重试。';
  const BILINGUAL_MEANING_ERROR = '请按「中文释义 EN: English definition」格式填写中英文释义。';
  const SPACE = /[\p{White_Space}\u001c-\u001f]+/gu;
  const HAN = /[\u3400-\u9fff\uf900-\ufaff\u{20000}-\u{323af}]/u;
  const UNSUPPORTED = /[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\p{Cs}\ufffe\uffff]/u;
  const encoder = new TextEncoder();
  const files = new Map();
  let csrfToken = '';
  let adminUntil = Number(storage('sessionStorage', ADMIN_KEY)) || 0;
  let lastSnapshot;

  function fail(status, message) {
    throw Object.assign(new Error(message), { status });
  }

  function trim(text) {
    return text.replace(/^[\p{White_Space}\u001c-\u001f]+|[\p{White_Space}\u001c-\u001f]+$/gu, '');
  }

  function storage(kind, name) {
    try { return window[kind].getItem(name); }
    catch { return null; }
  }

  function loadFile(name, optional = false) {
    if (!files.has(name)) {
      const url = new URL(`data/${name}.json`, document.baseURI);
      const loaded = fetch(url, { credentials: 'same-origin' }).then(response => {
        if (response.ok) return response.json();
        if (optional && response.status === 404) return null;
        fail(503, STORAGE_ERROR);
      }).catch(() => {
        files.delete(name);
        if (optional) return null;
        fail(503, STORAGE_ERROR);
      });
      files.set(name, loaded);
    }
    return files.get(name);
  }

  function validId(id) {
    return Number.isSafeInteger(id) && id > 0;
  }

  function bilingualMeaning(value) {
    const marker = /(?<=[\p{White_Space}\u001c-\u001f])EN:/u.exec(value);
    const chinese = marker ? trim(value.slice(0, marker.index)) : '';
    const english = marker ? trim(value.slice(marker.index + marker[0].length)) : '';
    if (!HAN.test(chinese) || !/\b(?!EN:)[A-Za-z]{2,}\b/u.test(english)) {
      fail(400, BILINGUAL_MEANING_ERROR);
    }
    return `${chinese} EN: ${english}`;
  }

  function validateRecord(record, categories, { requireBilingual = true } = {}) {
    const fieldError = field => fail(400, `请检查「${LABELS[field]}」，填写有效且完整的内容。`);
    const fieldText = (text, field, limit) => {
      if (typeof text !== 'string' || !trim(text) || Array.from(text).length > limit || UNSUPPORTED.test(text)) fieldError(field);
      return trim(text);
    };
    const fields = EDITABLE_FIELDS.map(field => {
      const value = record[field];
      if (field === 'meaning' && requireBilingual) {
        if (typeof value !== 'string' || !trim(value)) fail(400, BILINGUAL_MEANING_ERROR);
        const meaning = bilingualMeaning(fieldText(value, field, 6000));
        return [field, fieldText(meaning, field, 6000)];
      }
      if (!LIST_FIELDS.includes(field)) return [field, fieldText(value, field, 6000)];
      if (!Array.isArray(value) || !value.length || value.length > 50) fieldError(field);
      return [field, [...new Set(value.map(item => fieldText(item, field, 200)))]];
    });
    const cleaned = Object.fromEntries(fields);
    if (!categories.includes(cleaned.category)) fieldError('category');
    return cleaned;
  }

  function readEdits(raw, defaults, categories) {
    const seedMaxId = defaults.at(-1)?.id || 0;
    const records = new Map(defaults.map(term => [term.id, term]));
    let saved;
    try { saved = JSON.parse(raw); }
    catch { return { records, changes: {}, nextId: seedMaxId + 1, seedMaxId }; }
    const previousMaxId = validId(saved?.seedMaxId) ? saved.seedMaxId : LEGACY_SEED_MAX_ID;
    const edits = Object.entries(saved?.records || {}).flatMap(([key, record]) => {
      const id = Number(key);
      return validId(id) && String(id) === key && id < Number.MAX_SAFE_INTEGER ? [[id, record]] : [];
    });
    const validChanges = {};
    let nextId = edits.reduce((next, [id]) => Math.max(next, id + 1), seedMaxId + 1);
    for (const [id, record] of edits) {
      // Previously custom IDs may overlap terms appended to the bundled seed.
      const overlapsNewDefault = id > previousMaxId && records.has(id);
      if (record === null) {
        if (overlapsNewDefault) continue;
        records.delete(id);
        validChanges[id] = null;
      } else if (record && record.id === id) {
        try {
          const validated = validateRecord(record, categories, { requireBilingual: false });
          const savedId = overlapsNewDefault ? nextId++ : id;
          const term = { id: savedId, ...validated };
          if (typeof record.updated_at === 'string' && !UNSUPPORTED.test(record.updated_at)) term.updated_at = record.updated_at;
          records.set(savedId, term);
          validChanges[savedId] = term;
        } catch { continue; }
      }
    }
    return { records, changes: validChanges, nextId, seedMaxId };
  }

  function normalizeSearch(value, foldMap, foldPattern) {
    const normalized = value.normalize('NFKC');
    const folded = foldPattern ? normalized.split(foldPattern).map(part => Object.hasOwn(foldMap, part) ? foldMap[part] : part.toLowerCase()).join('')
      : normalized.toLowerCase();
    return folded.replace(/[-\u2010-\u2015\u2212]+/g, ' ').replace(SPACE, ' ').trim();
  }

  function searchExpressions(term, normalize) {
    const splitter = /\s+\/\s+|[／|]|(?<=[\u3400-\u9fff])\s*\/\s*|\s*\/\s*(?=[\u3400-\u9fff])/u;
    const values = [...EXPRESSIONS.map(field => term[field]), ...term.aliases];
    return [...new Set(values.flatMap(value => [value, ...value.split(splitter)]).map(normalize).filter(Boolean))];
  }

  function addPostings(postings, value, index) {
    let previous = '';
    for (const character of value) {
      if (!postings.has(character)) postings.set(character, new Set());
      postings.get(character).add(index);
      if (previous) {
        const gram = previous + character;
        if (!postings.has(gram)) postings.set(gram, new Set());
        postings.get(gram).add(index);
      }
      previous = character;
    }
  }

  function isConcise(term, normalize) {
    return term.term_en.length > 0 && Array.from(term.term_en).length <= 32 && normalize(term.term_en).split(' ').length <= 4
      && Math.max(Array.from(term.term_hk).length, Array.from(term.term_cn).length) <= 13;
  }

  function caseGroup() {
    return { all: [], featured: [], concise: [], unfeatured: [] };
  }

  function addCase(group, entry) {
    group.all.push(entry);
    if (entry.concise) {
      group.concise.push(entry);
      group[entry.featured ? 'featured' : 'unfeatured'].push(entry);
    }
  }

  function createIndex(records, metadata) {
    const categoryGroups = new Map(metadata.categories.map(category => [category, caseGroup()]));
    const postings = new Map();
    const positions = new Map();
    const featuredTerms = new Set(metadata.featured_terms || []);
    const foldMap = metadata.casefold || {};
    const foldChars = Object.keys(foldMap).map(character => `\\u{${character.codePointAt(0).toString(16)}}`);
    const foldPattern = foldChars.length ? new RegExp(`([${foldChars.join('')}])`, 'gu') : null;
    const normalize = value => normalizeSearch(value, foldMap, foldPattern);
    const entries = [...records.values()].sort((left, right) => left.id - right.id).map((term, position) => {
      const expressions = searchExpressions(term, normalize);
      const meaning = normalize(term.meaning);
      const context = [...new Set(CONTEXT_FIELDS.map(field => normalize(term[field])))];
      const concise = isConcise(term, normalize);
      const featured = term.id <= 100 || featuredTerms.has(term.term_en);
      const entry = { term, expressions, meaning, context, concise, featured };
      for (const field of [...expressions, meaning, ...context]) addPostings(postings, field, position);
      addCase(categoryGroups.get(term.category), entry);
      positions.set(term.id, entry);
      return entry;
    });
    const counts = Object.fromEntries([...categoryGroups].map(([category, group]) => [category, group.all.length]));
    return { entries, categoryGroups, counts, positions, postings, normalize };
  }

  async function library() {
    const [seed, metadata] = await Promise.all([loadFile('glossary_seed'), loadFile('pages_library')]);
    const raw = storage('localStorage', EDITS_KEY);
    if (lastSnapshot && lastSnapshot.raw === raw) return lastSnapshot;
    const defaults = lastSnapshot?.defaults || [...seed].sort((left, right) => left.id - right.id);
    const overlay = readEdits(raw, defaults, metadata.categories);
    const index = createIndex(overlay.records, metadata);
    lastSnapshot = {
      ...overlay, raw, index, metadata, defaults, terms: index.entries.map(({ term }) => term),
      defaultPositions: lastSnapshot?.defaultPositions || new Map(defaults.map(term => [term.id, term])),
      defaultTimestamp: lastSnapshot?.defaultTimestamp || metadata.seed_updated_at || new Date().toISOString(),
    };
    return lastSnapshot;
  }

  function searchPattern(tokens) {
    const shortWord = /^[a-z0-9]{1,5}$/;
    const left = shortWord.test(tokens[0]) ? '(?<![a-z0-9])' : '';
    const right = shortWord.test(tokens.at(-1)) ? '(?![a-z0-9])' : '';
    const literal = tokens.join(' ').replace(/[.*+?^$(){}|[\]\\]/g, '\\$&');
    return new RegExp(left + literal + right);
  }

  function rank(entry, query, phrase, tokens) {
    const { expressions, meaning, context } = entry;
    if (expressions.includes(query)) return 0;
    if (expressions.some(value => value.search(phrase) === 0)) return 1;
    if (expressions.some(value => phrase.test(value))) return 2;
    const missing = tokens.filter(token => !expressions.some(value => token.test(value)));
    if (!missing.length) return 3;
    const remaining = missing.filter(token => !token.test(meaning));
    if (!remaining.length) return 4;
    return remaining.every(token => context.some(value => token.test(value))) ? 5 : -1;
  }

  function orderedMatches(index, raw, category) {
    const query = index.normalize(raw);
    if (!query) return raw ? [] : (category ? index.categoryGroups.get(category).all : index.entries);
    const tokens = query.split(' ');
    const grams = new Set();
    for (const token of tokens) {
      const chars = Array.from(token);
      if (chars.length === 1) grams.add(token);
      else for (let position = 1; position < chars.length; position++) grams.add(chars[position - 1] + chars[position]);
    }
    const postings = [...grams].map(gram => index.postings.get(gram));
    if (postings.some(group => !group)) return [];
    const [smallest, ...rest] = postings.sort((left, right) => left.size - right.size);
    const phrase = searchPattern(tokens);
    const tokenPatterns = tokens.length > 1 ? tokens.map(token => searchPattern([token])) : [phrase];
    const ranked = Array.from({ length: 6 }, () => []);
    for (const position of smallest) {
      const entry = index.entries[position];
      if ((category && entry.term.category !== category) || !rest.every(group => group.has(position))) continue;
      const priority = rank(entry, query, phrase, tokenPatterns);
      if (priority >= 0) ranked[priority].push(entry);
    }
    return ranked.flat();
  }

  function shuffle(items) {
    for (let index = items.length - 1; index > 0; index--) {
      const other = Math.floor(Math.random() * (index + 1));
      [items[index], items[other]] = [items[other], items[index]];
    }
    return items;
  }

  function pick(items, banned) {
    if (!items.length) return undefined;
    if (items.length > banned.size * 2) {
      for (let attempt = 0; attempt < 8; attempt++) {
        const entry = items[Math.floor(Math.random() * items.length)];
        if (!banned.has(entry.term.id)) return entry;
      }
    }
    const available = items.filter(entry => !banned.has(entry.term.id));
    return available[Math.floor(Math.random() * available.length)];
  }

  function drawFeed(groups, target, selected, counts, banned) {
    const available = new Map([...groups].filter(([, group]) => group.all.length));
    while (available.size && selected.length < target) {
      const names = shuffle([...available.keys()]).sort((left, right) => (counts.get(left) || 0) - (counts.get(right) || 0));
      for (const name of names.slice(0, target - selected.length)) {
        const group = available.get(name);
        const preferred = selected.length < Math.ceil(target / 2) ? group.featured : group.unfeatured;
        const entry = pick(preferred, banned) || pick(group.concise, banned) || pick(group.all, banned);
        if (!entry) { available.delete(name); continue; }
        selected.push(entry);
        counts.set(name, (counts.get(name) || 0) + 1);
        banned.add(entry.term.id);
      }
    }
  }

  function sampleFeed(index, category, limit, excluded) {
    const groups = category ? new Map([[category, index.categoryGroups.get(category)]]) : index.categoryGroups;
    const total = category ? index.counts[category] : index.entries.length;
    const selected = [];
    const counts = new Map();
    const target = Math.min(limit, total);
    drawFeed(groups, target, selected, counts, new Set(excluded));
    if (selected.length < target) {
      const repeat = new Map([...groups.keys()].map(name => [name, caseGroup()]));
      for (const id of new Set(excluded)) {
        const entry = index.positions.get(id);
        if (entry && repeat.has(entry.term.category)) addCase(repeat.get(entry.term.category), entry);
      }
      drawFeed(repeat, target, selected, counts, new Set());
    }
    return shuffle(selected);
  }

  function learningTip(snapshot, term) {
    const original = snapshot.defaultPositions.get(term.id);
    const fields = ['term_hk', 'term_cn', 'good_example_hk', 'good_example_cn'];
    if (original && fields.every(field => original[field] === term[field])) {
      const saved = snapshot.metadata.learning_tips?.[term.id];
      if (saved) return saved;
    }
    const [hk, cn] = [term.term_hk, term.term_cn].map(value => value.replace(SPACE, ' ').trim());
    if (hk === cn) return '两地写法相同。';
    const comparison = `港用「${hk}」，内地用「${cn}」。`;
    const short = `港「${hk}」／内地「${cn}」`;
    return [comparison, short].find(text => Array.from(text).length <= 22) || '两地常用说法，见上方对照。';
  }

  function copyTerm(term, timestamp) {
    const result = Object.fromEntries(TERM_FIELDS.map(field => [field, LIST_FIELDS.includes(field) ? [...term[field]] : term[field]]));
    if (timestamp) result.updated_at = term.updated_at || timestamp;
    return result;
  }

  function page(snapshot, { query = '', category = '', offset = 0, limit = 60, feed = false, excluded = [] } = {}) {
    const { index } = snapshot;
    const total = index.entries.length;
    const matches = feed ? sampleFeed(index, category, limit, excluded) : orderedMatches(index, query, category);
    const matched = feed ? (category ? index.counts[category] : total) : matches.length;
    const terms = (feed ? matches : matches.slice(offset, offset + limit)).map(({ term }) => ({
      ...copyTerm(term), learning_tip: learningTip(snapshot, term),
    }));
    return {
      terms, total, matched_total: matched, offset: feed ? 0 : offset, limit,
      has_more: !feed && offset + terms.length < matched, category_counts: { ...index.counts },
    };
  }

  function pageParams(params, categories) {
    const query = params.get('q') || '';
    const category = params.get('category') || '';
    if (Array.from(query).length > 500 || (category && !categories.includes(category))) fail(400, '请缩短搜索内容或选择有效的业务分类。');
    const mode = params.get('mode');
    if (mode !== null && mode !== 'feed') fail(400, '请选择有效的案例浏览方式。');
    const feed = !trim(query) && (mode === 'feed' || params.has('exclude') || (!params.has('offset') && !params.has('limit')));
    const number = (key, defaultValue, min) => {
      const value = params.get(key) ?? String(defaultValue);
      if (!/^\d{1,19}$/.test(value) || Number(value) < min) fail(400, '请选择有效的词库分页范围。');
      return Number(value);
    };
    const offset = number('offset', 0, 0);
    const limit = Math.min(number('limit', feed ? FEED_BATCH : trim(query) ? 12 : 60, 1), MAX_PAGE);
    const raw = feed ? params.get('exclude') || '' : '';
    const excluded = raw ? raw.split(',') : [];
    if (excluded.length > MAX_PAGE || excluded.some(value => !/^\d{1,19}$/.test(value) || BigInt(value) <= 0n || BigInt(value) >= 2n ** 63n)) fail(400, '请选择有效的案例编号。');
    return { query: trim(query), category, offset, limit, feed, excluded: excluded.map(Number) };
  }

  function sessionState(rotate = false) {
    if (rotate || !csrfToken) {
      csrfToken = Array.from(crypto.getRandomValues(new Uint8Array(32)), byte => byte.toString(16).padStart(2, '0')).join('');
    }
    return { is_admin: adminUntil > Date.now(), csrf_token: csrfToken };
  }

  function setAdmin(until) {
    adminUntil = until;
    try {
      if (until) window.sessionStorage.setItem(ADMIN_KEY, String(until));
      else window.sessionStorage.removeItem(ADMIN_KEY);
    } catch { /* A storage-restricted tab can still keep a session in memory. */ }
  }

  function bodyOf(options, error = '请提交完整的填写内容后重试。') {
    let value;
    try { value = JSON.parse(options.body); }
    catch { fail(400, error); }
    if (!value || typeof value !== 'object' || Array.isArray(value)) fail(400, error);
    return value;
  }

  function onlyKeys(object, keys) {
    return Object.keys(object).length === keys.length && keys.every(key => Object.hasOwn(object, key));
  }

  async function adminLogin(options) {
    setAdmin(0);
    const value = bodyOf(options, '请输入维护口令。');
    if (!onlyKeys(value, ['password'])) fail(400, '请输入维护口令。');
    const { password } = value;
    if (typeof password !== 'string' || !password || Array.from(password).length > 1024 || /\p{Cs}/u.test(password)) fail(400, '请输入有效的维护口令。');
    if (!crypto.subtle) fail(503, '请通过 HTTPS 或本机地址解锁维护模式。');
    const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', encoder.encode(password)));
    const hex = Array.from(digest, byte => byte.toString(16).padStart(2, '0')).join('');
    if (hex !== ADMIN_DIGEST) fail(401, '维护口令不正确。');
    setAdmin(Date.now() + ADMIN_DURATION);
    return sessionState(true);
  }

  function writeEdits(changes, seedMaxId) {
    try {
      if (changes === null) window.localStorage.removeItem(EDITS_KEY);
      else window.localStorage.setItem(EDITS_KEY, JSON.stringify({ seedMaxId, records: changes }));
    } catch { fail(503, STORAGE_ERROR); }
  }

  function mutate(path, method, id, options) {
    const change = async () => {
      options.signal?.throwIfAborted();
      if (adminUntil <= Date.now()) fail(403, '请先解锁维护模式后再修改词库。');
      const snapshot = await library();
      options.signal?.throwIfAborted();
      if (path === '/api/library/reset') {
        const body = bodyOf(options);
        if (!onlyKeys(body, ['confirm']) || body.confirm !== true) fail(400, '请确认恢复默认词库后再继续。');
        writeEdits(null);
        return page(await library());
      }
      const term = id ? snapshot.records.get(id) : null;
      if (id && !term) fail(404, MISSING);
      if (method === 'DELETE') {
        writeEdits({ ...snapshot.changes, [id]: null }, snapshot.seedMaxId);
        return { id };
      }
      const body = bodyOf(options);
      if (!Object.keys(body).length || Object.keys(body).some(field => !EDITABLE_FIELDS.includes(field))) {
        fail(400, '请填写完整的三语表达、分类、例句和用词贴士，并检查别名与适用平台。');
      }
      const editedId = id || snapshot.nextId;
      const record = { id: editedId, ...validateRecord({ ...term, ...body }, snapshot.metadata.categories), updated_at: new Date().toISOString() };
      writeEdits({ ...snapshot.changes, [editedId]: record }, snapshot.seedMaxId);
      return copyTerm(record, record.updated_at);
    };
    return window.navigator?.locks ? window.navigator.locks.request(EDITS_KEY, change) : change();
  }

  function csvCell(value) {
    const text = Array.isArray(value) ? `[${value.map(item => JSON.stringify(item)).join(', ')}]` : String(value);
    const safe = /^[=+\-@]/u.test(trim(text)) || /^[\t\r]/u.test(text) ? `'${text}` : text;
    return /[",\r\n]/u.test(safe) ? `"${safe.replaceAll('"', '""')}"` : safe;
  }

  function tbxEntry(term) {
    const escape = value => String(value).replace(/[&<>]/gu, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[char]);
    const languages = [['en', 'en'], ['zh-Hant-HK', 'hk'], ['zh-Hans-CN', 'cn']];
    return `    <termEntry id="brandlex-${term.id}">\n`
      + `      <descrip type="subjectField">${escape(term.category)}</descrip>\n`
      + `      <descrip type="definition">${escape(term.meaning)}</descrip>\n`
      + `      <note>${escape(term.usage_tip)}</note>\n`
      + `      <note>Avoid: ${escape(term.bad_example)}</note>\n`
      + `      <note>Search aliases: ${escape(term.aliases.join(', '))}</note>\n`
      + `      <note>Platforms: ${escape(term.platforms.join(', '))}</note>\n`
      + languages.map(([tag, key]) => `      <langSet xml:lang="${tag}"><tig><term>${escape(term[`term_${key}`])}</term><descrip type="context">${escape(term[`good_example_${key}`])}</descrip></tig></langSet>\n`).join('')
      + '    </termEntry>\n';
  }

  function exportLibrary(snapshot, format) {
    const terms = snapshot.index.entries.map(({ term }) => copyTerm(term, snapshot.defaultTimestamp));
    let parts, type;
    if (format === 'csv') {
      const fields = [...TERM_FIELDS, 'updated_at'];
      const rows = terms.map(term => fields.map(field => csvCell(term[field])).join(',') + '\r\n');
      parts = ['\ufeff', fields.join(',') + '\r\n', ...rows];
      type = 'text/csv;charset=utf-8';
    } else if (format === 'tbx') {
      if (!terms.length) fail(400, '请先添加至少一条词条，再导出词库。');
      parts = [
        '<?xml version="1.0" encoding="UTF-8"?>\n<martif type="TBX-Basic" xml:lang="en">\n',
        '  <martifHeader><fileDesc><titleStmt><title>BrandLex Marketing Library</title></titleStmt><sourceDesc><p>BrandLex team library export.</p></sourceDesc></fileDesc>\n',
        '    <encodingDesc><p type="XCSURI">https://ethan-conso.github.io/brandlex/data/brandlex_tbx.xcs</p></encodingDesc>\n  </martifHeader>\n  <text><body>\n',
        ...terms.map(tbxEntry), '  </body></text>\n</martif>\n',
      ];
      type = 'application/xml;charset=utf-8';
    } else if (format === 'json') {
      parts = [JSON.stringify(terms, null, 2) + '\n'];
      type = 'application/json';
    } else fail(400, '请选择 Excel CSV、TBX 或 JSON 导出格式。');
    return { blob: new Blob(parts, { type }), filename: `BrandLex-Library.${format}` };
  }

  const CHECK_ACTIONS = {
    hk: [/立即(?:入手|選購|購買|登記|預訂|報名)|按(?:此|連結)(?:選購|購買|登記|了解)|私訊(?:我們|查詢)|了解更多|即刻(?:選購|登記)/giu, /[點点][擊击]這[裡里]|[點点]此|歡迎[選选][購购]|快[來来]看看|不容錯過/giu, ['按連結選購，查看產品詳情。', '私訊我們，了解適合你的選擇。', '立即登記，接收最新活動消息。']],
    cn: [/立即(?:购买|选购|下单|报名|预约|预订)|点击(?:链接|这里)[，,\s]*(?:购买|下单|报名|了解|查看)|私信(?:我们|咨询)|了解更多|马上(?:购买|下单)/giu, /点这里|点此|欢迎选购|快来看看|不容错过/giu, ['点击链接，查看产品详情并选购。', '私信我们，了解适合你的选择。', '立即报名，获取最新活动消息。']],
    en: [/\b(?:shop now|shop via the link|buy now|order now|sign up|register now|book now|pre-order now|discover more|learn more|get started|subscribe now|reserve your (?:place|spot)|send us a message)\b/giu, /\b(?:click here|check it out|welcome to buy|don't miss out)\b/giu, ['Shop now and find your favourite.', 'Discover more via the link.', 'Send us a message to find out more.']],
  };
  const CHINESE = /[\u3400-\u9fff]/gu;
  const WORDS = /[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*/g;

  function checkReplacements(text, rules, market) {
    let cursor = 0;
    const offsets = [];
    const characters = Array.from(text);
    characters.forEach((character, position) => {
      offsets[cursor] = position;
      cursor += character.length;
    });
    offsets[cursor] = characters.length;
    const matches = rules.filter(rule => rule.market === market).flatMap(rule => {
      const pattern = new RegExp(rule.pattern, 'giu');
      return [...text.matchAll(pattern)].filter(match => match[0] !== rule.replacement).map(match => {
        const start = offsets[match.index];
        const end = offsets[match.index + match[0].length];
        return { id: `${rule.id}-${start}-${end}`, start, end, original_span: match[0], suggested_replacement: rule.replacement, reason: rule.reason, category: rule.category };
      });
    }).sort((left, right) => left.start - right.start || right.end - left.end || left.id.localeCompare(right.id));
    let end = 0;
    return matches.filter(match => {
      if (match.start < end) return false;
      end = match.end;
      return true;
    });
  }

  function checkCta(text, market) {
    const [strong, weak, endings] = CHECK_ACTIONS[market];
    const content = text.replace(/https?:\/\/\S+|#[\p{L}\p{N}_]+/gu, '').trimEnd();
    const sections = [...content.matchAll(/[^.!?。！？\n]+/gu)].filter(match => /[A-Za-z0-9\u3400-\u9fff]/u.test(match[0]));
    const finalStart = sections.at(-1)?.index ?? content.length;
    const negative = /(?:don['’]t|(?:do|does|did|should|would|could|must|can|may|might|need)\s+not|(?:should|would|could|must|can|does|did)n['’]t|cannot|never|no need to|not ready to|(?:不要|请勿|請勿|勿|不必)(?:现在|現在|马上|馬上)?)\s*$/iu;
    const positive = pattern => [...content.matchAll(pattern)].filter(match => !negative.test(content.slice(Math.max(0, match.index - 40), match.index)));
    const actions = positive(strong);
    if (actions.some(match => match.index >= finalStart)) return { cta_strength: 'strong', cta_suggestions: [] };
    const strength = actions.length || positive(weak).length ? 'weak' : 'missing';
    const reason = strength === 'missing' ? '结尾可加一句清楚的行动引导，请按实际购买或报名入口选用。' : '把明确的行动引导放到结尾，并确认入口可用。';
    const length = Array.from(text).length;
    return {
      cta_strength: strength,
      cta_suggestions: endings.map((ending, index) => ({
        id: `cta-${market}-${index + 1}`, start: length, end: length, original_span: '',
        suggested_replacement: (trim(text) ? '\n\n' : '') + ending, reason, category: '行动号召',
      })),
    };
  }

  function checkLanguage(text, market) {
    const chinese = (text.match(CHINESE) || []).length;
    if (market === 'en' && chinese >= 4) {
      const letters = (text.match(/[A-Za-z]/g) || []).length;
      return [['正文仍有中文，请先改写成自然英文；当前建议仅覆盖已识别的表达。'], chinese > letters ? 50 : 15];
    }
    const distinctive = {
      hk: '这为与发选购预订优运费肤亲温适湿润质实测联赠减满开关广务户号礼鸟场现',
      cn: '這為與發選購預訂優運費膚親溫適濕潤質實測聯贈減滿開關廣務戶號禮鳥場現',
    }[market];
    if (!distinctive || [...distinctive].filter(character => text.includes(character)).length < 2) return [[], 0];
    const message = market === 'hk' ? '正文仍有简体字，发往香港前请核对繁体写法和当地表达；当前建议未覆盖全文转换。'
      : '正文仍有繁体字，发往内地前请核对简体写法和平台语气；当前建议未覆盖全文转换。';
    return [[message], 10];
  }

  function checkCopy(text, market, terms, resources) {
    const { countDraft } = window.BrandLexHelpers;
    const counts = countDraft(text);
    const suggestions = checkReplacements(text, resources.rules, market);
    const cta = checkCta(text, market);
    const [warnings, languagePenalty] = checkLanguage(text, market);
    const long = text.split(/[.!?。！？\n]+/u).filter(sentence => {
      const words = (sentence.match(WORDS) || []).length;
      const chinese = (sentence.match(CHINESE) || []).length;
      return market === 'en' ? words > 30 : chinese + words > 55;
    }).length;
    const issues = new Set(suggestions.map(item => item.id.replace(/-\d+-\d+$/u, ''))).size;
    const penalty = Math.min(60, issues * 7) + { strong: 0, weak: 9, missing: 18 }[cta.cta_strength] + Math.min(12, long * 4) + languagePenalty;
    const score = counts.word_count ? Math.max(0, 100 - penalty) : 0;
    const matched = window.BrandLexStaticRewrite.matchTerms(text, terms, resources.dictionaries);
    return {
      target_market: market, score, readiness_score: score, suggestions, ...cta, counts, ...counts, warnings,
      readability: { label: long ? '建议拆短句' : '易于浏览', long_sentence_count: long, tips: long ? ['把长句拆成两句，优先展示一个卖点，再交代优惠或下一步。'] : [] },
      matched_glossary_terms: matched,
    };
  }

  function validGatewayReport(data, body) {
    const nonempty = value => typeof value === 'string' && value.trim().length > 0;
    return data?.engine === 'deepseek' && data.target_market === body.target_market && data.tone === body.tone
      && [data.primary_copy, data.alt_copy].every(nonempty)
      && Array.isArray(data.cta_options) && data.cta_options.length === 2 && data.cta_options.every(nonempty)
      && Array.isArray(data.adaptations) && data.adaptations.every(item => item
        && [item.original, item.adapted, item.reason].every(nonempty) && (item.term_id === null || validId(item.term_id)))
      && Array.isArray(data.matched_glossary_terms) && data.matched_glossary_terms.every(term => term && validId(term.id)
        && EDITABLE_FIELDS.every(field => LIST_FIELDS.includes(field)
          ? Array.isArray(term[field]) && term[field].every(nonempty) : nonempty(term[field])));
  }

  async function requestPublicRewrite(body, signal) {
    if (Array.from(body.text).length > MAX_RELAY_DRAFT) fail(413, '在线改写支持 4,000 字以内的原稿。');
    const timeout = AbortSignal.timeout(90_000);
    const response = await fetch(rewriteGateway, {
      method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(body), signal: signal ? AbortSignal.any([signal, timeout]) : timeout,
      credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer', cache: 'no-store',
    });
    if (!response.ok) fail(response.status, '在线改写未完成。');
    const { success, data } = await response.json();
    if (success && data?.error_code === 'factual_mismatch') {
      fail(422, '改写结果的价格、日期或数量与原稿不一致。当前仅提供本地预览。');
    }
    if (!success || !validGatewayReport(data, body)) {
      fail(502, '在线改写未返回完整结果。');
    }
    return { ...data, engine_source: 'live' };
  }

  async function rewriteCopy(body, terms, resources, cache, signal) {
    const { text: draft, target_market: region, tone } = body;
    const rewriter = window.BrandLexStaticRewrite;
    const cached = rewriter.cacheResult(draft, region, tone, cache, terms);
    if (cached) return cached;

    const key = storage('sessionStorage', DEEPSEEK_KEY) || '';
    let notice = key ? 'DeepSeek 未返回完整结果，请核对密钥后重试。'
      : '当前为本地预览。可设置个人 DeepSeek API Key，启用全文改写和翻译。';
    if (!key && rewriteGateway) {
      try { return await requestPublicRewrite(body, signal); }
      catch (error) {
        signal?.throwIfAborted();
        notice = {
          400: '在线改写未接受此原稿，请检查或缩短文案。当前仅提供本地预览。',
          413: '在线改写支持 4,000 字以内的原稿。当前仅提供本地预览。',
          422: error.message,
          429: '在线改写请求较多，请稍后重试。当前仅提供本地预览。',
        }[error.status] || '在线改写暂不可用，请稍后重试。当前仅提供本地预览。';
      }
    }

    const report = await rewriter.rewrite({ draft, region, tone }, { ...resources, terms, key, signal });
    return report.engine === 'local' && report.error_code !== 'factual_mismatch'
      ? { ...report, notice: [notice, report.notice].filter(Boolean).join(' ') } : report;
  }

  async function copyOperation(path, options) {
    const isRewrite = path === '/api/rewrite';
    const body = bodyOf(options);
    const keys = isRewrite ? ['text', 'target_market', 'tone'] : ['text', 'target_market'];
    const { text, target_market: region, tone } = body;
    if (!onlyKeys(body, keys) || typeof text !== 'string' || (isRewrite && !trim(text))) {
      fail(400, isRewrite ? '请输入原稿并选择市场和风格。' : '请填写文案并选择目标市场。');
    }
    if (!MARKETS.includes(region)) fail(400, '请选择香港、内地或英语市场。');
    if (isRewrite && !TONES.includes(tone)) fail(400, '请选择品牌标准、社媒种草或精炼转化。');
    if (Array.from(text).length > MAX_DRAFT) fail(400, '文案太长，请缩短至 20,000 字以内后重试。');
    if (/\p{Cs}/u.test(text)) fail(400, '文案含有无法识别的字符，请重新粘贴后重试。');
    const [snapshot, resources, cache] = await Promise.all([
      library(), loadFile('pages_rewrite_resources'), isRewrite ? loadFile('pages_rewrites', true) : null,
    ]);
    options.signal?.throwIfAborted();
    const { terms } = snapshot;
    const report = isRewrite
      ? await rewriteCopy(body, terms, resources, cache, options.signal)
      : checkCopy(text, region, terms, resources);
    return {
      ...report,
      matched_glossary_terms: report.matched_glossary_terms.map(term => copyTerm(term, snapshot.defaultTimestamp)),
    };
  }

  async function request(path, options = {}) {
    options.signal?.throwIfAborted();
    const url = new URL(path, document.baseURI);
    const route = url.pathname;
    const method = (options.method || 'GET').toUpperCase();
    const match = route.match(/^\/api\/terms\/(\d+)$/u);
    const id = match ? Number(match[1]) : null;
    if (match && !validId(id)) fail(404, MISSING);
    if (typeof options.body === 'string' && encoder.encode(options.body).length > MAX_REQUEST) fail(413, '内容太长，请缩短后重试。');
    if (['POST', 'PATCH', 'DELETE'].includes(method)) {
      const header = new Headers(options.headers).get('X-CSRF-Token');
      if (!csrfToken || header !== csrfToken) fail(403, '页面连接已更新，请刷新页面后重试。');
    }
    const success = data => ({ success: true, data });
    if (method === 'GET') {
      if (route === '/api/bootstrap') {
        const [snapshot, samples] = await Promise.all([library(), loadFile('sample_drafts')]);
        options.signal?.throwIfAborted();
        return success({ ...page(snapshot, { feed: true, limit: FEED_BATCH }), categories: [...snapshot.metadata.categories], samples: structuredClone(samples), ...sessionState() });
      }
      if (route === '/api/terms' || id || route.startsWith('/api/export/')) {
        const snapshot = await library();
        options.signal?.throwIfAborted();
        if (route === '/api/terms') return success(page(snapshot, pageParams(url.searchParams, snapshot.metadata.categories)));
        if (route.startsWith('/api/export/')) return exportLibrary(snapshot, route.slice('/api/export/'.length));
        const term = snapshot.records.get(id);
        if (!term) fail(404, MISSING);
        return success(copyTerm(term, snapshot.defaultTimestamp));
      }
    } else if (method === 'POST') {
      if (route === '/api/admin/login') return success(await adminLogin(options));
      if (route === '/api/admin/logout') {
        if (!onlyKeys(bodyOf(options), [])) fail(400, '请刷新页面后退出维护模式。');
        setAdmin(0);
        return success(sessionState(true));
      }
      if (route === '/api/rewrite' || route === '/api/check') return success(await copyOperation(route, options));
      if (route === '/api/terms' || route === '/api/library/reset') return success(await mutate(route, method, id, options));
    } else if (id && (method === 'PATCH' || method === 'DELETE')) return success(await mutate(route, method, id, options));
    if (id || ['/api/bootstrap', '/api/terms', '/api/admin/login', '/api/admin/logout', '/api/library/reset', '/api/rewrite', '/api/check'].includes(route)) {
      fail(405, '暂时无法完成此操作，请刷新页面后重试。');
    }
    fail(404, MISSING);
  }

  window.BrandLexStaticEngine = Object.freeze({ request, hasPublicRewrite: Boolean(rewriteGateway) });
})();
