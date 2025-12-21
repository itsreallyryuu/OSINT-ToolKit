import os
from time import time
from utils.banner import RED, show_banner
from modules.whois_lookup import whois_domain
from modules.ip_lookup import ip_info
from modules.dns_lookup import dns_lookup
from modules.username_check import check_username
from modules.http_header import analyze_headers
from modules.tech_fingerprint import fingerprint
from modules.ip_geo import ip_geolocation
from modules.attack_surface import attack_surface_mapper
from modules.footprint_analyzer import footprint_analyzer
from modules.asset_monitor import asset_snapshot, compare_snapshot
from datetime import datetime




RESET       = "\033[0m"
BRIGHT_RED  = "\033[91m"
WHITE       = "\033[97m"
DARK_RED    = "\033[31;2m"  


def export_txt(data):
    with open("osint_report.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n" + "="*60 + "\n")
    print(BRIGHT_RED + "\n[✓] Berhasil di-export ke osint_report.txt" + RESET)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def post_action(result):
    while True:
        print(BRIGHT_RED + """
[1] Export to txt file
[2] Kembali ke menu utama
""" + RESET)
        choice = input(WHITE + "Pilih: " + RESET)

        if choice == "1":
            export_txt(result)
        elif choice == "2":
            clear_screen()
            break
        else:
            print(BRIGHT_RED + "Pilihan tidak valid!" + RESET)
            
def format_attack_surface(data):
    output = ""

    output += f"Domain        : {data['domain']}\n\n"

    output += "[IP ADDRESSES]\n"
    if data["ip_addresses"]:
        for ip in data["ip_addresses"]:
            output += f" - {ip}\n"
    else:
        output += " - Not found\n"

    output += "\n[SUBDOMAINS]\n"
    if data["subdomains"]:
        for sub in data["subdomains"]:
            output += f" - {sub}\n"
    else:
        output += " - None detected\n"

    output += "\n[DNS RECORDS]\n"
    for rtype, records in data["dns_records"].items():
        output += f" {rtype}:\n"
        if records:
            for r in records:
                output += f"   - {r}\n"
        else:
            output += "   - Not found\n"

    output += "\n[INFRASTRUCTURE]\n"
    output += f" Hosting : {data['hosting']}\n"
    output += f" CDN     : {data['cdn']}\n"

    return output
            
def format_online_presence(data):
    output = ""

    output += f"Username / Keyword : {data['username']}\n\n"

    output += "[PROFILES FOUND]\n"
    if data["profiles_found"]:
        for p in data["profiles_found"]:
            output += f" - {p['platform']}\n"
            output += f"   URL        : {p['url']}\n"
            output += f"   Confidence : {p['confidence']}\n\n"
    else:
        output += " - No profiles detected\n\n"

    output += f"[OVERALL CONFIDENCE]\n {data['overall_confidence']}\n"

    return output

def menu():
    print(BRIGHT_RED + """
===============================
        MENU - Siesta v1
===============================
""" + RESET)
    print(BRIGHT_RED + """
[1] Whois Domain
[2] IP Information
[3] DNSLookup
[4] Username Check
[5] HTTP Header Analyzer
[6] Web Tech Detection
[7] IP Geolocation
[8] Attack Surface Mapper
[9] Online Presence Scanner
[10] Website Change Monitor
[0] Exit
""" + RESET)

def main():
    clear_screen()
    show_banner()

    while True:
        menu()
        choice = input(WHITE + ">> " + RESET)

        if choice == "1":
            domain = input(WHITE + "Masukkan domain: " + RESET)
            print(BRIGHT_RED + "\n[INFO] Mengambil data WHOIS...\n" + RESET)
            raw = whois_domain(domain)
            result = f"""
{BRIGHT_RED}===== HASIL WHOIS DOMAIN ====={RESET}
{WHITE}Domain       : {WHITE}{domain}{RESET}

{BRIGHT_RED}Data:{RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)

        elif choice == "2":
            ip = input(WHITE + "Masukkan IP Address: " + RESET)
            print(BRIGHT_RED + "\n[INFO] Mengambil informasi IP...\n" + RESET)
            raw = ip_info(ip)
            result = f"""
{BRIGHT_RED}===== HASIL IP INFORMATION ====={RESET}
{WHITE}IP Address   : {WHITE}{ip}{RESET}

{BRIGHT_RED}Data:{RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)

        elif choice == "3":
            domain = input(WHITE + "Masukkan domain: " + RESET)
            print(BRIGHT_RED + "\n[INFO] Melakukan DNS Lookup...\n" + RESET)
            raw = dns_lookup(domain)
            result = f"""
{BRIGHT_RED}===== HASIL DNS LOOKUP ====={RESET}
{WHITE}Domain       : {WHITE}{domain}{RESET}

{BRIGHT_RED}Data:{RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)

        elif choice == "4":
            user = input(WHITE + "Masukkan username: " + RESET)
            print(BRIGHT_RED + "\n[INFO] Mengecek username...\n" + RESET)
            raw = check_username(user)
            result = f"""
{BRIGHT_RED}===== HASIL USERNAME CHECK ====={RESET}
{WHITE}Username     : {WHITE}{user}{RESET}

{BRIGHT_RED}Data:{RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)

        elif choice == "5":
            domain = input(WHITE + "Masukkan domain (contoh: example.com): " + RESET)
            print(BRIGHT_RED + "\n[INFO] Mengambil HTTP Header...\n" + RESET)
            url = "https://" + domain
            raw = analyze_headers(url)
            result = f"""
{BRIGHT_RED}===== HASIL HTTP HEADER ANALYZER ====={RESET}
{WHITE}Target URL   : {WHITE}{url}{RESET}

{BRIGHT_RED}Data:{RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)

        elif choice == "6":
            domain = input(WHITE + "Masukkan domain (contoh: example.com): " + RESET)
            print(BRIGHT_RED + "\n[INFO] Melakukan Website Technology Detection...\n" + RESET)
            url = "https://" + domain
            raw = fingerprint(url)
            result = f"""
{BRIGHT_RED}===== HASIL WEBSITE TECHNOLOGY DETECTION ====={RESET}
{WHITE}Target URL   : {WHITE}{url}{RESET}

{BRIGHT_RED}Data:{RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)

        elif choice == "7":
            print(RED + "\n[INFO] IP Geolocation Lookup\n" + RESET)

            ip = input("Target IP : ").strip()
            result = ip_geolocation(ip)

            if "error" in result:
                print(RED + "[ERROR] " + result["error"] + RESET)
            else:
                print(BRIGHT_RED + "\n===== GEO RESULT =====" + RESET)
                for k, v in result.items():
                    print(f"{WHITE}{k.upper():12}{RESET}: {v}{RESET}")


        elif choice == "8":
            domain = input(WHITE + "Masukkan domain: " + RESET)
            print(BRIGHT_RED + "\n[INFO] Mapping attack surface...\n" + RESET)

            raw_data = attack_surface_mapper(domain)
            raw = format_attack_surface(raw_data)

            result = f"""
{BRIGHT_RED}===== ATTACK SURFACE MAPPER ====={RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)


        elif choice == "9":
            keyword = input(WHITE + "Masukkan username / keyword: " + RESET)
            print(BRIGHT_RED + "\n[INFO] Scanning online presence...\n" + RESET)

            raw_data = footprint_analyzer(keyword)
            raw = format_online_presence(raw_data)

            result = f"""
{BRIGHT_RED}===== ONLINE PRESENCE SCANNER ====={RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)


        elif choice == "10":
            domain = input(WHITE + "Masukkan domain (contoh: example.com): " + RESET)
            print(BRIGHT_RED + "\n[INFO] Monitoring website changes...\n" + RESET)
            url = "https://" + domain
            old = asset_snapshot(url)
            new = asset_snapshot(url)
            raw = compare_snapshot(old, new)

            result = f"""
{BRIGHT_RED}===== WEBSITE CHANGE MONITOR ====={RESET}
{WHITE}Target URL : {url}{RESET}

{BRIGHT_RED}Status:{RESET}
{WHITE}{raw}{RESET}
"""
            print(result)
            post_action(result)

        elif choice == "0":
            print(BRIGHT_RED + f"[{datetime.now():%H:%M:%S}] Siesta off. Bye.\n" + RESET)
            break

        else:
            print(BRIGHT_RED + "Pilihan tidak valid!" + RESET)

            
            
        

if __name__ == "__main__":
    main()
