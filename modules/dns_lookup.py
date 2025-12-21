import requests, socket, textwrap, datetime
from dns.exception import DNSException
import dns.resolver
from urllib.parse import urlparse

RESET      = "\033[0m"
RED        = "\033[31m"
DARK_RED   = "\033[31;2m"
BRIGHT_RED = "\033[91m"
GREEN      = "\033[92m"
WHITE      = "\033[97m"

NINJA_KEY  = "n46KnJ/0Beyi/RpSdqqEww==Mcadb6j1TLP1uDvg"

def normalize_domain(d):
    d = d.lower().strip()
    return urlparse(d).netloc or d.split("/")[0]

def http_json(url, to=8, headers=None):
    try: return requests.get(url, timeout=to, headers=headers or {}).json()
    except: return {}

def http_text(url, to=8):
    try: return requests.get(url, timeout=to).text
    except: return ""

def vote(f, v, src, bucket):
    if not v: return
    bucket.setdefault(f, {}).setdefault(str(v).strip(), []).append(src)

def best(bucket, f):
    if f not in bucket: return None
    return max(bucket[f].items(), key=lambda kv: len(kv[1]))[0]

def date_norm(d):
    try: return datetime.datetime.fromisoformat(d.replace("Z","+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
    except: return d

def ninja_dns(domain):
    hdr = {"X-Api-Key": NINJA_KEY}
    j = http_json(f"https://api.api-ninjas.com/v1/dnslookup?domain={domain}", headers=hdr)
    if not j or not isinstance(j, list): return {}
    b = {}
    for rec in j:
        if isinstance(rec, dict):
            if "premium" in str(rec).lower(): continue
            rtype = rec.get("record_type")
            val   = rec.get("value")
            if rtype and val:
                vote(rtype, val, "Ninja", b)
    return b

def google_doh(domain, rtype):
    j = http_json(f"https://dns.google/resolve?name={domain}&type={rtype}")
    if j.get("Status") != 0: return []
    return [r["data"].rstrip(".") for r in j.get("Answer", [])]

def cf_doh(domain, rtype):
    hdr = {"Accept": "application/dns-json"}
    j = http_json(f"https://cloudflare-dns.com/dns-query?name={domain}&type={rtype}", headers=hdr)
    if j.get("Status") != 0: return []
    return [r["data"].rstrip(".") for r in j.get("Answer", [])]

def hackertarget_dns(domain):
    raw = http_text(f"https://api.hackertarget.com/dnslookup/?q={domain}")
    b = {}
    for line in raw.splitlines():
        if "\t" in line:
            rtype, value = line.split("\t", 1)
            vote(rtype.strip(), value.strip(), "HackerTarget", b)
    return b

def statdns(domain, rtype):
    j = http_json(f"https://api.statdns.com/{domain}/{rtype.lower()}")
    if not j.get("answer"): return []
    return [r["rdata"].rstrip(".") for r in j["answer"]]

def local_resolve(domain, rtype):
    try:
        ans = dns.resolver.resolve(domain, rtype, lifetime=5)
        return [str(r).rstrip(".") for r in ans]
    except DNSException:
        return []

def rdap_ip(domain):
    try:
        boot = requests.get("https://data.iana.org/rdap/dns.json", timeout=8).json()
        tld = domain.split(".")[-1]
        for e in boot.get("services", []):
            if tld in e[0]:
                url = e[1][0] + "domain/" + domain; break
        else: return {}
        j = requests.get(url, timeout=8).json()
        b = {}
        vote("Domain Name", j.get("ldhName"), "RDAP", b)
        for ev in j.get("events", []):
            act = ev.get("eventAction")
            if act == "registration": vote("Creation Date", ev.get("eventDate"), "RDAP", b)
            if act == "expiration": vote("Expiration Date", ev.get("eventDate"), "RDAP", b)
        for ns in j.get("nameservers", []):
            vote("Name Server", ns.get("ldhName"), "RDAP", b)
        return b
    except: return {}

def rev_hint(domain):
    try:
        ip = socket.gethostbyname(domain)
        rev = socket.gethostbyaddr(ip)[0]
        return {"Reverse Host": rev}
    except: return {}

def ip_geo(domain):
    try:
        ip = socket.gethostbyname(domain)
        j = http_json(f"http://ip-api.com/json/{ip}")
        if j.get("status") == "success":
            return {"IP Location": f"{j['city']}, {j['country']}"}
    except: return {}
    return {}

def zone_xfer(domain):
    try:
        ns_ans = dns.resolver.resolve(domain, "NS", lifetime=5)
        for ns in ns_ans:
            from dns import zone as z
            try:
                z.from_xfr(dns.query.xfr(str(ns), domain))
                return {"Zone Transfer": "VULNERABLE"}
            except: continue
    except: pass
    return {"Zone Transfer": "Not vulnerable / refused"}

def txt_sec(domain):
    txt = local_resolve(domain, "TXT")
    tokens = [t for t in txt if any(k in t.lower() for k in ("spf", "dkim", "dmarc"))]
    return {"TXT Security": tokens} if tokens else {}

def port_hint(domain):
    ip = best({"IP": {socket.gethostbyname(domain): ["socket"]}}, "IP") if "." in domain else None
    if not ip: return {}
    common = [21, 22, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 8080]
    openp = []
    for p in common:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            if s.connect_ex((ip, p)) == 0:
                openp.append(str(p))
            s.close()
        except: s.close()
    return {"Open Ports": ", ".join(openp)} if openp else {}

def cdn_waf(domain):
    try:
        r = requests.get(f"https://{domain}", timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        hdr = r.headers
        wafs = {
            "cloudflare": "Cloudflare",
            "akamai": "Akamai",
            "incapsula": "Incapsula",
            "sucuri": "Sucuri",
            "aws": "AWS WAF",
        }
        for k, v in hdr.items():
            for w in wafs:
                if w in v.lower() or w in k.lower():
                    return {"WAF/CDN": wafs[w]}
        if "server" in hdr:
            return {"Server": hdr["Server"]}
    except: pass
    return {}

def super_dns(domain):
    domain = normalize_domain(domain)
    bucket = {}

    for f, v in ninja_dns(domain).items():
        vote(f, v, "Ninja", bucket)

    sources = [
        ("Google DoH", lambda: google_doh(domain, "A")),
        ("Cloudflare DoH", lambda: cf_doh(domain, "A")),
        ("HackerTarget", lambda: hackertarget_dns(domain)),
        ("StatDNS", lambda: statdns(domain, "A")),
        ("Local Resolver", lambda: local_resolve(domain, "A")),
        ("RDAP", lambda: rdap_ip(domain)),
        ("Reverse IP", lambda: rev_hint(domain)),
        ("IP-API Geo", lambda: ip_geo(domain)),
        ("Zone Transfer", lambda: zone_xfer(domain)),
        ("TXT Security", lambda: txt_sec(domain)),
        ("Port Hint", lambda: port_hint(domain)),
        ("CDN/WAF", lambda: cdn_waf(domain)),
    ]

    for name, func in sources:
        try:
            data = func() or {}
            for f, v in data.items():
                if isinstance(v, list):
                    for item in v: vote(f, item, name, bucket)
                else:
                    vote(f, v, name, bucket)
        except: pass  

    GROUPS = {
        "DNS Records": ["A", "MX", "NS", "TXT", "TXT Security"],
        "Domain Life": ["Creation Date", "Expiration Date"],
        "Infrastructure": ["Name Server", "Reverse Host", "IP Location", "Open Ports"],
        "Security": ["Zone Transfer", "WAF/CDN", "Server"],
    }
    flat = {}
    for f in {ff for gg in GROUPS.values() for ff in gg}:
        raw = best(bucket, f)
        if f in {"Creation Date", "Expiration Date"}:
            flat[f] = date_norm(raw) if raw else "-"
        else:
            flat[f] = raw or "-"

    if flat["A"] == "-" and flat["MX"] == "-" and flat["NS"] == "-":
        return DARK_RED + "Semua sumber DNS gagal / domain tidak ditemukan.\n" + RESET

    return render_blackarch(GROUPS, flat, bucket)

def render_blackarch(groups, data, bucket):
    col1, col2 = 26, 52
    line = RED + "+" + "-"*col1 + "+" + "-"*col2 + "+" + RESET

    header  = "\n"
    header += DARK_RED + "┌" + "─"*(col1+col2+1) + "┐\n"
    header += "│" + BRIGHT_RED + "  ⚡ ULTRA-DNS – 13 SOURCES  " + DARK_RED + "│\n"
    header += "└" + "─"*(col1+col2+1) + "┘\n" + RESET

    out = [header, line]
    for grp, fields in groups.items():
        out.append(RED + "|" + RESET + BRIGHT_RED + grp.center(col1+col2+1) + RESET + RED + "|" + RESET)
        out.append(line)
        for f in fields:
            val = data.get(f, "-")
            for idx, w in enumerate(textwrap.wrap(str(val), col2) or ["-"]):
                prefix = f if idx == 0 else ""
                out.append(RED + "|" + RESET + WHITE + f" {prefix}".ljust(col1) +
                           RED + "|" + RESET + WHITE + f" {w}".ljust(col2) + RED + "|" + RESET)
            out.append(line)
    conf = GREEN + " 13-src merged" + RESET
    out.append(RED + "|" + RESET + f"Confidence{RED}|{RESET}" + conf.ljust(col2) + RED + "|" + RESET)
    out.append(line)
    return "\n".join(out)

dns_lookup = super_dns

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    print(super_dns(sys.argv[1]))