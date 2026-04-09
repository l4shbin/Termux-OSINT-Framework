import json
import os
from engine import check_username

def banner():
    os.system('clear')
    print("""
    \033[1;32m
    ██╗     ██╗  ██╗███████╗██╗  ██╗
    ██║     ██║  ██║██╔════╝██║  ██║
    ██║     ███████║███████╗███████║
    ██║     ╚════██║╚════██║██╔══██║
    ███████╗     ██║███████║██║  ██║
    ╚══════╝     ╚═╝╚══════╝╚═╝  ╚═╝
    \033[1;36m      OSINT USERNAME TRACKER v1.0
    \033[1;33m       Developed by l4shbin
    \033[0m""")

def run():
    banner()
    username = input("\033[1;37m[?] Enter username to track: \033[0m")
    
    try:
        with open('src/targets.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("\033[1;31m[!] Error: targets.json not found!\033[0m")
        return

    print(f"\n\033[1;34m[*] Searching for: {username}...\033[0m")
    print("\033[1;30m" + "-"*45 + "\033[0m")

    found = 0
    for site in data['sites']:
        is_found, link = check_username(username, site['url'])
        if is_found:
            print(f"\033[1;32m[+] FOUND: {site['name']} -> {link}\033[0m")
            found += 1
        else:
            print(f"\033[1;31m[-] NOT FOUND: {site['name']}\033[0m")

    print("\033[1;30m" + "-"*45 + "\033[0m")
    print(f"\033[1;36m[*] Finished. Found on {found} platforms.\033[0m\n")

if __name__ == "__main__":
    run()
