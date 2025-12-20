import requests

def ip_geolocation(ip):
    url = (
        f"http://ip-api.com/json/{ip}"
        "?fields=status,message,continent,continentCode,"
        "country,countryCode,region,regionName,city,district,"
        "zip,lat,lon,timezone,offset,currency,"
        "isp,org,as,asname,reverse,mobile,proxy,hosting,query"
    )

    try:
        res = requests.get(url, timeout=5).json()
    except requests.RequestException:
        return {"error": "Gagal koneksi ke layanan geolocation"}

    if res.get("status") != "success":
        return {"error": res.get("message", "IP tidak valid atau diblok")}

    lat = res.get("lat")
    lon = res.get("lon")

    google_maps = (
        f"https://www.google.com/maps?q={lat},{lon}"
        if lat is not None and lon is not None
        else "N/A"
    )

    return {
        "ip": res.get("query"),
        "continent": res.get("continent"),
        "country": f"{res.get('country')} ({res.get('countryCode')})",
        "region": f"{res.get('regionName')} ({res.get('region')})",
        "city": res.get("city"),
        "district": res.get("district"),
        "zip": res.get("zip"),
        "timezone": res.get("timezone"),
        "utc_offset": res.get("offset"),
        "currency": res.get("currency"),
        "isp": res.get("isp"),
        "organization": res.get("org"),
        "asn": res.get("as"),
        "asn_name": res.get("asname"),
        "reverse_dns": res.get("reverse"),
        "mobile": res.get("mobile"),
        "proxy": res.get("proxy"),
        "hosting": res.get("hosting"),
        "latitude": lat,
        "longitude": lon,
        "google_maps": google_maps
    }
