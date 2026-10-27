from dataclasses import dataclass


@dataclass
class Book:
    title: str
    price: float


def get_price_category(price: float) -> str:
    if price < 20:
        return "Дешёвые"
    elif price < 40:
        return "Средние"
    else:
        return "Дорогие"


def get_books():
    books = [
        Book(title="Python", price=850),
        Book(title="Java", price=1200),
        Book(title="C++", price=700),
        Book(title="JavaScript", price=950),
    ]
    return books


def get_cheap_books(max_price):
    books = get_books()
    cheap_books = []

    for book in books:
        if book.price < max_price:
            cheap_books.append(book)

    return cheap_books
if __name__ == "__main__":
    cheap_books = get_cheap_books(900)

    for book in cheap_books:
        print(book.title, book.price)