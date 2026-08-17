import requests

URL = "https://www.tgju.org/profile/geram18"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"
}

try:
    r = requests.get(URL, headers=headers, timeout=30)

    print("STATUS:", r.status_code)
    print("LENGTH:", len(r.text))

    if r.status_code == 200:
        print("TGJU CONNECTION OK")
    else:
        print("TGJU CONNECTION FAILED")

except Exception as e:
    print("ERROR:", repr(e))
    raise
