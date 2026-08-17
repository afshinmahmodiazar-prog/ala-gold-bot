import requests

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

print("====================================")
print("TGJU DATA RECEIVED")
print("====================================")


# پیدا کردن لیست اطلاعات
items = []

if isinstance(data, list):
    items = data

elif isinstance(data, dict):
    for key in ["data", "results", "items"]:
        if isinstance(data.get(key), list):
            items = data[key]
            break


print("تعداد رکوردها:", len(items))
print("====================================")


# نمایش رکوردهای مربوط به طلا و ارز
keywords = [
    "gold",
    "geram",
    "dollar",
    "usd",
    "eur",
    "euro",
    "iqd",
    "iraq",
    "dinar",
    "try",
    "turkey",
    "lira",
    "لیر",
    "دلار",
    "یورو",
    "دینار",
    "طلا"
]


found = 0


for item in items:

    if not isinstance(item, dict):
        continue

    name = str(item.get("name", ""))
    slug = str(item.get("slug", ""))
    title = str(item.get("title", ""))
    title_en = str(item.get("title_en", ""))

    text = (
        name + " " +
        slug + " " +
        title + " " +
        title_en
    ).lower()

    if any(keyword.lower() in text for keyword in keywords):

        print(
            "NAME:",
            name,
            "| SLUG:",
            slug,
            "| TITLE:",
            title,
            "| PRICE:",
            item.get("p")
        )

        found += 1


print("====================================")
print("تعداد موارد پیدا شده:", found)
print("تست TGJU تمام شد.")
print("====================================")
