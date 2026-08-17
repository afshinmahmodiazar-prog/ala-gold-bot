import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

URL = "https://www.tgju.org/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"
}

def get_price(page_id):
    url = f"https://www.tgju.org/profile/{page_id}"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # پیدا کردن مقدار قیمت در صفحه
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


# شناسه‌های TGJU
items = {
    "طلای ۱۸ عیار": "geram18",
    "آبشده نقدی": "abshodeh",
    "دلار": "price_dollar_rl",
    "یورو": "price_eur",
    "دینار عراق": "price_iqd",
    "لیر ترکیه": "price_try",
    "تتر": "price_usdt"
}

print("شروع دریافت قیمت‌ها...")

for name, page_id in items.items():
    try:
        rial_price = get_price(page_id)
        toman_price = rial_price // 10

        print(f"{name}: {toman_price:,} تومان")

    except Exception as e:
        print(f"{name}: ERROR -> {e}")

print("تست دریافت قیمت‌ها تمام شد.")
