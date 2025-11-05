#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download missing logos - try kost-sicherheitstechnik.de and alternative sources
"""
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logos_dir = Path("images/logos")
logos_dir.mkdir(parents=True, exist_ok=True)

print("Suche fehlende Logos auf kost-sicherheitstechnik.de...\n")

# Prüfe kost-sicherheitstechnik.de Website
base_url = "https://www.kost-sicherheitstechnik.de/"

try:
    response = requests.get(base_url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Suche nach allen Bildern
    images = soup.find_all('img')
    
    logo_mapping = {
        'wdi-schwerte': ['wdi', 'schwerte'],
        'hse-getraenkewelt': ['hse', 'getraenkewelt'],
        'kurt-pietsch': ['pietsch', 'kurt'],
    }
    
    for img in images:
        src = img.get('src', '') or img.get('data-src', '')
        alt = img.get('alt', '').lower()
        
        if not src:
            continue
        
        # Mache URL absolut
        if src.startswith('/'):
            src = base_url.rstrip('/') + src
        elif not src.startswith('http'):
            src = base_url + src.lstrip('/')
        
        # Prüfe ob es ein Logo ist, das wir brauchen
        for logo_name, patterns in logo_mapping.items():
            logo_path = logos_dir / f"{logo_name}.png"
            
            if logo_path.exists():
                continue
            
            if any(p in src.lower() or p in alt for p in patterns):
                try:
                    img_response = requests.get(src, timeout=10)
                    if img_response.status_code == 200 and len(img_response.content) > 1000:
                        with open(logo_path, 'wb') as f:
                            f.write(img_response.content)
                        print(f"✓ {logo_name}.png gefunden: {src} ({len(img_response.content)} bytes)")
                        break
                except Exception as e:
                    pass
    
    # Auch CSS Background-Images prüfen
    styles = soup.find_all('style')
    for style in styles:
        if style.string:
            bg_images = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', style.string)
            for bg_url in bg_images:
                if bg_url.startswith('/'):
                    bg_url = base_url.rstrip('/') + bg_url
                elif not bg_url.startswith('http'):
                    bg_url = base_url + bg_url.lstrip('/')
                
                for logo_name, patterns in logo_mapping.items():
                    logo_path = logos_dir / f"{logo_name}.png"
                    
                    if logo_path.exists():
                        continue
                    
                    if any(p in bg_url.lower() for p in patterns):
                        try:
                            img_response = requests.get(bg_url, timeout=10)
                            if img_response.status_code == 200 and len(img_response.content) > 1000:
                                with open(logo_path, 'wb') as f:
                                    f.write(img_response.content)
                                print(f"✓ {logo_name}.png gefunden (Background): {bg_url} ({len(img_response.content)} bytes)")
                                break
                        except:
                            pass

except Exception as e:
    print(f"Fehler beim Laden der Website: {e}")

# Alternative: Verwende Logo-APIs mit verschiedenen Domain-Varianten
print("\nVersuche alternative Logo-Quellen...")

alternative_domains = {
    'wdi-schwerte.png': [
        'wdi-schwerte.de',
        'wdi.de',
        'wdi-group.de',
    ],
    'hse-getraenkewelt.png': [
        'hse-getraenkewelt.de',
        'hse.de',
        'getraenkewelt.de',
    ],
    'kurt-pietsch.png': [
        'kurt-pietsch.de',
        'pietsch.de',
        'kurt-pietsch-group.de',
    ],
}

for logo_name, domains in alternative_domains.items():
    logo_path = logos_dir / logo_name
    
    if logo_path.exists():
        continue
    
    for domain in domains:
        clearbit_url = f"https://logo.clearbit.com/{domain}"
        try:
            response = requests.get(clearbit_url, timeout=10)
            if response.status_code == 200 and len(response.content) > 1000:
                with open(logo_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ {logo_name} von Clearbit ({domain}): {len(response.content)} bytes")
                break
        except:
            pass

print("\n" + "="*60)
print("Zusammenfassung:")
print("="*60)

missing_logos = ['wdi-schwerte.png', 'hse-getraenkewelt.png', 'kurt-pietsch.png']
for logo_name in missing_logos:
    logo_path = logos_dir / logo_name
    if logo_path.exists():
        size = logo_path.stat().st_size
        print(f"✓ {logo_name}: {size} bytes")
    else:
        print(f"✗ {logo_name}: Nicht gefunden")

