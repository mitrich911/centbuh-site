<?php
// Приём заявок с сайта: сообщение в MAX, а также (если заданы) письмо на почту и Telegram.
// Настройки берутся из переменных окружения хостинга или из config.php рядом (в репозиторий не кладётся).
header('Content-Type: application/json; charset=utf-8');

$cfg = is_file(__DIR__ . '/config.php') ? require __DIR__ . '/config.php' : [];
$MAX_TOKEN = $cfg['max_token'] ?? getenv('LEAD_MAX_TOKEN');
$MAX_CHAT  = $cfg['max_chat']  ?? getenv('LEAD_MAX_CHAT');   // id группового чата
$MAX_USER  = $cfg['max_user']  ?? getenv('LEAD_MAX_USER');   // или id пользователя для лички
$MAX_API   = $cfg['max_api']   ?? (getenv('LEAD_MAX_API') ?: 'https://platform-api2.max.ru');
$MAIL_TO  = $cfg['mail_to']  ?? getenv('LEAD_MAIL_TO');
$TG_TOKEN = $cfg['tg_token'] ?? getenv('LEAD_TG_TOKEN');
$TG_CHAT  = $cfg['tg_chat']  ?? getenv('LEAD_TG_CHAT');

function fail($code, $msg) { http_response_code($code); echo json_encode(['ok' => false, 'error' => $msg]); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail(405, 'method');
if (!empty($_POST['website'])) { echo json_encode(['ok' => true]); exit; } // бот заполнил скрытое поле
if (empty($_POST['consent'])) fail(422, 'consent');

$f = function ($k, $max = 200) { return mb_substr(trim(strip_tags($_POST[$k] ?? '')), 0, $max); };
$name  = $f('name', 80);
$phone = $f('phone', 25);
$digits = preg_replace('/\D/', '', $phone);
if ($name === '' || strlen($digits) < 10 || strlen($digits) > 12) fail(422, 'fields');

$labels = ['source' => 'Форма', 'business' => 'Кто', 'need' => 'Что нужно', 'staff' => 'Сотрудники', 'channel' => 'Связь', 'comment' => 'Комментарий'];
$lines = ["Новая заявка с сайта", "Имя: $name", "Телефон: $phone"];
foreach ($labels as $k => $label) { $v = $f($k, 1000); if ($v !== '') $lines[] = "$label: $v"; }
$lines[] = 'Время: ' . date('d.m.Y H:i');
$text = implode("\n", $lines);

$sent = false;
if ($MAX_TOKEN && ($MAX_CHAT || $MAX_USER)) {
    $to = $MAX_CHAT ? 'chat_id=' . urlencode($MAX_CHAT) : 'user_id=' . urlencode($MAX_USER);
    $body = json_encode(['text' => $text], JSON_UNESCAPED_UNICODE | JSON_INVALID_UTF8_SUBSTITUTE);
    $ctx = stream_context_create(['http' => ['method' => 'POST', 'timeout' => 8, 'ignore_errors' => true,
        'header' => "Authorization: $MAX_TOKEN\r\nContent-Type: application/json\r\nContent-Length: " . strlen($body),
        'content' => $body]]);
    $r = @file_get_contents(rtrim($MAX_API, '/') . "/messages?$to", false, $ctx);
    $code = isset($http_response_header[0]) && preg_match('/\s(\d{3})\s/', $http_response_header[0], $m) ? (int)$m[1] : 0;
    $sent = ($code === 200 && strpos((string)$r, '"message"') !== false) || $sent;
}
if ($MAIL_TO) {
    $host = preg_replace('/[^a-z0-9.\-]/i', '', $_SERVER['HTTP_HOST'] ?? 'localhost');
    $headers = "From: =?UTF-8?B?" . base64_encode('Сайт бухгалтерии') . "?= <noreply@$host>\r\nContent-Type: text/plain; charset=utf-8";
    $sent = mail($MAIL_TO, '=?UTF-8?B?' . base64_encode("Заявка: $name") . '?=', $text, $headers) || $sent;
}
if ($TG_TOKEN && $TG_CHAT) {
    $ctx = stream_context_create(['http' => ['method' => 'POST', 'timeout' => 8,
        'header' => 'Content-Type: application/x-www-form-urlencoded',
        'content' => http_build_query(['chat_id' => $TG_CHAT, 'text' => $text])]]);
    $r = @file_get_contents("https://api.telegram.org/bot$TG_TOKEN/sendMessage", false, $ctx);
    $sent = ($r && strpos($r, '"ok":true') !== false) || $sent;
}

if (!$sent) fail(500, 'delivery');
echo json_encode(['ok' => true]);
