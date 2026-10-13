// Krok 1: zapis – wysyła link potwierdzający (double opt-in). Zgoda liczy się dopiero po potwierdzeniu.
import {
  readBody, makeToken, sendMail, emailLayout, P, button, h,
  SITE_URL, OWNER_EMAIL, CONFIRM_TTL_HOURS, DISCOUNT_PERCENT,
} from '../../lib/newsletter.js';

function respond(req, res, ok, message) {
  if (String(req.headers.accept || '').includes('application/json')) {
    res.statusCode = ok ? 200 : 400;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(JSON.stringify({ ok, message }));
  } else {
    res.statusCode = 303;
    res.setHeader('Location', `/?newsletter=${ok ? 'wyslano' : 'blad'}#newsletter`);
    res.end();
  }
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return respond(req, res, false, 'Nieprawidłowe żądanie.');
  const body = await readBody(req);

  // Ochrona przed botami: ukryte pole i minimalny czas wypełniania.
  if (body.website) return respond(req, res, true, 'Dziękujemy!');
  const started = Number(body.ts || 0);
  if (started > 0 && Date.now() - started < 2500) return respond(req, res, false, 'Spróbuj ponownie za chwilę.');

  const email = String(body.email || '').trim().toLowerCase();
  const name = String(body.name || '').replace(/<[^>]*>/g, '').replace(/[\r\n]+/g, ' ').trim().slice(0, 60);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) {
    return respond(req, res, false, 'Podaj poprawny adres e-mail.');
  }
  if (!body.consent_newsletter || !body.consent_terms) {
    return respond(req, res, false, 'Aby się zapisać, zaznacz obie wymagane zgody.');
  }

  const token = makeToken({ e: email, n: name, t: Math.floor(Date.now() / 1000), a: 'confirm' });
  const link = `${SITE_URL}/api/newsletter/confirm?t=${encodeURIComponent(token)}`;
  const hi = name ? `Dzień dobry ${name},` : 'Dzień dobry,';

  try {
    await sendMail({
      to: email,
      subject: 'Potwierdź zapis do newslettera RKDP',
      html: emailLayout('Potwierdź zapis do newslettera',
        P(h(hi))
        + P(`dziękujemy za zapis do newslettera podatkowego RKDP. Kliknij przycisk poniżej, aby potwierdzić adres e-mail. Po potwierdzeniu otrzymasz kod rabatowy <strong>${DISCOUNT_PERCENT}%</strong> na kolejną usługę podatkową.`)
        + button(link, 'Potwierdzam zapis')
        + `<p style="font-size:13px;line-height:1.6;color:#6A6157;margin:0">Link jest ważny przez ${CONFIRM_TTL_HOURS} godziny. Jeśli to nie Ty zapisałeś/-aś się do newslettera, zignoruj tę wiadomość – bez potwierdzenia nie będziemy wysyłać żadnych wiadomości.</p>`),
      text: `${hi}\n\ndziękujemy za zapis do newslettera podatkowego RKDP. Aby potwierdzić adres e-mail i otrzymać kod rabatowy ${DISCOUNT_PERCENT}%, otwórz link:\n${link}\n\nLink jest ważny przez ${CONFIRM_TTL_HOURS} godziny. Jeśli to nie Ty, zignoruj tę wiadomość.\n\nRKDP spółka doradztwa podatkowego sp. z o.o.`,
    });
  } catch (err) {
    console.error('newsletter subscribe mail error', err);
    return respond(req, res, false, `Nie udało się wysłać wiadomości. Spróbuj ponownie lub napisz na ${OWNER_EMAIL}.`);
  }
  return respond(req, res, true, 'Sprawdź skrzynkę – wysłaliśmy link potwierdzający. Kod rabatowy otrzymasz po kliknięciu linku.');
}
