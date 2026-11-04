(() => {
  // 모든 옵션 = 실제 생성 이미지 한 장. 캔버스 합성·틴트·필터·반전 없음.
  const D = window.CATALOG;
  const IMG_AXES = D.imageKey;
  const EXTRA = { volume: 'normal', parting: 'style', color: 'natural', technique: 'whole' };
  const WEIGHT = { length: 8, curl: 4, color: 3, technique: 3, bangs: 2, volume: 2, parting: 2, cut: 1 };
  let gender = 'female', openGroup = 'shape';
  let state = {}, prev = null, front = 'A', seq = 0;

  const $ = (s, r = document) => r.querySelector(s);
  const axesOf = g => ({ ...D.axes[g], ...D.common });
  const axisOrder = () => D.groups.flatMap(x => x.axes);
  const allValues = (g, a) => axesOf(g)[a].values === 'COLORS' ? D.colors : axesOf(g)[a].values;
  const findVal = (g, a, id) => allValues(g, a).find(v => v.id === id);
  const src = f => `img/${f}.webp`, tsrc = f => `img/t/${f}.webp`;
  const pre = new Set(); const preload = f => { if (pre.has(f)) return; pre.add(f); const i = new Image(); i.decoding = 'async'; i.src = src(f); };

  // 후보 = 실제 이미지가 있는 상태 전체
  const parse = k => { const p = k.split('-'), s = {}; IMG_AXES.forEach((a, i) => s[a] = p[i + 1]); return { g: p[0], s }; };
  const CANDS = [
    ...D.available.map(k => { const { g, s } = parse(k); return { g, s: { ...s, ...EXTRA }, file: k }; }),
    ...D.variants.map(v => { const { g, s } = parse(v.key); return { g, s: { ...s, ...EXTRA, ...v.set }, file: v.file }; })
  ];
  const candsOf = g => CANDS.filter(c => c.g === g[0]);
  const same = (a, b) => axisOrder().every(x => a[x] === b[x]);
  const exact = (g, s) => candsOf(g).find(c => same(c.s, s));
  const valuesOf = (g, a) => allValues(g, a).filter(v => candsOf(g).some(c => c.s[a] === v.id)); // 이미지 없는 값은 숨김

  function snap(g, s, fixed) {
    const hit = exact(g, s); if (hit) return hit;
    let best = null, bc = Infinity;
    for (const c of candsOf(g)) {
      if (fixed && c.s[fixed] !== s[fixed]) continue;
      let cost = 0;
      for (const a of axisOrder()) if (c.s[a] !== s[a]) cost += WEIGHT[a] + allValues(g, a).findIndex(v => v.id === c.s[a]) * 0.01;
      if (cost < bc) { bc = cost; best = c; }
    }
    return best;
  }
  const defaults = g => { const s = {}; for (const a of axisOrder()) s[a] = allValues(g, a)[0].id; return s; };

  const brandOf = id => D.brands.find(b => b.id === id);
  function caption(s) {
    const c = findVal(gender, 'color', s.color);
    if (!c.brand) return '';
    const b = brandOf(c.brand);
    return `<b>${b.name}</b> · ${c.code} <span>(${c.name})</span>`;
  }

  function show(s, msg) {
    const my = ++seq, c = exact(gender, s);
    const back = front === 'A' ? $('#imB') : $('#imA');
    let fired = false;
    const done = () => {
      if (my !== seq || fired) return; fired = true;
      back.classList.add('on'); (front === 'A' ? $('#imA') : $('#imB')).classList.remove('on');
      front = front === 'A' ? 'B' : 'A';
      $('#frame').dataset.file = c.file;
    };
    back.onload = done; back.src = src(c.file); if (back.complete && back.naturalWidth) done();
    $('#cap').innerHTML = caption(s); $('#cap').classList.toggle('on', !!caption(s));
    if (msg) toast(msg);
  }

  let tt; function toast(t) { const e = $('#toast'); e.textContent = t; e.classList.add('on'); clearTimeout(tt); tt = setTimeout(() => e.classList.remove('on'), 2200); }

  const label = (a, id) => { const v = findVal(gender, a, id); return v.code ? `${v.code} ${v.name}` : v.label; };
  function choose(a, id) {
    if (state[a] === id) return;
    prev = { ...state };
    const want = { ...state, [a]: id };
    const c = snap(gender, want, a);
    let msg = `${axesOf(gender)[a].label} → ${label(a, id)}`;
    const changed = axisOrder().filter(x => c.s[x] !== want[x]);
    if (changed.length) msg += ` · 자동 조정: ${changed.map(x => `${axesOf(gender)[x].label} ${label(x, c.s[x])}`).join(', ')}`;
    state = { ...c.s };
    show(state, msg); drawPanel(); drawSummary();
  }

  function drawSummary() {
    $('#summary').innerHTML = axisOrder().map(a => {
      const g = D.groups.find(x => x.axes.includes(a));
      return `<button class="pill" data-group="${g.id}"><small>${axesOf(gender)[a].label}</small>${label(a, state[a])}</button>`;
    }).join('');
    $('#summary').querySelectorAll('.pill').forEach(b => b.onclick = () => { openGroup = b.dataset.group; drawPanel(); });
  }

  function chip(a, v) {
    const on = state[a] === v.id;
    const want = { ...state, [a]: v.id };
    const ok = !!exact(gender, want);
    const c = snap(gender, want, a);
    const name = v.code ? `${v.code}<small>${v.name}</small>` : v.label;
    return `<button class="chip ${on ? 'on' : ''}" data-axis="${a}" data-id="${v.id}" title="${ok ? '' : '현재 조합의 이미지가 없어 선택 시 다른 옵션이 자동 조정됩니다'}">
      <img class="thumb" loading="lazy" decoding="async" src="${tsrc(c.file)}" data-full="${c.file}" alt=""><b>${name}</b>${ok ? '' : '<i>자동 조정</i>'}</button>`;
  }
  function axisBody(a) {
    const vals = valuesOf(gender, a);
    if (a !== 'color') return `<div class="chips">${vals.map(v => chip(a, v)).join('')}</div>`;
    const groups = [{ id: '', name: '염색 안 함' }, ...D.brands];
    return groups.map(b => {
      const vs = vals.filter(v => (v.brand || '') === b.id); if (!vs.length) return '';
      return `<div class="brand-row"><h5>${b.name}${b.note ? ` <span>${b.note}</span>` : ''}${b.source ? ` <a href="${b.source}" target="_blank" rel="noopener">출처</a>` : ''}</h5><div class="chips">${vs.map(v => chip(a, v)).join('')}</div></div>`;
    }).join('');
  }

  function drawPanel() {
    $('#panel').innerHTML = D.groups.map((g, gi) => {
      const open = g.id === openGroup;
      const picked = g.axes.map(a => label(a, state[a])).join(' · ');
      return `<div class="group ${open ? 'open' : ''}">
        <button class="ghead" data-group="${g.id}"><em>0${gi + 1}</em><span><b>${g.title}</b><small>${open ? g.sub : picked}</small></span><i>${open ? '−' : '+'}</i></button>
        ${open ? `<div class="gbody">${g.axes.map(a => `<div class="axis"><h4>${axesOf(gender)[a].label}</h4>${axisBody(a)}</div>`).join('')}
          ${g.id === 'color' ? `<p class="note">컬러·기법·볼륨·가르마 이미지는 기장별 기본 스타일에서 생성했습니다. 다른 스타일에서 고르면 그 스타일로 자동 조정됩니다.</p>` : ''}
          ${gi < D.groups.length - 1 ? `<button class="next" data-group="${D.groups[gi + 1].id}">다음: ${D.groups[gi + 1].title} →</button>` : ''}
        </div>` : ''}
      </div>`;
    }).join('');
    $('#panel').querySelectorAll('.ghead,.next').forEach(b => b.onclick = () => { openGroup = openGroup === b.dataset.group && b.classList.contains('ghead') ? '' : b.dataset.group; drawPanel(); });
    $('#panel').querySelectorAll('.chip').forEach(b => {
      b.onclick = () => choose(b.dataset.axis, b.dataset.id);
      b.onpointerenter = () => preload(b.querySelector('.thumb').dataset.full);
    });
    // 이웃 프리로드: 열린 그룹에서 바로 고를 수 있는 이미지(최대 12장)를 유휴 시간에 미리 받음
    const next = [...$('#panel').querySelectorAll('.group.open .thumb')].map(i => i.dataset.full).slice(0, 12);
    (window.requestIdleCallback || setTimeout)(() => next.forEach(preload));
  }

  function setGender(g) {
    gender = g; state = { ...snap(g, defaults(g)).s }; prev = null;
    document.querySelectorAll('.gender button').forEach(b => b.classList.toggle('on', b.dataset.gender === g));
    drawPanel(); drawSummary(); show(state);
  }

  document.querySelectorAll('.gender button').forEach(b => b.onclick = () => setGender(b.dataset.gender));
  const cmp = $('#cmp');
  const hold = on => { if (!prev) return toast('먼저 옵션을 하나 바꿔보세요'); show(on ? prev : state, on ? '이전 모습' : null); };
  cmp.addEventListener('pointerdown', () => hold(true));
  ['pointerup', 'pointerleave'].forEach(e => cmp.addEventListener(e, () => prev && hold(false)));
  window.__hair = { choose, setGender, get state() { return state; }, get file() { return $('#frame').dataset.file; }, CANDS };
  setGender('female');
})();
