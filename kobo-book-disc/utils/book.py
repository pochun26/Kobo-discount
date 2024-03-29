
class Book:
    def __init__(self, title, price, discount) -> None:
        self.title = title
        self.price = price
        self.discount = discount

    def __repr__(self) -> str:
        s = f"{self.title} {self.price}({self.discount}%)"
        return s

    def __gt__(self, b):
        return self.price > b.price