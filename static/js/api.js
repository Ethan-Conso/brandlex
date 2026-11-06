/* Select the Flask API or the browser adapter before the first write. */
(() => {
  'use strict';
  const keyName = 'brandlex_deepseek_key';
  const requestError = '请求暂未完成，请稍后重试。';
  const forcedStatic = document.querySelector('meta[name="brandlex-mode"]')?.content === 'static' ||
    new URLSearchParams(location.search).get('mode') === 'static';
  let mode = forcedStatic ? 'static' : null;

  async function flaskRequest(path, options) {
    let response;
    try {
      response = await fetch(path, { credentials: 'same-origin', ...options });
    } catch (error) {
      if (error.name === 'AbortError') throw error;
      throw Object.assign(new Error(requestError), { unavailable: true });
    }
    const type = response.headers.get('Content-Type') || '';
    if (response.ok && path.startsWith('/api/export/') && response.headers.has('Content-Disposition')) {
      return { blob: await response.blob(), filename: `BrandLex-glossary.${path.split('/').pop()}` };
    }
    if (type.includes('application/json')) {
      const payload = await response.json().catch(error => {
        if (error.name === 'AbortError') throw error;
        return null;
      });
      if (response.ok && payload?.success === true) return payload;
      if (payload?.success === false) {
        throw Object.assign(new Error(payload.error || requestError), {
          status: response.status,
          unavailable: [404, 405, 500, 502, 503, 504].includes(response.status),
        });
      }
    }
    throw Object.assign(new Error(requestError), { unavailable: true });
  }

  async function request(path, options = {}) {
    if (mode === 'static') return window.BrandLexStaticEngine.request(path, options);
    if (mode === 'flask' || path !== '/api/bootstrap') return flaskRequest(path, options);
    try {
      const result = await flaskRequest(path, options);
      mode = 'flask';
      return result;
    } catch (error) {
      if (!error.unavailable) throw error;
      mode = 'static';
      return window.BrandLexStaticEngine.request(path, options);
    }
  }

  function getDeepSeekKey() {
    try { return sessionStorage.getItem(keyName) || ''; }
    catch { return ''; }
  }

  function setDeepSeekKey(value) {
    const key = value.trim();
    if (key && !/^[\x21-\x7e]{1,300}$/.test(key)) throw new Error('请输入有效的 DeepSeek API Key。');
    try {
      if (key) sessionStorage.setItem(keyName, key);
      else sessionStorage.removeItem(keyName);
    } catch { throw new Error('浏览器无法保存会话设置。'); }
  }

  async function downloadExport(format) {
    const { blob, filename } = await request(`/api/export/${format}`);
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
  }

  function engineLabel(report) {
    if (report.engine === 'deepseek') return report.engine_source === 'cache' ? 'DeepSeek · 缓存' : 'DeepSeek';
    return report.engine === 'local' ? '本地词库改写' : '本地预览';
  }

  window.BrandLexAPI = Object.freeze({ request, isStatic: () => mode === 'static', getDeepSeekKey, setDeepSeekKey, downloadExport, engineLabel });
})();
