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


def find_items(obj, results):
    if isinstance(obj, dict):

        # اگر این بخش یک رکورد قیمت باشد
        if "p" in obj and (
            "name" in obj or
            "slug" in obj or
            "title" in obj
        ):
            results.append(obj)

        # ادامه جستجو در تمام بخش‌های داخل آن
        for value in obj.values():
            find_items(value, results)

    elif isinstance(obj, list):

        for value in obj:
            find_items(value, results)


data = get_data()

print("====================================")
print("TGJU DATA RECEIVED")
print("====================================")


items = []

find_items(data, items)


# حذف رکوردهای تکراری
unique_items = {}

for item in items:

    key = (
        str(item.get("name", "")),
        str(item.get("slug", "")),
        str(item.get("title", ""))
    )

    unique_items[key] = item


items = list(unique_items.values())


print("تعداد رکوردهای قیمت:", len(items))
print("====================================")


keywords = [
    "gold",
    "geram",
    "18",
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
print("تعداد موارد مرتبط:", found)
print("====================================")
print("تست TGJU تمام شد.")
