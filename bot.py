import requests

URL = "https://call1.tgju.org/ajax.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def find_items(obj, results):

    if isinstance(obj, dict):

        if "p" in obj and (
            "name" in obj or
            "slug" in obj or
            "title" in obj
        ):
            results.append(obj)

        for value in obj.values():
            find_items(value, results)

    elif isinstance(obj, list):

        for value in obj:
            find_items(value, results)


response = requests.get(
    URL,
    headers=HEADERS,
    timeout=30
)

response.raise_for_status()

data = response.json()

items = []

find_items(data, items)


unique = {}

for item in items:

    key = (
        item.get("name"),
        item.get("slug"),
        item.get("title")
    )

    unique[key] = item


items = list(unique.values())


print("====================================")
print("ALL TGJU PRICE RECORDS")
print("====================================")

for number, item in enumerate(items, 1):

    print("")
    print("RECORD:", number)
    print("NAME:", item.get("name"))
    print("SLUG:", item.get("slug"))
    print("TITLE:", item.get("title"))
    print("TITLE_EN:", item.get("title_en"))
    print("PRICE:", item.get("p"))
    print("------------------------------------")

print("")
print("TOTAL:", len(items))
print("====================================")
