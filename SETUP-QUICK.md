# 🚀 Quick Setup Checklist

## ✅ Resend API Key (5 Minuten)

1. [ ] Gehe zu https://resend.com
2. [ ] Erstelle Account (mit Google oder E-Mail)
3. [ ] Klicke auf `API Keys` (links im Menü)
4. [ ] Klicke `Create API Key`
5. [ ] Name: `KOST Website`
6. [ ] Kopiere den Key (beginnt mit `re_`)
7. [ ] **WICHTIG:** Key sicher speichern!

## ✅ Cloudflare Environment Variable (3 Minuten)

1. [ ] Gehe zu https://dash.cloudflare.com
2. [ ] Klicke `Workers & Pages` → `Pages`
3. [ ] Klicke auf dein Projekt (`kost`)
4. [ ] Klicke `Settings` Tab
5. [ ] Scrolle zu `Environment Variables`
6. [ ] Klicke `Add variable`
7. [ ] Variable name: `RESEND_API_KEY`
8. [ ] Value: Füge deinen Resend API Key ein
9. [ ] Environment: `Production`
10. [ ] Klicke `Save`

## ✅ Testen (2 Minuten)

1. [ ] Gehe zu `Deployments` Tab
2. [ ] Klicke `Retry deployment` (oder warte auf nächsten Build)
3. [ ] Öffne die Live-Website
4. [ ] Fülle Kontaktformular aus
5. [ ] Klicke "Anfrage senden"
6. [ ] Prüfe E-Mail-Postfächer:
   - [ ] info@kost-sicherheitstechnik.de
   - [ ] info@graphiks.de

**Fertig! 🎉**

---

**Detaillierte Anleitung:** Siehe `SETUP-GUIDE-DETAILED.md`

