import requests
import re

RESET       = "\033[0m"
BRIGHT_RED  = "\033[91m"
GREEN       = "\033[92m"
WHITE       = "\033[97m"
CYAN        = "\033[96m"
YELLOW      = "\033[93m"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (OSINT Toolkit)"
}

TECH_SIGNS = {
    "WordPress": ["wp-content", "wp-includes"],
    "Laravel": ["laravel", "csrf-token"],
    "React": ["react", "__react"],
    "Vue.js": ["vue", "__vue"],
    "Next.js": ["_next"],
    "Bootstrap": ["bootstrap"],
    "jQuery": ["jquery"],
    "Cloudflare": ["cloudflare"],
}

def fingerprint(url):
    results = []

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        headers = str(r.headers).lower()
        body = r.text.lower()

        
        server = r.headers.get("Server", "Unknown")
        results.append(("Server", server))

        
        powered = r.headers.get("X-Powered-By", "Unknown")
        results.append(("X-Powered-By", powered))

        
        detected = []
        for tech, signs in TECH_SIGNS.items():
            for sign in signs:
                if sign in headers or sign in body:
                    detected.append(tech)
                    break

        tech_result = ", ".join(detected) if detected else "No strong fingerprint"
        results.append(("Detected Tech", tech_result))

    except requests.RequestException:
        return YELLOW + "[!] Tidak bisa fingerprint website" + RESET

    
    col1, col2 = 20, 60
    line = BRIGHT_RED + "+" + "-"*col1 + "+" + "-"*col2 + "+" + RESET

    table = line + "\n"
    table += BRIGHT_RED + "|" + RESET + WHITE + " Category".ljust(col1) + RESET
    table += BRIGHT_RED + "|" + RESET + WHITE + " Result".ljust(col2) + RESET
    table += BRIGHT_RED + "|" + RESET + "\n"
    table += line + "\n"

    for k, v in results:
        table += (
            BRIGHT_RED + "|" + RESET +
            WHITE + f" {k}".ljust(col1) + RESET +
            BRIGHT_RED + "|" + RESET +
            GREEN + f" {v}".ljust(col2) + RESET +
            BRIGHT_RED + "|" + RESET + "\n"
        )
        table += line + "\n"

    return table
