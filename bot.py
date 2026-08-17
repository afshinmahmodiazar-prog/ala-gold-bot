import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = "@alagoold"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"
}


def get_price(page_id):
    url = f"https://www.tgju.org/profile/{page_id}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    selectors = [
        "span.value",
        "span.price",
        ".price",
        ".value"
    ]

    for selector in selectors:
        element = soup.select_one(selector)

        if element:
            text = element.get_text(" ", strip=True)
            numbers = re.sub(r"[^\d]", "", text)

            if numbers:
                return int(numbers)

    raise ValueError(f"Price not found: {page_id}")


items = {
    "طلای ۱۸ عیار": "geram18",
    "دلار": "price_dollar_rl",
    "یورو": "price_eur",
    "دینار عراق": "price_iqd",
    "لیر ترکیه": "price_try"
}


prices = {}

for name, page_id in items.items():
    rial_price = get_price(page_id)
    prices[name] = rial_price // 10


iran_time = datetime.now(
    ZoneInfo("Asia/Tehran")
).strftime("%H:%M")


message = f"""🟡 قیمت لحظه‌ای طلا و ارز

🟡 طلای ۱۸ عیار: {prices["طلای ۱۸ عیار"]:,} تومان

💵 دلار: {prices["دلار"]:,} تومان
💶 یورو: {prices["یورو"]:,} تومان
🇮🇶 دینار عراق: {prices["دینار عراق"]:,} تومان
🇹🇷 لیر ترکیه: {prices["لیر ترکیه"]:,} تومان

🕐 آخرین بروزرسانی: {iran_time}

💎 زرگری ئالا

خرید و فروش آبشده و طلای دست دوم بدون اجرت

📞 تماس:
09141661837
09141661727
09144407480

📲 @alagoold
"""


telegram_url = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
)

response = requests.post(
    telegram_url,
    data={
        "chat_id": CHANNEL,
        "text": message
    },
    timeout=30
)

print("Telegram status:", response.status_code)
print("Telegram response:", response.text)

response.raise_for_status()
