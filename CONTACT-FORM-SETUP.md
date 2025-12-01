# Kontaktformular Setup

Das Kontaktformular verwendet Cloudflare Pages Functions und Resend API mit mehrschichtigem Spam-Schutz und Backup-Speicherung.

## Features

- **E-Mail-Versand** über Resend API
- **Turnstile CAPTCHA** mit automatischem Fallback für Adblocker-Nutzer
- **Math-Captcha** als Fallback (einfache Rechenaufgabe)
- **KV Backup**: Alle Anfragen werden gespeichert - auch wenn E-Mail fehlschlägt!
- **Spam-Schutz**: Honeypot, Rate Limiting, Bot Detection, Keyword-Filter

## Setup-Schritte

### 1. Resend Account erstellen
1. Gehe zu https://resend.com
2. Erstelle einen kostenlosen Account
3. Verifiziere die Domain `mail.kost-sicherheitstechnik.de` (für bessere Zustellbarkeit)

### 2. API Key erstellen
1. In Resend Dashboard: Settings → API Keys
2. Erstelle einen neuen API Key
3. Kopiere den API Key (wird nur einmal angezeigt!)

### 3. Cloudflare Pages Environment Variables setzen
1. Gehe zu Cloudflare Dashboard → Pages → Projekt "kost"
2. Settings → Environment variables
3. Füge hinzu:

| Variable | Wert | Type |
|----------|------|------|
| `RESEND_API_KEY` | Dein Resend API Key | Secret |
| `TURNSTILE_SECRET_KEY` | `0x4AAAAAACA6u-DUxcpSWGSv6Cf1Stuv7_Q` | Secret |

### 4. KV Namespace für Backup einrichten (WICHTIG!)

Das KV Backup stellt sicher, dass **keine Kontaktanfrage verloren geht** - auch wenn die E-Mail fehlschlägt!

1. Gehe zu **Cloudflare Dashboard** → **Workers & Pages** → **KV**
2. Klicke **"Create namespace"**
3. Name: `CONTACT_BACKUP_KV`
4. Gehe zu **Pages** → Projekt **"kost"** → **Settings** → **Functions** → **KV namespace bindings**
5. Klicke **"Add binding"**:
   - Variable name: `CONTACT_BACKUP_KV`
   - KV namespace: `CONTACT_BACKUP_KV`
6. **Wichtig**: Mache das gleiche Binding auch für **Preview** Environment!
7. **Retry deployment** um die Änderungen zu aktivieren

### 5. Kontakte aus KV abrufen

Alle Kontaktanfragen werden im Format `contact_{timestamp}_{random}` gespeichert.

**Option A: Cloudflare Dashboard**
1. Workers & Pages → KV → CONTACT_BACKUP_KV
2. Klicke auf einen Eintrag um die Details zu sehen

**Option B: Wrangler CLI**
```bash
# Alle Keys auflisten
npx wrangler kv:key list --namespace-id=<NAMESPACE_ID>

# Einzelnen Kontakt abrufen
npx wrangler kv:key get "contact_1234567890_abc123" --namespace-id=<NAMESPACE_ID>
```

**Option C: API Endpoint (optional)**
Ein API-Endpoint zum Abrufen kann bei Bedarf erstellt werden.

## Empfänger

E-Mails werden automatisch an beide Adressen gesendet:
- info@kost-sicherheitstechnik.de
- info@graphiks.de

## Spam-Schutz Features

| Feature | Beschreibung |
|---------|--------------|
| **Turnstile** | Cloudflare CAPTCHA (privacy-freundlich) |
| **Math-Captcha** | Fallback für Adblocker-Nutzer |
| **Honeypot** | Verstecktes Feld das nur Bots ausfüllen |
| **Rate Limiting** | Max. 5 Anfragen pro 15 Min. pro IP |
| **Bot Detection** | User-Agent & Header-Prüfung |
| **Keyword Filter** | Blockiert typische Spam-Begriffe |
| **URL Filter** | Keine Links in Nachrichten erlaubt |

## Wie funktioniert der Fallback?

1. **Normalfall**: Turnstile Widget wird geladen, User löst CAPTCHA
2. **Adblocker aktiv**: Nach 1 Sekunde wird erkannt dass Turnstile nicht verfügbar ist
3. **Fallback**: Einfache Rechenaufgabe (z.B. "7 + 3 = ?") wird angezeigt
4. **Server-Validierung**: Backend prüft entweder Turnstile-Token ODER Math-Captcha

## Kosten

**Resend Free Tier:**
- 3.000 E-Mails/Monat kostenlos
- 100 E-Mails/Tag Limit

**Cloudflare:**
- Turnstile: Kostenlos, unbegrenzt
- KV Storage: 100.000 Reads/Tag kostenlos, 1.000 Writes/Tag kostenlos
- Pages Functions: 100.000 Requests/Tag kostenlos

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| "Server-Konfiguration fehlt" | `RESEND_API_KEY` nicht gesetzt |
| "E-Mail konnte nicht gesendet werden" | Prüfe Resend Dashboard → Logs |
| E-Mails kommen nicht an | Spam-Ordner prüfen, Domain verifizieren |
| "Bitte bestätigen Sie..." | Weder Turnstile noch Math-Captcha wurde gelöst |
| Kontakt nicht gespeichert | KV Binding prüfen (CONTACT_BACKUP_KV) |

## E-Mail Format

Die gesendeten E-Mails enthalten:
- Name, Telefon, E-Mail des Absenders
- Nachrichtentext
- Verifizierungsmethode (turnstile/math)
- Backup-ID zur Referenz
