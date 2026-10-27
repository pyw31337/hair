<?php
header('Content-Type: text/html; charset=utf-8');

require_once('dbconn.php');

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

if ($rcomment === '') {
    $rcomment = '-';
}

if ($rpw === '' && $rid === '') {
    // -------------------------------------------------------------
    // [1] 신규 예약 등록
    // -------------------------------------------------------------
    if (empty($rname) || empty($rtel) || empty($cdate1) || empty($cdate2)) {
        echo "<script>alert('필수 입력 항목(이름, 연락처, 예약일시)이 누락되었습니다.'); window.history.back();</script>";
        exit;
    }

    // 중복 예약 방지 검사 (동일 날짜 및 시간에 활성 예약이 이미 존재하는지 확인)
    $check_query = "SELECT id FROM `jhair` WHERE reserve_date = ? AND reserve_time = ? AND trash = 0 LIMIT 1";
    $stmt_check = mysqli_prepare($conn, $check_query);
    mysqli_stmt_bind_param($stmt_check, "ss", $cdate1, $cdate2);
    mysqli_stmt_execute($stmt_check);
    mysqli_stmt_store_result($stmt_check);

    if (mysqli_stmt_num_rows($stmt_check) > 0) {
        mysqli_stmt_close($stmt_check);
        mysqli_close($conn);
        echo "<script>alert('죄송합니다. 선택하신 시간은 이미 예약이 완료되었습니다. 다른 시간을 선택해 주세요.'); window.history.back();</script>";
        exit;
    }
    mysqli_stmt_close($stmt_check);

    // 예약 등록 (Prepared Statement)
    $insert_query = "INSERT INTO `jhair` (`name`, `tel`, `style`, `comment`, `reserve_date`, `reserve_time`, `write_date`, `write_time`, `write_ip`, `trash`, `holiday`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)";
    $stmt = mysqli_prepare($conn, $insert_query);
    mysqli_stmt_bind_param($stmt, "sssssssss", $rname, $rtel, $hstyle, $rcomment, $cdate1, $cdate2, $wdate, $wtime, $wip);
    $executed = mysqli_stmt_execute($stmt);
    mysqli_stmt_close($stmt);

    if ($executed) {
        // 예약 확인 메일 발송
        @include('email.php');
        mysqli_close($conn);

        $redir_year = substr($cdate1, 0, 4);
        $redir_month = substr($cdate1, 5, 2);
        echo "<script>alert('예약이 성공적으로 완료되었습니다.'); location.href='index.php?year=" . urlencode($redir_year) . "&month=" . urlencode($redir_month) . "&date=" . urlencode($cdate1) . "&time=" . urlencode($cdate2) . "';</script>";
        exit;
    } else {
        mysqli_close($conn);
        echo "<script>alert('예약 처리 중 오류가 발생했습니다. 다시 시도해 주세요.'); window.history.back();</script>";
        exit;
    }

} else {
    // -------------------------------------------------------------
    // [2] 고객 직접 예약 취소 (휴대폰 뒷번호 4자리 인증)
    // -------------------------------------------------------------
    if (empty($rid) || empty($rpw)) {
        echo "<script>alert('예약 정보 또는 취소 비밀번호(휴대폰 뒷번호)가 올바르지 않습니다.'); window.history.back();</script>";
        exit;
    }

    $select_query = "SELECT id, tel, reserve_date FROM `jhair` WHERE id = ? AND trash = 0 LIMIT 1";
    $stmt = mysqli_prepare($conn, $select_query);
    mysqli_stmt_bind_param($stmt, "i", $rid);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    $reservation = mysqli_fetch_assoc($result);
    mysqli_stmt_close($stmt);

    if (!$reservation) {
        mysqli_close($conn);
        echo "<script>alert('취소할 수 있는 유효한 예약 내역이 없거나 이미 취소되었습니다.'); window.history.back();</script>";
        exit;
    }

    // 휴대폰 번호에서 숫자만 추출한 뒤 뒷자리 4자리와 대조
    $clean_tel = preg_replace('/[^0-9]/', '', $reservation['tel']);
    $last4 = substr($clean_tel, -4);

    if ($last4 === $rpw) {
        $update_query = "UPDATE `jhair` SET trash = 1 WHERE id = ?";
        $stmt_del = mysqli_prepare($conn, $update_query);
        mysqli_stmt_bind_param($stmt_del, "i", $rid);
        mysqli_stmt_execute($stmt_del);
        mysqli_stmt_close($stmt_del);
        mysqli_close($conn);

        $redir_year = substr($ddate, 0, 4);
        $redir_month = substr($ddate, 5, 2);
        echo "<script>alert('예약이 정상적으로 취소되었습니다.'); location.href='index.php?year=" . urlencode($redir_year) . "&month=" . urlencode($redir_month) . "&view=all';</script>";
        exit;
    } else {
        mysqli_close($conn);
        echo "<script>alert('비밀번호(휴대폰 뒷번호 4자리)가 일치하지 않습니다.'); window.history.back();</script>";
        exit;
    }
}
