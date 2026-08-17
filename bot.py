import requests
from bs4 import BeautifulSoup

URL = "https://www.tgju.org/profile/geram18"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

price = soup.select_one("#l-geram18")

if price:
    print("GOLD 18K:", price.get_text(strip=True))
else:
    print("GOLD PRICE NOT FOUND")
