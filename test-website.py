#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functionstest für die KOST Website
"""
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Test URLs
test_urls = [
    "https://maexftw.github.io/kost/",
    "https://www.kost-sicherheitstechnik.de/",
]

print("=" * 60)
print("KOST WEBSITE FUNKTIONSTEST")
print("=" * 60)

# Test 1: Lokale HTML-Datei prüfen
print("\n[TEST 1] Lokale HTML-Datei prüfen...")
index_path = Path("index.html")
if index_path.exists():
    print(f"✓ index.html gefunden")
    
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Prüfe wichtige Elemente
    checks = {
        "Hero Section": soup.find('section', class_='hero-apple'),
        "Services Section": soup.find('section', id='services'),
        "Fußballmuseum Section": soup.find('section', id='museum'),
        "About Section": soup.find('section', id='about'),
        "References Section": soup.find('section', id='references'),
        "Contact Section": soup.find('section', id='contact'),
        "Navigation": soup.find('nav', id='mainNav'),
        "Fußballmuseum Logo": soup.find('img', src=lambda x: x and 'DFM' in x or 'fussballmuseum' in x),
    }
    
    for name, element in checks.items():
        if element:
            print(f"  ✓ {name}: OK")
        else:
            print(f"  ✗ {name}: FEHLT")
    
    # Prüfe Bilder
    print("\n[BILD-CHECK] Prüfe wichtige Bilder...")
    images_to_check = [
        "images/logos/67b5989e98af53668eeae5dc_Logo_DFM.svg",
        "images/logos/paratos.png",
        "images/logos/boss-steinlen.png",
        "images/Kost-Logo-seit-1995.png",
    ]
    
    for img_path in images_to_check:
        img_file = Path(img_path)
        if img_file.exists():
            print(f"  ✓ {img_path}: OK ({img_file.stat().st_size} bytes)")
        else:
            print(f"  ✗ {img_path}: FEHLT")
    
    # Prüfe JavaScript
    print("\n[JAVASCRIPT-CHECK] Prüfe wichtige Funktionen...")
    scripts = soup.find_all('script')
    print(f"  ✓ {len(scripts)} Script-Tags gefunden")
    
    # Prüfe ob Lucide Icons geladen werden
    if 'lucide' in html_content.lower() or 'data-lucide' in html_content:
        print("  ✓ Lucide Icons: OK")
    else:
        print("  ✗ Lucide Icons: FEHLT")
    
    # Prüfe CSS
    print("\n[CSS-CHECK] Prüfe Stylesheets...")
    css_files = soup.find_all('link', rel='stylesheet')
    print(f"  ✓ {len(css_files)} Stylesheets gefunden")
    
    css_path = Path("css/theme.css")
    if css_path.exists():
        print(f"  ✓ css/theme.css: OK ({css_path.stat().st_size} bytes)")
    else:
        print(f"  ✗ css/theme.css: FEHLT")
    
    # Prüfe Links
    print("\n[LINK-CHECK] Prüfe interne Links...")
    links = soup.find_all('a', href=True)
    internal_links = [a['href'] for a in links if a['href'].startswith('#') or a['href'].startswith('pages/')]
    print(f"  ✓ {len(internal_links)} interne Links gefunden")
    
    # Prüfe Buttons
    print("\n[BUTTON-CHECK] Prüfe Call-to-Action Buttons...")
    buttons = soup.find_all('a', class_=lambda x: x and 'btn' in str(x))
    print(f"  ✓ {len(buttons)} Buttons gefunden")
    
    # Prüfe Footer
    footer = soup.find('footer')
    if footer:
        print("  ✓ Footer: OK")
    else:
        print("  ✗ Footer: FEHLT")
    
else:
    print("✗ index.html nicht gefunden!")

# Test 2: Live-Website prüfen
print("\n" + "=" * 60)
print("[TEST 2] Live-Website prüfen...")
print("=" * 60)

for url in test_urls:
    print(f"\nTeste: {url}")
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            print(f"  ✓ Status: {response.status_code} OK")
            print(f"  ✓ Größe: {len(response.content)} bytes")
            
            # Prüfe ob wichtige Inhalte vorhanden sind
            content = response.text.lower()
            checks = {
                "Fußballmuseum": "fussballmuseum" in content or "dfm" in content,
                "Kost Sicherheitstechnik": "kost" in content,
                "Referenzen": "referenzen" in content or "references" in content,
                "Kontakt": "kontakt" in content or "contact" in content,
            }
            
            for name, found in checks.items():
                if found:
                    print(f"  ✓ {name}: Gefunden")
                else:
                    print(f"  ? {name}: Nicht gefunden")
        else:
            print(f"  ✗ Status: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout - Website antwortet nicht")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Fehler: {e}")

print("\n" + "=" * 60)
print("TEST ABGESCHLOSSEN")
print("=" * 60)

