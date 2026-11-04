/* 옵션 데이터. image:true = 실제 매트릭스 이미지가 있는 축, placeholder:true = 이미지 준비중(가까운 결과로 대체) */
window.CATALOG = {
  imageKey: { female: ['length','bangs','curl'], male: ['length','bangs'] },
  groups: [
    { id:'shape', title:'형태', sub:'기장 · 커트 라인', axes:['length','cut'] },
    { id:'bangs', title:'앞머리', sub:'앞머리 · 가르마', axes:['bangs'] },
    { id:'texture', title:'질감', sub:'컬 · 펌', axes:['curl'] },
    { id:'color', title:'컬러', sub:'톤 · 강도', axes:['color'] }
  ],
  axes: {
    female: {
      length: { label:'기장', image:true, values:[
        {id:'short', label:'단발 보브'}, {id:'medium', label:'미디엄'}, {id:'long', label:'롱'} ]},
      cut: { label:'커트 라인', values:[
        {id:'natural', label:'내추럴'}, {id:'layered', label:'레이어드', placeholder:true},
        {id:'hush', label:'허쉬컷', placeholder:true}, {id:'hime', label:'히메컷', placeholder:true} ]},
      bangs: { label:'앞머리', image:true, values:[
        {id:'none', label:'없음 (이마 오픈)'}, {id:'seethrough', label:'시스루뱅'},
        {id:'full', label:'풀뱅', placeholder:true, fallback:'seethrough'},
        {id:'side', label:'사이드뱅', placeholder:true, fallback:'none'} ]},
      curl: { label:'컬 · 펌', image:true, values:[
        {id:'straight', label:'스트레이트'}, {id:'wave', label:'웨이브펌'},
        {id:'ccurl', label:'C컬펌', placeholder:true, fallback:'straight'},
        {id:'hippie', label:'히피펌', placeholder:true, fallback:'wave'} ]},
      color: { label:'컬러', values: 'COLORS' }
    },
    male: {
      length: { label:'기장', image:true, values:[ {id:'short', label:'숏'}, {id:'medium', label:'미디엄'} ]},
      cut: { label:'커트 라인', values:[
        {id:'natural', label:'내추럴'}, {id:'twoblock', label:'투블럭', placeholder:true}, {id:'wolf', label:'울프컷', placeholder:true} ]},
      bangs: { label:'앞머리', image:true, values:[ {id:'down', label:'다운 (내림)'}, {id:'up', label:'업 · 가르마'} ]},
      curl: { label:'컬 · 펌', values:[
        {id:'straight', label:'스트레이트'}, {id:'down', label:'다운펌', placeholder:true}, {id:'shadow', label:'쉐도우펌', placeholder:true} ]},
      color: { label:'컬러', values: 'COLORS' }
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
