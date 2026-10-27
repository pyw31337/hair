<?php
header('Content-Type: text/html; charset=utf-8');

session_start();
require_once('dbconn.php');

// 관리자 세션 체크
if (!isset($_SESSION['apw']) || $_SESSION['apw'] !== ADMIN_PASSWORD) {
    echo "<script>alert('관리자 권한이 없습니다.'); location.href='admin.php';</script>";
    exit;
}

$notice = isset($_POST['anotice']) ? trim($_POST['anotice']) : '';

$update_query = "UPDATE `jhair` SET comment = ? WHERE id = 1";
$stmt = mysqli_prepare($conn, $update_query);
mysqli_stmt_bind_param($stmt, "s", $notice);
mysqli_stmt_execute($stmt);
mysqli_stmt_close($stmt);

mysqli_close($conn);

echo "<script>alert('공지사항이 성공적으로 등록되었습니다.'); location.href='admin.php';</script>";
