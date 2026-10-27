<?php
header('Content-Type: text/html; charset=utf-8');

session_start();
require_once('dbconn.php');

// 관리자 세션 검증
if (!isset($_SESSION['apw']) || $_SESSION['apw'] !== ADMIN_PASSWORD) {
    echo "<script>alert('관리자 로그인이 필요합니다.'); location.href='admin.php';</script>";
    exit;
}

$rname = isset($_POST['rname']) ? trim($_POST['rname']) : '';
$rtel = isset($_POST['rtel']) ? trim($_POST['rtel']) : '';
$rstyle = isset($_POST['rstyle']) && is_array($_POST['rstyle']) ? $_POST['rstyle'] : [];
$rcomment = isset($_POST['rcomment']) ? trim($_POST['rcomment']) : '';

$rid = isset($_POST['rid']) ? trim($_POST['rid']) : '';
$rpw = isset($_POST['rpw']) ? trim($_POST['rpw']) : '';

$cdate1 = isset($_POST['cdate1']) ? trim($_POST['cdate1']) : '';
$cdate2 = isset($_POST['cdate2']) ? trim($_POST['cdate2']) : '';
$cyoil = isset($_POST['cyoil']) ? trim($_POST['cyoil']) : '';

$ddate = isset($_POST['ddate']) ? trim($_POST['ddate']) : '';

$wdate = date("Y-m-d");
$wtime = date("H:i:s");
$wip = isset($_SERVER["REMOTE_ADDR"]) ? $_SERVER["REMOTE_ADDR"] : '';

$hstyle = trim(implode(' ', array_map('trim', $rstyle)));

$holidate = isset($_REQUEST['holidate']) ? trim($_REQUEST['holidate']) : '';
$method = isset($_REQUEST['method']) ? trim($_REQUEST['method']) : '';
$hid = isset($_REQUEST['hid']) ? trim($_REQUEST['hid']) : '';

if ($rcomment === '') {
    $rcomment = '-';
}

if ($holidate !== '' && $method !== '') {
    // -------------------------------------------------------------
    // [1] 매장 임시 휴무 설정 / 해제
    // -------------------------------------------------------------
    if ($method === 'set') {
        $insert_query = "INSERT INTO `jhair` (`reserve_date`, `write_date`, `write_time`, `write_ip`, `holiday`, `trash`) VALUES (?, ?, ?, ?, 1, 0)";
        $stmt = mysqli_prepare($conn, $insert_query);
        mysqli_stmt_bind_param($stmt, "ssss", $holidate, $wdate, $wtime, $wip);
        mysqli_stmt_execute($stmt);
        mysqli_stmt_close($stmt);
    } else if ($method === 'cancel' && !empty($hid)) {
        $delete_query = "DELETE FROM `jhair` WHERE id = ? AND holiday = 1";
        $stmt = mysqli_prepare($conn, $delete_query);
        mysqli_stmt_bind_param($stmt, "i", $hid);
        mysqli_stmt_execute($stmt);
        mysqli_stmt_close($stmt);
    }

    mysqli_close($conn);
    exit;
}

if ($rid === '' && $holidate === '') {
    // -------------------------------------------------------------
    // [2] 관리자 대리 예약 등록
    // -------------------------------------------------------------
    if (empty($rname) || empty($rtel) || empty($cdate1) || empty($cdate2)) {
        echo "<script>alert('필수 입력 항목(이름, 연락처, 예약일시)이 누락되었습니다.'); window.history.back();</script>";
        exit;
    }

    $insert_query = "INSERT INTO `jhair` (`name`, `tel`, `style`, `comment`, `reserve_date`, `reserve_time`, `write_date`, `write_time`, `write_ip`, `trash`, `holiday`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)";
    $stmt = mysqli_prepare($conn, $insert_query);
    mysqli_stmt_bind_param($stmt, "sssssssss", $rname, $rtel, $hstyle, $rcomment, $cdate1, $cdate2, $wdate, $wtime, $wip);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_close($stmt);

    @include('email.php');
    mysqli_close($conn);

    $redir_year = substr($cdate1, 0, 4);
    $redir_month = substr($cdate1, 5, 2);
    echo "<script>alert('예약이 성공적으로 등록되었습니다.'); location.href='admin.php?year=" . urlencode($redir_year) . "&month=" . urlencode($redir_month) . "&date=" . urlencode($cdate1) . "&time=" . urlencode($cdate2) . "';</script>";
    exit;

} else if (!empty($rid)) {
    // -------------------------------------------------------------
    // [3] 관리자 직권 예약 취소
    // -------------------------------------------------------------
    $update_query = "UPDATE `jhair` SET trash = 1 WHERE id = ?";
    $stmt = mysqli_prepare($conn, $update_query);
    mysqli_stmt_bind_param($stmt, "i", $rid);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_close($stmt);

    mysqli_close($conn);

    $redir_year = substr($ddate, 0, 4);
    $redir_month = substr($ddate, 5, 2);
    echo "<script>alert('예약이 취소되었습니다.'); location.href='admin.php?year=" . urlencode($redir_year) . "&month=" . urlencode($redir_month) . "&view=all';</script>";
    exit;
}
