<?php
date_default_timezone_set('Europe/Warsaw');
/**
 * Newsletter RKDP – konfiguracja.
 * Ten plik jest chroniony przed dostępem z przeglądarki (.htaccess).
 */

// Adres, na który trafiają powiadomienia o zapisach, potwierdzeniach i rezygnacjach.
const OWNER_EMAIL = 'kancelaria@rkdp.pl';

// Nadawca wiadomości wysyłanych do subskrybentów. Powinien być w domenie rkdp.pl,
// żeby poczta nie trafiała do spamu.
const FROM_EMAIL = 'kancelaria@rkdp.pl';
const FROM_NAME  = 'RKDP – Kancelaria Ruszniak';

// Adres strony (bez ukośnika na końcu).
const SITE_URL = 'https://rkdp.pl';

// TAJNY KLUCZ – nie jest przechowywany w repozytorium.
// Przy pierwszym zapisie skrypt sam generuje losowy klucz i zapisuje go w data/secret.php
// (katalog chroniony przed dostępem z przeglądarki i wyłączony z Gita).
// Można go też podać w zmiennej środowiskowej RKDP_NEWSLETTER_SECRET.
// Nie zmieniaj klucza po uruchomieniu – unieważni to wysłane linki i zmieni sposób generowania kodów.
define('SECRET', (function (): string {
    $env = getenv('RKDP_NEWSLETTER_SECRET');
    if (is_string($env) && strlen($env) >= 32) return $env;
    $file = __DIR__ . '/data/secret.php';
    if (is_file($file)) {
        $s = include $file;
        if (is_string($s) && strlen($s) >= 32) return $s;
    }
    $s = rtrim(strtr(base64_encode(random_bytes(36)), '+/', '-_'), '=');
    if (!is_dir(__DIR__ . '/data')) @mkdir(__DIR__ . '/data', 0750, true);
    @file_put_contents($file, "<?php return '" . $s . "';\n", LOCK_EX);
    @chmod($file, 0640);
    return $s;
})());

// Ważność linku potwierdzającego (w godzinach).
const CONFIRM_TTL_HOURS = 72;

// Rabat.
const DISCOUNT_PERCENT = 15;
const DISCOUNT_VALID_MONTHS = 12;

// Wersja treści zgód – zmień, jeśli zmienisz ich brzmienie (trafia do rejestru zgód).
const CONSENT_VERSION = '2026-09-30';

// Treść zgód – musi być identyczna jak na stronie (index.html).
const CONSENT_NEWSLETTER = 'Wyrażam zgodę na przesyłanie mi przez RKDP spółka doradztwa podatkowego sp. z o.o. z siedzibą w Ozorzycach newslettera podatkowego zawierającego informacje handlowe, na podany adres e-mail (art. 398 ustawy – Prawo komunikacji elektronicznej), oraz na przetwarzanie w tym celu moich danych osobowych (art. 6 ust. 1 lit. a RODO). Zgodę mogę wycofać w każdej chwili.';
const CONSENT_TERMS = 'Zapoznałem/-am się z Regulaminem newslettera i promocji oraz Polityką prywatności i akceptuję ich treść.';

// Katalog z rejestrem zgód (chroniony .htaccess).
const DATA_DIR = __DIR__ . '/data';
