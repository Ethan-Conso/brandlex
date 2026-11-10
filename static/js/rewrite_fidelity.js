/* Deterministic marketing fact checks shared by browser rewrite paths. */
(function (root) {
  'use strict';

  const URL = /https?:\/\/[^\s<>"`“”‘’「」『』，。；！？、：）】》]+/gi;
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
  const FIRST_GUESTS = pattern(`(?:首|前)\\s*(?<han>${FACT_NUMBER})\\s*(?:位|名|人)|\\bfirst\\s+(?<en>${FACT_NUMBER})\\s+(?:guests?|visitors?|customers?|shoppers?|people|attendees?|to\\s+arrive)\\b`);
  const QUANTITY_LABELS = {
    bottle: '瓶 bottle bottles', box: '盒 box boxes', cup: '杯 cup cups', piece: '件 piece pieces item items',
    set: '套 set sets', person: '位 名 人 guest guests visitor visitors customer customers person people shopper shoppers attendee attendees',
    portion: '份 portion portions serving servings', unit: '台 臺 unit units', strip: '條 条 strip strips',
    sheet: '張 张 sheet sheets', pair: '雙 双 pair pairs', occurrence: '次 time times', pack: '包 pack packs',
    minute: '分鐘 分钟 minute minutes', hour: '小時 小时 hour hours',
    ml: '毫升 ml milliliter milliliters millilitre millilitres', l: '升 l liter liters litre litres',
    cm: '厘米 釐米 公分 cm centimeter centimeters centimetre centimetres', mm: '毫米 mm millimeter millimeters millimetre millimetres',
    g: '克 g gram grams', kg: '公斤 千克 kg kilogram kilograms',
  };
  const QUANTITY_UNITS = Object.fromEntries(Object.entries(QUANTITY_LABELS).flatMap(([unit, labels]) =>
    labels.split(' ').map(label => [label, unit])));
  const HAN_UNIT = words(Object.fromEntries(Object.entries(QUANTITY_UNITS).filter(([label]) => !/^[a-z]/.test(label))))
    .replace('包', '包(?![郵邮])');
  const EN_UNIT = words(Object.fromEntries(Object.entries(QUANTITY_UNITS).filter(([label]) => /^[a-z]{2,}$/.test(label))));
  const MEASUREMENT_UNITS = new Set(['ml', 'l', 'cm', 'mm', 'g', 'kg']);
  const LIMIT_PREFIX = '(?:限量(?:供應|供应|發售|发售)?|(?:只|僅|仅)(?:有|限|得|剩|餘|余|售)|[僅仅]'
    + '|\\b(?:limited\\s+stock|stock\\s+limit)(?=\\s*:)|\\b(?:only|limited\\s+to|capped\\s+at|up\\s+to)\\s+)';
  const LIMIT_SUFFIX = '(?:\\s*(?:限量(?:供應|供应|發售|发售)?|[為为]限)|\\s+(?:only|available\\s+in\\s+total|in\\s+total)\\b)';
  const QUANTITY = pattern(`(?:(?<prefix>${LIMIT_PREFIX})\\s*:?)?\\s*(?<amount>${FACT_NUMBER})`
    + `(?:\\s*(?<hanUnit>${HAN_UNIT})|\\s*(?<symbol>ml|cm|mm|kg|l|g)(?![a-z0-9])`
    + `|(?:\\s+|\\s*-\\s*)(?:(?:gift|starter|sample|trial|travel|limited-edition)\\s+)?(?<enUnit>${EN_UNIT})(?![a-z0-9]))`
    + `(?<suffix>${LIMIT_SUFFIX})?`);
  const MEMBER_OFFER = new RegExp(String.raw`(?<!非)[會会][員员]|[會会]籍|(?<!non-)\bvips?\b|\bloyalty\s+cardholders?\b`
    + String.raw`|\b(?:with|through)\s+(?:(?:your|our|a|the)\s+)?membership\b`
    + String.raw`|\bmembership\s+(?:benefits?|discount|offer|perks?|price)\b`
    + String.raw`|(?<!non-)(?<!non )\bmembers?\b(?!\s+of\s+(?!(?:(?:our|the|a)\s+)?(?:loyalty|rewards)\b))`, 'u');
  const MEMBER_UNRESTRICTED = new RegExp(String.raw`非[會会][員员](?:也|亦|均|同[樣样])?(?:可|能|享|[領领])|(?:[無无]需|不需(?:要)?|毋須)(?:成[為为])?[會会][員员]`
    + String.raw`|\bnon[- ]?members?\s+(?:(?:can|may|also)\s+)?(?:save|get|enjoy|qualif(?:y|ies))\b`
    + String.raw`|\bno\s+membership\s+(?:is\s+)?(?:required|needed|necessary)\b|\bincluding\s+(?:all\s+)?(?:members|vips?)\b`, 'gu');
  const HONG_KONG = String.raw`(?:香港|(?<![a-z0-9])(?:hong\s+kong|hk)(?![a-z0-9$]))`;
  const HONG_KONG_WORD = new RegExp(HONG_KONG, 'u');
  const FREE_SHIPPING = /包[郵邮]|免[運运](?:[費费])?|免[郵邮][費费]|[運运][費费](?:全免|豁免)|\b(?:free|complimentary)\s+(?:(?:local|hong\s+kong|hk)\s+)?(?:shipping|delivery)\b|\b(?:shipping|delivery)\b[^.!?;，,]{0,50}\b(?:is\s+(?:free|on\s+us)|at\s+no\s+(?:extra\s+)?charge)\b|\bships?\s+free\b/u;
  const ORDER_ZH = '(?:[訂订][單单]|下[單单]|[購购][買买]|[銷销]售|接受|受理)';
  const ONLY_ZH = '(?:[僅仅只](?:限[於于]?|供|接受)|限[於于]|限定[於于]?|限制[於于]?)';
  const ORDER_SCOPE = new RegExp(String.raw`${ORDER_ZH}(?:地[區区]|[範范][圍围])?\s*${ONLY_ZH}\s*${HONG_KONG}`
    + String.raw`|${ONLY_ZH}\s*(?:${ORDER_ZH}\s*)?${HONG_KONG}\s*(?:地[區区]|[顧顾]客|用[戶户]|居民)?\s*${ORDER_ZH}`
    + String.raw`|\b(?:orders?|purchases?|checkout)\s+(?:(?:are|is|will\s+be)\s+)?(?:restricted|limited)\s+to\s+${HONG_KONG}`
    + String.raw`|\b(?:only\s+(?:accept|process|allow|take)|(?:accept|process|allow|take)\s+only)\s+(?:orders?\s+(?:from|in|within)\s+${HONG_KONG}|${HONG_KONG}\s+orders?)`
    + String.raw`|\bonly\s+${HONG_KONG}(?:-based)?\s+(?:customers?|shoppers?|residents?)\s+(?:can|may)\s+(?:order|purchase|buy)\b`
    + String.raw`|(?:只|僅|仅)(?:可|能)(?:在|於|于)\s*${HONG_KONG}(?:地[區区])?\s*${ORDER_ZH}`
    + String.raw`|\b(?:orders?|purchases?)\s+(?:can|may)\s+only\s+be\s+(?:placed|made)\s+(?:in|within|from)\s+${HONG_KONG}`
    + String.raw`|\b(?:order|buy|purchase)\s+only\s+(?:in|from|within)\s+${HONG_KONG}`
    + String.raw`|\bonly\s+(?:customers?|shoppers?|residents?)\s+(?:in|from|within)\s+${HONG_KONG}\s+(?:can|may)\s+(?:order|purchase|buy|place\s+orders?)\b`, 'u');
  const AMBIGUOUS_ORDER_SCOPE = new RegExp(String.raw`${ONLY_ZH}\s*${HONG_KONG}`
    + String.raw`|\b(?:only\s+${HONG_KONG}\s+orders?|${HONG_KONG}\s+orders?\s+only|orders?\s+(?:from|in|within)\s+${HONG_KONG}\s+only)\b`, 'u');
  const PRICE_CLAUSE = /[\n;。；!?！？、]|(?<![0-9])[.,，]|[.,，](?![0-9])|\b(?:and|while|whereas)\b/u;
  const PRICE_SENTENCE = /[\n;。；!?！？]|(?<![0-9])\.|\.(?![0-9])/u;
  const PRICE_LIST_JOIN = /\s*(?:\b(?:and|or)\b|[,，、及和與与])\s*/u;
  const PRICE_LIST_JOIN_EXACT = new RegExp(`^(?:${PRICE_LIST_JOIN.source})$`, 'u');
  const PAIRED_PRICES = /\brespectively\b|分[別别]/u;
  const PRICE_STOP_WORDS = new Set(('a an are at and as available buy choose cost costs discover each for from get is just now of on only our per price priced '
    + 'prices purchase retail shop the then to today was were while with you your hkd usd rmb cny').split(' '));
  const PRICE_HAN_STOP = new Set(['價格', '价格', '價錢', '价钱', '售價', '售价', '定價', '定价', '現售', '现售', '只需']);
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

  function urlDestination(text, { 0: span, index }) {
    const previous = text[index - 1];
    if (previous === '<' && text[index + span.length] === '>') return span;
    const raw = previous === "'" && span.endsWith("'") ? span.slice(0, -1) : span;
    let end = raw.length;
    const unbalanced = new Map();
    const opening = { ')': '(', ']': '[', '}': '{' };
    for (const char of raw) {
      if ('([{'.includes(char)) unbalanced.set(char, (unbalanced.get(char) || 0) + 1);
      else if (opening[char]) unbalanced.set(opening[char], (unbalanced.get(opening[char]) || 0) - 1);
    }
    while (end) {
      const tail = raw[end - 1];
      if ('.!,;:'.includes(tail)) end -= 1;
      else if (opening[tail] && unbalanced.get(opening[tail]) < 0) {
        unbalanced.set(opening[tail], unbalanced.get(opening[tail]) + 1);
        end -= 1;
      } else break;
    }
    return raw.slice(0, end);
  }

  function priceLabels(clause) {
    const labels = new Set((clause.match(/[a-z][a-z0-9]*/g) ?? []).filter(word => !PRICE_STOP_WORDS.has(word)));
    for (const run of clause.match(/[\u3400-\u9fff]+/gu) ?? []) {
      for (let index = 0; index < run.length - 1; index += 1) {
        const label = run.slice(index, index + 2);
        if (!PRICE_HAN_STOP.has(label)) labels.add(label);
      }
    }
    return labels;
  }

  function pairedPriceLabels(prose, ordered) {
    const first = ordered[0].start;
    const last = ordered.at(-1).end;
    if (!PAIRED_PRICES.test(prose.slice(Math.max(0, first - 40), first) + ' ' + prose.slice(last, last + 40))) return null;
    if (!ordered.slice(1).every(({ start }, index) => PRICE_LIST_JOIN_EXACT.test(prose.slice(ordered[index].end, start)))) return null;
    const clause = prose.slice(0, first).split(PRICE_SENTENCE).at(-1);
    const labels = clause.replace(PAIRED_PRICES, '').split(PRICE_LIST_JOIN).filter(label => label.trim());
    return labels.length === ordered.length ? labels.map(priceLabels) : [];
  }

  function clausePriceLabels(prose, ordered) {
    return ordered.map(({ start, end }, index) => {
      const before = prose.slice(ordered[index - 1]?.end ?? 0, start).split(PRICE_CLAUSE).at(-1).slice(-80);
      const next = ordered[index + 1];
      const after = prose.slice(end, next?.start ?? prose.length).split(PRICE_CLAUSE);
      const suffix = !next || after.length > 1 ? after[0].slice(0, 80) : '';
      return priceLabels(before + ' ' + suffix);
    });
  }

  function priceAssignments(prose, occurrences) {
    const ordered = occurrences.sort((a, b) => a.start - b.start);
    const prices = [...new Set(ordered.map(({ value }) => value))];
    const anchors = new Map();
    const paired = prices.length > 1 ? pairedPriceLabels(prose, ordered) : null;
    const labels = paired ?? clausePriceLabels(prose, ordered);
    for (const [index, tokens] of labels.entries()) {
      for (const token of tokens) {
        if (!anchors.has(token)) anchors.set(token, new Set());
        anchors.get(token).add(ordered[index].value);
      }
    }
    return { prices, anchors };
  }

  function conflictingPrices(expected, actual, required) {
    if (expected.prices.length < 2) return false;
    const confirmed = new Set();
    for (const [label, values] of expected.anchors) {
      const current = actual.anchors.get(label);
      if (values.size !== 1 || !current) continue;
      const [value] = values;
      if (current.size !== 1 || !current.has(value)) return true;
      confirmed.add(value);
    }
    // Unrecognized or fully translated labels cannot justify reordering prices.
    if (!required) {
      const current = new Set(actual.prices);
      for (const value of expected.prices) if (!current.has(value)) confirmed.add(value);
    }
    const unmatched = sequence => sequence.filter(value => !confirmed.has(value));
    return unmatched(expected.prices).join('|') !== unmatched(actual.prices).join('|');
  }

  function extractFacts(text) {
    const facts = new Set(Array.from(text.matchAll(URL), match => 'url:' + urlDestination(text, match)));
    let prose = text.replace(URL, ' ').normalize('NFKC').toLowerCase().replace(/[\u2010-\u2015\u2212]/g, '-')
      .replace(/\s+/g, match => match.includes('\n') ? '\n' : ' ');
    const memberProse = prose.replace(MEMBER_UNRESTRICTED, () => {
      facts.add('membership_unrestricted');
      return ' ';
    });
    if (MEMBER_OFFER.test(memberProse)) facts.add('membership');
    for (const clause of prose.split(/[\n.!?;。！？；]/u)) {
      const shipping = HONG_KONG_WORD.test(clause) && FREE_SHIPPING.test(clause);
      if (shipping) facts.add('shipping:hk');
      // Bare geographic restrictions may refer to free shipping in the same clause.
      if (ORDER_SCOPE.test(clause) || (!shipping && AMBIGUOUS_ORDER_SCOPE.test(clause))) facts.add('orders:hk');
    }
    const implied = new Set();
    const labelProse = prose;
    const prices = [];
    const fact = (...values) => values.join(':');
    const take = (expression, read, capturePrice = false) => {
      prose = prose.replace(expression, (...match) => {
        const span = match[0];
        const found = read(match.at(-1), span);
        if (!found) return span;
        for (const value of (Array.isArray(found) ? found : [found])) facts.add(value);
        const start = match.at(-3);
        if (capturePrice) prices.push({ value: found, start, end: start + span.length });
        return '\0'.repeat(span.length); // Keep clause offsets without joining text across facts.
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
    take(pattern(MONEY), (_, span) => fact('money', ...moneyAmount(span)), true);
    take(BARE_PRICE, ({ amount }) => fact('money', '', factNumber(amount)), true);
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
    take(QUANTITY, ({ prefix, amount, hanUnit, symbol, enUnit, suffix }) => {
      const count = factNumber(amount);
      const unit = QUANTITY_UNITS[hanUnit || symbol || enUnit];
      if (prefix || suffix) return [fact('quantity', unit, count), fact('limited_quantity', unit, count)];
      const explicit = count !== '1' || /^[0-9]/.test(amount) || MEASUREMENT_UNITS.has(unit);
      return fact(explicit ? 'quantity' : 'optional_quantity', unit, count);
    });
    for (const match of prose.matchAll(pattern(ARABIC_NUMBER))) facts.add(fact('number', factNumber(match[0])));
    return { facts, implied, prices: priceAssignments(labelProse, prices) };
  }

  function verifyFactualFidelity(source, primary, alternate, ctas) {
    const expected = extractFacts(source);
    const allowed = new Set([...expected.facts, ...expected.implied]);
    for (const value of expected.facts) {
      if (value.startsWith('optional_quantity:')) allowed.add(value.slice('optional_'.length));
    }
    for (const [index, text] of [primary, alternate, ...ctas].entries()) {
      const actual = extractFacts(text);
      for (const value of actual.facts) {
        if (!value.startsWith('optional_quantity:')) continue;
        actual.facts.delete(value);
        const quantity = value.slice('optional_'.length);
        if (allowed.has(quantity)) actual.facts.add(quantity);
      }
      const conflicts = [...actual.facts].some(value => !allowed.has(value));
      const missing = index < 2 && [...expected.facts].some(value =>
        !value.startsWith('number:') && !value.startsWith('optional_quantity:') && !actual.facts.has(value));
      if (conflicts || missing || conflictingPrices(expected.prices, actual.prices, index < 2)) {
        throw new Error(FACTUAL_MISMATCH);
      }
    }
  }

  const api = Object.freeze({ verifyFactualFidelity, FACTUAL_MISMATCH });
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.BrandLexRewriteFidelity = api;
})(typeof window === 'undefined' ? globalThis : window);
