<?php 
    unset($_SESSION['apw']);

	$year = isset($_GET['year']) ? $_GET['year'] : date('Y');
	$month = isset($_GET['month']) ? $_GET['month'] : date('m');

	$date = "$year-$month-01"; 
	$time = strtotime($date); 
	$start_week = date('w', $time); 
	$total_day = date('t', $time); 
	$total_week = ceil(($total_day + $start_week) / 7);  

    $today = date("Y-m-d");
    $today_time = date("H:i:s");

    $sdate = isset($_REQUEST['date']) ? $_REQUEST['date'] : '';
    $stime = isset($_REQUEST['time']) ? $_REQUEST['time'] : '';
    $sname = isset($_REQUEST['name']) ? $_REQUEST['name'] : '';
    
    $limit_future = date('Y-m-d', strtotime($today. ' + 90 days'));
    $limit_past = date('Y-m-d', strtotime($today. ' - 30 days'));

    if($date > $limit_future) {
        echo "<script>alert('예약기간은 최대 4개월을 초과할 수 없습니다.'); window.history.back();</script>";
    } 

    if($date < $limit_past) {
        echo "<script>alert('마감된 예약기간입니다.'); window.history.back();</script>";
    }
      
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=5.0, user-scalable=yes"/>
    <meta http-equiv="refresh" content="300; url=./">
    <meta name="google" content="notranslate">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://bit.ly/jhairs">
    <meta property="og:title" content="제이헤어 시술예약">
    <meta property="og:image" content="image/1200x630.jpg">
    <meta property="og:description" content="구리시 수택동 [제이헤어] 시술예약">
    <meta property="og:site_name" content="제이헤어 시술예약">
    <meta property="og:locale" content="en_US">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
	<title>제이헤어 시술예약</title>
    <link rel="apple-touch-icon" sizes="57x57" href="favicon/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="favicon/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="favicon/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="favicon/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="favicon/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="favicon/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="favicon/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="favicon/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="favicon/apple-icon-180x180.png">
    <link rel="icon" type="image/png" sizes="192x192"  href="favicon/android-icon-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="favicon/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon/favicon-16x16.png">
    <link rel="manifest" href="favicon/manifest.json">
    <link rel="manifest" href="manifest.json" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-title" content="제이헤어" />
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="favicon/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">
    <link href="css/common.css" rel="stylesheet" />
    <link href="css/checkbox.css" rel="stylesheet" />
    <link href="css/infinite-carousel-css-only.webflow.182ee2047.css" rel="stylesheet" type="text/css"/>
</head>
<body>

<?php
require('dbconn.php');

$select_query = "SELECT * FROM `jhair` WHERE NOT trash = '1'";

$result_set = mysqli_query($conn, $select_query);

$i = 0;
$data = [];

while($row = mysqli_fetch_array($result_set)){
    $data[$i] = $row;
    $i++;
};

$holiday_data = [];

for($i=0;$i<count($data);$i++){
    if($data[$i]['holiday'] == 1) {
        $holiday_data[$i] = $data[$i]['reserve_date'];
    }
}

sort($holiday_data);

?>
    <div class="formcover">
        <div class='aside'>
            <div class='close' onclick=menuclose();></div>
            <div class='map' onclick=window.open('https://naver.me/50enuoRi');><div class='map_icon'></div><span>위치보기</span></div>
            <div class='tel' onclick=document.location.href='tel:0315550628'><div class='tel_icon'></div><span>문의전화</span></div>
            <div class='share' id="kakaotalk-sharing-btn" onclick="javascript:;"><div class='share_icon'></div><span>카카오톡 공유</span></div>
            <div class='share' onclick=share();><div class='qr_icon'></div><span>QR코드 보기</span></div>
            <div class='qr'></div>
            <div class='admin'>관리자 로그인</div>

            <form class="form_admin" method="post" action="admin.php">
                <div class=list><div class='icon_pw'></div> <input type=password id=apw name=apw class=inbox data-error-value-missing=PleaseEnterPassword placeholder='비밀번호를 입력해 주세요'></div>
                <button type="submit" class="submit" value="submit">관리자 로그인</button>
            </form>

        </div>

        <form class="form_reserve" method="post" action="send.php">
    
            <div class="card">
                <div class="content">
                    <div class="close"></div>
                    <div class="store">제이헤어 미용실</div>
                    <div class="discount"><span class='num'>10</span><span class='percent'>%</span><div>인터넷 예약후 시술시 <b>10% 결제 할인</b><span class='del'>해 드립니다.</span></div></div>
                    <input type=text id=cdate name=cdate class=box placeholder='2024-03-15 (금) 12시' readonly='true'>
                    <input type=text id=cname name=cname class=box placeholder='예약자' readonly='true'>
                    <div class="cstyle"><span id="bb1">커트</span><span id="bb2">염색</span><span id="bb3">파마</span><span id="bb4">기타</span></div>
                    <input type=hidden id=cdate1 name=cdate1>
                    <input type=hidden id=cdate2 name=cdate2>
                    <input type=hidden id=cyoil name=cyoil>
                </div>
                <div class="cardbg front"></div>
                <div class="cardbg back"></div>
            </div> 

            <div class=list><span id=cremain name=cremain class=box>예약시간이 지났습니다.<span class='del'> 다른시간을 선택해 주세요<i>!</i></span></span></div>
            <div class=list><span class=title>예약자</span> <div class='icon_human'></div> <input type=text id=rname name=rname class=inbox data-error-value-missing=PleaseEnterName placeholder='성함을 입력하세요'><div class="caution_name">↑ 성함을 입력해 주세요!</div></div>
            <div class=list><span class=title>연락처</span> <div class='icon_phone'></div> <input type="number" inputmode="numeric" pattern="[0-9]*" id=rtel name=rtel class=inbox data-error-value-missing=PleaseEnterTelNumber placeholder='연락처를 입력하세요' onfocusout="telcheck()"><div class="caution_tel">↑ 연락처를 입력해 주세요!</div></div>
            <div class=list><span class=title>시술명</span> 

                <div class='icon_style'></div>
                <div class="checkbox-wrapper-10">
                    <input class="tgl tgl-flip" id="cb1" type="checkbox" name="rstyle[]" value="커트" />
                    <label class="tgl-btn" data-tg-off="커트" data-tg-on="커트" for="cb1"></label>
                    <input class="tgl tgl-flip" id="cb2" type="checkbox" name="rstyle[]" value="염색"/>
                    <label class="tgl-btn" data-tg-off="염색" data-tg-on="염색" for="cb2"></label>
                    <input class="tgl tgl-flip" id="cb3" type="checkbox" name="rstyle[]" value="파마"/>
                    <label class="tgl-btn" data-tg-off="파마" data-tg-on="파마" for="cb3"></label>
                    <input class="tgl tgl-flip" id="cb4" type="checkbox" name="rstyle[]" value="기타"/>
                    <label class="tgl-btn" data-tg-off="기타" data-tg-on="기타" for="cb4"></label>
                </div>
                <div class="caution_style">↑ 한개 이상의 시술을 선택해 주세요!</div>

            </div>

            <div class=list><span class=title>요청사항</span> <div class='icon_note'></div> <textarea id=rcomment name=rcomment class=inbox data-error-value-missing=PleaseEnterComment placeholder='요청사항을 입력하세요'></textarea></div>
            <button type="submit" class="submit" value="submit">예약하기</button>

        </form>

        <form class="form_cancel" method="post" action="send.php">
            <div class="card">
                <div class="content">
                    <div class="close"></div>
                    <div class="store">제이헤어 미용실</div>
                    <div class="discount"><span class='num'>10</span><span class='percent'>%</span><div><b>10% 예약할인</b> 혜택이 소멸됩니다</div></div>
                    <input type=text id=ddate name=ddate class=box placeholder='2024-03-15 (금) 12시' readonly='true'>
                    <input type=text id=dname name=dname class=box placeholder='예약자' readonly='true'>
                    <div class="cstyle"><span id="bb1">커트</span><span id="bb2">염색</span><span id="bb3">파마</span><span id="bb4">기타</span></div>
                </div>
                <div class="cardbg front"></div>
                <div class="cardbg back"></div>
            </div> 

            <div class="caution_cancel">진짜로 취소하시겠습니까?</div>
            <div class=list><span class=title>비밀번호</span> <div class='icon_pw'></div> <input type=password inputmode="numeric" pattern="[0-9]*" id=rpw name=rpw class=inbox data-error-value-missing=PleaseEnterPassword placeholder='휴대폰 뒷번호 4자리를 입력해 주세요'><div class="caution_pw">↑ 휴대폰 뒷번호 4자리를 입력해 주세요!</div></div>
            <input type=hidden id=rid name=rid>

            <button type="submit" class="submit" value="submit">취소하기</button>

        </form>

        <div class="dim"></div>
    </div>
    <!-- Dim Divider -->
    
    <div class='header'>
        <div class='menu' onclick=menuopen();></div>
        <div class='store_name'>
            <div class='logo'><span class='symbol'><img src='image/symbol.png'></span><span class='txt'>J.Hair Shop</span></div>
            <div class='info'>영업시간&nbsp; <b>12:00 ~ 20:00</b></div>
            <div class='info'>매월 첫째주/셋째주 일요일 휴무</div>
            <?php
                $select_query = "SELECT * FROM `jhair` WHERE id = '1'";
                $result_set = mysqli_query($conn, $select_query);

                $i = 0;
                $noti = [];

                while($row = mysqli_fetch_array($result_set)){
                    $noti[$i] = $row;
                    $i++;
                };

                if($noti[0]['comment'] != null){
                    echo "<div class='info notice_list'><div class='icon_notice_w'></div><span class='notice'>".$noti[0]['comment']."</span></div>";
                }
            ?>
        </div>
        
        <div class='dim'></div>

        <div class="slider-wrapper">
            <div class="items-holder">
                <div class="items">
                    <img src="image/generated-female-layered.jpg" loading="eager" class="item"/>
                    <img src="image/generated-female-bob.jpg" loading="eager" class="item"/>
                    <img src="image/generated-female-wave.jpg" loading="eager" class="item"/>
                    <img src="image/generated-female-hush.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-female-bangs.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-female-lob.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-male-twoblock.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-male-part.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-male-leaf.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-male-crop.jpg" loading="lazy" class="item"/>
                </div>
                <div class="items">
                    <img src="image/generated-female-layered.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-female-bob.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-female-wave.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-female-hush.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-female-bangs.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-female-lob.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-male-twoblock.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-male-part.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-male-leaf.jpg" loading="lazy" class="item"/>
                    <img src="image/generated-male-crop.jpg" loading="lazy" class="item"/>
                </div>
            </div>
        </div>     <!-- Slider Close -->

    </div>     <!-- Header Close -->


    <div class="container_tab">
        <div class="tabs">
            <span class='tab' id='tab1' onclick=viewmode(1);>날짜별보기</span>
            <span class='tab' id='tab2'onclick=viewmode(2);>한번에보기</span>
        </div>
    </div>
    

    <div class='backdrop'>
        <span class='bday'></span>
        <span class='close'></span>
        <span class='div_content'></span>
    </div>


    <div class='calcovermini'>

    <?php // Month Move Module
    echo "<div class='head'>";
    if ($month == 1) { // Previous Month
        echo "<span onClick=location.href='?year=".($year-1)."&month=12' class='month_prev_txt'><span class='del'>".($year-1).".</span>12 <span class='month_prev'></span></span>";
    } else {
        $pmonth = $month - 1;
        if($pmonth<10) {$pmonth = "0".$pmonth;}
        echo "<span onClick=location.href='?year=".$year."&month=".$pmonth."' class='month_prev_txt'><span class='del'>".$year.".</span>".$pmonth." <span class='month_prev'></span></span>";
    }

    echo "<div class='hdate' onClick=location.href='?year=".date('Y')."&month=".date("m")."'><span class='hmonth'>".$year."</span><span class='hday'>".$month."</span></div>";

    if ($month == 12) { // Next Month
        echo "<span onClick=location.href='?year=".($year+1)."&month=01' class='month_next_txt'><span class='month_next'></span><span class='del'>".($year+1).".</span>01</span>";
    } else {
        $nmonth = $month + 1;
        if($nmonth<10) {$nmonth = "0".$nmonth;}
        echo "<span onClick=location.href='?year=".$year."&month=".$nmonth."' class='month_next_txt'><span class='month_next'></span><span class='del'>".$year.".</span>".$nmonth."</span>";
    } 
    echo "</div>";
    ?>

    <table class='calendar'>
        <tr> 
            <th>일</th> 
            <th>월</th> 
            <th>화</th> 
            <th>수</th> 
            <th>목</th> 
            <th>금</th> 
            <th>토</th> 
        </tr> 

        <?php 

        for ($n = 1, $i = 0; $i < $total_week; $i++) {
            echo "<tr>";
            

                for ($k = 0; $k < 7; $k++) {
                    echo "<td>";

                    if ( ($n > 1 || $k >= $start_week) && ($total_day >= $n) ) {

                        if($n<10) { $da = $year."-".$month."-0".$n;}
                        else { $da = $year."-".$month."-".$n; }
                        
                        $holiday_check = 0;

                        for($g=0;$g<count($holiday_data);$g++){
                            if($da == $holiday_data[$g]) {
                                $holiday_check = 1;
                            }
                        }

                        $yoil = array("일","월","화","수","목","금","토");
                        $target_yoil = $yoil[date('w', strtotime($da))];	   
                        
                        if($da == $today) { 
                            if($holiday_check == 1) { 
                                echo "<span class='date todayover'>".$n++."</span>"; 
                            } else {
                                echo "<span class='date today' onclick=drop_date('".$da."','".$target_yoil."');>".$n++."</span>";                                 
                            }
                        }
                        else if($da < $today) { echo "<span class='date past'>".$n++."</span>"; }
                        else { 
                            if($holiday_check == 1) { 
                                echo "<span class='date past'>".$n++."</span>"; 
                            } else {
                                echo "<span class='date' id='".$da."' onclick=drop_date('".$da."','".$target_yoil."');>".$n++."</span>"; 
                            }
                        }

                        if($sdate == $da){
                            echo "<div class='reservehere'>완료<span></span></div>";
                        }

                    }

                }
                    echo "</td>";  
            echo "</tr>"; 
        }

    ?>
        </table>
    </div>
    <!-- End .calcovermini -->


    <div class='calcover'>

    <?php // Month Move Module
    echo "<div class='head'>";
	if ($month == 1) { // Previous Month
        echo "<span onClick=location.href='?year=".($year-1)."&month=12&view=all' class='month_prev_txt'><span class='del'>".($year-1).".</span>12 <span class='month_prev'></span></span>";
    } else {
        $pmonth = $month - 1;
        if($pmonth<10) {$pmonth = "0".$pmonth;}
		echo "<span onClick=location.href='?year=".$year."&month=".$pmonth."&view=all' class='month_prev_txt'><span class='del'>".$year.".</span>".$pmonth." <span class='month_prev'></span></span>";
    }

    echo "<div class='hdate' onClick=location.href='?year=".date('Y')."&month=".date("m")."&view=all'><span class='hmonth'>".$year."</span><span class='hday'>".$month."</span></div>";

    if ($month == 12) { // Next Month
		echo "<span onClick=location.href='?year=".($year+1)."&month=01&view=all' class='month_next_txt'><span class='month_next'></span><span class='del'>".($year+1).".</span>01</span>";
    } else {
        $nmonth = $month + 1;
        if($nmonth<10) {$nmonth = "0".$nmonth;}
		echo "<span onClick=location.href='?year=".$year."&month=".$nmonth."&view=all' class='month_next_txt'><span class='month_next'></span><span class='del'>".$year.".</span>".$nmonth."</span>";
    } 
    echo "</div>";
    ?>

	<table class='calendar'>
		<tr> 
			<th>일</th> 
			<th>월</th> 
			<th>화</th> 
			<th>수</th> 
			<th>목</th> 
			<th>금</th> 
			<th>토</th> 
		</tr> 

		<?php 

        for ($n = 1, $i = 0; $i < $total_week; $i++) {
            echo "<tr>";
            

				for ($k = 0; $k < 7; $k++) {
					echo "<td>";

					if ( ($n > 1 || $k >= $start_week) && ($total_day >= $n) ) {

                        $da = $year."-".$month."-".$n;

                        if($n<10) { $da = $year."-".$month."-0".$n;}
                        else { $da = $year."-".$month."-".$n; }

                        $holiday_check = 0;

                        for($g=0;$g<count($holiday_data);$g++){
                            if($da == $holiday_data[$g]) {
                                $holiday_check = 1;
                            }
                        }

                        if($da == $today) { 
                            if($holiday_check == 1) { 
                                echo "<span class='date todayover'>".$n++."</span>"; 
                            } else {
                                echo "<span class='date today'>".$n++."</span>"; 
                            }
                        }
                        else if($da < $today) { echo "<span class='date past'>".$n++."</span>"; }
                        else {
                            if($holiday_check == 1) { 
                                echo "<span class='date past'>".$n++."</span>"; 
                            } else {
                                echo "<span class='date' id='f".$da."'>".$n++."</span>"; 
                            }
                        }
						
                       
                        if(($n-1)<10) { $cday = "0".($n-1); } else { $cday = ($n-1);}
                        $date = $year."-".$month."-".$cday;

                        $check_day = 0; // Reservation_Day or Not
                        $check_time = 0; // Reservation_Time or Not

                        for($j=0;$j<count($data);$j++){
                            if($date == $data[$j]['reserve_date']) {$check_day = 1;}
                        } // Day has Reservation Check

                        
                        $sum_data = ''; 

                        for($q=0;$q<count($data);$q++){
                            
                            if($date == $data[$q]['reserve_date']){
                                $sum_data[$q] = $data[$q];
                            }
                        
                        };

                        if($sum_data != null) { sort($sum_data); }
                        // print_r($sum_data);


                        if($date < $today) {
                            echo "<div class='holiday'>마감</div>";
                        } else {

                            if($holiday_check == 1) {
                                if($date == $today) { echo "<div class='holiday'>마감</div>"; } else  { echo "<div class='holiday'>휴무</div>"; }
                            } else {

                                for($a=12;$a<20;$a++){ // Create Day Schedule 

                                    $yoil = array("일","월","화","수","목","금","토");
                                    $target_yoil = $yoil[date('w', strtotime($date))];	         

                                    if($sdate == $date && $stime == $a){
                                        echo "<div class='reservehere'>완료<span></span></div>";
                                    }

                                    if($check_day == 1) { // Reservation Day

                                        for($b=0;$b<count($sum_data);$b++) {
                                            if($a == $sum_data[$b]['reserve_time']) { // Reservation Time
                                                $check_time = 1;

                                                $explode_style = explode(' ',$sum_data[$b]['style']);
                                                $style_num = '';

                                                for($e=0;$e<count($explode_style);$e++){
                                                    if($explode_style[$e] == '커트') { $style_num = $style_num.'1'; }
                                                    if($explode_style[$e] == '염색') { $style_num = $style_num.'2'; }
                                                    if($explode_style[$e] == '파마') { $style_num = $style_num.'3'; }
                                                    if($explode_style[$e] == '기타') { $style_num = $style_num.'4'; }
                                                }

                                                echo "<div class='time reserved' id='f".$date.'-'.$a."' onclick=reserve_over('".$date.'-'.$a."');>".$a."시 <button class='btn_cancel' onclick=popup_cancel('".$year."','".$month."','".$cday."','".$target_yoil."','".$a."','".mb_substr($sum_data[$b]['name'], 0, 1, 'utf-8')."','".$style_num."','".$sum_data[$b]['id']."');><span class='del'>예약</span>취소</button><span class='rdetail'><span class='style'>".$sum_data[$b]['style']."</span> ".mb_substr($sum_data[$b]['name'], 0, 1, 'utf-8')."**</span></span></div>"; 
                                            }
                                        }

                                        if($check_time != 1) {
                                            if($date == $today) { // Today Reservation Close

                                                if($a > $today_time) {                                                    
                                                    echo "<div class='time' onclick=popup_reserve('".$year."','".$month."','".$cday."','".$target_yoil."','".$a."');>".$a."시 <button>예약<span class='del'>하기</span></button></div>";
                                                } else {
                                                    echo "<div class='time reserved'>".$a."시 <button><span class='del'>예약</span>마감</button></div>";
                                                }
                                            } else { // Other Day Reservation Close
                                                echo "<div class='time' onclick=popup_reserve('".$year."','".$month."','".$cday."','".$target_yoil."','".$a."');>".$a."시 <button>예약<span class='del'>하기</span></button></div>";
                                            }
                                        }
                                        
                                        $check_time = 0;

                                    } else { // No Reservation Day

                                        if($date == $today) { // Today Reservation Close
                                            if($a > $today_time) {
                                                echo "<div class='time' onclick=popup_reserve('".$year."','".$month."','".$cday."','".$target_yoil."','".$a."');>".$a."시 <button>예약<span class='del'>하기</span></button></div>"; 
                                            } else {
                                                echo "<div class='time reserved'>".$a."시 <button><span class='del'>예약</span>마감</button></div>";
                                            }
                                        } else { // Other Day Reservation Close
                                            echo "<div class='time' onclick=popup_reserve('".$year."','".$month."','".$cday."','".$target_yoil."','".$a."');>".$a."시 <button>예약<span class='del'>하기</span></button></div>"; 
                                        }                                    

                                    }
                                }
                            }
                       }


                    }
					echo "</td>"; 
                } 
			echo "</tr>"; 
        }
        
        mysqli_close($conn);
    ?>
	    </table>
    </div>
    <!-- End .calcover -->

<div class='copyright'>Copyright @ 2024 J.Hairshop All Rights Reserved.</div>

</body>

<script type="text/javascript" src="https://cdn.jsdelivr.net/jquery/latest/jquery.min.js"></script>
<script src="https://t1.kakaocdn.net/kakao_js_sdk/2.7.1/kakao.min.js"
  integrity="sha384-kDljxUXHaJ9xAb2AzRd59KxjrFjzHa5TAoFQ6GbYTCAG0bjM55XohjjDT7tDDC01" crossorigin="anonymous"></script>
<script>
  Kakao.init('0236cfffa7cfef34abacd91a6d7c73c0'); // 사용하려는 앱의 JavaScript 키 입력
</script>
<script>
  Kakao.Share.createDefaultButton({
    container: '#kakaotalk-sharing-btn',
    objectType: 'feed',
    content: {
      title: '제이헤어 시술예약',
      description: '구리시 수택동 [제이헤어] 시술예약',
      imageUrl:
        'http://pyw31337.dothome.co.kr/reservation/jhair/image/kakao.jpg',
      link: {
        // [내 애플리케이션] > [플랫폼] 에서 등록한 사이트 도메인과 일치해야 함
        mobileWebUrl: 'http://pyw31337.dothome.co.kr/reservation/jhair/',
        webUrl: 'http://pyw31337.dothome.co.kr/reservation/jhair/',
      },
    },
    buttons: [
      {
        title: '웹으로 보기',
        link: {
          mobileWebUrl: 'http://pyw31337.dothome.co.kr/reservation/jhair/',
          webUrl: 'http://pyw31337.dothome.co.kr/reservation/jhair/',
        },
      },
    ],
  });
</script>
<script>

    var Dday;

    function getTime(){
        var today = new Date();
  
        var gap = Dday.getTime() - today.getTime();
        var day = Math.ceil(gap / (1000 * 60 * 60 * 24))-1;
        var hour = Math.ceil((gap % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))-1;
        var min = Math.floor((gap % (1000 * 60 * 60)) / (1000 * 60));
        var sec = Math.floor((gap % (1000 * 60)) / 1000);

        if(isNaN(sec)){
            $('#cremain').css("display","none");
        }  else {
            $('#cremain').fadeIn();
        }

        if(sec < 0) {
            $('#cremain').html('<span style=color:#f00;>예약시간이 지났습니다.<span class=del> 다른시간을 선택해 주세요<i>!</i></span></span>');    
            $('.form_reserve .submit').css('pointer-events','none');
            $('.form_reserve .submit').css('background-color','#aaa');
            $('.form_reserve .submit').html('예약마감');
        } else {
            if(day > 0) {
                $('#cremain').html('예약시간까지 <b>'+day+'일 '+hour+'시간 '+min+'분 '+sec+'초</b> 남았습니다<i>!</i>');
            } else {
                if(hour > 0) {
                    $('#cremain').html('예약시간까지 <b>'+hour+'시간 '+min+'분 '+sec+'초</b> 남았습니다<i>!</i>');
                } else {
                    $('#cremain').html('예약시간까지 <b>'+min+'분 '+sec+'초</b> 남았습니다<i>!</i>');
                }
            }
            $('.form_reserve .submit').css('pointer-events','all');
            $('.form_reserve .submit').css('background-color','#f35381');
            $('.form_reserve .submit').html('예약하기');
        } 



        // console.log(typeof sec);
    }


    function popup_reserve(year,month,day,yoil,time){
        $(".formcover").css("display","flex");
        $(".form_reserve").css("display","block");
        $(".aside").css("display","none");
        $(".calcover").css("filter","blur(2px)opacity(0.5)");

        $(".date").removeClass('selected');
        $("#"+year+"-"+month+"-"+day).addClass('selected');
        $("#f"+year+"-"+month+"-"+day).addClass('selected');

        $("#cdate").val(year+'-'+month+'-'+day+' ('+yoil+') '+time+'시');
        $("#cdate1").val(year+'-'+month+'-'+day);
        $("#cdate2").val(time+':00:00');      
        $("#cyoil").val(yoil);    

        Dday = new Date(year+'-'+month+'-'+day+' '+time+':00:00');
        setInterval(getTime, 1000);

    }

    function popup_cancel(year,month,day,yoil,time,name,style,id){
        $(".formcover").css("display","flex");
        $(".form_cancel").css("display","block");
        $(".aside").css("display","none");
        $(".calcover").css("filter","blur(2px)opacity(0.5)");

        $(".date").removeClass('selected');
        $("#"+year+"-"+month+"-"+day).addClass('selected');
        $("#f"+year+"-"+month+"-"+day).addClass('selected');

        $("#ddate").val(year+'-'+month+'-'+day+' ('+yoil+') '+time+'시');
        $("#dname").val(name+'**');
        $("#rid").val(id);

        if(style.indexOf('1') != -1) { $('.form_cancel #bb1').show(); }
        if(style.indexOf('2') != -1) { $('.form_cancel #bb2').show(); }
        if(style.indexOf('3') != -1) { $('.form_cancel #bb3').show(); }
        if(style.indexOf('4') != -1) { $('.form_cancel #bb4').show(); }

    }
    
    function telcheck(){
        let text1 = $('#rtel').val();
        let text2 = text1.replaceAll("-", "");
        let result = text2.replaceAll(" ", "");
        $('#rtel').val(result);
    }

    function reserve_over(id){
        $('#m'+id+' > button').toggle();
        $('#m'+id+' > .rdetail').toggle();
        $('#f'+id+' > button').toggle();
        $('#f'+id+' > .rdetail').toggle();
    }

    function drop_date(date,yoil) {
        $('.date').removeClass('selected');
        $('#'+date).addClass('selected');
        $('#f'+date).addClass('selected');

        $('.backdrop').slideDown('fast');
        $('.bday').html(date.replaceAll("-",".")+" ("+yoil+") 예약내역");
        drop_loadmore(date,yoil);
        
    }

    function drop_loadmore(date,yoil) {

        $.ajax({
            type: 'POST',
            url: 'script_backdrop.php',
            dataType: 'html',    
            data: {date,yoil},
            success: function(data) {

                $(".div_content").html(data); 
                // $(".div_content").append(data);

            } 
        }); 
    }

    function viewmode(num){
        if(num == 1) { $('.calcovermini').fadeIn(); $('.calcover').hide(); $('#tab1').addClass('tab_select'); $('#tab2').removeClass('tab_select');}
        if(num == 2) { $('.calcovermini').hide(); $('.calcover').fadeIn(); $('#tab1').removeClass('tab_select'); $('#tab2').addClass('tab_select');}
    }

    function menuopen(){
        $(".formcover").css("display","grid");
        $(".aside").css("display","block");
        $(".calcover").css("filter","blur(2px)opacity(0.5)");
        $(".calcovermini").css("filter","blur(2px)opacity(0.5)");
    }

    function menuclose(){
        $(".calcover").css("filter","none");
        $(".calcovermini").css("filter","none");
        $(".admin").css("display","block");
        $(".form_admin").css("display","none");
    }

    function share(){
        $(".qr").show();
        $(".admin").css("margin-top","30px");
        
        const urlToShare = 'http://bit.ly/jhairs';
        const textArea = document.createElement('textarea');
        textArea.value = urlToShare;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        alert('주소가 복사되었습니다. 붙여넣기하여 공유 하세요.');
    }

    const urlParams = new URL(location.href).searchParams;
    const date = urlParams.get('date');
    const view = urlParams.get('view');
    const year = urlParams.get('year');
    const month = urlParams.get('month');
   
    $('#'+date).addClass('selected');
    $('#f'+date).addClass('selected');


    
    if(view == 'all') {
        $('#tab2').addClass('tab_select'); $('.calcovermini').hide(); $('.calcover').show();
    } else { 
        $('#tab1').addClass('tab_select'); $('.calcovermini').show(); $('.calcover').hide();
    }

    if(screen.height < 570) {
        $('.store').hide();
        $('.form_reserve .cstyle').hide();
        $('.form_reserve #cremain').hide();

        $('.form_reserve').css("bottom","0");
        $('.form_reserve .card').css("margin-bottom","-100px");
        $('.form_reserve .card .content').css("padding-bottom","40px");
    }
    
    setTimeout(() => {
        $('.reservehere').fadeOut();
    }, 10000);


    $(".backdrop .close").on("click",function(){
        // $('.date').removeClass('selected');
        $('.backdrop').slideUp('fast');
    });

    $('.form_reserve .submit').on("click",function(){

        if($("#rname").val() == "") {
            $('.caution_name').fadeIn();
            $('#rname').focus();
            return false;
        } else { $('.caution_name').fadeOut(); }

        if($("#rtel").val() == "") {
            $('.caution_tel').fadeIn();
            $('#rtel').focus();
            return false;
        } else { $('.caution_tel').fadeOut(); }

        if(!$('#cb1').is(':checked') && !$('#cb2').is(':checked') && !$('#cb3').is(':checked') && !$('#cb4').is(':checked') ) {
            $('.caution_style').fadeIn();
            return false;
        } else { $('.caution_style').fadeOut(); }

    });

    $('.form_cancel .submit').on("click",function(){

        if($("#rpw").val() == "") {
            $('.caution_pw').fadeIn();
            $('#rpw').focus();
            return false;
        } else { $('.caution_pw').fadeOut(); }

    });

    $(".admin").on("click",function(){
        $(".qr").hide();
        $(".admin").css("display","none");
        $(".form_admin").css("margin-top","30px");
        $(".form_admin").css("display","block");
        $('#apw').focus();
    })

    $("#rname").on("propertychange change keyup paste input",function(){
        $("#cname").val($(this).val());

    });

    $(".close").on("click",function(){
        $(".qr").hide();
        $(".form_reserve").css("display","none");
        $(".form_cancel").css("display","none");
        $(".formcover").fadeOut();
        $(".calcover").css("filter","none");

        $('.form_cancel #bb1').hide();
        $('.form_cancel #bb2').hide();
        $('.form_cancel #bb3').hide();
        $('.form_cancel #bb4').hide();
    })

    $('#cb1, #cb2, #cb3, #cb4').on('click', function() {
        if ($('#cb1').is(':checked')){ $("#bb1").fadeIn() } else {{ $("#bb1").fadeOut() }};
        if ($('#cb2').is(':checked')){ $("#bb2").fadeIn() } else {{ $("#bb2").fadeOut() }};
        if ($('#cb3').is(':checked')){ $("#bb3").fadeIn() } else {{ $("#bb3").fadeOut() }};
        if ($('#cb4').is(':checked')){ $("#bb4").fadeIn() } else {{ $("#bb4").fadeOut() }};
    });

</script>
</html>
