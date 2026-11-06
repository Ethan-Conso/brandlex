/* Pure text helpers shared by the browser and Node's built-in test runner. */
(function (root) {
  'use strict';
  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
  }
  function parseList(value) {
    return [...new Set(String(value).split(/[,，、\n]/).map(item => item.trim()).filter(Boolean))];
  }
  function countDraft(text) {
    const chinese = (text.match(/[\u3400-\u9fff]/g) || []).length;
    const english = (text.match(/[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*/g) || []).length;
    return {
      character_count: Array.from(text).filter(character => !/\s/u.test(character)).length,
      word_count: chinese + english,
      paragraph_count: text.trim().split(/\n\s*\n/).filter(part => part.trim()).length,
      reading_time_seconds: Math.ceil(chinese * 60 / 400 + english * 60 / 220),
    };
  }
  function applyReplacement(text, suggestion) {
    const points = Array.from(text);
    const { start, end, original_span: original, suggested_replacement: replacement } = suggestion;
    if (!Number.isInteger(start) || !Number.isInteger(end) || start < 0 || end < start || end > points.length || typeof original !== 'string' || typeof replacement !== 'string' || points.slice(start, end).join('') !== original) {
      throw new Error('文案已更新，请重新检查后再应用建议。');
    }
    return points.slice(0, start).join('') + replacement + points.slice(end).join('');
  }
  function appendCta(text, cta) {
    const copy = String(text || '').trimEnd();
    const ending = String(cta || '').trim();
    if (!ending || copy.endsWith(ending)) return copy;
    return copy ? `${copy}\n\n${ending}` : ending;
  }
  function resultText(report, version) {
    if (!report) return '';
    return String((version === 'alt' ? report.alt_copy : report.primary_copy) || '');
  }
  function isOfferCondition(text) {
    const detail = text.replace(/^[\s，、：:;,；—]+/u, '');
    return /^(?:(?:实际|實際|本活动|本活動|本优惠|本優惠|優惠|优惠)\s*)?(?:仅限|僅限|只限|限于|限於|限领|限領|限今日|不?[适適]用(?!的)|每人|每单|每單|有效期|凭|憑)/u.test(detail)
      || /(?:限定|除外|另计|另計)[。.!！]?$/u.test(detail)
      || /^(?:offer\b|only\b|valid\b|available\b|terms apply\b|while stocks last\b|excludes?\b)/i.test(detail);
  }
  function cleanCaseDraft(value) {
    const text = String(value ?? '').trim();
    // Seeded examples mark a complete quotation before any editorial commentary.
    const quote = { '『': '』', '「': '」', '“': '”', '"': '"' }[text[0]];
    const end = quote ? text.indexOf(quote, 1) : -1;
    if (end > 1) {
      const draft = text.slice(1, end).trim();
      const tail = text.slice(end + 1).trim();
      if (!tail) return draft;
      if (isOfferCondition(tail)) return text;
      if (tail.startsWith('——') || /[。！？.!?]$/.test(draft)) return draft;
    }
    const note = text.match(/^([\s\S]*?[。！？.!?])\s*(?:——\s*([\s\S]*)|（([^（）]*)）|\(([^()]*)\))$/u);
    return note && !isOfferCondition(note[2] ?? note[3] ?? note[4]) ? note[1] : text;
  }
  const helpers = Object.freeze({ escapeHtml, parseList, countDraft, applyReplacement, appendCta, resultText, cleanCaseDraft });
  if (typeof module !== 'undefined' && module.exports) module.exports = helpers;
  else root.BrandLexHelpers = helpers;
})(typeof window === 'undefined' ? globalThis : window);
