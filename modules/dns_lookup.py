import dns.resolver

RESET  = "\033[0m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"

def render_section(title, records):
    output = CYAN + f"\n[{title} RECORDS]\n" + RESET
    if not records:
        return output + RED + "Not found\n" + RESET

    for r in records:
        output += GREEN + "- " + WHITE + str(r) + RESET + "\n"
    return output

def dns_lookup(domain):
    record_types = ["A", "MX", "NS", "TXT"]
    result = CYAN + f"Target Domain : {domain}\n" + RESET

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            result += render_section(rtype, answers)
        except:
            result += render_section(rtype, None)

    return result
