(() => {
  const D = window.CATALOG;
  const W = 600, H = 800;
  const imgCache = {}, maskCache = {};
  let gender = 'female', openGroup = 'shape', strength = 70;
  let state = {}, prev = null, front = 'A';

  const $ = (s, r = document) => r.querySelector(s);
  const axesOf = g => D.axes[g];
  const valuesOf = (g, a) => axesOf(g)[a].values === 'COLORS' ? D.colors : axesOf(g)[a].values;
  const findVal = (g, a, id) => valuesOf(g, a).find(v => v.id === id);

  function defaults(g) { const s = {}; for (const a in axesOf(g)) s[a] = valuesOf(g, a)[0].id; return s; }

  // 이미지 키: 플레이스홀더 값은 fallback(가장 가까운 실제 이미지)로 매핑
  function resolvedId(g, a, id) { const v = findVal(g, a, id); return v && v.fallback ? v.fallback : id; }
  function keyFor(g, s) { return [g[0], ...D.imageKey[g].map(a => resolvedId(g, a, s[a]))].join('-'); }
  const src = k => `img/${k}.jpg`, msrc = k => `img/${k}-mask.png`;

  function load(url, cache) {
    if (!cache[url]) cache[url] = new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(i); i.onerror = no; i.src = url; });
    return cache[url];
  }
  function preloadAll() {
    const g = gender, ax = D.imageKey[g];
    const combos = ax.reduce((acc, a) => acc.flatMap(c => valuesOf(g, a).filter(v => !v.placeholder).map(v => ({ ...c, [a]: v.id }))), [{}]);
    combos.forEach(c => { const k = keyFor(g, c); load(src(k), imgCache); load(msrc(k), maskCache); });
  }

  // 머리카락만 염색: 마스크(hair 확률) × 강도로, 밝기는 유지하고 색만 바꿈
  async function render(canvas, s) {
    const k = keyFor(gender, s);
    const img = await load(src(k), imgCache);
    canvas.width = W; canvas.height = H;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, W, H);
    const col = D.colors.find(c => c.id === s.color);
    if (!col || !col.hex) return;
    const mask = await load(msrc(k), maskCache);
    const mc = document.createElement('canvas'); mc.width = W; mc.height = H;
    const mctx = mc.getContext('2d'); mctx.drawImage(mask, 0, 0, W, H);
    const m = mctx.getImageData(0, 0, W, H).data;
    const id = ctx.getImageData(0, 0, W, H), p = id.data;
    const tr = parseInt(col.hex.slice(1, 3), 16), tg = parseInt(col.hex.slice(3, 5), 16), tb = parseInt(col.hex.slice(5, 7), 16);
    const tl = 0.299 * tr + 0.587 * tg + 0.114 * tb || 1;
    const st = strength / 100;
    for (let i = 0; i < p.length; i += 4) {
      const a = (m[i] / 255) * st; if (a < 0.02) continue;
      const l = 0.299 * p[i] + 0.587 * p[i + 1] + 0.114 * p[i + 2];
      // 어두운 모발도 색이 보이도록 밝기를 목표 톤 쪽으로 일부 끌어올림
      const lift = l + (tl - l) * 0.45, f = lift / tl;
      p[i] += (Math.min(255, tr * f) - p[i]) * a;
      p[i + 1] += (Math.min(255, tg * f) - p[i + 1]) * a;
      p[i + 2] += (Math.min(255, tb * f) - p[i + 2]) * a;
    }
    ctx.putImageData(id, 0, 0);
  }

  async function show(s, changedLabel) {
    const back = front === 'A' ? $('#cvB') : $('#cvA');
    await render(back, s);
    back.classList.add('on'); (front === 'A' ? $('#cvA') : $('#cvB')).classList.remove('on');
    front = front === 'A' ? 'B' : 'A';
    if (changedLabel) toast(changedLabel);
    const ph = Object.keys(s).map(a => findVal(gender, a, s[a])).filter(v => v && v.placeholder);
    $('#ph').textContent = ph.length ? `이미지 준비중: ${ph.map(v => v.label).join(', ')} · 가장 가까운 결과로 표시` : '';
    $('#ph').classList.toggle('on', ph.length > 0);
  }

  let tt; function toast(t) { const e = $('#toast'); e.textContent = t; e.classList.add('on'); clearTimeout(tt); tt = setTimeout(() => e.classList.remove('on'), 1600); }

  function choose(a, id) {
    if (state[a] === id) return;
    prev = { ...state };
    state[a] = id;
    const v = findVal(gender, a, id);
    show(state, `${axesOf(gender)[a].label} → ${v.label}`);
    drawPanel(); drawSummary();
  }

  function drawSummary() {
    $('#summary').innerHTML = Object.keys(state).map(a => {
      const g = D.groups.find(x => x.axes.includes(a));
      return `<button class="pill" data-group="${g.id}"><small>${axesOf(gender)[a].label}</small>${findVal(gender, a, state[a]).label}</button>`;
    }).join('');
    $('#summary').querySelectorAll('.pill').forEach(b => b.onclick = () => { openGroup = b.dataset.group; drawPanel(); });
  }

  function chip(a, v) {
    const on = state[a] === v.id;
    if (a === 'color') {
      const bg = v.hex || 'linear-gradient(135deg,#6b4a3a,#3a281f)';
      return `<button class="chip color ${on ? 'on' : ''}" data-axis="${a}" data-id="${v.id}"><span class="sw" style="background:${bg}"></span><b>${v.label}</b></button>`;
    }
    const k = keyFor(gender, { ...state, [a]: v.id });
    return `<button class="chip ${on ? 'on' : ''}" data-axis="${a}" data-id="${v.id}">
      <span class="thumb" style="background-image:url(${src(k)})"></span>
      <b>${v.label}</b>${v.placeholder ? '<i>이미지 준비중</i>' : ''}</button>`;
  }

  function drawPanel() {
    $('#panel').innerHTML = D.groups.map((g, gi) => {
      const open = g.id === openGroup;
      const picked = g.axes.map(a => findVal(gender, a, state[a]).label).join(' · ');
      return `<div class="group ${open ? 'open' : ''}">
        <button class="ghead" data-group="${g.id}"><em>0${gi + 1}</em><span><b>${g.title}</b><small>${open ? g.sub : picked}</small></span><i>${open ? '−' : '+'}</i></button>
        ${open ? `<div class="gbody">${g.axes.map(a => `
          <div class="axis"><h4>${axesOf(gender)[a].label}${axesOf(gender)[a].image ? '' : (a === 'color' ? '' : ' <span class="tag">이미지 준비중</span>')}</h4>
          <div class="chips ${a === 'color' ? 'colors' : ''}">${valuesOf(gender, a).map(v => chip(a, v)).join('')}</div></div>`).join('')}
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
    gender = g; state = defaults(g); prev = null;
    document.querySelectorAll('.gender button').forEach(b => b.classList.toggle('on', b.dataset.gender === g));
    preloadAll(); drawPanel(); drawSummary(); show(state);
  }

  document.querySelectorAll('.gender button').forEach(b => b.onclick = () => setGender(b.dataset.gender));
  const cmp = $('#cmp');
  const hold = on => { if (!prev) return toast('먼저 옵션을 하나 바꿔보세요'); show(on ? prev : state, on ? '이전 모습' : null); };
  cmp.addEventListener('pointerdown', () => hold(true));
  ['pointerup', 'pointerleave'].forEach(e => cmp.addEventListener(e, () => prev && hold(false)));
  setGender('female');
})();
