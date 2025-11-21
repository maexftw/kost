#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare WAF Rules Checker
Prüft alle WAF Rules auf mögliche Googlebot-Blockierungen
"""

import requests
import json
import sys

# Cloudflare API Konfiguration
CLOUDFLARE_API_TOKEN = ""  # Hier deinen API Token eintragen
ZONE_ID = ""  # Deine Zone ID (findest du in Cloudflare Dashboard → Overview → Zone ID)

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
            return data["result"][0]["id"]
    
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
        print("❌ FEHLER: CLOUDFLARE_API_TOKEN ist leer!")
        print()
        print("So erstellst du einen API Token:")
        print("1. Gehe zu: https://dash.cloudflare.com/profile/api-tokens")
        print("2. Klicke auf 'Create Token'")
        print("3. Wähle 'Edit zone DNS' Template oder erstelle Custom Token mit:")
        print("   - Zone: Zone:Read, Zone Settings:Read, Zone WAF:Read")
        print("   - Account: Account WAF:Read")
        print("4. Kopiere den Token und füge ihn oben in CLOUDFLARE_API_TOKEN ein")
        print()
        return
    
    # Zone ID holen falls nicht gesetzt
    if not ZONE_ID:
        domain = "kost-sicherheitstechnik.de"
        print(f"🔍 Suche Zone ID für {domain}...")
        zone_id = get_zone_id(CLOUDFLARE_API_TOKEN, domain)
        if zone_id:
            print(f"✅ Zone ID gefunden: {zone_id}")
            print(f"   (Füge diese oben in ZONE_ID ein für zukünftige Läufe)")
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

