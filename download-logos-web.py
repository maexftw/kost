#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download remaining logos from web sources
"""
import requests
from pathlib import Path

logos_dir = Path("images/logos")
logos_dir.mkdir(parents=True, exist_ok=True)

# Known logo URLs - these are commonly available logos
logo_urls = {
    "mcfit.png": "https://www.mcfit.com/favicon.ico",  # Will use favicon as fallback
    "dortmund.png": "https://www.dortmund.de/fileadmin/website/logo/logo_stadt_dortmund.png",
    "versatel.png": "https://www.versatel.de/favicon.ico",
}

# Try to download from logo APIs
logo_apis = {
    "fussballmuseum.png": "https://logo.clearbit.com/deutsches-fussballmuseum.de",
    "uni-muenster.png": "https://logo.clearbit.com/uni-muenster.de", 
    "mcfit.png": "https://logo.clearbit.com/mcfit.com",
    "versatel.png": "https://logo.clearbit.com/versatel.de",
    "future-x.png": "https://logo.clearbit.com/future-x.de",
    "larrivee.png": "https://logo.clearbit.com/larrivee.de",
    "olympia-gruppe.png": "https://logo.clearbit.com/olympia-gruppe.de",
    "carlos.png": "https://logo.clearbit.com/carlos.de",
}

print("Downloading logos from web sources...\n")

for logo_name, url in logo_apis.items():
    logo_path = logos_dir / logo_name
    
    # Skip if already exists
    if logo_path.exists():
        print(f"[SKIP] {logo_name} already exists")
        continue
    
    try:
        print(f"Downloading {logo_name} from {url}...")
        response = requests.get(url, timeout=10, allow_redirects=True)
        
        if response.status_code == 200 and len(response.content) > 1000:  # At least 1KB
            with open(logo_path, 'wb') as f:
                f.write(response.content)
            print(f"  [OK] Saved {logo_name} ({len(response.content)} bytes)")
        else:
            print(f"  [FAIL] Invalid response for {logo_name}")
    except Exception as e:
        print(f"  [ERROR] {logo_name}: {e}")

print(f"\n[OK] Download complete!")
print(f"Check {logos_dir} for downloaded logos.")




