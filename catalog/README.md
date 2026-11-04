# Let's Hair · 헤어 시뮬레이터 (Phase 1)
독립 정적 앱. GitHub Pages에서 `/hair/catalog/` 로 배포됩니다. 기존 사이트 파일은 건드리지 않습니다.
- `data.js` 옵션 체계(그룹 4개 · 축 · 값). `placeholder:true` 값은 이미지 준비중 → `fallback` 이미지 표시
- `img/` 프리뷰 매트릭스(`f-{length}-{bangs}-{curl}.jpg`, `m-{length}-{bangs}.jpg`) + 머리카락 마스크(`*-mask.png`)
- `tools/build_masks.py` 원본 렌더 → 600x800 리사이즈 + MediaPipe hair 마스크 추출
## 이미지 추가 방법
1. 같은 모델·구도로 새 조합 렌더 (예: `f-medium-full-straight`)
2. `build_masks.py` 실행 → `img/`에 결과 저장
3. `data.js`에서 해당 값의 `placeholder`/`fallback` 제거 (새 축이면 `imageKey`에 추가)
