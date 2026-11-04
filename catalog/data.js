/* 옵션 데이터.
 * image:true 축은 실제 렌더 이미지 키(img/{g}-{length}-{cut}-{bangs}-{curl}.jpg)를 구성한다.
 * available = 실제 존재하는 조합 목록. 불가능한 조합을 고르면 가장 가까운 유효 조합으로 자동 조정된다.
 * 볼륨/가르마/컬러 기법은 캔버스 효과(마스크 기반)로 실시간 미리보기. */
window.CATALOG = {
  imageKey: ['length','cut','bangs','curl'],
  available: ['f-short-natural-none-straight','f-short-natural-none-ccurl','f-short-natural-none-wave','f-short-natural-seethrough-straight','f-short-natural-seethrough-ccurl','f-short-natural-seethrough-wave','f-short-natural-full-straight','f-short-natural-full-ccurl','f-short-natural-full-wave','f-short-natural-side-straight','f-short-natural-side-ccurl','f-short-natural-side-wave','f-short-layered-none-straight','f-short-layered-none-ccurl','f-short-layered-none-wave','f-short-layered-seethrough-straight','f-short-layered-seethrough-ccurl','f-short-layered-seethrough-wave','f-short-layered-full-straight','f-short-layered-full-ccurl','f-short-layered-full-wave','f-short-layered-side-straight','f-short-layered-side-ccurl','f-short-layered-side-wave','f-medium-natural-none-straight','f-medium-natural-none-ccurl','f-medium-natural-none-wave','f-medium-natural-seethrough-straight','f-medium-natural-seethrough-ccurl','f-medium-natural-seethrough-wave','f-medium-natural-full-straight','f-medium-natural-full-ccurl','f-medium-natural-full-wave','f-medium-natural-side-straight','f-medium-natural-side-ccurl','f-medium-natural-side-wave','f-medium-layered-none-straight','f-medium-layered-none-ccurl','f-medium-layered-none-wave','f-medium-layered-none-hippie','f-medium-layered-seethrough-straight','f-medium-layered-seethrough-ccurl','f-medium-layered-seethrough-wave','f-medium-layered-seethrough-hippie','f-medium-layered-full-straight','f-medium-layered-full-ccurl','f-medium-layered-full-wave','f-medium-layered-full-hippie','f-medium-layered-side-straight','f-medium-layered-side-ccurl','f-medium-layered-side-wave','f-medium-layered-side-hippie','f-medium-hush-none-straight','f-medium-hush-none-ccurl','f-medium-hush-none-wave','f-medium-hush-seethrough-straight','f-medium-hush-seethrough-ccurl','f-medium-hush-seethrough-wave','f-medium-hush-side-straight','f-medium-hush-side-ccurl','f-medium-hush-side-wave','f-medium-hime-full-straight','f-long-natural-none-straight','f-long-natural-none-ccurl','f-long-natural-none-wave','f-long-natural-seethrough-straight','f-long-natural-seethrough-ccurl','f-long-natural-seethrough-wave','f-long-natural-full-straight','f-long-natural-full-ccurl','f-long-natural-full-wave','f-long-natural-side-straight','f-long-natural-side-ccurl','f-long-natural-side-wave','f-long-layered-none-straight','f-long-layered-none-ccurl','f-long-layered-none-wave','f-long-layered-none-hippie','f-long-layered-seethrough-straight','f-long-layered-seethrough-ccurl','f-long-layered-seethrough-wave','f-long-layered-seethrough-hippie','f-long-layered-full-straight','f-long-layered-full-ccurl','f-long-layered-full-wave','f-long-layered-full-hippie','f-long-layered-side-straight','f-long-layered-side-ccurl','f-long-layered-side-wave','f-long-layered-side-hippie','f-long-hush-none-straight','f-long-hush-none-ccurl','f-long-hush-none-wave','f-long-hush-seethrough-straight','f-long-hush-seethrough-ccurl','f-long-hush-seethrough-wave','f-long-hush-side-straight','f-long-hush-side-ccurl','f-long-hush-side-wave','f-long-hime-full-straight','m-short-natural-down-straight','m-short-natural-down-downperm','m-short-natural-down-shadow','m-short-natural-up-straight','m-short-natural-up-downperm','m-short-natural-up-shadow','m-short-twoblock-down-straight','m-short-twoblock-down-downperm','m-short-twoblock-down-shadow','m-short-twoblock-up-straight','m-short-twoblock-up-downperm','m-short-twoblock-up-shadow','m-medium-natural-down-straight','m-medium-natural-down-downperm','m-medium-natural-down-shadow','m-medium-natural-up-straight','m-medium-natural-up-downperm','m-medium-natural-up-shadow','m-medium-wolf-down-straight','m-medium-wolf-down-downperm','m-medium-wolf-down-shadow','m-medium-wolf-up-straight','m-medium-wolf-up-downperm','m-medium-wolf-up-shadow'],
  groups: [
    { id:'shape', title:'형태', sub:'기장 · 커트 라인 · 볼륨', axes:['length','cut','volume'] },
    { id:'bangs', title:'앞머리', sub:'앞머리 · 가르마', axes:['bangs','parting'] },
    { id:'texture', title:'질감', sub:'컬 · 펌', axes:['curl'] },
    { id:'color', title:'컬러', sub:'톤 · 기법 · 강도', axes:['color','technique'] }
  ],
  common: {
    volume: { label:'볼륨', values:[ {id:'normal', label:'보통'}, {id:'up', label:'볼륨업'} ]},
    parting: { label:'가르마 방향', values:[ {id:'left', label:'왼쪽'}, {id:'right', label:'오른쪽'} ]},
    color: { label:'컬러', values:'COLORS' },
    technique: { label:'컬러 기법', values:[ {id:'whole', label:'전체 염색'}, {id:'highlight', label:'하이라이트'}, {id:'balayage', label:'발레아쥬'} ]}
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
  colors: [
    {id:'natural', label:'내추럴', hex:null},
    {id:'black', label:'블루 블랙', hex:'#1b2233'},
    {id:'choco', label:'초코 브라운', hex:'#5a3826'},
    {id:'ash', label:'애쉬 베이지', hex:'#a8977f'},
    {id:'copper', label:'코퍼 오렌지', hex:'#b5532a'},
    {id:'rose', label:'로즈 브라운', hex:'#93505d'},
    {id:'milk', label:'밀크 브라운', hex:'#b88a62'}
  ]
};
