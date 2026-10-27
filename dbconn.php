<?php
/**
 * Database Connection Module
 */

$config_file = __DIR__ . '/config.php';
if (!file_exists($config_file)) {
    die("환경 설정 파일(config.php)이 존재하지 않습니다. config.sample.php를 복사하여 생성해 주세요.");
}

require_once($config_file);

// DB 연결
$conn = mysqli_init();
if (!$conn) {
    die("mysqli_init 초기화 실패");
}

$conn->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);

$connected = @mysqli_real_connect(
    $conn,
    DB_SERVER,
    DB_USER,
    DB_PASSWORD,
    DB_DATABASE,
    defined('DB_PORT') ? DB_PORT : 3306
);

if (!$connected) {
    die("데이터베이스 연결 실패: " . mysqli_connect_error());
}

$conn->set_charset(defined('DB_CHARSET') ? DB_CHARSET : "utf8mb4");
