import requests

RESET       = "\033[0m"
BRIGHT_RED  = "\033[91m"  
RED         = "\033[31m"
GREEN       = "\033[92m"
CYAN        = "\033[96m"
WHITE       = "\033[97m"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (OSINT Toolkit)"
}

def analyze_headers(url):
    col1, col2 = 25, 55
    line = BRIGHT_RED + "+" + "-"*col1 + "+" + "-"*col2 + "+" + RESET

    table = line + "\n"
    table += BRIGHT_RED + "|" + RESET + " Header".ljust(col1)
    table += BRIGHT_RED + "|" + RESET + " Value".ljust(col2)
    table += BRIGHT_RED + "|" + RESET + "\n"
    table += line + "\n"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)

        for key, value in r.headers.items():
            table += (
                BRIGHT_RED + "|" + RESET +
                WHITE + f" {key}".ljust(col1) + RESET +
                BRIGHT_RED + "|" + RESET +
                GREEN + f" {value}".ljust(col2) + RESET +
                BRIGHT_RED + "|" + RESET + "\n"
            )
            table += line + "\n"

        return table

    except requests.RequestException:
        return BRIGHT_RED + "[!] Gagal mengambil HTTP Header" + RESET
