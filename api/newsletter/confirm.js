// Krok 2: potwierdzenie (double opt-in).
// Link z maila otwiera stronę z przyciskiem; zgoda zostaje zapisana dopiero po kliknięciu (POST).
// Dzięki temu automatyczne skanery linków w programach pocztowych nie potwierdzają zapisu za klienta.
import {
  readBody, readToken, makeToken, discountCode, validUntil, nowPl, clientIp, userAgent,
  sendMail, emailLayout, sendPage, P, button, h,
  SITE_URL, OWNER_EMAIL, CONFIRM_TTL_HOURS, DISCOUNT_PERCENT,
  CONSENT_VERSION, CONSENT_NEWSLETTER, CONSENT_TERMS,
} from '../../lib/newsletter.js';

export default async function handler(req, res) {
  const body = req.method === 'POST' ? await readBody(req) : {};
  const token = String(req.query?.t || body.t || '');
  const data = readToken(token);

  if (!data || data.a !== 'confirm' || !data.e) {
    return sendPage(res, 'Nieprawidłowy link', '<p>Ten link potwierdzający jest nieprawidłowy. Zapisz się ponownie na stronie.</p>', 400);
  }
  if (Date.now() / 1000 - Number(data.t) > CONFIRM_TTL_HOURS * 3600) {
    return sendPage(res, 'Link wygasł', '<p>Link potwierdzający wygasł. Zapisz się ponownie na stronie – wyślemy nowy.</p>', 410);
  }

  const email = data.e;
  const name = data.n || '';

  if (req.method !== 'POST') {
    return sendPage(res, 'Potwierdź zapis',
      `<p>Potwierdź zapis adresu <strong>${h(email)}</strong> do newslettera podatkowego RKDP. Po potwierdzeniu od razu zobaczysz swój kod rabatowy ${DISCOUNT_PERCENT}%.</p>`
      + `<form method="post"><input type="hidden" name="t" value="${h(token)}"><button type="submit">Potwierdzam zapis i odbieram rabat</button></form>`);
  }

  const code = discountCode(email);
  const until = validUntil();
  const unsub = `${SITE_URL}/api/newsletter/unsubscribe?t=${encodeURIComponent(makeToken({ e: email, a: 'unsub' }))}`;
  const hi = name ? `Dzień dobry ${name},` : 'Dzień dobry,';

  try {
    // Mail do subskrybenta z kodem.
    await sendMail({
      to: email,
      subject: `Twój kod rabatowy ${DISCOUNT_PERCENT}% – RKDP`,
      html: emailLayout(`Twój kod rabatowy ${DISCOUNT_PERCENT}%`,
        P(h(hi))
        + P('dziękujemy za potwierdzenie zapisu do newslettera podatkowego RKDP. Oto Twój kod rabatowy na kolejną usługę podatkową:')
        + `<p style="margin:20px 0"><span style="display:inline-block;font-size:24px;font-weight:bold;letter-spacing:2px;color:#7A5A37;border:2px dashed #7A5A37;border-radius:12px;padding:12px 20px">${h(code)}</span></p>`
        + P(`Kod daje <strong>${DISCOUNT_PERCENT}% rabatu</strong> na wynagrodzenie za jedną kolejną usługę podatkową. Podaj go przy zleceniu usługi. Kod jest ważny do <strong>${until}</strong>. Szczegóły w <a href="${h(SITE_URL)}/regulamin-newslettera.html" style="color:#7A5A37">Regulaminie newslettera i promocji</a>.`)
        + button(`${SITE_URL}/#termin`, 'Umów konsultację')
        + `<p style="font-size:12px;line-height:1.6;color:#6A6157;margin:0">Nie chcesz otrzymywać newslettera? <a href="${h(unsub)}" style="color:#6A6157">Wypisz się</a> w dowolnej chwili.</p>`),
      text: `${hi}\n\ndziękujemy za potwierdzenie zapisu do newslettera podatkowego RKDP.\n\nTwój kod rabatowy: ${code}\n${DISCOUNT_PERCENT}% rabatu na wynagrodzenie za jedną kolejną usługę podatkową, ważny do ${until}.\nRegulamin: ${SITE_URL}/regulamin-newslettera.html\n\nWypisanie z newslettera: ${unsub}\n\nRKDP spółka doradztwa podatkowego sp. z o.o.`,
    });

    // Powiadomienie do kancelarii – dowód wyrażenia zgody (rozliczalność, art. 7 ust. 1 RODO).
    const rows = [
      ['E-mail', email],
      ['Imię', name || '—'],
      ['Data i godzina potwierdzenia', nowPl()],
      ['Adres IP', clientIp(req)],
      ['Przeglądarka', userAgent(req)],
      ['Sposób wyrażenia zgody', 'formularz na rkdp.pl + potwierdzenie linkiem z e-maila i przyciskiem na stronie (double opt-in)'],
      ['Wersja treści zgód', CONSENT_VERSION],
      ['Zgoda 1 (newsletter / informacje handlowe)', CONSENT_NEWSLETTER],
      ['Zgoda 2 (regulamin i polityka prywatności)', CONSENT_TERMS],
      ['Przyznany kod rabatowy', `${code} (${DISCOUNT_PERCENT}%, ważny do ${until})`],
    ];
    const tbl = '<table cellpadding="0" cellspacing="0" style="width:100%;font-size:14px;border-collapse:collapse">'
      + rows.map(([k, v]) => `<tr><td style="padding:8px 12px 8px 0;border-bottom:1px solid #E3D9CA;color:#6A6157;vertical-align:top;width:38%">${h(k)}</td><td style="padding:8px 0;border-bottom:1px solid #E3D9CA;color:#1D1A16">${h(v)}</td></tr>`).join('')
      + '</table>';
    await sendMail({
      to: OWNER_EMAIL,
      subject: `Newsletter: nowa zgoda – ${email}`,
      html: emailLayout('Nowy subskrybent newslettera', P('Subskrybent potwierdził zapis. Zachowaj tę wiadomość jako dowód wyrażenia zgody.') + tbl),
      text: 'Nowy subskrybent newslettera (zgoda potwierdzona)\n\n' + rows.map(([k, v]) => `${k}: ${v}`).join('\n'),
      replyTo: email,
    });
  } catch (err) {
    console.error('newsletter confirm mail error', err);
    return sendPage(res, 'Coś poszło nie tak', `<p>Nie udało się zakończyć zapisu. Spróbuj ponownie za chwilę lub napisz na <a href="mailto:${h(OWNER_EMAIL)}">${h(OWNER_EMAIL)}</a>.</p>`, 500);
  }

  return sendPage(res, 'Zapis potwierdzony',
    '<p>Dziękujemy! Twój adres został potwierdzony. Oto Twój kod rabatowy na kolejną usługę podatkową – wysłaliśmy go również e-mailem:</p>'
    + `<div class="code">${h(code)}</div>`
    + `<p>${DISCOUNT_PERCENT}% rabatu na wynagrodzenie za jedną kolejną usługę podatkową. Kod podaj przy zleceniu usługi. Szczegóły w <a href="/regulamin-newslettera.html">Regulaminie newslettera i promocji</a>.</p>`);
}
