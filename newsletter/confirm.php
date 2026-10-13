<?php
/**
 * Krok 2: potwierdzenie (double opt-in).
 * Subskrybent dostaje kod rabatowy, a kancelaria – powiadomienie z pełnym zapisem zgód.
 */
require_once __DIR__ . '/lib.php';

$data = read_token((string)($_GET['t'] ?? ''));
if (!$data || ($data['a'] ?? '') !== 'confirm' || empty($data['e'])) {
    result_page('Nieprawidłowy link', '<p>Ten link potwierdzający jest nieprawidłowy. Zapisz się ponownie na stronie.</p>');
}
if (time() - (int)$data['t'] > CONFIRM_TTL_HOURS * 3600) {
    result_page('Link wygasł', '<p>Link potwierdzający wygasł. Zapisz się ponownie na stronie – wyślemy nowy.</p>');
}

$email = $data['e'];
$name  = (string)($data['n'] ?? '');
$code  = discount_code($email);
$validUntil = date('d.m.Y', strtotime('+' . DISCOUNT_VALID_MONTHS . ' months'));
$unsub = SITE_URL . '/newsletter/unsubscribe.php?t=' . urlencode(make_token(['e' => $email, 'a' => 'unsub']));
$now   = date('d.m.Y H:i:s');

// Ten sam link może zostać kliknięty kilka razy – maile wysyłamy tylko przy pierwszym potwierdzeniu.
$marker = DATA_DIR . '/potwierdzone-' . hash('sha256', $email . SECRET) . '.flag';
$unsubMarker = DATA_DIR . '/wypisani-' . hash('sha256', $email . SECRET) . '.flag';
// Ponowny zapis po wcześniejszej rezygnacji traktujemy jak nową zgodę.
$first  = !file_exists($marker) || file_exists($unsubMarker);
if ($first && file_exists($unsubMarker)) @unlink($unsubMarker);

if ($first) {
    if (!is_dir(DATA_DIR)) @mkdir(DATA_DIR, 0750, true);
    @file_put_contents($marker, date('c'));
    log_event('zgoda_potwierdzona', $email, $name, 'kod=' . $code);

    // Mail do subskrybenta z kodem.
    $hi = $name !== '' ? 'Dzień dobry ' . $name . ',' : 'Dzień dobry,';
    $html = email_layout('Twój kod rabatowy ' . DISCOUNT_PERCENT . '%',
        '<p style="font-size:15px;line-height:1.7;color:#4A433B;margin:0 0 12px">' . h($hi) . '</p>'
      . '<p style="font-size:15px;line-height:1.7;color:#4A433B;margin:0 0 12px">dziękujemy za potwierdzenie zapisu do newslettera podatkowego RKDP. Oto Twój kod rabatowy na kolejną usługę podatkową:</p>'
      . '<p style="margin:20px 0"><span style="display:inline-block;font-size:24px;font-weight:bold;letter-spacing:2px;color:#7A5A37;border:2px dashed #7A5A37;border-radius:12px;padding:12px 20px">' . h($code) . '</span></p>'
      . '<p style="font-size:14px;line-height:1.7;color:#4A433B;margin:0 0 12px">Kod daje <strong>' . DISCOUNT_PERCENT . '% rabatu</strong> na wynagrodzenie za jedną kolejną usługę podatkową. Podaj go przy zleceniu usługi. Kod jest ważny do <strong>' . $validUntil . '</strong>. Szczegóły w <a href="' . h(SITE_URL . '/regulamin-newslettera.html') . '" style="color:#7A5A37">Regulaminie newslettera i promocji</a>.</p>'
      . button(SITE_URL . '/#termin', 'Umów konsultację')
      . '<p style="font-size:12px;line-height:1.6;color:#6A6157;margin:0">Nie chcesz otrzymywać newslettera? <a href="' . h($unsub) . '" style="color:#6A6157">Wypisz się</a> w dowolnej chwili.</p>');
    $text = "$hi\n\ndziękujemy za potwierdzenie zapisu do newslettera podatkowego RKDP.\n\nTwój kod rabatowy: $code\n" . DISCOUNT_PERCENT . "% rabatu na wynagrodzenie za jedną kolejną usługę podatkową, ważny do $validUntil.\nRegulamin: " . SITE_URL . "/regulamin-newslettera.html\n\nWypisanie z newslettera: $unsub\n\nRKDP spółka doradztwa podatkowego sp. z o.o.";
    send_mail($email, 'Twój kod rabatowy ' . DISCOUNT_PERCENT . '% – RKDP', $html, $text);

    // Powiadomienie do kancelarii – zapis zgody jako dowód (rozliczalność, art. 7 ust. 1 RODO).
    $rows = [
        'E-mail' => $email,
        'Imię' => $name !== '' ? $name : '—',
        'Data i godzina potwierdzenia' => $now,
        'Adres IP' => client_ip(),
        'Przeglądarka' => user_agent(),
        'Sposób wyrażenia zgody' => 'formularz na rkdp.pl + potwierdzenie linkiem z e-maila (double opt-in)',
        'Wersja treści zgód' => CONSENT_VERSION,
        'Zgoda 1 (newsletter / informacje handlowe)' => CONSENT_NEWSLETTER,
        'Zgoda 2 (regulamin i polityka prywatności)' => CONSENT_TERMS,
        'Przyznany kod rabatowy' => $code . ' (' . DISCOUNT_PERCENT . '%, ważny do ' . $validUntil . ')',
    ];
    $tbl = '<table cellpadding="0" cellspacing="0" style="width:100%;font-size:14px;border-collapse:collapse">';
    $txt = '';
    foreach ($rows as $k => $v) {
        $tbl .= '<tr><td style="padding:8px 12px 8px 0;border-bottom:1px solid #E3D9CA;color:#6A6157;vertical-align:top;width:38%">' . h($k) . '</td><td style="padding:8px 0;border-bottom:1px solid #E3D9CA;color:#1D1A16">' . h($v) . '</td></tr>';
        $txt .= "$k: $v\n";
    }
    $tbl .= '</table>';
    send_mail(OWNER_EMAIL, 'Newsletter: nowa zgoda – ' . $email,
        email_layout('Nowy subskrybent newslettera', '<p style="font-size:15px;color:#4A433B;margin:0 0 16px">Subskrybent potwierdził zapis. Zachowaj tę wiadomość jako dowód wyrażenia zgody.</p>' . $tbl),
        "Nowy subskrybent newslettera (zgoda potwierdzona)\n\n$txt", $email);
}

result_page('Zapis potwierdzony',
    '<p>Dziękujemy! Twój adres został potwierdzony. Oto Twój kod rabatowy na kolejną usługę podatkową – wysłaliśmy go również e-mailem:</p>'
  . '<div class="code">' . h($code) . '</div>'
  . '<p>' . DISCOUNT_PERCENT . '% rabatu na wynagrodzenie za jedną kolejną usługę podatkową. Kod podaj przy zleceniu usługi. Szczegóły w <a href="../regulamin-newslettera.html">Regulaminie newslettera i promocji</a>.</p>');
