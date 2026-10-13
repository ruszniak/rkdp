# -*- coding: utf-8 -*-
# Podstrony księgowe i lokalne rkdp.pl

PAGES = []

PAGES.append(dict(
slug="ksiegowosc-spolki-z-o-o", group="Księgowość", short="Księgowość spółki z o.o.",
nav_desc="Pełna księgowość pod nadzorem doradcy",
title="Księgowość spółki z o.o. Wrocław – pełna księgowość z doradcą podatkowym | RKDP",
meta="Pełna księgowość spółki z o.o. we Wrocławiu prowadzona pod nadzorem doradcy podatkowego: księgi rachunkowe, VAT i JPK, KSeF, CIT i estoński CIT, sprawozdanie finansowe.",
eyebrow="Księgowość pod nadzorem doradcy",
h1="Księgowość spółki z o.o. we Wrocławiu",
lead="Prowadzimy pełną księgowość spółek – a każde rozliczenie nadzoruje doradca podatkowy. Gdy pojawia się pytanie podatkowe albo pismo z urzędu, nie musisz szukać pomocy gdzie indziej.",
body="""
<h2>Co obejmuje obsługa</h2>
<ul>
<li><strong>Księgi rachunkowe</strong> zgodnie z ustawą o rachunkowości, polityka rachunkowości i plan kont dopasowane do spółki.</li>
<li><strong>VAT</strong> – ewidencje, JPK_V7, rozliczenia transakcji unijnych i importu, VAT-UE.</li>
<li><strong>KSeF</strong> – obieg faktur ustrukturyzowanych i uprawnienia w Krajowym Systemie e-Faktur.</li>
<li><strong>CIT</strong> – zaliczki, zeznanie CIT-8, estoński CIT (CIT-8E), ceny transferowe w podstawowym zakresie.</li>
<li><strong>Raportowanie JPK</strong> – w tym nowe obowiązki raportowania ksiąg w strukturze JPK_CIT.</li>
<li><strong>Sprawozdanie finansowe</strong> – sporządzenie, przygotowanie uchwał i złożenie do KRS oraz do Szefa KAS.</li>
<li><strong>Kadry i płace</strong> – jeśli spółka zatrudnia, zobacz <a href="/kadry-i-place">kadry i płace</a>.</li>
<li><strong>Kontakt z urzędem</strong> – odpowiedzi na wezwania i <a href="/czynnosci-sprawdzajace">czynności sprawdzające</a> przygotowuje doradca podatkowy.</li>
</ul>

<h2>Kalendarz spółki – najważniejsze terminy</h2>
<div class="law">
<div><b>do 25. dnia</b>JPK_V7 i VAT za poprzedni miesiąc</div>
<div><b>do 20. dnia</b>zaliczka na CIT i PIT od wynagrodzeń</div>
<div><b>3 miesiące</b>od końca roku: sprawozdanie finansowe i CIT-8</div>
<div><b>6 miesięcy</b>od końca roku: zatwierdzenie sprawozdania, potem 15 dni na złożenie do KRS</div>
</div>
<p>Pilnujemy tych terminów za Ciebie i przypominamy o dokumentach, które potrzebujemy od spółki – np. o uchwałach zgromadzenia wspólników czy podpisach zarządu pod sprawozdaniem.</p>

<h2>Księgowość z doradcą – co to zmienia</h2>
<p>Biuro rachunkowe księguje to, co dostanie. Doradca podatkowy patrzy dalej: czy umowa z kontrahentem nie rodzi ryzyka, czy wypłata dla wspólnika jest najtańsza z możliwych, czy nie warto przejść na estoński CIT, czy dokumentacja obroni się w razie kontroli. W RKDP te dwie perspektywy są w jednym miejscu:</p>
<ul>
<li>doradca przegląda kluczowe rozliczenia i zamknięcie roku,</li>
<li>pytania podatkowe zadajesz tej samej kancelarii, która prowadzi księgi,</li>
<li>w razie <a href="/kontrola-podatkowa">kontroli</a> doradca reprezentuje spółkę jako pełnomocnik – z pełną znajomością ksiąg,</li>
<li>przy decyzjach o <a href="/wyplata-pieniedzy-ze-spolki">wypłacie pieniędzy ze spółki</a> masz wyliczenia na bieżących danych.</li>
</ul>

<h2>Jak wygląda współpraca</h2>
<ol>
<li><strong>Bezpłatna rozmowa do 20 minut</strong> – poznajemy spółkę i przygotowujemy wycenę.</li>
<li><strong>Umowa i pełnomocnictwa</strong> – do urzędu skarbowego, ZUS, KSeF i e-sprawozdań.</li>
<li><strong>Przejęcie dokumentacji</strong> – jeśli zmieniasz biuro, zajmujemy się tym za Ciebie (zobacz <a href="/zmiana-biura-rachunkowego">zmiana biura rachunkowego</a>).</li>
<li><strong>Stały obieg dokumentów</strong> – elektronicznie, z KSeF i bankowości; papierowe dokumenty możesz zostawić w kancelarii na Jagodnie.</li>
<li><strong>Miesięczne podsumowanie</strong> – kwoty podatków do zapłaty i najważniejsze informacje o wyniku.</li>
</ol>

<h2>Od czego zależy cena księgowości spółki</h2>
<p>Cenę ustalamy indywidualnie. Wpływają na nią przede wszystkim:</p>
<ul>
<li>liczba dokumentów księgowych w miesiącu,</li>
<li>rejestracja do VAT, transakcje zagraniczne i waluty,</li>
<li>liczba pracowników i zleceniobiorców,</li>
<li>forma opodatkowania – klasyczny CIT czy estoński CIT,</li>
<li>dodatkowe obowiązki: ceny transferowe, środki trwałe, magazyn, projekty z dotacji.</li>
</ul>
""",
faqs=[
("Ile kosztuje księgowość spółki z o.o.?","Nie podajemy cennika, bo koszt zależy głównie od liczby dokumentów, VAT, pracowników i formy opodatkowania. Wycenę przygotowujemy po krótkiej rozmowie – pierwsze 20 minut jest bezpłatne."),
("Czy prowadzicie księgowość spółek na estońskim CIT?","Tak. Pilnujemy warunków estońskiego CIT, ukrytych zysków i rozliczeń CIT-8E, a doradca pomaga ocenić, czy ta forma nadal się opłaca."),
("Czy muszę przynosić dokumenty do biura?","Nie. Większość dokumentów trafia do nas elektronicznie – z KSeF, bankowości i e-maila. Dokumenty papierowe możesz zostawić w kancelarii na Jagodnie."),
("Kto przygotuje sprawozdanie finansowe?","My – razem z projektami uchwał i e-sprawozdaniem. Zarząd musi je podpisać, a zgromadzenie wspólników zatwierdzić."),
],
related=["wyplata-pieniedzy-ze-spolki","zmiana-biura-rachunkowego","kadry-i-place"],
posts=["ksef-w-malej-firmie","estonski-cit-dla-kogo"],
))

PAGES.append(dict(
slug="ksiegowosc-jdg", group="Księgowość", short="Księgowość JDG (KPiR, ryczałt)",
nav_desc="KPiR, ryczałt, ZUS i PIT dla firm",
title="Księgowość JDG Wrocław – KPiR, ryczałt, ZUS | RKDP biuro z doradcą podatkowym",
meta="Księgowość jednoosobowej działalności we Wrocławiu: KPiR, ewidencja ryczałtu, VAT i KSeF, ZUS i składka zdrowotna, PIT roczny. Pod nadzorem doradcy podatkowego.",
eyebrow="Księgowość pod nadzorem doradcy",
h1="Księgowość jednoosobowej działalności (JDG) we Wrocławiu",
lead="Prowadzimy podatkową księgę przychodów i rozchodów oraz ewidencję ryczałtu dla przedsiębiorców – z doradcą podatkowym, który pomaga wybrać formę opodatkowania i reprezentuje Cię, gdy urząd ma pytania.",
body="""
<h2>Co robimy dla JDG</h2>
<ul>
<li><strong>KPiR lub ewidencja przychodów</strong> (ryczałt) – prowadzona elektronicznie, zgodnie z nowymi wymogami przesyłania ewidencji w JPK.</li>
<li><strong>Zaliczki na PIT</strong> – na skali, podatku liniowym lub ryczałcie, miesięcznie albo kwartalnie.</li>
<li><strong>VAT</strong> – JPK_V7, transakcje unijne, odwrotne obciążenie, zwroty VAT.</li>
<li><strong>KSeF</strong> – pomoc we wdrożeniu i obieg faktur ustrukturyzowanych (zobacz <a href="/blog/ksef-w-malej-firmie">KSeF w małej firmie</a>).</li>
<li><strong>ZUS</strong> – składki społeczne i składka zdrowotna, ulga na start, mały ZUS plus, preferencyjne składki.</li>
<li><strong>Zeznanie roczne</strong> – PIT-36, PIT-36L lub PIT-28, ulgi i rozliczenie z małżonkiem.</li>
<li><strong>Środki trwałe i samochód w firmie</strong> – ewidencja, amortyzacja, limity kosztów.</li>
</ul>

<h2>Doradca przy wyborze formy opodatkowania</h2>
<p>W JDG forma opodatkowania wpływa nie tylko na PIT, ale też na składkę zdrowotną – a zmienić ją można zwykle raz w roku. Przed końcem roku przygotowujemy dla klientów porównanie skali, podatku liniowego i ryczałtu na ich danych. Gdy dochody rosną, pokazujemy też, czy i kiedy warto przejść do spółki (zobacz <a href="/forma-opodatkowania">forma opodatkowania</a>).</p>
<div class="law">
<div><b>do 20. dnia</b>zaliczka na PIT i składki ZUS za poprzedni miesiąc</div>
<div><b>do 25. dnia</b>JPK_V7 i VAT</div>
<div><b>do 20. dnia</b>po pierwszym przychodzie – wybór formy opodatkowania na rok</div>
<div><b>do 30 kwietnia</b>zeznanie roczne PIT-36, PIT-36L lub PIT-28</div>
</div>

<h2>Dla kogo</h2>
<p>Dla przedsiębiorców, którzy chcą mieć spokój z rozliczeniami i dostęp do doradcy, gdy pojawi się nietypowa sytuacja: duża faktura zagraniczna, zakup samochodu, sprzedaż środka trwałego, wezwanie z urzędu. Pracujemy z branżami usługowymi, budowlanymi, handlem, IT, wolnymi zawodami i lekarzami.</p>

<h2>Gdy przychodzi pismo z urzędu</h2>
<p>Jeśli urząd skarbowy wezwie Cię do wyjaśnień rozbieżności w JPK albo zawiadomi o kontroli, nie zostajesz sam z księgową. Doradca podatkowy przygotowuje odpowiedź i – jako pełnomocnik – prowadzi <a href="/czynnosci-sprawdzajace">czynności sprawdzające</a> lub <a href="/kontrola-podatkowa">kontrolę</a>.</p>

<h2>Jak zacząć</h2>
<ol>
<li>Bezpłatna rozmowa do 20 minut i wycena.</li>
<li>Pełnomocnictwa do urzędu skarbowego, ZUS i KSeF.</li>
<li>Przejęcie dokumentów od poprzedniego biura (jeśli je zmieniasz) – zobacz <a href="/zmiana-biura-rachunkowego">zmiana biura rachunkowego</a>.</li>
<li>Comiesięczna informacja o kwotach PIT, VAT i ZUS do zapłaty.</li>
</ol>

<h2>Od czego zależy cena</h2>
<p>Od liczby dokumentów, rejestracji do VAT, transakcji zagranicznych, zatrudnienia pracowników oraz formy opodatkowania. Wycenę przygotowujemy po krótkiej rozmowie.</p>
""",
faqs=[
("Czy mogę zmienić formę opodatkowania z liniowego na ryczałt?","Tak, ale co do zasady od nowego roku – składając oświadczenie do 20. dnia miesiąca po pierwszym przychodzie w roku. Przed zmianą warto porównać podatek i składkę zdrowotną w obu wariantach."),
("Czy prowadzicie księgowość dla lekarzy i wolnych zawodów?","Tak. Prowadzimy rozliczenia lekarzy, prawników, architektów i innych wolnych zawodów, także przy współpracy kilku przedsiębiorców w spółce cywilnej."),
("Czy muszę mieć KSeF w jednoosobowej działalności?","Większość przedsiębiorców ma obowiązek wystawiania faktur w KSeF, a przepisy przewidywały okresy przejściowe dla najmniejszych firm. Sprawdzamy, jakie terminy dotyczą Twojej działalności."),
],
related=["forma-opodatkowania","zmiana-biura-rachunkowego","czynnosci-sprawdzajace"],
posts=["jdg-czy-spolka-z-o-o","ksef-w-malej-firmie"],
))

PAGES.append(dict(
slug="kadry-i-place", group="Księgowość", short="Kadry i płace",
nav_desc="Umowy, listy płac, ZUS, PPK",
title="Kadry i płace Wrocław – obsługa kadrowo-płacowa firm | RKDP",
meta="Obsługa kadrowo-płacowa we Wrocławiu: umowy o pracę i cywilnoprawne, listy płac, ZUS i PIT pracowników, PPK, akta osobowe. Pod nadzorem doradcy podatkowego.",
eyebrow="Księgowość pod nadzorem doradcy",
h1="Kadry i płace dla firm we Wrocławiu",
lead="Prowadzimy sprawy kadrowe i płacowe małych i średnich firm – od umowy z pierwszym pracownikiem po roczne rozliczenia. Podatkowe wątpliwości wokół wynagrodzeń rozstrzyga doradca podatkowy.",
body="""
<h2>Zakres obsługi</h2>
<ul>
<li><strong>Umowy</strong> – o pracę, zlecenia, o dzieło, kontrakty menedżerskie i powołania członków zarządu; aneksy i świadectwa pracy.</li>
<li><strong>Listy płac</strong> – wynagrodzenia, nadgodziny, premie, nieobecności, zasiłki chorobowe i macierzyńskie.</li>
<li><strong>ZUS</strong> – zgłoszenia i wyrejestrowania, deklaracje rozliczeniowe, korekty.</li>
<li><strong>PIT pracowników</strong> – zaliczki, PIT-11 i PIT-4R, ulgi i zwolnienia (np. dla młodych).</li>
<li><strong>PPK</strong> – zapisy, wpłaty, rezygnacje i automatyczne zapisy.</li>
<li><strong>Akta osobowe</strong> – w postaci papierowej lub elektronicznej, ewidencja czasu pracy i urlopów.</li>
<li><strong>Raporty i zaświadczenia</strong> – dla banków, GUS i PFRON.</li>
</ul>

<h2>Gdzie przydaje się doradca podatkowy</h2>
<p>Wynagrodzenia to obszar, w którym łatwo o kosztowny błąd – i w podatku, i w składkach. Doradca pomaga m.in. przy:</p>
<ul>
<li>wyborze formy zatrudnienia członka zarządu i wspólnika (zobacz <a href="/wyplata-pieniedzy-ze-spolki">wypłata pieniędzy ze spółki</a>),</li>
<li>świadczeniach dla pracowników – samochód służbowy, telefon, benefity, pakiety medyczne – i ich opodatkowaniu,</li>
<li>pracy zdalnej i podróżach służbowych, w tym zagranicznych,</li>
<li>zatrudnianiu cudzoziemców i pracowników delegowanych,</li>
<li>kontrolach ZUS i odwołaniach od decyzji ZUS.</li>
</ul>
<div class="law">
<div><b>do 15. dnia</b>składki ZUS za pracowników (firmy z osobowością prawną)</div>
<div><b>do 20. dnia</b>zaliczki na PIT od wynagrodzeń</div>
<div><b>do końca lutego</b>PIT-11 dla pracowników i zleceniobiorców</div>
<div><b>do 31 stycznia</b>PIT-4R za poprzedni rok</div>
</div>

<h2>Jak pracujemy</h2>
<ol>
<li>Ustalamy zasady obiegu informacji – kto przekazuje dane o czasie pracy, nieobecnościach i premiach.</li>
<li>Przygotowujemy listy płac i przelewy do zatwierdzenia przez Ciebie.</li>
<li>Rozliczamy ZUS i PIT w terminach i przekazujemy pracownikom paski płacowe.</li>
<li>Prowadzimy dokumentację kadrową i pilnujemy terminów badań i szkoleń okresowych (we współpracy z Twoim specjalistą BHP).</li>
</ol>

<h2>Od czego zależy cena</h2>
<p>Od liczby pracowników i zleceniobiorców, systemu czasu pracy, liczby składników wynagrodzeń oraz tego, czy prowadzimy też akta osobowe. Kadry i płace prowadzimy zarówno dla klientów, którym prowadzimy księgowość, jak i dla firm, których księgi prowadzi inne biuro.</p>
""",
faqs=[
("Czy obsłużycie firmę z jednym pracownikiem?","Tak. Obsługujemy zarówno mikrofirmy z jednym pracownikiem, jak i spółki zatrudniające kilkadziesiąt osób."),
("Czy pomożecie przy kontroli ZUS?","Tak. Przygotowujemy dokumenty i wyjaśnienia, a od decyzji ZUS – odwołanie do sądu."),
("Czy mogę mieć kadry u was, a księgowość w innym biurze?","Tak, choć najwygodniej, gdy obie usługi są w jednym miejscu – listy płac od razu trafiają do ksiąg."),
],
related=["ksiegowosc-spolki-z-o-o","ksiegowosc-jdg","wyplata-pieniedzy-ze-spolki"],
posts=["wynagrodzenie-wspolnika-art-176-ksh","zmiana-biura-rachunkowego"],
))

PAGES.append(dict(
slug="zmiana-biura-rachunkowego", group="Księgowość", short="Zmiana biura rachunkowego",
nav_desc="Przejęcie księgowości bez przerwy",
title="Zmiana biura rachunkowego Wrocław – przejęcie księgowości bez przerwy | RKDP",
meta="Chcesz zmienić biuro rachunkowe? Przejmujemy księgowość spółki lub JDG od poprzedniego biura: pełnomocnictwa, dokumentacja, weryfikacja rozliczeń. Pod nadzorem doradcy podatkowego.",
eyebrow="Księgowość pod nadzorem doradcy",
h1="Zmiana biura rachunkowego – przejmujemy księgowość",
lead="Zmiana biura nie musi oznaczać chaosu. Ustalamy termin, odbieramy dokumentację od poprzedniego biura, sprawdzamy ostatnie rozliczenia i prowadzimy księgi dalej – bez przerwy w terminach.",
body="""
<h2>Kiedy klienci zmieniają biuro</h2>
<ul>
<li>biuro nie odpowiada na pytania albo odpowiada po terminie,</li>
<li>pojawiły się błędy w rozliczeniach, korekty i odsetki,</li>
<li>firma urosła i potrzebuje doradcy podatkowego, a nie tylko księgowania,</li>
<li>przyszło pismo z urzędu, a biuro nie może reprezentować firmy przed urzędem,</li>
<li>przejście z JDG do spółki albo na estoński CIT wymaga innego zakresu obsługi.</li>
</ul>

<h2>Jak wygląda przejęcie – krok po kroku</h2>
<ol>
<li><strong>Termin zmiany.</strong> Najwygodniej od początku miesiąca, a najlepiej od początku roku obrotowego. Ustalamy, za jaki okres rozlicza jeszcze poprzednie biuro.</li>
<li><strong>Wypowiedzenie umowy</strong> z poprzednim biurem – podpowiadamy, na co zwrócić uwagę w okresie wypowiedzenia i przy przekazaniu dokumentów.</li>
<li><strong>Pełnomocnictwa</strong> – do urzędu skarbowego (UPL-1, PPS-1), ZUS, KSeF i e-sprawozdań; poprzednie pełnomocnictwa warto odwołać.</li>
<li><strong>Przejęcie dokumentacji</strong> – księgi, ewidencje, deklaracje, dowody księgowe, kartoteki środków trwałych, dokumentacja kadrowa, hasła i dostępy.</li>
<li><strong>Bilans otwarcia i weryfikacja.</strong> Sprawdzamy ostatnie rozliczenia, salda z urzędem i ZUS. Jeśli znajdziemy błędy, mówimy o nich od razu i proponujemy korekty.</li>
<li><strong>Ciągłość terminów.</strong> Pierwszy miesiąc rozliczamy w naszym systemie bez przesunięć terminów płatności.</li>
</ol>
<div class="callout"><strong>Przejęcie w trakcie roku</strong>Zmiana biura w trakcie roku jest możliwa, ale wymaga przeniesienia danych ksiąg i dokładnego uzgodnienia sald. W spółkach odpowiedzialność za zamknięcie roku ustalamy na piśmie z poprzednim biurem.</div>

<h2>Co sprawdzamy przy przejęciu</h2>
<ul>
<li>zgodność JPK_V7 z ewidencjami i fakturami w KSeF,</li>
<li>salda rozrachunków z urzędem skarbowym i ZUS,</li>
<li>środki trwałe i amortyzację, w tym limity dla samochodów,</li>
<li>poprawność formy opodatkowania i terminów jej wyboru,</li>
<li>w spółkach – sprawozdanie za poprzedni rok i jego złożenie do KRS.</li>
</ul>

<h2>Dlaczego RKDP</h2>
<p>W RKDP księgowość prowadzi zespół pod nadzorem doradcy podatkowego. Jeśli przy przejęciu znajdziemy błąd poprzedniego biura, wiemy, jak go naprawić – korektą, czynnym żalem albo wyjaśnieniami w urzędzie. A gdy urząd ma pytania, doradca reprezentuje Cię jako pełnomocnik.</p>
<p>Prowadzimy <a href="/ksiegowosc-spolki-z-o-o">księgowość spółek z o.o.</a>, <a href="/ksiegowosc-jdg">JDG</a> oraz <a href="/kadry-i-place">kadry i płace</a>.</p>

<h2>Od czego zależy cena</h2>
<p>Przejęcie księgowości nie jest osobno płatne przy standardowej zmianie od początku miesiąca. Jeśli dokumentacja wymaga uporządkowania lub korekt za poprzednie okresy, wyceniamy to osobno, po przeglądzie.</p>
""",
faqs=[
("Ile trwa zmiana biura rachunkowego?","Zwykle wystarczy kilka tygodni – zależnie od okresu wypowiedzenia w poprzednim biurze i szybkości przekazania dokumentów. Najlepiej zacząć przygotowania na miesiąc przed planowaną zmianą."),
("Co jeśli poprzednie biuro nie chce wydać dokumentów?","Dokumentacja księgowa należy do firmy, nie do biura. Pomagamy przygotować wezwanie do wydania dokumentów i ustalić, co jest niezbędne do dalszego prowadzenia ksiąg."),
("Czy odpowiadacie za błędy poprzedniego biura?","Nie, ale pomagamy je naprawić. Przy przejęciu weryfikujemy ostatnie rozliczenia i informujemy o wykrytych nieprawidłowościach."),
],
related=["ksiegowosc-spolki-z-o-o","ksiegowosc-jdg","czynnosci-sprawdzajace"],
posts=["zmiana-biura-rachunkowego","ksef-w-malej-firmie"],
))

PAGES.append(dict(
slug="doradca-podatkowy-jagodno", group="Lokalnie", short="Doradca podatkowy Jagodno",
nav_desc="Kancelaria przy ul. Beaty Artemskiej",
title="Doradca podatkowy Jagodno, Wrocław-Krzyki – kancelaria RKDP",
meta="Kancelaria doradcy podatkowego na Jagodnie (Wrocław-Krzyki), ul. Beaty Artemskiej 11/44. Doradztwo, księgowość, pomoc przy pismach z urzędu skarbowego. Pierwsze 20 minut bezpłatnie.",
eyebrow="Wrocław – Jagodno",
h1="Doradca podatkowy na Jagodnie",
lead="Kancelaria RKDP mieści się na wrocławskim Jagodnie, przy ul. Beaty Artemskiej 11/44. Pomagamy firmom i mieszkańcom osiedla w sprawach podatkowych i księgowych – na miejscu albo online.",
body="""
<h2>Kancelaria blisko domu</h2>
<p>Jagodno to jedno z najszybciej rosnących osiedli Wrocławia. Mieszka tu wiele młodych rodzin, a w lokalach usługowych na parterach bloków działają dziesiątki małych firm: gabinety, salony, sklepy, biura projektowe, firmy budowlane i wykończeniowe. Wiele z tych firm prowadzą osoby, które pracują z domu i rozliczają się same – do pierwszego pisma z urzędu.</p>
<p>Dla nich jesteśmy na miejscu: można przyjść z dokumentami, zostawić je w kancelarii albo umówić się na rozmowę online.</p>

<h2>Z czym przychodzą do nas mieszkańcy Jagodna</h2>
<ul>
<li><strong>Zakup i sprzedaż mieszkania</strong> – PIT przy sprzedaży przed upływem 5 lat, ulga mieszkaniowa, zakup kolejnego lokalu na wynajem (zobacz <a href="/podatki-nieruchomosci">podatki od nieruchomości</a>).</li>
<li><strong>Najem mieszkania</strong> – ryczałt od najmu prywatnego, rozliczenie przez małżonków, najem krótkoterminowy.</li>
<li><strong>Założenie firmy</strong> – JDG czy spółka, forma opodatkowania, ulga na start i składki (zobacz <a href="/forma-opodatkowania">forma opodatkowania</a>).</li>
<li><strong>Księgowość dla lokalnych firm</strong> – <a href="/ksiegowosc-jdg">KPiR i ryczałt dla JDG</a>, <a href="/ksiegowosc-spolki-z-o-o">pełna księgowość spółek</a>, kadry dla pierwszych pracowników.</li>
<li><strong>Pismo z urzędu skarbowego</strong> – wezwanie do wyjaśnień, rozbieżności w JPK, kontrola (zobacz <a href="/czynnosci-sprawdzajace">czynności sprawdzające</a>).</li>
<li><strong>Ulgi rodzinne i rozliczenie roczne</strong> – gdy w rodzinie jest działalność gospodarcza, najem i zatrudnienie jednocześnie.</li>
</ul>

<h2>Jak dojechać</h2>
<p>Kancelaria znajduje się przy ul. Beaty Artemskiej 11/44 (52-234 Wrocław), w zachodniej części Jagodna, w dzielnicy Krzyki. Na spotkanie najlepiej umówić się wcześniej – przez kalendarz online albo telefonicznie – żeby doradca miał czas przejrzeć Twoje dokumenty przed rozmową.</p>
<div class="callout"><strong>Pierwsze 20 minut bezpłatnie</strong>Na pierwszej rozmowie ustalamy, czego potrzebujesz i ile to kosztuje. Możesz przyjść do kancelarii albo porozmawiać z nami online.</div>

<h2>Dla firm z sąsiedztwa</h2>
<p>Obsługujemy firmy z Jagodna, Wojszyc, Ołtaszyna, Brochowa, Bieńkowic i Partynic, a także z gmin położonych na południe od Wrocławia – <a href="/doradca-podatkowy-siechnice">Siechnic, Radwanic i Żernik Wrocławskich</a>. Dla wielu klientów to po prostu najbliższy doradca podatkowy – bez dojazdów do centrum miasta.</p>

<h2>Doradca, a nie tylko biuro rachunkowe</h2>
<p>RKDP to spółka doradztwa podatkowego wpisana do rejestru KIDP pod nr 855. Oprócz księgowości możemy udzielać porad podatkowych i reprezentować klientów przed urzędem skarbowym i sądem administracyjnym – czego biuro rachunkowe robić nie może.</p>
""",
faqs=[
("Gdzie dokładnie jest kancelaria?","Przy ul. Beaty Artemskiej 11/44, 52-234 Wrocław (Jagodno, dzielnica Krzyki). Przed wizytą prosimy o umówienie terminu."),
("Czy mogę zostawić dokumenty w kancelarii?","Tak, po wcześniejszym umówieniu. Większość dokumentów klienci przesyłają jednak elektronicznie."),
("Czy pomagacie przy rozliczeniu sprzedaży mieszkania na Jagodnie?","Tak. Ustalamy, czy sprzedaż podlega PIT, czy można skorzystać z ulgi mieszkaniowej, i przygotowujemy zeznanie PIT-39."),
],
related=["podatki-nieruchomosci","ksiegowosc-jdg","doradca-podatkowy-siechnice"],
posts=["sprzedaz-dzialki-pit-vat-pcc","jdg-czy-spolka-z-o-o"],
))

PAGES.append(dict(
slug="doradca-podatkowy-siechnice", group="Lokalnie", short="Doradca podatkowy Siechnice",
nav_desc="Siechnice, Radwanice, Żerniki, Ozorzyce",
title="Doradca podatkowy Siechnice, Radwanice, Żerniki Wrocławskie, Ozorzyce | RKDP",
meta="Doradca podatkowy dla mieszkańców i firm z Siechnic, Radwanic, Żernik Wrocławskich i Ozorzyc: podatek od nieruchomości, sprzedaż działek, księgowość. Kancelaria tuż obok, na Jagodnie.",
eyebrow="Siechnice i okolice",
h1="Doradca podatkowy dla Siechnic i okolic",
lead="Siedziba RKDP mieści się w Ozorzycach, a kancelaria – na sąsiednim wrocławskim Jagodnie. Znamy sprawy, z którymi przychodzą mieszkańcy i firmy z Siechnic, Radwanic, Żernik Wrocławskich i okolicznych wsi.",
body="""
<h2>Podatki na terenach, które szybko się zmieniają</h2>
<p>Okolice Siechnic to w ostatnich latach miejsce intensywnej zabudowy: dawne pola zamieniają się w osiedla domów, powstają nowe ulice i lokale usługowe. Za tym idą konkretne sprawy podatkowe – sprzedaż działek odziedziczonych po rodzicach, podział gruntu, budowa domu na sprzedaż, najem, a także spory z gminą o podatek od nieruchomości.</p>

<h2>Sprzedaż działki – PIT, VAT czy PCC</h2>
<p>Właściciele gruntów w Radwanicach, Żernikach Wrocławskich czy Ozorzycach często pytają, czy od sprzedaży działki trzeba zapłacić podatek. Odpowiedź zależy od tego, kiedy i jak działka została nabyta (zakup, spadek, darowizna, gospodarstwo rolne), oraz od tego, co sprzedający robił z gruntem przed sprzedażą – podział na mniejsze działki, uzbrojenie, warunki zabudowy, ogłoszenia. Przy kilku sprzedażach urząd może uznać sprzedającego za podatnika VAT. Wyjaśniamy to w artykule <a href="/blog/sprzedaz-dzialki-pit-vat-pcc">sprzedaż działki: PIT, VAT czy PCC</a> i na stronie <a href="/podatki-nieruchomosci">podatki od nieruchomości</a>.</p>

<h2>Podatek od nieruchomości w gminie</h2>
<p>Stawki podatku od nieruchomości uchwala rada gminy, więc w gminie Siechnice są one inne niż we Wrocławiu czy w Kobierzycach. Decyzje wymiarowe dla osób fizycznych wydaje burmistrz, a przedsiębiorcy i osoby prawne składają deklaracje sami. Najczęstsze spory dotyczą:</p>
<ul>
<li>uznania gruntu lub budynku za „związany z prowadzeniem działalności gospodarczej” – co podnosi stawkę,</li>
<li>powierzchni użytkowej budynków i pomieszczeń o niższej wysokości,</li>
<li>gruntów pod budowami i zmian sposobu wykorzystania działki,</li>
<li>zaległości i odsetek po korekcie deklaracji.</li>
</ul>
<p>Od decyzji burmistrza przysługuje odwołanie do samorządowego kolegium odwoławczego w terminie 14 dni. Przygotowujemy odwołania i prowadzimy sprawy dalej przed sądem – zobacz <a href="/odwolanie-od-decyzji">odwołanie od decyzji</a>.</p>

<h2>Firmy z okolic Siechnic</h2>
<p>Obsługujemy firmy budowlane i wykończeniowe, deweloperów realizujących niewielkie inwestycje, gospodarstwa rolne prowadzące działalność pozarolniczą, a także przedsiębiorców, którzy prowadzą firmę z domu. Dla nich prowadzimy <a href="/ksiegowosc-jdg">księgowość JDG</a> i <a href="/ksiegowosc-spolki-z-o-o">spółek</a>, doradzamy przy <a href="/forma-opodatkowania">wyborze formy opodatkowania</a> i przy <a href="/firmy-rodzinne-sukcesja">przekazaniu firmy lub gospodarstwa</a> w rodzinie.</p>

<h2>Blisko, ale też zdalnie</h2>
<p>Z Siechnic i Radwanic na Jagodno jest tylko kilka kilometrów, więc łatwo przyjechać na spotkanie do kancelarii przy ul. Beaty Artemskiej 11/44. Większość spraw prowadzimy jednak zdalnie – dokumenty przesyłasz elektronicznie, a rozmowy odbywamy telefonicznie lub online.</p>
<div class="callout"><strong>Pierwsze 20 minut bezpłatnie</strong>Opowiedz o swojej sprawie – powiemy, co możesz zrobić i ile to kosztuje.</div>
""",
faqs=[
("Czy obsługujecie też gminę Kobierzyce i Żórawinę?","Tak. Pracujemy z klientami z całego powiatu wrocławskiego, a większość spraw prowadzimy zdalnie."),
("Gmina naliczyła wyższy podatek od nieruchomości. Co mogę zrobić?","Sprawdzić podstawę i stawkę w decyzji, a jeśli są błędne – złożyć odwołanie do samorządowego kolegium odwoławczego w ciągu 14 dni od doręczenia decyzji."),
("Odziedziczyłem działkę w Radwanicach. Czy zapłacę podatek przy sprzedaży?","Pięcioletni termin liczy się od końca roku, w którym nieruchomość nabył spadkodawca. Jeśli minął, sprzedaż co do zasady nie podlega PIT – ale trzeba też sprawdzić kwestię VAT."),
],
related=["podatki-nieruchomosci","odwolanie-od-decyzji","doradca-podatkowy-jagodno"],
posts=["sprzedaz-dzialki-pit-vat-pcc","przekazanie-firmy-dzieciom"],
))
