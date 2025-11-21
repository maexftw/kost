#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare Management Tool
Vollständiges Tool zum Verwalten von Cloudflare WAF Rules, Firewall Rules, etc.
"""

import requests
import json
import sys
import os
from typing import Dict, List, Optional

# Konfiguration
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID", "")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
DOMAIN = "kost-sicherheitstechnik.de"

class CloudflareManager:
    def __init__(self, api_token: str, zone_id: Optional[str] = None):
        self.api_token = api_token
        self.zone_id = zone_id
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def get_zone_id(self, domain: str) -> Optional[str]:
        """Holt Zone ID für eine Domain"""
        if self.zone_id:
            return self.zone_id
        
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones?name={domain}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("result") and len(data["result"]) > 0:
                return data["result"][0]["id"]
        
        return None
    
    def list_waf_rules(self) -> List[Dict]:
        """Listet alle WAF Custom Rules"""
        if not self.zone_id:
            self.zone_id = self.get_zone_id(DOMAIN)
        
        # Versuche verschiedene Endpoints
        endpoints = [
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint",
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/rulesets",
        ]
        
        for endpoint in endpoints:
            response = requests.get(endpoint, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                result = data.get("result", {})
                if isinstance(result, dict):
                    return result.get("rules", [])
                elif isinstance(result, list):
                    return result
        
        return []
    
    def list_rate_limiting_rules(self) -> List[Dict]:
        """Listet alle Rate Limiting Rules"""
        if not self.zone_id:
            self.zone_id = self.get_zone_id(DOMAIN)
        
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/rate_limits",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json().get("result", [])
        
        return []
    
    def list_firewall_rules(self) -> List[Dict]:
        """Listet alle Firewall Rules"""
        if not self.zone_id:
            self.zone_id = self.get_zone_id(DOMAIN)
        
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/firewall/rules",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json().get("result", [])
        
        return []
    
    def update_waf_rule(self, rule_id: str, expression: str, action: str, description: str) -> bool:
        """Aktualisiert eine WAF Rule"""
        if not self.zone_id:
            self.zone_id = self.get_zone_id(DOMAIN)
        
        # TODO: Implementiere Update-Logik
        # Dies hängt von der Cloudflare API Struktur ab
        print(f"⚠️ Update noch nicht implementiert für Rule {rule_id}")
        return False
    
    def add_googlebot_exception(self, rule: Dict) -> Dict:
        """Fügt Googlebot-Ausnahme zu einer Regel hinzu"""
        expression = rule.get("expression", "")
        
        # Prüfe ob bereits Ausnahme vorhanden
        if "googlebot" in expression.lower():
            return rule
        
        # Füge Ausnahme hinzu
        new_expression = f"({expression}) and not (http.user_agent contains \"Googlebot\" or http.user_agent contains \"Bingbot\" or http.user_agent contains \"Slurp\" or http.user_agent contains \"DuckDuckBot\")"
        
        updated_rule = rule.copy()
        updated_rule["expression"] = new_expression
        
        return updated_rule
    
    def analyze_rules(self) -> Dict:
        """Analysiert alle Rules auf Probleme"""
        issues = {
            "waf_rules": [],
            "rate_limiting": [],
            "firewall": []
        }
        
        # WAF Rules
        waf_rules = self.list_waf_rules()
        for rule in waf_rules:
            expression = rule.get("expression", "")
            action = rule.get("action", "")
            
            # Prüfe auf Probleme
            if ("/" in expression or 'eq "/"' in expression) and "/api/contact" not in expression:
                if "googlebot" not in expression.lower():
                    issues["waf_rules"].append({
                        "rule": rule,
                        "problem": "Zielt auf Startseite ohne Googlebot-Ausnahme"
                    })
            
            if ("bot" in expression.lower() or "cf.client.bot" in expression) and "googlebot" not in expression.lower():
                if action.lower() in ["block", "challenge"]:
                    issues["waf_rules"].append({
                        "rule": rule,
                        "problem": "Blockiert Bots ohne Googlebot-Ausnahme"
                    })
        
        # Rate Limiting
        rate_rules = self.list_rate_limiting_rules()
        for rule in rate_rules:
            match = rule.get("match", {})
            match_str = json.dumps(match)
            
            if "/" in match_str and "/api/contact" not in match_str:
                issues["rate_limiting"].append({
                    "rule": rule,
                    "problem": "Zielt auf Startseite '/'"
                })
        
        return issues

def main():
    print("=" * 60)
    print("Cloudflare Management Tool")
    print("=" * 60)
    print()
    
    # API Token prüfen
    if not CLOUDFLARE_API_TOKEN:
        print("❌ FEHLER: CLOUDFLARE_API_TOKEN nicht gesetzt!")
        print("Siehe CLOUDFLARE-API-FULL-SETUP.md für Setup-Anleitung")
        return
    
    # Manager erstellen
    manager = CloudflareManager(CLOUDFLARE_API_TOKEN, CLOUDFLARE_ZONE_ID)
    
    if not manager.zone_id:
        manager.zone_id = manager.get_zone_id(DOMAIN)
    
    if not manager.zone_id:
        print("❌ Konnte Zone ID nicht finden!")
        return
    
    print(f"✅ Zone ID: {manager.zone_id}")
    print()
    
    # Analysiere Rules
    print("🔍 Analysiere alle Rules...")
    print()
    
    issues = manager.analyze_rules()
    
    total_issues = len(issues["waf_rules"]) + len(issues["rate_limiting"]) + len(issues["firewall"])
    
    if total_issues > 0:
        print(f"⚠️ {total_issues} Probleme gefunden:\n")
        
        if issues["waf_rules"]:
            print("WAF Rules:")
            for issue in issues["waf_rules"]:
                rule = issue["rule"]
                print(f"  - {rule.get('description', 'Unbenannt')}: {issue['problem']}")
            print()
        
        if issues["rate_limiting"]:
            print("Rate Limiting Rules:")
            for issue in issues["rate_limiting"]:
                rule = issue["rule"]
                print(f"  - {rule.get('description', 'Unbenannt')}: {issue['problem']}")
            print()
    else:
        print("✅ Keine Probleme gefunden!")
    
    # Zeige alle Rules
    print("=" * 60)
    print("Alle WAF Rules")
    print("=" * 60)
    
    waf_rules = manager.list_waf_rules()
    if waf_rules:
        for i, rule in enumerate(waf_rules, 1):
            print(f"\n{i}. {rule.get('description', 'Unbenannt')}")
            print(f"   Expression: {rule.get('expression', 'N/A')}")
            print(f"   Action: {rule.get('action', 'N/A')}")
    else:
        print("Keine WAF Rules gefunden")

if __name__ == "__main__":
    main()

