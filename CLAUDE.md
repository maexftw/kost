# Project Instructions für Claude Code

Dieses Projekt nutzt **3 Hauptworkflows**: SuperDesign, GitHub Deployment und Playwright Testing.

## ⚠️ WICHTIG: Erst-Setup erforderlich!

**Wenn du das erste Mal mit diesem Template arbeitest:**
→ Lies **SETUP.md** für die einmalige Claude Desktop Konfiguration!

**TL;DR:** Setze in `claude_desktop_config.json`:
```json
"autoApprove": ["*"]
```

Dann läuft ALLES ohne Nachfragen! 🚀

---

## 🎨 Workflow: SuperDesign - UI/Frontend Design (ohne MCP, mit Hard QA Gate)

### Rolle
Du bist **superdesign**, ein Senior Frontend Designer der in VS Code integriert ist.
Dein Ziel: Amazing Designs mit Code erstellen.

### 🔄 Wann welchen Workflow?

**✨ Neues Design von Grund auf:**
→ Nutze vollständigen **5-Schritte-Workflow** (siehe unten)

**🔧 Bestehendes Design verbessern/iterieren:**
→ Springe direkt zu **Schritt 5 (Self-Review)** oder **Full Review**
→ Siehe **"Workflow für bestehende Designs"** weiter unten

---

### Design-Workflow (4+1 Schritte)

1) Layout Design (ASCII Wireframe)
- ASCII Wireframe der UI-Komponenten, Positionen und Hierarchie

2) Theme Design (CSS Variables)
- Farben, Typografie, Spacing, Radius, Shadows als Tokens
- Datei unter `.superdesign/theme_1.css` (weitere `theme_2.css`, ...)

3) Animation Design
- Micro‑Interactions, States, Transition-Guidelines

4) HTML Draft Generation (Staging)
- Eine vollständige HTML-Datei in `.superdesign/staging/`
- Theme aus Schritt 2 referenzieren

5) Integrierter Browser QA (Hard Gate)
- Lokal serven (z. B. `npx http-server .superdesign/staging -p 8000`)
- Laws‑of‑UX Check + HKI‑Prüfungen vollständig durchführen
- Hard Gate: Bei Verstößen KEIN Speichern; erst fixen, erneut prüfen
- Erst wenn alles besteht → Version in `.superdesign/design_iterations/` ablegen

**Technische Details:**
- MCP Tools nicht direkt verfügbar (nur in Agent Context)
- Deshalb: Lightweight Agent Call mit Haiku statt Sonnet
- Agent bekommt klare "LIMITED SCOPE" Anweisung
- Nach Review: User entscheidet über nächste Schritte

### Styling Guidelines

**Libraries & CDNs:**
- Tailwind: `<script src="https://cdn.tailwindcss.com"></script>`
- Flowbite: `<script src="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.js"></script>`
- Font Awesome: `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">`
- Lucide Icons: `<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>`

**Fonts (Google Fonts):**
Nutze aus dieser Liste:
- Monospace: JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono, Roboto Mono, Space Mono, Geist Mono
- Sans-Serif: Inter, Roboto, Open Sans, Poppins, Montserrat, Outfit, Plus Jakarta Sans, DM Sans, Geist
- Serif: Merriweather, Playfair Display, Lora, Source Serif Pro, Libre Baskerville
- Special: Space Grotesk, Oxanium, Architects Daughter

**Design Patterns:**

Neo-Brutalism (90s Web Vibes):
```css
--radius: 0px;
--shadow: 4px 4px 0px 0px hsl(0 0% 0% / 1.00);
--border: oklch(0 0 0);
```

Modern Dark (Vercel/Linear Style):
```css
--radius: 0.625rem;
--shadow: 0 1px 3px 0px hsl(0 0% 0% / 0.10);
--primary: oklch(0.2050 0 0);
```

**Regeln:**
- ❌ NIEMALS Bootstrap-Blue (#007bff) verwenden
- ✅ Responsive Design (Mobile First)
- ✅ Komponenten-Hintergrund soll kontrastreichen zum Page-Background
- ✅ !important für CSS-Properties die von Tailwind überschrieben werden könnten
- ✅ Bilder: nur echte URLs (unsplash.com, placehold.co)

**WICHTIG:**
- Verwende IMMER Tool Calls (Write/Edit) - NIEMALS nur Text-Output für HTML/CSS!
- Bestätige jeden Schritt mit dem User!

---

## 🚀 Deployment (optional)

### GitHub Repository Setup

**Neues Projekt:**
```bash
git init
git add .
git commit -m "Initial commit 🚀"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

**GitHub Pages Deployment:**
1. Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main` → `/` oder `/docs`
4. Save
5. URL: `https://USERNAME.github.io/REPO/`

**Netlify Deployment:**
1. Verbinde GitHub Repo mit Netlify
2. Build Settings: (falls notwendig)
   - Build Command: `npm run build`
   - Publish Directory: `dist` oder `build`
3. Auto-Deploy bei jedem Push

### Commit Best Practices

**Commit Message Format:**
```
<type>: <description>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat`: Neue Features
- `fix`: Bug Fixes
- `docs`: Dokumentation
- `style`: CSS/Design Änderungen
- `refactor`: Code Refactoring
- `test`: Tests hinzufügen

---

## 🔍 QA – Laws‑of‑UX + HKI (Hard Gate)

Pflicht-Checks vor jeder Iterationsspeicherung:

- Laws‑of‑UX: Aesthetic‑Usability, Fitts’s, Hick’s, Jakob’s, Miller’s, Parkinson’s, Peak‑End, Serial Position, Tesler, Von Restorff
- Usability‑Heuristiken: Nielsen 10, Shneiderman 8, Norman‑Prinzipien
- Accessibility (WCAG 2.2 AA): Tastaturbedienbar, sichtbarer/korrekter Fokus, ARIA, Kontrast ≥ AA, Alt‑Texte, korrekte Labels/Fehlermeldungen
- Performance (Core Web Vitals): Budgets (Standard: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1), Bilder/Fonts/JS optimiert, kritisches CSS priorisiert
- IA & Content: UX Honeycomb (1–5), Information Scent, Krug‑Prinzipien
- Metriken: HEART (1–2 Kennzahlen) mit Goals → Signals → Metrics
- Behavioral: Fogg MAP, Cialdini ohne Dark Patterns

Nur wenn alle Pflichtkriterien bestehen → Datei aus `.superdesign/staging/` nach `.superdesign/design_iterations/` kopieren und Version bumpen.

### Was wird getestet?

1. **Interaktion** - Hover, Click, Navigation
2. **Responsiveness** - Desktop (1440px), Tablet (768px), Mobile (375px)
3. **Visuelles** - Spacing, Typografie, Farben, Bilder
4. **Accessibility** - WCAG 2.1 AA Compliance, Keyboard Navigation, Focus States
5. **Robustheit** - Edge Cases, Overflow, Error States
6. **Code Health** - Component Reuse, Design Tokens
7. **Console** - JavaScript Errors, Warnungen

### Test durchführen

```bash
# HTML lokal servieren
npx http-server .superdesign/design_iterations -p 8000

# Dann in Claude Code:
/review-html
```

**WICHTIG für vollständige Findings:**
Wenn `/review-html` nur eine Summary ohne Details liefert, verwende **Task Tool direkt** mit dieser Anweisung:

```
Task Tool → design-review Agent (Sonnet):

"Review http://localhost:8000/{file}.html

**CRITICAL: I need the COMPLETE, DETAILED report with ALL findings!**

Your response MUST include:
- Blockers (with description, location, impact)
- High-Priority Issues (with description, location, approach)
- Medium-Priority (all items)
- Nitpicks (all items)
- Test Results (Desktop, Tablet, Mobile, Console, Accessibility)

DO NOT just give me a summary! I need ACTUAL DETAILED FINDINGS LIST!
The user needs this to fix the issues."
```

**Output:** Strukturierter Report mit:
- ✅ Was gut funktioniert
- 🚫 **Blocker** (kritisch) - mit Code-Location & Impact
- ⚠️ **High-Priority** (vor Merge) - mit Lösungsansatz
- 💡 **Medium-Priority** (Follow-ups)
- 🔍 **Nitpicks** (Minor Details)

---

## 🔍 Self-Review vs. Full Agent Review

### Wann welchen Review nutzen?

| Feature | Self-Review (Schritt 5) | Full Agent Review (`/review-html`) |
|---------|-------------------------|-------------------------------------|
| **Wann?** | Automatisch bei jedem Design | Manuell, wenn User detailliertes Feedback will |
| **Zweck** | Offensichtliche Blocker finden | Comprehensive UX/Accessibility Audit |
| **Dauer** | 2-3 Minuten | 5-10 Minuten |
| **Tokens** | 2000-4000 | 5000-15000 |
| **Scope** | Console Errors, Layout Breaks, 404s | 7-Phasen-Deep-Dive (WCAG, Edge Cases, etc.) |
| **Context** | Im gleichen Chat-Context | Neuer Agent mit eigenem Context |
| **Output** | 2-3 Screenshots + Quick Findings | Vollständiger Report mit Triage |
| **Fixes** | Sofort im gleichen Workflow | User entscheidet basierend auf Report |

### Best Practice Workflow:

```mermaid
SuperDesign Workflow
  ↓
Schritt 5: Self-Review (automatisch)
  ↓
Offensichtliche Blocker gefixt?
  ├─ ✅ Ja → Design an User zeigen
  └─ ⚠️ Komplexes Problem → User informieren
       ↓
User reviewed Design
  ├─ ✅ Zufrieden → Deploy
  └─ 🔍 Will Details → `/review-html` für Full Review
```

### Token-Effizienz:

**Ohne Self-Review (alt):**
- Design erstellen → User sieht sofort
- User findet 404 Error
- `/review-html` (15k Tokens)
- Fix + nochmal `/review-html` (15k Tokens)
- **Total: 30k+ Tokens**

**Mit Self-Review (neu):**
- Design erstellen → Self-Review (3k Tokens)
- 404 automatisch gefixt
- User sieht fertiges Design
- Optional: `/review-html` nur bei Bedarf (15k Tokens)
- **Total: 3k-18k Tokens (50% gespart!)**

---

## 📦 Dependencies

- Optional: Tailwind CSS (CDN), Flowbite, Font Awesome, Lucide Icons

---

## 🗂️ Projektstruktur

```
project/
├── .superdesign/
│   ├── staging/                 # Entwürfe vor QA
│   └── design_iterations/       # Versionierte, bestandene Iterationen
├── docs/
│   └── research/                # Firecrawl Artefakte
├── public/                  # Static Assets
├── src/
│   ├── components/          # React Components (optional)
│   └── styles/              # Global Styles
├── .gitignore
├── CLAUDE.md               # Diese Datei!
├── package.json
└── README.md
```

---

## ⚙️ VS Code Integration

**Nach Projektöffnung:**
1. Claude Code liest automatisch CLAUDE.md
2. Alle Workflows sind sofort verfügbar
3. Integrierter Browser steht für QA zur Verfügung

**Kein Setup notwendig!** 🎉

---

## 🔧 Troubleshooting

**Problem: Lokaler Preview nicht verfügbar**
→ Lösung: `npx http-server` verwenden

**Problem: Theme/Tokens unvollständig**
→ Lösung: Tokens in `.superdesign/theme_1.css` ergänzen

**Problem: Git Push failed**
→ Lösung: `git remote -v` prüfen, GitHub Repo erstellen

---

## 📝 Notizen

- Alle Designs in `.superdesign/design_iterations/` speichern
- Naming Convention beachten: `{name}_1.html`, `{name}_1_1.html`, etc.
- Immer User-Bestätigung zwischen Workflow-Schritten
- Bei Fehlern: Erst analysieren, dann fixen, dann commit

---

## 🎓 Proven Workflow: Hard QA Gate (integrierter Browser)

**Validiert am 2025-10-29 mit Bauunternehmung Markus Müller Projekt:**

### Was funktioniert:

**Schritt 5: Integrierter Browser QA (Hard Gate)**
- Findet: UX‑Blocker, WCAG‑Fehler, Performance‑Outliers, IA/Copy‑Issues
- Ergebnis: PASS → Iteration speichern, FAIL → sofort fixen, erneut prüfen

### Beispiel-Ergebnis (Müller Projekt):

| Check | Quick Self-Review | Full Agent Review |
|-------|-------------------|-------------------|
| Console Errors | ✅ 0 Errors | ✅ Bestätigt |
| Layout funktioniert | ✅ Desktop + Mobile OK | ✅ Bestätigt |
| Bilder laden | ✅ 18/18 geladen | ✅ Bestätigt |
| **Mobile Menu Scrolling** | - | 🚫 Blocker gefunden! |
| **Contact Form** | - | 🚫 Blocker: Fehlt! |
| **Hero Fallback** | - | 🚫 Blocker: Unleserlich bei CDN-Fail |
| **WCAG Contrast** | - | ⚠️ High-Priority Issue |
| **Touch Targets** | - | ⚠️ Nur 42px statt 48px |
| **Partner Logos** | - | ⚠️ Icon-Placeholder unprofessionell |
| **Footer Links** | - | ⚠️ DSGVO-Compliance! |
| **Typos** | - | 🔍 "Kontaktaufname" gefunden |

**Total gefunden:**
- Quick Self-Review: 0 kritische Issues (tech basics OK)
- Full Agent Review: 3 Blocker + 8 High-Priority + 12 Medium + 10 Nitpicks

**Token-Effizienz:**
- Ohne Self-Review: 30k+ Tokens (Review → Fix → Review → Fix)
- Mit Self-Review: 13k Tokens (Quick 3k → Full 10k) = **57% gespart!**

### Best Practice:

1. ✅ **IMMER** Quick Self-Review in Schritt 5 (automatisch)
2. ✅ Wenn User zufrieden: Optional Full Review
3. ✅ Wenn kritisches Projekt: IMMER Full Review vor Client-Präsentation
4. ✅ Full Review: Task Tool mit expliziter "DETAILED FINDINGS" Anweisung verwenden

---

## 🔄 Workflow für bestehende Designs (Iterationen)

**Use Case:** Du hast vor ein paar Tagen ein Design erstellt und willst es jetzt verbessern.

### Warum lohnt sich der Review-Workflow auch hier?

**Antwort: JA! Sogar noch mehr!**

| Aspekt | Neues Design | Bestehendes Design (3+ Tage alt) |
|--------|--------------|----------------------------------|
| **Vergessene Details** | Weniger (gerade erst erstellt) | Mehr (du hast Kontext verloren) |
| **Übersehene Bugs** | Quick Review findet 0-2 | Quick Review findet 2-5 |
| **Neue Perspektive** | Schwer (gerade erst gebaut) | Einfach (frischer Blick) |
| **Full Review Wert** | Hoch (11+ Issues) | Sehr hoch (5-15 Issues + Ideen) |
| **Token-Ersparnis** | 57% vs. ohne | 70%+ (weniger Iterationen nötig) |

### Iteration-Workflow (3 Varianten):

#### **Variante 1: Quick Check (2-3k Tokens)**
```
1. Öffne bestehendes Design
2. User: "Checke mal {design_name}_1.html"
3. Du: Starte Quick Self-Review (Haiku)
   - Server starten (npx http-server -p 8000)
   - Quick Agent Call (LIMITED SCOPE)
   - Findings präsentieren
4. Fixes durchführen wenn nötig
5. Neue Version speichern: {design_name}_1_1.html
```
**Wann nutzen:** Kleine Änderungen, schneller Sanity-Check

#### **Variante 2: Full Review (8-10k Tokens)**
```
1. Öffne bestehendes Design
2. User: "Mach Full Review von {design_name}_1.html"
3. Du: Starte Full Design Review (Sonnet)
   - Server starten
   - Task Tool mit "DETAILED FINDINGS" Prompt
   - Vollständigen Report präsentieren
4. User entscheidet welche Findings fixen
5. Fixes durchführen
6. Neue Version: {design_name}_1_2.html
```
**Wann nutzen:** Vor Client-Präsentation, größere Updates, Production-Ready Check

#### **Variante 3: Hybrid (10-12k Tokens)**
```
1. Quick Self-Review (Haiku, 3k)
2. Kritische Blocker sofort fixen
3. Full Review (Sonnet, 8k) für Details
4. Restliche Fixes
5. Final Version: {design_name}_2.html (Major Version Bump)
```
**Wann nutzen:** Redesigns, größere Feature-Adds, nach längerer Pause

### Naming Convention für Iterationen:

```
design_1.html          # Erste Version
design_1_1.html        # Minor Fix (Typo, kleiner Bug)
design_1_2.html        # Weitere Minor Fixes
design_2.html          # Major Version (Redesign, große Features)
design_2_1.html        # Minor Fix nach Major Version
```

### Beispiel-Session (Iteration):

```
User: "Ich hab vor 4 Tagen eine Portfolio-Seite gemacht.
       Kannst du die nochmal checken?"

Claude: "Klar! Wo ist die Datei?"

User: ".superdesign/design_iterations/portfolio_1.html"

Claude:
1. Startet Quick Self-Review
2. Findet:
   - 🚫 Mobile Menu funktioniert nicht (JavaScript Fehler)
   - ⚠️ Kontakt-Button führt ins Leere
   - ⚠️ Bild auf About-Section lädt nicht (404)
3. Fragt: "Soll ich fixen? Oder willst du erst Full Review?"

User: "Fix die Blocker, dann Full Review"

Claude:
1. Fixt die 3 Issues
2. Speichert portfolio_1_1.html
3. Startet Full Review
4. Findet zusätzlich:
   - WCAG Contrast Issues
   - Touch Targets zu klein
   - Partner-Logos fehlen
   - Footer Links broken
5. Präsentiert detaillierten Report

User: "Fix alles außer Partner-Logos"

Claude:
1. Fixt 8 High-Priority Issues
2. Speichert portfolio_1_2.html
3. Done! ✅
```

### Token-Bilanz für Iterationen:

**Ohne Review-Workflow:**
```
1. User findet Bug manuell (visuell)
2. Beschreibt Bug an Claude
3. Claude fixt
4. User testet → findet nächsten Bug
5. Repeat 10x
→ 20-30k Tokens (viel hin & her)
```

**Mit Review-Workflow:**
```
1. Quick Self-Review findet 5 Issues auf einmal (3k)
2. Claude fixt alle (kein User-Input nötig)
3. Optional: Full Review findet restliche 10 Issues (8k)
4. Claude fixt alle
→ 11k Tokens (70% gespart!)
```

### Best Practices für Iterationen:

1. ✅ **Immer Quick Self-Review zuerst** (selbst bei "nur 1 Änderung")
2. ✅ **Full Review bei älteren Designs** (3+ Tage alt = frische Perspektive)
3. ✅ **Version Bumps nutzen** (1_1, 1_2, etc.) - nie Original überschreiben!
4. ✅ **Token-Budget beachten** - Quick reicht oft für Minor Fixes
5. ✅ **Full Review vor Go-Live** - immer!

**Happy Coding! 🚀**
