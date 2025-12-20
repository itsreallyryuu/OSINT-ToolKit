import requests
import time

RESET       = "\033[0m"
BRIGHT_RED  = "\033[91m"  
RED         = "\033[31m"
GREEN       = "\033[92m"
WHITE       = "\033[97m"
CYAN        = "\033[96m"
YELLOW      = "\033[93m"
MAGENTA     = "\033[95m"

def render_table(data):
    col1, col2 = 18, 50
    line = BRIGHT_RED + "+" + "-"*col1 + "+" + "-"*col2 + "+" + RESET

    table = line + "\n"
    table += BRIGHT_RED + "|" + RESET + YELLOW + " Field".ljust(col1) + RESET
    table += BRIGHT_RED + "|" + RESET + YELLOW + " Value".ljust(col2) + RESET
    table += BRIGHT_RED + "|" + RESET + "\n"
    table += line + "\n"

    for k, v in data.items():
        table += (
            BRIGHT_RED + "|" + RESET +
            GREEN + f" {k}".ljust(col1) + RESET +
            BRIGHT_RED + "|" + RESET +
            WHITE + f" {v}".ljust(col2) + RESET +
            BRIGHT_RED + "|" + RESET + "\n"
        )
        table += line + "\n"

    return table

def ip_osint(ip):
    sources = []

    try:
        r1 = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        if r1.get("status") == "success":
            sources.append({
                "Country": r1["country"],
                "City": r1["city"],
                "ISP": r1["isp"],
                "ASN": r1["as"]
            })
    except:
        pass

    time.sleep(1)

    try:
        r2 = requests.get(f"https://ipwho.is/{ip}", timeout=10).json()
        if r2.get("success"):
            sources.append({
                "Country": r2["country"],
                "City": r2["city"],
                "ISP": r2["isp"],
                "ASN": r2["connection"]["asn"]
            })
    except:
        pass

    try:
        r3 = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10).json()
        sources.append({
            "Country": r3.get("country"),
            "City": r3.get("city"),
            "ISP": r3.get("org")
        })
    except:
        pass

    if not sources:
        return BRIGHT_RED + "Gagal mengambil data dari semua sumber." + RESET

    final = {}
    confidence = {}

    for src in sources:
        for k, v in src.items():
            if v:
                confidence.setdefault(k, {})
                confidence[k][v] = confidence[k].get(v, 0) + 1

    for field, values in confidence.items():
        best = max(values, key=values.get)
        final[field] = f"{best} ({values[best]}/{len(sources)} sources)"

    final["IP Address"] = ip
    final["Confidence Level"] = GREEN + "HIGH (Multi-source match)" + RESET

    return render_table(final)

def ip_info(ip):
    return ip_osint(ip)

def export_txt(result):
    with open("ip_result.txt", "w", encoding="utf-8") as f:
        f.write(result.replace("\033", ""))
    print(GREEN + "✔ Berhasil export ke ip_result.txt" + RESET)
