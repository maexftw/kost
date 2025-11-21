#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare WAF Rules Checker
Prüft alle WAF Rules auf mögliche Googlebot-Blockierungen
"""

import requests
import json
import sys
import os
from pathlib import Path

# Lade Konfiguration aus Datei oder Umgebungsvariablen
def load_config():
    """Lädt Cloudflare API Konfiguration"""
    config = {}
    
    # 1. Versuche Config-Datei zu laden
    config_file = Path(".cloudflare-config.json")
    if not config_file.exists():
        config_file = Path("cloudflare-config.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"⚠️ Fehler beim Laden der Config-Datei: {e}")
    
    # 2. Überschreibe mit Umgebungsvariablen (haben Priorität)
    if os.getenv("CLOUDFLARE_API_TOKEN"):
        config["api_token"] = os.getenv("CLOUDFLARE_API_TOKEN")
    if os.getenv("CLOUDFLARE_ZONE_ID"):
        config["zone_id"] = os.getenv("CLOUDFLARE_ZONE_ID")
    if os.getenv("CLOUDFLARE_ACCOUNT_ID"):
        config["account_id"] = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    if os.getenv("CLOUDFLARE_DOMAIN"):
        config["domain"] = os.getenv("CLOUDFLARE_DOMAIN")
    
    return config

# Cloudflare API Konfiguration
config = load_config()
CLOUDFLARE_API_TOKEN = config.get("api_token", "")
ZONE_ID = config.get("zone_id", "")
DOMAIN = config.get("domain", "kost-sicherheitstechnik.de")

def get_zone_id(api_token, domain):
    """Holt die Zone ID für eine Domain"""
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones?name={domain}",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get("result") and len(data["result"]) > 0:
            zone_id = data["result"][0]["id"]
            # Speichere Zone ID in Config falls nicht vorhanden
            if not ZONE_ID:
                try:
                    config_file = Path(".cloudflare-config.json")
                    if config_file.exists():
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                        config["zone_id"] = zone_id
                        with open(config_file, 'w', encoding='utf-8') as f:
                            json.dump(config, f, indent=2, ensure_ascii=False)
                except:
                    pass
            return zone_id
    
    return None

def get_waf_rules(api_token, zone_id):
    """Holt alle WAF Custom Rules"""
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen der WAF Rules: {response.status_code}")
        print(response.text)
        return None

def get_rate_limiting_rules(api_token, zone_id):
    """Holt alle Rate Limiting Rules"""
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rate_limits",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen der Rate Limiting Rules: {response.status_code}")
        return None

def get_firewall_rules(api_token, zone_id):
    """Holt alle Firewall Rules"""
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen der Firewall Rules: {response.status_code}")
        return None

def analyze_rule(rule, rule_type="WAF"):
    """Analysiert eine Regel auf mögliche Googlebot-Blockierungen"""
    issues = []
    
    # Prüfe Expression
    expression = rule.get("expression", "")
    action = rule.get("action", "")
    
    # Prüfe ob Regel auf Startseite zielt
    if "/" in expression or "eq \"/\"" in expression or "eq \"/\"" in expression:
        if "/api/contact" not in expression:
            issues.append(f"⚠️ Regel zielt auf Startseite '/' (nicht nur /api/contact)")
    
    # Prüfe ob Regel Bots blockiert
    if "bot" in expression.lower() or "cf.client.bot" in expression:
        if "googlebot" not in expression.lower():
            issues.append(f"⚠️ Regel blockiert Bots, aber hat keine Googlebot-Ausnahme")
    
    # Prüfe Action
    if action.lower() in ["block", "challenge", "js_challenge"]:
        if "googlebot" not in expression.lower():
            issues.append(f"⚠️ Regel blockiert/challenged ohne Googlebot-Ausnahme")
    
    return issues

def main():
    print("=" * 60)
    print("Cloudflare WAF Rules Checker")
    print("=" * 60)
    print()
    
    # API Token prüfen
    if not CLOUDFLARE_API_TOKEN:
        print("❌ FEHLER: CLOUDFLARE_API_TOKEN ist nicht konfiguriert!")
        print()
        print("Zwei Möglichkeiten:")
        print()
        print("1. Setup-Script ausführen (empfohlen):")
        print("   python setup-cloudflare-api.py")
        print()
        print("2. Oder manuell:")
        print("   - Erstelle .cloudflare-config.json mit deinem API Token")
        print("   - Oder setze Umgebungsvariable: CLOUDFLARE_API_TOKEN")
        print()
        print("Siehe auch: CLOUDFLARE-API-FULL-SETUP.md")
        print()
        return
    
    # Zone ID holen falls nicht gesetzt
    if not ZONE_ID:
        print(f"🔍 Suche Zone ID für {DOMAIN}...")
        zone_id = get_zone_id(CLOUDFLARE_API_TOKEN, DOMAIN)
        if zone_id:
            print(f"✅ Zone ID gefunden: {zone_id}")
            print(f"   (Wird automatisch in Config gespeichert)")
        else:
            print("❌ Zone ID nicht gefunden!")
            return
    else:
        zone_id = ZONE_ID
    
    print()
    print("=" * 60)
    print("WAF Custom Rules")
    print("=" * 60)
    
    # WAF Rules holen
    waf_data = get_waf_rules(CLOUDFLARE_API_TOKEN, zone_id)
    if waf_data:
        rules = waf_data.get("result", {}).get("rules", [])
        if rules:
            print(f"📋 {len(rules)} WAF Custom Rules gefunden:\n")
            for i, rule in enumerate(rules, 1):
                print(f"Rule #{i}: {rule.get('description', 'Keine Beschreibung')}")
                print(f"  Expression: {rule.get('expression', 'N/A')}")
                print(f"  Action: {rule.get('action', 'N/A')}")
                
                issues = analyze_rule(rule, "WAF")
                if issues:
                    print("  ⚠️ PROBLEME:")
                    for issue in issues:
                        print(f"    - {issue}")
                else:
                    print("  ✅ Keine Probleme gefunden")
                print()
        else:
            print("✅ Keine WAF Custom Rules gefunden")
    else:
        print("❌ Konnte WAF Rules nicht abrufen")
    
    print()
    print("=" * 60)
    print("Rate Limiting Rules")
    print("=" * 60)
    
    # Rate Limiting Rules holen
    rate_limit_data = get_rate_limiting_rules(CLOUDFLARE_API_TOKEN, zone_id)
    if rate_limit_data:
        rules = rate_limit_data.get("result", [])
        if rules:
            print(f"📋 {len(rules)} Rate Limiting Rules gefunden:\n")
            for i, rule in enumerate(rules, 1):
                match = rule.get("match", {})
                print(f"Rule #{i}: {rule.get('description', 'Keine Beschreibung')}")
                print(f"  Match: {json.dumps(match, indent=2)}")
                print(f"  Threshold: {rule.get('threshold', 'N/A')}")
                print(f"  Action: {rule.get('action', {}).get('mode', 'N/A')}")
                
                # Prüfe ob auf Startseite zielt
                match_str = json.dumps(match)
                if "/" in match_str and "/api/contact" not in match_str:
                    print("  ⚠️ PROBLEM: Regel zielt auf Startseite '/' (sollte nur /api/contact sein)")
                else:
                    print("  ✅ Regel zielt nur auf /api/contact")
                print()
        else:
            print("✅ Keine Rate Limiting Rules gefunden")
    else:
        print("❌ Konnte Rate Limiting Rules nicht abrufen")
    
    print()
    print("=" * 60)
    print("Firewall Rules")
    print("=" * 60)
    
    # Firewall Rules holen
    firewall_data = get_firewall_rules(CLOUDFLARE_API_TOKEN, zone_id)
    if firewall_data:
        rules = firewall_data.get("result", [])
        if rules:
            print(f"📋 {len(rules)} Firewall Rules gefunden:\n")
            for i, rule in enumerate(rules, 1):
                print(f"Rule #{i}: {rule.get('description', 'Keine Beschreibung')}")
                print(f"  Filter: {json.dumps(rule.get('filter', {}), indent=2)}")
                print(f"  Action: {rule.get('action', 'N/A')}")
                
                issues = analyze_rule(rule, "Firewall")
                if issues:
                    print("  ⚠️ PROBLEME:")
                    for issue in issues:
                        print(f"    - {issue}")
                else:
                    print("  ✅ Keine Probleme gefunden")
                print()
        else:
            print("✅ Keine Firewall Rules gefunden")
    else:
        print("❌ Konnte Firewall Rules nicht abrufen")
    
    print()
    print("=" * 60)
    print("Zusammenfassung")
    print("=" * 60)
    print("Prüfe die oben genannten Probleme und stelle sicher, dass:")
    print("1. Keine Regel auf '/' zielt (außer sie hat Googlebot-Ausnahme)")
    print("2. Alle Bot-Blockierungen haben Googlebot-Ausnahme")
    print("3. Rate Limiting nur für '/api/contact' gilt")

if __name__ == "__main__":
    main()

