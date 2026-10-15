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
      <nav aria-label="Informacje"><span class="k">Informacje</span><a href="/zespol/">Zespół</a><a href="/cennik/">Cennik</a><a href="/polityka-prywatnosci.html">RODO (Polityka prywatności)</a><a href="/aml.html">AML</a><a href="/dokumenty/procedura-sygnalisci-rkdp.pdf" target="_blank" rel="noopener">Sygnaliści</a><a href="/dokumenty/regulamin-umowy-do-31-12-2025.pdf" target="_blank" rel="noopener">Regulamin (umowy do 31.12.2025)</a></nav>
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
        {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "/#marcin-otreba", "name": "Marcin Otręba", "jobTitle": "Doradca podatkowy, Partner Zarządzający", "image": SITE + "/img/marcin-otreba.jpg", "sameAs": ["https://kidp.pl/doradca/14609"]},
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
        offer("Konsultacja wstępna (do 20 minut)", 0), offer("Konsultacja podatkowa", 400, "godzina"),
        offer("Abonament Doradca Podatkowy", 369, "miesiąc"), offer("Abonament Księgowość JDG + Doradca Podatkowy", 419, "miesiąc"), offer("Abonament Księgowość + Doradca Podatkowy", 790, "miesiąc")]}]
    body = head('Cennik – doradca podatkowy i księgowość Wrocław | RKDP', 'Cennik RKDP: pierwsza konsultacja do 20 minut bezpłatnie, konsultacja podatkowa od 400 zł/h, abonament doradcy od 369 zł, księgowość JDG z doradcą od 419 zł, księgowość z doradcą od 790 zł miesięcznie.', path, extra_ld=ld)
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
    tile = lambda i, p: f'<a class="spec" href="{url(p["slug"])}"><span class="num">{i:02d}</span><h3>{e(p["menu"])}</h3><p>{e(p["tile"])}</p><em class="spec-more">Dowiedz się więcej →</em></a>'
    home = ['doradztwo-podatkowe', 'kontrola-podatkowa', 'czynnosci-sprawdzajace', 'interpretacja-indywidualna', 'wyplata-pieniedzy-ze-spolki']
    put('doradztwo', ''.join(tile(i + 1, BY_SLUG[sl]) for i, sl in enumerate(home)))
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
