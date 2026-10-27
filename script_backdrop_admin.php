<?php 
session_start();
require_once('dbconn.php');

if (!isset($_SESSION['apw']) || $_SESSION['apw'] !== ADMIN_PASSWORD) {
    exit;
}

$date = isset($_REQUEST['date']) ? trim($_REQUEST['date']) : ''; 
$target_yoil = isset($_REQUEST['yoil']) ? trim($_REQUEST['yoil']) : ''; 

if (empty($date)) {
    exit;
}

$year = substr($date, 0, 4);
$month = substr($date, 5, 2);
$cday = substr($date, 8, 2); 

$today = date("Y-m-d");
$time = date("H:i:s");

$select_query = "SELECT * FROM `jhair` WHERE reserve_date = ? AND trash = 0 AND holiday = 0";
$stmt = mysqli_prepare($conn, $select_query);
mysqli_stmt_bind_param($stmt, "s", $date);
mysqli_stmt_execute($stmt);
$result_set = mysqli_stmt_get_result($stmt);

$data = [];
while ($row = mysqli_fetch_assoc($result_set)) {
    $data[] = $row;
}
mysqli_stmt_close($stmt);

for ($a = 12; $a < 20; $a++) { 
    $matching_res = null;
    foreach ($data as $res) {
        if ((int)$a === (int)$res['reserve_time']) {
            $matching_res = $res;
            break;
        }
    }

    if ($matching_res !== null) {
        $explode_style = explode(' ', $matching_res['style']);
        $style_num = '';
        foreach ($explode_style as $st) {
            if ($st === '커트') { $style_num .= '1'; }
            if ($st === '염색') { $style_num .= '2'; }
            if ($st === '파마') { $style_num .= '3'; }
            if ($st === '기타') { $style_num .= '4'; }
        }

        $cust_name = htmlspecialchars($matching_res['name'], ENT_QUOTES, 'UTF-8');
        $safe_style = htmlspecialchars($matching_res['style'], ENT_QUOTES, 'UTF-8');
        $safe_comment = htmlspecialchars(str_replace(' ', '&nbsp;', $matching_res['comment']), ENT_QUOTES, 'UTF-8');
        $safe_tel = htmlspecialchars($matching_res['tel'], ENT_QUOTES, 'UTF-8');
        $item_id = htmlspecialchars($date . '-' . $a, ENT_QUOTES, 'UTF-8');
        $res_id = (int)$matching_res['id'];

        echo "<div class='time reserved' id='m{$item_id}' onclick=reserve_over('{$item_id}');>";
        echo "{$a}시 <button class='btn_cancel' onclick=\"popup_cancel('{$year}','{$month}','{$cday}','{$target_yoil}','{$a}','{$cust_name}','{$style_num}','{$res_id}','{$safe_comment}');\"><span class='del'>예약</span>취소</button>";
        echo "<span class='rdetail'><span class='style'>{$safe_style}</span> {$cust_name}</span>";
        echo "<button class='call' onclick=\"document.location.href='tel:{$safe_tel}'\"></button>";
        echo "</div>";
    } else {
        if ($date === $today) {
            if ((int)$a > (int)date('H')) {
                echo "<div class='time' onclick=\"popup_reserve('{$year}','{$month}','{$cday}','{$target_yoil}','{$a}');\">{$a}시 <button>예약<span class='del'>하기</span></button></div>";
            } else {
                echo "<div class='time reserved'>{$a}시 <button><span class='del'>예약</span>마감</button></div>";
            }
        } else {
            echo "<div class='time' onclick=\"popup_reserve('{$year}','{$month}','{$cday}','{$target_yoil}','{$a}');\">{$a}시 <button>예약<span class='del'>하기</span></button></div>";
        }
    }
}

mysqli_close($conn);