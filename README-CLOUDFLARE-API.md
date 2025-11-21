# Cloudflare API - Permanente Einrichtung

## 🎯 Ziel
Permanente API-Verbindung zu Cloudflare, die über alle Sessions hinweg funktioniert.

## 🚀 Schnellstart

### 1. Setup einmalig ausführen

```bash
cd kost-repo
python setup-cloudflare-api.py
```

Das Script fragt dich nach:
- **API Token** (erstellst du hier: https://dash.cloudflare.com/profile/api-tokens)
- **Zone ID** (optional - wird automatisch gefunden)
- **Account ID** (optional)
- **Domain** (Standard: kost-sicherheitstechnik.de)

### 2. Config wird gespeichert

Die Konfiguration wird in `.cloudflare-config.json` gespeichert:
- ✅ **NICHT** in Git committed (ist in .gitignore)
- ✅ Wird von allen Scripts automatisch verwendet
- ✅ Funktioniert über alle Sessions hinweg

### 3. Scripts verwenden

Jetzt kannst du alle Cloudflare-Scripts verwenden:

```bash
# Prüfe alle WAF Rules
python check-cloudflare-rules.py

# Analysiere und fixe Googlebot-Probleme
python fix-googlebot-403.py

# Verwalte alle Cloudflare Rules
python manage-cloudflare.py
```

**Alle Scripts verwenden automatisch die gespeicherte Konfiguration!**

## 📋 API Token erstellen

1. Gehe zu: https://dash.cloudflare.com/profile/api-tokens
2. Klicke auf **"Create Token"**
3. Wähle **"Create Custom Token"**

**Permissions (empfohlen):**
- Zone → Zone:Read, Zone:Edit
- Zone → Zone Settings:Read, Zone Settings:Edit
- Zone → Zone WAF:Read, Zone WAF:Edit
- Zone → Zone Firewall Services:Read, Zone Firewall Services:Edit
- Zone → Zone Rate Limiting:Read, Zone Rate Limiting:Edit

**Zone Resources:**
- Include → Specific zone → `kost-sicherheitstechnik.de`

4. Kopiere den Token (wird nur einmal angezeigt!)

## 🔒 Sicherheit

- ✅ Config-Datei ist in `.gitignore` (wird nicht committed)
- ✅ Token kann jederzeit in Cloudflare Dashboard gelöscht werden
- ✅ Umgebungsvariablen haben Priorität (falls gesetzt)

## 🔄 Config aktualisieren

Falls du den Token ändern musst:

```bash
python setup-cloudflare-api.py
```

Das Script fragt, ob die bestehende Config überschrieben werden soll.

## 📁 Dateien

- `setup-cloudflare-api.py` - Einmaliges Setup
- `.cloudflare-config.json` - Gespeicherte Konfiguration (nicht in Git)
- `check-cloudflare-rules.py` - Prüft alle Rules
- `fix-googlebot-403.py` - Fixt Googlebot-Probleme
- `manage-cloudflare.py` - Verwaltet alle Rules

## 💡 Zusammenarbeit

Nach dem Setup kann ich (Auto) direkt mit Cloudflare arbeiten:
- ✅ Rules analysieren
- ✅ Probleme identifizieren
- ✅ Fixes vorschlagen UND umsetzen
- ✅ Änderungen testen

**Du musst nur einmal das Setup ausführen, dann funktioniert alles automatisch!**

