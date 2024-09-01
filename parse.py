import requests
from bs4 import BeautifulSoup
from statistics import mean

def get_avg_price(brand, model, year):
    query = f"{brand} {model} {year}"
    url = f"https://www.avito.ru/rossiya/avtomobili?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    prices = []
    for item in soup.find_all('span', class_='price-text'):
        price_text = item.get_text(strip=True).replace("₽", "").replace(" ", "")
        try:
            prices.append(int(price_text))
        except ValueError:
            continue

    if prices:
        return mean(prices)
    else:
        return 0

