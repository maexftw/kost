# Netlify Deployment Workflow für Kaffee Fänsen

## Übersicht
Diese Anleitung beschreibt den kompletten Workflow für das Deployment der Kaffee Fänsen Website auf Netlify.

## Site-Informationen
- **Site Name:** dancing-elf-56bc97
- **Site ID:** c08fb486-dca7-408e-8346-f4d6cd794e79
- **Live URL:** https://dancing-elf-56bc97.netlify.app
- **GitHub Repo:** https://github.com/maexftw/kaffee-faensen
- **Netlify Personal Access Token:** `nfp_dCbuWGG...` (Gespeichert in deinen Netlify Account Settings)

## Wichtige Erkenntnisse

### 1. Hidden Folder Problem
**Problem:** Netlify ignoriert Ordner die mit `.` beginnen (wie `.superdesign/`)

**Lösung:** Alle Deploy-relevanten Dateien müssen in einem sichtbaren Ordner liegen.

**Aktuelle Struktur:**
```
CODEX/
├── .superdesign/design_iterations/  ← BACKUP (wird nicht deployed)
│   ├── faensen_homepage_3_final_3.html
│   └── faensen_shop_1.html
├── shop/                            ← PRODUCTION (wird deployed)
│   ├── homepage.html
│   ├── shop.html
│   ├── faensen_navigation.js
│   ├── faensen_shop_theme.css
│   └── stripe-payment-links.js
├── netlify/functions/
│   ├── create-checkout.js
│   ├── create-checkout-session.js
│   └── stripe-webhook.js
├── index.html                       ← Redirect zu /shop/homepage.html
├── success.html
├── cancel.html
├── netlify.toml
└── package.json
```

### 2. Relative Links in Navigation
Alle Links in `faensen_navigation.js` müssen relativ zum `/shop/` Ordner sein:
- ✅ `homepage.html` (nicht `faensen_homepage_3_final_3.html`)
- ✅ `shop.html` (nicht `faensen_shop_1.html`)
- ✅ `homepage.html#start` für Anchor-Links

## Workflow: Änderungen an der Website machen

### Schritt 1: Lokale Änderungen in `.superdesign/`
Arbeite normal in `.superdesign/design_iterations/` an deinen Designs:
```bash
# Beispiel: Bearbeite die Homepage
# Datei: .superdesign/design_iterations/faensen_homepage_3_final_3.html
```

### Schritt 2: Dateien in den `shop/` Ordner kopieren
Wenn du mit den Änderungen zufrieden bist, kopiere sie nach `shop/`:

```bash
# Homepage aktualisieren
cp .superdesign/design_iterations/faensen_homepage_3_final_3.html shop/homepage.html

# Shop-Seite aktualisieren
cp .superdesign/design_iterations/faensen_shop_1.html shop/shop.html

# Weitere Dateien bei Bedarf
cp .superdesign/design_iterations/faensen_navigation.js shop/
cp .superdesign/design_iterations/faensen_shop_theme.css shop/
cp .superdesign/design_iterations/stripe-payment-links.js shop/
```

### Schritt 3: Links überprüfen
**WICHTIG:** Stelle sicher, dass alle internen Links in den kopierten Dateien korrekt sind:

In `shop/faensen_navigation.js`:
```javascript
// ✅ RICHTIG - Relative Pfade innerhalb von /shop/
<a href="homepage.html">
<a href="shop.html">
<a href="homepage.html#start">

// ❌ FALSCH - Alte Dateinamen
<a href="faensen_homepage_3_final_3.html">
<a href="faensen_shop_1.html">
<a href="../.superdesign/...">
```

### Schritt 4: Git Commit & Push

⚠️ **KRITISCH: Repository-Check vor jedem Push!**

```bash
# ⚠️ IMMER ZUERST: Überprüfe dass du im richtigen Repository bist!
git remote -v
# Muss zeigen: origin https://github.com/maexftw/kaffee-faensen.git

# Überprüfe Working Directory
pwd
# Muss zeigen: .../CODEX oder ähnlich (NICHT bf6-squad!)

# ⚠️ Falls falsches Repository: STOP! Navigiere zum richtigen Ordner!
```

**Warum ist das wichtig?**
- Es gibt mehrere Projekte im gleichen Workspace (bf6-squad, kaffee-faensen, holdontime)
- Ein Push zum falschen Repository überschreibt fremde Projekte
- Immer verifizieren BEVOR du pushst!

```bash
# Geänderte Dateien zum Staging hinzufügen
git add shop/

# Optional: Auch andere Änderungen
git add index.html
git add netlify/functions/

# Commit erstellen
git commit -m "Update: [Beschreibung deiner Änderungen]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# ⚠️ NOCHMAL CHECKEN vor dem Push!
git remote -v

# Zum korrekten Repository pushen
git push origin main
```

### Schritt 5: Netlify Deployment triggern (Optional)
Netlify deployed automatisch bei jedem Push. Wenn du es manuell triggern willst:

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_NETLIFY_TOKEN" \
  "https://api.netlify.com/api/v1/sites/YOUR_SITE_ID/builds"
```

### Schritt 6: Deployment Status prüfen
```bash
# Deployment Status abrufen (ersetze DEPLOY_ID mit der ID aus Schritt 5)
curl -H "Authorization: Bearer YOUR_NETLIFY_TOKEN" \
  "https://api.netlify.com/api/v1/sites/YOUR_SITE_ID/deploys/DEPLOY_ID" \
  | grep -o '"state":"[^"]*"'

# Status "ready" = Deployment erfolgreich
```

## Häufige Probleme & Lösungen

### Problem: 404 Fehler auf deployed Site
**Ursache:** Dateien liegen in einem Hidden Folder (`.superdesign/`)
**Lösung:** Dateien nach `shop/` kopieren (siehe Schritt 2)

### Problem: Navigation funktioniert nicht / 404 beim Klicken
**Ursache:** Links zeigen noch auf alte Dateinamen oder Pfade
**Lösung:** Links in `faensen_navigation.js` auf neue Namen aktualisieren (siehe Schritt 3)

### Problem: Änderungen werden nicht deployed
**Ursache 1:** Dateien wurden in `.superdesign/` geändert aber nicht nach `shop/` kopiert
**Lösung:** Schritt 2 durchführen

**Ursache 2:** Änderungen nicht committed/pushed
**Lösung:** Git Status prüfen: `git status`, dann Schritt 4 durchführen

### Problem: GitHub blockiert Push wegen Secrets
**Ursache:** Stripe API Keys oder andere Secrets in Dateien
**Lösung:**
1. Secrets aus Dateien entfernen (durch Platzhalter ersetzen)
2. Letzten Commit zurücksetzen: `git reset --soft HEAD~1`
3. Dateien erneut bearbeiten und committen

### Problem: Falsches Repository ⚠️ KRITISCH!
**Ursache:** Git Remote zeigt auf falsches Repo (z.B. bf6-squad statt kaffee-faensen)

**Symptome:**
- Fremde Website zeigt falsche Inhalte (z.B. bf6-squad zeigt Hold-on-Time)
- Push wird zu falschem Repository durchgeführt
- Andere Projekte werden überschrieben

**Prävention:**
```bash
# ⚠️ VOR JEDEM PUSH diese Checks durchführen:

# 1. Repository überprüfen
git remote -v
# Erwartete Ausgabe: origin https://github.com/maexftw/kaffee-faensen.git

# 2. Working Directory überprüfen
pwd
# Erwartete Ausgabe: .../CODEX (NICHT bf6-squad oder holdontime!)

# 3. Branch überprüfen
git branch --show-current
# Erwartete Ausgabe: main
```

**Falls falsches Repository erkannt:**
```bash
# Option 1: Remote URL korrigieren (wenn im richtigen Ordner)
git remote set-url origin https://github.com/maexftw/kaffee-faensen.git

# Option 2: Zum richtigen Ordner navigieren
cd "I:\Wordpress_NEU\Design Projekte\CAS\CODEX"
git remote -v  # Nochmal verifizieren!

# Option 3: Falls bereits falsch gepusht (NOTFALL)
# Siehe Abschnitt "Notfall: Falscher Push rückgängig machen"
```

## Notfall: Falscher Push rückgängig machen

**Szenario:** Du hast versehentlich Kaffee Fänsen Dateien ins bf6-squad (oder anderes) Repository gepusht.

### Schritt 1: Backup des falschen Repos finden
```bash
# Clone das betroffene Repository in temp Verzeichnis
cd /tmp
git clone https://github.com/maexftw/bf6-squad.git bf6-recovery
cd bf6-recovery

# Finde den letzten korrekten Commit (VOR dem falschen Push)
git log --oneline --all
# Suche nach dem letzten richtigen Commit (z.B. "Update: Eric MIA redesign")
```

### Schritt 2: Korrekte Version wiederherstellen
```bash
# Checkout des korrekten Commits (ersetze COMMIT_HASH mit richtigem Hash)
git checkout COMMIT_HASH -- index.html

# Oder: Bestimmte Dateien aus altem Commit wiederherstellen
git show COMMIT_HASH:index.html > index.html

# Überprüfen ob Datei korrekt ist
head -20 index.html
```

### Schritt 3: Fix committen und pushen
```bash
git add index.html
git commit -m "CRITICAL FIX: Restore correct [project name] page

- Restored original content from commit COMMIT_HASH
- Removed incorrect content that was accidentally pushed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push zum korrekten Repository
git push origin main

# GitHub Pages Cache leeren (leerer Commit zum Neu-Deployen)
git commit --allow-empty -m "Trigger GitHub Pages rebuild"
git push origin main
```

### Schritt 4: Warten und verifizieren
```bash
# Warte 5-10 Minuten bis GitHub Pages neu deployed
# Dann teste in Inkognito-Fenster oder mit Hard Refresh (Ctrl+Shift+R)
```

## Stripe Checkout Konfiguration

### Environment Variable (bereits gesetzt)
- **Variable:** `STRIPE_SECRET_KEY`
- **Wert:** `sk_test_51Qux1Q...` (Dein Stripe Test Secret Key)
- **Wo:** Netlify Dashboard → Site Settings → Environment Variables

### Netlify Functions
Die folgenden Functions sind deployed und funktionieren:
1. **create-checkout.js** - Multi-Produkt Checkout
2. **create-checkout-session.js** - Single-Produkt Checkout
3. **stripe-webhook.js** - Webhook Handler

### Payment Methods
- Kreditkarte (card)
- SEPA Lastschrift (sepa_debit)

### Test-Zahlung
- **Test Card:** `4242 4242 4242 4242`
- **Datum:** Beliebiges zukünftiges Datum
- **CVC:** Beliebige 3 Ziffern
- **PLZ:** Beliebige 5 Ziffern

## Netlify API Befehle

### Deployment Status abrufen
```bash
curl -H "Authorization: Bearer YOUR_NETLIFY_TOKEN" \
  "https://api.netlify.com/api/v1/sites/YOUR_SITE_ID"
```

### Deployed Files auflisten
```bash
curl -H "Authorization: Bearer YOUR_NETLIFY_TOKEN" \
  "https://api.netlify.com/api/v1/sites/YOUR_SITE_ID/files"
```

### Neue Deployment triggern
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_NETLIFY_TOKEN" \
  "https://api.netlify.com/api/v1/sites/YOUR_SITE_ID/builds"
```

**Hinweis:** Ersetze `YOUR_NETLIFY_TOKEN` und `YOUR_SITE_ID` mit den tatsächlichen Werten aus den Site-Informationen oben.

## Schnell-Checkliste für Deployment

- [ ] Änderungen in `.superdesign/design_iterations/` gemacht
- [ ] Dateien nach `shop/` kopiert
- [ ] Links in Navigation überprüft (keine alten Dateinamen)
- [ ] ⚠️ **KRITISCH:** Working Directory überprüft: `pwd` (muss CODEX zeigen!)
- [ ] ⚠️ **KRITISCH:** Git Remote überprüft: `git remote -v` (muss kaffee-faensen zeigen!)
- [ ] `git status` geprüft
- [ ] Dateien staged: `git add shop/`
- [ ] Commit erstellt mit aussagekräftiger Message
- [ ] ⚠️ **VOR DEM PUSH:** Nochmal `git remote -v` überprüfen!
- [ ] Zu richtigem Repo gepusht: `git push origin main`
- [ ] Netlify Deployment abwarten (ca. 30-60 Sekunden)
- [ ] Live-Site testen: https://dancing-elf-56bc97.netlify.app
- [ ] Navigation testen (zwischen Shop und Homepage wechseln)
- [ ] Checkout-Flow testen (optional)

## URLs zum Testen

- **Homepage:** https://dancing-elf-56bc97.netlify.app
- **Shop:** https://dancing-elf-56bc97.netlify.app/shop/shop.html
- **Success Page:** https://dancing-elf-56bc97.netlify.app/success.html
- **Cancel Page:** https://dancing-elf-56bc97.netlify.app/cancel.html

## Backup-Strategie

**Immer die Originale in `.superdesign/` behalten!**
- `.superdesign/design_iterations/` = Source of Truth, Backup
- `shop/` = Production-Kopie für Deployment

Bei Problemen kannst du jederzeit von `.superdesign/` neu kopieren.

---

**Zuletzt aktualisiert:** 2025-10-27
**Funktioniert mit:** Netlify, GitHub, Stripe Checkout
