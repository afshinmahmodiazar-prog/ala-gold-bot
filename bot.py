import os,re,requests
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN=os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL="@alagoold"

items={
"طلای ۱۸ عیار":"geram18",
"دلار":"price_dollar_rl",
"یورو":"price_eur",
"دینار عراق":"price_iqd",
"لیر ترکیه":"price_try"
}

H={"User-Agent":"Mozilla/5.0"}

def price(slug):
    r=requests.get(f"https://www.tgju.org/profile/{slug}",headers=H,timeout=30)
    r.raise_for_status()
    s=BeautifulSoup(r.text,"html.parser")

    for x in ["#last","#last-price",".last-price",".last","[data-field='last']"]:
        e=s.select_one(x)
        if e:
            n=re.sub(r"\D","",e.get_text())
            if n:return int(n)//10

    t=s.get_text(" ",strip=True)
    for p in [r"نرخ فعلی\s*([\d,]+)",r"آخرین قیمت\s*([\d,]+)"]:
        m=re.search(p,t)
        if m:return int(re.sub(r"\D","",m.group(1)))//10

    raise ValueError(f"قیمت {slug} پیدا نشد")

p={}

for name,slug in items.items():
    try:p[name]=price(slug)
    except Exception as e:print(name,e)

if not p.get("طلای ۱۸ عیار"):
    raise ValueError("قیمت طلا دریافت نشد")

time=datetime.now(ZoneInfo("Asia/Tehran")).strftime("%H:%M")

msg=f"""🟡 قیمت لحظه‌ای طلا و ارز

🟡 طلای ۱۸ عیار: {p.get("طلای ۱۸ عیار","نامشخص"):,} تومان
💵 دلار: {p.get("دلار","نامشخص"):,} تومان
💶 یورو: {p.get("یورو","نامشخص"):,} تومان
🇮🇶 دینار عراق: {p.get("دینار عراق","نامشخص"):,} تومان
🇹🇷 لیر ترکیه: {p.get("لیر ترکیه","نامشخص"):,} تومان

🕐 بروزرسانی: {time}

💎 زرگری ئالا
خرید و فروش آبشده و طلای دست دوم بدون اجرت

📞 09141661837
📞 09141661727
📞 09144407480

📲 @alagoold"""

r=requests.post(
 f"https://api.telegram.org/bot{TOKEN}/sendMessage",
 data={"chat_id":CHANNEL,"text":msg},
 timeout=30
)

print(r.text)
r.raise_for_status()
