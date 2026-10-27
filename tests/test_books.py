from book_scraper.books import get_price_category


def test_cheap_book():
    assert get_price_category(15) == "Дешёвые"


def test_medium_book():
    assert get_price_category(30) == "Средние"


def test_expensive_book():
    assert get_price_category(50) == "Дорогие"


def test_price_boundaries():
    assert get_price_category(20) == "Средние"
    assert get_price_category(40) == "Дорогие"