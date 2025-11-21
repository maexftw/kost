# Cloudflare API Setup für WAF Rules Check

## Schritt 1: API Token erstellen

1. Gehe zu: https://dash.cloudflare.com/profile/api-tokens
2. Klicke auf **"Create Token"**
3. Wähle **"Edit zone DNS"** Template ODER erstelle Custom Token:

### Custom Token (Empfohlen - nur Leserechte)

**Token Name:** `WAF Rules Checker`

**Permissions:**
- **Zone** → `Zone:Read`
- **Zone** → `Zone Settings:Read`  
- **Zone** → `Zone WAF:Read`
- **Account** → `Account WAF:Read` (falls vorhanden)

**Zone Resources:**
- Include → Specific zone → `kost-sicherheitstechnik.de`

4. Klicke auf **"Continue to summary"**
5. Klicke auf **"Create Token"**
6. **WICHTIG:** Kopiere den Token sofort (wird nur einmal angezeigt!)

## Schritt 2: Zone ID finden

1. Gehe zu: https://dash.cloudflare.com
2. Wähle deine Domain: `kost-sicherheitstechnik.de`
3. Rechts in der Sidebar findest du **"Zone ID"**
4. Kopiere diese ID

## Schritt 3: Script konfigurieren

1. Öffne `check-cloudflare-rules.py`
2. Füge deinen API Token ein:
   ```python
   CLOUDFLARE_API_TOKEN = "dein-token-hier"
   ```
3. Füge deine Zone ID ein (optional, wird automatisch gefunden):
   ```python
   ZONE_ID = "deine-zone-id-hier"
   ```

## Schritt 4: Script ausführen

```bash
cd kost-repo
python check-cloudflare-rules.py
```

Das Script zeigt dir:
- ✅ Alle WAF Custom Rules
- ✅ Alle Rate Limiting Rules
- ✅ Alle Firewall Rules
- ⚠️ Mögliche Probleme (Regeln die Googlebot blockieren könnten)

## Alternative: API Token per Umgebungsvariable

Sicherer ist es, den Token als Umgebungsvariable zu setzen:

**Windows PowerShell:**
```powershell
$env:CLOUDFLARE_API_TOKEN = "dein-token-hier"
python check-cloudflare-rules.py
```

**Linux/Mac:**
```bash
export CLOUDFLARE_API_TOKEN="dein-token-hier"
python check-cloudflare-rules.py
```

Dann im Script ändern:
```python
import os
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
```

## Was das Script prüft

1. **WAF Custom Rules:**
   - Zielt die Regel auf `/` statt nur `/api/contact`?
   - Blockiert die Regel Bots ohne Googlebot-Ausnahme?
   - Hat die Regel eine Blocking-Action ohne Googlebot-Ausnahme?

2. **Rate Limiting Rules:**
   - Zielt die Regel auf `/` statt nur `/api/contact`?

3. **Firewall Rules:**
   - Blockiert die Regel Googlebot?

## Beispiel-Output

```
============================================================
WAF Custom Rules
============================================================
📋 2 WAF Custom Rules gefunden:

Rule #1: Block Bots on Contact Form
  Expression: (http.request.uri.path eq "/api/contact") and (cf.client.bot eq true)
  Action: block
  ✅ Keine Probleme gefunden

Rule #2: Block All Bots
  Expression: (cf.client.bot eq true)
  Action: block
  ⚠️ PROBLEME:
    - ⚠️ Regel blockiert Bots, aber hat keine Googlebot-Ausnahme
    - ⚠️ Regel blockiert/challenged ohne Googlebot-Ausnahme
```

## Sicherheit

⚠️ **WICHTIG:** 
- Teile deinen API Token **NIEMALS** öffentlich
- Verwende nur Leserechte (Read Permissions)
- Token kann jederzeit in Cloudflare Dashboard gelöscht werden

