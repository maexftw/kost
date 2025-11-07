# 📧 Kontaktformular Setup - Schritt für Schritt

Diese Anleitung führt dich durch das komplette Setup des Kontaktformulars.

---

## 🎯 Teil 1: Resend Account & API Key erstellen

### Schritt 1: Account erstellen

1. **Öffne deinen Browser** und gehe zu: **https://resend.com**
2. Klicke oben rechts auf **"Sign Up"** oder **"Get Started"**
3. **Wähle eine Anmeldemethode:**
   - Mit Google Account (empfohlen, schnell)
   - Mit E-Mail-Adresse
4. **Fülle das Formular aus:**
   - Name
   - E-Mail-Adresse
   - Passwort (wenn nicht Google)
5. **Bestätige deine E-Mail** (falls nötig)

### Schritt 2: API Key erstellen

1. **Nach dem Login** siehst du das Resend Dashboard
2. **Klicke links im Menü auf:** `API Keys` (oder gehe zu: https://resend.com/api-keys)
3. **Klicke auf den Button:** `Create API Key` (oben rechts)
4. **Gib dem Key einen Namen:**
   - Z.B.: `KOST Website Contact Form`
   - Oder: `Cloudflare Pages`
5. **Wähle die Berechtigung:**
   - Wähle `Full Access` (oder `Sending Access` wenn verfügbar)
6. **Klicke auf:** `Add` oder `Create`
7. **⚠️ WICHTIG:** Der API Key wird **nur einmal** angezeigt!
   - **Kopiere ihn SOFORT** (Strg+C / Cmd+C)
   - **Speichere ihn sicher** (z.B. in einem Textdokument oder Passwort-Manager)
   - Er sieht aus wie: `re_1234567890abcdefghijklmnopqrstuvwxyz`

**✅ Du hast jetzt deinen Resend API Key!**

---

## ☁️ Teil 2: Cloudflare Pages Environment Variable setzen

### Schritt 1: Cloudflare Dashboard öffnen

1. **Öffne:** https://dash.cloudflare.com
2. **Logge dich ein** mit deinem Cloudflare Account
3. **Wähle dein Account** aus (falls mehrere vorhanden)

### Schritt 2: Zu Pages navigieren

1. **Im linken Menü** findest du verschiedene Optionen
2. **Suche nach:** `Workers & Pages` oder `Pages`
   - Falls du `Workers & Pages` siehst, klicke darauf
   - Dann siehst du `Pages` als Untermenü
3. **Klicke auf:** `Pages`

### Schritt 3: Dein Projekt auswählen

1. **Du siehst eine Liste** deiner Pages-Projekte
2. **Suche nach:** `kost` oder deinem Projektnamen
3. **Klicke auf den Projektnamen** (nicht auf die URL, sondern auf den Namen)

### Schritt 4: Settings öffnen

1. **Oben im Projekt** siehst du Tabs wie:
   - `Deployments`
   - `Settings`
   - `Custom domains`
   - etc.
2. **Klicke auf:** `Settings` (oder `Einstellungen`)

### Schritt 5: Environment Variables finden

1. **Im Settings-Menü** scrollst du nach unten
2. **Suche nach dem Abschnitt:** `Environment Variables` oder `Umgebungsvariablen`
   - Er befindet sich meist unter "Builds & deployments" oder "Functions"
3. **Du siehst eine Tabelle** mit Spalten wie:
   - Variable name
   - Value
   - Environment
   - Actions

### Schritt 6: Neue Variable hinzufügen

1. **Klicke auf den Button:** `Add variable` oder `Add environment variable` oder `+ Add`
2. **Es öffnet sich ein Formular** mit drei Feldern:

   **Feld 1: Variable name**
   - **Trage ein:** `RESEND_API_KEY`
   - ⚠️ **WICHTIG:** Genau so, mit Großbuchstaben und Unterstrichen!

   **Feld 2: Value**
   - **Füge hier deinen Resend API Key ein** (den du in Teil 1 kopiert hast)
   - Er beginnt mit `re_` gefolgt von vielen Zeichen

   **Feld 3: Environment**
   - **Wähle:** `Production` (oder beide: `Production` und `Preview`)
   - Für den Start reicht `Production`

3. **Klicke auf:** `Save` oder `Add variable`

### Schritt 7: Bestätigung

1. **Du siehst jetzt** die Variable in der Liste:
   ```
   RESEND_API_KEY    [••••••••]    Production    [Edit] [Delete]
   ```
2. **Der Value wird versteckt** angezeigt (aus Sicherheitsgründen)

**✅ Du hast die Environment Variable gesetzt!**

---

## 🚀 Teil 3: Deployment triggern

### Automatisch (empfohlen)

1. **Cloudflare Pages** erkennt automatisch neue Environment Variables
2. **Der nächste Build** verwendet die neue Variable automatisch
3. **Du kannst einen neuen Build triggern:**
   - Gehe zu `Deployments` Tab
   - Klicke auf `Retry deployment` beim letzten Build
   - Oder: Mache einen kleinen Commit und Push zu GitHub

### Manuell triggern (optional)

1. **Gehe zu:** `Deployments` Tab
2. **Klicke auf:** `Retry deployment` beim letzten Build
   - Oder: `Create deployment` → `Retry latest deployment`

---

## ✅ Teil 4: Testen

### Schritt 1: Warte auf Deployment

1. **Gehe zu:** `Deployments` Tab
2. **Warte bis** der Build Status `Success` zeigt (grünes Häkchen)
3. **Klicke auf die URL** um die Live-Version zu öffnen

### Schritt 2: Formular testen

1. **Scrolle zum Kontaktformular** auf der Website
2. **Fülle alle Felder aus:**
   - Name: Test
   - Telefon: +49 123 456789
   - E-Mail: deine-test-email@example.com
   - Nachricht: Testnachricht
3. **Klicke auf:** "Anfrage senden"
4. **Du solltest sehen:**
   - Button wird zu "Sende…"
   - Dann: "Danke! Wir melden uns kurzfristig."
   - Formular wird geleert

### Schritt 3: E-Mail prüfen

1. **Prüfe beide E-Mail-Postfächer:**
   - `info@kost-sicherheitstechnik.de`
   - `info@graphiks.de`
2. **Du solltest eine E-Mail erhalten** mit:
   - Betreff: "Neue Anfrage von Test - KOST Sicherheitstechnik"
   - Alle Formulardaten
   - Professionelles HTML-Format

**✅ Wenn die E-Mail ankommt, funktioniert alles!**

---

## 🔍 Troubleshooting

### Problem: "Server-Konfiguration fehlt"

**Ursache:** `RESEND_API_KEY` nicht gesetzt oder falsch geschrieben

**Lösung:**
1. Prüfe in Cloudflare: Settings → Environment Variables
2. Stelle sicher, dass der Name **genau** `RESEND_API_KEY` ist (Großbuchstaben!)
3. Prüfe, dass der Value der komplette API Key ist (beginnt mit `re_`)
4. Stelle sicher, dass `Production` ausgewählt ist
5. Trigger einen neuen Build

### Problem: "E-Mail konnte nicht gesendet werden"

**Ursache:** API Key ungültig oder Resend Account-Problem

**Lösung:**
1. Gehe zu Resend Dashboard → API Keys
2. Prüfe, ob der Key noch aktiv ist
3. Erstelle einen neuen API Key falls nötig
4. Aktualisiere die Variable in Cloudflare
5. Prüfe Resend Dashboard → Logs für Fehlerdetails

### Problem: E-Mails kommen nicht an

**Mögliche Ursachen:**
1. **Spam-Ordner prüfen** - E-Mails könnten dort landen
2. **Domain nicht verifiziert** - Resend sendet von `noreply@kost-sicherheitstechnik.de`
   - Lösung: Domain bei Resend verifizieren (optional, aber empfohlen)
3. **E-Mail-Adresse falsch** - Prüfe die Empfänger-Adressen

### Problem: Variable wird nicht erkannt

**Lösung:**
1. Stelle sicher, dass du im richtigen Projekt bist
2. Prüfe, dass `Production` Environment ausgewählt ist
3. Trigger einen neuen Build nach dem Setzen der Variable
4. Warte 1-2 Minuten, bis der Build fertig ist

---

## 📋 Checkliste

- [ ] Resend Account erstellt
- [ ] API Key erstellt und kopiert
- [ ] Cloudflare Dashboard geöffnet
- [ ] Pages Projekt gefunden
- [ ] Settings → Environment Variables geöffnet
- [ ] Variable `RESEND_API_KEY` hinzugefügt
- [ ] Value (API Key) eingefügt
- [ ] Environment `Production` ausgewählt
- [ ] Gespeichert
- [ ] Neuer Build getriggert
- [ ] Build erfolgreich
- [ ] Formular getestet
- [ ] E-Mail erhalten

---

## 💡 Tipps

1. **API Key sicher aufbewahren**
   - Nie in Git committen!
   - Nur in Cloudflare Environment Variables speichern

2. **Domain-Verifizierung (optional)**
   - Bessere Zustellbarkeit
   - Professionellerer Absender
   - Weniger Spam-Filter-Probleme

3. **Resend Free Tier Limits**
   - 3.000 E-Mails/Monat kostenlos
   - 100 E-Mails/Tag
   - Für die meisten Websites ausreichend

4. **Monitoring**
   - Resend Dashboard → Logs zeigt alle gesendeten E-Mails
   - Cloudflare Dashboard → Pages → Deployments zeigt Build-Status

---

## 🆘 Hilfe benötigt?

Falls du an einer Stelle nicht weiterkommst:
1. Prüfe die Screenshots in dieser Anleitung
2. Schau in die Resend/Cloudflare Dokumentation
3. Prüfe die Browser-Konsole für Fehler (F12 → Console)
4. Prüfe Cloudflare Pages → Deployments → Logs für Build-Fehler

**Viel Erfolg! 🚀**

