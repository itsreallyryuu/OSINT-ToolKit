import requests
import hashlib

def _hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

def asset_snapshot(url):
    try:
        r = requests.get(url, timeout=5)
        return {
            "status_code": r.status_code,
            "headers_hash": _hash(str(r.headers)),
            "body_hash": _hash(r.text[:2000])
        }
    except:
        return None

def compare_snapshot(old, new):
    if not old or not new:
        return "UNKNOWN"

    changes = []

    if old["status_code"] != new["status_code"]:
        changes.append("STATUS_CODE_CHANGED")

    if old["headers_hash"] != new["headers_hash"]:
        changes.append("HEADERS_CHANGED")

    if old["body_hash"] != new["body_hash"]:
        changes.append("CONTENT_CHANGED")

    return changes if changes else ["NO_CHANGE"]
