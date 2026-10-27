
import asyncio
import aiohttp
import json
import time
import logging
import hashlib

from datetime import datetime
from dataclasses import asdict
from bs4 import BeautifulSoup
from .books import Book


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Создание SHA-256 хеша книги
def get_book_hash(book):
    book_data = f'{book["title"]}|{book["price"]:.2f}'

    return hashlib.sha256(
        book_data.encode("utf-8")
    ).hexdigest()


# Асинхронное получение одной страницы
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

            price = book.find(
                "p", class_="price_color"
            ).text.strip()

            price = float(price.replace("£", ""))

            books_data.append(
                Book(title=title, price=price)
            )

        logger.info(
            f"Страница {page_number}: найдено {len(books_data)} книг"
        )

        return books_data

    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        logger.error(
            f"Ошибка на странице {page_number}: {error}"
        )
        return []

    finally:
        print(f"Обработка страницы {page_number} завершена")


# Главная функция парсера
async def main():
    start_time = time.perf_counter()
    logger.info("Парсер запущен")

    timeout = aiohttp.ClientTimeout(total=15)

    # Получаем три страницы асинхронно
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            get_page(session, 1),
            get_page(session, 2),
            get_page(session, 3)
        ]

        results = await asyncio.gather(*tasks)

    # Проверяем количество книг на страницах
    for page_number, page_books in enumerate(results, start=1):
        print(
            f"Проверка страницы {page_number}: "
            f"{len(page_books)} книг"
        )

    # Защита от сохранения неполных данных
    if any(len(page_books) != 20 for page_books in results):
        logger.warning(
            "Не все страницы загружены полностью. "
            "Сохранение отменено."
        )
        return

    # Объединяем книги со всех страниц
    all_books = []

    for page_books in results:
        all_books.extend(page_books)

    print(f"\nВсего собрано книг: {len(all_books)}")

    # Рассчитываем статистику
    prices = [book.price for book in all_books]

    print(f"Средняя цена: £{sum(prices) / len(prices):.2f}")
    print(f"Максимальная цена: £{max(prices):.2f}")
    print(f"Минимальная цена: £{min(prices):.2f}")

    # Преобразуем Book в словари
    books_for_json = []

    for book in all_books:
        books_for_json.append(asdict(book))

    # Загружаем данные предыдущего запуска
    try:
        with open("async_books.json", "r", encoding="utf-8") as file:
            old_books = json.load(file)

    except FileNotFoundError:
        old_books = []

    # Создаём хеши старых книг
    old_hashes = {}

    for book in old_books:
        old_hashes[book["title"]] = get_book_hash(book)

    # Создаём списки изменений
    new_books = []
    changed_books = []

    # Сравниваем текущие и предыдущие данные
    for book in books_for_json:
        title = book["title"]
        new_hash = get_book_hash(book)

        if title not in old_hashes:
            new_books.append(title)

        elif old_hashes[title] != new_hash:
            changed_books.append(title)

    print(f"\nСтарых книг в JSON: {len(old_books)}")
    print(f"Хешей в словаре: {len(old_hashes)}")
    print(f"Новых книг получено: {len(books_for_json)}")

    print(f"Новых книг: {len(new_books)}")
    print(f"Изменённых книг: {len(changed_books)}")

    # Сохраняем актуальные данные
    with open("async_books.json", "w", encoding="utf-8") as file:
        json.dump(
            books_for_json,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("Все книги сохранены в async_books.json")

    # Измеряем время выполнения
    execution_time = time.perf_counter() - start_time

    logger.info(
        f"Парсер завершён за {execution_time:.2f} секунд"
    )

    # Формируем запись истории запуска
    run_log = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "books_count": len(all_books),
        "execution_time": round(execution_time, 2),
        "new_books": len(new_books),
        "changed_books": len(changed_books)
    }

    # Читаем историю предыдущих запусков
    try:
        with open("runs.json", "r", encoding="utf-8") as file:
            runs = json.load(file)

    except FileNotFoundError:
        runs = []

    # Добавляем новый запуск в историю
    runs.append(run_log)

    # Сохраняем историю
    with open("runs.json", "w", encoding="utf-8") as file:
        json.dump(
            runs,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("История запусков сохранена в runs.json")


# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
