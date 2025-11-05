#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download logos from kost-sicherheitstechnik.de website
"""
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import re

logos_dir = Path("images/logos")
logos_dir.mkdir(parents=True, exist_ok=True)

base_url = "https://www.kost-sicherheitstechnik.de/"

print("Fetching logos from kost-sicherheitstechnik.de...\n")

try:
    # Get the website HTML
    response = requests.get(base_url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all images in the references section
    # Look for logo images - they might be in img tags or background images
    images = soup.find_all('img')
    
    logo_patterns = {
        'fussballmuseum': ['fussballmuseum', 'fussball', 'dfb'],
        'wdi-schwerte': ['wdi', 'schwerte'],
        'uni-muenster': ['uni', 'muenster', 'universitaet'],
        'hse-getraenkewelt': ['hse', 'getraenkewelt'],
        'kurt-pietsch': ['pietsch', 'kurt'],
        'olympia-gruppe': ['olympia'],
        'larrivee': ['larrivee', 'arrivee'],
        'future-x': ['future'],
        'versatel': ['versatel'],
        'mcfit': ['mcfit'],
        'dortmund': ['dortmund', 'stadt'],
        'carlos': ['carlos'],
        'boss-steinlen': ['boss', 'steinlen'],
        'paratos': ['paratos']
    }
    
    downloaded = {}
    
    for img in images:
        src = img.get('src', '') or img.get('data-src', '')
        alt = img.get('alt', '').lower()
        
        if not src:
            continue
            
        # Make absolute URL
        if src.startswith('/'):
            src = base_url.rstrip('/') + src
        elif not src.startswith('http'):
            src = base_url + src.lstrip('/')
        
        # Check if this looks like a logo
        for logo_name, patterns in logo_patterns.items():
            if logo_name in downloaded:
                continue
                
            # Check if URL or alt text matches
            if any(p in src.lower() or p in alt for p in patterns):
                try:
                    img_response = requests.get(src, timeout=10)
                    if img_response.status_code == 200 and len(img_response.content) > 1000:
                        logo_path = logos_dir / f"{logo_name}.png"
                        
                        # Save as PNG (convert if needed)
                        with open(logo_path, 'wb') as f:
                            f.write(img_response.content)
                        
                        downloaded[logo_name] = src
                        print(f"[OK] Downloaded {logo_name}.png from {src}")
                        break
                except Exception as e:
                    pass
    
    # Also check for CSS background images
    styles = soup.find_all('style')
    for style in styles:
        if style.string:
            # Look for background-image URLs
            bg_images = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', style.string)
            for bg_url in bg_images:
                if bg_url.startswith('/'):
                    bg_url = base_url.rstrip('/') + bg_url
                elif not bg_url.startswith('http'):
                    bg_url = base_url + bg_url.lstrip('/')
                
                for logo_name, patterns in logo_patterns.items():
                    if logo_name in downloaded:
                        continue
                    if any(p in bg_url.lower() for p in patterns):
                        try:
                            img_response = requests.get(bg_url, timeout=10)
                            if img_response.status_code == 200 and len(img_response.content) > 1000:
                                logo_path = logos_dir / f"{logo_name}.png"
                                with open(logo_path, 'wb') as f:
                                    f.write(img_response.content)
                                downloaded[logo_name] = bg_url
                                print(f"[OK] Downloaded {logo_name}.png from background image: {bg_url}")
                                break
                        except:
                            pass
    
    print(f"\n[OK] Downloaded {len(downloaded)} logos from website")
    
except Exception as e:
    print(f"[ERROR] Error fetching website: {e}")

# Also try direct logo paths that might exist
logo_paths = [
    "/wp-content/uploads/",
    "/images/logos/",
    "/assets/logos/",
    "/logos/",
]

print("\nTrying common logo paths...")
for logo_name in logo_patterns.keys():
    if logo_name in downloaded:
        continue
    
    for base_path in logo_paths:
        for ext in ['.png', '.jpg', '.svg']:
            test_url = base_url.rstrip('/') + base_path + logo_name + ext
            try:
                response = requests.get(test_url, timeout=5)
                if response.status_code == 200 and len(response.content) > 1000:
                    logo_path = logos_dir / f"{logo_name}.png"
                    with open(logo_path, 'wb') as f:
                        f.write(response.content)
                    print(f"[OK] Found {logo_name}.png at {test_url}")
                    downloaded[logo_name] = test_url
                    break
            except:
                pass
        if logo_name in downloaded:
            break

print(f"\n[OK] Total logos downloaded: {len(downloaded)}")
print(f"Check {logos_dir} for logos.")




