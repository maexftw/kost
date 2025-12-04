# Website Handover: kost-sicherheitstechnik.de

**Datum:** Dezember 2024
**Von:** Maxi
**An:** Moritz

---

## 🤝 Was wird übergeben?

Mit diesem Handover erhältst du die vollständige Kontrolle über die Website **kost-sicherheitstechnik.de**:

| Komponente | Beschreibung |
|------------|--------------|
| **GitHub Repository** | Quellcode der gesamten Website |
| **Cloudflare Pages** | Hosting & automatisches Deployment |
| **Domain** | kost-sicherheitstechnik.de |

---

## ⚠️ Wichtig: Verantwortungsübergang

**Ab dem Moment, in dem du dieses Repository übernimmst, liegt die Verantwortung für die Website bei dir.**

Das bedeutet:
- Du bist verantwortlich für Änderungen und deren Auswirkungen
- Du bist verantwortlich für Backups
- Du bist verantwortlich für die Wartung

**Support von mir:**
- Bei Fragen kannst du dich gerne melden
- Ich helfe, wenn ich Zeit habe – aber ohne Garantie auf sofortige Reaktion
- Für dringende Produktionsprobleme solltest du einen eigenen Plan haben

---

## 🚀 So funktioniert das Deployment

Die Website nutzt **Cloudflare Pages** mit automatischem Deployment:

```
Du änderst Code → Push zu GitHub → Cloudflare baut automatisch → Website ist live
```

Das Prinzip ist immer gleich – egal welches Tool du nutzt.

---

## 🛠️ Wie du Änderungen machen kannst

Du hast mehrere Optionen, je nachdem womit du dich wohlfühlst:

### Option A: Klassisch mit Git (für Git-Erfahrene)

Wenn du Git schon kennst, einfach wie gewohnt:

```bash
git clone https://github.com/maexftw/kost.git
cd kost
# Dateien bearbeiten...
git add . && git commit -m "Beschreibung" && git push
```

### Option B: Mit einer IDE wie Cursor oder VS Code (Empfehlung)

**Cursor** (https://cursor.sh) oder **VS Code** bieten:
- Visuelles Interface für Git (kein Terminal nötig)
- Syntax-Highlighting für HTML/CSS
- Live-Preview möglich
- Eingebaute KI-Unterstützung (besonders Cursor)

**Workflow mit Cursor/VS Code:**
1. Repo klonen (einmalig): `git clone https://github.com/maexftw/kost.git`
2. Ordner in Cursor/VS Code öffnen
3. Dateien bearbeiten
4. Im Source Control Panel: Stage → Commit → Push (alles per Klick)

### Option C: AI-unterstützt arbeiten

Du kannst KI-Tools nutzen, die dir beim Bearbeiten helfen:

| Tool | Beschreibung |
|------|--------------|
| **Cursor** | IDE mit eingebauter KI – kann Code erklären, ändern, generieren |
| **Claude Code** | Anthropics CLI-Tool – arbeitet direkt im Terminal |
| **ChatGPT / Claude** | Code-Snippets generieren lassen, dann manuell einfügen |
| **GitHub Copilot** | KI-Autocomplete in VS Code |

**Beispiel mit Cursor:**
- Öffne eine HTML-Datei
- Drücke `Cmd+K` (Mac) oder `Ctrl+K` (Windows)
- Schreibe: "Ändere die Telefonnummer zu 0231 98983-51"
- Cursor macht die Änderung für dich

### Option D: Direkt auf GitHub (für kleine Änderungen)

Für schnelle Text-Änderungen kannst du auch direkt auf GitHub editieren:
1. Gehe zu https://github.com/maexftw/kost
2. Navigiere zur Datei
3. Klick auf den Stift (Edit)
4. Änderung machen → "Commit changes"

⚠️ Nur für kleine Änderungen empfohlen – kein Preview, keine Syntax-Prüfung.

---

**Meine Empfehlung:** Starte mit **Cursor**. Falls du Hilfe beim Einrichten brauchst, melde dich.

---

## 📁 Projekt-Struktur

```
kost-repo/
├── index.html              # Startseite
├── pages/                  # Unterseiten
│   ├── alarmanlagen.html
│   ├── videoueberwachung.html
│   ├── zutrittskontrolle.html
│   ├── mechanische-sicherung.html
│   ├── briefkasten.html
│   ├── fussballmuseum.html
│   ├── impressum.html
│   └── datenschutz.html
├── css/                    # Stylesheets
├── images/                 # Bilder & Logos
├── functions/              # Cloudflare Functions (Kontaktformular)
└── robots.txt, sitemap.xml # SEO
```

---

## 💾 Backups anlegen

### Option 1: Git ist dein Backup
Jeder Commit ist ein Snapshot. Du kannst jederzeit zu einem früheren Stand zurück:

```bash
# Alle Commits anzeigen
git log --oneline

# Zu einem bestimmten Commit zurück (VORSICHT: überschreibt aktuelle Änderungen)
git checkout <commit-hash>

# Zurück zum neuesten Stand
git checkout main
```

### Option 2: Manuelles Backup
Regelmäßig das komplette Repo als ZIP herunterladen:
- GitHub → Repository → Code → Download ZIP

### Option 3: Fork als Sicherheitskopie
Erstelle einen Fork des Repos in deinem eigenen GitHub-Account als zusätzliche Sicherung.

**Empfehlung:** Vor größeren Änderungen immer einen neuen Branch erstellen:
```bash
git checkout -b meine-aenderung
# Änderungen machen...
git push -u origin meine-aenderung
# Wenn alles funktioniert: Pull Request oder direkt mergen
```

---

## 🔧 Häufige Aufgaben

### Text ändern
1. HTML-Datei öffnen (z.B. `index.html`)
2. Text finden und ändern
3. Speichern, committen, pushen

### Bild austauschen
1. Neues Bild in `images/` legen (gleicher Dateiname = automatisch ersetzt)
2. Oder: neuen Dateinamen in HTML referenzieren
3. Committen, pushen

### Neue Seite erstellen
1. Bestehende Seite kopieren (z.B. `pages/alarmanlagen.html`)
2. Inhalt anpassen
3. In Navigation verlinken (in `index.html` und anderen Seiten)
4. Committen, pushen

---

## 🌐 Cloudflare-Zugang

Die Website läuft auf Cloudflare Pages. Falls du Zugang zum Dashboard brauchst (DNS, SSL, Analytics), melde dich bei mir – dann übertrage ich das separat.

**Was Cloudflare automatisch macht:**
- SSL/HTTPS
- CDN (weltweites Caching)
- DDoS-Schutz
- Automatisches Deployment bei Git-Push

---

## 🆘 Wenn etwas kaputt geht

1. **Ruhe bewahren** – Git hat alles gespeichert
2. **Letzten funktionierenden Commit finden:** `git log --oneline`
3. **Zurücksetzen:**
   ```bash
   git revert HEAD  # Letzten Commit rückgängig machen (sicher)
   # oder
   git reset --hard <commit-hash>  # Komplett zurück (überschreibt alles)
   ```
4. **Pushen:** `git push` (bei reset evtl. `git push --force` nötig)

---

## 📞 Kontakt bei Fragen

Du kannst dich bei mir melden, wenn du Fragen hast. Bitte versteh, dass ich nicht immer sofort verfügbar bin und keine Garantie für Support geben kann.

Für den Alltag empfehle ich:
- Google / Stack Overflow für HTML/CSS-Fragen
- GitHub Docs für Git-Fragen
- Cloudflare Docs für Hosting-Fragen

---

## ✅ Nächste Schritte

1. [ ] Du bestätigst, dass du die Verantwortung übernimmst
2. [ ] Ich lade dich als Collaborator ein (brauche deinen GitHub-Username)
3. [ ] Du klonst das Repo lokal: `git clone https://github.com/maexftw/kost.git`
4. [ ] Optional: Cloudflare-Zugang übertragen

---

**Fragen? Melde dich einfach. Viel Erfolg mit der Website!**
