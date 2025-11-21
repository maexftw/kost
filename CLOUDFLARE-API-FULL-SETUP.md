# Cloudflare API - Vollzugang Setup

## Ziel
Vollständiger API-Zugang für direkte Zusammenarbeit - Lesen UND Schreiben von WAF Rules, Firewall Rules, etc.

## Schritt 1: API Token mit Vollzugang erstellen

### Option A: Global API Key (Einfach, aber weniger sicher)
1. Gehe zu: https://dash.cloudflare.com/profile/api-tokens
2. Scrolle nach unten zu **"API Keys"**
3. Klicke auf **"View"** bei **"Global API Key"**
4. Kopiere den Key (wird nur einmal angezeigt!)

**⚠️ WICHTIG:** Global API Key hat Zugriff auf ALLE Domains in deinem Account!

### Option B: Custom Token mit spezifischen Rechten (EMPFOHLEN)

1. Gehe zu: https://dash.cloudflare.com/profile/api-tokens
2. Klicke auf **"Create Token"**
3. Klicke auf **"Create Custom Token"**

**Token Name:** `KOST Website Management`

**Permissions:**
- **Zone** → `Zone:Read`
- **Zone** → `Zone Settings:Read`
- **Zone** → `Zone Settings:Edit`
- **Zone** → `Zone WAF:Read`
- **Zone** → `Zone WAF:Edit`
- **Zone** → `Zone Firewall Services:Read`
- **Zone** → `Zone Firewall Services:Edit`
- **Zone** → `Zone Rate Limiting:Read`
- **Zone** → `Zone Rate Limiting:Edit`
- **Zone** → `Zone DNS:Read`
- **Zone** → `Zone DNS:Edit`
- **Account** → `Account WAF:Read` (falls vorhanden)
- **Account** → `Account WAF:Edit` (falls vorhanden)

**Zone Resources:**
- Include → Specific zone → `kost-sicherheitstechnik.de`

4. Klicke auf **"Continue to summary"**
5. Prüfe die Permissions
6. Klicke auf **"Create Token"**
7. **WICHTIG:** Kopiere den Token sofort!

## Schritt 2: Zone ID finden

1. Gehe zu: https://dash.cloudflare.com
2. Wähle Domain: `kost-sicherheitstechnik.de`
3. Rechts in der Sidebar: **"Zone ID"** kopieren

## Schritt 3: Account ID finden (optional, für Account-WAF)

1. In Cloudflare Dashboard → Rechts oben auf dein Profil
2. Account ID steht dort

## Schritt 4: Konfiguration speichern

Erstelle eine Datei `.cloudflare-config.json` (wird zu .gitignore hinzugefügt):

```json
{
  "api_token": "dein-api-token-hier",
  "zone_id": "deine-zone-id-hier",
  "account_id": "deine-account-id-hier",
  "domain": "kost-sicherheitstechnik.de"
}
```

**ODER** als Umgebungsvariablen (sicherer):

**Windows PowerShell:**
```powershell
$env:CLOUDFLARE_API_TOKEN = "dein-token"
$env:CLOUDFLARE_ZONE_ID = "deine-zone-id"
$env:CLOUDFLARE_ACCOUNT_ID = "deine-account-id"
```

**Linux/Mac:**
```bash
export CLOUDFLARE_API_TOKEN="dein-token"
export CLOUDFLARE_ZONE_ID="deine-zone-id"
export CLOUDFLARE_ACCOUNT_ID="deine-account-id"
```

## Schritt 5: Scripts verwenden

Ich habe mehrere Scripts erstellt:
- `check-cloudflare-rules.py` - Prüft alle Rules
- `fix-googlebot-403.py` - Behebt Googlebot 403-Fehler automatisch
- `manage-waf-rules.py` - Verwaltet WAF Rules

## Sicherheit

⚠️ **WICHTIG:**
- API Token **NIEMALS** in Git committen!
- `.cloudflare-config.json` ist in `.gitignore`
- Token kann jederzeit in Cloudflare Dashboard gelöscht/regeneriert werden
- Bei Verdacht auf Kompromittierung: Token sofort löschen und neu erstellen

## Was wir damit machen können

✅ **Lesen:**
- Alle WAF Custom Rules
- Alle Rate Limiting Rules
- Alle Firewall Rules
- Bot Fight Mode Status
- IP Access Rules

✅ **Schreiben/Ändern:**
- WAF Rules erstellen/ändern/löschen
- Rate Limiting Rules anpassen
- Firewall Rules modifizieren
- Googlebot-Ausnahmen hinzufügen
- Regeln deaktivieren/aktivieren

## Zusammenarbeit

Wenn du mir den API Token gibst (per Nachricht, nicht in Git!), kann ich:
1. Alle Rules analysieren
2. Probleme identifizieren
3. Fixes vorschlagen UND direkt umsetzen
4. Änderungen testen
5. Status prüfen

**Workflow:**
1. Du gibst mir Token (oder setzt Umgebungsvariable)
2. Ich analysiere die Rules
3. Ich schlage Fixes vor
4. Du bestätigst → Ich setze um
5. Wir testen zusammen

