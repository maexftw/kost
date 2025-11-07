# 🌐 Cloudflare DNS Migration - E-Mail bei all-incl behalten

Diese Anleitung zeigt dir, wie du die Domain `kost-sicherheitstechnik.de` zu Cloudflare migrierst, während die E-Mail-Funktionalität bei all-incl bleibt.

---

## 📋 Vorbereitung: Aktuelle DNS-Records von all-incl sichern

### Schritt 1: DNS-Records bei all-incl dokumentieren

1. **Logge dich bei all-incl ein**
2. **Gehe zu:** Domain-Verwaltung → DNS-Verwaltung
3. **Notiere dir ALLE Records**, besonders:
   - **MX Records** (E-Mail-Server)
   - **SPF Records** (TXT mit "v=spf1")
   - **DKIM Records** (TXT mit "v=DKIM1")
   - **DMARC Records** (TXT mit "v=DMARC1")
   - **A/AAAA Records** (falls vorhanden)
   - **CNAME Records** (falls vorhanden)

**Beispiel für E-Mail-Records:**
```
MX: mail.all-incl.de (Priority: 10)
TXT: v=spf1 include:all-incl.de ~all
TXT: v=DKIM1 ...
TXT: v=DMARC1 ...
```

---

## 🚀 Teil 1: Domain zu Cloudflare hinzufügen

### Schritt 1: Domain in Cloudflare hinzufügen

1. **Gehe zu:** https://dash.cloudflare.com
2. **Klicke:** "Add a Site" oder "+ Add Site"
3. **Gib ein:** `kost-sicherheitstechnik.de`
4. **Klicke:** "Add site"

### Schritt 2: Plan auswählen

- **Wähle:** "Free" Plan (reicht für DNS + Pages)
- **Klicke:** "Continue"

### Schritt 3: DNS-Records scannen lassen

- Cloudflare scannt automatisch die aktuellen DNS-Records
- **WICHTIG:** Prüfe, ob alle E-Mail-Records erkannt wurden
- Falls nicht: Wir fügen sie manuell hinzu

---

## 📧 Teil 2: E-Mail-Records von all-incl übertragen

### Schritt 1: MX Records hinzufügen

1. **In Cloudflare:** DNS → Records
2. **Klicke:** "Add record"
3. **Wähle:** Type: `MX`
4. **Fülle aus:**
   - **Name:** `@` (oder leer lassen für Root-Domain)
   - **Mail server:** `mail.all-incl.de` (oder was bei all-incl steht)
   - **Priority:** `10` (oder was bei all-incl steht)
   - **Proxy status:** OFF (graue Wolke) ⚠️ WICHTIG!
5. **Klicke:** "Save"

**Wiederhole für alle MX Records von all-incl**

### Schritt 2: SPF Record hinzufügen

1. **Klicke:** "Add record"
2. **Wähle:** Type: `TXT`
3. **Fülle aus:**
   - **Name:** `@`
   - **Content:** `v=spf1 include:all-incl.de ~all` (oder was bei all-incl steht)
   - **Proxy status:** OFF ⚠️
4. **Klicke:** "Save"

### Schritt 3: DKIM Record hinzufügen (falls vorhanden)

1. **Klicke:** "Add record"
2. **Wähle:** Type: `TXT`
3. **Fülle aus:**
   - **Name:** `default._domainkey` (oder was bei all-incl steht)
   - **Content:** (Kopiere den kompletten DKIM-String von all-incl)
   - **Proxy status:** OFF ⚠️
4. **Klicke:** "Save"

### Schritt 4: DMARC Record hinzufügen (falls vorhanden)

1. **Klicke:** "Add record"
2. **Wähle:** Type: `TXT`
3. **Fülle aus:**
   - **Name:** `_dmarc`
   - **Content:** `v=DMARC1; p=none; rua=mailto:...` (oder was bei all-incl steht)
   - **Proxy status:** OFF ⚠️
4. **Klicke:** "Save"

---

## 🌍 Teil 3: Website-Records für Cloudflare Pages konfigurieren

### Schritt 1: Alte Website-Records entfernen (falls vorhanden)

- Entferne alte A/AAAA Records, die auf all-incl zeigen
- **NICHT** die E-Mail-Records entfernen!

### Schritt 2: Cloudflare Pages Domain verbinden

1. **Gehe zu:** Pages → `kost` → Custom domains
2. **Klicke:** "Set up a custom domain"
3. **Gib ein:** `kost-sicherheitstechnik.de`
4. **Klicke:** "Continue"

Cloudflare erstellt automatisch die nötigen DNS-Records:
- `A` Record → Cloudflare IPs
- `CNAME` Record → Pages URL

**WICHTIG:** Diese Records haben automatisch Proxy ON (orange Wolke) ✓

---

## 🔄 Teil 4: Nameserver auf Cloudflare umstellen

### Schritt 1: Cloudflare Nameserver notieren

Nach dem Hinzufügen der Domain zeigt Cloudflare dir die Nameserver:
```
Beispiel:
ns1.cloudflare.com
ns2.cloudflare.com
```

**Notiere dir diese!**

### Schritt 2: Nameserver bei all-incl ändern

1. **Logge dich bei all-incl ein**
2. **Gehe zu:** Domain-Verwaltung → Nameserver
3. **Ändere die Nameserver zu:**
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`
4. **Speichere** die Änderung

### Schritt 3: Propagation abwarten

- **Dauer:** 24-48 Stunden (meist schneller)
- **Prüfen:** https://www.whatsmydns.net
- Gib `kost-sicherheitstechnik.de` ein und prüfe, ob die Nameserver auf Cloudflare zeigen

---

## ✅ Teil 5: Verifizierung

### E-Mail testen

1. **Sende eine Test-E-Mail** an `info@kost-sicherheitstechnik.de`
2. **Prüfe:** Kommt die E-Mail an?
3. **Antworte:** Funktioniert das Antworten?

### Website testen

1. **Öffne:** https://kost-sicherheitstechnik.de
2. **Prüfe:** Lädt die Website?
3. **Teste:** Kontaktformular funktioniert?

---

## 🔧 Troubleshooting

### Problem: E-Mails kommen nicht an

**Lösung:**
- Prüfe MX Records in Cloudflare DNS
- Stelle sicher, dass Proxy OFF ist (graue Wolke)
- Prüfe SPF Record
- Warte auf DNS-Propagation (kann bis zu 48h dauern)

### Problem: Website lädt nicht

**Lösung:**
- Prüfe Custom Domain in Cloudflare Pages
- Stelle sicher, dass A/CNAME Records auf Cloudflare zeigen
- Prüfe SSL/TLS Status (sollte "Full" sein)

### Problem: Nameserver ändern sich nicht

**Lösung:**
- Prüfe bei all-incl, ob die Änderung gespeichert wurde
- Warte auf Propagation (kann bis zu 48h dauern)
- Prüfe mit https://www.whatsmydns.net

---

## 📝 Checkliste

- [ ] DNS-Records von all-incl dokumentiert
- [ ] Domain zu Cloudflare hinzugefügt
- [ ] MX Records übertragen (Proxy OFF)
- [ ] SPF Record übertragen (Proxy OFF)
- [ ] DKIM Record übertragen (Proxy OFF, falls vorhanden)
- [ ] DMARC Record übertragen (Proxy OFF, falls vorhanden)
- [ ] Cloudflare Pages Custom Domain konfiguriert
- [ ] Nameserver bei all-incl geändert
- [ ] DNS-Propagation geprüft
- [ ] E-Mail getestet
- [ ] Website getestet

---

## 🎯 Ergebnis

Nach erfolgreicher Migration:
- ✅ **E-Mail:** Läuft weiterhin über all-incl
- ✅ **Website:** Läuft über Cloudflare Pages (schneller, sicherer)
- ✅ **DNS:** Verwaltet von Cloudflare (bessere Performance)
- ✅ **SSL:** Automatisch von Cloudflare (kostenlos)

---

## 💡 Tipp

Falls du Hilfe beim Übertragen der DNS-Records brauchst:
1. Screenshot der DNS-Records von all-incl machen
2. Ich kann dir helfen, sie richtig zu konfigurieren

**Wichtig:** Die Migration kann 24-48 Stunden dauern. Während dieser Zeit funktionieren sowohl E-Mail als auch Website weiterhin normal.

