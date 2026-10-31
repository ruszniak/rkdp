#!/usr/bin/env python3
"""Generator podstron rkdp.pl.

Uruchom z katalogu repozytorium:  python3 tools/build.py
Tworzy katalogi <slug>/index.html dla podstron i artykułów, blog/index.html,
aktualizuje sitemap.xml oraz wstawia wspólne menu do index.html.
Treści są w plikach tools/content_*.py.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content_doradztwo import PAGES as P_DOR
from content_ksiegowosc import PAGES as P_KSI
from content_lokalne import PAGES as P_LOK
from content_blog import POSTS
from content_extra import EXTRA

SITE = 'https://rkdp.pl'
TODAY = '2026-10-13'
PHONE = '+48 883 643 565'
PHONE_HREF = 'tel:+48883643565'
EMAIL = 'kancelaria@rkdp.pl'
BOOK = 'https://m2taxdoradcypodatkowi.zohobookings.eu/m2taxdoradcypodatkowi'

ALL_PAGES = P_DOR + P_KSI + P_LOK
for _p in ALL_PAGES:
    _extra = EXTRA.get(_p['slug'])
    if _extra:
        _i = next((k for k, b in enumerate(_p['body']) if b[0] == 'h2' and b[1].startswith('Od czego zależy')), len(_p['body']))
        _p['body'][_i:_i] = _extra
BY_SLUG = {p['slug']: p for p in ALL_PAGES}
POST_BY_SLUG = {p['slug']: p for p in POSTS}

e = lambda s: html.escape(s, quote=True)
CHEV = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PHONE_ICO = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'


def url(slug):
    return f'/{slug}/'


def dd(label, pages):
    items = ''.join(f'<a href="{url(p["slug"])}">{e(p.get("nav_label", p["menu"]))}<small>{e(p["menu_sub"])}</small></a>' for p in pages)
    return f'<div class="dd"><button type="button" aria-expanded="false">{label} {CHEV}</button><div class="dd-menu">{items}</div></div>'


def nav_html():
    dor = [p for p in P_DOR if p['slug'] not in ('kontrola-podatkowa', 'czynnosci-sprawdzajace', 'odwolanie-od-decyzji')]
    dor = dor[:1] + [BY_SLUG['doradca-podatkowy-siechnice']] + dor[1:]
    spory = [BY_SLUG[s] for s in ('kontrola-podatkowa', 'czynnosci-sprawdzajace', 'odwolanie-od-decyzji')]
    return ('<header class="site-header">\n  <div class="wrap nav">\n'
            '    <a href="/" class="nav-logo" aria-label="RKDP spółka doradztwa podatkowego – strona główna"><img src="/img/logo-rkdp.png" alt="RKDP spółka doradztwa podatkowego" width="183" height="54"></a>\n'
            '    <button class="menu-btn" type="button" aria-label="Otwórz menu" aria-expanded="false" aria-controls="menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>\n'
            '    <nav id="menu" class="nav-links" aria-label="Menu główne">\n'
            f'      {dd("Doradztwo podatkowe", dor)}\n'
            f'      {dd("Kontrole i postępowania", spory)}\n'
            f'      {dd("Księgowość", P_KSI)}\n'
            '      <a href="/zespol/">Zespół</a>\n'
            '      <a href="/cennik/">Cennik</a>\n'
            '      <a href="/#kontakt">Kontakt</a>\n'
            '      <a href="/#termin" class="btn btn-primary" data-booking-open>Umów konsultację</a>\n'
            '    </nav>\n  </div>\n</header>')


def footer_html():
    col = lambda pages: ''.join(f'<a href="{url(p["slug"])}">{e(p["menu"])}</a>' for p in pages)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="/img/logo-rkdp.png" alt="RKDP spółka doradztwa podatkowego" width="217" height="64" loading="lazy">
        <p>RKDP spółka doradztwa podatkowego sp. z o.o.<br>ul. Czereśniowa 28d, 55-010 Ozorzyce · NIP 8992871126 · KRS 0000812185<br>Kancelaria: ul. Beaty Artemskiej 11/44, 52-234 Wrocław (Jagodno)<br><a href="{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>Sprawy sporne z organami podatkowymi prowadzimy także w spółce partnerskiej <a href="https://m2tax.pl" target="_blank" rel="noopener" style="color:var(--gold)">M2 TAX Doradcy Podatkowi</a>.</p>
      </div>
      <nav aria-label="Doradztwo podatkowe"><span class="k">Doradztwo</span>{col(P_DOR)}</nav>
      <nav aria-label="Księgowość"><span class="k">Księgowość</span>{col(P_KSI)}<span class="k" style="margin-top:14px">Okolice</span>{col(P_LOK)}</nav>
      <nav aria-label="Informacje"><span class="k">Informacje</span><a href="/zespol/">Zespół</a><a href="/cennik/">Cennik</a><a href="https://share.google/NmuxQZlwzieY9TcN3" target="_blank" rel="noopener">Wizytówka Google</a><a href="/polityka-prywatnosci.html">RODO (Polityka prywatności)</a><a href="/aml.html">AML</a><a href="/dokumenty/procedura-sygnalisci-rkdp.pdf" target="_blank" rel="noopener">Sygnaliści</a><a href="/dokumenty/regulamin-umowy-do-31-12-2025.pdf" target="_blank" rel="noopener">Regulamin (umowy do 31.12.2025)</a></nav>
    </div>
    <div class="footer-bottom">
      <span>© <span class="year">2026</span> RKDP spółka doradztwa podatkowego sp. z o.o. Wszelkie prawa zastrzeżone.</span>
      <span>Doradca podatkowy nr 15009 · Podmiot uprawniony nr 855 · Wykonanie: <a href="https://ruszniak.io" target="_blank" rel="noopener">druslak</a></span>
    </div>
  </div>
</footer>
<div class="fab-stack" aria-label="Szybki kontakt">
<a class="fab tel-fab" href="tel:+48883643565" aria-label="Zadzwoń: +48 883 643 565">
  <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path fill="currentColor" d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.61 21 3 13.39 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2Z"/></svg>
  <span class="wa-label">Zadzwoń: +48 883 643 565</span>
</a>
<a class="fab wa-fab" href="https://wa.me/48883643565?text=Dzie%C5%84%20dobry%2C%20mam%20pytanie%20podatkowe%3A%20" target="_blank" rel="noopener" aria-label="Napisz do nas na WhatsApp">
  <svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M16.04 3C9.4 3 4 8.36 4 14.970c0 2.11.56 4.17 1.62 5.99L4 29l8.25-2.15a12.1 12.1 0 0 0 5.790 1.47h.01c6.63 0 12.03-5.36 12.03-11.97C28.07 8.36 22.67 3 16.04 3Zm0 21.980h-.01c-1.8 0-3.56-.48-5.1-1.39l-.37-.22-4.9 1.27 1.31-4.750-.24-.39a9.85 9.85 0 0 1-1.52-5.53c0-5.48 4.49-9.94 10.01-9.94 2.67 0 5.18 1.04 7.07 2.91a9.83 9.83 0 0 1 2.93 7.03c0 5.48-4.49 9.94-10 9.94Zm5.49-7.44c-.3-.15-1.78-.87-2.05-.97-.28-.1-.48-.15-.68.15-.2.3-.78.97-.95 1.17-.18.2-.35.22-.65.07-.3-.15-1.27-.46-2.42-1.48-.89-.79-1.5-1.77-1.67-2.070-.18-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.68-1.63-.93-2.23-.24-.58-.49-.5-.68-.51h-.58c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.48.71.31 1.27.49 1.7.63.71.23 1.36.2 1.88.12.57-.09 1.78-.72 2.03-1.42.25-.7.25-1.3.18-1.42-.08-.13-.28-.2-.58-.35Z"/></svg>
  <span class="wa-label">Napisz na WhatsApp</span>
</a>
</div>'''


NAV_JS = '''<dialog class="booking-modal" id="booking-modal" aria-labelledby="booking-title">
  <div class="modal-head">
    <strong id="booking-title">Wybierz termin konsultacji</strong>
    <div class="tools">
      <a href="https://m2taxdoradcypodatkowi.zohobookings.eu/m2taxdoradcypodatkowi" target="_blank" rel="noopener">Otwórz w nowej karcie</a>
      <button type="button" class="modal-close" data-booking-close aria-label="Zamknij kalendarz"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
  </div>
  <div class="modal-body"><div class="modal-loading">Ładowanie kalendarza…</div><div id="inline-container"></div></div>
</dialog>
<script>
(function(){
  // Rezerwacja Zoho w okienku na stronie
  var modal=document.getElementById('booking-modal'), zohoLoaded=false;
  function loadZoho(){
    if(zohoLoaded) return; zohoLoaded=true;
    var sc=document.createElement('script'); sc.src='https://bookings.nimbuspop.com/assets/embed.js';
    sc.onload=function(){var h=Math.max(600,document.getElementById('inline-container').clientHeight);Bookings.inlineEmbed({url:'https://m2taxdoradcypodatkowi.zohobookings.eu/portal-embed#/m2taxdoradcypodatkowi',parent:'#inline-container',height:h+'px'});};
    document.head.appendChild(sc);
  }
  if(modal && typeof modal.showModal==='function'){
    document.addEventListener('click',function(e){
      var a=e.target.closest('[data-booking-open], a[href*="zohobookings.eu"]');
      if(!a || a.closest('#booking-modal')) return;
      e.preventDefault(); modal.showModal(); loadZoho();
    });
    modal.querySelector('[data-booking-close]').addEventListener('click',function(){modal.close();});
    modal.addEventListener('click',function(e){if(e.target===modal) modal.close();});
  }
  var btn=document.querySelector('.menu-btn'), menu=document.getElementById('menu');
  if(btn&&menu){btn.addEventListener('click',function(){var o=menu.classList.toggle('open');btn.setAttribute('aria-expanded',o);btn.setAttribute('aria-label',o?'Zamknij menu':'Otwórz menu');});}
  document.querySelectorAll('.dd>button').forEach(function(b){b.addEventListener('click',function(ev){ev.stopPropagation();var d=b.parentElement,o=!d.classList.contains('open');document.querySelectorAll('.dd.open').forEach(function(x){x.classList.remove('open');x.firstElementChild.setAttribute('aria-expanded','false');});if(o){d.classList.add('open');b.setAttribute('aria-expanded','true');}});});
  document.addEventListener('click',function(){document.querySelectorAll('.dd.open').forEach(function(x){x.classList.remove('open');});});
  document.querySelectorAll('.year').forEach(function(y){y.textContent=new Date().getFullYear();});
})();
</script>'''


def head(title, desc, path, og_type='website', extra_ld=()):
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in extra_ld)
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="RKDP spółka doradztwa podatkowego">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/img/michal-ruszniak.jpg">
<meta name="theme-color" content="#1D1A16">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700&family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/css/site.css">
{ld}</head>
<body>
<div class="bg-fx" aria-hidden="true"><span class="orb o1"></span><span class="orb o2"></span></div>
{nav_html()}
'''


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    parts = []
    for i, (n, u) in enumerate(items):
        parts.append(f'<span>{e(n)}</span>' if i == len(items) - 1 else f'<a href="{u}">{e(n)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Ścieżka">' + ''.join(parts) + '</nav>'


def render_blocks(blocks):
    out = []
    for b in blocks:
        kind = b[0]
        if kind == 'h2': out.append(f'<h2>{b[1]}</h2>')
        elif kind == 'h3': out.append(f'<h3>{b[1]}</h3>')
        elif kind == 'p': out.append(f'<p>{b[1]}</p>')
        elif kind == 'ul': out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in b[1]) + '</ul>')
        elif kind == 'ol': out.append('<ol>' + ''.join(f'<li>{x}</li>' for x in b[1]) + '</ol>')
        elif kind == 'note': out.append(f'<div class="note"><p>{b[1]}</p></div>')
        elif kind == 'facts': out.append('<div class="facts">' + ''.join(f'<div class="fact"><b>{a}</b><span>{c}</span></div>' for a, c in b[1]) + '</div>')
        else: raise ValueError(kind)
    return '\n'.join(out)


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def word_count(blocks):
    n = 0
    for b in blocks:
        if b[0] in ('ul', 'ol'): n += sum(len(strip_tags(x).split()) for x in b[1])
        elif b[0] == 'facts': n += sum(len(strip_tags(a + ' ' + c).split()) for a, c in b[1])
        else: n += len(strip_tags(b[1]).split())
    return n


def faq_html(faq):
    if not faq: return ''
    items = ''.join(f'<details><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in faq)
    return f'<section class="faq-block" aria-labelledby="faq-h"><h2 id="faq-h">Najczęstsze pytania</h2>{items}</section>'


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faq]}


def related_html(slugs, title='Zobacz też'):
    cards = []
    for s in slugs:
        if s in BY_SLUG:
            p = BY_SLUG[s]; cards.append(f'<a class="card" href="{url(s)}"><b>{e(p["menu"])}</b><span>{e(p["menu_sub"])}</span><em>Czytaj więcej →</em></a>')
    if not cards: return ''
    return f'<section class="related"><h2>{title}</h2><div class="cards">{"".join(cards)}</div></section>'


def aside_html(links):
    ls = ''.join(f'<a href="{url(s)}">{e(BY_SLUG[s]["menu"])}</a>' for s in links if s in BY_SLUG)
    return f'''<aside class="aside">
  <div class="aside-card">
    <span class="eyebrow">Konsultacja</span>
    <h2>Porozmawiajmy o Twojej sprawie</h2>
    <p>Zadzwoń albo wybierz termin w kalendarzu. Masz pismo z urzędu? Przygotuj datę jego doręczenia.</p>
    <a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">Wybierz termin {ARROW}</a>
    <a class="tel" href="{PHONE_HREF}">{PHONE}</a>
  </div>
  <div class="aside-links"><h2>Powiązane usługi</h2>{ls}</div>
</aside>'''


def cta_band(title='Masz pytanie podatkowe?', text='Umów konsultację z doradcą podatkowym – w kancelarii na Jagodnie albo online.'):
    return f'''<section class="wrap cta-band"><div class="cta-box"><div><h2>{title}</h2><p>{text}</p></div><div class="ctas"><a class="btn btn-light" href="{BOOK}" target="_blank" rel="noopener">Umów konsultację {ARROW}</a><a class="btn btn-light" href="{PHONE_HREF}">{PHONE_ICO} {PHONE}</a></div></div></section>'''


def org_ref():
    return {"@type": "AccountingService", "@id": SITE + "/#firma", "name": "RKDP spółka doradztwa podatkowego sp. z o.o.",
            "address": {"@type": "PostalAddress", "streetAddress": "ul. Beaty Artemskiej 11/44", "postalCode": "52-234", "addressLocality": "Wrocław", "addressCountry": "PL"},
            "telephone": "+48883643565"}


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)


def build_page(p, group_name):
    path = url(p['slug'])
    crumbs = [('Strona główna', '/'), (group_name, '/#uslugi'), (p['menu'], path)]
    ld = [breadcrumb_ld(crumbs),
          {"@context": "https://schema.org", "@type": "Service", "name": p['h1'], "serviceType": p['menu'], "description": p['desc'],
           "provider": org_ref(), "areaServed": {"@type": "City", "name": "Wrocław"}, "url": SITE + path}]
    if p.get('faq'): ld.append(faq_ld(p['faq']))
    body = head(p['title'], p['desc'], path, extra_ld=ld)
    body += f'''<main>
<section class="wrap page-hero"><div class="inner">
  {crumbs_html(crumbs)}
  <span class="eyebrow">{e(p['eyebrow'])}</span>
  <h1>{e(p['h1'])}</h1>
  <p class="lead">{p['lead']}</p>
  <div class="ctas"><a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">Umów konsultację {ARROW}</a><a class="btn btn-outline" href="{PHONE_HREF}">{PHONE_ICO} {PHONE}</a></div>
</div></section>
<div class="wrap page-body">
  <article class="prose">
{render_blocks(p['body'])}
{faq_html(p.get('faq'))}
{related_html(p.get('related', []))}
  </article>
  {aside_html(p.get('aside', p.get('related', [])))}
</div>
{cta_band()}
</main>
{footer_html()}
{NAV_JS}
</body>
</html>
'''
    write(p['slug'] + '/index.html', body)
    return word_count(p['body']) + sum(len(strip_tags(a).split()) + len(q.split()) for q, a in p.get('faq', []))


MONTHS = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']
def pl_date(d):
    y, m, dd_ = d.split('-'); return f'{int(dd_)} {MONTHS[int(m) - 1]} {y}'


AUTHORS = {
    'michal': {'id': 'michal-ruszniak', 'name': 'Michał Ruszniak', 'nr': '15009', 'img': 'michal-ruszniak'},
    'marcin': {'id': 'marcin-otreba', 'name': 'Marcin Otręba', 'nr': '14609', 'img': 'marcin-otreba'},
}

def build_post(p):
    a = AUTHORS[p.get('author', 'michal')]
    path = f'/blog/{p["slug"]}/'
    crumbs = [('Strona główna', '/'), ('Blog', '/blog/'), (p['title'], path)]
    ld = [breadcrumb_ld(crumbs), {
        "@context": "https://schema.org", "@type": "Article", "headline": p['title'], "description": p['desc'],
        "datePublished": p['date'], "dateModified": p.get('updated', p['date']), "inLanguage": "pl-PL",
        "author": {"@type": "Person", "@id": SITE + "/#" + a['id'], "name": a['name'], "jobTitle": "Doradca podatkowy", "url": SITE + "/zespol/"},
        "publisher": {"@id": SITE + "/#firma", "@type": "Organization", "name": "RKDP spółka doradztwa podatkowego sp. z o.o.", "logo": {"@type": "ImageObject", "url": SITE + "/img/logo-rkdp.png"}},
        "image": SITE + "/img/michal-ruszniak.jpg", "mainEntityOfPage": SITE + path}]
    if p.get('faq'): ld.append(faq_ld(p['faq']))
    body = head(p['title'] + ' | Blog RKDP', p['desc'], path, og_type='article', extra_ld=ld)
    target = BY_SLUG.get(p['target'])
    body += f'''<main>
<section class="wrap page-hero"><div class="inner">
  {crumbs_html(crumbs)}
  <span class="eyebrow">{e(p['tag'])}</span>
  <h1>{e(p['title'])}</h1>
  <p class="lead">{p['lead']}</p>
</div></section>
<div class="wrap page-body">
  <article class="prose">
    <div class="author"><img src="/img/{a['img']}.webp" alt="{a['name']}, doradca podatkowy" width="64" height="64" loading="lazy"><div><b>{a['name']}</b><span>Doradca podatkowy nr {a['nr']} · <a href="/zespol/">o autorze</a></span><br><span class="meta">Opublikowano <time datetime="{p['date']}">{pl_date(p['date'])}</time>{' · aktualizacja <time datetime="' + p['updated'] + '">' + pl_date(p['updated']) + '</time>' if p.get('updated') else ''}</span></div></div>
{render_blocks(p['body'])}
{faq_html(p.get('faq'))}
<div class="note"><p>Artykuł ma charakter informacyjny i opisuje stan prawny na dzień publikacji. Nie zastępuje porady podatkowej w indywidualnej sprawie.</p></div>
{related_html([p['target']] + p.get('related', []), 'Jak możemy pomóc')}
  </article>
  {aside_html([p['target']] + [s for s in p.get('related', []) if s in BY_SLUG])}
</div>
{cta_band()}
</main>
{footer_html()}
{NAV_JS}
</body>
</html>
'''
    write(f'blog/{p["slug"]}/index.html', body)
    return word_count(p['body'])


def build_blog_index():
    path = '/blog/'
    crumbs = [('Strona główna', '/'), ('Blog', path)]
    posts = sorted(POSTS, key=lambda x: x['date'], reverse=True)
    cards = ''.join(f'<a class="post" href="/blog/{p["slug"]}/"><span class="tag">{e(p["tag"])}</span><b>{e(p["title"])}</b><span>{e(p["desc"])}</span><time datetime="{p["date"]}">{pl_date(p["date"])} · {AUTHORS[p.get("author","michal")]["name"]}</time></a>' for p in posts)
    ld = [breadcrumb_ld(crumbs), {"@context": "https://schema.org", "@type": "Blog", "name": "Blog podatkowy RKDP", "url": SITE + path,
          "blogPost": [{"@type": "BlogPosting", "headline": p['title'], "url": f'{SITE}/blog/{p["slug"]}/', "datePublished": p['date']} for p in posts]}]
    body = head('Blog podatkowy – doradca podatkowy Wrocław | RKDP', 'Artykuły doradcy podatkowego z Wrocławia: KSeF, wezwania z urzędu skarbowego, estoński CIT, sprzedaż nieruchomości, sukcesja w firmie rodzinnej i zmiana biura rachunkowego.', path, extra_ld=ld)
    body += f'''<main>
<section class="wrap page-hero"><div class="inner">
  {crumbs_html(crumbs)}
  <span class="eyebrow">Blog</span>
  <h1>Blog podatkowy RKDP</h1>
  <p class="lead">Odpowiedzi doradcy podatkowego na konkretne pytania przedsiębiorców i osób prywatnych. Każdy artykuł opisuje jedną sprawę – krótko, z odesłaniem do przepisów i do usługi, w której możemy pomóc.</p>
</div></section>
<section class="wrap"><div class="posts">{cards}</div></section>
{cta_band()}
</main>
{footer_html()}
{NAV_JS}
</body>
</html>
'''
    write('blog/index.html', body)


def build_team_page():
    cards = open(os.path.join(ROOT, 'tools', 'partials', 'zespol.html'), encoding='utf-8').read().strip().replace('<section id="zespol" class="wrap team">', '<section class="wrap team" aria-label="Doradcy podatkowi">')
    path = '/zespol/'
    crumbs = [('Strona główna', '/'), ('Zespół', path)]
    people = [
        {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "/#michal-ruszniak", "name": "Michał Ruszniak", "jobTitle": "Doradca podatkowy, Prezes Zarządu RKDP", "image": SITE + "/img/michal-ruszniak.jpg", "sameAs": ["https://kidp.pl/doradca/15009"], "worksFor": {"@id": SITE + "/#firma"}},
        {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "/#marcin-otreba", "name": "Marcin Otręba", "jobTitle": "Doradca podatkowy", "image": SITE + "/img/marcin-otreba.jpg", "sameAs": ["https://kidp.pl/doradca/14609"]},
    ]
    ld = [breadcrumb_ld(crumbs), {"@context": "https://schema.org", "@type": "AboutPage", "name": "Zespół RKDP", "url": SITE + path}] + people
    body = head('Zespół – doradcy podatkowi Michał Ruszniak i Marcin Otręba | RKDP Wrocław', 'Poznaj doradców podatkowych RKDP: Michał Ruszniak (nr wpisu 15009, prezes zarządu) i Marcin Otręba (nr wpisu 14609). Doradztwo, kontrole, spory i księgowość we Wrocławiu.', path, extra_ld=ld)
    body += f'''<main>
<section class="wrap page-hero"><div class="inner">
  {crumbs_html(crumbs)}
  <span class="eyebrow">Zespół</span>
  <h1>Nasi doradcy podatkowi</h1>
  <p class="lead">Dwóch doradców podatkowych, jedna kancelaria. Łączymy doświadczenie przedsiębiorcy z doświadczeniem z administracji skarbowej – Twoją sprawą zajmuje się doradca podatkowy wpisany na listę Krajowej Izby Doradców Podatkowych.</p>
</div></section>
{cards}
{cta_band('Porozmawiaj z doradcą', 'Umów konsultację w kancelarii na Jagodnie albo online.')}
</main>
{footer_html()}
{NAV_JS}
</body>
</html>
'''
    write('zespol/index.html', body)


def build_pricing_page():
    grid = open(os.path.join(ROOT, 'tools', 'partials', 'cennik.html'), encoding='utf-8').read()
    path = '/cennik/'
    crumbs = [('Strona główna', '/'), ('Cennik', path)]
    def offer(name, price, unit=None):
        ps = {"@type": "UnitPriceSpecification", "priceCurrency": "PLN", "minPrice": price}
        if unit: ps["unitText"] = unit
        return {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name}, "priceSpecification": ps}
    ld = [breadcrumb_ld(crumbs), {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Cennik RKDP – doradztwo podatkowe i księgowość", "url": SITE + path, "itemListElement": [
        offer("Konsultacja wstępna (do 20 minut)", 0), offer("Konsultacja podatkowa", 300, "godzina"),
        offer("Abonament Doradca Podatkowy", 369, "miesiąc"), offer("Abonament Księgowość JDG + Doradca Podatkowy", 419, "miesiąc"), offer("Abonament Księgowość + Doradca Podatkowy", 790, "miesiąc")]}]
    body = head('Cennik – doradca podatkowy i księgowość Wrocław | RKDP', 'Cennik RKDP: pierwsza konsultacja do 20 minut bezpłatnie, konsultacja podatkowa od 300 zł/h, abonament doradcy od 369 zł, księgowość JDG z doradcą od 419 zł, księgowość z doradcą od 790 zł miesięcznie.', path, extra_ld=ld)
    body += f'''<main>
<section class="wrap page-hero"><div class="inner">
  {crumbs_html(crumbs)}
  <span class="eyebrow">Cennik</span>
  <h1>Jasne ceny, bez niespodzianek</h1>
  <p class="lead">Zacznij od bezpłatnej rozmowy z doradcą podatkowym – a potem wybierz jednorazową konsultację albo stałą opiekę: samego doradcy lub księgowości razem z doradcą.</p>
</div></section>
<section class="wrap pricing pricing-page" aria-label="Pakiety i ceny">{grid}</section>
{cta_band('Nie wiesz, który pakiet wybrać?', 'Umów bezpłatną 20-minutową rozmowę – doradzimy i przygotujemy wycenę.')}
</main>
{footer_html()}
{NAV_JS}
</body>
</html>
'''
    write('cennik/index.html', body)


def build_sitemap():
    urls = [('/', '1.0', 'monthly')]
    urls += [(url(p['slug']), '0.8', 'monthly') for p in P_DOR + P_KSI]
    urls += [(url(p['slug']), '0.7', 'monthly') for p in P_LOK]
    urls += [('/cennik/', '0.7', 'monthly'), ('/zespol/', '0.6', 'monthly')]
    urls += [('/aml.html', '0.3', 'yearly'), ('/polityka-prywatnosci.html', '0.2', 'yearly')]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    x += ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n' for u, pr, c in urls)
    x += '</urlset>\n'
    write('sitemap.xml', x)
    return len(urls)


def update_index():
    """Wstawia wspólne menu, kafelki usług i najnowsze artykuły do index.html (między znacznikami)."""
    f = os.path.join(ROOT, 'index.html')
    s = open(f, encoding='utf-8').read()
    def put(name, content):
        nonlocal s
        a, b = f'<!-- gen:{name} -->', f'<!-- /gen:{name} -->'
        if a not in s: raise SystemExit(f'Brak znacznika {a} w index.html')
        i, j = s.index(a) + len(a), s.index(b)
        s = s[:i] + '\n' + content + '\n' + s[j:]
    put('nav', nav_html())
    put('footer', footer_html())
    kon_slugs = ('kontrola-podatkowa', 'czynnosci-sprawdzajace', 'odwolanie-od-decyzji')
    groups = [('Doradztwo podatkowe', [p for p in P_DOR if p['slug'] not in kon_slugs]),
              ('Kontrole i postępowania', [p for p in P_DOR if p['slug'] in kon_slugs]),
              ('Księgowość', P_KSI)]
    ic = {
      'doradztwo-podatkowe': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
      'kontrola-podatkowa': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
      'czynnosci-sprawdzajace': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
      'interpretacja-indywidualna': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
      'odwolanie-od-decyzji': '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
      'wyplata-pieniedzy-ze-spolki': '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 9h.01M18 15h.01"/>',
      'forma-opodatkowania': '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
      'restrukturyzacje-spolek': '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7.5 8l3.5 7.8M16.5 8L13 15.8M8.5 6h7"/>',
      'firmy-rodzinne-sukcesja': '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M9 21v-6h6v6"/>',
      'podatki-nieruchomosci': '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M14.5 8.5l2 2"/>',
      'ksiegowosc-spolki-z-o-o': '<path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16M16 9h3a1 1 0 0 1 1 1v11M2 21h20M8 7h4M8 11h4M8 15h4"/>',
      'ksiegowosc-jdg': '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 18.5h.01M12 18.5h4"/>',
      'kadry-i-place': '<circle cx="9" cy="8" r="3.5"/><path d="M2 21a7 7 0 0 1 14 0M16 4.5a3.5 3.5 0 0 1 0 7M22 21a7 7 0 0 0-4-6.3"/>',
      'zmiana-biura-rachunkowego': '<path d="M4 8h15l-4-4M20 16H5l4 4"/>',
      '_cta': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M9 15l2 2 4-4"/>',
    }
    svg = lambda k: f'<span class="n-ic"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ic[k]}</svg></span>'
    more = '<em class="n-more">Dowiedz się więcej <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></em>'
    tabs, panels, n = [], [], 0
    for k, (name, pages) in enumerate(groups):
        tabs.append(f'<button type="button" role="tab" id="tab-{k+1}" aria-controls="dzial-{k+1}" aria-selected="{"true" if k == 0 else "false"}"{"" if k == 0 else " tabindex=\"-1\""}>{name}<small>{len(pages)}</small></button>')
        cards = []
        for j, p in enumerate(pages):
            n += 1
            big = ' n-big' if j == 0 else ''
            deco = '<svg class="n-gl" viewBox="-200 -200 400 400" aria-hidden="true"><use href="#n-gil" x="-200" y="-200" width="400" height="400"/></svg>' if j == 0 else ''
            cards.append(f'<a class="n-bc{big}" href="{url(p["slug"])}">{deco}<span class="n-top">{svg(p["slug"])}<span class="n-no">§ {n}</span></span><h3>{e(p["menu"])}</h3><p>{e(p["tile"])}</p>{more}</a>')
        r = (len(pages) + 1) % 3
        span = 3 - r if r else 3
        cards.append(f'<a class="n-bc n-cta" style="--sp:{span}" href="/#termin" data-booking-open><span class="n-top">{svg("_cta")}</span><h3>Nie widzisz swojej sprawy?</h3><p>Opisz ją w krótkiej rozmowie – konsultacja do 20 minut jest bezpłatna.</p><em class="n-more">Umów konsultację <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></em></a>')
        panels.append(f'<div class="n-panel{" on" if k == 0 else ""}" id="dzial-{k+1}" role="tabpanel" aria-labelledby="tab-{k+1}"{"" if k == 0 else " hidden"}>{"".join(cards)}</div>')
    sym = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="n-gil" viewBox="-200 -200 400 400"><path d="M150 0L152 4L154 8L155 12L156 16L156 20L155 25L153 28L151 32L148 36L145 39L142 42L139 45L136 48L134 51L132 55L131 58L130 62L130 66L130 71L130 75L130 80L129 84L128 88L127 92L125 96L122 99L118 101L115 103L110 105L106 106L102 107L98 108L94 110L90 111L87 113L84 116L82 119L79 122L77 126L75 130L73 134L70 137L67 140L64 143L60 145L56 146L52 147L48 147L43 146L39 145L35 144L30 143L26 142L22 142L19 142L15 143L11 144L8 146L4 148L0 150L-4 152L-8 154L-12 155L-16 156L-20 156L-25 155L-28 153L-32 151L-36 148L-39 145L-42 142L-45 139L-48 136L-51 134L-55 132L-58 131L-62 130L-66 130L-71 130L-75 130L-80 130L-84 129L-88 128L-92 127L-96 125L-99 122L-101 118L-103 115L-105 110L-106 106L-107 102L-108 98L-110 94L-111 90L-113 87L-116 84L-119 82L-122 79L-126 77L-130 75L-134 73L-137 70L-140 67L-143 64L-145 60L-146 56L-147 52L-147 48L-146 43L-145 39L-144 35L-143 30L-142 26L-142 22L-142 19L-143 15L-144 11L-146 8L-148 4L-150 0L-152 -4L-154 -8L-155 -12L-156 -16L-156 -20L-155 -25L-153 -28L-151 -32L-148 -36L-145 -39L-142 -42L-139 -45L-136 -48L-134 -51L-132 -55L-131 -58L-130 -62L-130 -66L-130 -71L-130 -75L-130 -80L-129 -84L-128 -88L-127 -92L-125 -96L-122 -99L-118 -101L-115 -103L-110 -105L-106 -106L-102 -107L-98 -108L-94 -110L-90 -111L-87 -113L-84 -116L-82 -119L-79 -122L-77 -126L-75 -130L-73 -134L-70 -137L-67 -140L-64 -143L-60 -145L-56 -146L-52 -147L-48 -147L-43 -146L-39 -145L-35 -144L-30 -143L-26 -142L-22 -142L-19 -142L-15 -143L-11 -144L-8 -146L-4 -148L-0 -150L4 -152L8 -154L12 -155L16 -156L20 -156L25 -155L28 -153L32 -151L36 -148L39 -145L42 -142L45 -139L48 -136L51 -134L55 -132L58 -131L62 -130L66 -130L71 -130L75 -130L80 -130L84 -129L88 -128L92 -127L96 -125L99 -122L101 -118L103 -115L105 -110L106 -106L107 -102L108 -98L110 -94L111 -90L113 -87L116 -84L119 -82L122 -79L126 -77L130 -75L134 -73L137 -70L140 -67L143 -64L145 -60L146 -56L147 -52L147 -48L146 -43L145 -39L144 -35L143 -30L142 -26L142 -22L142 -19L143 -15L144 -11L146 -8L148 -4L150 -0ZM153 0L155 4L156 8L156 12L156 16L155 20L153 24L151 28L148 31L145 35L142 38L139 41L137 44L135 48L134 51L133 55L132 59L132 63L133 68L133 72L133 77L132 81L131 85L129 89L127 92L124 95L121 98L117 100L112 101L108 103L104 104L100 105L96 107L93 109L90 111L87 114L85 117L83 121L81 125L79 129L77 133L74 136L71 139L68 142L64 143L60 144L56 145L51 145L47 144L42 143L38 142L34 141L30 141L26 141L22 141L19 142L15 144L12 146L8 149L4 151L0 153L-4 155L-8 156L-12 156L-16 156L-20 155L-24 153L-28 151L-31 148L-35 145L-38 142L-41 139L-44 137L-48 135L-51 134L-55 133L-59 132L-63 132L-68 133L-72 133L-77 133L-81 132L-85 131L-89 129L-92 127L-95 124L-98 121L-100 117L-101 112L-103 108L-104 104L-105 100L-107 96L-109 93L-111 90L-114 87L-117 85L-121 83L-125 81L-129 79L-133 77L-136 74L-139 71L-142 68L-143 64L-144 60L-145 56L-145 51L-144 47L-143 42L-142 38L-141 34L-141 30L-141 26L-141 22L-142 19L-144 15L-146 12L-149 8L-151 4L-153 0L-155 -4L-156 -8L-156 -12L-156 -16L-155 -20L-153 -24L-151 -28L-148 -31L-145 -35L-142 -38L-139 -41L-137 -44L-135 -48L-134 -51L-133 -55L-132 -59L-132 -63L-133 -68L-133 -72L-133 -77L-132 -81L-131 -85L-129 -89L-127 -92L-124 -95L-121 -98L-117 -100L-112 -101L-108 -103L-104 -104L-100 -105L-96 -107L-93 -109L-90 -111L-87 -114L-85 -117L-83 -121L-81 -125L-79 -129L-77 -133L-74 -136L-71 -139L-68 -142L-64 -143L-60 -144L-56 -145L-51 -145L-47 -144L-42 -143L-38 -142L-34 -141L-30 -141L-26 -141L-22 -141L-19 -142L-15 -144L-12 -146L-8 -149L-4 -151L-0 -153L4 -155L8 -156L12 -156L16 -156L20 -155L24 -153L28 -151L31 -148L35 -145L38 -142L41 -139L44 -137L48 -135L51 -134L55 -133L59 -132L63 -132L68 -133L72 -133L77 -133L81 -132L85 -131L89 -129L92 -127L95 -124L98 -121L100 -117L101 -112L103 -108L104 -104L105 -100L107 -96L109 -93L111 -90L114 -87L117 -85L121 -83L125 -81L129 -79L133 -77L136 -74L139 -71L142 -68L143 -64L144 -60L145 -56L145 -51L144 -47L143 -42L142 -38L141 -34L141 -30L141 -26L141 -22L142 -19L144 -15L146 -12L149 -8L151 -4L153 -0ZM155 0L156 4L157 8L156 12L155 16L153 20L151 24L148 27L145 31L142 34L140 37L138 41L136 44L135 48L135 52L135 56L135 60L135 64L135 69L135 73L135 78L133 82L132 86L129 89L126 92L122 94L118 96L114 98L110 99L106 101L102 102L99 104L96 106L93 109L91 112L89 116L87 119L85 123L83 127L80 131L78 135L75 138L71 140L67 141L63 142L59 143L55 142L50 142L46 141L42 140L37 140L33 139L30 140L26 141L23 142L19 144L15 147L12 149L8 152L4 154L0 155L-4 156L-8 157L-12 156L-16 155L-20 153L-24 151L-27 148L-31 145L-34 142L-37 140L-41 138L-44 136L-48 135L-52 135L-56 135L-60 135L-64 135L-69 135L-73 135L-78 135L-82 133L-86 132L-89 129L-92 126L-94 122L-96 118L-98 114L-99 110L-101 106L-102 102L-104 99L-106 96L-109 93L-112 91L-116 89L-119 87L-123 85L-127 83L-131 80L-135 78L-138 75L-140 71L-141 67L-142 63L-143 59L-142 55L-142 50L-141 46L-140 42L-140 37L-139 33L-140 30L-141 26L-142 23L-144 19L-147 15L-149 12L-152 8L-154 4L-155 0L-156 -4L-157 -8L-156 -12L-155 -16L-153 -20L-151 -24L-148 -27L-145 -31L-142 -34L-140 -37L-138 -41L-136 -44L-135 -48L-135 -52L-135 -56L-135 -60L-135 -64L-135 -69L-135 -73L-135 -78L-133 -82L-132 -86L-129 -89L-126 -92L-122 -94L-118 -96L-114 -98L-110 -99L-106 -101L-102 -102L-99 -104L-96 -106L-93 -109L-91 -112L-89 -116L-87 -119L-85 -123L-83 -127L-80 -131L-78 -135L-75 -138L-71 -140L-67 -141L-63 -142L-59 -143L-55 -142L-50 -142L-46 -141L-42 -140L-37 -140L-33 -139L-30 -140L-26 -141L-23 -142L-19 -144L-15 -147L-12 -149L-8 -152L-4 -154L-0 -155L4 -156L8 -157L12 -156L16 -155L20 -153L24 -151L27 -148L31 -145L34 -142L37 -140L41 -138L44 -136L48 -135L52 -135L56 -135L60 -135L64 -135L69 -135L73 -135L78 -135L82 -133L86 -132L89 -129L92 -126L94 -122L96 -118L98 -114L99 -110L101 -106L102 -102L104 -99L106 -96L109 -93L112 -91L116 -89L119 -87L123 -85L127 -83L131 -80L135 -78L138 -75L140 -71L141 -67L142 -63L143 -59L142 -55L142 -50L141 -46L140 -42L140 -37L139 -33L140 -30L141 -26L142 -23L144 -19L147 -15L149 -12L152 -8L154 -4L155 -0ZM157 0L157 4L156 8L155 12L153 16L150 20L148 23L145 27L142 30L140 34L138 37L137 41L137 44L136 48L137 52L137 57L138 61L138 66L138 70L137 74L136 78L134 82L131 85L128 88L124 90L120 92L116 94L112 96L108 97L104 99L101 101L98 104L96 107L94 110L92 114L90 118L89 122L87 126L84 130L82 133L78 136L75 138L71 139L67 140L62 140L58 140L54 139L49 139L45 138L41 138L37 138L33 139L30 140L26 142L23 145L19 147L16 150L12 152L8 154L4 156L0 157L-4 157L-8 156L-12 155L-16 153L-20 150L-23 148L-27 145L-30 142L-34 140L-37 138L-41 137L-44 137L-48 136L-52 137L-57 137L-61 138L-66 138L-70 138L-74 137L-78 136L-82 134L-85 131L-88 128L-90 124L-92 120L-94 116L-96 112L-97 108L-99 104L-101 101L-104 98L-107 96L-110 94L-114 92L-118 90L-122 89L-126 87L-130 84L-133 82L-136 78L-138 75L-139 71L-140 67L-140 62L-140 58L-139 54L-139 49L-138 45L-138 41L-138 37L-139 33L-140 30L-142 26L-145 23L-147 19L-150 16L-152 12L-154 8L-156 4L-157 0L-157 -4L-156 -8L-155 -12L-153 -16L-150 -20L-148 -23L-145 -27L-142 -30L-140 -34L-138 -37L-137 -41L-137 -44L-136 -48L-137 -52L-137 -57L-138 -61L-138 -66L-138 -70L-137 -74L-136 -78L-134 -82L-131 -85L-128 -88L-124 -90L-120 -92L-116 -94L-112 -96L-108 -97L-104 -99L-101 -101L-98 -104L-96 -107L-94 -110L-92 -114L-90 -118L-89 -122L-87 -126L-84 -130L-82 -133L-78 -136L-75 -138L-71 -139L-67 -140L-62 -140L-58 -140L-54 -139L-49 -139L-45 -138L-41 -138L-37 -138L-33 -139L-30 -140L-26 -142L-23 -145L-19 -147L-16 -150L-12 -152L-8 -154L-4 -156L-0 -157L4 -157L8 -156L12 -155L16 -153L20 -150L23 -148L27 -145L30 -142L34 -140L37 -138L41 -137L44 -137L48 -136L52 -137L57 -137L61 -138L66 -138L70 -138L74 -137L78 -136L82 -134L85 -131L88 -128L90 -124L92 -120L94 -116L96 -112L97 -108L99 -104L101 -101L104 -98L107 -96L110 -94L114 -92L118 -90L122 -89L126 -87L130 -84L133 -82L136 -78L138 -75L139 -71L140 -67L140 -62L140 -58L139 -54L139 -49L138 -45L138 -41L138 -37L139 -33L140 -30L142 -26L145 -23L147 -19L150 -16L152 -12L154 -8L156 -4L157 -0ZM157 0L156 4L154 8L152 12L150 16L147 19L145 23L142 26L140 30L139 33L138 37L138 41L138 45L139 49L139 54L140 58L140 62L140 67L139 71L138 75L136 78L133 82L130 84L126 87L122 89L118 90L114 92L110 94L107 96L104 98L101 101L99 104L97 108L96 112L94 116L92 120L90 124L88 128L85 131L82 134L78 136L74 137L70 138L66 138L61 138L57 137L52 137L48 136L44 137L41 137L37 138L34 140L30 142L27 145L23 148L20 150L16 153L12 155L8 156L4 157L0 157L-4 156L-8 154L-12 152L-16 150L-19 147L-23 145L-26 142L-30 140L-33 139L-37 138L-41 138L-45 138L-49 139L-54 139L-58 140L-62 140L-67 140L-71 139L-75 138L-78 136L-82 133L-84 130L-87 126L-89 122L-90 118L-92 114L-94 110L-96 107L-98 104L-101 101L-104 99L-108 97L-112 96L-116 94L-120 92L-124 90L-128 88L-131 85L-134 82L-136 78L-137 74L-138 70L-138 66L-138 61L-137 57L-137 52L-136 48L-137 44L-137 41L-138 37L-140 34L-142 30L-145 27L-148 23L-150 20L-153 16L-155 12L-156 8L-157 4L-157 0L-156 -4L-154 -8L-152 -12L-150 -16L-147 -19L-145 -23L-142 -26L-140 -30L-139 -33L-138 -37L-138 -41L-138 -45L-139 -49L-139 -54L-140 -58L-140 -62L-140 -67L-139 -71L-138 -75L-136 -78L-133 -82L-130 -84L-126 -87L-122 -89L-118 -90L-114 -92L-110 -94L-107 -96L-104 -98L-101 -101L-99 -104L-97 -108L-96 -112L-94 -116L-92 -120L-90 -124L-88 -128L-85 -131L-82 -134L-78 -136L-74 -137L-70 -138L-66 -138L-61 -138L-57 -137L-52 -137L-48 -136L-44 -137L-41 -137L-37 -138L-34 -140L-30 -142L-27 -145L-23 -148L-20 -150L-16 -153L-12 -155L-8 -156L-4 -157L-0 -157L4 -156L8 -154L12 -152L16 -150L19 -147L23 -145L26 -142L30 -140L33 -139L37 -138L41 -138L45 -138L49 -139L54 -139L58 -140L62 -140L67 -140L71 -139L75 -138L78 -136L82 -133L84 -130L87 -126L89 -122L90 -118L92 -114L94 -110L96 -107L98 -104L101 -101L104 -99L108 -97L112 -96L116 -94L120 -92L124 -90L128 -88L131 -85L134 -82L136 -78L137 -74L138 -70L138 -66L138 -61L137 -57L137 -52L136 -48L137 -44L137 -41L138 -37L140 -34L142 -30L145 -27L148 -23L150 -20L153 -16L155 -12L156 -8L157 -4L157 -0ZM155 0L154 4L152 8L149 12L147 15L144 19L142 23L141 26L140 30L139 33L140 37L140 42L141 46L142 50L142 55L143 59L142 63L141 67L140 71L138 75L135 78L131 80L127 83L123 85L119 87L116 89L112 91L109 93L106 96L104 99L102 102L101 106L99 110L98 114L96 118L94 122L92 126L89 129L86 132L82 133L78 135L73 135L69 135L64 135L60 135L56 135L52 135L48 135L44 136L41 138L37 140L34 142L31 145L27 148L24 151L20 153L16 155L12 156L8 157L4 156L0 155L-4 154L-8 152L-12 149L-15 147L-19 144L-23 142L-26 141L-30 140L-33 139L-37 140L-42 140L-46 141L-50 142L-55 142L-59 143L-63 142L-67 141L-71 140L-75 138L-78 135L-80 131L-83 127L-85 123L-87 119L-89 116L-91 112L-93 109L-96 106L-99 104L-102 102L-106 101L-110 99L-114 98L-118 96L-122 94L-126 92L-129 89L-132 86L-133 82L-135 78L-135 73L-135 69L-135 64L-135 60L-135 56L-135 52L-135 48L-136 44L-138 41L-140 37L-142 34L-145 31L-148 27L-151 24L-153 20L-155 16L-156 12L-157 8L-156 4L-155 0L-154 -4L-152 -8L-149 -12L-147 -15L-144 -19L-142 -23L-141 -26L-140 -30L-139 -33L-140 -37L-140 -42L-141 -46L-142 -50L-142 -55L-143 -59L-142 -63L-141 -67L-140 -71L-138 -75L-135 -78L-131 -80L-127 -83L-123 -85L-119 -87L-116 -89L-112 -91L-109 -93L-106 -96L-104 -99L-102 -102L-101 -106L-99 -110L-98 -114L-96 -118L-94 -122L-92 -126L-89 -129L-86 -132L-82 -133L-78 -135L-73 -135L-69 -135L-64 -135L-60 -135L-56 -135L-52 -135L-48 -135L-44 -136L-41 -138L-37 -140L-34 -142L-31 -145L-27 -148L-24 -151L-20 -153L-16 -155L-12 -156L-8 -157L-4 -156L-0 -155L4 -154L8 -152L12 -149L15 -147L19 -144L23 -142L26 -141L30 -140L33 -139L37 -140L42 -140L46 -141L50 -142L55 -142L59 -143L63 -142L67 -141L71 -140L75 -138L78 -135L80 -131L83 -127L85 -123L87 -119L89 -116L91 -112L93 -109L96 -106L99 -104L102 -102L106 -101L110 -99L114 -98L118 -96L122 -94L126 -92L129 -89L132 -86L133 -82L135 -78L135 -73L135 -69L135 -64L135 -60L135 -56L135 -52L135 -48L136 -44L138 -41L140 -37L142 -34L145 -31L148 -27L151 -24L153 -20L155 -16L156 -12L157 -8L156 -4L155 -0ZM153 0L151 4L149 8L146 12L144 15L142 19L141 22L141 26L141 30L141 34L142 38L143 42L144 47L145 51L145 56L144 60L143 64L142 68L139 71L136 74L133 77L129 79L125 81L121 83L117 85L114 87L111 90L109 93L107 96L105 100L104 104L103 108L101 112L100 117L98 121L95 124L92 127L89 129L85 131L81 132L77 133L72 133L68 133L63 132L59 132L55 133L51 134L48 135L44 137L41 139L38 142L35 145L31 148L28 151L24 153L20 155L16 156L12 156L8 156L4 155L0 153L-4 151L-8 149L-12 146L-15 144L-19 142L-22 141L-26 141L-30 141L-34 141L-38 142L-42 143L-47 144L-51 145L-56 145L-60 144L-64 143L-68 142L-71 139L-74 136L-77 133L-79 129L-81 125L-83 121L-85 117L-87 114L-90 111L-93 109L-96 107L-100 105L-104 104L-108 103L-112 101L-117 100L-121 98L-124 95L-127 92L-129 89L-131 85L-132 81L-133 77L-133 72L-133 68L-132 63L-132 59L-133 55L-134 51L-135 48L-137 44L-139 41L-142 38L-145 35L-148 31L-151 28L-153 24L-155 20L-156 16L-156 12L-156 8L-155 4L-153 0L-151 -4L-149 -8L-146 -12L-144 -15L-142 -19L-141 -22L-141 -26L-141 -30L-141 -34L-142 -38L-143 -42L-144 -47L-145 -51L-145 -56L-144 -60L-143 -64L-142 -68L-139 -71L-136 -74L-133 -77L-129 -79L-125 -81L-121 -83L-117 -85L-114 -87L-111 -90L-109 -93L-107 -96L-105 -100L-104 -104L-103 -108L-101 -112L-100 -117L-98 -121L-95 -124L-92 -127L-89 -129L-85 -131L-81 -132L-77 -133L-72 -133L-68 -133L-63 -132L-59 -132L-55 -133L-51 -134L-48 -135L-44 -137L-41 -139L-38 -142L-35 -145L-31 -148L-28 -151L-24 -153L-20 -155L-16 -156L-12 -156L-8 -156L-4 -155L-0 -153L4 -151L8 -149L12 -146L15 -144L19 -142L22 -141L26 -141L30 -141L34 -141L38 -142L42 -143L47 -144L51 -145L56 -145L60 -144L64 -143L68 -142L71 -139L74 -136L77 -133L79 -129L81 -125L83 -121L85 -117L87 -114L90 -111L93 -109L96 -107L100 -105L104 -104L108 -103L112 -101L117 -100L121 -98L124 -95L127 -92L129 -89L131 -85L132 -81L133 -77L133 -72L133 -68L132 -63L132 -59L133 -55L134 -51L135 -48L137 -44L139 -41L142 -38L145 -35L148 -31L151 -28L153 -24L155 -20L156 -16L156 -12L156 -8L155 -4L153 -0ZM150 0L148 4L146 8L144 11L143 15L142 19L142 22L142 26L143 30L144 35L145 39L146 43L147 48L147 52L146 56L145 60L143 64L140 67L137 70L134 73L130 75L126 77L122 79L119 82L116 84L113 87L111 90L110 94L108 98L107 102L106 106L105 110L103 115L101 118L99 122L96 125L92 127L88 128L84 129L80 130L75 130L71 130L66 130L62 130L58 131L55 132L51 134L48 136L45 139L42 142L39 145L36 148L32 151L28 153L25 155L20 156L16 156L12 155L8 154L4 152L0 150L-4 148L-8 146L-11 144L-15 143L-19 142L-22 142L-26 142L-30 143L-35 144L-39 145L-43 146L-48 147L-52 147L-56 146L-60 145L-64 143L-67 140L-70 137L-73 134L-75 130L-77 126L-79 122L-82 119L-84 116L-87 113L-90 111L-94 110L-98 108L-102 107L-106 106L-110 105L-115 103L-118 101L-122 99L-125 96L-127 92L-128 88L-129 84L-130 80L-130 75L-130 71L-130 66L-130 62L-131 58L-132 55L-134 51L-136 48L-139 45L-142 42L-145 39L-148 36L-151 32L-153 28L-155 25L-156 20L-156 16L-155 12L-154 8L-152 4L-150 0L-148 -4L-146 -8L-144 -11L-143 -15L-142 -19L-142 -22L-142 -26L-143 -30L-144 -35L-145 -39L-146 -43L-147 -48L-147 -52L-146 -56L-145 -60L-143 -64L-140 -67L-137 -70L-134 -73L-130 -75L-126 -77L-122 -79L-119 -82L-116 -84L-113 -87L-111 -90L-110 -94L-108 -98L-107 -102L-106 -106L-105 -110L-103 -115L-101 -118L-99 -122L-96 -125L-92 -127L-88 -128L-84 -129L-80 -130L-75 -130L-71 -130L-66 -130L-62 -130L-58 -131L-55 -132L-51 -134L-48 -136L-45 -139L-42 -142L-39 -145L-36 -148L-32 -151L-28 -153L-25 -155L-20 -156L-16 -156L-12 -155L-8 -154L-4 -152L-0 -150L4 -148L8 -146L11 -144L15 -143L19 -142L22 -142L26 -142L30 -143L35 -144L39 -145L43 -146L48 -147L52 -147L56 -146L60 -145L64 -143L67 -140L70 -137L73 -134L75 -130L77 -126L79 -122L82 -119L84 -116L87 -113L90 -111L94 -110L98 -108L102 -107L106 -106L110 -105L115 -103L118 -101L122 -99L125 -96L127 -92L128 -88L129 -84L130 -80L130 -75L130 -71L130 -66L130 -62L131 -58L132 -55L134 -51L136 -48L139 -45L142 -42L145 -39L148 -36L151 -32L153 -28L155 -25L156 -20L156 -16L155 -12L154 -8L152 -4L150 -0ZM147 0L145 4L144 8L143 11L142 15L142 19L143 23L144 27L145 31L147 35L148 40L148 44L149 48L148 52L147 56L144 60L142 63L138 66L135 69L131 71L127 73L124 76L121 78L118 81L116 84L114 87L113 91L112 95L111 100L109 104L108 108L107 112L104 116L102 119L99 122L95 124L91 125L87 126L82 127L78 127L73 127L69 128L65 128L62 129L58 131L55 133L52 135L49 138L46 141L43 145L40 148L36 151L32 153L29 154L25 155L20 155L16 154L12 153L8 151L4 149L0 147L-4 145L-8 144L-11 143L-15 142L-19 142L-23 143L-27 144L-31 145L-35 147L-40 148L-44 148L-48 149L-52 148L-56 147L-60 144L-63 142L-66 138L-69 135L-71 131L-73 127L-76 124L-78 121L-81 118L-84 116L-87 114L-91 113L-95 112L-100 111L-104 109L-108 108L-112 107L-116 104L-119 102L-122 99L-124 95L-125 91L-126 87L-127 82L-127 78L-127 73L-128 69L-128 65L-129 62L-131 58L-133 55L-135 52L-138 49L-141 46L-145 43L-148 40L-151 36L-153 32L-154 29L-155 25L-155 20L-154 16L-153 12L-151 8L-149 4L-147 0L-145 -4L-144 -8L-143 -11L-142 -15L-142 -19L-143 -23L-144 -27L-145 -31L-147 -35L-148 -40L-148 -44L-149 -48L-148 -52L-147 -56L-144 -60L-142 -63L-138 -66L-135 -69L-131 -71L-127 -73L-124 -76L-121 -78L-118 -81L-116 -84L-114 -87L-113 -91L-112 -95L-111 -100L-109 -104L-108 -108L-107 -112L-104 -116L-102 -119L-99 -122L-95 -124L-91 -125L-87 -126L-82 -127L-78 -127L-73 -127L-69 -128L-65 -128L-62 -129L-58 -131L-55 -133L-52 -135L-49 -138L-46 -141L-43 -145L-40 -148L-36 -151L-32 -153L-29 -154L-25 -155L-20 -155L-16 -154L-12 -153L-8 -151L-4 -149L-0 -147L4 -145L8 -144L11 -143L15 -142L19 -142L23 -143L27 -144L31 -145L35 -147L40 -148L44 -148L48 -149L52 -148L56 -147L60 -144L63 -142L66 -138L69 -135L71 -131L73 -127L76 -124L78 -121L81 -118L84 -116L87 -114L91 -113L95 -112L100 -111L104 -109L108 -108L112 -107L116 -104L119 -102L122 -99L124 -95L125 -91L126 -87L127 -82L127 -78L127 -73L128 -69L128 -65L129 -62L131 -58L133 -55L135 -52L138 -49L141 -46L145 -43L148 -40L151 -36L153 -32L154 -29L155 -25L155 -20L154 -16L153 -12L151 -8L149 -4L147 -0ZM145 0L143 4L143 7L143 11L143 15L144 19L146 23L147 27L149 32L150 36L150 40L150 44L149 49L148 52L145 56L143 59L139 62L136 65L132 67L128 70L125 72L122 75L120 78L118 81L117 85L116 89L115 93L114 97L113 102L112 106L110 110L108 114L105 117L102 119L98 121L94 122L90 123L85 124L81 124L76 125L72 125L68 126L65 127L62 129L59 132L56 135L53 138L50 141L47 144L44 148L40 150L37 152L33 154L29 154L24 154L20 153L16 152L12 150L8 148L4 146L0 145L-4 143L-7 143L-11 143L-15 143L-19 144L-23 146L-27 147L-32 149L-36 150L-40 150L-44 150L-49 149L-52 148L-56 145L-59 143L-62 139L-65 136L-67 132L-70 128L-72 125L-75 122L-78 120L-81 118L-85 117L-89 116L-93 115L-97 114L-102 113L-106 112L-110 110L-114 108L-117 105L-119 102L-121 98L-122 94L-123 90L-124 85L-124 81L-125 76L-125 72L-126 68L-127 65L-129 62L-132 59L-135 56L-138 53L-141 50L-144 47L-148 44L-150 40L-152 37L-154 33L-154 29L-154 24L-153 20L-152 16L-150 12L-148 8L-146 4L-145 0L-143 -4L-143 -7L-143 -11L-143 -15L-144 -19L-146 -23L-147 -27L-149 -32L-150 -36L-150 -40L-150 -44L-149 -49L-148 -52L-145 -56L-143 -59L-139 -62L-136 -65L-132 -67L-128 -70L-125 -72L-122 -75L-120 -78L-118 -81L-117 -85L-116 -89L-115 -93L-114 -97L-113 -102L-112 -106L-110 -110L-108 -114L-105 -117L-102 -119L-98 -121L-94 -122L-90 -123L-85 -124L-81 -124L-76 -125L-72 -125L-68 -126L-65 -127L-62 -129L-59 -132L-56 -135L-53 -138L-50 -141L-47 -144L-44 -148L-40 -150L-37 -152L-33 -154L-29 -154L-24 -154L-20 -153L-16 -152L-12 -150L-8 -148L-4 -146L-0 -145L4 -143L7 -143L11 -143L15 -143L19 -144L23 -146L27 -147L32 -149L36 -150L40 -150L44 -150L49 -149L52 -148L56 -145L59 -143L62 -139L65 -136L67 -132L70 -128L72 -125L75 -122L78 -120L81 -118L85 -117L89 -116L93 -115L97 -114L102 -113L106 -112L110 -110L114 -108L117 -105L119 -102L121 -98L122 -94L123 -90L124 -85L124 -81L125 -76L125 -72L126 -68L127 -65L129 -62L132 -59L135 -56L138 -53L141 -50L144 -47L148 -44L150 -40L152 -37L154 -33L154 -29L154 -24L153 -20L152 -16L150 -12L148 -8L146 -4L145 -0ZM143 0L143 4L143 8L144 11L146 15L147 19L149 24L150 28L151 32L152 36L151 41L151 45L149 48L146 52L143 55L140 58L136 61L133 63L130 66L127 69L124 72L122 75L120 78L119 82L118 86L118 90L117 95L116 99L115 103L113 107L111 111L108 114L105 116L101 118L97 119L92 120L88 121L83 121L79 122L75 123L72 124L68 126L65 128L62 131L60 134L57 137L54 141L51 144L48 147L44 150L41 151L37 153L33 153L28 153L24 152L20 150L16 149L12 147L8 145L4 144L0 143L-4 143L-8 143L-11 144L-15 146L-19 147L-24 149L-28 150L-32 151L-36 152L-41 151L-45 151L-48 149L-52 146L-55 143L-58 140L-61 136L-63 133L-66 130L-69 127L-72 124L-75 122L-78 120L-82 119L-86 118L-90 118L-95 117L-99 116L-103 115L-107 113L-111 111L-114 108L-116 105L-118 101L-119 97L-120 92L-121 88L-121 83L-122 79L-123 75L-124 72L-126 68L-128 65L-131 62L-134 60L-137 57L-141 54L-144 51L-147 48L-150 44L-151 41L-153 37L-153 33L-153 28L-152 24L-150 20L-149 16L-147 12L-145 8L-144 4L-143 0L-143 -4L-143 -8L-144 -11L-146 -15L-147 -19L-149 -24L-150 -28L-151 -32L-152 -36L-151 -41L-151 -45L-149 -48L-146 -52L-143 -55L-140 -58L-136 -61L-133 -63L-130 -66L-127 -69L-124 -72L-122 -75L-120 -78L-119 -82L-118 -86L-118 -90L-117 -95L-116 -99L-115 -103L-113 -107L-111 -111L-108 -114L-105 -116L-101 -118L-97 -119L-92 -120L-88 -121L-83 -121L-79 -122L-75 -123L-72 -124L-68 -126L-65 -128L-62 -131L-60 -134L-57 -137L-54 -141L-51 -144L-48 -147L-44 -150L-41 -151L-37 -153L-33 -153L-28 -153L-24 -152L-20 -150L-16 -149L-12 -147L-8 -145L-4 -144L-0 -143L4 -143L8 -143L11 -144L15 -146L19 -147L24 -149L28 -150L32 -151L36 -152L41 -151L45 -151L48 -149L52 -146L55 -143L58 -140L61 -136L63 -133L66 -130L69 -127L72 -124L75 -122L78 -120L82 -119L86 -118L90 -118L95 -117L99 -116L103 -115L107 -113L111 -111L114 -108L116 -105L118 -101L119 -97L120 -92L121 -88L121 -83L122 -79L123 -75L124 -72L126 -68L128 -65L131 -62L134 -60L137 -57L141 -54L144 -51L147 -48L150 -44L151 -41L153 -37L153 -33L153 -28L152 -24L150 -20L149 -16L147 -12L145 -8L144 -4L143 -0ZM143 0L144 4L145 8L147 12L149 16L150 20L152 24L153 28L153 33L153 37L151 41L150 44L147 48L144 51L141 54L137 57L134 60L131 62L128 65L126 68L124 72L123 75L122 79L121 83L121 88L120 92L119 97L118 101L116 105L114 108L111 111L107 113L103 115L99 116L95 117L90 118L86 118L82 119L78 120L75 122L72 124L69 127L66 130L63 133L61 136L58 140L55 143L52 146L48 149L45 151L41 151L36 152L32 151L28 150L24 149L19 147L15 146L11 144L8 143L4 143L0 143L-4 144L-8 145L-12 147L-16 149L-20 150L-24 152L-28 153L-33 153L-37 153L-41 151L-44 150L-48 147L-51 144L-54 141L-57 137L-60 134L-62 131L-65 128L-68 126L-72 124L-75 123L-79 122L-83 121L-88 121L-92 120L-97 119L-101 118L-105 116L-108 114L-111 111L-113 107L-115 103L-116 99L-117 95L-118 90L-118 86L-119 82L-120 78L-122 75L-124 72L-127 69L-130 66L-133 63L-136 61L-140 58L-143 55L-146 52L-149 48L-151 45L-151 41L-152 36L-151 32L-150 28L-149 24L-147 19L-146 15L-144 11L-143 8L-143 4L-143 0L-144 -4L-145 -8L-147 -12L-149 -16L-150 -20L-152 -24L-153 -28L-153 -33L-153 -37L-151 -41L-150 -44L-147 -48L-144 -51L-141 -54L-137 -57L-134 -60L-131 -62L-128 -65L-126 -68L-124 -72L-123 -75L-122 -79L-121 -83L-121 -88L-120 -92L-119 -97L-118 -101L-116 -105L-114 -108L-111 -111L-107 -113L-103 -115L-99 -116L-95 -117L-90 -118L-86 -118L-82 -119L-78 -120L-75 -122L-72 -124L-69 -127L-66 -130L-63 -133L-61 -136L-58 -140L-55 -143L-52 -146L-48 -149L-45 -151L-41 -151L-36 -152L-32 -151L-28 -150L-24 -149L-19 -147L-15 -146L-11 -144L-8 -143L-4 -143L-0 -143L4 -144L8 -145L12 -147L16 -149L20 -150L24 -152L28 -153L33 -153L37 -153L41 -151L44 -150L48 -147L51 -144L54 -141L57 -137L60 -134L62 -131L65 -128L68 -126L72 -124L75 -123L79 -122L83 -121L88 -121L92 -120L97 -119L101 -118L105 -116L108 -114L111 -111L113 -107L115 -103L116 -99L117 -95L118 -90L118 -86L119 -82L120 -78L122 -75L124 -72L127 -69L130 -66L133 -63L136 -61L140 -58L143 -55L146 -52L149 -48L151 -45L151 -41L152 -36L151 -32L150 -28L149 -24L147 -19L146 -15L144 -11L143 -8L143 -4L143 -0ZM145 0L146 4L148 8L150 12L152 16L153 20L154 24L154 29L154 33L152 37L150 40L148 44L144 47L141 50L138 53L135 56L132 59L129 62L127 65L126 68L125 72L125 76L124 81L124 85L123 90L122 94L121 98L119 102L117 105L114 108L110 110L106 112L102 113L97 114L93 115L89 116L85 117L81 118L78 120L75 122L72 125L70 128L67 132L65 136L62 139L59 143L56 145L52 148L49 149L44 150L40 150L36 150L32 149L27 147L23 146L19 144L15 143L11 143L7 143L4 143L0 145L-4 146L-8 148L-12 150L-16 152L-20 153L-24 154L-29 154L-33 154L-37 152L-40 150L-44 148L-47 144L-50 141L-53 138L-56 135L-59 132L-62 129L-65 127L-68 126L-72 125L-76 125L-81 124L-85 124L-90 123L-94 122L-98 121L-102 119L-105 117L-108 114L-110 110L-112 106L-113 102L-114 97L-115 93L-116 89L-117 85L-118 81L-120 78L-122 75L-125 72L-128 70L-132 67L-136 65L-139 62L-143 59L-145 56L-148 52L-149 49L-150 44L-150 40L-150 36L-149 32L-147 27L-146 23L-144 19L-143 15L-143 11L-143 7L-143 4L-145 0L-146 -4L-148 -8L-150 -12L-152 -16L-153 -20L-154 -24L-154 -29L-154 -33L-152 -37L-150 -40L-148 -44L-144 -47L-141 -50L-138 -53L-135 -56L-132 -59L-129 -62L-127 -65L-126 -68L-125 -72L-125 -76L-124 -81L-124 -85L-123 -90L-122 -94L-121 -98L-119 -102L-117 -105L-114 -108L-110 -110L-106 -112L-102 -113L-97 -114L-93 -115L-89 -116L-85 -117L-81 -118L-78 -120L-75 -122L-72 -125L-70 -128L-67 -132L-65 -136L-62 -139L-59 -143L-56 -145L-52 -148L-49 -149L-44 -150L-40 -150L-36 -150L-32 -149L-27 -147L-23 -146L-19 -144L-15 -143L-11 -143L-7 -143L-4 -143L-0 -145L4 -146L8 -148L12 -150L16 -152L20 -153L24 -154L29 -154L33 -154L37 -152L40 -150L44 -148L47 -144L50 -141L53 -138L56 -135L59 -132L62 -129L65 -127L68 -126L72 -125L76 -125L81 -124L85 -124L90 -123L94 -122L98 -121L102 -119L105 -117L108 -114L110 -110L112 -106L113 -102L114 -97L115 -93L116 -89L117 -85L118 -81L120 -78L122 -75L125 -72L128 -70L132 -67L136 -65L139 -62L143 -59L145 -56L148 -52L149 -49L150 -44L150 -40L150 -36L149 -32L147 -27L146 -23L144 -19L143 -15L143 -11L143 -7L143 -4L145 -0ZM147 0L149 4L151 8L153 12L154 16L155 20L155 25L154 29L153 32L151 36L148 40L145 43L141 46L138 49L135 52L133 55L131 58L129 62L128 65L128 69L127 73L127 78L127 82L126 87L125 91L124 95L122 99L119 102L116 104L112 107L108 108L104 109L100 111L95 112L91 113L87 114L84 116L81 118L78 121L76 124L73 127L71 131L69 135L66 138L63 142L60 144L56 147L52 148L48 149L44 148L40 148L35 147L31 145L27 144L23 143L19 142L15 142L11 143L8 144L4 145L0 147L-4 149L-8 151L-12 153L-16 154L-20 155L-25 155L-29 154L-32 153L-36 151L-40 148L-43 145L-46 141L-49 138L-52 135L-55 133L-58 131L-62 129L-65 128L-69 128L-73 127L-78 127L-82 127L-87 126L-91 125L-95 124L-99 122L-102 119L-104 116L-107 112L-108 108L-109 104L-111 100L-112 95L-113 91L-114 87L-116 84L-118 81L-121 78L-124 76L-127 73L-131 71L-135 69L-138 66L-142 63L-144 60L-147 56L-148 52L-149 48L-148 44L-148 40L-147 35L-145 31L-144 27L-143 23L-142 19L-142 15L-143 11L-144 8L-145 4L-147 0L-149 -4L-151 -8L-153 -12L-154 -16L-155 -20L-155 -25L-154 -29L-153 -32L-151 -36L-148 -40L-145 -43L-141 -46L-138 -49L-135 -52L-133 -55L-131 -58L-129 -62L-128 -65L-128 -69L-127 -73L-127 -78L-127 -82L-126 -87L-125 -91L-124 -95L-122 -99L-119 -102L-116 -104L-112 -107L-108 -108L-104 -109L-100 -111L-95 -112L-91 -113L-87 -114L-84 -116L-81 -118L-78 -121L-76 -124L-73 -127L-71 -131L-69 -135L-66 -138L-63 -142L-60 -144L-56 -147L-52 -148L-48 -149L-44 -148L-40 -148L-35 -147L-31 -145L-27 -144L-23 -143L-19 -142L-15 -142L-11 -143L-8 -144L-4 -145L-0 -147L4 -149L8 -151L12 -153L16 -154L20 -155L25 -155L29 -154L32 -153L36 -151L40 -148L43 -145L46 -141L49 -138L52 -135L55 -133L58 -131L62 -129L65 -128L69 -128L73 -127L78 -127L82 -127L87 -126L91 -125L95 -124L99 -122L102 -119L104 -116L107 -112L108 -108L109 -104L111 -100L112 -95L113 -91L114 -87L116 -84L118 -81L121 -78L124 -76L127 -73L131 -71L135 -69L138 -66L142 -63L144 -60L147 -56L148 -52L149 -48L148 -44L148 -40L147 -35L145 -31L144 -27L143 -23L142 -19L142 -15L143 -11L144 -8L145 -4L147 -0ZM176 0L178 5L179 9L179 14L178 19L176 23L174 28L171 32L169 36L167 40L167 45L167 49L167 54L168 59L168 64L166 69L164 73L161 77L157 80L153 83L149 86L147 90L145 94L143 99L142 103L141 108L139 113L137 117L133 120L129 123L124 124L120 126L115 128L112 131L109 134L106 138L103 142L101 147L98 151L94 153L90 155L85 156L80 157L75 157L70 158L66 159L62 161L58 164L54 167L51 171L46 173L42 175L37 176L32 175L28 174L23 173L18 172L13 171L9 172L5 174L0 176L-5 178L-9 179L-14 179L-19 178L-23 176L-28 174L-32 171L-36 169L-40 167L-45 167L-49 167L-54 167L-59 168L-64 168L-69 166L-73 164L-77 161L-80 157L-83 153L-86 149L-90 147L-94 145L-99 143L-103 142L-108 141L-113 139L-117 137L-120 133L-123 129L-124 124L-126 120L-128 115L-131 112L-134 109L-138 106L-142 103L-147 101L-151 98L-153 94L-155 90L-156 85L-157 80L-157 75L-158 70L-159 66L-161 62L-164 58L-167 54L-171 51L-173 46L-175 42L-176 37L-175 32L-174 28L-173 23L-172 18L-171 13L-172 9L-174 5L-176 0L-178 -5L-179 -9L-179 -14L-178 -19L-176 -23L-174 -28L-171 -32L-169 -36L-167 -40L-167 -45L-167 -49L-167 -54L-168 -59L-168 -64L-166 -69L-164 -73L-161 -77L-157 -80L-153 -83L-149 -86L-147 -90L-145 -94L-143 -99L-142 -103L-141 -108L-139 -113L-137 -117L-133 -120L-129 -123L-124 -124L-120 -126L-115 -128L-112 -131L-109 -134L-106 -138L-103 -142L-101 -147L-98 -151L-94 -153L-90 -155L-85 -156L-80 -157L-75 -157L-70 -158L-66 -159L-62 -161L-58 -164L-54 -167L-51 -171L-46 -173L-42 -175L-37 -176L-32 -175L-28 -174L-23 -173L-18 -172L-13 -171L-9 -172L-5 -174L-0 -176L5 -178L9 -179L14 -179L19 -178L23 -176L28 -174L32 -171L36 -169L40 -167L45 -167L49 -167L54 -167L59 -168L64 -168L69 -166L73 -164L77 -161L80 -157L83 -153L86 -149L90 -147L94 -145L99 -143L103 -142L108 -141L113 -139L117 -137L120 -133L123 -129L124 -124L126 -120L128 -115L131 -112L134 -109L138 -106L142 -103L147 -101L151 -98L153 -94L155 -90L156 -85L157 -80L157 -75L158 -70L159 -66L161 -62L164 -58L167 -54L171 -51L173 -46L175 -42L176 -37L175 -32L174 -28L173 -23L172 -18L171 -13L172 -9L174 -5L176 -0ZM179 0L180 5L180 9L179 14L176 19L174 23L171 27L169 31L168 36L168 40L169 45L169 50L170 55L169 60L168 64L165 69L162 72L158 75L155 79L151 82L149 86L147 90L146 95L146 100L144 105L143 109L140 113L136 116L132 119L127 121L123 123L119 125L115 128L112 132L110 136L108 140L105 144L102 148L98 151L94 153L89 154L84 154L79 155L74 155L70 157L66 160L63 163L59 167L55 170L51 172L47 174L42 174L37 173L32 172L27 171L22 171L18 171L14 172L9 174L5 177L0 179L-5 180L-9 180L-14 179L-19 176L-23 174L-27 171L-31 169L-36 168L-40 168L-45 169L-50 169L-55 170L-60 169L-64 168L-69 165L-72 162L-75 158L-79 155L-82 151L-86 149L-90 147L-95 146L-100 146L-105 144L-109 143L-113 140L-116 136L-119 132L-121 127L-123 123L-125 119L-128 115L-132 112L-136 110L-140 108L-144 105L-148 102L-151 98L-153 94L-154 89L-154 84L-155 79L-155 74L-157 70L-160 66L-163 63L-167 59L-170 55L-172 51L-174 47L-174 42L-173 37L-172 32L-171 27L-171 22L-171 18L-172 14L-174 9L-177 5L-179 0L-180 -5L-180 -9L-179 -14L-176 -19L-174 -23L-171 -27L-169 -31L-168 -36L-168 -40L-169 -45L-169 -50L-170 -55L-169 -60L-168 -64L-165 -69L-162 -72L-158 -75L-155 -79L-151 -82L-149 -86L-147 -90L-146 -95L-146 -100L-144 -105L-143 -109L-140 -113L-136 -116L-132 -119L-127 -121L-123 -123L-119 -125L-115 -128L-112 -132L-110 -136L-108 -140L-105 -144L-102 -148L-98 -151L-94 -153L-89 -154L-84 -154L-79 -155L-74 -155L-70 -157L-66 -160L-63 -163L-59 -167L-55 -170L-51 -172L-47 -174L-42 -174L-37 -173L-32 -172L-27 -171L-22 -171L-18 -171L-14 -172L-9 -174L-5 -177L-0 -179L5 -180L9 -180L14 -179L19 -176L23 -174L27 -171L31 -169L36 -168L40 -168L45 -169L50 -169L55 -170L60 -169L64 -168L69 -165L72 -162L75 -158L79 -155L82 -151L86 -149L90 -147L95 -146L100 -146L105 -144L109 -143L113 -140L116 -136L119 -132L121 -127L123 -123L125 -119L128 -115L132 -112L136 -110L140 -108L144 -105L148 -102L151 -98L153 -94L154 -89L154 -84L155 -79L155 -74L157 -70L160 -66L163 -63L167 -59L170 -55L172 -51L174 -47L174 -42L173 -37L172 -32L171 -27L171 -22L171 -18L172 -14L174 -9L177 -5L179 -0ZM180 0L180 5L178 9L176 14L174 18L171 23L170 27L169 31L170 36L170 41L171 46L172 51L171 56L169 60L167 64L163 68L160 71L156 74L153 78L151 82L150 87L149 92L149 97L148 101L146 106L143 109L139 112L134 115L130 117L125 119L122 122L119 125L116 129L114 133L112 138L109 142L106 146L102 148L97 150L92 151L87 151L83 152L78 153L74 155L71 158L67 162L64 166L60 169L56 171L51 172L46 172L41 172L36 171L32 170L27 170L22 171L18 172L14 175L9 177L5 179L0 180L-5 180L-9 178L-14 176L-18 174L-23 171L-27 170L-31 169L-36 170L-41 170L-46 171L-51 172L-56 171L-60 169L-64 167L-68 163L-71 160L-74 156L-78 153L-82 151L-87 150L-92 149L-97 149L-101 148L-106 146L-109 143L-112 139L-115 134L-117 130L-119 125L-122 122L-125 119L-129 116L-133 114L-138 112L-142 109L-146 106L-148 102L-150 97L-151 92L-151 87L-152 83L-153 78L-155 74L-158 71L-162 67L-166 64L-169 60L-171 56L-172 51L-172 46L-172 41L-171 36L-170 32L-170 27L-171 22L-172 18L-175 14L-177 9L-179 5L-180 0L-180 -5L-178 -9L-176 -14L-174 -18L-171 -23L-170 -27L-169 -31L-170 -36L-170 -41L-171 -46L-172 -51L-171 -56L-169 -60L-167 -64L-163 -68L-160 -71L-156 -74L-153 -78L-151 -82L-150 -87L-149 -92L-149 -97L-148 -101L-146 -106L-143 -109L-139 -112L-134 -115L-130 -117L-125 -119L-122 -122L-119 -125L-116 -129L-114 -133L-112 -138L-109 -142L-106 -146L-102 -148L-97 -150L-92 -151L-87 -151L-83 -152L-78 -153L-74 -155L-71 -158L-67 -162L-64 -166L-60 -169L-56 -171L-51 -172L-46 -172L-41 -172L-36 -171L-32 -170L-27 -170L-22 -171L-18 -172L-14 -175L-9 -177L-5 -179L-0 -180L5 -180L9 -178L14 -176L18 -174L23 -171L27 -170L31 -169L36 -170L41 -170L46 -171L51 -172L56 -171L60 -169L64 -167L68 -163L71 -160L74 -156L78 -153L82 -151L87 -150L92 -149L97 -149L101 -148L106 -146L109 -143L112 -139L115 -134L117 -130L119 -125L122 -122L125 -119L129 -116L133 -114L138 -112L142 -109L146 -106L148 -102L150 -97L151 -92L151 -87L152 -83L153 -78L155 -74L158 -71L162 -67L166 -64L169 -60L171 -56L172 -51L172 -46L172 -41L171 -36L170 -32L170 -27L171 -22L172 -18L175 -14L177 -9L179 -5L180 -0ZM179 0L178 5L176 9L173 14L172 18L171 22L170 27L171 32L172 37L173 42L173 46L173 51L171 55L168 59L164 63L161 67L158 70L155 74L154 78L153 83L152 88L152 93L151 98L148 102L145 105L141 108L137 111L132 113L128 115L125 118L122 122L120 126L118 131L116 135L113 139L110 143L105 145L101 147L96 148L91 148L86 149L82 151L78 154L75 157L72 161L68 164L64 168L60 170L55 171L51 171L46 170L41 169L36 169L31 169L27 170L23 173L18 175L14 177L9 179L5 180L0 179L-5 178L-9 176L-14 173L-18 172L-22 171L-27 170L-32 171L-37 172L-42 173L-46 173L-51 173L-55 171L-59 168L-63 164L-67 161L-70 158L-74 155L-78 154L-83 153L-88 152L-93 152L-98 151L-102 148L-105 145L-108 141L-111 137L-113 132L-115 128L-118 125L-122 122L-126 120L-131 118L-135 116L-139 113L-143 110L-145 105L-147 101L-148 96L-148 91L-149 86L-151 82L-154 78L-157 75L-161 72L-164 68L-168 64L-170 60L-171 55L-171 51L-170 46L-169 41L-169 36L-169 31L-170 27L-173 23L-175 18L-177 14L-179 9L-180 5L-179 0L-178 -5L-176 -9L-173 -14L-172 -18L-171 -22L-170 -27L-171 -32L-172 -37L-173 -42L-173 -46L-173 -51L-171 -55L-168 -59L-164 -63L-161 -67L-158 -70L-155 -74L-154 -78L-153 -83L-152 -88L-152 -93L-151 -98L-148 -102L-145 -105L-141 -108L-137 -111L-132 -113L-128 -115L-125 -118L-122 -122L-120 -126L-118 -131L-116 -135L-113 -139L-110 -143L-105 -145L-101 -147L-96 -148L-91 -148L-86 -149L-82 -151L-78 -154L-75 -157L-72 -161L-68 -164L-64 -168L-60 -170L-55 -171L-51 -171L-46 -170L-41 -169L-36 -169L-31 -169L-27 -170L-23 -173L-18 -175L-14 -177L-9 -179L-5 -180L-0 -179L5 -178L9 -176L14 -173L18 -172L22 -171L27 -170L32 -171L37 -172L42 -173L46 -173L51 -173L55 -171L59 -168L63 -164L67 -161L70 -158L74 -155L78 -154L83 -153L88 -152L93 -152L98 -151L102 -148L105 -145L108 -141L111 -137L113 -132L115 -128L118 -125L122 -122L126 -120L131 -118L135 -116L139 -113L143 -110L145 -105L147 -101L148 -96L148 -91L149 -86L151 -82L154 -78L157 -75L161 -72L164 -68L168 -64L170 -60L171 -55L171 -51L170 -46L169 -41L169 -36L169 -31L170 -27L173 -23L175 -18L177 -14L179 -9L180 -5L179 -0ZM177 0L175 5L173 9L172 14L171 18L171 23L172 27L174 32L175 37L175 42L174 47L172 51L169 55L165 59L162 62L159 66L157 70L156 74L156 79L155 84L155 89L153 94L151 98L148 101L143 104L139 107L135 109L131 112L128 115L125 119L123 123L122 128L119 133L117 137L113 140L109 142L104 143L99 144L94 145L90 147L86 149L83 152L79 156L76 159L73 163L69 166L64 168L60 169L55 169L50 168L45 168L40 167L36 168L32 170L27 172L23 175L19 178L14 179L9 180L5 179L0 177L-5 175L-9 173L-14 172L-18 171L-23 171L-27 172L-32 174L-37 175L-42 175L-47 174L-51 172L-55 169L-59 165L-62 162L-66 159L-70 157L-74 156L-79 156L-84 155L-89 155L-94 153L-98 151L-101 148L-104 143L-107 139L-109 135L-112 131L-115 128L-119 125L-123 123L-128 122L-133 119L-137 117L-140 113L-142 109L-143 104L-144 99L-145 94L-147 90L-149 86L-152 83L-156 79L-159 76L-163 73L-166 69L-168 64L-169 60L-169 55L-168 50L-168 45L-167 40L-168 36L-170 32L-172 27L-175 23L-178 19L-179 14L-180 9L-179 5L-177 0L-175 -5L-173 -9L-172 -14L-171 -18L-171 -23L-172 -27L-174 -32L-175 -37L-175 -42L-174 -47L-172 -51L-169 -55L-165 -59L-162 -62L-159 -66L-157 -70L-156 -74L-156 -79L-155 -84L-155 -89L-153 -94L-151 -98L-148 -101L-143 -104L-139 -107L-135 -109L-131 -112L-128 -115L-125 -119L-123 -123L-122 -128L-119 -133L-117 -137L-113 -140L-109 -142L-104 -143L-99 -144L-94 -145L-90 -147L-86 -149L-83 -152L-79 -156L-76 -159L-73 -163L-69 -166L-64 -168L-60 -169L-55 -169L-50 -168L-45 -168L-40 -167L-36 -168L-32 -170L-27 -172L-23 -175L-19 -178L-14 -179L-9 -180L-5 -179L-0 -177L5 -175L9 -173L14 -172L18 -171L23 -171L27 -172L32 -174L37 -175L42 -175L47 -174L51 -172L55 -169L59 -165L62 -162L66 -159L70 -157L74 -156L79 -156L84 -155L89 -155L94 -153L98 -151L101 -148L104 -143L107 -139L109 -135L112 -131L115 -128L119 -125L123 -123L128 -122L133 -119L137 -117L140 -113L142 -109L143 -104L144 -99L145 -94L147 -90L149 -86L152 -83L156 -79L159 -76L163 -73L166 -69L168 -64L169 -60L169 -55L168 -50L168 -45L167 -40L168 -36L170 -32L172 -27L175 -23L178 -19L179 -14L180 -9L179 -5L177 -0ZM175 0L173 5L172 9L172 14L172 18L174 23L175 28L176 33L176 37L175 42L172 46L169 50L166 54L163 58L161 62L159 66L158 71L158 75L158 81L157 85L156 90L153 94L150 97L146 100L141 103L137 105L134 108L131 112L129 116L127 121L125 125L123 130L120 134L117 137L112 139L108 140L103 141L98 143L94 144L90 147L87 150L84 154L81 158L77 162L73 164L69 166L64 167L59 167L54 166L49 166L45 166L40 167L36 170L32 172L28 175L23 178L19 179L14 179L9 178L5 177L0 175L-5 173L-9 172L-14 172L-18 172L-23 174L-28 175L-33 176L-37 176L-42 175L-46 172L-50 169L-54 166L-58 163L-62 161L-66 159L-71 158L-75 158L-81 158L-85 157L-90 156L-94 153L-97 150L-100 146L-103 141L-105 137L-108 134L-112 131L-116 129L-121 127L-125 125L-130 123L-134 120L-137 117L-139 112L-140 108L-141 103L-143 98L-144 94L-147 90L-150 87L-154 84L-158 81L-162 77L-164 73L-166 69L-167 64L-167 59L-166 54L-166 49L-166 45L-167 40L-170 36L-172 32L-175 28L-178 23L-179 19L-179 14L-178 9L-177 5L-175 0L-173 -5L-172 -9L-172 -14L-172 -18L-174 -23L-175 -28L-176 -33L-176 -37L-175 -42L-172 -46L-169 -50L-166 -54L-163 -58L-161 -62L-159 -66L-158 -71L-158 -75L-158 -81L-157 -85L-156 -90L-153 -94L-150 -97L-146 -100L-141 -103L-137 -105L-134 -108L-131 -112L-129 -116L-127 -121L-125 -125L-123 -130L-120 -134L-117 -137L-112 -139L-108 -140L-103 -141L-98 -143L-94 -144L-90 -147L-87 -150L-84 -154L-81 -158L-77 -162L-73 -164L-69 -166L-64 -167L-59 -167L-54 -166L-49 -166L-45 -166L-40 -167L-36 -170L-32 -172L-28 -175L-23 -178L-19 -179L-14 -179L-9 -178L-5 -177L-0 -175L5 -173L9 -172L14 -172L18 -172L23 -174L28 -175L33 -176L37 -176L42 -175L46 -172L50 -169L54 -166L58 -163L62 -161L66 -159L71 -158L75 -158L81 -158L85 -157L90 -156L94 -153L97 -150L100 -146L103 -141L105 -137L108 -134L112 -131L116 -129L121 -127L125 -125L130 -123L134 -120L137 -117L139 -112L140 -108L141 -103L143 -98L144 -94L147 -90L150 -87L154 -84L158 -81L162 -77L164 -73L166 -69L167 -64L167 -59L166 -54L166 -49L166 -45L167 -40L170 -36L172 -32L175 -28L178 -23L179 -19L179 -14L178 -9L177 -5L175 -0ZM173 0L172 5L172 9L173 14L175 18L176 23L177 28L177 33L176 37L173 42L170 46L167 49L164 53L162 57L161 62L161 67L161 72L161 77L160 81L158 86L155 90L152 93L148 96L143 99L140 101L136 105L134 109L132 113L131 118L129 123L127 127L124 131L120 133L116 135L111 137L106 138L101 140L97 142L94 145L91 148L88 152L85 156L81 160L77 162L73 164L68 164L63 164L58 164L53 164L49 165L45 167L41 169L37 172L32 175L28 177L23 178L19 178L14 177L9 176L5 174L0 173L-5 172L-9 172L-14 173L-18 175L-23 176L-28 177L-33 177L-37 176L-42 173L-46 170L-49 167L-53 164L-57 162L-62 161L-67 161L-72 161L-77 161L-81 160L-86 158L-90 155L-93 152L-96 148L-99 143L-101 140L-105 136L-109 134L-113 132L-118 131L-123 129L-127 127L-131 124L-133 120L-135 116L-137 111L-138 106L-140 101L-142 97L-145 94L-148 91L-152 88L-156 85L-160 81L-162 77L-164 73L-164 68L-164 63L-164 58L-164 53L-165 49L-167 45L-169 41L-172 37L-175 32L-177 28L-178 23L-178 19L-177 14L-176 9L-174 5L-173 0L-172 -5L-172 -9L-173 -14L-175 -18L-176 -23L-177 -28L-177 -33L-176 -37L-173 -42L-170 -46L-167 -49L-164 -53L-162 -57L-161 -62L-161 -67L-161 -72L-161 -77L-160 -81L-158 -86L-155 -90L-152 -93L-148 -96L-143 -99L-140 -101L-136 -105L-134 -109L-132 -113L-131 -118L-129 -123L-127 -127L-124 -131L-120 -133L-116 -135L-111 -137L-106 -138L-101 -140L-97 -142L-94 -145L-91 -148L-88 -152L-85 -156L-81 -160L-77 -162L-73 -164L-68 -164L-63 -164L-58 -164L-53 -164L-49 -165L-45 -167L-41 -169L-37 -172L-32 -175L-28 -177L-23 -178L-19 -178L-14 -177L-9 -176L-5 -174L-0 -173L5 -172L9 -172L14 -173L18 -175L23 -176L28 -177L33 -177L37 -176L42 -173L46 -170L49 -167L53 -164L57 -162L62 -161L67 -161L72 -161L77 -161L81 -160L86 -158L90 -155L93 -152L96 -148L99 -143L101 -140L105 -136L109 -134L113 -132L118 -131L123 -129L127 -127L131 -124L133 -120L135 -116L137 -111L138 -106L140 -101L142 -97L145 -94L148 -91L152 -88L156 -85L160 -81L162 -77L164 -73L164 -68L164 -63L164 -58L164 -53L165 -49L167 -45L169 -41L172 -37L175 -32L177 -28L178 -23L178 -19L177 -14L176 -9L174 -5L173 -0ZM172 0L173 5L174 9L176 14L178 19L178 23L178 28L176 33L173 37L170 41L168 45L165 49L164 53L163 58L163 63L163 68L163 73L162 77L160 82L157 85L154 89L149 92L145 94L142 98L139 101L137 105L136 110L134 115L133 119L130 124L127 127L123 130L119 132L114 133L109 135L105 137L101 139L98 143L95 146L92 151L89 155L86 158L82 160L77 162L72 162L67 162L62 162L57 162L53 164L49 166L45 169L41 172L37 175L33 177L28 178L23 178L19 176L14 175L9 173L5 172L0 172L-5 173L-9 174L-14 176L-19 178L-23 178L-28 178L-33 176L-37 173L-41 170L-45 168L-49 165L-53 164L-58 163L-63 163L-68 163L-73 163L-77 162L-82 160L-85 157L-89 154L-92 149L-94 145L-98 142L-101 139L-105 137L-110 136L-115 134L-119 133L-124 130L-127 127L-130 123L-132 119L-133 114L-135 109L-137 105L-139 101L-143 98L-146 95L-151 92L-155 89L-158 86L-160 82L-162 77L-162 72L-162 67L-162 62L-162 57L-164 53L-166 49L-169 45L-172 41L-175 37L-177 33L-178 28L-178 23L-176 19L-175 14L-173 9L-172 5L-172 0L-173 -5L-174 -9L-176 -14L-178 -19L-178 -23L-178 -28L-176 -33L-173 -37L-170 -41L-168 -45L-165 -49L-164 -53L-163 -58L-163 -63L-163 -68L-163 -73L-162 -77L-160 -82L-157 -85L-154 -89L-149 -92L-145 -94L-142 -98L-139 -101L-137 -105L-136 -110L-134 -115L-133 -119L-130 -124L-127 -127L-123 -130L-119 -132L-114 -133L-109 -135L-105 -137L-101 -139L-98 -143L-95 -146L-92 -151L-89 -155L-86 -158L-82 -160L-77 -162L-72 -162L-67 -162L-62 -162L-57 -162L-53 -164L-49 -166L-45 -169L-41 -172L-37 -175L-33 -177L-28 -178L-23 -178L-19 -176L-14 -175L-9 -173L-5 -172L-0 -172L5 -173L9 -174L14 -176L19 -178L23 -178L28 -178L33 -176L37 -173L41 -170L45 -168L49 -165L53 -164L58 -163L63 -163L68 -163L73 -163L77 -162L82 -160L85 -157L89 -154L92 -149L94 -145L98 -142L101 -139L105 -137L110 -136L115 -134L119 -133L124 -130L127 -127L130 -123L132 -119L133 -114L135 -109L137 -105L139 -101L143 -98L146 -95L151 -92L155 -89L158 -86L160 -82L162 -77L162 -72L162 -67L162 -62L162 -57L164 -53L166 -49L169 -45L172 -41L175 -37L177 -33L178 -28L178 -23L176 -19L175 -14L173 -9L172 -5L172 -0ZM173 0L175 5L177 9L179 14L179 19L178 23L176 28L174 32L171 36L168 40L166 45L165 49L165 54L165 59L166 64L165 69L164 73L162 77L159 81L155 84L151 87L147 90L144 94L142 98L140 102L139 107L138 112L136 116L134 120L130 124L126 126L122 128L117 130L112 132L108 134L105 137L102 140L99 144L97 149L94 153L90 156L86 158L81 159L76 159L71 160L66 160L62 161L57 162L54 165L50 168L46 171L42 174L37 176L33 177L28 176L23 175L18 174L14 172L9 172L5 172L0 173L-5 175L-9 177L-14 179L-19 179L-23 178L-28 176L-32 174L-36 171L-40 168L-45 166L-49 165L-54 165L-59 165L-64 166L-69 165L-73 164L-77 162L-81 159L-84 155L-87 151L-90 147L-94 144L-98 142L-102 140L-107 139L-112 138L-116 136L-120 134L-124 130L-126 126L-128 122L-130 117L-132 112L-134 108L-137 105L-140 102L-144 99L-149 97L-153 94L-156 90L-158 86L-159 81L-159 76L-160 71L-160 66L-161 62L-162 57L-165 54L-168 50L-171 46L-174 42L-176 37L-177 33L-176 28L-175 23L-174 18L-172 14L-172 9L-172 5L-173 0L-175 -5L-177 -9L-179 -14L-179 -19L-178 -23L-176 -28L-174 -32L-171 -36L-168 -40L-166 -45L-165 -49L-165 -54L-165 -59L-166 -64L-165 -69L-164 -73L-162 -77L-159 -81L-155 -84L-151 -87L-147 -90L-144 -94L-142 -98L-140 -102L-139 -107L-138 -112L-136 -116L-134 -120L-130 -124L-126 -126L-122 -128L-117 -130L-112 -132L-108 -134L-105 -137L-102 -140L-99 -144L-97 -149L-94 -153L-90 -156L-86 -158L-81 -159L-76 -159L-71 -160L-66 -160L-62 -161L-57 -162L-54 -165L-50 -168L-46 -171L-42 -174L-37 -176L-33 -177L-28 -176L-23 -175L-18 -174L-14 -172L-9 -172L-5 -172L-0 -173L5 -175L9 -177L14 -179L19 -179L23 -178L28 -176L32 -174L36 -171L40 -168L45 -166L49 -165L54 -165L59 -165L64 -166L69 -165L73 -164L77 -162L81 -159L84 -155L87 -151L90 -147L94 -144L98 -142L102 -140L107 -139L112 -138L116 -136L120 -134L124 -130L126 -126L128 -122L130 -117L132 -112L134 -108L137 -105L140 -102L144 -99L149 -97L153 -94L156 -90L158 -86L159 -81L159 -76L160 -71L160 -66L161 -62L162 -57L165 -54L168 -50L171 -46L174 -42L176 -37L177 -33L176 -28L175 -23L174 -18L172 -14L172 -9L172 -5L173 -0ZM122 0L123 3L125 7L126 10L126 13L126 17L126 20L126 23L125 27L124 30L122 33L120 36L118 38L115 41L113 43L111 46L108 48L106 51L104 53L102 55L100 58L99 61L98 64L97 67L96 70L95 73L94 76L93 80L92 83L91 86L89 89L88 92L85 95L83 97L81 99L78 101L75 103L71 104L68 105L64 105L61 106L58 106L54 106L51 107L48 107L45 108L42 108L39 109L36 111L33 112L30 114L28 116L25 118L22 119L19 121L16 123L13 125L10 126L7 127L3 128L0 128L-3 128L-7 127L-10 126L-13 125L-16 123L-19 121L-22 119L-25 118L-28 116L-30 114L-33 112L-36 111L-39 109L-42 108L-45 108L-48 107L-51 107L-54 106L-58 106L-61 106L-64 105L-68 105L-71 104L-75 103L-78 101L-81 99L-83 97L-85 95L-88 92L-89 89L-91 86L-92 83L-93 80L-94 76L-95 73L-96 70L-97 67L-98 64L-99 61L-100 58L-102 55L-104 53L-106 51L-108 48L-111 46L-113 43L-115 41L-118 38L-120 36L-122 33L-124 30L-125 27L-126 23L-126 20L-126 17L-126 13L-126 10L-125 7L-123 3L-122 0L-121 -3L-119 -6L-118 -9L-117 -12L-115 -15L-115 -18L-114 -21L-114 -24L-114 -27L-114 -30L-114 -34L-114 -37L-115 -41L-115 -44L-115 -48L-115 -51L-114 -54L-113 -58L-112 -61L-111 -64L-109 -67L-107 -69L-104 -72L-102 -74L-99 -76L-96 -77L-92 -79L-89 -80L-86 -82L-83 -83L-80 -85L-78 -86L-75 -88L-73 -90L-71 -92L-69 -95L-67 -97L-65 -100L-63 -103L-61 -106L-59 -108L-57 -111L-54 -114L-52 -116L-49 -118L-46 -119L-43 -121L-39 -121L-36 -122L-33 -122L-29 -122L-26 -121L-22 -120L-19 -120L-16 -119L-12 -118L-9 -117L-6 -116L-3 -116L-0 -116L3 -116L6 -116L9 -117L12 -118L16 -119L19 -120L22 -120L26 -121L29 -122L33 -122L36 -122L39 -121L43 -121L46 -119L49 -118L52 -116L54 -114L57 -111L59 -108L61 -106L63 -103L65 -100L67 -97L69 -95L71 -92L73 -90L75 -88L78 -86L80 -85L83 -83L86 -82L89 -80L92 -79L96 -77L99 -76L102 -74L104 -72L107 -69L109 -67L111 -64L112 -61L113 -58L114 -54L115 -51L115 -48L115 -44L115 -41L114 -37L114 -34L114 -30L114 -27L114 -24L114 -21L115 -18L115 -15L117 -12L118 -9L119 -6L121 -3L122 -0ZM126 0L127 3L127 7L128 10L127 13L127 17L126 20L124 23L122 26L120 29L118 32L116 34L114 37L112 40L110 42L108 45L106 47L105 50L103 53L102 56L102 59L101 62L100 65L100 69L99 72L98 75L97 79L96 82L94 85L93 88L90 90L88 93L85 95L82 96L79 98L76 99L73 100L69 101L66 101L62 102L59 102L56 103L53 104L50 105L47 106L44 107L42 109L39 111L37 113L34 115L31 117L29 119L26 122L23 123L20 125L17 126L13 127L10 128L7 128L3 127L0 127L-3 126L-7 124L-10 123L-13 121L-16 119L-19 117L-21 116L-24 114L-27 113L-30 112L-33 111L-36 111L-39 110L-42 110L-46 110L-49 110L-52 110L-56 110L-59 110L-63 109L-66 108L-69 107L-72 105L-75 104L-78 101L-80 99L-82 96L-84 93L-85 90L-87 87L-88 83L-89 80L-90 77L-91 74L-93 71L-94 68L-96 66L-97 63L-99 61L-102 59L-104 57L-107 54L-109 52L-112 50L-114 47L-117 45L-119 42L-121 39L-122 36L-124 33L-124 30L-125 27L-125 23L-124 20L-124 16L-123 13L-122 10L-120 6L-119 3L-118 0L-117 -3L-116 -6L-116 -9L-115 -12L-115 -15L-115 -18L-116 -21L-116 -25L-117 -28L-117 -31L-118 -35L-118 -38L-118 -42L-118 -45L-118 -49L-117 -52L-116 -55L-114 -58L-112 -61L-110 -63L-107 -66L-104 -68L-101 -70L-98 -71L-95 -73L-92 -75L-90 -77L-87 -78L-84 -80L-82 -82L-80 -84L-78 -87L-76 -89L-74 -92L-73 -95L-71 -98L-69 -101L-67 -103L-65 -106L-63 -109L-61 -111L-58 -114L-55 -115L-52 -117L-49 -118L-46 -119L-42 -119L-39 -119L-35 -119L-32 -118L-28 -118L-25 -117L-22 -117L-18 -116L-15 -116L-12 -116L-9 -116L-6 -116L-3 -117L-0 -117L3 -118L6 -119L9 -121L13 -122L16 -123L20 -124L23 -124L26 -124L30 -124L33 -124L36 -123L39 -121L42 -120L45 -118L48 -115L50 -113L53 -110L55 -108L57 -105L59 -102L61 -100L63 -98L66 -96L68 -94L71 -92L74 -91L76 -90L80 -88L83 -87L86 -86L89 -85L92 -83L95 -81L98 -80L101 -78L103 -75L105 -72L107 -70L109 -67L110 -63L110 -60L111 -56L111 -53L111 -49L111 -46L111 -43L111 -39L111 -36L112 -33L112 -30L113 -27L114 -24L115 -21L117 -18L118 -16L120 -13L122 -10L123 -6L125 -3L126 -0ZM128 0L128 3L128 7L127 10L126 13L124 16L122 19L121 22L119 25L116 28L115 31L113 33L111 36L110 39L108 42L107 44L107 47L106 51L105 54L105 57L105 60L104 64L104 67L103 71L102 74L101 77L99 80L97 83L95 86L93 88L90 90L87 91L84 93L80 94L77 95L73 96L70 97L67 97L64 98L61 99L58 101L55 102L53 104L50 105L48 108L45 110L43 112L41 114L38 117L35 119L32 121L30 123L26 125L23 126L20 126L17 127L13 127L10 126L7 125L3 124L0 123L-3 122L-6 120L-9 119L-12 117L-15 116L-18 115L-21 114L-24 114L-27 113L-30 113L-34 113L-37 113L-40 114L-44 114L-47 114L-51 114L-54 114L-58 113L-61 112L-64 111L-67 109L-70 107L-72 105L-74 102L-76 99L-78 96L-80 93L-81 90L-82 87L-84 84L-85 81L-87 78L-88 75L-90 73L-92 71L-94 69L-97 66L-99 64L-102 62L-105 60L-108 58L-110 56L-113 54L-115 51L-117 49L-119 46L-121 43L-122 40L-122 36L-123 33L-122 29L-122 26L-121 23L-121 19L-120 16L-119 12L-118 9L-117 6L-116 3L-116 0L-116 -3L-116 -6L-116 -9L-117 -12L-118 -16L-119 -19L-119 -22L-120 -26L-121 -29L-121 -32L-121 -36L-121 -39L-120 -43L-119 -46L-118 -49L-116 -52L-114 -55L-112 -57L-109 -59L-107 -62L-104 -64L-101 -65L-98 -67L-95 -69L-93 -71L-90 -73L-88 -75L-86 -78L-84 -80L-83 -83L-81 -86L-80 -89L-78 -92L-77 -95L-75 -98L-73 -101L-71 -104L-69 -106L-67 -109L-64 -111L-61 -112L-58 -114L-55 -115L-51 -115L-48 -116L-44 -116L-41 -116L-37 -115L-34 -115L-31 -115L-27 -114L-24 -114L-21 -114L-18 -115L-15 -115L-12 -116L-9 -117L-6 -118L-3 -120L-0 -121L3 -122L6 -124L10 -125L13 -125L17 -126L20 -126L23 -126L27 -125L30 -124L33 -123L36 -121L39 -119L41 -116L44 -114L46 -112L49 -109L51 -107L53 -104L56 -102L58 -101L61 -99L63 -98L66 -96L69 -95L72 -94L76 -93L79 -92L82 -91L85 -90L89 -89L92 -87L95 -85L97 -83L99 -81L101 -78L103 -75L104 -72L105 -68L106 -65L107 -62L107 -58L107 -55L107 -51L108 -48L108 -45L109 -42L109 -39L110 -36L112 -33L113 -30L115 -28L117 -25L118 -22L120 -19L122 -16L124 -13L125 -10L127 -7L127 -3L128 -0ZM127 0L126 3L125 7L124 10L122 13L120 16L118 19L117 22L115 24L114 27L112 30L111 33L110 36L110 39L110 42L109 45L109 49L109 52L109 56L109 59L108 62L108 66L107 69L105 72L104 75L102 78L99 80L97 82L94 84L91 86L87 87L84 89L81 90L78 91L74 92L71 93L68 94L66 96L63 97L61 99L58 101L56 103L54 106L52 108L49 111L47 113L44 116L42 118L39 120L36 122L33 123L30 124L27 125L23 125L20 125L16 125L13 124L10 123L6 122L3 120L0 119L-3 118L-6 117L-9 116L-12 115L-15 115L-18 115L-21 115L-25 115L-28 116L-31 116L-35 117L-38 117L-42 117L-45 117L-49 117L-52 116L-55 115L-58 114L-61 112L-64 110L-66 108L-68 105L-70 102L-72 99L-74 96L-75 93L-77 90L-79 87L-80 85L-82 82L-84 80L-86 78L-89 76L-91 74L-94 72L-97 70L-100 68L-103 67L-105 65L-108 62L-111 60L-113 58L-115 55L-117 52L-118 49L-119 46L-120 42L-120 39L-120 35L-119 32L-119 29L-118 25L-117 22L-117 18L-116 15L-116 12L-116 9L-116 6L-116 3L-117 0L-118 -3L-119 -6L-120 -9L-121 -13L-122 -16L-123 -19L-123 -23L-124 -26L-124 -30L-123 -33L-123 -36L-122 -40L-120 -43L-118 -45L-116 -48L-114 -51L-111 -53L-108 -55L-106 -57L-103 -60L-101 -62L-98 -64L-96 -66L-94 -68L-92 -71L-90 -73L-89 -76L-88 -79L-86 -82L-85 -85L-84 -88L-82 -92L-81 -95L-79 -98L-77 -101L-75 -103L-72 -105L-70 -107L-67 -109L-64 -110L-60 -111L-57 -112L-53 -112L-50 -112L-46 -112L-43 -112L-40 -112L-36 -112L-33 -112L-30 -112L-27 -113L-24 -114L-21 -115L-18 -116L-15 -117L-12 -119L-9 -121L-6 -122L-3 -124L-0 -125L3 -126L7 -127L10 -127L13 -127L17 -127L20 -126L23 -125L26 -123L29 -121L32 -119L35 -117L37 -115L40 -113L42 -110L45 -108L47 -106L50 -105L53 -103L55 -102L58 -101L61 -100L65 -100L68 -99L71 -98L75 -97L78 -96L81 -95L85 -94L88 -92L90 -90L93 -88L95 -86L97 -83L98 -80L100 -76L101 -73L101 -70L102 -66L103 -63L103 -60L104 -56L104 -53L105 -50L106 -47L107 -44L109 -42L110 -39L112 -36L114 -34L116 -31L118 -28L121 -26L122 -23L124 -20L126 -17L127 -13L128 -10L128 -7L128 -3L127 -0ZM124 0L123 3L121 6L120 9L118 12L117 15L115 18L114 21L113 24L113 27L113 30L112 33L113 37L113 40L113 43L113 47L113 50L113 54L112 57L112 61L111 64L109 67L107 70L105 72L103 75L100 77L97 79L94 80L91 82L88 83L84 84L81 86L78 87L76 89L73 90L71 92L68 94L66 96L64 99L62 101L60 104L58 107L56 109L53 112L51 115L48 117L46 119L43 120L40 122L36 123L33 123L30 123L26 123L23 122L19 122L16 121L13 120L9 119L6 118L3 117L0 116L-3 116L-6 116L-9 116L-12 116L-15 117L-19 118L-22 118L-25 119L-29 120L-32 120L-36 121L-39 121L-43 120L-46 119L-49 118L-52 117L-55 115L-57 113L-60 110L-62 107L-64 105L-66 102L-68 99L-70 96L-72 93L-73 91L-75 88L-78 86L-80 84L-82 82L-85 81L-88 79L-91 78L-94 76L-97 74L-100 73L-103 71L-106 69L-108 66L-111 64L-112 61L-114 58L-115 55L-116 52L-116 48L-117 45L-117 41L-116 38L-116 34L-115 31L-115 28L-115 24L-115 21L-115 18L-115 15L-116 12L-116 9L-117 6L-119 3L-120 0L-121 -3L-123 -6L-124 -10L-125 -13L-125 -17L-126 -20L-126 -23L-125 -27L-124 -30L-123 -33L-121 -36L-120 -39L-117 -42L-115 -44L-112 -47L-110 -49L-107 -51L-105 -54L-103 -56L-101 -58L-99 -61L-97 -63L-96 -66L-95 -69L-94 -72L-93 -75L-92 -78L-91 -81L-89 -85L-88 -88L-87 -91L-85 -94L-83 -97L-80 -99L-78 -102L-75 -103L-72 -105L-69 -106L-65 -107L-62 -107L-59 -108L-55 -108L-52 -108L-48 -108L-45 -109L-42 -109L-39 -110L-36 -110L-33 -111L-30 -113L-27 -114L-25 -116L-22 -118L-19 -119L-16 -121L-13 -123L-10 -125L-7 -126L-3 -127L-0 -128L3 -128L7 -128L10 -127L13 -126L16 -125L20 -123L23 -122L25 -120L28 -117L31 -115L34 -113L36 -112L39 -110L42 -108L44 -107L47 -106L50 -105L53 -105L57 -104L60 -104L63 -103L67 -103L70 -102L74 -101L77 -100L80 -99L83 -97L86 -95L88 -93L90 -90L92 -87L93 -84L95 -81L96 -77L97 -74L97 -71L98 -67L99 -64L100 -61L101 -58L102 -55L103 -53L105 -50L107 -48L109 -45L111 -43L113 -40L116 -38L118 -35L120 -32L122 -29L124 -26L125 -23L126 -20L127 -17L127 -13L127 -10L126 -7L125 -3L124 -0ZM120 0L119 3L117 6L116 9L116 12L115 15L115 18L115 21L115 24L115 28L115 31L116 34L116 38L117 41L117 45L116 48L116 52L115 55L114 58L112 61L111 64L108 66L106 69L103 71L100 73L97 74L94 76L91 78L88 79L85 81L82 82L80 84L78 86L75 88L73 91L72 93L70 96L68 99L66 102L64 105L62 107L60 110L57 113L55 115L52 117L49 118L46 119L43 120L39 121L36 121L32 120L29 120L25 119L22 118L19 118L15 117L12 116L9 116L6 116L3 116L0 116L-3 117L-6 118L-9 119L-13 120L-16 121L-19 122L-23 122L-26 123L-30 123L-33 123L-36 123L-40 122L-43 120L-46 119L-48 117L-51 115L-53 112L-56 109L-58 107L-60 104L-62 101L-64 99L-66 96L-68 94L-71 92L-73 90L-76 89L-78 87L-81 86L-84 84L-88 83L-91 82L-94 80L-97 79L-100 77L-103 75L-105 72L-107 70L-109 67L-111 64L-112 61L-112 57L-113 54L-113 50L-113 47L-113 43L-113 40L-113 37L-112 33L-113 30L-113 27L-113 24L-114 21L-115 18L-117 15L-118 12L-120 9L-121 6L-123 3L-124 0L-125 -3L-126 -7L-127 -10L-127 -13L-127 -17L-126 -20L-125 -23L-124 -26L-122 -29L-120 -32L-118 -35L-116 -38L-113 -40L-111 -43L-109 -45L-107 -48L-105 -50L-103 -53L-102 -55L-101 -58L-100 -61L-99 -64L-98 -67L-97 -71L-97 -74L-96 -77L-95 -81L-93 -84L-92 -87L-90 -90L-88 -93L-86 -95L-83 -97L-80 -99L-77 -100L-74 -101L-70 -102L-67 -103L-63 -103L-60 -104L-57 -104L-53 -105L-50 -105L-47 -106L-44 -107L-42 -108L-39 -110L-36 -112L-34 -113L-31 -115L-28 -117L-25 -120L-23 -122L-20 -123L-16 -125L-13 -126L-10 -127L-7 -128L-3 -128L-0 -128L3 -127L7 -126L10 -125L13 -123L16 -121L19 -119L22 -118L25 -116L27 -114L30 -113L33 -111L36 -110L39 -110L42 -109L45 -109L48 -108L52 -108L55 -108L59 -108L62 -107L65 -107L69 -106L72 -105L75 -103L78 -102L80 -99L83 -97L85 -94L87 -91L88 -88L89 -85L91 -81L92 -78L93 -75L94 -72L95 -69L96 -66L97 -63L99 -61L101 -58L103 -56L105 -54L107 -51L110 -49L112 -47L115 -44L117 -42L120 -39L121 -36L123 -33L124 -30L125 -27L126 -23L126 -20L125 -17L125 -13L124 -10L123 -6L121 -3L120 -0ZM117 0L116 3L116 6L116 9L116 12L116 15L117 18L117 22L118 25L119 29L119 32L120 35L120 39L120 42L119 46L118 49L117 52L115 55L113 58L111 60L108 62L105 65L103 67L100 68L97 70L94 72L91 74L89 76L86 78L84 80L82 82L80 85L79 87L77 90L75 93L74 96L72 99L70 102L68 105L66 108L64 110L61 112L58 114L55 115L52 116L49 117L45 117L42 117L38 117L35 117L31 116L28 116L25 115L21 115L18 115L15 115L12 115L9 116L6 117L3 118L0 119L-3 120L-6 122L-10 123L-13 124L-16 125L-20 125L-23 125L-27 125L-30 124L-33 123L-36 122L-39 120L-42 118L-44 116L-47 113L-49 111L-52 108L-54 106L-56 103L-58 101L-61 99L-63 97L-66 96L-68 94L-71 93L-74 92L-78 91L-81 90L-84 89L-87 87L-91 86L-94 84L-97 82L-99 80L-102 78L-104 75L-105 72L-107 69L-108 66L-108 62L-109 59L-109 56L-109 52L-109 49L-109 45L-110 42L-110 39L-110 36L-111 33L-112 30L-114 27L-115 24L-117 22L-118 19L-120 16L-122 13L-124 10L-125 7L-126 3L-127 0L-128 -3L-128 -7L-128 -10L-127 -13L-126 -17L-124 -20L-122 -23L-121 -26L-118 -28L-116 -31L-114 -34L-112 -36L-110 -39L-109 -42L-107 -44L-106 -47L-105 -50L-104 -53L-104 -56L-103 -60L-103 -63L-102 -66L-101 -70L-101 -73L-100 -76L-98 -80L-97 -83L-95 -86L-93 -88L-90 -90L-88 -92L-85 -94L-81 -95L-78 -96L-75 -97L-71 -98L-68 -99L-65 -100L-61 -100L-58 -101L-55 -102L-53 -103L-50 -105L-47 -106L-45 -108L-42 -110L-40 -113L-37 -115L-35 -117L-32 -119L-29 -121L-26 -123L-23 -125L-20 -126L-17 -127L-13 -127L-10 -127L-7 -127L-3 -126L-0 -125L3 -124L6 -122L9 -121L12 -119L15 -117L18 -116L21 -115L24 -114L27 -113L30 -112L33 -112L36 -112L40 -112L43 -112L46 -112L50 -112L53 -112L57 -112L60 -111L64 -110L67 -109L70 -107L72 -105L75 -103L77 -101L79 -98L81 -95L82 -92L84 -88L85 -85L86 -82L88 -79L89 -76L90 -73L92 -71L94 -68L96 -66L98 -64L101 -62L103 -60L106 -57L108 -55L111 -53L114 -51L116 -48L118 -45L120 -43L122 -40L123 -36L123 -33L124 -30L124 -26L123 -23L123 -19L122 -16L121 -13L120 -9L119 -6L118 -3L117 -0ZM116 0L116 3L117 6L118 9L119 12L120 16L121 19L121 23L122 26L122 29L123 33L122 36L122 40L121 43L119 46L117 49L115 51L113 54L110 56L108 58L105 60L102 62L99 64L97 66L94 69L92 71L90 73L88 75L87 78L85 81L84 84L82 87L81 90L80 93L78 96L76 99L74 102L72 105L70 107L67 109L64 111L61 112L58 113L54 114L51 114L47 114L44 114L40 114L37 113L34 113L30 113L27 113L24 114L21 114L18 115L15 116L12 117L9 119L6 120L3 122L0 123L-3 124L-7 125L-10 126L-13 127L-17 127L-20 126L-23 126L-26 125L-30 123L-32 121L-35 119L-38 117L-41 114L-43 112L-45 110L-48 108L-50 105L-53 104L-55 102L-58 101L-61 99L-64 98L-67 97L-70 97L-73 96L-77 95L-80 94L-84 93L-87 91L-90 90L-93 88L-95 86L-97 83L-99 80L-101 77L-102 74L-103 71L-104 67L-104 64L-105 60L-105 57L-105 54L-106 51L-107 47L-107 44L-108 42L-110 39L-111 36L-113 33L-115 31L-116 28L-119 25L-121 22L-122 19L-124 16L-126 13L-127 10L-128 7L-128 3L-128 0L-127 -3L-127 -7L-125 -10L-124 -13L-122 -16L-120 -19L-118 -22L-117 -25L-115 -28L-113 -30L-112 -33L-110 -36L-109 -39L-109 -42L-108 -45L-108 -48L-107 -51L-107 -55L-107 -58L-107 -62L-106 -65L-105 -68L-104 -72L-103 -75L-101 -78L-99 -81L-97 -83L-95 -85L-92 -87L-89 -89L-85 -90L-82 -91L-79 -92L-76 -93L-72 -94L-69 -95L-66 -96L-63 -98L-61 -99L-58 -101L-56 -102L-53 -104L-51 -107L-49 -109L-46 -112L-44 -114L-41 -116L-39 -119L-36 -121L-33 -123L-30 -124L-27 -125L-23 -126L-20 -126L-17 -126L-13 -125L-10 -125L-6 -124L-3 -122L-0 -121L3 -120L6 -118L9 -117L12 -116L15 -115L18 -115L21 -114L24 -114L27 -114L31 -115L34 -115L37 -115L41 -116L44 -116L48 -116L51 -115L55 -115L58 -114L61 -112L64 -111L67 -109L69 -106L71 -104L73 -101L75 -98L77 -95L78 -92L80 -89L81 -86L83 -83L84 -80L86 -78L88 -75L90 -73L93 -71L95 -69L98 -67L101 -65L104 -64L107 -62L109 -59L112 -57L114 -55L116 -52L118 -49L119 -46L120 -43L121 -39L121 -36L121 -32L121 -29L120 -26L119 -22L119 -19L118 -16L117 -12L116 -9L116 -6L116 -3L116 -0ZM118 0L119 3L120 6L122 10L123 13L124 16L124 20L125 23L125 27L124 30L124 33L122 36L121 39L119 42L117 45L114 47L112 50L109 52L107 54L104 57L102 59L99 61L97 63L96 66L94 68L93 71L91 74L90 77L89 80L88 83L87 87L85 90L84 93L82 96L80 99L78 101L75 104L72 105L69 107L66 108L63 109L59 110L56 110L52 110L49 110L46 110L42 110L39 110L36 111L33 111L30 112L27 113L24 114L21 116L19 117L16 119L13 121L10 123L7 124L3 126L0 127L-3 127L-7 128L-10 128L-13 127L-17 126L-20 125L-23 123L-26 122L-29 119L-31 117L-34 115L-37 113L-39 111L-42 109L-44 107L-47 106L-50 105L-53 104L-56 103L-59 102L-62 102L-66 101L-69 101L-73 100L-76 99L-79 98L-82 96L-85 95L-88 93L-90 90L-93 88L-94 85L-96 82L-97 79L-98 75L-99 72L-100 69L-100 65L-101 62L-102 59L-102 56L-103 53L-105 50L-106 47L-108 45L-110 42L-112 40L-114 37L-116 34L-118 32L-120 29L-122 26L-124 23L-126 20L-127 17L-127 13L-128 10L-127 7L-127 3L-126 0L-125 -3L-123 -6L-122 -10L-120 -13L-118 -16L-117 -18L-115 -21L-114 -24L-113 -27L-112 -30L-112 -33L-111 -36L-111 -39L-111 -43L-111 -46L-111 -49L-111 -53L-111 -56L-110 -60L-110 -63L-109 -67L-107 -70L-105 -72L-103 -75L-101 -78L-98 -80L-95 -81L-92 -83L-89 -85L-86 -86L-83 -87L-80 -88L-76 -90L-74 -91L-71 -92L-68 -94L-66 -96L-63 -98L-61 -100L-59 -102L-57 -105L-55 -108L-53 -110L-50 -113L-48 -115L-45 -118L-42 -120L-39 -121L-36 -123L-33 -124L-30 -124L-26 -124L-23 -124L-20 -124L-16 -123L-13 -122L-9 -121L-6 -119L-3 -118L-0 -117L3 -117L6 -116L9 -116L12 -116L15 -116L18 -116L22 -117L25 -117L28 -118L32 -118L35 -119L39 -119L42 -119L46 -119L49 -118L52 -117L55 -115L58 -114L61 -111L63 -109L65 -106L67 -103L69 -101L71 -98L73 -95L74 -92L76 -89L78 -87L80 -84L82 -82L84 -80L87 -78L90 -77L92 -75L95 -73L98 -71L101 -70L104 -68L107 -66L110 -63L112 -61L114 -58L116 -55L117 -52L118 -49L118 -45L118 -42L118 -38L118 -35L117 -31L117 -28L116 -25L116 -21L115 -18L115 -15L115 -12L116 -9L116 -6L117 -3L118 -0Z" fill="none" stroke="currentColor" stroke-width=".9"/></symbol></svg>'
    put('doradztwo', sym + '<div class="n-tabs" role="tablist" aria-label="Działy usług" id="n-tabs">' + ''.join(tabs) + '<span class="n-pill" aria-hidden="true"></span></div>' + '<div class="n-panels" id="n-panels">' + ''.join(panels) + '</div>')
    put('local', ' · '.join(f'<a href="{url(p["slug"])}">{e(p["menu"])}</a>' for p in P_LOK))
    open(f, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    counts = {}
    for p in P_DOR: counts[p['slug']] = build_page(p, 'Doradztwo podatkowe')
    for p in P_KSI: counts[p['slug']] = build_page(p, 'Księgowość')
    for p in P_LOK: counts[p['slug']] = build_page(p, 'Doradca podatkowy w okolicy')
    build_team_page()
    build_pricing_page()
    n = build_sitemap()
    if '--no-index' not in sys.argv: update_index()
    for k, v in counts.items(): print(f'{v:5d} słów  {k}')
    print(f'sitemap: {n} adresów')
