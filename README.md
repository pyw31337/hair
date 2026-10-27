# J.Hair Shop Reservation System (제이헤어 시술예약 시스템)

> **실시간 호스팅 서비스:** [http://pyw31337.dothome.co.kr/reservation/jhair/](http://pyw31337.dothome.co.kr/reservation/jhair/)  
> **GitHub Pages 인터랙티브 데모:** [https://pyw31337.github.io/jhair/](https://pyw31337.github.io/jhair/)  
> 구리시 수택동 1인 미용실 **[제이헤어]**를 위해 설계된 실시간 시술 예약·취소 및 매장 관리 시스템입니다.

---

## 🌟 주요 기능

1. **실시간 캘린더 2-Way 뷰 모드**
   - **날짜별 보기**: 미니 달력에서 원하는 일자를 터치하면 하단 슬라이드 패널로 해당 일자의 1시간 단위(12:00 ~ 20:00) 예약 가능/마감 현황 표시
   - **한번에 보기**: 월간 전체 달력에 모든 시간대별 예약 상태를 한눈에 조망
2. **고객 예약 프로세스**
   - 예약자명, 연락처, 시술 항목(커트, 염색, 파마, 기타 복수 선택), 요청사항
   - 3D 플립 카드 UI 및 시술 시 10% 결제 할인 혜택 안내
   - 실시간 카운트다운 타이머 연동
   - 중복 예약 방지 (Race Condition 방지)
3. **간편한 예약 취소 프로세스**
   - 본인 휴대폰 번호 뒷자리 4자리 간편 인증으로 즉시 예약 취소
4. **관리자 모드 (`admin.php`)**
   - 세션 기반 관리자 인증
   - 월별 누적 예약 총계 및 시술별(커트/염색/파마/기타) 실시간 통계 산출
   - 전체 예약 조회 및 관리자 직권 취소
   - 특정 일자 매장 임시 휴무 설정/해제
   - 상단 공지사항 즉시 변경
5. **예약 알림 이메일 자동 발송**
   - 고객 예약 완료 시 관리자 이메일로 예약 상세 내역 및 직통 전화 링크 HTML 메일 즉시 발송

---

## 🛡️ 코드 분석 및 주요 개선 내역

| 분류 | 기존 문제점 | 개선 및 해결책 |
| :--- | :--- | :--- |
| **보안 (Security)** | `send.php`, `admin.php` 등에 SQL 쿼리 문자열 직접 연결로 **SQL Injection** 취약점 노출 | `mysqli_prepare` **Prepared Statement** 전면 도입으로 악의적 입력 완전 차단 |
| **보안 (Credentials)** | `dbconn.php` 및 `admin.php`에 DB 패스워드와 관리자 암호 하드코딩 | `config.sample.php` 템플릿 도입 및 `config.php` 분리, `.gitignore` 등록으로 민감정보 유출 차단 |
| **보안 (XSS)** | 사용자 입력값 미이스케이프 | `htmlspecialchars` 적용 및 HTML 메일 인코딩 보강 |
| **안정성 (Race Condition)** | 동일 시간대 동시 클릭 시 이중 예약 위험 | 예약 전 활성 예약 존재 여부를 검증하는 쿼리 및 트랜잭션 안전성 추가 |
| **버그 (Logic)** | `script_backdrop.php`에서 `$style_num` 변수 미정의로 취소 팝업 시술 태그 누락 | `$style_num` 정수 플래그 연산 로직 추가로 정상 동작 복구 |
| **버그 (오타)** | `alert('예약취소이 취소 되었습니다.');` 등 오타 | `alert('예약이 정상적으로 취소되었습니다.');` 등 사용자 경험 정돈 |
| **PHP 8+ 호환성** | `$_REQUEST[date]` 등 따옴표 없는 배열 키로 인해 최신 PHP 버전에서 Fatal/Notice 발생 위험 | 모든 배열 키에 따옴표(`$_REQUEST['date']`) 적용 및 `<?` 단축 태그를 `<?php`로 표준화 |
| **배포 지원** | PHP 미지원 정적 호스팅(GitHub Pages)에서 체험 불가 | `LocalStorage` 기반의 풀 인터랙티브 클라이언트 데모 엔진(`index.html`) 탑재 |

---

## 📁 프로젝트 구조

```bash
jhair/
├── index.html               # GitHub Pages용 인터랙티브 클라이언트 데모
├── index.php                # 메인 캘린더 및 예약 화면 (PHP 호스팅용)
├── admin.php                # 관리자 대시보드 및 통계 (PHP 호스팅용)
├── config.sample.php        # DB 및 관리자 설정 템플릿 (버전 관리 포함)
├── config.php               # 실제 환경설정 파일 (git-ignored)
├── dbconn.php               # DB 연결 모듈 (Prepared Statement 지원)
├── schema.sql               # MySQL 테이블 스키마 DDL
├── send.php                 # 예약 생성 및 고객 취소 API
├── send_admin.php           # 관리자 대리 예약 / 취소 / 휴무 설정 API
├── send_notice.php          # 공지사항 업데이트 API
├── script_backdrop.php      # 일자별 예약 현황 비동기 API
├── script_backdrop_admin.php# 관리자 일자별 예약 현황 비동기 API
├── email.php                # 예약 알림 HTML 메일 발송 모듈
├── css/                     # 스타일시트 (common.css, checkbox.css 등)
├── image/                   # 매장 및 헤어 갤러리 이미지
├── icon/                    # 인터페이스 아이콘
└── favicon/                 # PWA 및 브라우저 파비콘
```

---

## 🚀 설치 및 실행 가이드

### 1. PHP 호스팅 서버 배포 (Dothome, Cafe24, AWS 등)
1. MySQL 데이터베이스에 `schema.sql`을 임포트합니다.
   ```bash
   mysql -u [사용자] -p [DB이름] < schema.sql
   ```
2. `config.sample.php`를 복사하여 `config.php`를 생성하고 DB 접속 정보 및 관리자 패스워드를 입력합니다.
   ```bash
   cp config.sample.php config.php
   vi config.php
   ```
3. 웹 서버(Document Root)에 파일들을 업로드합니다.

### 2. GitHub Pages 데모 배포
- 본 저장소의 `main` 브랜치는 정적 `index.html`을 포함하고 있어 GitHub Pages 활성화 시 별도 빌드 없이 즉시 브라우저에서 인터랙티브 데모로 동작합니다.
- [GitHub Pages 데모 확인](https://pyw31337.github.io/jhair/)

---

## 📄 라이선스
Copyright © 2024 J.Hairshop & pyw31337. All Rights Reserved.
