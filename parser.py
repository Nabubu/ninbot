import requests
import json

def fetch_eshop_prices(region="US"):
    currency = {
        "US": "USD",
        "CA": "CAD",
        "PL": "PLN",
        "JP": "JPY"
    }.get(region.upper(), "USD")

    url = f"https://eshop-prices.com/games.json?currency={currency}"

    print(f"📥 Получаю игры для региона {region}...")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Ошибка при получении данных")

    data = response.json()
    result = []
    for item in data:
        try:
            result.append({
                "title": item["title"],
                "price": float(item["price"]),
                "region": region.upper(),
                "url": item["url"]
            })
        except Exception:
            continue

    with open("data/games.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"✅ Сохранено {len(result)} игр в data/games.json")

if __name__ == "__main__":
    fetch_eshop_prices("US")
