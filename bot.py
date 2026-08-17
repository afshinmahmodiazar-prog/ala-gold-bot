import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = "@alagoold"

message = """🟡 قیمت لحظه‌ای طلا و ارز

🔸 طلای ۱۸ عیار: XXXXX تومان
💵 دلار آزاد: XXXXX تومان

🕐 آخرین بروزرسانی: تست

💎 زرگری ئالا

خرید و فروش آبشده و طلای دست دوم بدون اجرت

📞 تماس:
09141661837
09141661727
09144407480

📲 @alagoold
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHANNEL,
        "text": message
    },
    timeout=30
)

print("Telegram status:", response.status_code)
print("Telegram response:", response.text)

response.raise_for_status()
