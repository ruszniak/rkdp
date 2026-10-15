# rkdp.pl – strona RKDP spółka doradztwa podatkowego

Strona internetowa kancelarii RKDP spółka doradztwa podatkowego sp. z o.o. (www.rkdp.pl), publikowana na **Vercelu**.
Strona jest w pełni statyczna – nie wymaga żadnych zmiennych środowiskowych ani kroku budowania.

| Ścieżka | Opis |
|---|---|
| `index.html` | Strona główna; fragmenty między `<!-- gen:... -->` uzupełnia generator |
| `<slug>/index.html` | 16 podstron usługowych i lokalnych (generowane) |
| `zespol/`, `cennik/` | Zakładki Zespół i Cennik (generowane z `tools/partials/`) |
| `css/site.css` | Wspólne style podstron |
| `polityka-prywatnosci.html`, `aml.html` | RODO i informacje AML |
| `img/`, `dokumenty/` | Obrazy i dokumenty PDF |
| `sitemap.xml`, `robots.txt` | Mapa strony (generowana) i plik dla wyszukiwarek |
| `tools/` | Generator i treści podstron (nie są publikowane – `.vercelignore`) |

## Jak edytować treści

1. Teksty podstron są w `tools/content_doradztwo.py`, `tools/content_ksiegowosc.py`, `tools/content_lokalne.py`, `tools/content_extra.py`.
2. Po zmianie uruchom `python3 tools/build.py` – przebuduje podstrony, Zespół, Cennik, sitemapę oraz menu, kafelki i stopkę na stronie głównej.
3. Pełne karty zespołu i cennika są w `tools/partials/zespol.html` i `tools/partials/cennik.html` (strona główna ma ich skrócone wersje).
