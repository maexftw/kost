#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detaillierter Funktionstest für die KOST Website
"""
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("DETAILLIERTER FUNKTIONSTEST - KOST WEBSITE")
print("=" * 70)

# Teste lokale Datei
index_path = Path("index.html")
errors = []
warnings = []

if index_path.exists():
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    print("\n[1] STRUKTUR-CHECK")
    print("-" * 70)
    
    # Prüfe alle Sections
    required_sections = {
        'hero-apple': 'Hero Section',
        '#services': 'Services Section',
        '#museum': 'Fußballmuseum Section',
        '#about': 'About Section',
        '#process': 'Process Section',
        '#sicherheitscheck': 'Sicherheitscheck Section',
        '#references': 'References Section',
        '#contact': 'Contact Section',
    }
    
    for section_id, name in required_sections.items():
        if section_id.startswith('#'):
            section = soup.find('section', id=section_id[1:])
        else:
            section = soup.find('section', class_=lambda x: x and section_id in str(x))
        
        if section:
            print(f"  ✓ {name}: OK")
        else:
            print(f"  ✗ {name}: FEHLT")
            errors.append(f"{name} fehlt")
    
    print("\n[2] NAVIGATION-CHECK")
    print("-" * 70)
    
    nav = soup.find('nav', id='mainNav')
    if nav:
        nav_links = nav.find_all('a', href=True)
        print(f"  ✓ Navigation gefunden mit {len(nav_links)} Links")
        
        # Prüfe ob alle Sections verlinkt sind
        section_links = [a['href'] for a in nav_links if a['href'].startswith('#')]
        print(f"  ✓ {len(section_links)} Section-Links gefunden")
    else:
        print("  ✗ Navigation nicht gefunden")
        errors.append("Navigation fehlt")
    
    print("\n[3] FUSSBALLMUSEUM-SECTION CHECK")
    print("-" * 70)
    
    museum_section = soup.find('section', id='museum')
    if museum_section:
        # Prüfe Logo
        dfm_logo = museum_section.find('img', src=lambda x: x and ('DFM' in x or 'fussballmuseum' in x))
        if dfm_logo:
            logo_src = dfm_logo.get('src', '')
            print(f"  ✓ DFM Logo gefunden: {logo_src}")
            
            # Prüfe ob Logo-Datei existiert
            logo_path = Path(logo_src)
            if logo_path.exists():
                print(f"  ✓ Logo-Datei existiert: {logo_path.stat().st_size} bytes")
            else:
                print(f"  ⚠ Logo-Datei nicht gefunden lokal: {logo_src}")
                warnings.append(f"Logo-Datei nicht gefunden: {logo_src}")
        else:
            print("  ✗ DFM Logo nicht gefunden")
            errors.append("DFM Logo fehlt")
        
        # Prüfe Text "setzt auf Kost Sicherheitstechnik"
        museum_text = museum_section.get_text()
        if 'setzt auf' in museum_text.lower() and 'kost' in museum_text.lower():
            print("  ✓ 'setzt auf Kost Sicherheitstechnik' Text gefunden")
        else:
            print("  ✗ Text 'setzt auf Kost Sicherheitstechnik' fehlt")
            errors.append("Museum Text fehlt")
        
        # Prüfe Button
        museum_button = museum_section.find('a', class_=lambda x: x and 'btn' in str(x))
        if museum_button:
            print("  ✓ Button gefunden")
        else:
            print("  ⚠ Button nicht gefunden")
            warnings.append("Museum Button fehlt")
        
        # Prüfe Layout (split-apple)
        if 'split-apple' in museum_section.get('class', []):
            print("  ✓ Split-Apple Layout korrekt")
        else:
            print("  ⚠ Split-Apple Layout fehlt")
            warnings.append("Split-Apple Layout fehlt")
    
    print("\n[4] REFERENZEN-SECTION CHECK")
    print("-" * 70)
    
    ref_section = soup.find('section', id='references')
    if ref_section:
        # Prüfe Featured Testimonial
        featured = ref_section.find('div', class_=lambda x: x and 'featured-testimonial' in str(x))
        if featured:
            print("  ✓ Featured Testimonial gefunden")
        else:
            print("  ⚠ Featured Testimonial nicht gefunden")
            warnings.append("Featured Testimonial fehlt")
        
        # Prüfe Logo-Grid
        logo_grid = ref_section.find('div', class_=lambda x: x and 'references-grid' in str(x))
        if logo_grid:
            logo_cards = logo_grid.find_all('div', class_=lambda x: x and 'reference-card' in str(x))
            print(f"  ✓ Logo-Grid gefunden mit {len(logo_cards)} Cards")
        else:
            print("  ✗ Logo-Grid nicht gefunden")
            errors.append("Logo-Grid fehlt")
        
        # Prüfe Logos
        logo_images = ref_section.find_all('img', src=lambda x: x and 'logos' in x)
        print(f"  ✓ {len(logo_images)} Logo-Bilder gefunden")
    
    print("\n[5] BILDER-CHECK")
    print("-" * 70)
    
    all_images = soup.find_all('img')
    missing_images = []
    
    for img in all_images[:20]:  # Erste 20 Bilder prüfen
        src = img.get('src', '')
        if src and not src.startswith('http') and not src.startswith('//'):
            img_path = Path(src)
            if not img_path.exists():
                missing_images.append(src)
    
    if missing_images:
        print(f"  ⚠ {len(missing_images)} Bilder fehlen lokal:")
        for img in missing_images[:5]:
            print(f"    - {img}")
    else:
        print("  ✓ Alle geprüften Bilder vorhanden")
    
    print("\n[6] RESPONSIVE DESIGN CHECK")
    print("-" * 70)
    
    # Prüfe ob Media Queries vorhanden sind
    style_tags = soup.find_all('style')
    has_media_queries = False
    for style in style_tags:
        if style.string and '@media' in style.string:
            has_media_queries = True
            break
    
    if has_media_queries:
        print("  ✓ Media Queries gefunden")
    else:
        print("  ⚠ Media Queries nicht gefunden")
        warnings.append("Media Queries fehlen")
    
    # Prüfe ob mobile Navigation vorhanden
    mobile_nav = soup.find('div', class_=lambda x: x and 'mobile' in str(x).lower())
    if mobile_nav:
        print("  ✓ Mobile Navigation gefunden")
    else:
        print("  ⚠ Mobile Navigation nicht gefunden")
        warnings.append("Mobile Navigation fehlt")
    
    print("\n[7] LIVESITE-CHECK")
    print("-" * 70)
    
    live_url = "https://maexftw.github.io/kost/"
    try:
        response = requests.get(live_url, timeout=10)
        if response.status_code == 200:
            print(f"  ✓ Live-Website erreichbar: {live_url}")
            print(f"  ✓ Status: {response.status_code}")
            print(f"  ✓ Größe: {len(response.content)} bytes")
            
            # Prüfe ob DFM Logo auf Live-Site vorhanden
            if 'DFM' in response.text or 'fussballmuseum' in response.text.lower():
                print("  ✓ Fußballmuseum Content auf Live-Site gefunden")
            else:
                print("  ⚠ Fußballmuseum Content nicht auf Live-Site gefunden")
                warnings.append("Fußballmuseum Content fehlt auf Live-Site")
        else:
            print(f"  ✗ Live-Website Status: {response.status_code}")
            errors.append(f"Live-Site Status: {response.status_code}")
    except Exception as e:
        print(f"  ✗ Live-Website nicht erreichbar: {e}")
        errors.append(f"Live-Site nicht erreichbar: {e}")
    
    print("\n" + "=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)
    
    if errors:
        print(f"\n✗ FEHLER ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print(f"\n⚠ WARNUNGEN ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("\n✓ ALLE TESTS BESTANDEN!")
    elif not errors:
        print("\n✓ Keine kritischen Fehler, aber einige Warnungen vorhanden")
    else:
        print("\n✗ Kritische Fehler gefunden!")

