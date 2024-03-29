import re
from app import app


def discount_calculator(now_price, was_price) -> int:
    try:
        now_price = int(re.search(r"\d+", now_price).group(0))
        was_price = int(re.search(r"\d+", was_price).group(0))
        percentage = int((1 - now_price/was_price)*100)
    except ValueError as e:
        app.logger.error(f"Discount calculator error {e}")
        return 0
    return percentage
