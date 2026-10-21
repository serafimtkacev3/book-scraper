def get_books():
	books = [
		{"title": "Python", "price": 850},
		{"title": "Java", "price": 1200},
		{"title": "C++", "price": 700},
	    {"title": "JavaScript", "price": 950},
    ]
	return books
def get_cheap_books(max_price):
    books = get_books()
    cheap_books = []

    for book in books:
        if book["price"] < max_price:
           cheap_books.append(book)

    return cheap_books