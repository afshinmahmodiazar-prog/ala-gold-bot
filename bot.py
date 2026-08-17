import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = "@alagoold"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36",
    "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8"
}


ITEMS = {
    "طلای ۱۸ عیار": "geram18",
    "دلار": "price_dollar_rl",
    "یورو": "price_eur",
    "دینار عراق": "price_iqd",
    "لیر ترکیه": "price_try"
}


def get_price(name, page_id):

    url = f"https://www.tgju.org/profile/{page_id}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # روش‌های مختلف پیدا کردن نرخ فعلی TGJU
    selectors = [
        "#last",
        "#last-price",
        ".last-price",
        ".last",
        "[data-field='last']",
        "[data-field='p']"
    ]

    for selector in selectors:

        element = soup.select_one(selector)

        if element:

            text = element.get_text(
                " ",
                strip=True
            )

            numbers = re.sub(
                r"[^\d]",
                "",
                text
            )

            if numbers:

                print(
                    name,
                    "=>",
                    numbers
                )

                return int(numbers)

    # جستجوی متنی برای «نرخ فعلی»
    text = soup.get_text(
        " ",
        strip=True
    )

    patterns = [
        r"نرخ فعلی\s*([0-9,]+)",
        r"آخرین قیمت\s*([0-9,]+)",
        r"قیمت فعلی\s*([0-9,]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            numbers = re.sub(
                r"[^\d]",
                "",
                match.group(1)
            )

            if numbers:

                print(
                    name,
                    "=>",
                    numbers
                )

                return int(numbers)

    raise ValueError(
        f"قیمت فعلی {name} پیدا نشد"
    )


prices = {}

print("================================")
print("شروع دریافت قیمت‌ها")
print("================================")


for name, page_id in ITEMS.items():

    try:

        rial_price = get_price(
            name,
            page_id
        )

        toman_price = rial_price // 10

        prices[name] = toman_price

    except Exception as error:

        print(
            name,
            "ERROR:",
            error
        )


print("================================")
print("قیمت‌های دریافت‌شده:")
print(prices)
print("================================")


if "طلای ۱۸ عیار" not in prices:
    raise ValueError(
        "قیمت طلای ۱۸ عیار دریافت نشد"
    )


iran_time = datetime.now(
    ZoneInfo("Asia/Tehran")
).strftime("%H:%M")


message = f"""🟡 قیمت لحظه‌ای طلا و ارز

🟡 طلای ۱۸ عیار:
{prices.get("طلای ۱۸ عیار", "نامشخص"):,} تومان

💵 دلار:
{prices.get("دلار", "نامشخص"):,} تومان

💶 یورو:
{prices.get("یورو", "نامشخص"):,} تومان

🇮🇶 دینار عراق:
{prices.get("دینار عراق", "نامشخص"):,} تومان

🇹🇷 لیر ترکیه:
{prices.get("لیر ترکیه", "نامشخص"):,} تومان

🕐 آخرین بروزرسانی:
{iran_time}

💎 زرگری ئالا

خرید و فروش آبشده و طلای دست دوم بدون اجرت

📞 تماس:
09141661837
09141661727
09144407480

📲 @alagoold
"""


telegram_url = (
    f"https://api.telegram.org/"
    f"bot{BOT_TOKEN}/sendMessage"
)


response = requests.post(
    telegram_url,
    data={
        "chat_id": CHANNEL,
        "text": message
    },
    timeout=30
)


print("================================")
print("Telegram status:", response.status_code)
print(response.text)
print("================================")


response.raise_for_status()

print("پیام با موفقیت ارسال شد.")
