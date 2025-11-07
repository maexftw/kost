# DNS Setup Status - kost-sicherheitstechnik.de

## ✅ Was bereits korrekt ist:
- MX Record: DNS only ✓
- SPF TXT: DNS only ✓  
- MS TXT: DNS only ✓

## ⚠️ Was noch zu tun ist:

### 1. autodiscover CNAME: Proxy auf "DNS only" ändern
- Aktuell: Proxied
- Soll: DNS only
- **Aktion:** Edit → Proxy-Status deaktivieren → Save

### 2. A/AAAA Records: Proxy auf "DNS only" ändern
- A Record (*): Proxied → DNS only
- A Record (kost-sicherheitstechnik.de): Proxied → DNS only  
- AAAA Record: Proxied → DNS only
- **Hinweis:** Diese können auch gelöscht werden, wenn Cloudflare Pages verwendet wird

### 3. NS Records löschen
- ns5.kasserver.com → löschen
- ns6.kasserver.com → löschen
- **Grund:** Werden durch Cloudflare Nameserver ersetzt

### 4. DKIM Record hinzufügen
- **Type:** TXT
- **Name:** `kas202508221135._domainkey`
- **Content:** `v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuieW7oxkjto1ATvJGJ2cqmMipnhMuxMG8MKTMGkqU4tgXrlR63PyNjnXChzm++nqdt0NHoplpmUaOFhfBRQGyHDuQukwObX/3fICtOWsuk1aucgvZw7agZXLjhoqlYzQb2Ni3xHO4dKkP5vBSMd8SbsU/4OgoRxbxmofZbobRBJtkOC9yQs866OqloxxPgVp1E+6oQ2eSKxyxP+Kua5RpH7DNtp8XBxczc+JzOA1HaqArFkCn1no8NSb+HnjGyr2ripFUo3pheQnCGrgEqOCgMsBSh54n7sW5/qQdi0avG8kPG+4SNJPZinLSz6exbwqs+wEhdPh3AD30SBE9fBKcQIDAQAB`
- **Proxy:** DNS only

### 5. Nameserver bei all-incl ändern
- **Alte Nameserver löschen:**
  - ns5.kasserver.com
  - ns6.kasserver.com
- **Neue Nameserver hinzufügen:**
  - may.ns.cloudflare.com
  - vern.ns.cloudflare.com

## Cloudflare Nameserver:
- may.ns.cloudflare.com
- vern.ns.cloudflare.com

