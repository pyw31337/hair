# 렛츠헤어 개선 사항 (2026-10-28)

## 복구 방법
현재 시점의 원본은 다음 브랜치에 보존되어 있습니다:
- 브랜치: `backup/original-2026-10-28`
- 커밋 SHA: `57ea5440702f0884cd607f473fa9a2f58bfd3427`

복구하려면:
```bash
git checkout backup/original-2026-10-28
# 또는
git reset --hard 57ea5440702f0884cd607f473fa9a2f58bfd3427
```

## 적용된 개선
1. **보안 주석 추가**: 평문 비밀번호 위험성 명시, Cloud Functions 이전 권고
2. **동적 시술 목록**: 매장 설정의 `styles` / `services` 기반 체크박스 동적 렌더링
3. **시술별 가격·소요시간 데이터 모델 확장**:
   - `services: [{ name, price, duration }]` 구조 추가
   - 예약 폼에서 가격/소요시간 표시
   - 새 매장 생성 시 기본 services 포함
   - 기존 `styles` 배열과 하위 호환 유지
4. **관리자 로그인**: 클라이언트 측 인증의 한계를 주석으로 명시

## 추가 권장 사항 (P0/P1)
- Firestore Security Rules 설정
- 관리자 비밀번호 해시화 + Cloud Functions로 인증 이전
- 예약 생성 시 duration 기반 시간 블록 확보 (중복 방지 강화)
- 카카오 알림톡 또는 SMS 연동
- 관리자 화면에서 시술 가격/시간 편집 UI

자세한 내용은 이전 분석 참고.
