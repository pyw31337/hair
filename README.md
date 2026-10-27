# 렛츠헤어 (Let's Hair) | 실시간 미용실 예약 & 멀티 테넌트 SaaS

> **공식 서비스 URL:** [https://pyw31337.github.io/hair/](https://pyw31337.github.io/hair/)  
> **대표 레퍼런스 매장 (제이헤어):** [https://pyw31337.github.io/hair/?shop=jhair](https://pyw31337.github.io/hair/?shop=jhair)  
> 링크 하나로 회원가입이나 앱 설치 없이 10초 만에 예약하고, 아이디 발급만으로 누구나 무료 매장 예약 시스템을 개설하는 **1인 미용실 & 뷰티숍 전용 실시간 예약 솔루션 (SaaS)**입니다.

---

## 🌟 주요 특징 및 기능

### 1. 💈 아이디 기반 멀티 테넌트 (Multi-Tenant SaaS)
- **URL 파라미터 기반 매장 분리**: `https://pyw31337.github.io/hair/?shop={shopId}`
- **신규 매장 즉시 무료 개설**: 상단 `+ 새 매장 개설` 버튼을 통해 매장 아이디, 상호명, 전화번호, 관리자 비밀번호를 입력하면 즉시 독립된 예약 시스템 발급.
- 매장별 고유 설정: 상호명, 영업시간, 정기 휴무일 규칙, 시술 항목, 공지사항, 관리자 비밀번호 독립 운영.

### 2. ⚡ Firebase Cloud Firestore 실시간 양방향 동기화
- **실시간 중복 예약 원천 차단 (`onSnapshot`)**: A 고객이 15시를 예약하면, 접속 중인 모든 손님의 화면에서 새로고침 없이 즉시 `[예약마감]`으로 전환.
- **Race Condition 방어**: 동일 시간대 동시 클릭 시 충돌 검증 및 사전 안내.
- **무서버(Serverless) 평생 무료 운영**: 별도의 유료 웹호스팅 없이 GitHub Pages와 Firebase 무료 Spark 요금제만으로 100% 무중단 서비스.

### 3. 📅 직관적인 2-Way 캘린더 인터페이스
- **날짜별 보기**: 미니 달력에서 원하는 일자를 선택하면 하단 슬라이드 패널로 시간대별 예약 현황 출력.
- **한번에 보기**: 월간 달력 전체에 1시간 단위 슬롯 현황을 한눈에 조망.
- **3D 플립 카드 UI**: 예약 진행 시 3D 카드 애니메이션과 함께 인터넷 예약 10% 결제 할인 혜택 안내.

### 4. 👑 원장님 전용 관리자 모드
- **원클릭 관리자 인증**: 상단 메뉴 ➔ 관리자 로그인
- **월간 실시간 통계**: 이번 달 총 예약 건수 및 시술별(커트/염색/파마/기타) 실시간 집계.
- **고객 연락처 확인 및 직통 전화(📞) 연동**.
- **원클릭 임시 휴무 지정/해제**: 특정 일자를 터치 한 번으로 전체 마감 처리.
- **상단 공지사항 즉시 수정 및 실시간 반영**.

### 5. 🔒 간편한 고객 예약 취소
- 예약한 시간대를 터치하고 본인 **휴대폰 번호 뒷자리 4자리**만 입력하면 즉시 취소 처리 및 슬롯 자동 복구.

---

## 📁 저장소 구조

```bash
jhair/
├── index.html               # Firebase Firestore 기반 멀티 테넌트 실시간 예약 SaaS (GitHub Pages)
├── index.php                # PHP/MySQL 기존 레거시 호스팅 버전
├── admin.php                # PHP 관리자 대시보드
├── config.sample.php        # PHP 환경설정 템플릿
├── dbconn.php               # PHP DB 접속 모듈 (Prepared Statements 적용)
├── schema.sql               # MySQL 데이터베이스 스키마
├── send.php                 # PHP 예약 API
├── css/                     # common.css, checkbox.css 등
├── image/                   # 매장 및 헤어 갤러리 이미지
├── icon/                    # SVG 및 인터페이스 아이콘
└── .github/workflows/       # GitHub Pages 자동 배포 CI/CD
```

---

## 🚀 기술 스택
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3 Grid/Flexbox, jQuery, PWA
- **Database & Realtime**: Firebase Cloud Firestore
- **Deployment**: GitHub Pages, GitHub Actions CI/CD
- **Share**: Kakao JavaScript SDK, Web Share API

---

## 📄 라이선스
Copyright © 2024 J.Hairshop & Let's Hair by pyw31337. All Rights Reserved.
