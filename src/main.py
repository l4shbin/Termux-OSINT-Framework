#!/usr/bin/env python3
import asyncio
import aiohttp
import json
import sys
import os
from urllib.parse import quote
from tqdm import tqdm
from tabulate import tabulate
from colorama import init, Fore, Style
import requests
from datetime import datetime

init(autoreset=True)

class L4SHOSINT:
    def __init__(self):
        with open('sites.json', 'r') as f:
            self.sites = json.load(f)
        self.results = []
        self.session = None

    async def check_site(self, session, name, url, username):
        try:
            async with session.get(url.format(quote(username)), 
                                 timeout=aiohttp.ClientTimeout(total=10)) as resp:
                status = resp.status
                exists = status == 200
                return {
                    'platform': name,
                    'url': url.format(username),
                    'status': status,
                    'exists': exists,
                    'response_time': f"{resp.real_url.hostname}"
                }
        except:
            return {'platform': name, 'url': url.format(username), 'error': 'Timeout/Blocked'}

    async def scan_username(self, username):
        print(f"{Fore.CYAN}🔍 Scanning {Fore.WHITE}{username} {Fore.CYAN}across 70+ platforms...\n")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for category, platforms in self.sites.items():
                for name, url in platforms.items():
                    tasks.append(self.check_site(session, name, url, username))
            
            results = []
            for future in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Scanning"):
                result = await future
                results.append(result)
                if result.get('exists'):
                    self.results.append(result)
                    print(f"{Fore.GREEN}✅ {result['platform']}: {result['url']}")
                elif result.get('error'):
                    print(f"{Fore.RED}❌ {result['platform']}: Error")
            
            self.export_results(username, results)

    def advanced_osint(self, username):
        print(f"\n{Fore.YELLOW}🛡️ ADVANCED OSINT MODULES\n")
        
        # Breach check (HIBP)
        try:
            resp = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{username}", 
                              headers={'User-Agent': 'OSINT-Tool'})
            if resp.status_code == 200:
                breaches = resp.json()
                print(f"{Fore.RED}💥 Found in {len(breaches)} breaches!")
                for b in breaches[:5]:
                    print(f"   - {b['Name']} ({b['BreachDate']})")
        except:
            pass

        # Email finder pattern
        emails = [f"{username}@gmail.com", f"{username}@yahoo.com"]
        print(f"\n📧 Potential emails: {', '.join(emails)}")

    def export_results(self, username, all_results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"osint_{username}_{timestamp}.json"
        
        data = {
            'target': username,
            'timestamp': timestamp,
            'hits': self.results,
            'total_scanned': len(all_results),
            'success_rate': len(self.results)/len(all_results)*100
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Pretty table
        table = [[r['platform'], r['url'], r.get('status', 'N/A')] for r in self.results]
        print(f"\n{Fore.GREEN}📊 SUMMARY TABLE:")
        print(tabulate(table, headers=['Platform', 'URL', 'Status'], tablefmt='grid'))
        print(f"{Fore.CYAN}💾 Results saved: {filename}")

async def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python main.py <username>")
        sys.exit(1)
    
    target = sys.argv[1]
    osint = L4SHOSINT()
    
    await osint.scan_username(target)
    osint.advanced_osint(target)

if __name__ == "__main__":
    asyncio.run(main())
