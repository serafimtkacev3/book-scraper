
# Book Scraper

Учебный Python-проект для сбора и анализа информации о книгах с сайта Books to Scrape.

## Возможности

- Парсинг HTML с помощью requests и BeautifulSoup
- Асинхронный сбор данных через aiohttp и asyncio
- Обработка ошибок через try/except/finally
- Использование dataclass, Counter и defaultdict
- Сохранение результатов в JSON
- Логирование работы программы
- Измерение времени выполнения
- Построение графиков через matplotlib
- Запуск в Docker

## Установка

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Активировать его в Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить проект:

```powershell
python -m pip install -e .
```

## Запуск парсера

```powershell
python -m book_scraper.async_scraper
```

Парсер собирает книги с трёх страниц сайта и сохраняет результат в async_books.json.

## Построение графиков

```powershell
python -m book_scraper.charts
```

## Запуск через Docker

Собрать образ:

```powershell
docker build -t book-scraper .
```

Запустить контейнер:

```powershell
docker run --rm -v "${PWD}:/data" -w /data book-scraper
```

## Результаты

При успешном выполнении программа собирает 60 книг, рассчитывает среднюю, минимальную и максимальную цену и сохраняет данные в JSON.
