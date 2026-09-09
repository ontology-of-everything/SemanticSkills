/* html-slides · deck 运行时（≤120 行，无依赖）。整段复制进 deck 末尾的 <script>。
   滚动模式（默认）：所有 build 已显示、layer 可点选，便于阅读与 ?debug。
   放映模式（P / ▶）：方向键 / 空格 / 点击空白 / 滚轮逐拍推进；Home/End 首末页；F 全屏。
   刷新回到上次页（#页号 优先，其次 localStorage）。?debug 标出溢出并在控制台列出。 */
(() => {
  const W = 1920, H = 1080, d = document;
  const wraps = [...d.querySelectorAll('.slide-wrap')], slides = wraps.map(w => w.firstElementChild);
  const key = 'html-slides:' + location.pathname, q = new URLSearchParams(location.search);
  let cur = 0, level = 0, present = false, manual = new Map();
  const clamp = i => Math.max(0, Math.min(slides.length - 1, i));
  const steps = s => [...s.querySelectorAll('[data-step]')].map(e => +e.dataset.step);
  const total = s => steps(s).length ? Math.max(...steps(s)) + 1 : 0;

  function setLayer(s, g, k) {
    s.querySelectorAll(`[data-layer-group="${g}"]`).forEach(e =>
      e.toggleAttribute('data-active', (e.dataset.layerBtn ?? e.dataset.layerPanel) === k));
  }
  function paint(s, lv) {
    s.querySelectorAll('.build').forEach(e => e.toggleAttribute('data-shown', !present || lv > +e.dataset.step));
    new Set([...s.querySelectorAll('[data-layer-group]')].map(e => e.dataset.layerGroup)).forEach(g => {
      const btns = [...s.querySelectorAll(`[data-layer-btn][data-layer-group="${g}"]`)];
      let act = btns[0];
      const m = manual.get(s)?.[g];
      if (m) act = btns.find(b => b.dataset.layerBtn === m) || act;
      else if (present) btns.forEach(b => {
        if (b.dataset.step !== undefined && +b.dataset.step < lv &&
            (act.dataset.step === undefined || +b.dataset.step >= +act.dataset.step)) act = b;
      });
      if (act) setLayer(s, g, act.dataset.layerBtn);
    });
  }
  function paintAll() { slides.forEach((s, i) => paint(s, i === cur ? level : (present ? 0 : 99))); }
  function fit() {
    const s = present ? Math.min(innerWidth / W, innerHeight / H) : Math.min(1, (innerWidth - 48) / W);
    d.documentElement.style.setProperty('--s', s);
  }
  function remember() {
    wraps.forEach((w, j) => w.classList.toggle('cur', j === cur));
    localStorage.setItem(key, cur); history.replaceState(null, '', '#' + (cur + 1));
    d.querySelectorAll('.pn').forEach(e => e.textContent = `${cur + 1} / ${slides.length}`);
  }
  function goto(i, lv = 0) {
    cur = clamp(i); level = lv; manual.delete(slides[cur]);
    if (!present) wraps[cur].scrollIntoView({ block: 'start' });
    paintAll(); remember();
  }
  function advance() { level < total(slides[cur]) ? (level++, paint(slides[cur], level)) : cur < slides.length - 1 && goto(cur + 1); }
  function back() { level > 0 ? (level--, paint(slides[cur], level)) : cur > 0 && goto(cur - 1, total(slides[cur - 1])); }
  function setMode(p) {
    present = p; d.body.classList.toggle('present', p); fit();
    if (p && d.fullscreenEnabled && !d.fullscreenElement) d.documentElement.requestFullscreen().catch(() => {});
    goto(cur, 0);
  }

  d.addEventListener('click', e => {
    const btn = e.target.closest('[data-layer-btn]');
    if (btn) {
      const s = btn.closest('.slide'), g = btn.dataset.layerGroup;
      manual.set(s, { ...(manual.get(s) || {}), [g]: btn.dataset.layerBtn }); setLayer(s, g, btn.dataset.layerBtn); return;
    }
    const mode = e.target.closest('[data-mode]');
    if (mode) return setMode(mode.dataset.mode === 'present');
    if (present && !e.target.closest('a,button,iframe,input,textarea,video')) advance();
  });
  d.addEventListener('keydown', e => {
    if (e.target.matches?.('input,textarea')) return;
    if (e.key === 'p' || e.key === 'P') return setMode(!present);
    if (e.key === 'f' || e.key === 'F') return d.fullscreenElement ? d.exitFullscreen() : d.documentElement.requestFullscreen();
    if (!present) return;
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); advance(); }
    if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); back(); }
    if (e.key === 'Home') goto(0);
    if (e.key === 'End') goto(slides.length - 1);
  });
  let wheelLock = 0;
  d.addEventListener('wheel', e => {
    if (!present || e.ctrlKey || e.metaKey) return;
    e.preventDefault(); const now = Date.now(); if (now - wheelLock < 180) return; wheelLock = now;
    e.deltaY > 0 ? advance() : back();
  }, { passive: false });
  let tick = 0;
  addEventListener('scroll', () => {
    if (present || tick) return;
    tick = requestAnimationFrame(() => {
      tick = 0; let i = 0, best = Infinity;
      wraps.forEach((w, j) => { const d = Math.abs(w.getBoundingClientRect().top); if (d < best) { best = d; i = j; } });
      if (i !== cur) { cur = i; remember(); }
    });
  });
  addEventListener('resize', () => { fit(); if (!present) wraps[cur].scrollIntoView({ block: 'start' }); });
  addEventListener('hashchange', () => { const i = parseInt(location.hash.slice(1)) - 1; if (i >= 0 && i !== cur) goto(i); });

  slides.forEach((s, i) => s.querySelectorAll('.foot-l').forEach(e => e.dataset.pn = i + 1));
  if (q.has('debug')) {
    const bad = [];
    slides.forEach(s => {
      if (s.scrollHeight > H + 1 || s.scrollWidth > W + 1) { s.classList.add('dbg-overflow'); bad.push(`${s.dataset.label}: ${s.scrollWidth}×${s.scrollHeight}`); }
      s.querySelectorAll('*').forEach(e => {
        if (e.offsetParent === null || e.tagName === 'SVG') return;
        if (getComputedStyle(e).overflow !== 'visible' && (e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1)) {
          e.classList.add('dbg-clip'); bad.push(`${s.dataset.label} › ${e.tagName.toLowerCase()}.${(e.className || '').split(' ')[0]} clipped`);
        }
      });
    });
    console.log(bad.length ? `[html-slides debug] ${bad.length} overflow issue(s):\n` + bad.join('\n') : '[html-slides debug] no overflow');
    d.title = (bad.length ? `⚠${bad.length} ` : '✓ ') + d.title;
  }
  fit();
  goto(clamp((parseInt(location.hash.slice(1)) || +localStorage.getItem(key) + 1 || 1) - 1));
})();
