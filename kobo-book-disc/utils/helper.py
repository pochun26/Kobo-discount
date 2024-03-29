import re
from app import app


def extract_price(price):
    return int(re.search(r"\d{1,3}(?:,\d{3})*", price).group(0).replace(",", ""))
    

def discount_calculator(now_price, was_price) -> int:
    try:
        now_price = extract_price(now_price)
        was_price = extract_price(was_price)
        percentage = int((1 - now_price/was_price)*100)
    except ValueError as e:
        app.logger.error(f"Discount calculator error {e}")
        return 0
    return percentage


def sort_books(books):
    if app.settings.sort == "price":
        app.logger.debug("Sort by price")
        books.sort()
    elif app.settings.sort == "discount":
        app.logger.debug("Sort by discount")
        books.sort(key=lambda book: book.discount, reverse=True)


def log_books(books):
    for b in books:
        app.logger.info(b)
