const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { createParticles, advanceParticles, miniCopy } = require('../static/js/home.js');

test('particle field creates exactly 45 bounded subtle dots', () => {
  const particles = createParticles(1200, 720, () => 0.5);
  assert.equal(particles.length, 45);
  assert(particles.every(point => point.x >= 0 && point.x <= 1200 && point.y >= 0 && point.y <= 720));
  assert(particles.every(point => point.radius > 0 && point.radius < 4 && point.opacity < 0.7));
  assert(particles.every(point => ['#6366F1', '#94A3B8', '#0EA5E9'].includes(point.color)));
});

test('particle updates drift upward without mutating an earlier frame', () => {
  const particles = createParticles(1200, 720, () => 0.5);
  const before = structuredClone(particles);
  const next = advanceParticles(particles, {width: 1200, height: 720, elapsed: 0.016, pointer: null});
  assert.deepEqual(particles, before);
  assert.notEqual(next, particles);
  assert(next.every((point, index) => point.y < before[index].y && point !== particles[index]));
});

test('nearby cursor pushes particles away and wrapping stays in bounds', () => {
  const particles = createParticles(1200, 720, () => 0.5);
  const ordinary = advanceParticles(particles, {width: 1200, height: 720, elapsed: 0.016, pointer: null});
  const repelled = advanceParticles(particles, {width: 1200, height: 720, elapsed: 0.016, pointer: {x: 590, y: 360}});
  assert(repelled[0].x > ordinary[0].x);
  const edge = [{...particles[0], x: 1201, y: -10}];
  const wrapped = advanceParticles(edge, {width: 1200, height: 720, elapsed: 50, pointer: {x: 600, y: 360}});
  assert(wrapped.every(point => point.x >= 0 && point.x <= 1200 && point.y >= 0 && point.y <= 720));
});

test('mini previews cover nine distinct market and tone combinations', () => {
  const previews = ['hk', 'cn', 'en'].flatMap(market => ['standard', 'social', 'concise'].map(tone => miniCopy(market, tone)));
  assert.equal(new Set(previews).size, 9);
  assert.match(miniCopy('hk', 'standard'), /禮|聯|運/);
  assert.match(miniCopy('cn', 'standard'), /礼|联|邮/);
  assert.doesNotMatch(miniCopy('en', 'standard'), /[\u3400-\u9fff]/);
  assert.equal(miniCopy('invalid', 'invalid'), miniCopy('hk', 'standard'));
});

function fakeBrowser(contextUnavailable = false) {
  const frames = new Map();
  const listeners = {};
  const media = {matches: false, addEventListener: (name, fn) => { listeners.media = fn; }};
  const canvas = {dataset: {}, style: {}, getContext: () => {
    if (contextUnavailable) throw new Error('Canvas disabled by browser');
    return context;
  }};
  const context = Object.fromEntries(['setTransform', 'fillRect', 'beginPath', 'arc', 'fill'].map(name => [name, () => {}]));
  const hero = {getBoundingClientRect: () => ({width: 1200, height: 720, left: 0, top: 0}), addEventListener: (name, fn) => { listeners[name] = fn; }};
  const document = {hidden: false, querySelector: selector => ({'#antigravity-canvas': canvas, '.home-hero': hero}[selector] || null), querySelectorAll: () => [], addEventListener: (name, fn) => { listeners[name] = fn; }};
  let observer;
  const window = {
    document, devicePixelRatio: 3, matchMedia: () => media,
    requestAnimationFrame: fn => { const id = Symbol(); frames.set(id, fn); return id; },
    cancelAnimationFrame: id => frames.delete(id),
    addEventListener: (name, fn) => { listeners[name] = fn; },
    IntersectionObserver: class { constructor(fn) { observer = fn; } observe() {} },
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../static/js/home.js'), 'utf8'), {window});
  return {api: window.BrandLexHome, canvas, document, frames, media, listeners, intersect: value => observer([{target: hero, isIntersecting: value}])};
}

test('canvas pauses outside home, offscreen, in background, and reduced motion', () => {
  const browser = fakeBrowser();
  assert.equal(browser.api.initialize(), true);
  assert.equal(browser.api.initialize(), true);
  assert.equal(browser.frames.size, 0);
  assert.equal(browser.canvas.width, 2400, 'DPR capped at two');
  assert.equal(browser.canvas.dataset.particleCount, '45');
  browser.api.setVisible(true);
  assert.equal(browser.frames.size, 1);
  assert.equal(browser.canvas.dataset.motion, 'running');
  browser.api.setVisible(true);
  assert.equal(browser.frames.size, 1, 'No duplicate animation loop');
  browser.intersect(false);
  assert.equal(browser.frames.size, 0);
  browser.intersect(true);
  assert.equal(browser.frames.size, 1);
  browser.document.hidden = true;
  browser.listeners.visibilitychange();
  assert.equal(browser.frames.size, 0);
  browser.document.hidden = false;
  browser.listeners.visibilitychange();
  assert.equal(browser.frames.size, 1);
  browser.media.matches = true;
  browser.listeners.media();
  assert.equal(browser.frames.size, 0);
  assert.equal(browser.canvas.dataset.motion, 'reduced');
  browser.api.setVisible(false);
  assert.equal(browser.frames.size, 0);
  assert.equal(browser.canvas.dataset.motion, 'paused');
});

test('disabled canvas does not prevent homepage controls from initializing', () => {
  const browser = fakeBrowser(true);
  assert.equal(browser.api.initialize(), true);
  assert.equal(browser.canvas.dataset.motion, 'unavailable');
  assert.doesNotThrow(() => browser.api.setVisible(true));
  assert.equal(browser.frames.size, 0);
  assert.equal(typeof browser.listeners.click, 'function');
  assert.equal(typeof browser.listeners.keydown, 'function');
});

test('pending frame synchronizes a reduced preference before its media event arrives', () => {
  const browser = fakeBrowser();
  browser.api.initialize();
  browser.api.setVisible(true);
  browser.media.matches = true;
  const [id, frame] = browser.frames.entries().next().value;
  browser.frames.delete(id);
  frame(1000);
  assert.equal(browser.canvas.dataset.motion, 'reduced');
  assert.equal(browser.frames.size, 0, 'Reduced motion leaves no pending frame');
  browser.media.matches = false;
  browser.listeners.media();
  assert.equal(browser.canvas.dataset.motion, 'running');
  assert.equal(browser.frames.size, 1, 'Preference change resumes exactly one loop');
});
