/* Home-only visual interactions. No draft submission or workspace state. */
(function (root) {
  'use strict';
  const COLORS = Object.freeze(['#6366F1', '#94A3B8', '#0EA5E9']);
  const SURFACES = Object.freeze(['rewrite', 'glossary', 'export']);
  const MINI_COPIES = Object.freeze({
    hk: Object.freeze({
      standard: '跨界聯乘禮盒，讓香氣成為日常。',
      social: '週末好物推介：把城市香氣帶回家。',
      concise: '聯乘禮盒現已登場，立即預訂。',
    }),
    cn: Object.freeze({
      standard: '联名香氛礼盒上新，把城市灵感带回家。',
      social: '这份联名礼盒，藏着周末的小心动。',
      concise: '早鸟福利限时开放，立即预订。',
    }),
    en: Object.freeze({
      standard: 'City-inspired fragrance. Made to feel like you.',
      social: 'Your next little scent obsession starts here.',
      concise: 'Meet the gift set. Pre-order today.',
    }),
  });

  function createParticles(width, height, random = Math.random) {
    return Array.from({length: 45}, (_, index) => ({
      x: random() * Math.max(1, width), y: random() * Math.max(1, height),
      vx: (random() - 0.5) * 3, vy: -(4 + random() * 5),
      radius: 1.2 + random() * 1.6, opacity: 0.22 + random() * 0.32,
      color: COLORS[index % COLORS.length],
    }));
  }

  function advanceParticles(particles, {width, height, elapsed, pointer}) {
    const step = Math.max(0, Math.min(0.05, elapsed || 0));
    const wrap = (value, bound) => ((value % Math.max(1, bound)) + Math.max(1, bound)) % Math.max(1, bound);
    return particles.map(point => {
      let x = point.x + point.vx * step;
      let y = point.y + point.vy * step;
      if (pointer) {
        const dx = point.x - pointer.x || 0.01;
        const dy = point.y - pointer.y;
        const distance = Math.hypot(dx, dy);
        const force = Math.max(0, 1 - distance / 140) * 55 * step;
        x += dx / distance * force;
        y += dy / distance * force;
      }
      return {...point, x: wrap(x, width), y: wrap(y, height)};
    });
  }

  function miniCopy(market, tone) {
    const nextMarket = Object.hasOwn(MINI_COPIES, market) ? market : 'hk';
    const nextTone = Object.hasOwn(MINI_COPIES[nextMarket], tone) ? tone : 'standard';
    return MINI_COPIES[nextMarket][nextTone];
  }

  function createCanvasController(canvas, hero) {
    let context;
    try { context = canvas.getContext('2d'); }
    catch { canvas.dataset.motion = 'unavailable'; return null; }
    if (!context) { canvas.dataset.motion = 'unavailable'; return null; }
    const document = root.document;
    const supportsAnimation = typeof root.requestAnimationFrame === 'function' && typeof root.cancelAnimationFrame === 'function';
    const media = root.matchMedia?.('(prefers-reduced-motion: reduce)') || {matches: false};
    let field = {width: 1, height: 1, particles: createParticles(1, 1), pointer: null};
    let requestedVisible = false;
    let intersecting = true;
    let frameId = null;
    let lastTime = null;
    canvas.dataset.particleCount = '45';

    function draw() {
      context.globalAlpha = 1;
      context.fillStyle = '#FFFFFF';
      context.fillRect(0, 0, field.width, field.height);
      field.particles.forEach(point => {
        context.beginPath();
        context.fillStyle = point.color;
        context.globalAlpha = point.opacity;
        context.arc(point.x, point.y, point.radius, 0, Math.PI * 2);
        context.fill();
      });
      context.globalAlpha = 1;
    }

    function resize() {
      const bounds = hero.getBoundingClientRect();
      const width = Math.max(1, bounds.width);
      const height = Math.max(1, bounds.height);
      const ratio = Math.min(2, Math.max(1, root.devicePixelRatio || 1));
      field = {...field, width, height, particles: field.particles.map(point => ({
        ...point, x: point.x / field.width * width, y: point.y / field.height * height,
      }))};
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      draw();
    }

    function canAnimate() {
      return supportsAnimation && requestedVisible && intersecting && !document.hidden && !media.matches;
    }

    function frame(time) {
      frameId = null;
      if (!canAnimate()) { sync(); return; }
      const elapsed = lastTime === null ? 0 : (time - lastTime) / 1000;
      lastTime = time;
      field = {...field, particles: advanceParticles(field.particles, {...field, elapsed})};
      draw();
      frameId = root.requestAnimationFrame(frame);
    }

    function sync() {
      const active = requestedVisible && intersecting && !document.hidden;
      canvas.dataset.motion = active ? (media.matches ? 'reduced' : supportsAnimation ? 'running' : 'paused') : 'paused';
      if (canAnimate() && frameId === null) frameId = root.requestAnimationFrame(frame);
      else if (!canAnimate()) {
        if (frameId !== null) root.cancelAnimationFrame(frameId);
        frameId = null;
        lastTime = null;
        field = {...field, pointer: null};
        draw();
      }
    }

    hero.addEventListener('pointermove', event => {
      if (!canAnimate() || event.pointerType === 'touch') return;
      const bounds = hero.getBoundingClientRect();
      field = {...field, pointer: {x: event.clientX - bounds.left, y: event.clientY - bounds.top}};
    }, {passive: true});
    const clearPointer = () => { field = {...field, pointer: null}; };
    hero.addEventListener('pointerleave', clearPointer, {passive: true});
    root.addEventListener('blur', clearPointer);
    document.addEventListener('visibilitychange', sync);
    if (media.addEventListener) media.addEventListener('change', sync);
    else media.addListener?.(sync);
    if (root.IntersectionObserver) {
      const observer = new root.IntersectionObserver(entries => {
        const entry = entries.find(item => item.target === hero);
        if (entry) { intersecting = entry.isIntersecting; sync(); }
      });
      observer.observe(hero);
    }
    if (root.ResizeObserver) new root.ResizeObserver(resize).observe(hero);
    else root.addEventListener('resize', resize, {passive: true});
    resize();
    sync();
    return Object.freeze({setVisible(value) { requestedVisible = Boolean(value); if (value) resize(); sync(); }});
  }

  let initialized = false;
  let controller = null;
  let ui = {surface: 'rewrite', market: 'hk', tone: 'standard'};

  function renderMini() {
    const document = root.document;
    const copy = document.querySelector('#home-mini-copy');
    if (copy) {
      copy.textContent = miniCopy(ui.market, ui.tone);
      copy.lang = {hk: 'zh-HK', cn: 'zh-CN', en: 'en'}[ui.market];
    }
    ['market', 'tone'].forEach(type => document.querySelectorAll(`[data-mini-${type}]`).forEach(button => {
      const active = button.dataset[type === 'market' ? 'miniMarket' : 'miniTone'] === ui[type];
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    }));
  }

  function selectSurface(surface, focus = false) {
    const next = SURFACES.includes(surface) ? surface : 'rewrite';
    ui = {...ui, surface: next};
    root.document.querySelectorAll('[data-home-surface]').forEach(button => {
      const active = button.dataset.homeSurface === next;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
      if (active && focus) button.focus();
    });
    root.document.querySelectorAll('[data-home-surface-panel]').forEach(panel => {
      const active = panel.dataset.homeSurfacePanel === next;
      panel.hidden = !active;
      panel.classList.toggle('is-active', active);
    });
  }

  function onClick(event) {
    const button = event.target.closest('button');
    if (button?.matches('[data-home-surface]')) selectSurface(button.dataset.homeSurface);
    else if (button?.matches('[data-mini-market], [data-mini-tone]')) {
      const type = button.dataset.miniMarket ? 'market' : 'tone';
      const value = button.dataset[type === 'market' ? 'miniMarket' : 'miniTone'];
      if (type === 'market' ? Object.hasOwn(MINI_COPIES, value) : Object.hasOwn(MINI_COPIES.hk, value)) {
        ui = {...ui, [type]: value};
        renderMini();
      }
    }
  }

  function onKeydown(event) {
    if (!event.target.matches('[data-home-surface]')) return;
    const keys = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'];
    if (!keys.includes(event.key)) return;
    event.preventDefault();
    const index = SURFACES.indexOf(event.target.dataset.homeSurface);
    const backwards = ['ArrowLeft', 'ArrowUp'].includes(event.key);
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? SURFACES.length - 1
      : (index + (backwards ? -1 : 1) + SURFACES.length) % SURFACES.length;
    selectSurface(SURFACES[next], true);
  }

  function initialize() {
    if (initialized) return true;
    const document = root.document;
    if (!document) return false;
    const canvas = document.querySelector('#antigravity-canvas');
    const hero = document.querySelector('.home-hero');
    if (!canvas || !hero) return false;
    controller = createCanvasController(canvas, hero);
    document.addEventListener('click', onClick);
    document.addEventListener('keydown', onKeydown);
    selectSurface(ui.surface);
    renderMini();
    initialized = true;
    return true;
  }

  function setVisible(visible) {
    if (!initialized) initialize();
    controller?.setVisible(visible);
  }

  const api = Object.freeze({initialize, setVisible, createParticles, advanceParticles, miniCopy});
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.BrandLexHome = api;
})(typeof window === 'undefined' ? globalThis : window);
