import requests

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "Twitter/X": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "Facebook": "https://www.facebook.com/{}",
    "Threads": "https://www.threads.net/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}",
    "Dev.to": "https://dev.to/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Steam": "https://steamcommunity.com/id/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Telegram": "https://t.me/{}"
}


HEADERS = {
    "User-Agent": "Mozilla/5.0 (OSINT Toolkit)"
}

def footprint_analyzer(username):
    findings = []

    for name, url in PLATFORMS.items():
        try:
            r = requests.get(url.format(username), headers=HEADERS, timeout=5)
            if r.status_code == 200:
                findings.append({
                    "platform": name,
                    "url": url.format(username),
                    "confidence": "HIGH"
                })
        except:
            pass

    confidence = "LOW"
    if len(findings) >= 3:
        confidence = "HIGH"
    elif len(findings) == 2:
        confidence = "MEDIUM"

    return {
        "username": username,
        "profiles_found": findings,
        "overall_confidence": confidence
    }
