import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = "@alagoold"

URL = "https://call1.tgju.org/ajax.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def get_data():
    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


data = get_data()

print("TGJU DATA RECEIVED")
print(type(data))

if isinstance(data, dict):
    print("DATA KEYS:")
    print(list(data.keys())[:100])

print(data)


print("تست دریافت اطلاعات TGJU تمام شد.")
