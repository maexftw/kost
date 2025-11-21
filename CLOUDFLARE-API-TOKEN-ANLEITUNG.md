# Cloudflare API Token - Einfache Anleitung

## 🎯 Welche Option?

**Empfehlung: Custom Token** (5 Minuten Setup, aber genau richtig)

Templates sind einfacher, aber haben **nicht alle Rechte**, die wir brauchen (WAF, Firewall, Rate Limiting).

## ✅ Option 1: Custom Token (EMPFOHLEN)

### Schritt-für-Schritt:

1. **Gehe zu:** https://dash.cloudflare.com/profile/api-tokens
2. **Klicke auf:** "Create Token"
3. **Klicke auf:** "Create Custom Token" (ganz unten)

### Token konfigurieren:

**Token Name:** `KOST Website Management`

**Permissions hinzufügen:**

Klicke auf **"Add"** bei Zone und füge diese Permissions hinzu:

```
Zone - Zone:Read
Zone - Zone:Edit
Zone - Zone Settings:Read
Zone - Zone Settings:Edit
Zone - Zone WAF:Read
Zone - Zone WAF:Edit
Zone - Zone Firewall Services:Read
Zone - Zone Firewall Services:Edit
Zone - Zone Rate Limiting:Read
Zone - Zone Rate Limiting:Edit
Zone - Zone DNS:Read
Zone - Zone DNS:Edit
```

**Zone Resources:**

- Klicke auf **"Include"** → **"Specific zone"**
- Wähle: `kost-sicherheitstechnik.de`

4. **Klicke auf:** "Continue to summary"
5. **Prüfe** die Permissions
6. **Klicke auf:** "Create Token"
7. **WICHTIG:** Kopiere den Token sofort! (wird nur einmal angezeigt)

### ✅ Fertig!

Jetzt kannst du `python setup-cloudflare-api.py` ausführen und den Token eingeben.

---

## ⚠️ Option 2: Template (Einfacher, aber eingeschränkt)

Falls du es **schnell** testen willst:

1. **Gehe zu:** https://dash.cloudflare.com/profile/api-tokens
2. **Klicke auf:** "Create Token"
3. **Wähle:** "Edit zone DNS" Template
4. **Zone:** Wähle `kost-sicherheitstechnik.de`
5. **Klicke auf:** "Continue to summary"
6. **Klicke auf:** "Create Token"

**⚠️ Problem:** Dieses Template hat **KEINE** WAF/Firewall-Rechte!

- ✅ Funktioniert für: DNS, Zone Settings
- ❌ Funktioniert **NICHT** für: WAF Rules, Firewall Rules, Rate Limiting

**Du kannst damit:**
- ✅ Rules **lesen** (manchmal)
- ❌ Rules **ändern** (funktioniert nicht)

---

## 🔒 Option 3: Global API Key (Nicht empfohlen)

**⚠️ Sicherheitsrisiko:** Hat Zugriff auf **ALLE** Domains in deinem Account!

Nur verwenden, wenn du nur eine Domain hast und es schnell testen willst.

---

## 💡 Meine Empfehlung

**Nimm Option 1 (Custom Token):**
- ✅ Genau die Rechte, die wir brauchen
- ✅ Nur für eine Domain (sicherer)
- ✅ Funktioniert für alles (Lesen UND Schreiben)
- ⏱️ Dauert nur 5 Minuten

**Template nur, wenn:**
- Du es schnell testen willst
- Du nur Rules **lesen** willst (nicht ändern)

---

## 🚀 Nach dem Token erstellen

1. Führe aus: `python setup-cloudflare-api.py`
2. Gib den Token ein
3. Fertig! Alle Scripts funktionieren jetzt.

