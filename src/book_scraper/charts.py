import json
import matplotlib.pyplot as plt


def create_chart():
    with open("async_books.json", "r", encoding="utf-8") as file:
        books = json.load(file)

    prices = []

    for book in books:
        prices.append(book["price"])

    plt.hist(prices, bins=10, edgecolor="black")

    plt.title("Распределение цен книг")
    plt.xlabel("Цена (£)")
    plt.ylabel("Количество книг")

    plt.tight_layout()
    plt.show()
    cheap = 0
    medium = 0
    expensive = 0

    for price in prices:
        if price < 20:
            cheap += 1
        elif price < 40:
            medium += 1
        else:
            expensive += 1

    categories = ["Дешёвые", "Средние", "Дорогие"]
    counts = [cheap, medium, expensive]

    plt.figure(figsize=(8, 5))

    plt.bar(categories, counts)

    plt.title("Количество книг по категориям")
    plt.xlabel("Категория")
    plt.ylabel("Количество книг")

    plt.tight_layout()
    plt.savefig("price_categories.png")
    plt.show()

if __name__ == "__main__":
    create_chart()