import asyncio
from datetime import datetime

from .async_scraper import main


async def scheduler():
    interval = 10

    while True:
        print(f"\nЗапуск парсера: {datetime.now()}")

        try:
            await main()

        except Exception as error:
            print(f"Ошибка парсера: {error}")

        print("Ожидаем следующего запуска...")
        await asyncio.sleep(interval)


if __name__ == "__main__":
    try:
        asyncio.run(scheduler())

    except KeyboardInterrupt:
        print("\nАвтоматический парсинг остановлен")