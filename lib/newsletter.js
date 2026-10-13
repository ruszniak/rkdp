// Wspólna logika newslettera RKDP (funkcje serverless na Vercelu).
// Konfiguracja przez zmienne środowiskowe w Vercel → Settings → Environment Variables.
import crypto from 'node:crypto';
import nodemailer from 'nodemailer';

export const OWNER_EMAIL = process.env.NEWSLETTER_OWNER_EMAIL || 'kancelaria@rkdp.pl';
export const FROM_EMAIL = process.env.NEWSLETTER_FROM_EMAIL || 'kancelaria@rkdp.pl';
export const FROM_NAME = 'RKDP – Kancelaria Ruszniak';
export const SITE_URL = (process.env.SITE_URL || 'https://rkdp.pl').replace(/\/$/, '');
export const CONFIRM_TTL_HOURS = 72;
export const DISCOUNT_PERCENT = 15;
export const DISCOUNT_VALID_MONTHS = 12;

// Wersja i treść zgód – muszą być identyczne jak w formularzu w index.html.
export const CONSENT_VERSION = '2026-09-30';
export const CONSENT_NEWSLETTER = 'Wyrażam zgodę na przesyłanie mi przez RKDP spółka doradztwa podatkowego sp. z o.o. z siedzibą w Ozorzycach newslettera podatkowego zawierającego informacje handlowe, na podany adres e-mail (art. 398 ustawy – Prawo komunikacji elektronicznej), oraz na przetwarzanie w tym celu moich danych osobowych (art. 6 ust. 1 lit. a RODO). Zgodę mogę wycofać w każdej chwili.';
export const CONSENT_TERMS = 'Zapoznałem/-am się z Regulaminem newslettera i promocji oraz Polityką prywatności i akceptuję ich treść.';

function secret() {
  const s = process.env.NEWSLETTER_SECRET;
  if (!s || s.length < 32) throw new Error('Brak zmiennej NEWSLETTER_SECRET (min. 32 znaki).');
  return s;
}

const b64url = (buf) => Buffer.from(buf).toString('base64url');

export function makeToken(data) {
  const payload = b64url(JSON.stringify(data));
  const sig = crypto.createHmac('sha256', secret()).update(payload).digest('base64url');
  return `${payload}.${sig}`;
}

export function readToken(token) {
  if (typeof token !== 'string') return null;
  const [payload, sig] = token.split('.');
  if (!payload || !sig) return null;
  const expected = crypto.createHmac('sha256', secret()).update(payload).digest('base64url');
  const a = Buffer.from(sig), b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  try { return JSON.parse(Buffer.from(payload, 'base64url').toString('utf8')); } catch { return null; }
}

/** Indywidualny kod rabatowy – zawsze ten sam dla danego adresu. */
export function discountCode(email) {
  const h = crypto.createHmac('sha256', secret() + '|code').update(email.toLowerCase()).digest('hex').slice(0, 8).toUpperCase();
  return `RKDP${DISCOUNT_PERCENT}-${h}`;
}

export const nowPl = () => new Date().toLocaleString('pl-PL', { timeZone: 'Europe/Warsaw' });
export function validUntil() {
  const d = new Date(); d.setMonth(d.getMonth() + DISCOUNT_VALID_MONTHS);
  return d.toLocaleDateString('pl-PL', { timeZone: 'Europe/Warsaw' });
}

export const clientIp = (req) => String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || req.socket?.remoteAddress || '';
export const userAgent = (req) => String(req.headers['user-agent'] || '').slice(0, 300);

export const h = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

let transporter;
function getTransporter() {
  if (transporter) return transporter;
  if (process.env.NEWSLETTER_DEV === '1') {
    transporter = nodemailer.createTransport({ jsonTransport: true });
  } else {
    const port = Number(process.env.SMTP_PORT || 465);
    transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port,
      secure: port === 465,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
    });
  }
  return transporter;
}

export async function sendMail({ to, subject, html, text, replyTo }) {
  const info = await getTransporter().sendMail({
    from: { name: FROM_NAME, address: FROM_EMAIL },
    to, subject, html, text,
    replyTo: replyTo || OWNER_EMAIL,
  });
  if (process.env.NEWSLETTER_DEV === '1') (globalThis.__sentMails ||= []).push(JSON.parse(info.message));
  return info;
}

/** Szablon maila w kolorach RKDP. */
export function emailLayout(title, inner) {
  return '<!doctype html><html lang="pl"><body style="margin:0;background:#F8F5F0;font-family:Arial,Helvetica,sans-serif;color:#1D1A16">'
    + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F8F5F0;padding:32px 12px"><tr><td align="center">'
    + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border:1px solid #E3D9CA;border-radius:16px">'
    + `<tr><td style="padding:28px 32px 8px"><img src="${h(SITE_URL)}/img/logo-rkdp.png" alt="RKDP spółka doradztwa podatkowego" width="160" style="display:block;height:auto"></td></tr>`
    + `<tr><td style="padding:8px 32px 32px"><h1 style="font-size:22px;line-height:1.3;margin:12px 0 16px;color:#1D1A16">${h(title)}</h1>${inner}</td></tr>`
    + '<tr><td style="padding:20px 32px;border-top:1px solid #E3D9CA;font-size:12px;line-height:1.6;color:#6A6157">'
    + 'RKDP spółka doradztwa podatkowego sp. z o.o., ul. Czereśniowa 28d, 55-010 Ozorzyce, NIP 8992871126, KRS 0000812185.<br>'
    + 'Kancelaria: ul. Beaty Artemskiej 11/44, 52-234 Wrocław · +48 883 643 565'
    + '</td></tr></table></td></tr></table></body></html>';
}

export const P = (s) => `<p style="font-size:15px;line-height:1.7;color:#4A433B;margin:0 0 12px">${s}</p>`;
export const button = (url, label) => `<p style="margin:24px 0"><a href="${h(url)}" style="display:inline-block;background:#7A5A37;color:#ffffff;text-decoration:none;font-weight:bold;padding:14px 26px;border-radius:999px">${h(label)}</a></p>`;

/** Strona wynikowa w stylu witryny. */
export function sendPage(res, title, html, status = 200) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('X-Robots-Tag', 'noindex');
  res.setHeader('Cache-Control', 'no-store');
  res.end('<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">'
    + `<title>${h(title)} – RKDP</title><link rel="icon" href="/img/favicon.svg" type="image/svg+xml">`
    + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=Montserrat:wght@400;600&display=swap">'
    + '<style>body{margin:0;background:#F8F5F0;color:#1D1A16;font-family:Montserrat,system-ui,sans-serif;line-height:1.7}'
    + '.box{max-width:620px;margin:8vh auto;padding:40px 32px;background:#fff;border:1px solid #E3D9CA;border-radius:24px}'
    + 'h1{font-family:"Plus Jakarta Sans",sans-serif;font-weight:700;letter-spacing:-.02em;font-size:30px;line-height:1.15;margin:24px 0 16px}'
    + 'p{color:#4A433B}a{color:#7A5A37}.code{display:inline-block;font-family:"Plus Jakarta Sans",sans-serif;font-weight:700;font-size:26px;letter-spacing:.06em;padding:14px 22px;border:2px dashed #7A5A37;border-radius:12px;color:#7A5A37;margin:8px 0 16px}'
    + '.btn,button{display:inline-block;font:inherit;font-weight:600;cursor:pointer;border:0;margin-top:12px;background:#7A5A37;color:#fff;text-decoration:none;padding:14px 24px;border-radius:999px}'
    + '.btn.dark,button.dark{background:#1D1A16}'
    + '@media(max-width:640px){.box{margin:0;border-radius:0;border:0;min-height:100vh}}</style></head><body><div class="box">'
    + '<a href="/"><img src="/img/logo-rkdp.png" alt="RKDP spółka doradztwa podatkowego" height="48"></a>'
    + `<h1>${h(title)}</h1>${html}`
    + '<p><a class="btn" href="/">Wróć na stronę główną</a></p></div></body></html>');
}

/** Odczyt treści formularza (urlencoded lub JSON) niezależnie od parsera Vercela. */
export async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  let raw = typeof req.body === 'string' ? req.body : '';
  if (!raw) { for await (const chunk of req) raw += chunk; }
  const ct = String(req.headers['content-type'] || '');
  if (ct.includes('application/json')) { try { return JSON.parse(raw || '{}'); } catch { return {}; } }
  return Object.fromEntries(new URLSearchParams(raw));
}
