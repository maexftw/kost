# 🎨 SuperDesign Template

**Professional Frontend Design Workflow mit integriertem Browser‑QA (ohne MCP)**

Ein vollständig integriertes Template, das production‑ready UI/UX Designs ermöglicht – mit Hard‑Gate QA vor jeder Iteration.

---

## 🚀 Quick Start

### 1. Template in neues Projekt kopieren

```bash
# Kopiere diesen Ordner in dein neues Projekt
cp -r "I:/Ai Claude/SuperDesign-Template" "/path/to/your/new-project"

# Oder: Nutze diesen Ordner direkt als Projekt-Basis
```

### 2. In VS Code öffnen

```bash
code "/path/to/your/new-project"
```

### 3. Cursor/Claude Code starten

- Öffne Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
- Starte Chat mit Claude
- Claude liest automatisch `CLAUDE.md` und ist ready! ✅

---

## 📋 Was ist enthalten?

```
SuperDesign-Template/
├── .superdesign/
│   ├── staging/                      # Drafts vor QA
│   └── design_iterations/            # Versionierte, bestandene Designs
├── docs/
│   └── research/                     # Firecrawl Artefakte
├── CLAUDE.md                         # Vollständige Workflow-Anleitung
└── README.md                         # Diese Datei
```

---

## 🎯 Workflows

### 🆕 Neues Design erstellen

**SuperDesign Workflow:**

1. ASCII Wireframe (Layout)
2. Theme CSS (Design Tokens)
3. Animation Design (Micro‑Interactions)
4. HTML Draft (in `.superdesign/staging/`)
5. Integrierter Browser QA – Laws‑of‑UX + HKI (Hard Gate). Bei Verstoß: fixen und erneut prüfen. Erst bei PASS nach `.superdesign/design_iterations/` speichern.

**User sagt:**
```
"Erstelle eine Landing Page für [Projekt]"
```

**Claude macht:**
- Führt durch die 4 Schritte
- Führt Hard‑Gate QA durch
- Zeigt fertiges, geprüftes Design

---

### 🔄 Bestehendes Design verbessern

**Quick Check:**
```
User: "Checke mal portfolio_1.html"
Claude: [Startet integrierten Browser‑QA]
        → Findings dokumentieren (QA Report Template)
        → Blocker sofort fixen
        → PASS? Dann portfolio_1_1.html speichern
```

**Full Review (manuell, optional):**
```
User: "Mach Full Review von dashboard_1.html"
Claude: [Tiefer Audit ohne MCP]
        → WCAG/UX/Perf/IA Deep-Dive
        → Detaillierter Report
        → Du priorisierst Fixes
        → Speichert dashboard_1_2.html
```

---

## 🔍 QA-Typen

### Integrierter Browser QA (Schritt 5, Hard Gate)
- Laws‑of‑UX + HKI Pflicht‑Checklisten
- Ziel: "Bestandene UX/AA/Perf/IA-Prüfung?" – sonst kein Speichern

### Optionaler tiefer Review
- Vor Go‑Live/größeren Projekten, als ausführliches Audit (ohne MCP)

---

## 🛠️ Requirements

### Software
- **Cursor/VS Code** mit Claude Code
- **Node.js** (für `npx http-server` Preview)

---

## 🎓 Lernen

### Erste Schritte
1. Lies `CLAUDE.md` – komplette Workflow‑Doku
2. Starte mit "Neues Design" Workflow
3. Sieh dir den Hard‑Gate QA Ablauf an
4. Probiere dann "Bestehendes Design verbessern"

### Best Practices
- ✅ Immer Hard‑Gate QA vor dem Speichern in `design_iterations/`
- ✅ Version Bumps nutzen (nie Original überschreiben)
- ✅ Design‑System projektabhängig wählen (Material/GOV.UK/BBC/Custom)

---

## 📚 Weitere Infos

### Design Patterns unterstützt
- Neo‑Brutalism, Modern Dark, Clean Corporate

### Libraries (optional)
- Tailwind CSS (CDN), Font Awesome, Flowbite, Lucide Icons

---

## 🤝 Workflow‑Vorteile

Mit Hard‑Gate QA:
```
1. User beschreibt Design
2. Claude baut 4 Schritte
3. Claude prüft streng (Laws‑of‑UX + HKI)
4. Nur PASS wird gespeichert
→ Produktionstauglich, konsistent, schnell iterierbar
```

---

## 🎉 Ready to Start?

```bash
# 1. Kopiere Template
cp -r "I:/Ai Claude/SuperDesign-Template" "./my-new-project"

# 2. Öffne in VS Code
code "./my-new-project"

# 3. Sage zu Claude:
"Erstelle eine Landing Page für mein [Projekt]"

# 4. QA durchlaufen, dann versioniert speichern! 🚀
```
