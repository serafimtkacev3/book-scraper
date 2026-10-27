import hashlib


def get_hash(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


old_book = "Python — 30"
new_book = "Python — 40"

old_hash = get_hash(old_book)
new_hash = get_hash(new_book)

if old_hash == new_hash:
    print("Данные не изменились")
else:
    print("Обнаружены изменения!")