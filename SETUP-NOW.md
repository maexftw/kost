# 🎯 Cloudflare Environment Variable setzen - JETZT

## Schritt-für-Schritt (2 Minuten)

**⚠️ WICHTIG:** 
- Verwende **"Secret"** (nicht "Text") für den API Key in Cloudflare!
- Der API Key sollte NIEMALS in Git committed werden.

### 1. Cloudflare Dashboard öffnen
- Gehe zu: **https://dash.cloudflare.com**
- Logge dich ein

### 2. Zu Pages navigieren
- Klicke links im Menü auf: **"Workers & Pages"**
- Dann klicke auf: **"Pages"**

### 3. Projekt auswählen
- Klicke auf dein Projekt: **"kost"** (oder wie es heißt)

### 4. Settings öffnen
- Klicke oben auf den Tab: **"Settings"**

### 5. Environment Variables finden
- Scrolle nach unten zu: **"Environment Variables"**
- Du siehst eine Tabelle oder Liste

### 6. Variable hinzufügen
- Klicke auf: **"Add variable"** oder **"+ Add"** Button

### 7. Formular ausfüllen

**Variable name:**
```
RESEND_API_KEY
```
⚠️ Genau so, mit Großbuchstaben!

**Type:**
- Wähle: **"Secret"** (NICHT "Text"!) ⚠️

**Value:**
- Füge deinen Resend API Key ein (aus Resend Dashboard kopiert)

**Environment:**
- Wähle: **"Production"** ✓

### 8. Speichern
- Klicke auf: **"Save"** oder **"Add variable"**

### 9. Build triggern
- Gehe zum Tab: **"Deployments"**
- Klicke auf: **"Retry deployment"** beim letzten Build
- Oder warte auf den nächsten automatischen Build

## ✅ Fertig!

Nach dem Build (1-2 Minuten) sollte das Kontaktformular funktionieren.

## Testen
1. Öffne deine Live-Website
2. Fülle das Kontaktformular aus
3. Klicke "Anfrage senden"
4. Prüfe die E-Mail-Postfächer:
   - info@kost-sicherheitstechnik.de
   - info@graphiks.de

---

## 🔒 Sicherheitshinweis

**WICHTIG:** 
- API Keys sollten **NIEMALS** in Git committed werden
- Verwende immer **"Secret"** (nicht "Text") in Cloudflare für API Keys
- Falls ein Key versehentlich committed wurde: Key im Resend Dashboard rotieren (löschen und neu erstellen)

