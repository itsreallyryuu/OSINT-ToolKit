import os
from utils.banner import show_banner
from modules.whois_lookup import whois_domain
from modules.ip_lookup import ip_info
from modules.dns_lookup import dns_lookup
from modules.username_check import check_username

RESET  = "\033[0m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
MAGENTA = "\033[95m"

def export_txt(data):
    with open("osint_report.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n" + "="*60 + "\n")
    print(GREEN + "\n[✓] Berhasil di-export ke osint_report.txt" + RESET)
    
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def post_action(result):
    while True:
        print(CYAN + """
[1] Export hasil ke TXT
[2] Kembali ke menu utama
""" + RESET)
        choice = input(YELLOW + "Pilih: " + RESET)

        if choice == "1":
            export_txt(result)
        elif choice == "2":
            clear_screen()
            break
        else:
            print(RED + "Pilihan tidak valid!" + RESET)

def menu():
    print(MAGENTA + """
==============================
            MENU
==============================
""" + RESET)
    print(CYAN + """
[1] Whois Domain
[2] IP Information
[3] DNS Lookup
[4] Username Check
[0] Exit
""" + RESET)

def main():
    clear_screen()
    show_banner()

    while True:
        menu()
        choice = input(YELLOW + ">> " + RESET)

        if choice == "1":
            domain = input(YELLOW + "Masukkan domain: " + RESET)
            print(BLUE + "\n[INFO] Mengambil data WHOIS...\n" + RESET)

            raw = whois_domain(domain)
            result = f"""
{CYAN}===== HASIL WHOIS DOMAIN ====={RESET}
{WHITE}Domain       : {GREEN}{domain}{RESET}

{CYAN}Data:{RESET}
{raw}
"""
            print(result)
            post_action(result)

        elif choice == "2":
            ip = input(YELLOW + "Masukkan IP Address: " + RESET)
            print(BLUE + "\n[INFO] Mengambil informasi IP...\n" + RESET)

            raw = ip_info(ip)
            result = f"""
{CYAN}===== HASIL IP INFORMATION ====={RESET}
{WHITE}IP Address   : {GREEN}{ip}{RESET}

{CYAN}Data:{RESET}
{raw}
"""
            print(result)
            post_action(result)

        elif choice == "3":
            domain = input(YELLOW + "Masukkan domain: " + RESET)
            print(BLUE + "\n[INFO] Melakukan DNS Lookup...\n" + RESET)

            raw = dns_lookup(domain)
            result = f"""
{CYAN}===== HASIL DNS LOOKUP ====={RESET}
{WHITE}Domain       : {GREEN}{domain}{RESET}

{CYAN}Data:{RESET}
{raw}
"""
            print(result)
            post_action(result)

        elif choice == "4":
            user = input(YELLOW + "Masukkan username: " + RESET)
            print(BLUE + "\n[INFO] Mengecek username...\n" + RESET)

            raw = check_username(user)
            result = f"""
{CYAN}===== HASIL USERNAME CHECK ====={RESET}
{WHITE}Username     : {GREEN}{user}{RESET}

{CYAN}Data:{RESET}
{raw}
"""
            print(result)
            post_action(result)

        elif choice == "0":
            print(GREEN + "Exit..." + RESET)
            break

        else:
            print(RED + "Pilihan tidak valid!" + RESET)

if __name__ == "__main__":
    main()
