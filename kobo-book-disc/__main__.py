import argparse
from app import app
from settings import Settings
from logger import Logger
from worker import Worker
import concurrent.futures
from utils.helper import sort_books, log_books


def main():
    executor = concurrent.futures.ThreadPoolExecutor(app.settings.max_workers)

    # page 1
    w = Worker()
    future = executor.submit(w.run)
    books = future.result()
    total_pages = w.total_pages
    app.logger.debug(f"Total pages: {total_pages}")

    # page 2~n
    futures = []
    for i in range(2, total_pages+1):
        futures.append(executor.submit(Worker(i).run))
    concurrent.futures.wait(futures, 30, concurrent.futures.ALL_COMPLETED)
    for f in futures:
        books.extend(f.result())

    if not books:
        app.logger.info("Book list is empty")
        return

    sort_books(books)
    log_books(books)


if __name__ == "__main__":
    app_logger = Logger()
    app.logger = app_logger.logger
    app.settings = Settings("config.ini")
    app_logger.set_logfile("kobo-book-disc.log")

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sort", choices=["price", "discount"], default="price", help="sort books by price or discount")
    parser.add_argument("-a", "--all", action="store_true", help="List all books")
    args = parser.parse_args()
    app.settings.sort = args.sort
    app.settings.show_all = args.all
    main()
