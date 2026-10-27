FROM python:3.12-slim

WORKDIR /app

COPY src/ ./src/

RUN pip install --no-cache-dir aiohttp beautifulsoup4

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "book_scraper.async_scraper"]