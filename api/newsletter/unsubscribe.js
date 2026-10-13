// Wypisanie z newslettera (wycofanie zgody). Wypisanie następuje po kliknięciu przycisku (POST),
// żeby skanery linków w programach pocztowych nie wypisywały subskrybentów przypadkiem.
import { readBody, readToken, nowPl, clientIp, sendMail, emailLayout, sendPage, P, h, OWNER_EMAIL } from '../../lib/newsletter.js';

export default async function handler(req, res) {
  const body = req.method === 'POST' ? await readBody(req) : {};
  const token = String(req.query?.t || body.t || '');
  const data = readToken(token);

  if (!data || data.a !== 'unsub' || !data.e) {
    return sendPage(res, 'Nieprawidłowy link',
      `<p>Nie udało się rozpoznać linku. Aby wypisać się z newslettera, napisz na <a href="mailto:${h(OWNER_EMAIL)}">${h(OWNER_EMAIL)}</a>.</p>`, 400);
  }
  const email = data.e;

  if (req.method !== 'POST') {
    return sendPage(res, 'Wypisanie z newslettera',
      `<p>Czy na pewno chcesz wypisać adres <strong>${h(email)}</strong> z newslettera podatkowego RKDP?</p>`
      + `<form method="post"><input type="hidden" name="t" value="${h(token)}"><button type="submit" class="dark">Tak, wypisz mnie</button></form>`);
  }

  try {
    await sendMail({
      to: OWNER_EMAIL,
      subject: `Newsletter: rezygnacja – ${email}`,
      html: emailLayout('Rezygnacja z newslettera',
        P(`Adres <strong>${h(email)}</strong> wycofał zgodę i wypisał się z newslettera (${nowPl()}, IP ${h(clientIp(req))}). Usuń go z listy wysyłkowej.`)),
      text: `Adres ${email} wypisał się z newslettera (${nowPl()}). Usuń go z listy wysyłkowej.`,
      replyTo: email,
    });
  } catch (err) {
    console.error('newsletter unsubscribe mail error', err);
    return sendPage(res, 'Coś poszło nie tak',
      `<p>Nie udało się zapisać rezygnacji. Napisz proszę na <a href="mailto:${h(OWNER_EMAIL)}">${h(OWNER_EMAIL)}</a> – wypiszemy Cię ręcznie.</p>`, 500);
  }

  return sendPage(res, 'Wypisano z newslettera',
    `<p>Adres <strong>${h(email)}</strong> został wypisany. Nie będziemy wysyłać już newslettera. Otrzymany wcześniej kod rabatowy pozostaje ważny.</p>`);
}
