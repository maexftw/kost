# Cloudflare Spam-Schutz Optionen - Übersicht

## ✅ Bereits implementiert (im Code)

1. **In-Memory Rate Limiting** - `functions/api/contact.js`
   - Max 3 Anfragen pro 15 Minuten pro IP
   - Resetet bei Function-Neustart (nicht persistent)

2. **Honeypot Field** - Verstecktes Feld im Formular
   - Fängt einfache Bots ab

3. **Enhanced Validation** - Spam-Keyword-Erkennung, URL-Filter
   - Filtert bekannte Spam-Begriffe (inkl. "cloudflare")

4. **Cloudflare Turnstile** - Vorbereitet, benötigt nur Setup
   - Site Key + Secret Key als Environment Variables

---

## 🚀 Einfach hinzufügbar (mit Code-Anpassung)

### Option 1: Cloudflare KV für persistentes Rate Limiting ⭐ EMPFOHLEN

**Vorteile:**
- Persistent auch nach Neustart
- Globale Rate Limits über alle Worker-Instanzen
- Kostenlos im Free Tier (100.000 Reads/Tag, 1.000 Writes/Tag)
- Sehr einfach im Code zu verwenden

**Setup:**
1. Cloudflare Dashboard → Workers & Pages → KV
2. "Create a namespace" → Name: `RATE_LIMIT_KV`
3. Pages Projekt → Settings → Functions → KV Namespace Bindings
4. Variable name: `RATE_LIMIT_KV`, Namespace: `RATE_LIMIT_KV`

**Code-Anpassung:** Ich kann die `checkRateLimit` Funktion in 2 Minuten auf KV umstellen.

---

### Option 2: Cloudflare Access Rules (programmatisch)

**Was es tut:**
- Blockt Requests basierend auf IP, Country, ASN
- Kann im Code über `request.cf` Headers genutzt werden

**Vorteile:**
- Bereits im Request verfügbar
- Kein zusätzliches Setup nötig
- Kann bestimmte Länder/IPs blocken

**Code-Beispiel:**
```javascript
// Prüfen ob Request aus bestimmten Ländern kommt
const country = request.headers.get('CF-IPCountry');
if (country === 'CN' || country === 'RU') { // Beispiel: China, Russland
  return new Response('Blocked', { status: 403 });
}

// Prüfen ob bekanntes Bot
const isBot = request.headers.get('CF-Request-ID');
const userAgent = request.headers.get('User-Agent');
if (isKnownBot(userAgent)) {
  return new Response('Bot blocked', { status: 403 });
}
```

**Einfachheit:** ✅ Sehr einfach - Headers sind bereits verfügbar

---

### Option 3: Cloudflare Firewall Rules (Dashboard, aber einfach)

**Was es tut:**
- Blockt Requests VOR dem Worker (am Edge)
- Schützt auch vor DDoS

**Setup:**
1. Cloudflare Dashboard → Security → WAF → Custom Rules
2. Regel erstellen:
   - **Rule name:** Block Bot User-Agents
   - **Expression:** 
     ```
     (http.request.uri.path eq "/api/contact") and 
     (http.user_agent contains "bot" or http.user_agent contains "crawler" or http.user_agent contains "spider")
     ```
   - **Action:** Block

**Alternative für Spam:**
```
(http.request.uri.path eq "/api/contact") and 
(http.user_agent not contains "Mozilla" and http.user_agent not contains "Chrome" and http.user_agent not contains "Safari" and http.user_agent not contains "Firefox")
```

**Einfachheit:** ⚠️ Dashboard-Konfiguration (kein Code), aber sehr effektiv

---

## 🎯 Dashboard-Optionen (kein Code nötig)

### Option 4: Bot Fight Mode (Free Tier)

**Was es tut:**
- Automatische Bot-Erkennung und Blockierung
- Aktivierung im Dashboard

**Setup:**
1. Cloudflare Dashboard → Security → Bots
2. "Bot Fight Mode" aktivieren
3. Fertig - funktioniert automatisch

**Einfachheit:** ✅✅✅ Sehr einfach - nur Dashboard-Click

**Hinweis:** Kann manchmal auch legitime Bots blockieren (Google Bot, etc.)

---

### Option 5: Super Bot Fight Mode (Paid)

**Was es tut:**
- Erweiterte Bot-Erkennung
- Weniger False Positives als Bot Fight Mode

**Kosten:** Ab $5/Monat (Pro Plan)

**Einfachheit:** ✅✅ Sehr einfach - Dashboard-Aktivierung

---

### Option 6: Rate Limiting Rules (Dashboard)

**Was es tut:**
- Rate Limiting direkt am Edge
- Besser als in-Worker Rate Limiting (schont Worker-CPU)

**Setup:**
1. Cloudflare Dashboard → Security → WAF → Rate limiting rules
2. Regel erstellen:
   - **Rule name:** Contact Form Rate Limit
   - **Match:** `http.request.uri.path eq "/api/contact"`
   - **Threshold:** 5 requests per 1 minute
   - **Action:** Block

**Einfachheit:** ⚠️ Dashboard-Konfiguration

**Vorteil:** Blockt VOR dem Worker (spart Ressourcen)

---

## 📊 Empfehlung nach Einfachheit

### Sehr einfach (sofort umsetzbar):

1. **Bot Fight Mode** - Dashboard-Click ✅
2. **Cloudflare KV Rate Limiting** - 2 Minuten Code-Anpassung ✅
3. **Access Rules im Code** - Headers bereits vorhanden ✅

### Mittel (Dashboard-Konfiguration):

4. **Firewall Rules** - Dashboard, aber sehr effektiv ⚠️
5. **Rate Limiting Rules** - Dashboard, schont Worker-Ressourcen ⚠️

### Optional (Paid):

6. **Super Bot Fight Mode** - Wenn Budget vorhanden, sehr gut

---

## 💡 Meine Empfehlung für dich

**Phase 1 (Jetzt - kostenlos):**
1. ✅ Turnstile aktivieren (Site Key + Secret Key setzen)
2. ✅ Cloudflare KV für Rate Limiting hinzufügen (2 Min Code)
3. ✅ Bot Fight Mode im Dashboard aktivieren

**Phase 2 (Optional - wenn noch mehr Spam kommt):**
4. Firewall Rule für bekannte Bot User-Agents
5. Rate Limiting Rule am Edge (schont Worker)

**Soll ich dir Option 1 (Cloudflare KV) direkt implementieren?** 
Das ist die einfachste Verbesserung mit 2 Minuten Code-Anpassung.

