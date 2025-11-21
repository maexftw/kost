# KRITISCH: Googlebot 403-Fehler beheben

## Problem
Google Search Console zeigt: **"Wegen Zugriffsverbot (403) blockiert"**

Das bedeutet, dass Googlebot die Seite nicht crawlen kann, obwohl es in AI Crawl Control auf "Allow" steht.

## Mögliche Ursachen (wenn Googlebot auf "Allow" steht)

1. **WAF Custom Rules** blockieren Googlebot
2. **Rate Limiting Rules** blockieren zu viele Requests
3. **IP Access Rules** blockieren Googlebot IPs
4. **Firewall Rules** mit falscher Konfiguration
5. **robots.txt** oder andere Server-Konfigurationen

## Lösung: Andere Blockierungen finden und beheben

### Schritt 1: WAF Custom Rules prüfen (WICHTIG!)
1. Gehe zu: **Security** → **WAF** → **Custom Rules**
2. Prüfe **ALLE** aktiven Regeln
3. Suche nach Regeln, die:
   - Auf `/` oder `/*` zielen (nicht nur `/api/contact`)
   - Bots blockieren ohne Googlebot-Ausnahme
   - Rate Limiting ohne Googlebot-Ausnahme haben
4. **Falls eine Regel Googlebot blockiert:**
   - Füge eine Ausnahme hinzu: `and not (http.user_agent contains "Googlebot")`
   - Oder ändere die Regel, dass sie nur `/api/contact` betrifft

### Schritt 2: Rate Limiting Rules prüfen
1. Gehe zu: **Security** → **WAF** → **Rate limiting rules**
2. Prüfe alle aktiven Rate Limiting Regeln
3. **WICHTIG:** Rate Limiting sollte **NUR** für `/api/contact` gelten, nicht für `/` oder `/*`
4. Falls eine Regel die Startseite betrifft, füge Googlebot-Ausnahme hinzu

### Schritt 3: IP Access Rules prüfen
1. Gehe zu: **Security** → **WAF** → **Tools** → **IP Access Rules**
2. Prüfe, ob Googlebot IPs blockiert sind
3. Googlebot IPs sollten **nicht** blockiert sein

### Schritt 4: robots.txt prüfen
1. Öffne: `https://www.kost-sicherheitstechnik.de/robots.txt`
2. Stelle sicher, dass es **KEINE** Blockierungen gibt
3. Sollte sein: `User-agent: *` und `Disallow:` (leer)

### Schritt 5: Verifizierung
1. Warte 5-10 Minuten
2. Gehe zu Google Search Console: https://search.google.com/search-console
3. Verwende **URL Inspection Tool**
4. Teste die URL: `https://www.kost-sicherheitstechnik.de/`
5. Klicke auf **"LIVE-TEST"**
6. Die Seite sollte jetzt **200 OK** statt **403** zeigen

## Häufigste Ursache: WAF Custom Rules

**Das häufigste Problem:** Eine WAF Custom Rule blockiert **alle** Requests auf `/` oder `/*`, ohne Googlebot auszunehmen.

**Beispiel einer problematischen Regel:**
```
(http.request.uri.path eq "/") and (cf.client.bot eq true)
Action: Block
```

**Lösung:** Regel ändern zu:
```
(http.request.uri.path eq "/") and 
(cf.client.bot eq true) and 
not (http.user_agent contains "Googlebot")
Action: Block
```

**ODER noch besser:** Regel nur auf `/api/contact` beschränken:
```
(http.request.uri.path eq "/api/contact") and (cf.client.bot eq true)
Action: Block
```

## Warum passiert das?

Auch wenn Googlebot in AI Crawl Control auf "Allow" steht, können **WAF Custom Rules** oder **Rate Limiting Rules** Googlebot trotzdem blockieren, wenn sie nicht korrekt konfiguriert sind.

## Nach der Behebung

1. **Google Search Console:**
   - Verwende "URL Inspection Tool"
   - Klicke auf **"INDEXIERUNG BEANTRAGEN"** für die Startseite
   - Wiederhole für alle wichtigen Seiten

2. **Warte 24-48 Stunden:**
   - Google crawlt die Seiten erneut
   - Die 403-Fehler sollten verschwinden

3. **Prüfe erneut:**
   - Nach 24 Stunden in Google Search Console prüfen
   - Coverage-Bericht sollte sich verbessern

## Notfall-Lösung (Sofort)

Wenn die Seite sofort erreichbar sein muss:

1. **Cloudflare Dashboard** → **Security** → **Bots**
2. **Bot Fight Mode** → **Off** (temporär)
3. Warte 5 Minuten
4. Teste in Google Search Console URL Inspection
5. Wenn es funktioniert, implementiere Option B (Googlebot explizit erlauben)

---

**Status:** ⚠️ KRITISCH - Muss sofort behoben werden, sonst wird die Seite nicht indexiert!

