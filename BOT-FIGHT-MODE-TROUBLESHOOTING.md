# Bot Fight Mode Troubleshooting

## Warum Bot Fight Mode möglicherweise nicht greift

Bot Fight Mode blockt **nur bekannte Bot-User-Agents**, nicht alle automatisierten Requests. Viele Spam-Bots verwenden gefälschte Browser-User-Agents und werden daher nicht erkannt.

### Was Bot Fight Mode blockt:
- ✅ Bekannte Crawler (Googlebot, Bingbot, etc.) - aber diese werden oft erlaubt
- ✅ Bekannte Spam-Bots mit offensichtlichen Bot-User-Agents
- ✅ Requests ohne User-Agent Header

### Was Bot Fight Mode NICHT blockt:
- ❌ Bots mit gefälschten Browser-User-Agents (z.B. "Mozilla/5.0...")
- ❌ Bots die sich als normale Browser ausgeben
- ❌ Automatisierte Form-Submissions mit Browser-ähnlichen Headers

## Lösung: Mehrschichtiger Schutz

Da Bot Fight Mode allein nicht ausreicht, haben wir mehrere Schutzebenen:

### 1. ✅ Bot Fight Mode (Dashboard)
- Aktiviert im Dashboard
- Blockt offensichtliche Bots

### 2. ✅ Cloudflare KV Rate Limiting (Code)
- Max 3 Anfragen pro 15 Minuten pro IP
- Funktioniert auch wenn Bot Fight Mode versagt
- **Setup:** Siehe `CLOUDFLARE-KV-SETUP.md`

### 3. ✅ Honeypot Field (Code)
- Verstecktes Feld im Formular
- Fängt einfache Bots ab

### 4. ✅ Enhanced Validation (Code)
- Spam-Keyword-Erkennung
- URL-Filter
- Längenprüfung

### 5. ✅ Cloudflare Turnstile (Optional)
- Moderne CAPTCHA-Alternative
- Sehr effektiv gegen Bots
- **Setup:** Siehe `CONTACT-FORM-SETUP.md`

## Prüfen ob Bot Fight Mode aktiv ist

1. Cloudflare Dashboard → Security → Bots
2. Prüfe ob "Bot Fight Mode" auf "On" steht
3. Prüfe "Analytics" Tab für Bot-Statistiken

## Zusätzliche Optionen wenn Bot Fight Mode nicht ausreicht

### Option A: Firewall Rule für fehlende/verdächtige User-Agents

**Dashboard:** Security → WAF → Custom Rules

**Rule:**
```
(http.request.uri.path eq "/api/contact") and 
(http.user_agent eq "" or not http.user_agent contains "Mozilla" or not http.user_agent contains "Chrome" or not http.user_agent contains "Safari" or not http.user_agent contains "Firefox" or not http.user_agent contains "Edge")
```

**Action:** Block

### Option B: Rate Limiting Rule am Edge

**Dashboard:** Security → WAF → Rate limiting rules

**Rule:**
- Match: `http.request.uri.path eq "/api/contact"`
- Threshold: 5 requests per 1 minute
- Action: Block

**Vorteil:** Blockt VOR dem Worker (spart Ressourcen)

### Option C: Turnstile aktivieren (Empfohlen)

Turnstile ist die beste Lösung gegen Spam-Bots:
- Sehr effektiv
- Privacy-freundlich (keine Cookies)
- Kostenlos
- Unsichtbar für die meisten User

**Setup:** Siehe `CONTACT-FORM-SETUP.md` Abschnitt "3b. Cloudflare Turnstile Setup"

## Empfehlung

**Aktuell aktiv:**
1. ✅ Bot Fight Mode (Dashboard)
2. ✅ KV Rate Limiting (Code - nach Setup)
3. ✅ Honeypot + Validation (Code)

**Nächster Schritt:**
- **Turnstile aktivieren** - Das ist die effektivste Lösung gegen Spam-Bots

Die Kombination aus allen Schutzebenen sollte den meisten Spam abfangen.

