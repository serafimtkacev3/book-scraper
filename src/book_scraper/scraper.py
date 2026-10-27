import json
from dataclasses import asdict
from collections import Counter, defaultdict
from collections import Counter
import requests
from bs4 import BeautifulSoup
from .books import Book


def get_website():
    url = "https://books.toscrape.com/"
    try:
     response = requests.get(url, timeout=10)
     response.raise_for_status()
     response.encoding = "utf-8"

    except requests.RequestException as error:
     print(f"Ошибка при получении сайта: {error}")
     return

    finally:
     print("Попытка подключения к сайту завершена")

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    books_data = []

    for book in books:
        title = book.find("h3").find("a")["title"]

        price = book.find("p", class_="price_color").text.strip()
        price = price.replace("£", "")
        price = float(price)

        books_data.append(
            Book(title=title, price=price)
        )

    print(f"Всего книг: {len(books_data)}")

    for item in books_data:
        print(f"{item.title} — £{item.price:.2f}")

    prices = []

    for book in books_data:
        prices.append(book.price)

    if prices:
        average_price = sum(prices) / len(prices)

        print(f"Средняя цена: £{average_price:.2f}")
        print(f"Максимальная цена: £{max(prices):.2f}")
        print(f"Минимальная цена: £{min(prices):.2f}")
    price_categories = []

    for book in books_data:
        if book.price < 20:
            price_categories.append("Дешёвые")
        elif book.price < 40:
            price_categories.append("Средние")
        else:
            price_categories.append("Дорогие")

    result = Counter(price_categories)

    print("Категории книг по цене:")

    for category, count in result.items():
        print(f"{category}: {count}")
        books_by_category = defaultdict(list)

    for book in books_data:
        if book.price < 20:
            category = "Дешёвые"
        elif book.price < 40:
            category = "Средние"
        else:
            category = "Дорогие"

        books_by_category[category].append(book.title)

    print("\nКниги по категориям:")

    for category, titles in books_by_category.items():
        print(f"\n{category}:")

        for title in titles:
            print(f" - {title}")
    books_for_json = []

    for book in books_data:
        books_for_json.append(asdict(book))

    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(books_for_json, file, ensure_ascii=False, indent=4)

    print("Книги успешно сохранены в books.json")
    with open("books.json", "r", encoding="utf-8") as file:
        loaded_books = json.load(file)

        print(f"Загружено книг из JSON: {len(loaded_books)}")

        print("Первая книга:")
        print(loaded_books[0]["title"])
        print(loaded_books[0]["price"])
            