import os
import requests
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# فعلاً برای تست اتصال به API
API_URL = "https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json"

def get_prices():
    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()
    return response.json()

try:
    data = get_prices()

    print("API CONNECTED")
    print(data)

except Exception as e:
    print("API ERROR:", e)
    raise
