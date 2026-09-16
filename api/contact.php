<?php
declare(strict_types=1);
// Optional PHP 8+ handler. The website itself is plain static HTML.
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
function reply(int $code, bool $ok): never { http_response_code($code); echo json_encode(['ok'=>$ok]); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') reply(405, false);
if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 24000) reply(413, false);
if (getenv('ORPHARX_MAIL_ENABLED') !== '1') reply(503, false);
$origin = rtrim((string)getenv('ORPHARX_SITE_ORIGIN'), '/');
if (!$origin || ($_SERVER['HTTP_ORIGIN'] ?? '') !== $origin) reply(403, false);
$sender = (string)getenv('ORPHARX_MAIL_FROM');
if (!filter_var($sender, FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/', $sender)) reply(503, false);
$keys = ['company','name','position','email','phone','product','therapeutic_area','interest','message','website','phone_country'];
$data=[];
foreach ($keys as $key) {
    if (isset($_POST[$key]) && !is_string($_POST[$key])) reply(422, false);
    $data[$key]=trim((string)($_POST[$key] ?? ''));
    if (strlen($data[$key]) > ($key==='message' ? 15000 : 1000)) reply(422, false);
}
if ($data['website'] !== '') reply(422, false);
if (!$data['name'] || !$data['message'] || !filter_var($data['email'], FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/', $data['email'])) reply(422, false);
if ($data['phone'] !== '' && (!preg_match('/^\+[1-9][0-9]{6,14}$/', $data['phone']) || !preg_match('/^[A-Z]{2}$/', $data['phone_country']))) reply(422, false);
// Private temp files, keyed by a hash; no submitted content is persisted here.
$ip = (string)($_SERVER['REMOTE_ADDR'] ?? 'unknown');
$file = sys_get_temp_dir().'/orpharx-'.hash('sha256', __DIR__.$ip).'.lock';
$lock = fopen($file, 'c+');
if (!$lock || !flock($lock, LOCK_EX)) reply(503, false);
$last = (int)stream_get_contents($lock);
if (time()-$last < 60) { flock($lock, LOCK_UN); fclose($lock); reply(429, false); }
ftruncate($lock, 0); rewind($lock); fwrite($lock, (string)time()); fflush($lock);
flock($lock, LOCK_UN); fclose($lock);
unset($data['website']);
$body = "OrphaRx website enquiry\n\n";
foreach ($data as $key=>$value) $body .= strtoupper(str_replace('_',' ',$key)).":\n".$value."\n\n";
$accepted = mail('fatmatartuk@gmail.com', 'OrphaRx - Partnership enquiry', $body, [
    'From'=>$sender,
    'Reply-To'=>$data['email'],
    'MIME-Version'=>'1.0',
    'Content-Type'=>'text/plain; charset=UTF-8'
]);
reply($accepted ? 200 : 502, $accepted);
