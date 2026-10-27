<?php
/**
 * Reservation Notification Email
 */

if (!defined('MAIL_RECIPIENT')) {
    $config_file = __DIR__ . '/config.php';
    if (file_exists($config_file)) {
        require_once($config_file);
    }
}

$recipient = defined('MAIL_RECIPIENT') ? MAIL_RECIPIENT : 'pyw213@naver.com';
$mail_from = defined('MAIL_FROM') ? MAIL_FROM : 'reservation@jhairs.com';
$base_url = defined('SITE_URL') ? SITE_URL : 'http://pyw31337.dothome.co.kr/reservation/jhair/';

$safe_rname = htmlspecialchars($rname, ENT_QUOTES, 'UTF-8');
$safe_hstyle = htmlspecialchars(ltrim($hstyle), ENT_QUOTES, 'UTF-8');
$safe_rcomment = nl2br(htmlspecialchars($rcomment, ENT_QUOTES, 'UTF-8'));
$safe_cdate1 = htmlspecialchars($cdate1, ENT_QUOTES, 'UTF-8');
$safe_cdate2 = htmlspecialchars($cdate2, ENT_QUOTES, 'UTF-8');
$safe_cyoil = htmlspecialchars($cyoil, ENT_QUOTES, 'UTF-8');
$safe_rtel = htmlspecialchars($rtel, ENT_QUOTES, 'UTF-8');

$subject_raw = "[제이헤어 예약] {$rname} 님 {$cdate1}({$cyoil}) " . substr($cdate2, 0, 2) . "시 <" . ltrim($hstyle) . "> 예약";
$subject = '=?UTF-8?B?' . base64_encode($subject_raw) . '?=';

$link = $base_url . "?year=" . substr($cdate1, 0, 4) . "&month=" . substr($cdate1, 5, 2) . "&date=" . urlencode($cdate1) . "&time=" . urlencode($cdate2) . "&view=all";

$mail_body = <<<HTML
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', sans-serif; line-height: 1.6; color: #333;">
  <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
    <div style="background: #f35381; color: #fff; padding: 18px 24px;">
      <h2 style="margin: 0; font-size: 1.25rem;">💇 제이헤어 시술예약 알림</h2>
    </div>
    <table style="width: 100%; border-collapse: collapse; font-size: 0.95rem;">
      <tr style="border-bottom: 1px solid #edf2f7;">
        <th style="width: 110px; padding: 12px 16px; background: #f8fafc; text-align: left; color: #64748b;">예약일자</th>
        <td style="padding: 12px 16px;"><strong>{$safe_cdate1} ({$safe_cyoil})</strong></td>
      </tr>
      <tr style="border-bottom: 1px solid #edf2f7;">
        <th style="padding: 12px 16px; background: #f8fafc; text-align: left; color: #64748b;">예약시간</th>
        <td style="padding: 12px 16px;"><strong>{$safe_cdate2}</strong></td>
      </tr>
      <tr style="border-bottom: 1px solid #edf2f7;">
        <th style="padding: 12px 16px; background: #f8fafc; text-align: left; color: #64748b;">예약자</th>
        <td style="padding: 12px 16px;">{$safe_rname}</td>
      </tr>
      <tr style="border-bottom: 1px solid #edf2f7;">
        <th style="padding: 12px 16px; background: #f8fafc; text-align: left; color: #64748b;">연락처</th>
        <td style="padding: 12px 16px;"><a href="tel:{$safe_rtel}" style="color: #f35381; text-decoration: none;">{$safe_rtel}</a></td>
      </tr>
      <tr style="border-bottom: 1px solid #edf2f7;">
        <th style="padding: 12px 16px; background: #f8fafc; text-align: left; color: #64748b;">예약시술</th>
        <td style="padding: 12px 16px;"><span style="display: inline-block; padding: 2px 10px; background: #fee2e2; color: #e11d48; border-radius: 9999px; font-weight: 600; font-size: 0.85rem;">{$safe_hstyle}</span></td>
      </tr>
      <tr style="border-bottom: 1px solid #edf2f7;">
        <th style="padding: 12px 16px; background: #f8fafc; text-align: left; color: #64748b;">요청사항</th>
        <td style="padding: 12px 16px;">{$safe_rcomment}</td>
      </tr>
    </table>
    <div style="padding: 20px; text-align: center; background: #f8fafc;">
      <a href="{$link}" target="_blank" style="display: inline-block; padding: 10px 24px; background: #f35381; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold;">캘린더에서 예약 확인하기</a>
    </div>
  </div>
</body>
</html>
HTML;

$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8',
    'From: =?UTF-8?B?' . base64_encode('제이헤어 예약시스템') . '?= <' . $mail_from . '>',
    'X-Mailer: PHP/' . phpversion()
];

@mail($recipient, $subject, $mail_body, implode("\r\n", $headers));
