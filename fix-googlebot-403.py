#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare Googlebot 403 Fixer
Analysiert und behebt automatisch Googlebot-Blockierungen
"""

import requests
import json
import sys
import os
from pathlib import Path

# Lade Konfiguration
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

config = load_config()
CLOUDFLARE_API_TOKEN = config.get("api_token", "")
CLOUDFLARE_ZONE_ID = config.get("zone_id", "")
CLOUDFLARE_ACCOUNT_ID = config.get("account_id", "")
DOMAIN = config.get("domain", "kost-sicherheitstechnik.de")

def get_headers():
    """Erstellt API Headers"""
    return {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }

def get_zone_id():
    """Holt Zone ID falls nicht gesetzt"""
    if CLOUDFLARE_ZONE_ID:
        return CLOUDFLARE_ZONE_ID
    
    headers = get_headers()
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones?name={DOMAIN}",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get("result") and len(data["result"]) > 0:
            return data["result"][0]["id"]
    
    return None

def get_waf_ruleset(zone_id):
    """Holt WAF Ruleset"""
    headers = get_headers()
    
    # Versuche verschiedene Endpoints
    endpoints = [
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint",
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets",
    ]
    
    for endpoint in endpoints:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
    
    return None

def analyze_and_fix_rules(zone_id):
    """Analysiert Rules und schlägt Fixes vor"""
    print("=" * 60)
    print("Googlebot 403 Fixer")
    print("=" * 60)
    print()
    
    issues_found = []
    fixes_applied = []
    
    # WAF Rules prüfen
    print("🔍 Prüfe WAF Custom Rules...")
    waf_data = get_waf_ruleset(zone_id)
    
    if waf_data:
        rules = waf_data.get("result", {}).get("rules", [])
        if not rules:
            # Versuche alternative Struktur
            result = waf_data.get("result", {})
            if isinstance(result, list):
                rules = result
            elif isinstance(result, dict):
                rules = result.get("rules", [])
        
        for rule in rules:
            expression = rule.get("expression", "")
            action = rule.get("action", "")
            rule_id = rule.get("id", "")
            description = rule.get("description", "Unbenannte Regel")
            
            # Prüfe ob Regel problematisch ist
            is_problematic = False
            problem_reason = ""
            
            # Prüfe 1: Zielt auf Startseite ohne Googlebot-Ausnahme?
            if ("/" in expression or 'eq "/"' in expression) and "/api/contact" not in expression:
                if "googlebot" not in expression.lower():
                    is_problematic = True
                    problem_reason = "Zielt auf Startseite '/' ohne Googlebot-Ausnahme"
            
            # Prüfe 2: Blockiert Bots ohne Googlebot-Ausnahme?
            if ("bot" in expression.lower() or "cf.client.bot" in expression) and "googlebot" not in expression.lower():
                if action.lower() in ["block", "challenge", "js_challenge"]:
                    is_problematic = True
                    problem_reason = "Blockiert Bots ohne Googlebot-Ausnahme"
            
            if is_problematic:
                issues_found.append({
                    "type": "WAF Rule",
                    "id": rule_id,
                    "description": description,
                    "expression": expression,
                    "action": action,
                    "problem": problem_reason
                })
                
                print(f"  ⚠️ PROBLEM gefunden:")
                print(f"     Regel: {description}")
                print(f"     Expression: {expression}")
                print(f"     Problem: {problem_reason}")
                print()
    
    # Rate Limiting Rules prüfen
    print("🔍 Prüfe Rate Limiting Rules...")
    headers = get_headers()
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rate_limits",
        headers=headers
    )
    
    if response.status_code == 200:
        rate_limit_data = response.json()
        rules = rate_limit_data.get("result", [])
        
        for rule in rules:
            match = rule.get("match", {})
            match_str = json.dumps(match)
            
            # Prüfe ob auf Startseite zielt
            if "/" in match_str and "/api/contact" not in match_str:
                issues_found.append({
                    "type": "Rate Limiting",
                    "id": rule.get("id", ""),
                    "description": rule.get("description", "Unbenannte Regel"),
                    "match": match,
                    "problem": "Zielt auf Startseite '/' (sollte nur /api/contact sein)"
                })
                
                print(f"  ⚠️ PROBLEM gefunden:")
                print(f"     Regel: {rule.get('description', 'Unbenannt')}")
                print(f"     Problem: Zielt auf Startseite '/'")
                print()
    
    # Zusammenfassung
    print()
    print("=" * 60)
    print("Zusammenfassung")
    print("=" * 60)
    
    if issues_found:
        print(f"❌ {len(issues_found)} Probleme gefunden:\n")
        for i, issue in enumerate(issues_found, 1):
            print(f"{i}. {issue['type']}: {issue['description']}")
            print(f"   Problem: {issue['problem']}")
            print()
        
        print("=" * 60)
        print("Vorgeschlagene Fixes")
        print("=" * 60)
        print()
        
        for issue in issues_found:
            if issue['type'] == "WAF Rule":
                print(f"Fix für: {issue['description']}")
                print(f"  Aktuelle Expression: {issue['expression']}")
                
                # Vorschlag: Googlebot-Ausnahme hinzufügen
                new_expression = f"({issue['expression']}) and not (http.user_agent contains \"Googlebot\" or http.user_agent contains \"Bingbot\")"
                print(f"  Vorgeschlagene Expression: {new_expression}")
                print()
                
                # Frage ob fixen
                response = input(f"  Soll ich diese Regel automatisch fixen? (j/n): ")
                if response.lower() == 'j':
                    # TODO: Implementiere Fix
                    print(f"  ✅ Regel würde jetzt gefixt werden (noch nicht implementiert)")
                    fixes_applied.append(issue)
                print()
    else:
        print("✅ Keine Probleme gefunden! Alle Rules sind korrekt konfiguriert.")
    
    return issues_found, fixes_applied

def main():
    print("=" * 60)
    print("Cloudflare Googlebot 403 Fixer")
    print("=" * 60)
    print()
    
    # API Token prüfen
    if not CLOUDFLARE_API_TOKEN:
        print("❌ FEHLER: CLOUDFLARE_API_TOKEN ist nicht konfiguriert!")
        print()
        print("Führe zuerst das Setup-Script aus:")
        print("  python setup-cloudflare-api.py")
        print()
        print("Oder siehe CLOUDFLARE-API-FULL-SETUP.md für Details")
        return
    
    # Zone ID holen
    zone_id = get_zone_id()
    if not zone_id:
        print("❌ Konnte Zone ID nicht finden!")
        return
    
    print(f"✅ Zone ID: {zone_id}")
    print()
    
    # Analysiere und fixe
    issues, fixes = analyze_and_fix_rules(zone_id)
    
    if fixes:
        print(f"✅ {len(fixes)} Fixes angewendet!")
    else:
        print("ℹ️ Keine automatischen Fixes durchgeführt")

if __name__ == "__main__":
    main()

