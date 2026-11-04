# Let's Hair · 헤어 시뮬레이터
독립 정적 앱. GitHub Pages에서 `/hair/catalog/` 로 배포됩니다. 기존 사이트 파일은 건드리지 않습니다.

## 구성
- `data.js` 옵션 체계(그룹 4개 · 축 · 값) + `available`(실제 렌더가 있는 조합 124개)
- `img/` 프리뷰 매트릭스 `{f|m}-{length}-{cut}-{bangs}-{curl}.jpg` + 머리카락 마스크 `*-mask.png` + 인물(전경) 마스크 `*-fg.png`
- `tools/build_masks.py` 원본 렌더 → 600x800 리사이즈 + MediaPipe selfie_multiclass로 hair/전경 마스크 추출

## 옵션
| 그룹 | 여성 | 남성 | 방식 |
|---|---|---|---|
| 형태 | 기장(보브·미디엄·롱), 커트(내추럴·레이어드·허쉬·히메), 볼륨(보통·볼륨업) | 기장(숏·미디엄), 커트(내추럴·투블럭·울프), 볼륨 | 기장·커트 = 이미지, 볼륨 = 마스크로 머리 레이어 확대 |
| 앞머리 | 없음·시스루·풀뱅·사이드뱅, 가르마 좌/우 | 다운·업, 가르마 좌/우 | 앞머리 = 이미지, 가르마 = 좌우 반전 |
| 질감 | 스트레이트·C컬·웨이브·히피 | 스트레이트·다운펌·쉐도우펌 | 이미지 |
| 컬러 | 7색 × 전체/하이라이트/발레아쥬 + 강도 | 동일 | hair 마스크 기반 캔버스 염색 |

## 조합 규칙 (비현실적 조합 제외)
- 여성: 보브는 내추럴/레이어드만, 히피펌 없음 · 히피펌은 레이어드만 · 허쉬컷은 풀뱅/히피 불가 · 히메컷은 미디엄/롱 + 풀뱅 + 스트레이트만
- 남성: 숏 = 내추럴/투블럭, 미디엄 = 내추럴/울프
- 불가능한 조합을 고르면 방금 고른 값은 유지하고 나머지 축을 최소 변경해 자동 조정 + 토스트 안내 (썸네일에 `자동 조정` 배지)

## 이미지 추가 방법
1. 같은 모델·구도로 새 조합 렌더 → `raw/{g}-{length}-{cut}-{bangs}-{curl}.jpg`
2. `python tools/build_masks.py raw img selfie_multiclass_256x256.tflite`
3. `data.js`의 `available`에 키 추가 (새 값이면 해당 축 `values`에도 추가)

## 이미지 방식 (v3: 모든 옵션 = 실제 생성 이미지)
CSS/JS 효과(틴트·그라데이션 오버레이·볼륨 확대·좌우 반전)는 모두 제거했습니다. 화면에 보이는 것은 항상 `img/` 안의 실제 생성 이미지 한 장입니다.

- 스타일 124장: 성별 × 기장 × 커트 × 앞머리 × 컬 중 실제로 가능한 조합
- 컬러 45장: 기본 스타일 5종(여 숏·미디엄·롱 / 남 숏·미디엄) × 살롱 컬러 9종 (`-c-<id>`)
- 기법 8장: 하이라이트 5, 발레아쥬 3(여성만) (`-t-highlight`, `-t-balayage`)
- 볼륨업 5장 (`-vol`), 가르마 5장 (`-part-center`, `-part-side`). 원래 가르마인 쪽은 베이스 이미지를 그대로 씀
- 합계 187장 (600×800 JPEG)

### 트레이드오프
모든 옵션 값에는 실제 이미지가 있지만 **모든 교차 조합**까지 있지는 않습니다. 124 스타일 × 10 컬러 × 3 기법 × 2 볼륨 × 3 가르마면 2만 장이 넘기 때문입니다. 볼륨·가르마·컬러·기법 변형은 기본 스타일에서만 만들었고, 한 번에 하나만 기본값이 아닐 수 있습니다. 이미지가 없는 조합을 고르면 방금 고른 값은 그대로 두고, 가중치 비용(기장 8, 컬 4, 컬러 3, 기법 3, 앞머리 2, 볼륨 2, 가르마 2, 커트 1)이 가장 낮은 실제 이미지로 자동 조정합니다. 이때 토스트와 칩에 "자동 조정"이 표시됩니다. 해당 성별에 이미지가 하나도 없는 값(예: 남성 발레아쥬)은 숨깁니다.

## 살롱 염모제 (제품명 · 공식 컬러 코드/이름)
| 브랜드 / 제품 | 코드 | 공식 컬러명 |
|---|---|---|
| Milbon Ordeve Addicthy | 9-S-Topaz | Smoky Topaz |
| Milbon Ordeve Addicthy | 7-Sapphire | Sapphire |
| Milbon Ordeve Addicthy | 9-Silver | Silver |
| Milbon Ordeve Addicthy | 7-Amethyst | Amethyst |
| Wella Professionals Illumina Color | 7/81 | Medium Pearl Ash Blonde |
| Wella Professionals Illumina Color | 5/7 | Light Brunette Brown |
| Wella Professionals Illumina Color | 7/43 | Medium Red Gold Blonde |
| L'Oréal Professionnel Majirel | 5.8 | Mocha Light Brown |
| L'Oréal Professionnel Majirel | 6.34 | Dark Gold Copper Blonde |

출처
- Addicthy 공식 컬러 차트: https://ordevebrand-digital.com/color/addicthy/standard-line · 인기 컬러: https://fyb.milbon.co.jp/addicthy-color/
- Illumina 공식 브로셔: https://www.wella.com/professional/m/pdf/MH0771-Illumina%20Intro%20Brochure.v2.pdf
- Majirel 5.8: https://in.lorealpartnershop.com/en/majirel-5.8---mocha-light-brown/IN8901526571864.html · 6.34: https://in.lorealpartnershop.com/en/majirel-6.34---dark-gold-copper-blonde/IN8901526400560.html
- 국내 시장: 이투데이(아모스 약 52%, 웰라 재진출) https://www.etoday.co.kr/news/view/2576811 · 코스인코리아(밀본 브랜드평판 1위) https://www.cosinkorea.com/news/article.html?no=42626

색은 생성 이미지로 근사한 것이라 실제 시술 결과와 다를 수 있습니다. 아모스(국내 점유율 1위)는 공식 컬러 차트를 확인하지 못해 아직 넣지 않았습니다.

### 재생성
`python tools/build_images.py <원본 폴더> img`: 리사이즈만 하며 마스크나 합성은 없습니다.
