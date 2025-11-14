# Cloudflare KV Setup für Rate Limiting

## Schritt-für-Schritt Anleitung

### 1. KV Namespace erstellen

1. Gehe zu **Cloudflare Dashboard**: https://dash.cloudflare.com
2. Klicke auf **"Workers & Pages"** (links im Menü)
3. Klicke auf **"KV"** Tab
4. Klicke auf **"Create a namespace"**
5. **Name:** `RATE_LIMIT_KV`
6. Klicke **"Add"**

### 2. KV Namespace an Pages Projekt binden

1. Gehe zu **"Workers & Pages"** → **"Pages"**
2. Klicke auf dein Projekt (**"kost"** oder wie es heißt)
3. Klicke auf **"Settings"** Tab
4. Scrolle zu **"Functions"** Sektion
5. Klicke auf **"KV Namespace Bindings"**
6. Klicke **"Add binding"**
7. **Variable name:** `RATE_LIMIT_KV` (genau so, mit Großbuchstaben!)
8. **KV namespace:** Wähle `RATE_LIMIT_KV` aus der Liste
9. Klicke **"Save"**

### 3. Deployment triggern

1. Gehe zu **"Deployments"** Tab
2. Klicke **"Retry deployment"** beim letzten Build
3. Oder warte auf den nächsten automatischen Build (bei Git Push)

### 4. Testen

Nach dem Deployment:
- Rate Limiting funktioniert jetzt persistent
- Auch nach Worker-Neustart bleiben Limits erhalten
- Max 3 Anfragen pro 15 Minuten pro IP

## ✅ Fertig!

Das Rate Limiting verwendet jetzt Cloudflare KV und ist persistent.

**Hinweis:** Falls KV nicht konfiguriert ist, fällt der Code automatisch auf In-Memory Rate Limiting zurück (funktioniert auch, aber nicht persistent).

