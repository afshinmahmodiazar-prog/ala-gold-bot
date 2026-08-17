import requests

url = "https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("STATUS:", response.status_code)
    print("CONTENT:")
    print(response.text[:10000])

    response.raise_for_status()

except Exception as e:
    print("ERROR:", repr(e))
    raise
