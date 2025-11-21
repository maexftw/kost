# Cloudflare API - Vollständige Dokumentation

## 📋 Übersicht

Die Cloudflare API ist **permanent eingerichtet** und funktioniert über alle Sessions hinweg.

**Status:** ✅ **AKTIV** - Config-Datei vorhanden, API-Verbindung getestet

---

## 🔑 Aktuelle Konfiguration

**Config-Datei:** `.cloudflare-config.json` (lokal, nicht in Git)

**Enthält:**
- ✅ API Token (aktiv)
- ✅ Zone ID: `3e5e9a329ee3b8643bf3e8f8b7aef32c`
- ✅ Domain: `kost-sicherheitstechnik.de`

**Sicherheit:**
- ✅ Datei ist in `.gitignore` (wird nicht committed)
- ✅ Token kann jederzeit in Cloudflare Dashboard gelöscht werden

---

## 🚀 Verwendung

### Für AIs/Scripts (automatisch)

Alle Scripts laden die Config **automatisch**:

```python
# Scripts prüfen automatisch:
# 1. .cloudflare-config.json (lokal)
# 2. cloudflare-config.json (Fallback)
# 3. Umgebungsvariablen (CLOUDFLARE_API_TOKEN, etc.)
```

**Verfügbare Scripts:**
- `check-cloudflare-rules.py` - Prüft alle WAF/Firewall Rules
- `fix-googlebot-403.py` - Fixt Googlebot-Blockierungen
- `manage-cloudflare.py` - Verwaltet alle Rules

### Für andere AIs/Sessions

**Option 1: Lokal (automatisch)**
- Wenn AI auf demselben System läuft → Config wird automatisch geladen
- Keine zusätzliche Konfiguration nötig

**Option 2: Umgebungsvariablen**
```powershell
# Windows PowerShell
$env:CLOUDFLARE_API_TOKEN = "dein-token"
$env:CLOUDFLARE_ZONE_ID = "3e5e9a329ee3b8643bf3e8f8b7aef32c"
```

```bash
# Linux/Mac
export CLOUDFLARE_API_TOKEN="dein-token"
export CLOUDFLARE_ZONE_ID="3e5e9a329ee3b8643bf3e8f8b7aef32c"
```

**Option 3: Config-Datei neu erstellen**
```bash
python setup-cloudflare-api.py
```

---

## 📁 Dateien

### Scripts
- `setup-cloudflare-api.py` - Einmaliges Setup (interaktiv)
- `check-cloudflare-rules.py` - Analysiert alle Rules
- `fix-googlebot-403.py` - Automatischer Fixer
- `manage-cloudflare.py` - Vollständiges Management-Tool

### Config
- `.cloudflare-config.json` - Gespeicherte Konfiguration (lokal, nicht in Git)

### Dokumentation
- `README-CLOUDFLARE-API.md` - Schnellstart-Anleitung
- `CLOUDFLARE-API-FULL-SETUP.md` - Detailliertes Setup
- `CLOUDFLARE-API-TOKEN-ANLEITUNG.md` - Token-Erstellung
- `CLOUDFLARE-API-SETUP.md` - Erste Setup-Anleitung
- `CLOUDFLARE-API-DOKUMENTATION.md` - Diese Datei (Übersicht)

---

## 🔧 API-Endpunkte die wir nutzen

### Zone-Informationen
```
GET /zones/{zone_id}
GET /zones?name={domain}
```

### WAF Rules
```
GET /zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint
PUT /zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}
```

### Firewall Rules
```
GET /zones/{zone_id}/firewall/rules
POST /zones/{zone_id}/firewall/rules
PUT /zones/{zone_id}/firewall/rules/{rule_id}
DELETE /zones/{zone_id}/firewall/rules/{rule_id}
```

### Rate Limiting
```
GET /zones/{zone_id}/rate_limits
POST /zones/{zone_id}/rate_limits
PUT /zones/{zone_id}/rate_limits/{rule_id}
DELETE /zones/{zone_id}/rate_limits/{rule_id}
```

---

## 🎯 Was wir damit machen können

### Lesen
- ✅ Alle WAF Custom Rules
- ✅ Alle Firewall Rules
- ✅ Alle Rate Limiting Rules
- ✅ Zone-Informationen
- ✅ Bot Fight Mode Status

### Schreiben/Ändern
- ✅ WAF Rules erstellen/ändern/löschen
- ✅ Firewall Rules modifizieren
- ✅ Rate Limiting Rules anpassen
- ✅ Googlebot-Ausnahmen hinzufügen
- ✅ Regeln deaktivieren/aktivieren

---

## 🔍 Aktuelle Probleme & Lösungen

### Problem: Googlebot 403-Fehler

**Gefundene WAF Rule:**
- **Name:** "Geography-based rule [Template]"
- **Expression:** `(ip.geoip.country ne "DE")`
- **Action:** `block`
- **Problem:** Blockiert alle IPs außerhalb Deutschlands, inkl. Googlebot

**Lösung:**
Expression ändern zu:
```
(ip.geoip.country ne "DE") and not (http.user_agent contains "Googlebot" or http.user_agent contains "Bingbot" or http.user_agent contains "Slurp" or http.user_agent contains "DuckDuckBot")
```

**Status:** ⚠️ Noch nicht gefixt - wartet auf Bestätigung

---

## 🔄 Config aktualisieren

### Token ändern
```bash
python setup-cloudflare-api.py
```

### Manuell bearbeiten
Öffne `.cloudflare-config.json`:
```json
{
  "api_token": "dein-neuer-token",
  "zone_id": "3e5e9a329ee3b8643bf3e8f8b7aef32c",
  "account_id": null,
  "domain": "kost-sicherheitstechnik.de"
}
```

---

## 🛡️ Sicherheit

### Best Practices
- ✅ Config-Datei ist in `.gitignore`
- ✅ Token hat nur notwendige Permissions
- ✅ Token ist nur für eine Zone (nicht alle Domains)
- ✅ Token kann jederzeit gelöscht werden

### Bei Kompromittierung
1. Gehe zu: https://dash.cloudflare.com/profile/api-tokens
2. Lösche den kompromittierten Token
3. Erstelle neuen Token
4. Führe `python setup-cloudflare-api.py` aus

---

## 📞 Support

**Probleme?**
1. Prüfe ob `.cloudflare-config.json` existiert
2. Teste API-Verbindung: `python check-cloudflare-rules.py`
3. Siehe `CLOUDFLARE-API-FULL-SETUP.md` für Details

**Token-Erstellung:**
- Siehe `CLOUDFLARE-API-TOKEN-ANLEITUNG.md`

---

## 📝 Changelog

**2025-11-21:**
- ✅ API-Verbindung eingerichtet
- ✅ Config-Datei erstellt
- ✅ Zone ID automatisch gefunden
- ✅ WAF Rules analysiert
- ✅ Googlebot-Blockierung identifiziert

---

**Letzte Aktualisierung:** 2025-11-21

