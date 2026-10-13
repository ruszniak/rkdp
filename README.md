# rkdp.pl – strona RKDP spółka doradztwa podatkowego

Strona internetowa kancelarii RKDP spółka doradztwa podatkowego sp. z o.o. (www.rkdp.pl), publikowana na **Vercelu**.

## Zawartość

| Ścieżka | Opis |
|---|---|
| `index.html` | Strona główna (responsywna, z rezerwacją konsultacji przez Kalendarz Google i zapisem do newslettera) |
| `polityka-prywatnosci.html` | Polityka prywatności (RODO) |
| `regulamin-newslettera.html` | Regulamin newslettera i promocji „15% na kolejną usługę” |
| `img/` | Logo, zdjęcie, ikona strony |
| `dokumenty/` | Dokumenty PDF podlinkowane w stopce (AML, procedura dla sygnalistów, regulamin) |
| `api/newsletter/` | Funkcje serverless Vercela: zapis, potwierdzenie (double opt-in), wypisanie |
| `lib/newsletter.js` | Wspólna logika newslettera: tokeny, kody rabatowe, wysyłka maili, treść zgód |

## Jak działa newsletter

1. Formularz na stronie wysyła dane do `/api/newsletter/subscribe` – subskrybent dostaje maila z linkiem potwierdzającym.
2. Link prowadzi do `/api/newsletter/confirm`, gdzie subskrybent klika „Potwierdzam” – dostaje kod rabatowy (na stronie i mailem),
   a na `kancelaria@rkdp.pl` przychodzi powiadomienie z pełnym zapisem zgody (data, IP, przeglądarka, treść zgód, kod).
   **Te powiadomienia są rejestrem zgód – nie usuwaj ich.**
3. Każdy mail do subskrybenta zawiera link do `/api/newsletter/unsubscribe` – po rezygnacji przychodzi powiadomienie na `kancelaria@rkdp.pl`.

Kod rabatowy jest stały dla danego adresu e-mail (wyliczany z adresu i tajnego klucza), więc nie wymaga bazy danych.

## Zmienne środowiskowe (Vercel → Project → Settings → Environment Variables)

| Zmienna | Wymagana | Opis |
|---|---|---|
| `NEWSLETTER_SECRET` | tak | Długi losowy ciąg (min. 32 znaki). Podpisuje linki i generuje kody. **Nie zmieniaj po uruchomieniu.** |
| `SMTP_HOST` | tak | Serwer poczty wychodzącej skrzynki kancelaria@rkdp.pl (z panelu hostingu poczty) |
| `SMTP_PORT` | nie | Domyślnie `465` (SSL). Dla STARTTLS ustaw `587`. |
| `SMTP_USER` | tak | Login skrzynki, zwykle `kancelaria@rkdp.pl` |
| `SMTP_PASS` | tak | Hasło skrzynki |
| `NEWSLETTER_OWNER_EMAIL` | nie | Adres powiadomień, domyślnie `kancelaria@rkdp.pl` |
| `NEWSLETTER_FROM_EMAIL` | nie | Nadawca maili, domyślnie `kancelaria@rkdp.pl` (musi być zgodny z `SMTP_USER`) |
| `SITE_URL` | nie | Adres strony w linkach z maili, domyślnie `https://rkdp.pl` |

Po dodaniu lub zmianie zmiennych trzeba ponownie wdrożyć projekt (Deployments → Redeploy).

## Zmiana treści zgód

Treść zgód jest w **dwóch miejscach**: w formularzu w `index.html` i w `lib/newsletter.js`. Zmień ją w obu i podnieś `CONSENT_VERSION`.
