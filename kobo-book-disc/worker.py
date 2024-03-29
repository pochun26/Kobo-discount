import requests
from app import app
from utils.helper import discount_calculator
from utils.book import Book


class Worker:
    def __init__(self, page=1) -> None:
        self.page = page

    def run(self):
        results = []
        url = "https://www.kobo.com/account/wishlist/fetch"
        payload = {"pageIndex": self.page}
        headers = {
            "cookie": app.settings.kobo_cookies,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }

        r = requests.post(url, json=payload, headers=headers)
        if r.status_code == 200:
            data = r.json()
            self.total_pages = data.get("TotalNumPages")
            for d in data.get("Items", []):
                if d["WasPrice"] is not None:
                    results.append(Book(d["Title"], d["Price"], discount_calculator(d["Price"], d["WasPrice"])))
        else:
            app.logger.error(f"Request error {r.status_code}")

        return results
