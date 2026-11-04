/* 옵션 데이터 — 모든 옵션은 실제 생성 이미지 1장에 대응한다 (CSS/JS 효과 없음).
 * 이미지 파일: img/<스타일키>[-<변형>].jpg
 *   스타일키 = {f|m}-{length}-{cut}-{bangs}-{curl}  (available 목록)
 *   변형     = -vol | -part-center | -part-side | -t-highlight | -t-balayage | -c-<shadeId>
 * 변형(볼륨·가르마·컬러·기법)은 성별·기장별 '베이스 스타일'에서만 생성했다(variants 목록).
 * 조합이 없으면 app.js가 방금 고른 값을 유지한 채 가장 가까운 실제 이미지로 자동 조정한다. */
window.CATALOG = {
  imageKey: ['length','cut','bangs','curl'],
  available: ['f-short-natural-none-straight','f-short-natural-none-ccurl','f-short-natural-none-wave','f-short-natural-seethrough-straight','f-short-natural-seethrough-ccurl','f-short-natural-seethrough-wave','f-short-natural-full-straight','f-short-natural-full-ccurl','f-short-natural-full-wave','f-short-natural-side-straight','f-short-natural-side-ccurl','f-short-natural-side-wave','f-short-layered-none-straight','f-short-layered-none-ccurl','f-short-layered-none-wave','f-short-layered-seethrough-straight','f-short-layered-seethrough-ccurl','f-short-layered-seethrough-wave','f-short-layered-full-straight','f-short-layered-full-ccurl','f-short-layered-full-wave','f-short-layered-side-straight','f-short-layered-side-ccurl','f-short-layered-side-wave','f-medium-natural-none-straight','f-medium-natural-none-ccurl','f-medium-natural-none-wave','f-medium-natural-seethrough-straight','f-medium-natural-seethrough-ccurl','f-medium-natural-seethrough-wave','f-medium-natural-full-straight','f-medium-natural-full-ccurl','f-medium-natural-full-wave','f-medium-natural-side-straight','f-medium-natural-side-ccurl','f-medium-natural-side-wave','f-medium-layered-none-straight','f-medium-layered-none-ccurl','f-medium-layered-none-wave','f-medium-layered-none-hippie','f-medium-layered-seethrough-straight','f-medium-layered-seethrough-ccurl','f-medium-layered-seethrough-wave','f-medium-layered-seethrough-hippie','f-medium-layered-full-straight','f-medium-layered-full-ccurl','f-medium-layered-full-wave','f-medium-layered-full-hippie','f-medium-layered-side-straight','f-medium-layered-side-ccurl','f-medium-layered-side-wave','f-medium-layered-side-hippie','f-medium-hush-none-straight','f-medium-hush-none-ccurl','f-medium-hush-none-wave','f-medium-hush-seethrough-straight','f-medium-hush-seethrough-ccurl','f-medium-hush-seethrough-wave','f-medium-hush-side-straight','f-medium-hush-side-ccurl','f-medium-hush-side-wave','f-medium-hime-full-straight','f-long-natural-none-straight','f-long-natural-none-ccurl','f-long-natural-none-wave','f-long-natural-seethrough-straight','f-long-natural-seethrough-ccurl','f-long-natural-seethrough-wave','f-long-natural-full-straight','f-long-natural-full-ccurl','f-long-natural-full-wave','f-long-natural-side-straight','f-long-natural-side-ccurl','f-long-natural-side-wave','f-long-layered-none-straight','f-long-layered-none-ccurl','f-long-layered-none-wave','f-long-layered-none-hippie','f-long-layered-seethrough-straight','f-long-layered-seethrough-ccurl','f-long-layered-seethrough-wave','f-long-layered-seethrough-hippie','f-long-layered-full-straight','f-long-layered-full-ccurl','f-long-layered-full-wave','f-long-layered-full-hippie','f-long-layered-side-straight','f-long-layered-side-ccurl','f-long-layered-side-wave','f-long-layered-side-hippie','f-long-hush-none-straight','f-long-hush-none-ccurl','f-long-hush-none-wave','f-long-hush-seethrough-straight','f-long-hush-seethrough-ccurl','f-long-hush-seethrough-wave','f-long-hush-side-straight','f-long-hush-side-ccurl','f-long-hush-side-wave','f-long-hime-full-straight','m-short-natural-down-straight','m-short-natural-down-downperm','m-short-natural-down-shadow','m-short-natural-up-straight','m-short-natural-up-downperm','m-short-natural-up-shadow','m-short-twoblock-down-straight','m-short-twoblock-down-downperm','m-short-twoblock-down-shadow','m-short-twoblock-up-straight','m-short-twoblock-up-downperm','m-short-twoblock-up-shadow','m-medium-natural-down-straight','m-medium-natural-down-downperm','m-medium-natural-down-shadow','m-medium-natural-up-straight','m-medium-natural-up-downperm','m-medium-natural-up-shadow','m-medium-wolf-down-straight','m-medium-wolf-down-downperm','m-medium-wolf-down-shadow','m-medium-wolf-up-straight','m-medium-wolf-up-downperm','m-medium-wolf-up-shadow'],
  // 베이스 스타일: 여성 = 내추럴·앞머리 없음·스트레이트 / 남성 = 내추럴·다운·스트레이트 (가르마만 업 스타일)
  variants: [
    ...['f-short','f-medium','f-long','m-short','m-medium'].flatMap(p => {
      const base = p[0] === 'f' ? `${p}-natural-none-straight` : `${p}-natural-down-straight`;
      const v = [{ key: base, set: { volume: 'up' }, file: `${base}-vol` },
                 { key: base, set: { technique: 'highlight' }, file: `${base}-t-highlight` }];
      if (p[0] === 'f') v.push({ key: base, set: { technique: 'balayage' }, file: `${base}-t-balayage` });
      return v.concat(SHADES_IDS().map(id => ({ key: base, set: { color: id }, file: `${base}-c-${id}` })));
    }),
    // 가르마: 여성 베이스는 원래 옆가르마 → side는 베이스 이미지, center는 생성
    ...['short','medium','long'].flatMap(l => [
      { key: `f-${l}-natural-none-straight`, set: { parting: 'center' }, file: `f-${l}-natural-none-straight-part-center` },
      { key: `f-${l}-natural-none-straight`, set: { parting: 'side' }, file: `f-${l}-natural-none-straight` } ]),
    // 남성 숏 업 = 원래 옆으로 넘긴 스타일(side=베이스), 미디엄 업 = 원래 센터(center=베이스)
    { key: 'm-short-natural-up-straight', set: { parting: 'center' }, file: 'm-short-natural-up-straight-part-center' },
    { key: 'm-short-natural-up-straight', set: { parting: 'side' }, file: 'm-short-natural-up-straight' },
    { key: 'm-medium-natural-up-straight', set: { parting: 'center' }, file: 'm-medium-natural-up-straight' },
    { key: 'm-medium-natural-up-straight', set: { parting: 'side' }, file: 'm-medium-natural-up-straight-part-side' }
  ],
  groups: [
    { id:'shape', title:'형태', sub:'기장 · 커트 라인 · 볼륨', axes:['length','cut','volume'] },
    { id:'bangs', title:'앞머리', sub:'앞머리 · 가르마', axes:['bangs','parting'] },
    { id:'texture', title:'질감', sub:'컬 · 펌', axes:['curl'] },
    { id:'color', title:'컬러', sub:'살롱 염모제 공식 컬러 · 기법', axes:['color','technique'] }
  ],
  common: {
    volume: { label:'볼륨', values:[ {id:'normal', label:'기본'}, {id:'up', label:'볼륨업'} ]},
    parting: { label:'가르마', values:[ {id:'style', label:'스타일 기본'}, {id:'center', label:'센터 가르마'}, {id:'side', label:'옆 가르마'} ]},
    color: { label:'컬러', values:'COLORS' },
    technique: { label:'컬러 기법', values:[ {id:'whole', label:'기본 (없음)'}, {id:'highlight', label:'하이라이트'}, {id:'balayage', label:'발레아쥬'} ]}
  },
  axes: {
    female: {
      length: { label:'기장', image:true, values:[
        {id:'short', label:'단발 보브'}, {id:'medium', label:'미디엄'}, {id:'long', label:'롱'} ]},
      cut: { label:'커트 라인', image:true, values:[
        {id:'natural', label:'내추럴'}, {id:'layered', label:'레이어드'},
        {id:'hush', label:'허쉬컷'}, {id:'hime', label:'히메컷'} ]},
      bangs: { label:'앞머리', image:true, values:[
        {id:'none', label:'없음 (이마 오픈)'}, {id:'seethrough', label:'시스루뱅'},
        {id:'full', label:'풀뱅'}, {id:'side', label:'사이드뱅'} ]},
      curl: { label:'컬 · 펌', image:true, values:[
        {id:'straight', label:'스트레이트'}, {id:'ccurl', label:'C컬펌'},
        {id:'wave', label:'웨이브펌'}, {id:'hippie', label:'히피펌'} ]}
    },
    male: {
      length: { label:'기장', image:true, values:[ {id:'short', label:'숏'}, {id:'medium', label:'미디엄'} ]},
      cut: { label:'커트 라인', image:true, values:[
        {id:'natural', label:'내추럴'}, {id:'twoblock', label:'투블럭'}, {id:'wolf', label:'울프컷'} ]},
      bangs: { label:'앞머리', image:true, values:[ {id:'down', label:'다운 (내림)'}, {id:'up', label:'업 · 가르마'} ]},
      curl: { label:'컬 · 펌', image:true, values:[
        {id:'straight', label:'스트레이트'}, {id:'downperm', label:'다운펌'}, {id:'shadow', label:'쉐도우펌'} ]}
    }
  },
  // 살롱 전문가용 염모제 — 제품명·컬러 코드·공식 컬러명은 공식 자료에서 확인한 것만 사용
  brands: [
    { id:'addicthy', name:'Milbon Ordeve Addicthy', note:'밀본 오르디브 아딕시', source:'https://ordevebrand-digital.com/color/addicthy/standard-line' },
    { id:'illumina', name:'Wella Professionals Illumina Color', note:'웰라 일루미나 컬러', source:'https://www.wella.com/professional/m/pdf/MH0771-Illumina%20Intro%20Brochure.v2.pdf' },
    { id:'majirel', name:"L'Oréal Professionnel Majirel", note:'로레알 프로페셔널 마지렐', source:'https://in.lorealpartnershop.com/en/majirel-5.8---mocha-light-brown/IN8901526571864.html' }
  ],
  colors: [
    {id:'natural', label:'내추럴 (염색 안 함)'},
    {id:'ad-stopaz', brand:'addicthy', code:'9-S-Topaz', name:'Smoky Topaz', label:'9-S-Topaz'},
    {id:'ad-sapphire', brand:'addicthy', code:'7-Sapphire', name:'Sapphire', label:'7-Sapphire'},
    {id:'ad-silver', brand:'addicthy', code:'9-Silver', name:'Silver', label:'9-Silver'},
    {id:'ad-amethyst', brand:'addicthy', code:'7-Amethyst', name:'Amethyst', label:'7-Amethyst'},
    {id:'il-781', brand:'illumina', code:'7/81', name:'Medium Pearl Ash Blonde', label:'7/81'},
    {id:'il-57', brand:'illumina', code:'5/7', name:'Light Brunette Brown', label:'5/7'},
    {id:'il-743', brand:'illumina', code:'7/43', name:'Medium Red Gold Blonde', label:'7/43'},
    {id:'mj-58', brand:'majirel', code:'5.8', name:'Mocha Light Brown', label:'5.8', source:'https://in.lorealpartnershop.com/en/majirel-5.8---mocha-light-brown/IN8901526571864.html'},
    {id:'mj-634', brand:'majirel', code:'6.34', name:'Dark Gold Copper Blonde', label:'6.34', source:'https://in.lorealpartnershop.com/en/majirel-6.34---dark-gold-copper-blonde/IN8901526400560.html'}
  ]
};
function SHADES_IDS() { return ['ad-stopaz','ad-sapphire','ad-silver','ad-amethyst','il-781','il-57','il-743','mj-58','mj-634']; }
