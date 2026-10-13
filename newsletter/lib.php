<?php
require_once __DIR__ . '/config.php';

function b64url_encode(string $s): string { return rtrim(strtr(base64_encode($s), '+/', '-_'), '='); }
function b64url_decode(string $s): string|false { return base64_decode(strtr($s, '-_', '+/'), true); }

/** Podpisany token (bez bazy danych): dane + HMAC. */
function make_token(array $data): string {
    $payload = b64url_encode(json_encode($data, JSON_UNESCAPED_UNICODE));
    $sig = b64url_encode(hash_hmac('sha256', $payload, SECRET, true));
    return $payload . '.' . $sig;
}

function read_token(string $token): ?array {
    $parts = explode('.', $token);
    if (count($parts) !== 2) return null;
    [$payload, $sig] = $parts;
    $expected = b64url_encode(hash_hmac('sha256', $payload, SECRET, true));
    if (!hash_equals($expected, $sig)) return null;
    $json = b64url_decode($payload);
    if ($json === false) return null;
    $data = json_decode($json, true);
    return is_array($data) ? $data : null;
}

/** Indywidualny kod rabatowy – zawsze ten sam dla danego adresu e-mail. */
function discount_code(string $email): string {
    $h = strtoupper(substr(hash_hmac('sha256', strtolower($email), SECRET . '|code'), 0, 8));
    return 'RKDP' . DISCOUNT_PERCENT . '-' . $h;
}

function client_ip(): string { return $_SERVER['REMOTE_ADDR'] ?? ''; }
function user_agent(): string { return substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 300); }

/** Rejestr zgód i zdarzeń (CSV) – dowód wyrażenia i wycofania zgody. */
function log_event(string $event, string $email, string $name = '', string $extra = ''): void {
    if (!is_dir(DATA_DIR)) @mkdir(DATA_DIR, 0750, true);
    $file = DATA_DIR . '/rejestr-zgod.csv';
    $new = !file_exists($file);
    $fh = @fopen($file, 'a');
    if (!$fh) return;
    if (flock($fh, LOCK_EX)) {
        if ($new) fputcsv($fh, ['data_czas', 'zdarzenie', 'email', 'imie', 'ip', 'przegladarka', 'wersja_zgod', 'uwagi'], ';');
        fputcsv($fh, [date('c'), $event, $email, $name, client_ip(), user_agent(), CONSENT_VERSION, $extra], ';');
        flock($fh, LOCK_UN);
    }
    fclose($fh);
}

function mime_header(string $s): string { return '=?UTF-8?B?' . base64_encode($s) . '?='; }

/** Wysyłka maila HTML + tekst. */
function send_mail(string $to, string $subject, string $html, string $text, ?string $replyTo = null): bool {
    $boundary = 'b' . bin2hex(random_bytes(12));
    $headers = [
        'MIME-Version: 1.0',
        'From: ' . mime_header(FROM_NAME) . ' <' . FROM_EMAIL . '>',
        'Reply-To: ' . ($replyTo ?: OWNER_EMAIL),
        'Content-Type: multipart/alternative; boundary="' . $boundary . '"',
    ];
    $body  = "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($text)) . "\r\n";
    $body .= "--$boundary\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($html)) . "\r\n";
    $body .= "--$boundary--\r\n";
    return @mail($to, mime_header($subject), $body, implode("\r\n", $headers), '-f' . FROM_EMAIL);
}

function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

/** Szablon maila w kolorach RKDP. */
function email_layout(string $title, string $inner): string {
    $logo = SITE_URL . '/img/logo-rkdp.png';
    return '<!doctype html><html lang="pl"><body style="margin:0;background:#F8F5F0;font-family:Arial,Helvetica,sans-serif;color:#1D1A16">'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F8F5F0;padding:32px 12px"><tr><td align="center">'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border:1px solid #E3D9CA;border-radius:16px">'
        . '<tr><td style="padding:28px 32px 8px"><img src="' . h($logo) . '" alt="RKDP spółka doradztwa podatkowego" width="160" style="display:block;height:auto"></td></tr>'
        . '<tr><td style="padding:8px 32px 32px"><h1 style="font-size:22px;line-height:1.3;margin:12px 0 16px;color:#1D1A16">' . h($title) . '</h1>'
        . $inner . '</td></tr>'
        . '<tr><td style="padding:20px 32px;border-top:1px solid #E3D9CA;font-size:12px;line-height:1.6;color:#6A6157">'
        . 'RKDP spółka doradztwa podatkowego sp. z o.o., ul. Czereśniowa 28d, 55-010 Ozorzyce, NIP 8992871126, KRS 0000812185.<br>'
        . 'Kancelaria: ul. Beaty Artemskiej 11/44, 52-234 Wrocław · +48 883 643 565'
        . '</td></tr></table></td></tr></table></body></html>';
}

function button(string $url, string $label): string {
    return '<p style="margin:24px 0"><a href="' . h($url) . '" style="display:inline-block;background:#7A5A37;color:#ffffff;text-decoration:none;font-weight:bold;padding:14px 26px;border-radius:999px">' . h($label) . '</a></p>';
}

/** Prosta strona wynikowa (potwierdzenie / rezygnacja) w stylu strony. */
function result_page(string $title, string $html): void {
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Robots-Tag: noindex');
    echo '<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">'
        . '<title>' . h($title) . ' – RKDP</title><link rel="icon" href="../img/favicon.svg" type="image/svg+xml">'
        . '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=Montserrat:wght@400;600&display=swap">'
        . '<style>body{margin:0;background:#F8F5F0;color:#1D1A16;font-family:Montserrat,system-ui,sans-serif;line-height:1.7}'
        . '.box{max-width:620px;margin:8vh auto;padding:40px 32px;background:#fff;border:1px solid #E3D9CA;border-radius:24px}'
        . 'h1{font-family:"Plus Jakarta Sans",sans-serif;font-weight:700;letter-spacing:-.02em;font-size:30px;line-height:1.15;margin:24px 0 16px}'
        . 'p{color:#4A433B}a{color:#7A5A37}.code{display:inline-block;font-family:"Plus Jakarta Sans",sans-serif;font-weight:700;font-size:26px;letter-spacing:.06em;padding:14px 22px;border:2px dashed #7A5A37;border-radius:12px;color:#7A5A37;margin:8px 0 16px}'
        . 'a.btn{display:inline-block;margin-top:12px;background:#7A5A37;color:#fff;text-decoration:none;font-weight:600;padding:14px 24px;border-radius:999px}'
        . '@media(max-width:640px){.box{margin:0;border-radius:0;border:0;min-height:100vh}}</style></head><body><div class="box">'
        . '<a href="../index.html"><img src="../img/logo-rkdp.png" alt="RKDP spółka doradztwa podatkowego" height="48"></a>'
        . '<h1>' . h($title) . '</h1>' . $html
        . '<p><a class="btn" href="../index.html">Wróć na stronę główną</a></p></div></body></html>';
    exit;
}
