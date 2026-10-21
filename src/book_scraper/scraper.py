
import requests
from bs4 import BeautifulSoup



import requests
from bs4 import BeautifulSoup


def get_website():
    url = "https://books.toscrape.com/"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    books_data = []

    for book in books:
        title = book.find("h3").find("a")["title"]
        price = book.find("p", class_="price_color").text.strip()
        price = price.replace("£", "")
        price = float(price)
        books_data.append({
            "title": title,
            "price": price
        })

    print(f"Всего книг: {len(books_data)}")

    for item in books_data:
        print(f'{item["title"]} — {item["price"]}')
    prices = []
    for book in books_data:
        prices.append(book["price"])
    if prices:
            average_price = sum(prices) / len(prices)

            print(f"Средняя цена: £{average_price:.2f}")
            print(f"Максимальная цена: £{max(prices):.2f}")
            print(f"Минимальная цена: £{min(prices):.2f}")