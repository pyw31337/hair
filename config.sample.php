<?php
/**
 * J.Hair Shop Reservation System Configuration Template
 * 
 * 복사하여 config.php로 이름을 변경한 뒤 서버 환경에 맞게 수정하세요.
 * config.php는 .gitignore에 등록되어 버전 관리에 노출되지 않습니다.
 */

// 데이터베이스 접속 정보
define('DB_SERVER', 'localhost');
define('DB_USER', 'your_db_user');
define('DB_PASSWORD', 'your_db_password');
define('DB_DATABASE', 'your_db_name');
define('DB_PORT', 3306);
define('DB_CHARSET', 'utf8mb4');

// 관리자 계정 설정
define('ADMIN_PASSWORD', 'your_admin_password');

// 알림 이메일 설정
define('MAIL_RECIPIENT', 'admin@example.com');
define('MAIL_FROM', 'reservation@jhairs.com');
define('SITE_URL', 'http://pyw31337.dothome.co.kr/reservation/jhair/');

// 시간대 설정
date_default_timezone_set('Asia/Seoul');
