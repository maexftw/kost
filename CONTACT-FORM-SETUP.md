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

## Kosten

Resend Free Tier:
- 3.000 E-Mails/Monat kostenlos
- 100 E-Mails/Tag Limit

Für höhere Limits: Upgrade auf Paid Plan.

