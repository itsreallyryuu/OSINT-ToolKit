"""
Ultra-WHOIS  :  12 sumber bebas, tanpa API-key, anti gagal
Author       :  Siesta v1
"""
import socket, re, requests, textwrap, datetime
from urllib.parse import urlparse

RESET = "\033[0m"
RED   = "\033[91m"
GREEN = "\033[92m"
WHITE = "\033[97m"
CYAN  = "\033[96m"
YELLOW= "\033[93m"

def normalize_domain(d):
    d = d.lower().strip()
    return urlparse(d).netloc or d.split("/")[0]

def vote(f, v, src, bucket):
    if not v: return
    bucket.setdefault(f, {}).setdefault(str(v).strip(), []).append(src)

def best(bucket, f):
    if f not in bucket: return None
    return max(bucket[f].items(), key=lambda kv: len(kv[1]))[0]

def http_text(url, to=12):
    try: return requests.get(url, timeout=to).text
    except: return ""

def date_norm(d):
    try: return datetime.datetime.fromisoformat(d.replace("Z","+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
    except: return d

def whois_port43(domain):
    def query(srv):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(12)
            s.connect((srv, 43))
            s.send(f"{domain}\r\n".encode())
            data = b""; chunk = True
            while chunk: chunk = s.recv(4096); data += chunk
            s.close(); return data.decode(errors="ignore")
        except: return ""
    raw = query("whois.iana.org")
    srv = re.search(r"whois:\s*(.+)", raw, re.I)
    if not srv: return {}
    server = srv.group(1).strip()
    raw = query(server) or ""
    ref = re.search(r"Whois Server:\s*(.+)", raw, re.I)
    if ref: raw += "\n" + (query(ref.group(1).strip()) or "")
    b = {}
    pts = {
        "Domain Name": r"Domain Name:\s*(.+)",
        "Registry Domain ID": r"Registry Domain ID:\s*(.+)",
        "Registrar": r"Registrar:\s*(.+)",
        "Registrar IANA ID": r"Registrar IANA ID:\s*(.+)",
        "Registrar Abuse Email": r"Registrar Abuse Contact Email:\s*(.+)",
        "Registrar Abuse Phone": r"Registrar Abuse Contact Phone:\s*(.+)","Creation Date": r"Creation Date:\s*(.+)",
        "Updated Date": r"Updated Date:\s*(.+)",
        "Expiration Date": r"Expir\w* Date:\s*(.+)",
        "Registrant Name": r"Registrant Name:\s*(.+)",
        "Registrant Organization": r"Registrant Organization:\s*(.+)",
        "Registrant Country": r"Registrant Country:\s*(.+)",
        "Registrant Email": r"Registrant Email:\s*(.+)",
        "Admin Name": r"Admin Name:\s*(.+)",
        "Admin Email": r"Admin Email:\s*(.+)",
        "Tech Name": r"Tech Name:\s*(.+)",
        "Tech Email": r"Tech Email:\s*(.+)",
        "Billing Name": r"Billing Name:\s*(.+)",
        "Billing Email": r"Billing Email:\s*(.+)",
        "Name Server": r"Name Server:\s*(.+)",
        "DNSSEC": r"DNSSEC:\s*(.+)",
        "Domain Status": r"Status:\s*(.+)",
        "WHOIS Server": r"Whois Server:\s*(.+)",
        "Registrar URL": r"Registrar URL:\s*(.+)",
    }
    for f, p in pts.items():
        for m in re.finditer(p, raw, re.I):
            vote(f, m.group(1), "port43", b)
    return b

def whois_rdap(domain):
    tld = domain.split(".")[-1]
    try:
        boot = requests.get("https://data.iana.org/rdap/dns.json", timeout=10).json()
        for e in boot.get("services", []):
            if tld in e[0]:
                url = e[1][0] + "domain/" + domain; break
        else: return {}
    except: return {}
    try: j = requests.get(url, timeout=10).json()
    except: return {}
    b = {}
    vote("Domain Name", j.get("ldhName"), "rdap", b)
    vote("Registry Domain ID", j.get("handle"), "rdap", b)
    for ent in j.get("entities", []):
        roles = ent.get("roles", [])
        if "registrar" in roles:
            vote("Registrar", ent.get("handle"), "rdap", b)
        for vc in ent.get("vcardArray", []):
            if vc[0] == "fn":
                if "registrant" in roles: vote("Registrant Name", vc[3], "rdap", b)
                if "admin" in roles: vote("Admin Name", vc[3], "rdap", b)
                if "tech" in roles: vote("Tech Name", vc[3], "rdap", b)
                if "billing" in roles: vote("Billing Name", vc[3], "rdap", b)
            if vc[0] == "org":
                if "registrant" in roles: vote("Registrant Organization", vc[3], "rdap", b)
            if vc[0] == "email":
                if "registrant" in roles: vote("Registrant Email", vc[3], "rdap", b)
                if "admin" in roles: vote("Admin Email", vc[3], "rdap", b)
                if "tech" in roles: vote("Tech Email", vc[3], "rdap", b)
                if "billing" in roles: vote("Billing Email", vc[3], "rdap", b)
    for ev in j.get("events", []):
        act = ev.get("eventAction")
        if act == "registration": vote("Creation Date", ev.get("eventDate"), "rdap", b)
        if act == "last changed": vote("Updated Date", ev.get("eventDate"), "rdap", b)
        if act == "expiration": vote("Expiration Date", ev.get("eventDate"), "rdap", b)
    for ns in j.get("nameservers", []):
        vote("Name Server", ns.get("ldhName"), "rdap", b)
    for st in j.get("status", []):
        vote("Domain Status", st, "rdap", b)
    vote("DNSSEC", "signed" if j.get("dnssec") else "unsigned", "rdap", b)
    return b

def whois_ht(domain):
    raw = http_text(f"https://api.hackertarget.com/whois/?q={domain}")
    b = {}
    pts = {
        "Domain Name": r"Domain Name:\s*(.+)",
        "Registrar": r"Registrar:\s*(.+)",
        "Registrar IANA ID": r"Registrar IANA ID:\s*(.+)",
        "Creation Date": r"Creation Date:\s*(.+)",
        "Expiration Date": r"Expir\w* Date:\s*(.+)",
        "Name Server": r"Name Server:\s*(.+)",
        "Domain Status": r"Status:\s*(.+)",
        "DNSSEC": r"DNSSEC:\s*(.+)",
    }
    for f, p in pts.items():
        for m in re.finditer(p, raw, re.I):
            vote(f, m.group(1), "ht", b)
    return b

def whois_lean(domain):
    raw = http_text(f"https://leanwhois.com/whois/{domain}")
    b = {}
    pts = {
        "Domain Name": r"Domain Name:\s*(.+)",
        "Registrar": r"Registrar:\s*(.+)",
        "Creation Date": r"Creation Date:\s*(.+)",
        "Updated Date": r"Updated Date:\s*(.+)",
        "Expiration Date": r"Expir\w* Date:\s*(.+)",
        "Name Server": r"Name Server:\s*(.+)",
        "Domain Status": r"Status:\s*(.+)",
        "DNSSEC": r"DNSSEC:\s*(.+)",
    }
    for f, p in pts.items():
        for m in re.finditer(p, raw, re.I):
            vote(f, m.group(1), "lean", b)
    return b

def whois_nimbus(domain):
    raw = http_text(f"https://whois.nimbus.co.id/{domain}")
    b = {}
    pts = {
        "Domain Name": r"Domain Name:\s*(.+)",
        "Registrar": r"Registrar:\s*(.+)",
        "Creation Date": r"Creation Date:\s*(.+)",
        "Expiration Date": r"Expir\w* Date:\s*(.+)",
        "Name Server": r"Name Server:\s*(.+)",
        "Domain Status": r"Status:\s*(.+)",
        "DNSSEC": r"DNSSEC:\s*(.+)",
    }
    for f, p in pts.items():
        for m in re.finditer(p, raw, re.I):
            vote(f, m.group(1), "nimbus", b)
    return b

def whois_lizard(domain):
    raw = http_text(f"https://dnslizard.com/whois/{domain}")
    b = {}
    pts = {
        "Domain Name": r"Domain Name:\s*(.+)",
        "Registrar": r"Registrar:\s*(.+)",
        "Creation Date": r"Creation Date:\s*(.+)",
        "Expiration Date": r"Expir\w* Date:\s*(.+)",
        "Name Server": r"Name Server:\s*(.+)",
        "Domain Status": r"Status:\s*(.+)",
        "DNSSEC": r"DNSSEC:\s*(.+)",
    }
    for f, p in pts.items():
        for m in re.finditer(p, raw, re.I):
            vote(f, m.group(1), "lizard", b)
    return b

def whois_cymru(domain):
    raw = http_text(f"https://whois.cymru.com/whois/{domain}")
    b = {}
    pts = {
        "Domain Name": r"Domain Name:\s*(.+)",
        "Registrar": r"Registrar:\s*(.+)",
        "Creation Date": r"Creation Date:\s*(.+)",
        "Expiration Date": r"Expir\w* Date:\s*(.+)",
        "Name Server": r"Name Server:\s*(.+)",
        "Domain Status": r"Status:\s*(.+)",
        "DNSSEC": r"DNSSEC:\s*(.+)",
    }
    for f, p in pts.items():
        for m in re.finditer(p, raw, re.I):
            vote(f, m.group(1), "cymru", b)
    return b

def whois_ninxus(domain):
    raw = http_text(f"https://whois.ninxus.com/whois/{domain}")
    b = {}
    pts = {
        "Domain Name": r"Domain Name:\s*(.+)",
        "Registrar": r"Registrar:\s*(.+)",
        "Creation Date": r"Creation Date:\s*(.+)",
        "Expiration Date": r"Expir\w* Date:\s*(.+)",
        "Name Server": r"Name Server:\s*(.+)",
        "Domain Status": r"Status:\s*(.+)",
        "DNSSEC": r"DNSSEC:\s*(.+)",
    }
    for f, p in pts.items():
        for m in re.finditer(p, raw, re.I):
            vote(f, m.group(1), "ninxus", b)
    return b

def whois_leanws(domain):
    raw = http_text(f"https://whois.lean.ws/whois/{domain}")
    b = {}
    pts = {
        "Domain Name": r"Domain Name:\s*(.+)",
        "Registrar": r"Registrar:\s*(.+)",
        "Creation Date": r"Creation Date:\s*(.+)",
        "Expiration Date": r"Expir\w* Date:\s*(.+)",
        "Name Server": r"Name Server:\s*(.+)",
        "Domain Status": r"Status:\s*(.+)",
        "DNSSEC": r"DNSSEC:\s*(.+)",
    }
    for f, p in pts.items():
        for m in re.finditer(p, raw, re.I):
            vote(f, m.group(1), "leanws", b)
    return b

def ns_hint(domain):
    try:
        ans = requests.get(f"https://dns.google/resolve?name={domain}&type=NS", timeout=8).json()
        ns = [ar["data"][:-1] for ar in ans.get("Answer", [])]
        return {"Name Server": ns} if ns else {}
    except: return {}

def hist_whois(domain):
    try:
        j = requests.get(f"https://domaininfo.shreshtait.com/api/search/{domain}", timeout=8).json()
        if j.get("creation_date"):
            return {"Historical WHOIS": f'1 record – first: {j["creation_date"]}'}
    except: return {}
    return {}

def pro_whois(domain):
    domain = normalize_domain(domain)
    bucket = {}
    sources = [whois_port43, whois_rdap, whois_ht, whois_lean,
               whois_nimbus, whois_lizard, whois_cymru, whois_ninxus,
               whois_leanws, hist_whois, ns_hint]
    for src in sources:
        data = src(domain) or {}
        for f, v in data.items():
            if isinstance(v, list):
                for item in v: vote(f, item, src.__name__, bucket)
            else:
                vote(f, v, src.__name__, bucket)

    GROUPS = {
        "Registrasi": ["Domain Name","Registry Domain ID","Creation Date",
                       "Updated Date","Expiration Date","Domain Status"],
        "Registrar": ["Registrar","Registrar IANA ID","Registrar Abuse Email",
                      "Registrar Abuse Phone","Registrar URL","WHOIS Server"],
        "Kontak": ["Registrant Name","Registrant Organization","Registrant Country",
                   "Registrant Email","Admin Name","Admin Email","Tech Name",
                   "Tech Email","Billing Name","Billing Email"],
        "Infrastruktur": ["Name Server","DNSSEC"],
        "Tambahan": ["Historical WHOIS","Age (days)","Privacy Detected","NS Hint"]
    }
    flat = {}
    for f in {ff for gg in GROUPS.values() for ff in gg}:
        raw = best(bucket, f)
        if f in {"Creation Date","Updated Date","Expiration Date"}:
            flat[f] = date_norm(raw) if raw else "-"
        else:
            flat[f] = raw or "-"

    create = flat.get("Creation Date", "-")
    if create != "-":
        try:
            age = (datetime.datetime.now(datetime.timezone.utc) -
                   datetime.datetime.fromisoformat(create.replace("Z","+00:00"))).days
            flat["Age (days)"] = str(age)
        except Exception:
            flat["Age (days)"] = "-"
    else:
        flat["Age (days)"] = "-"

    raw_all = str(bucket)
    flat["Privacy Detected"] = "YES" if "redacted" in raw_all.lower() or "privacy" in raw_all.lower() else "NO"
    ns = best(bucket, "Name Server")
    flat["NS Hint"] = ns if ns and ns != "-" else "-"
    hist = best(bucket, "Historical WHOIS")
    flat["Historical WHOIS"] = hist or "-"

    if flat["Domain Name"] == "-":
        return RED + "Semua sumber WHOIS gagal / data kosong." + RESET

    return render_pro(GROUPS, flat)

def render_pro(groups, data):
    col1, col2 = 28, 50
    line = RED + "+" + "-"*col1 + "+" + "-"*col2 + "+" + RESET
    out = [line]
    for grp, fields in groups.items():
        out.append(RED + "|" + RESET + CYAN + grp.center(col1+col2+1) + RESET + RED + "|" + RESET)
        out.append(line)
        for f in fields:
            val = data.get(f, "-")
            for idx, w in enumerate(textwrap.wrap(str(val), col2) or ["-"]):
                prefix = f if idx == 0 else ""
                out.append(RED + "|" + RESET + WHITE + f" {prefix}".ljust(col1) +
                           RED + "|" + RESET + WHITE + f" {w}".ljust(col2) + RED + "|" + RESET)
            out.append(line)
    conf = GREEN + "ULTRA (11-src merged)" + RESET
    out.append(RED + "|" + RESET + f"Confidence{RED}|{RESET}" + conf.ljust(col2) + RED + "|" + RESET)
    out.append(line)
    return "\n".join(out)

whois_domain = pro_whois

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: whois_lookup.py domain.tld")
        sys.exit(1)
    print(pro_whois(sys.argv[1]))