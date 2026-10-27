import time
import logging
import asyncio
import aiohttp
import json

from dataclasses import asdict
from bs4 import BeautifulSoup
from .books import Book

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
async def get_page(session, page_number):
    url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"

    try:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text(encoding="utf-8")

        soup = BeautifulSoup(html, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        books_data = []

        for book in books:
            title = book.find("h3").find("a")["title"]
            price = book.find("p", class_="price_color").text.strip()
            price = float(price.replace("£", ""))

            books_data.append(
                Book(title=title, price=price)
            )

        logger.info(f"Страница {page_number}: найдено {len(books_data)} книг")
        return books_data

    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        print(f"Ошибка на странице {page_number}: {error}")
        return []

    finally:
        print(f"Обработка страницы {page_number} завершена")


async def main():
    start_time = time.perf_counter()
    logger.info("Парсер запущен")
    timeout = aiohttp.ClientTimeout(total=15)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            get_page(session, 1),
            get_page(session, 2),
            get_page(session, 3)
        ]

        results = await asyncio.gather(*tasks)

    all_books = []

    for page_books in results:
        all_books.extend(page_books)

    print(f"\nВсего собрано книг: {len(all_books)}")

    if all_books:
        prices = [book.price for book in all_books]

        print(f"Средняя цена: £{sum(prices) / len(prices):.2f}")
        print(f"Максимальная цена: £{max(prices):.2f}")
        print(f"Минимальная цена: £{min(prices):.2f}")


    books_for_json = []

    for book in all_books:
        books_for_json.append(asdict(book))

    with open("async_books.json", "w", encoding="utf-8") as file:
        json.dump(books_for_json, file, ensure_ascii=False, indent=4)

    print("Все книги сохранены в async_books.json")
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    logger.info(f"Парсер завершён за {execution_time:.2f} секунд")


if __name__ == "__main__":
    asyncio.run(main())
