# Kontaktformular Setup

Das Kontaktformular verwendet Cloudflare Pages Functions und Resend API, um E-Mails zu versenden.

## Setup-Schritte

### 1. Resend Account erstellen
1. Gehe zu https://resend.com
2. Erstelle einen kostenlosen Account
3. Verifiziere deine Domain (optional, aber empfohlen für bessere Zustellbarkeit)

### 2. API Key erstellen
1. In Resend Dashboard: Settings → API Keys
2. Erstelle einen neuen API Key
3. Kopiere den API Key (wird nur einmal angezeigt!)

### 3. Cloudflare Pages Environment Variables setzen
1. Gehe zu Cloudflare Dashboard → Pages → Dein Projekt
2. Settings → Environment variables
3. Füge hinzu:
   - **Variable name:** `RESEND_API_KEY`
   - **Value:** Dein Resend API Key
   - **Environment:** Production (und Preview, falls gewünscht)
   - **Type:** Secret

### 3b. Cloudflare Turnstile Setup (Spam-Schutz) ✅ AKTIVIERT

**Site Key:** Bereits im HTML eingefügt ✅

**Secret Key Setup:**
1. Gehe zu Cloudflare Dashboard → **Workers & Pages** → **Pages**
2. Klicke auf dein Projekt (**"kost"** oder wie es heißt)
3. Klicke auf **"Settings"** Tab
4. Scrolle zu **"Environment variables"**
5. Klicke **"Add variable"**:
   - **Variable name:** `TURNSTILE_SECRET_KEY`
   - **Value:** `0x4AAAAAACA6u29B4YZsfcPe`
   - **Environment:** Production (und Preview, falls gewünscht)
   - **Type:** Secret ⚠️ WICHTIG: Wähle "Secret" (nicht "Text")!
6. Klicke **"Save"**
7. Gehe zu **"Deployments"** Tab und klicke **"Retry deployment"** beim letzten Build

**Fertig!** Nach dem Deployment ist Turnstile aktiv und schützt das Formular.

### 4. Domain-Verifizierung (optional, aber empfohlen)
Für bessere Zustellbarkeit solltest du deine Domain bei Resend verifizieren:
1. In Resend Dashboard: Domains → Add Domain
2. Füge `kost-sicherheitstechnik.de` hinzu
3. Füge die DNS-Records zu Cloudflare hinzu (wie von Resend angegeben)
4. Nach Verifizierung kannst du `from` in `functions/api/contact.js` anpassen

## Empfänger

E-Mails werden automatisch an beide Adressen gesendet:
- info@kost-sicherheitstechnik.de
- info@graphiks.de

## Testen

Nach dem Setup:
1. Push die Änderungen zu GitHub
2. Cloudflare Pages baut automatisch neu
3. Teste das Formular auf der Live-Website
4. Prüfe beide E-Mail-Postfächer

## Troubleshooting

- **"Server-Konfiguration fehlt"**: RESEND_API_KEY nicht gesetzt
- **"E-Mail konnte nicht gesendet werden"**: Prüfe Resend Dashboard → Logs für Details
- **E-Mails kommen nicht an**: Prüfe Spam-Ordner, Domain-Verifizierung

## Spam-Schutz Features

Das Kontaktformular verfügt über mehrschichtigen Spam-Schutz:

1. **Honeypot Field** - Verstecktes Feld, das Bots ausfüllen, Menschen aber nicht sehen
2. **Rate Limiting** - Max. 3 Anfragen pro 15 Minuten pro IP-Adresse
3. **Enhanced Validation** - Spam-Keyword-Erkennung, URL-Filter, Längenprüfung
4. **Cloudflare Turnstile** (optional) - Moderne, privacy-freundliche CAPTCHA-Alternative

**Turnstile ist kostenlos** und erfordert keine Cookies (DSGVO-freundlich).

## Kosten

Resend Free Tier:
- 3.000 E-Mails/Monat kostenlos
- 100 E-Mails/Tag Limit

Für höhere Limits: Upgrade auf Paid Plan.

Cloudflare Turnstile:
- Vollständig kostenlos
- Unbegrenzte Verifizierungen

