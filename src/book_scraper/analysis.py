import pandas as pd

df = pd.read_json("async_books.json")

print(df.head())
print(df["price"].mean())
expensive_books = df[df["price"] > 40]

print("\nКниги дороже £40:")
print(expensive_books)
top_books = df.sort_values(
    by="price",
    ascending=False
).head(5)

print("\nТОП-5 самых дорогих книг:")
print(top_books)
print("\nПропущенные значения:")
print(df.isnull().sum())

print("\nОсновная статистика:")
print(df.describe())