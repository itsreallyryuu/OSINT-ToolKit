import socket
import dns.resolver
import requests

def attack_surface_mapper(domain):
    result = {
        "domain": domain,
        "ip_addresses": [],
        "subdomains": [],
        "dns_records": {},
        "hosting": "Unknown",
        "cdn": "Unknown"
    }

    
    try:
        result["ip_addresses"] = list(
            set([socket.gethostbyname(domain)])
        )
    except:
        pass

    
    for rtype in ["A", "MX", "NS", "TXT"]:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            result["dns_records"][rtype] = [str(r) for r in answers]
        except:
            result["dns_records"][rtype] = []

    
    common_subs = ["www", "mail", "api", "dev", "test"]
    for sub in common_subs:
        try:
            host = f"{sub}.{domain}"
            socket.gethostbyname(host)
            result["subdomains"].append(host)
        except:
            pass

    
    try:
        r = requests.get(f"http://{domain}", timeout=5)
        server = r.headers.get("Server", "").lower()

        if "cloudflare" in server:
            result["cdn"] = "Cloudflare"
        else:
            result["hosting"] = server or "Unknown"
    except:
        pass

    return result
