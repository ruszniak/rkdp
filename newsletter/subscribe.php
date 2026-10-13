<?php
/**
 * Krok 1: zapis. Wysyła do subskrybenta link potwierdzający (double opt-in).
 * Zgoda liczy się dopiero po kliknięciu linku.
 */
require_once __DIR__ . '/lib.php';

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');

function respond(bool $ok, string $msg, bool $json): void {
    if ($json) {
        header('Content-Type: application/json; charset=UTF-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'message' => $msg], JSON_UNESCAPED_UNICODE);
        exit;
    }
    header('Location: ../index.html?newsletter=' . ($ok ? 'wyslano' : 'blad') . '#newsletter', true, 303);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') respond(false, 'Nieprawidłowe żądanie.', $wantsJson);

// Ochrona przed botami: ukryte pole i minimalny czas wypełniania.
if (!empty($_POST['website'])) respond(true, 'Dziękujemy!', $wantsJson);
$started = (int)($_POST['ts'] ?? 0);
if ($started > 0 && (time() * 1000 - $started) < 2500) respond(false, 'Spróbuj ponownie za chwilę.', $wantsJson);

$email = trim((string)($_POST['email'] ?? ''));
$name  = trim(mb_substr(strip_tags((string)($_POST['name'] ?? '')), 0, 60));
$name  = preg_replace('/[\r\n]+/', ' ', $name);

if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 254) {
    respond(false, 'Podaj poprawny adres e-mail.', $wantsJson);
}
if (empty($_POST['consent_newsletter']) || empty($_POST['consent_terms'])) {
    respond(false, 'Aby się zapisać, zaznacz obie wymagane zgody.', $wantsJson);
}

$token = make_token(['e' => strtolower($email), 'n' => $name, 't' => time(), 'a' => 'confirm']);
$link  = SITE_URL . '/newsletter/confirm.php?t=' . urlencode($token);
$hi    = $name !== '' ? 'Dzień dobry ' . $name . ',' : 'Dzień dobry,';

$html = email_layout('Potwierdź zapis do newslettera',
    '<p style="font-size:15px;line-height:1.7;color:#4A433B;margin:0 0 12px">' . h($hi) . '</p>'
  . '<p style="font-size:15px;line-height:1.7;color:#4A433B;margin:0 0 12px">dziękujemy za zapis do newslettera podatkowego RKDP. Kliknij przycisk poniżej, aby potwierdzić adres e-mail. Po potwierdzeniu otrzymasz kod rabatowy <strong>' . DISCOUNT_PERCENT . '%</strong> na kolejną usługę podatkową.</p>'
  . button($link, 'Potwierdzam zapis')
  . '<p style="font-size:13px;line-height:1.6;color:#6A6157;margin:0">Link jest ważny przez ' . CONFIRM_TTL_HOURS . ' godziny. Jeśli to nie Ty zapisałeś/-aś się do newslettera, zignoruj tę wiadomość – bez potwierdzenia nie będziemy wysyłać żadnych wiadomości.</p>');
$text = "$hi\n\ndziękujemy za zapis do newslettera podatkowego RKDP. Aby potwierdzić adres e-mail i otrzymać kod rabatowy " . DISCOUNT_PERCENT . "%, otwórz link:\n$link\n\nLink jest ważny przez " . CONFIRM_TTL_HOURS . " godziny. Jeśli to nie Ty, zignoruj tę wiadomość.\n\nRKDP spółka doradztwa podatkowego sp. z o.o.";

$sent = send_mail($email, 'Potwierdź zapis do newslettera RKDP', $html, $text);
log_event('zapis_oczekuje_na_potwierdzenie', $email, $name, $sent ? '' : 'BLAD_WYSYLKI');

if (!$sent) respond(false, 'Nie udało się wysłać wiadomości. Spróbuj ponownie lub napisz na ' . OWNER_EMAIL . '.', $wantsJson);
respond(true, 'Sprawdź skrzynkę – wysłaliśmy link potwierdzający. Kod rabatowy otrzymasz po kliknięciu linku.', $wantsJson);
