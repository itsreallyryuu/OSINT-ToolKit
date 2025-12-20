import os
from utils.banner import show_banner
from modules.whois_lookup import whois_domain
from modules.ip_lookup import ip_info
from modules.dns_lookup import dns_lookup
from modules.username_check import check_username
from modules.http_header import analyze_headers
from modules.tech_fingerprint import fingerprint

RESET       = "\033[0m"
BRIGHT_RED  = "\033[91m"  # merah menyala, untuk borders, info, error
WHITE       = "\033[97m"  # text utama
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

def menu():
    print(BRIGHT_RED + """
===============================
        MENU - SIESTA v1
===============================
""" + RESET)
    print(BRIGHT_RED + """
[1] Whois Domain
[2] IP Information
[3] DNS Lookup
[4] Username Check
[5] HTTP Header Analyzer
[6] Web Tech Detection
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
        

        elif choice == "0":
            print(BRIGHT_RED + "Exit..." + RESET)
            break

        else:
            print(BRIGHT_RED + "Pilihan tidak valid!" + RESET)

if __name__ == "__main__":
    main()
