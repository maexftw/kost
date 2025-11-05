#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download missing logos from web
"""
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logos_dir = Path("images/logos")
logos_dir.mkdir(parents=True, exist_ok=True)

print("Suche fehlende Logos im Netz...\n")

# Logo URLs und Suchoptionen
logos_to_find = {
    "wdi-schwerte.png": {
        "search_terms": ["WDI Schwerte", "WDI Schwerte Logo"],
        "clearbit": "wdi-schwerte.de",
        "direct_urls": [
            "https://www.wdi-schwerte.de/logo.png",
            "https://www.wdi-schwerte.de/images/logo.png",
            "https://www.wdi-schwerte.de/assets/logo.png",
        ]
    },
    "hse-getraenkewelt.png": {
        "search_terms": ["HSE Getränkewelt Essen", "HSE Getränkewelt Logo"],
        "clearbit": "hse-getraenkewelt.de",
        "direct_urls": [
            "https://www.hse-getraenkewelt.de/logo.png",
            "https://www.hse-getraenkewelt.de/images/logo.png",
        ]
    },
    "kurt-pietsch.png": {
        "search_terms": ["Kurt Pietsch GmbH Group", "Kurt Pietsch Logo"],
        "clearbit": "kurt-pietsch.de",
        "direct_urls": [
            "https://www.kurt-pietsch.de/logo.png",
            "https://www.kurt-pietsch.de/images/logo.png",
        ]
    }
}

# Clearbit Logo API
for logo_name, info in logos_to_find.items():
    logo_path = logos_dir / logo_name
    
    if logo_path.exists():
        print(f"[SKIP] {logo_name} existiert bereits")
        continue
    
    print(f"\nSuche {logo_name}...")
    
    # Versuche Clearbit API
    if info.get("clearbit"):
        clearbit_url = f"https://logo.clearbit.com/{info['clearbit']}"
        try:
            print(f"  Versuche Clearbit: {clearbit_url}")
            response = requests.get(clearbit_url, timeout=10)
            if response.status_code == 200 and len(response.content) > 1000:
                with open(logo_path, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ Geladen von Clearbit ({len(response.content)} bytes)")
                continue
        except Exception as e:
            print(f"  ✗ Clearbit fehlgeschlagen: {e}")
    
    # Versuche direkte URLs
    for url in info.get("direct_urls", []):
        try:
            print(f"  Versuche: {url}")
            response = requests.get(url, timeout=10, allow_redirects=True)
            if response.status_code == 200 and len(response.content) > 1000:
                with open(logo_path, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ Geladen von {url} ({len(response.content)} bytes)")
                break
        except Exception as e:
            print(f"  ✗ {url}: {e}")
    else:
        print(f"  ⚠ {logo_name} konnte nicht geladen werden")

print("\n" + "="*60)
print("Suche auf Websites nach Logos...")
print("="*60)

# Versuche Logos direkt von Websites zu scrapen
websites = {
    "wdi-schwerte.png": "https://www.wdi-schwerte.de",
    "hse-getraenkewelt.png": "https://www.hse-getraenkewelt.de",
    "kurt-pietsch.png": "https://www.kurt-pietsch.de",
}

for logo_name, website_url in websites.items():
    logo_path = logos_dir / logo_name
    
    if logo_path.exists():
        continue
    
    try:
        print(f"\nScrape {website_url}...")
        response = requests.get(website_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Suche nach Logo-Images
            logo_patterns = ['logo', 'brand', 'header']
            images = soup.find_all('img')
            
            for img in images:
                src = img.get('src', '') or img.get('data-src', '')
                alt = img.get('alt', '').lower()
                
                if any(pattern in src.lower() or pattern in alt for pattern in logo_patterns):
                    # Mache URL absolut
                    if src.startswith('/'):
                        img_url = website_url.rstrip('/') + src
                    elif not src.startswith('http'):
                        img_url = website_url.rstrip('/') + '/' + src.lstrip('/')
                    else:
                        img_url = src
                    
                    try:
                        img_response = requests.get(img_url, timeout=10)
                        if img_response.status_code == 200 and len(img_response.content) > 1000:
                            with open(logo_path, 'wb') as f:
                                f.write(img_response.content)
                            print(f"  ✓ Logo gefunden: {img_url} ({len(img_response.content)} bytes)")
                            break
                    except:
                        pass
    except Exception as e:
        print(f"  ✗ Fehler: {e}")

print("\n" + "="*60)
print("Zusammenfassung:")
print("="*60)

for logo_name in logos_to_find.keys():
    logo_path = logos_dir / logo_name
    if logo_path.exists():
        size = logo_path.stat().st_size
        print(f"✓ {logo_name}: {size} bytes")
    else:
        print(f"✗ {logo_name}: Nicht gefunden")

