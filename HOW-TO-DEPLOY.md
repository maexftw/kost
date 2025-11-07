# 🚀 Neuen Build in Cloudflare Pages triggern

## Option 1: Über Cloudflare Dashboard (manuell)

1. **Gehe zu:** https://dash.cloudflare.com
2. **Klicke:** `Workers & Pages` → `Pages`
3. **Klicke auf dein Projekt:** `kost`
4. **Gehe zum Tab:** `Deployments`
5. **Suche den letzten Build** in der Liste
6. **Klicke auf die drei Punkte** (⋯) rechts neben dem Build
7. **Wähle:** `Retry deployment` oder `Redeploy`

**Oder:**
- Klicke direkt auf den letzten Build
- Oben rechts sollte ein Button `Retry deployment` sein

## Option 2: Über Git Push (automatisch) - EINFACHER

Einfach einen kleinen Commit pushen, dann baut Cloudflare automatisch neu:

1. **Öffne Terminal** in deinem Projekt-Ordner
2. **Führe aus:**
   ```bash
   git commit --allow-empty -m "chore: Trigger rebuild after Secret setup"
   git push origin main
   ```
3. **Warte 1-2 Minuten** - Cloudflare baut automatisch neu

## Nach dem Build

1. **Prüfe den Build-Status:**
   - Cloudflare Dashboard → Deployments
   - Status sollte `Success` (grün) sein

2. **Teste das Formular:**
   - Gehe zu https://kost-9h6.pages.dev
   - Fülle das Kontaktformular aus
   - Prüfe, ob die E-Mail ankommt

---

**Tipp:** Option 2 (Git Push) ist einfacher, da Cloudflare automatisch erkennt, dass sich etwas geändert hat und einen neuen Build startet.

