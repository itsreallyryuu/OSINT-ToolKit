import requests
from urllib.parse import urlparse

RESET  = "\033[0m"
RED    = "\033[91m"      # border merah
BRIGHT_RED = "\033[91m"  # bisa juga pakai ini kalau mau lebih menyala
GREEN  = "\033[92m"
WHITE  = "\033[97m"
YELLOW = "\033[93m"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; OSINT Toolkit)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

PLATFORMS = {
    "GitHub": {"url": "https://github.com/{}", "not_found": ["not found", "404"]},
    "Instagram": {"url": "https://www.instagram.com/{}/", "not_found": ["sorry, this page isn't available", "page not found"]},
    "Twitter/X": {"url": "https://twitter.com/{}", "not_found": ["this account doesn’t exist", "page doesn’t exist"]},
    "TikTok": {"url": "https://www.tiktok.com/@{}", "not_found": ["couldn't find this account", "page not found"]},
    "Facebook": {"url": "https://www.facebook.com/{}", "not_found": ["content isn't available", "page isn't available"]},
    "Reddit": {"url": "https://www.reddit.com/user/{}", "not_found": ["nobody on reddit goes by that name", "page not found"]},
    "Medium": {"url": "https://medium.com/@{}", "not_found": ["404", "page not found"]},
    "Pinterest": {"url": "https://www.pinterest.com/{}/", "not_found": ["404", "page not found"]},
    "GitLab": {"url": "https://gitlab.com/{}", "not_found": ["404", "page not found"]},
    "Steam": {"url": "https://steamcommunity.com/id/{}", "not_found": ["could not be found", "profile not found"]},
    "Twitch": {"url": "https://www.twitch.tv/{}", "not_found": ["sorry. unless you’ve got a time machine", "page not found"]}
}

def check_username(username):
    col1, col2 = 16, 55
    line = RED + "+" + "-"*col1 + "+" + "-"*col2 + "+" + RESET

    table = line + "\n"
    table += RED + "|" + RESET + WHITE + " Platform".ljust(col1) + RESET
    table += RED + "|" + RESET + WHITE + " Status / Evidence".ljust(col2) + RESET
    table += RED + "|" + RESET + "\n"
    table += line + "\n"

    for name, data in PLATFORMS.items():
        url = data["url"].format(username)
        try:
            r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
            page = r.text.lower().replace("\n", " ").replace("\r", " ").strip()
            final_path = urlparse(r.url).path.lower()

            found = False
            if r.status_code == 200:
                for keyword in data["not_found"]:
                    if keyword.lower() in page:
                        found = False
                        break
                else:
                    if final_path in ["/", "/login", "/signup"]:
                        found = False
                    else:
                        found = True

            if found:
                status = GREEN + f" FOUND → {url}" + RESET
            else:
                status = RED + " NOT FOUND" + RESET

        except requests.RequestException:
            status = YELLOW + " ERROR / BLOCKED" + RESET

        table += (
            RED + "|" + RESET +
            WHITE + f" {name}".ljust(col1) + RESET +
            RED + "|" + RESET +
            status.ljust(col2) +
            RED + "|" + RESET + "\n"
        )
        table += line + "\n"

    return table
