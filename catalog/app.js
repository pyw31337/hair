(() => {
  const D = window.CATALOG;
  const W = 600, H = 800;
  const AVAIL = new Set(D.available);
  const IMG_AXES = D.imageKey;
  const cache = {};
  let gender = 'female', openGroup = 'shape', strength = 70;
  let state = {}, prev = null, front = 'A', renderSeq = 0;

  const $ = (s, r = document) => r.querySelector(s);
  const axesOf = g => ({ ...D.axes[g], ...D.common });
  const axisOrder = g => D.groups.flatMap(x => x.axes);
  const valuesOf = (g, a) => axesOf(g)[a].values === 'COLORS' ? D.colors : axesOf(g)[a].values;
  const findVal = (g, a, id) => valuesOf(g, a).find(v => v.id === id);
  const keyFor = (g, s) => [g[0], ...IMG_AXES.map(a => s[a])].join('-');
  const src = k => `img/${k}.jpg`, msrc = k => `img/${k}-mask.png`, fsrc = k => `img/${k}-fg.png`;

  function defaults(g) { const s = {}; for (const a of axisOrder(g)) s[a] = valuesOf(g, a)[0].id; return s; }

  // 불가능한 조합 → 방금 고른 값(fixed)은 유지하고, 나머지 이미지 축 변경이 가장 적은 유효 조합으로 스냅
  function snap(g, s, fixed) {
    if (AVAIL.has(keyFor(g, s))) return s;
    const weight = { length: 8, curl: 4, bangs: 2, cut: 1 };
    let best = null, bestCost = Infinity;
    for (const k of D.available) {
      const parts = k.split('-'); if (parts[0] !== g[0]) continue;
      const cand = {}; IMG_AXES.forEach((a, i) => cand[a] = parts[i + 1]);
      if (fixed && cand[fixed] !== s[fixed]) continue;
      let cost = 0; IMG_AXES.forEach(a => { if (cand[a] !== s[a]) cost += weight[a]; });
      // 같은 비용이면 각 축의 첫 번째(기본) 값 쪽을 선호
      IMG_AXES.forEach(a => { if (cand[a] !== s[a]) cost += valuesOf(g, a).findIndex(v => v.id === cand[a]) * 0.01; });
      if (cost < bestCost) { bestCost = cost; best = cand; }
    }
    return best ? { ...s, ...best } : s;
  }

  function load(url) {
    if (!cache[url]) cache[url] = new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(i); i.onerror = no; i.src = url; });
    return cache[url];
  }
  function preloadAll() { D.available.filter(k => k[0] === gender[0]).forEach(k => load(src(k))); }

  function pixels(img) {
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0, W, H);
    return x.getImageData(0, 0, W, H).data;
  }

  // 컬러 기법별 가중치: 전체 / 하이라이트(가는 세로 결) / 발레아쥬(아래로 갈수록 진해지는 그라데이션)
  function techWeight(tech, x, y, top, bot) {
    if (tech === 'highlight') {
      // 모발 결을 따라 흐르는 가늘고 부드러운 결(위상은 y에 따라 천천히 흔들림) + 뿌리 쪽은 옅게
      const ph = x * 0.33 + Math.sin(y * 0.012 + x * 0.02) * 2.2;
      const band = 0.55 + 0.45 * Math.sin(x * 0.047 + 1.3) * Math.sin(x * 0.021);
      const streak = Math.pow(Math.max(0, Math.sin(ph)), 8) * Math.max(0, band);
      const t = (y - top) / Math.max(1, bot - top);
      return Math.min(1, streak * 1.6) * Math.min(1, Math.max(0.25, t * 3));
    }
    if (tech === 'balayage') {
      const t = (y - top) / Math.max(1, bot - top);
      const s = Math.min(1, Math.max(0, (t - 0.25) / 0.55));
      return s * s * (3 - 2 * s);
    }
    return 1;
  }

  async function render(canvas, s) {
    const k = keyFor(gender, s);
    const needMask = (D.colors.find(c => c.id === s.color) || {}).hex || s.volume === 'up';
    const [img, mask, fg] = await Promise.all([load(src(k)), needMask ? load(msrc(k)) : null, s.volume === 'up' ? load(fsrc(k)) : null]);
    const work = document.createElement('canvas'); work.width = W; work.height = H;
    const ctx = work.getContext('2d');
    ctx.drawImage(img, 0, 0, W, H);
    const m = mask ? pixels(mask) : null;

    // 1) 머리카락만 염색 (마스크 × 강도 × 기법 가중치, 밝기 결은 유지)
    const col = D.colors.find(c => c.id === s.color);
    if (col && col.hex && m) {
      let top = H, bot = 0;
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x += 6) if (m[(y * W + x) * 4] > 128) { if (y < top) top = y; bot = y; }
      const id = ctx.getImageData(0, 0, W, H), p = id.data;
      const tr = parseInt(col.hex.slice(1, 3), 16), tg = parseInt(col.hex.slice(3, 5), 16), tb = parseInt(col.hex.slice(5, 7), 16);
      const tl = 0.299 * tr + 0.587 * tg + 0.114 * tb || 1;
      const st = strength / 100, tech = s.technique;
      const liftAmt = tech === 'whole' ? 0.45 : 0.75; // 하이라이트/발레아쥬는 더 밝게 리프트
      for (let i = 0, n = 0; i < p.length; i += 4, n++) {
        let a = (m[i] / 255) * st; if (a < 0.02) continue;
        a *= techWeight(tech, n % W, (n / W) | 0, top, bot); if (a < 0.02) continue;
        const l = 0.299 * p[i] + 0.587 * p[i + 1] + 0.114 * p[i + 2];
        const lift = l + (Math.max(tl, tech === 'whole' ? 0 : 150) - l) * liftAmt, f = lift / tl;
        p[i] += (Math.min(255, tr * f) - p[i]) * a;
        p[i + 1] += (Math.min(255, tg * f) - p[i + 1]) * a;
        p[i + 2] += (Math.min(255, tb * f) - p[i + 2]) * a;
      }
      ctx.putImageData(id, 0, 0);
    }

    // 2) 볼륨업: 머리카락 레이어를 정수리 기준으로 키워 뒤에 깔고, 얼굴·몸(전경−머리)을 다시 위에 올림
    if (s.volume === 'up' && m && fg) {
      const f = pixels(fg);
      const base = ctx.getImageData(0, 0, W, H);
      const hairL = new ImageData(new Uint8ClampedArray(base.data), W, H);
      const bodyL = new ImageData(new Uint8ClampedArray(base.data), W, H);
      for (let i = 0; i < base.data.length; i += 4) {
        hairL.data[i + 3] = m[i];
        bodyL.data[i + 3] = Math.max(0, f[i] - m[i]);
      }
      const tmp = c => { const cv = document.createElement('canvas'); cv.width = W; cv.height = H; cv.getContext('2d').putImageData(c, 0, 0); return cv; };
      const hc = tmp(hairL), bc = tmp(bodyL);
      const sc = 1.07, cx = W / 2, cy = H * 0.36;
      ctx.save(); ctx.translate(cx, cy); ctx.scale(sc, sc * 1.02); ctx.translate(-cx, -cy); ctx.drawImage(hc, 0, 0); ctx.restore();
      ctx.drawImage(hc, 0, 0);
      ctx.drawImage(bc, 0, 0);
    }

    // 3) 가르마 방향: 오른쪽이면 좌우 반전
    canvas.width = W; canvas.height = H;
    const out = canvas.getContext('2d');
    out.save();
    if (s.parting === 'right') { out.translate(W, 0); out.scale(-1, 1); }
    out.drawImage(work, 0, 0); out.restore();
  }

  async function show(s, msg) {
    const seq = ++renderSeq;
    const back = front === 'A' ? $('#cvB') : $('#cvA');
    await render(back, s);
    if (seq !== renderSeq) return;
    back.classList.add('on'); (front === 'A' ? $('#cvA') : $('#cvB')).classList.remove('on');
    front = front === 'A' ? 'B' : 'A';
    if (msg) toast(msg);
  }

  let tt; function toast(t) { const e = $('#toast'); e.textContent = t; e.classList.add('on'); clearTimeout(tt); tt = setTimeout(() => e.classList.remove('on'), 2200); }

  function choose(a, id) {
    if (state[a] === id) return;
    prev = { ...state };
    let next = { ...state, [a]: id };
    const v = findVal(gender, a, id);
    let msg = `${axesOf(gender)[a].label} → ${v.label}`;
    if (IMG_AXES.includes(a)) {
      const snapped = snap(gender, next, a);
      const changed = IMG_AXES.filter(x => snapped[x] !== next[x]);
      if (changed.length) msg += ` · 자동 조정: ${changed.map(x => `${axesOf(gender)[x].label} ${findVal(gender, x, snapped[x]).label}`).join(', ')}`;
      next = snapped;
    }
    state = next;
    show(state, msg);
    drawPanel(); drawSummary();
  }

  function drawSummary() {
    $('#summary').innerHTML = axisOrder(gender).map(a => {
      const g = D.groups.find(x => x.axes.includes(a));
      return `<button class="pill" data-group="${g.id}"><small>${axesOf(gender)[a].label}</small>${findVal(gender, a, state[a]).label}</button>`;
    }).join('');
    $('#summary').querySelectorAll('.pill').forEach(b => b.onclick = () => { openGroup = b.dataset.group; drawPanel(); });
  }

  const TECH_SW = { whole: 'linear-gradient(135deg,#8a5a3c,#8a5a3c)', highlight: 'repeating-linear-gradient(100deg,#3a281f 0 6px,#d9b48a 6px 9px)', balayage: 'linear-gradient(180deg,#3a281f 25%,#d9b48a)' };
  function chip(a, v) {
    const on = state[a] === v.id;
    if (a === 'color') {
      const bg = v.hex || 'linear-gradient(135deg,#6b4a3a,#3a281f)';
      return `<button class="chip color ${on ? 'on' : ''}" data-axis="${a}" data-id="${v.id}"><span class="sw" style="background:${bg}"></span><b>${v.label}</b></button>`;
    }
    if (a === 'technique') return `<button class="chip color ${on ? 'on' : ''}" data-axis="${a}" data-id="${v.id}"><span class="sw" style="background:${TECH_SW[v.id]}"></span><b>${v.label}</b></button>`;
    if (!IMG_AXES.includes(a)) return `<button class="chip text ${on ? 'on' : ''}" data-axis="${a}" data-id="${v.id}"><b>${v.label}</b></button>`;
    const want = { ...state, [a]: v.id };
    const ok = AVAIL.has(keyFor(gender, want));
    const k = keyFor(gender, snap(gender, want, a));
    return `<button class="chip ${on ? 'on' : ''}" data-axis="${a}" data-id="${v.id}" title="${ok ? '' : '현재 조합과 맞지 않아 선택 시 다른 옵션이 자동 조정됩니다'}">
      <span class="thumb${a === 'parting' ? '' : ''}" style="background-image:url(${src(k)})"></span>
      <b>${v.label}</b>${ok ? '' : '<i>자동 조정</i>'}</button>`;
  }

  function drawPanel() {
    $('#panel').innerHTML = D.groups.map((g, gi) => {
      const open = g.id === openGroup;
      const picked = g.axes.map(a => findVal(gender, a, state[a]).label).join(' · ');
      return `<div class="group ${open ? 'open' : ''}">
        <button class="ghead" data-group="${g.id}"><em>0${gi + 1}</em><span><b>${g.title}</b><small>${open ? g.sub : picked}</small></span><i>${open ? '−' : '+'}</i></button>
        ${open ? `<div class="gbody">${g.axes.map(a => `
          <div class="axis"><h4>${axesOf(gender)[a].label}</h4>
          <div class="chips ${IMG_AXES.includes(a) ? '' : 'colors'}">${valuesOf(gender, a).map(v => chip(a, v)).join('')}</div></div>`).join('')}
          ${g.id === 'color' ? `<label class="range"><span>컬러 강도 <b id="sv">${strength}%</b></span><input type="range" min="0" max="100" value="${strength}" id="str"></label>` : ''}
          ${gi < D.groups.length - 1 ? `<button class="next" data-group="${D.groups[gi + 1].id}">다음: ${D.groups[gi + 1].title} →</button>` : ''}
        </div>` : ''}
      </div>`;
    }).join('');
    $('#panel').querySelectorAll('.ghead,.next').forEach(b => b.onclick = () => { openGroup = openGroup === b.dataset.group && b.classList.contains('ghead') ? '' : b.dataset.group; drawPanel(); });
    $('#panel').querySelectorAll('.chip').forEach(b => b.onclick = () => choose(b.dataset.axis, b.dataset.id));
    const r = $('#str'); if (r) r.oninput = () => { strength = +r.value; $('#sv').textContent = strength + '%'; show(state); };
  }

  function setGender(g) {
    gender = g; state = snap(g, defaults(g)); prev = null;
    document.querySelectorAll('.gender button').forEach(b => b.classList.toggle('on', b.dataset.gender === g));
    preloadAll(); drawPanel(); drawSummary(); show(state);
  }

  document.querySelectorAll('.gender button').forEach(b => b.onclick = () => setGender(b.dataset.gender));
  const cmp = $('#cmp');
  const hold = on => { if (!prev) return toast('먼저 옵션을 하나 바꿔보세요'); show(on ? prev : state, on ? '이전 모습' : null); };
  cmp.addEventListener('pointerdown', () => hold(true));
  ['pointerup', 'pointerleave'].forEach(e => cmp.addEventListener(e, () => prev && hold(false)));
  window.__hair = { choose, get state() { return state; }, setGender, setStrength: v => { strength = v; show(state); } };
  setGender('female');
})();
