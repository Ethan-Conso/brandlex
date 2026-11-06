const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { applyReplacement, countDraft, parseList, escapeHtml } = require('../static/js/helpers.js');

test('replaces only the selected occurrence with Unicode code point offsets', () => {
  const draft = '🎁 包邮，再次包邮';
  assert.equal(applyReplacement(draft, { start: 7, end: 9, original_span: '包邮', suggested_replacement: '免運費' }), '🎁 包邮，再次免運費');
  assert.throws(() => applyReplacement('草稿已改', { start: 0, end: 2, original_span: '包邮', suggested_replacement: '免運費' }));
});

test('CTA insertions append safely and invalid offsets are refused', () => {
  assert.equal(applyReplacement('Hello', { start: 5, end: 5, original_span: '', suggested_replacement: '\nShop now.' }), 'Hello\nShop now.');
  assert.throws(() => applyReplacement('Hello', { start: -1, end: 2, original_span: '', suggested_replacement: 'x' }));
});

test('counts mixed Chinese and English drafts like the backend', () => {
  assert.deepEqual(countDraft('好物推荐\n\nShop now.'), { character_count: 12, word_count: 6, paragraph_count: 2, reading_time_seconds: 2 });
  assert.equal(countDraft('  ').word_count, 0);
});

test('parses distinct comma-separated array fields and escapes untrusted text', () => {
  assert.deepEqual(parseList(' IG, 小红书，IG、EDM '), ['IG', '小红书', 'EDM']);
  assert.equal(escapeHtml('<img onerror="x"> & \'hello\''), '&lt;img onerror=&quot;x&quot;&gt; &amp; &#39;hello&#39;');
});

test('CTA append preserves copy paragraphs and avoids duplicate endings', () => {
  const { appendCta } = require('../static/js/helpers.js');
  assert.equal(appendCta('A thoughtful gift.  ', 'Explore the collection.'), 'A thoughtful gift.\n\nExplore the collection.');
  assert.equal(appendCta('A thoughtful gift.\n\nExplore the collection.', 'Explore the collection.'), 'A thoughtful gift.\n\nExplore the collection.');
  assert.equal(appendCta('', '  Shop now.  '), 'Shop now.');
});

test('selects a known result version without exposing arbitrary object fields', () => {
  const { resultText } = require('../static/js/helpers.js');
  const report = { primary_copy: 'Recommended', alt_copy: 'Shorter', notice: 'Internal' };
  assert.equal(resultText(report, 'primary'), 'Recommended');
  assert.equal(resultText(report, 'alt'), 'Shorter');
  assert.equal(resultText(report, 'notice'), 'Recommended');
  assert.equal(resultText(null, 'primary'), '');
});

test('loads case copy without editorial annotations and keeps offer details intact', () => {
  const { cleanCaseDraft } = require('../static/js/helpers.js');
  assert.equal(cleanCaseDraft('『亲，这支精华必须种草！』——直接搬到香港会显得突兀。'), '亲，这支精华必须种草！');
  assert.equal(cleanCaseDraft('『欢迎来到我们的弹出商店。』把 pop-up 当成电脑弹窗直译。'), '欢迎来到我们的弹出商店。');
  assert.equal(cleanCaseDraft('「好易用，自己試吓。」代替具體步驟。'), '好易用，自己試吓。');
  assert.equal(cleanCaseDraft('香港全場包郵，詳情結帳時才公布。（地区用词不贴切，条件出现太迟）'), '香港全場包郵，詳情結帳時才公布。');
  assert.equal(cleanCaseDraft('欢迎接收我们的新闻信。——机械照搬 newsletter 的字面意思。'), '欢迎接收我们的新闻信。');
  assert.equal(cleanCaseDraft('「玫瑰礼盒」现在 HK$280（会员专享）。'), '「玫瑰礼盒」现在 HK$280（会员专享）。');
  assert.equal(cleanCaseDraft('欢迎来取货 (周末除外)'), '欢迎来取货 (周末除外)');
  assert.equal(cleanCaseDraft('全部免费——仅限首单'), '全部免费——仅限首单');
  assert.equal(cleanCaseDraft('『免费试用！』仅限香港地区。'), '『免费试用！』仅限香港地区。');
  assert.equal(cleanCaseDraft('免費送貨。（港島地區限定）'), '免費送貨。（港島地區限定）');
  assert.equal(cleanCaseDraft('到店即送。——每人限领一份。'), '到店即送。——每人限领一份。');
  assert.equal(cleanCaseDraft('“Shop now!” Offer valid in Hong Kong only.'), '“Shop now!” Offer valid in Hong Kong only.');
  assert.equal(cleanCaseDraft('「动力储备等于电池寿命。」——适用的驱动形式不同。'), '动力储备等于电池寿命。');
});

test('all shipped HTML, CSS and JavaScript are free of emoji code points', () => {
  const root = path.resolve(__dirname, '..');
  const filesIn = directory => fs.readdirSync(directory, {withFileTypes: true}).flatMap(entry => {
    const file = path.join(directory, entry.name);
    return entry.isDirectory() ? filesIn(file) : [file];
  });
  const assets = [...filesIn(path.join(root, 'templates')), ...filesIn(path.join(root, 'static'))]
    .filter(file => /\.(?:html|css|js)$/.test(file));
  for (const file of assets) {
    assert.doesNotMatch(fs.readFileSync(file, 'utf8'), /\p{Extended_Pictographic}|[\u{1F1E6}-\u{1F1FF}]|[\uFE0F\u200D\u20E3]/u, path.relative(root, file));
  }
});
