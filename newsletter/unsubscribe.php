<?php
/**
 * Wypisanie z newslettera (wycofanie zgody) – jednym kliknięciem z linku w mailu.
 */
require_once __DIR__ . '/lib.php';

$data = read_token((string)($_GET['t'] ?? ''));
if (!$data || ($data['a'] ?? '') !== 'unsub' || empty($data['e'])) {
    result_page('Nieprawidłowy link', '<p>Nie udało się rozpoznać linku. Aby wypisać się z newslettera, napisz na <a href="mailto:' . h(OWNER_EMAIL) . '">' . h(OWNER_EMAIL) . '</a>.</p>');
}
$email = $data['e'];

// Pierwsze wejście pokazuje przycisk, a dopiero kliknięcie (POST) wypisuje – chroni to
// przed przypadkowym wypisaniem przez skanery linków w programach pocztowych.
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    result_page('Wypisanie z newslettera',
        '<p>Czy na pewno chcesz wypisać adres <strong>' . h($email) . '</strong> z newslettera podatkowego RKDP?</p>'
      . '<form method="post"><button type="submit" style="font:inherit;font-weight:600;cursor:pointer;border:0;background:#1D1A16;color:#fff;padding:14px 24px;border-radius:999px">Tak, wypisz mnie</button></form>');
}

$marker = DATA_DIR . '/wypisani-' . hash('sha256', $email . SECRET) . '.flag';
if (!file_exists($marker)) {
    if (!is_dir(DATA_DIR)) @mkdir(DATA_DIR, 0750, true);
    @file_put_contents($marker, date('c'));
    log_event('zgoda_wycofana', $email);
    send_mail(OWNER_EMAIL, 'Newsletter: rezygnacja – ' . $email,
        email_layout('Rezygnacja z newslettera', '<p style="font-size:15px;color:#4A433B">Adres <strong>' . h($email) . '</strong> wycofał zgodę i wypisał się z newslettera (' . date('d.m.Y H:i:s') . ', IP ' . h(client_ip()) . '). Usuń go z listy wysyłkowej.</p>'),
        "Adres $email wypisał się z newslettera (" . date('d.m.Y H:i:s') . "). Usuń go z listy wysyłkowej.");
}

result_page('Wypisano z newslettera', '<p>Adres <strong>' . h($email) . '</strong> został wypisany. Nie będziemy wysyłać już newslettera. Otrzymany wcześniej kod rabatowy pozostaje ważny.</p>');
