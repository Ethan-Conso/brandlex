/* Deterministic numeric fact checks shared by browser rewrite paths. */
(function (root) {
  'use strict';

  const URL = /(https?:\/\/[^\s<>"，。！？；]+)/gi;
  const ARABIC_NUMBER = String.raw`(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?:\.[0-9]+)?`;
  const HAN_DIGITS = '零〇一二兩两三四五六七八九';
  const HAN_NUMBER = '[' + HAN_DIGITS + '廿十百千萬万]{1,16}(?:[點点][' + HAN_DIGITS + ']{1,8})?';
  const EN_DIGITS = Object.fromEntries('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'
    .split(' ').map((word, value) => [word, value]));
  'twenty thirty forty fifty sixty seventy eighty ninety'.split(' ').forEach((word, index) => { EN_DIGITS[word] = (index + 2) * 10; });
  const EN_ORDINALS = Object.fromEntries('first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth fifteenth sixteenth seventeenth eighteenth nineteenth twentieth'
    .split(' ').map((word, index) => [word, index + 1]));
  'thirtieth fortieth fiftieth sixtieth seventieth eightieth ninetieth'.split(' ').forEach((word, index) => { EN_ORDINALS[word] = (index + 3) * 10; });
  const EN_UNITS = { hundred: 100, thousand: 1000, million: 1000000 };
  const words = mapping => '(?:' + Object.keys(mapping).sort((a, b) => b.length - a.length).join('|') + ')';
  const CARDINAL = words({ ...EN_DIGITS, ...EN_UNITS });
  const EN_NUMBER = `(?<![a-z])${CARDINAL}(?:(?:[ -]+(?:and[ -]+)?)${CARDINAL}){0,7}(?![a-z])`;
  const EN_ORDINAL_DAY = `(?<![a-z])(?:${CARDINAL}[ -]+)?${words(EN_ORDINALS)}(?![a-z])`;
  const FACT_NUMBER = `(?:(?<![0-9])(?<![0-9]\\.)(?!(?<=[0-9],)[0-9]{3}(?![0-9]))${ARABIC_NUMBER}(?![0-9])|${HAN_NUMBER}|${EN_NUMBER})`;
  const ORDINAL_DAY = `(?:[0-9]{1,2}(?:st|nd|rd|th)|${EN_ORDINAL_DAY})`;
  const DAY_NUMBER = `(?:[0-9]{1,2}(?:st|nd|rd|th)?|${HAN_NUMBER}|${EN_ORDINAL_DAY}|${EN_NUMBER})`;
  const MONTH_NAMES = [
    'january jan', 'february feb', 'march mar', 'april apr', 'may', 'june jun', 'july jul', 'august aug',
    'september sept sep', 'october oct', 'november nov', 'december dec',
  ];
  const MONTH_NUMBERS = Object.fromEntries(MONTH_NAMES.flatMap((names, index) => names.split(' ').map(name => [name, index + 1])));
  const EN_MONTH = '(?<![a-z])(?:' + Object.keys(MONTH_NUMBERS).join('|') + ')(?![a-z])\\.?';
  const FULL_MONTH = '(?<![a-z])(?:' + MONTH_NAMES.filter(names => names !== 'may').flatMap(names => names === 'march mar' ? ['march'] : names.split(' ')).join('|') + ')(?![a-z])';
  const DATE_JOIN = '(?:[-~〜至到]|to\\b|through\\b|until\\b|and\\b)';
  const CURRENCY_LABELS = {
    hkd: 'hk$|hkd$|hkd|港幣|港币|港元|港圓|港圆|hong kong dollar|hong kong dollars',
    usd: 'us$|usd$|usd|$|美元|美金|us dollar|us dollars',
    cny: 'cn¥|rmb|cny|¥|人民幣|人民币|元|圓|圆|yuan|chinese yuan',
    eur: 'eur|€|歐元|欧元|euro|euros', gbp: 'gbp|£|英鎊|英镑|pound sterling|pounds sterling',
    sgd: 'sg$|sgd|新加坡元', twd: 'nt$|twd|新台幣|新台币', jpy: 'jp¥|jpy|日圓|日圆|日元',
  };
  const CURRENCY_CODES = Object.fromEntries(Object.entries(CURRENCY_LABELS).flatMap(([code, labels]) =>
    labels.split('|').map(label => [label, code])));
  const CURRENCY = '(?:' + Object.keys(CURRENCY_CODES).sort((a, b) => b.length - a.length).map(label => label.replace(/\$/g, '\\$')).join('|') + ')';
  const MONEY = `(?:(?<![a-z])(?<before>${CURRENCY})\\s*(?<amount>${FACT_NUMBER})(?:\\s*[元圓圆])?|(?<suffixAmount>${FACT_NUMBER})\\s*(?<after>${CURRENCY})(?![a-z]))`;
  const SPEND = `(?:${CURRENCY}\\s*)?${FACT_NUMBER}(?:\\s*${CURRENCY}(?![a-z]))?`;
  const pattern = source => new RegExp(source, 'gu');
  const YEAR = String.raw`(?:,?\s+(?<year>[0-9]{4})(?![0-9]))?`;
  const DATE_RANGES = [
    `(?:(?<year>[0-9]{4})\\s*年\\s*)?(?:(?<month>${FACT_NUMBER})\\s*月\\s*)?(?<start>${DAY_NUMBER})\\s*[日號号]?\\s*[-~〜至到]\\s*(?:(?<endMonth>${FACT_NUMBER})\\s*月\\s*)?(?<end>${DAY_NUMBER})\\s*[日號号]`,
    `(?<month>${EN_MONTH})\\s+(?<start>${DAY_NUMBER})\\s*${DATE_JOIN}\\s*(?:(?<endMonth>${EN_MONTH})\\s+)?(?<end>${DAY_NUMBER})(?![a-z0-9])${YEAR}`,
    `(?<![a-z0-9])(?<start>${DAY_NUMBER})\\s*${DATE_JOIN}\\s*(?<end>${DAY_NUMBER})\\s+(?<month>${EN_MONTH})${YEAR}`,
    `(?<![a-z0-9])(?<start>${DAY_NUMBER})\\s+(?<month>${EN_MONTH})\\s*${DATE_JOIN}\\s*(?<end>${DAY_NUMBER})\\s+(?<endMonth>${EN_MONTH})${YEAR}`,
    `\\b(?:from|between)\\s+(?:the\\s+)?(?<start>${ORDINAL_DAY})\\s*${DATE_JOIN}\\s*(?:the\\s+)?(?<end>${ORDINAL_DAY})(?![a-z0-9])`,
  ].map(pattern);
  const DATES = [
    `(?:(?<year>[0-9]{4})\\s*年\\s*)?(?<month>${FACT_NUMBER})\\s*月\\s*(?<day>${DAY_NUMBER})\\s*[日號号]`,
    String.raw`(?<![0-9])(?<year>[0-9]{4})[-/](?<month>[0-9]{1,2})[-/](?<day>[0-9]{1,2})(?![0-9])`,
    `(?<month>${EN_MONTH})\\s+(?:the\\s+)?(?<day>${DAY_NUMBER})(?![a-z0-9])${YEAR}`,
    `(?<![a-z0-9])(?<day>${DAY_NUMBER})\\s+(?<month>${EN_MONTH})${YEAR}`,
    `(?<day>${DAY_NUMBER})\\s*[日號号](?=\\s*(?:起|止|截止|推出|[發发]售|開售|开售|上[線线市]|[開开]放|[結结]束))`,
    `\\bon\\s+(?:the\\s+)?(?<day>${ORDINAL_DAY})(?![a-z0-9])`,
  ].map(pattern);
  const CLOCK = String.raw`(?:[0-9]{1,2}:[0-9]{2}(?:\s*[ap]\.?m\.?(?![a-z]))?|[0-9]{1,2}\s*[ap]\.?m\.?(?![a-z]))`;
  const CLOCK_BETWEEN = pattern(`\\bbetween\\s+(?<start>${CLOCK})\\s+and\\s+(?<end>${CLOCK})(?![0-9])`);
  const TIME = pattern(`(?<![0-9])(?<start>${CLOCK})(?:\\s*(?:[-~〜至到]|to\\b)\\s*(?<end>${CLOCK}))?(?![0-9])`);
  const THRESHOLDS = [
    ['at_least', `(?:滿|满|最低(?:消[費费]|金[額额])|至少(?:消[費费]|[購购][買买]))\\s*(?<amount>${SPEND})`],
    ['over', `(?:超[過过]\\s*|\\b(?:orders?\\s+)?(?:over|above|more\\s+than)\\s+)(?<amount>${SPEND})`],
    ['at_least', `\\b(?:orders?\\s+of\\s+|spend\\s+|free shipping\\s+at\\s+)?(?<amount>${SPEND})\\s+(?:or\\s+more|and\\s+(?:above|up)|or\\s+above)\\b`],
    ['at_least', `\\b(?:free shipping\\s+from|minimum spend(?:\\s+of)?|spend\\s+at\\s+least|orders?\\s+(?:of\\s+)?at\\s+least)\\s+(?<amount>${SPEND})`],
    ['at_least', `\\b(?:orders?(?:\\s+of)?|spend|free shipping(?:\\s+(?:at|from))?)\\s+(?<amount>${SPEND})\\s*\\+(?![0-9])`],
    ['at_least', `(?<amount>${SPEND})\\s*(?:或以上|及以上|以上)(?!的)`],
  ].map(([comparator, source]) => [comparator, pattern(source)]);
  const MONTH_ONLY = pattern(`(?<numeric>${FACT_NUMBER})\\s*月(?![份龄齡])|(?<name>${FULL_MONTH})|\\b(?:in|from|during|until|this|by)\\s+(?<short>${EN_MONTH})`);
  const BARE_PRICE = pattern(`(?:(?:[售定原特][價价])(?:為|为)?\\s*:?\\s*|\\bprice\\s*:\\s*|\\b(?:priced\\s+at|price\\s+(?:is|of)|costs?)\\s+)(?<amount>${FACT_NUMBER})`);
  const FOLD = pattern(`(?<amount>${FACT_NUMBER})\\s*折`);
  const OFF = pattern(`(?:(?:\\bsave\\s+|立[減减]|省)\\s*(?<before>${FACT_NUMBER})\\s*%|(?<after>${FACT_NUMBER})\\s*%\\s*(?:off\\b|折扣|[優优]惠))`);
  const PERCENT = pattern(`(?<amount>${FACT_NUMBER})\\s*%`);
  const DURATION = pattern(`(?<!同)(?<cue>[為为]期|[僅仅]限|限[時时]|持[續续]|呢|[這这]|\\b(?:for|only|lasts?)\\s+)?\\s*(?<amount>${FACT_NUMBER})\\s*(?<dash>-)?\\s*(?:days?\\b|[個个]?天|[個个]?日(?![期子]))(?<suffix>[以]?[內内]|\\s+only\\b)?`);
  const FIRST_GUESTS = pattern(`(?:首|前)\\s*(?<han>${FACT_NUMBER})\\s*(?:位|名|人)|\\bfirst\\s+(?<en>${FACT_NUMBER})\\s+(?:guests?|visitors?|customers?|shoppers?|people|attendees?)\\b`);
  const QUANTITY = pattern(`(?<han>${FACT_NUMBER})\\s*(?:瓶|盒|杯|件|套|位|名|人|份|台|條|条|張|张|雙|双|次|分鐘|分钟|小時|小时)|(?<en>${FACT_NUMBER})\\s+(?:bottles?|boxes?|cups?|pieces?|units?|sets?|guests?|visitors?|customers?|people|items?|packs?|pairs?|minutes?|hours?)\\b`);
  const FACTUAL_MISMATCH = 'Factual mismatch in DeepSeek rewrite';

  function factNumber(raw) {
    if (/^[0-9]/.test(raw)) {
      const [whole, fraction] = raw.replace(/,|(?:st|nd|rd|th)$/g, '').split('.');
      const digits = whole.replace(/^0+(?=\d)/, '');
      const decimals = fraction?.replace(/0+$/, '');
      return decimals ? digits + '.' + decimals : digits;
    }
    if (/^[a-z]/.test(raw)) {
      let total = 0;
      let current = 0;
      for (const word of raw.split(/[ -]+/)) {
        if (word === 'hundred') current = (current || 1) * 100;
        else if (word === 'thousand' || word === 'million') {
          total += (current || 1) * EN_UNITS[word];
          current = 0;
        } else if (word !== 'and') current += EN_DIGITS[word] ?? EN_ORDINALS[word];
      }
      return String(total + current);
    }
    const [whole, fraction] = raw.replace(/廿/g, '二十').split(/[點点]/);
    const digits = '0012223456789';
    const digit = char => digits[HAN_DIGITS.indexOf(char)];
    const powers = { 十: 10, 百: 100, 千: 1000, 萬: 10000, 万: 10000 };
    const decimals = fraction ? Array.from(fraction, digit).join('').replace(/0+$/, '') : '';
    if (!/[十百千萬万]/.test(whole)) {
      const number = Array.from(whole, digit).join('').replace(/^0+(?=\d)/, '');
      return decimals ? number + '.' + decimals : number;
    }
    let total = 0;
    let section = 0;
    let current = 0;
    for (const char of whole) {
      const unit = powers[char];
      if (unit === 10000) {
        total += (section + current || 1) * unit;
        section = current = 0;
      } else if (unit) {
        section += (current || 1) * unit;
        current = 0;
      } else {
        current = Number(digit(char));
      }
    }
    return String(total + section + current) + (decimals ? '.' + decimals : '');
  }

  function clockMinutes(text) {
    const match = text.match(/^([0-9]{1,2})(?::([0-9]{2}))?\s*(?:([ap])\.?m\.?)?$/);
    let hour = Number(match[1]);
    const minute = Number(match[2] || 0);
    if (match[3]) {
      if (hour < 1 || hour > 12) return null;
      hour = hour % 12 + (match[3] === 'p' ? 12 : 0);
    }
    return hour < 24 && minute < 60 ? hour * 60 + minute : null;
  }

  function moneyAmount(text) {
    const fields = new RegExp('^' + MONEY + '$', 'u').exec(text)?.groups;
    return fields ? [CURRENCY_CODES[fields.before || fields.after], factNumber(fields.amount || fields.suffixAmount)]
      : ['', factNumber(text)];
  }

  function monthNumber(raw) {
    return raw ? MONTH_NUMBERS[raw.replace(/\.$/, '')] ?? Number(factNumber(raw)) : 0;
  }

  function dateWindowLength(year, month, day, endMonth, endDay) {
    const first = new Date(Date.UTC(year, (month || 1) - 1, day));
    const last = new Date(Date.UTC(year + Number(endMonth < month), (endMonth || 1) - 1, endDay));
    if (first.getUTCDate() !== day || last.getUTCDate() !== endDay || last < first) return 0;
    return (last - first) / 86_400_000 + 1;
  }

  function extractFacts(text) {
    let prose = text.replace(URL, ' ').normalize('NFKC').toLowerCase().replace(/[\u2010-\u2015\u2212]/g, '-').replace(/\s+/g, ' ');
    const facts = new Set();
    const implied = new Set();
    const fact = (...values) => values.join(':');
    const take = (expression, read) => {
      prose = prose.replace(expression, (...match) => {
        const found = read(match.at(-1), match[0]);
        if (!found) return match[0];
        facts.add(found);
        return '\0'; // Do not join text across a recognized fact.
      });
    };
    const dates = ({ year, month, endMonth, start, end, day }) => {
      const y = Number(year || 0);
      const m = monthNumber(month);
      const d = Number(factNumber(start || day));
      if (!(m >= 0 && m <= 12 && d >= 1 && d <= 31)) return null;
      if (m) implied.add(fact('month', m));
      if (!end) return fact('date', y, m, d);
      const n = monthNumber(endMonth) || m;
      const e = Number(factNumber(end));
      if (!(n >= 0 && n <= 12 && e >= 1 && e <= 31)) return null;
      if (n) implied.add(fact('month', n));
      for (const rangeYear of (y ? [y] : [2000, 2001])) {
        const duration = dateWindowLength(rangeYear, m, d, n, e);
        if (duration) implied.add(fact('duration', duration));
      }
      return fact('date_range', y, m, d, n, e);
    };
    for (const expression of DATE_RANGES) take(expression, dates);
    for (const expression of DATES) take(expression, dates);
    take(MONTH_ONLY, ({ numeric, name, short }) => fact('month', monthNumber(numeric || name || short)));
    const clock = ({ start, end }) => {
      const from = clockMinutes(start);
      const to = end ? clockMinutes(end) : null;
      if (from === null || (end && to === null)) return null;
      if (!end) return fact('time', from);
      implied.add(fact('time', from));
      implied.add(fact('time', to));
      return fact('time_range', from, to);
    };
    take(CLOCK_BETWEEN, clock);
    take(TIME, clock);
    for (const [comparator, expression] of THRESHOLDS) take(expression, ({ amount }) => fact('threshold', comparator, ...moneyAmount(amount)));
    take(pattern(MONEY), (_, span) => fact('money', ...moneyAmount(span)));
    take(BARE_PRICE, ({ amount }) => fact('money', '', factNumber(amount)));
    take(FOLD, ({ amount }) => {
      const pay = Number(factNumber(amount));
      return fact('discount', Number((100 - pay * (pay <= 10 ? 10 : 1)).toFixed(8)));
    });
    take(OFF, ({ before, after }) => fact('discount', factNumber(before || after)));
    take(PERCENT, ({ amount }) => fact('percent', factNumber(amount)));
    take(DURATION, ({ amount, cue, dash, suffix }) => {
      const count = factNumber(amount);
      return count !== '1' || cue || dash || suffix || /^[0-9]/.test(amount) ? fact('duration', count) : null;
    });
    take(FIRST_GUESTS, ({ han, en }) => fact('first_guests', factNumber(han || en)));
    take(QUANTITY, ({ han, en }) => {
      const amount = han || en;
      const count = factNumber(amount);
      return count !== '1' || /^[0-9]/.test(amount) ? fact('number', count) : null;
    });
    for (const match of prose.matchAll(pattern(ARABIC_NUMBER))) facts.add(fact('number', factNumber(match[0])));
    return { facts, implied };
  }

  function verifyFactualFidelity(source, primary, alternate, ctas) {
    const expected = extractFacts(source);
    for (const [index, text] of [primary, alternate, ...ctas].entries()) {
      const actual = extractFacts(text);
      const conflicts = [...actual.facts].some(value => !expected.facts.has(value) && !expected.implied.has(value));
      const missing = index < 2 && [...expected.facts].some(value =>
        !value.startsWith('number:') && !actual.facts.has(value));
      if (conflicts || missing) throw new Error(FACTUAL_MISMATCH);
    }
  }

  const api = Object.freeze({ verifyFactualFidelity, FACTUAL_MISMATCH });
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.BrandLexRewriteFidelity = api;
})(typeof window === 'undefined' ? globalThis : window);
