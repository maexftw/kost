#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare API Setup Script
Erstellt eine permanente Konfigurationsdatei für die Cloudflare API
"""

import json
import os
import sys
from pathlib import Path

CONFIG_FILE = ".cloudflare-config.json"
CONFIG_FILE_ALT = "cloudflare-config.json"  # Fallback

def setup_config():
    """Interaktives Setup der Cloudflare API Konfiguration"""
    print("=" * 60)
    print("Cloudflare API - Permanente Einrichtung")
    print("=" * 60)
    print()
    print("Dieses Script erstellt eine lokale Konfigurationsdatei,")
    print("die von allen Cloudflare-Scripts automatisch verwendet wird.")
    print()
    print("Die Datei wird NICHT in Git committed (ist in .gitignore)")
    print()
    
    # Prüfe ob Config bereits existiert
    config_path = Path(CONFIG_FILE)
    if config_path.exists():
        print(f"⚠️ Konfigurationsdatei existiert bereits: {CONFIG_FILE}")
        response = input("  Überschreiben? (j/n): ")
        if response.lower() != 'j':
            print("Abgebrochen.")
            return
    
    print("Bitte gib deine Cloudflare API-Daten ein:")
    print()
    
    # API Token
    print("1. Cloudflare API Token")
    print("   Erstelle einen Token hier: https://dash.cloudflare.com/profile/api-tokens")
    print("   Permissions: Zone Read/Edit, Zone WAF Read/Edit, Zone Firewall Read/Edit")
    api_token = input("   API Token: ").strip()
    
    if not api_token:
        print("❌ API Token ist erforderlich!")
        return
    
    # Zone ID
    print()
    print("2. Zone ID (optional - wird automatisch gefunden wenn leer)")
    print("   Findest du in: Cloudflare Dashboard → Domain → Overview → Zone ID")
    zone_id = input("   Zone ID (Enter für Auto-Detection): ").strip()
    
    # Account ID
    print()
    print("3. Account ID (optional)")
    print("   Findest du in: Cloudflare Dashboard → Rechts oben bei deinem Profil")
    account_id = input("   Account ID (Enter zum Überspringen): ").strip()
    
    # Domain
    print()
    print("4. Domain")
    domain = input(f"   Domain (Standard: kost-sicherheitstechnik.de): ").strip()
    if not domain:
        domain = "kost-sicherheitstechnik.de"
    
    # Erstelle Config
    config = {
        "api_token": api_token,
        "zone_id": zone_id if zone_id else None,
        "account_id": account_id if account_id else None,
        "domain": domain
    }
    
    # Speichere Config
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print()
        print("=" * 60)
        print("✅ Konfiguration gespeichert!")
        print("=" * 60)
        print()
        print(f"Config-Datei: {CONFIG_FILE}")
        print("Diese Datei wird von allen Cloudflare-Scripts automatisch verwendet.")
        print()
        print("Nächste Schritte:")
        print("1. Teste die Verbindung: python check-cloudflare-rules.py")
        print("2. Analysiere Rules: python manage-cloudflare.py")
        print("3. Fixe Googlebot-Probleme: python fix-googlebot-403.py")
        print()
        
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")
        return
    
    # Teste Verbindung
    print("🔍 Teste API-Verbindung...")
    try:
        import requests
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        # Teste mit Zone ID oder Domain
        if zone_id:
            test_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}"
        else:
            test_url = f"https://api.cloudflare.com/client/v4/zones?name={domain}"
        
        response = requests.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ API-Verbindung erfolgreich!")
            data = response.json()
            if data.get("success"):
                if zone_id:
                    zone_name = data.get("result", {}).get("name", "Unbekannt")
                    print(f"   Zone: {zone_name}")
                else:
                    zones = data.get("result", [])
                    if zones:
                        zone_name = zones[0].get("name", "Unbekannt")
                        zone_id_found = zones[0].get("id", "")
                        print(f"   Zone: {zone_name}")
                        print(f"   Zone ID gefunden: {zone_id_found}")
                        
                        # Aktualisiere Config mit gefundener Zone ID
                        if not zone_id:
                            config["zone_id"] = zone_id_found
                            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                                json.dump(config, f, indent=2, ensure_ascii=False)
                            print(f"   ✅ Zone ID in Config gespeichert")
            else:
                print("⚠️ API antwortet, aber mit Fehler")
                print(f"   {data.get('errors', [])}")
        else:
            print(f"❌ API-Verbindung fehlgeschlagen: {response.status_code}")
            print(f"   {response.text}")
    
    except ImportError:
        print("⚠️ 'requests' Modul nicht installiert. Installiere mit: pip install requests")
    except Exception as e:
        print(f"⚠️ Fehler beim Testen: {e}")

def load_config():
    """Lädt die Konfiguration aus der Datei"""
    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        config_path = Path(CONFIG_FILE_ALT)
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Fehler beim Laden der Config: {e}")
            return None
    
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "load":
        # Nur Config laden (für andere Scripts)
        config = load_config()
        if config:
            print(json.dumps(config, indent=2))
    else:
        # Interaktives Setup
        setup_config()

