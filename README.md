# rkdp.pl – strona RKDP spółka doradztwa podatkowego

Strona internetowa kancelarii RKDP spółka doradztwa podatkowego sp. z o.o. (www.rkdp.pl).

## Zawartość

| Ścieżka | Opis |
|---|---|
| `index.html` | Strona główna (responsywna, z rezerwacją konsultacji przez Kalendarz Google) |
| `polityka-prywatnosci.html` | Polityka prywatności (RODO) |
| `regulamin-newslettera.html` | Regulamin newslettera i promocji „15% na kolejną usługę” |
| `img/` | Logo, zdjęcie, ikona strony |
| `dokumenty/` | Dokumenty PDF podlinkowane w stopce (AML, procedura dla sygnalistów, regulamin) |
| `newsletter/` | Zapis do newslettera (PHP): double opt-in, kod rabatowy, powiadomienia na kancelaria@rkdp.pl, rejestr zgód |

## Wymagania hostingu

- Statyczne pliki HTML działają na każdym hostingu.
- Folder `newsletter/` wymaga **PHP 8.0+** z działającą funkcją `mail()` oraz serwera Apache (pliki `.htaccess` blokują dostęp do konfiguracji i rejestru zgód).
- Katalog `newsletter/data/` musi mieć prawo zapisu dla PHP.
- Hostingi statyczne (GitHub Pages, Vercel bez dodatkowej konfiguracji, Netlify) **nie uruchomią** PHP – formularz newslettera nie będzie tam działał.

## Newsletter – konfiguracja

Ustawienia są w `newsletter/config.php` (adres powiadomień, nadawca, rabat, treść zgód).
Tajny klucz **nie jest** w repozytorium: przy pierwszym zapisie skrypt generuje go sam i zapisuje w `newsletter/data/secret.php`
(albo można go podać w zmiennej środowiskowej `RKDP_NEWSLETTER_SECRET`).

Rejestr zgód: `newsletter/data/rejestr-zgod.csv` na serwerze (pobierany przez FTP, wyłączony z Gita).

Jeśli zmienisz treść zgód, zmień ją w **dwóch miejscach**: w `index.html` (formularz) i w `newsletter/config.php`, oraz podnieś `CONSENT_VERSION`.
