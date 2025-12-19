import socket
import re

RESET  = "\033[0m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"

WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com",
    "net": "whois.verisign-grs.com",
    "org": "whois.pir.org",
    "id": "whois.pandi.or.id",
}

FIELDS = {
    "Domain Name": r"Domain Name:\s*(.+)",
    "Registrar": r"Registrar:\s*(.+)",
    "Creation Date": r"Creation Date:\s*(.+)",
    "Expiration Date": r"Expir\w+ Date:\s*(.+)",
    "Updated Date": r"Updated Date:\s*(.+)",
    "Name Server": r"Name Server:\s*(.+)",
    "Status": r"Status:\s*(.+)",
}

def query_whois(server, domain):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((server, 43))
    s.send((domain + "\r\n").encode())
    response = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data
    s.close()
    return response.decode(errors="ignore")

def parse_whois(raw):
    result = {}
    for field, pattern in FIELDS.items():
        matches = re.findall(pattern, raw, re.IGNORECASE)
        if matches:
            result[field] = list(set(m.strip() for m in matches))
    return result

def render_table(data):
    col1 = 18
    col2 = 44

    line = CYAN + "+" + "-"*col1 + "+" + "-"*col2 + "+" + RESET

    table = line + "\n"
    table += (
        CYAN + "|" + RESET +
        YELLOW + " Field".ljust(col1) + RESET +
        CYAN + "|" + RESET +
        YELLOW + " Value".ljust(col2) + RESET +
        CYAN + "|" + RESET + "\n"
    )
    table += line + "\n"

    for field, values in data.items():
        for i, value in enumerate(values):
            if i == 0:
                table += (
                    CYAN + "|" + RESET +
                    GREEN + f" {field}".ljust(col1) + RESET +
                    CYAN + "|" + RESET +
                    WHITE + f" {value}".ljust(col2) + RESET +
                    CYAN + "|" + RESET + "\n"
                )
            else:
                table += (
                    CYAN + "|" + RESET +
                    " ".ljust(col1) +
                    CYAN + "|" + RESET +
                    WHITE + f" {value}".ljust(col2) + RESET +
                    CYAN + "|" + RESET + "\n"
                )
        table += line + "\n"

    return table

def whois_domain(domain):
    tld = domain.split(".")[-1].lower()
    server = WHOIS_SERVERS.get(tld)

    if not server:
        return RED + "WHOIS server untuk TLD ini belum didukung." + RESET

    raw = query_whois(server, domain)
    parsed = parse_whois(raw)

    if not parsed:
        return RED + "Data WHOIS tidak ditemukan atau diproteksi." + RESET

    return render_table(parsed)
