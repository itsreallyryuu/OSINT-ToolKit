import requests

RESET  = "\033[0m"
RED    = "\033[91m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
YELLOW = "\033[93m"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (OSINT Toolkit)"
}

PLATFORMS = {
    "GitHub": {
        "url": "https://github.com/{}",
        "not_found": "Not Found"
    },
    "Instagram": {
        "url": "https://www.instagram.com/{}/",
        "not_found": "Sorry, this page isn't available"
    },
    "Twitter/X": {
        "url": "https://twitter.com/{}",
        "not_found": "This account doesn’t exist"
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@{}",
        "not_found": "Couldn't find this account"
    },
    "Facebook": {
        "url": "https://www.facebook.com/{}",
        "not_found": "content isn't available"
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{}",
        "not_found": "Sorry, nobody on Reddit goes by that name"
    },
    "Medium": {
        "url": "https://medium.com/@{}",
        "not_found": "404"
    },
    "Pinterest": {
        "url": "https://www.pinterest.com/{}/",
        "not_found": "404"
    },
    "GitLab": {
        "url": "https://gitlab.com/{}",
        "not_found": "404"
    },
    "Steam": {
        "url": "https://steamcommunity.com/id/{}",
        "not_found": "The specified profile could not be found"
    },
    "Twitch": {
        "url": "https://www.twitch.tv/{}",
        "not_found": "Sorry. Unless you’ve got a time machine"
    }
}

def check_username(username):
    col1, col2 = 16, 55
    line = CYAN + "+" + "-"*col1 + "+" + "-"*col2 + "+" + RESET

    table = line + "\n"
    table += CYAN + "|" + RESET + " Platform".ljust(col1)
    table += CYAN + "|" + RESET + " Status / Evidence".ljust(col2)
    table += CYAN + "|" + RESET + "\n"
    table += line + "\n"

    for name, data in PLATFORMS.items():
        url = data["url"].format(username)

        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            page = r.text.lower()

            if r.status_code == 200 and data["not_found"].lower() not in page:
                status = GREEN + f" FOUND → {url}" + RESET
            else:
                status = RED + " NOT FOUND" + RESET

        except requests.RequestException:
            status = YELLOW + " ERROR / BLOCKED" + RESET

        table += (
            CYAN + "|" + RESET +
            WHITE + f" {name}".ljust(col1) + RESET +
            CYAN + "|" + RESET +
            status.ljust(col2) +
            CYAN + "|" + RESET + "\n"
        )

        table += line + "\n"

    return table
