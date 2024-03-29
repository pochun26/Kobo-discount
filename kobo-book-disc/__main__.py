from app import app
from settings import Settings
from logger import Logger
from worker import Worker
import concurrent.futures


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

    books.sort()
    for b in books:
        app.logger.info(b)


if __name__ == "__main__":
    app_logger = Logger()
    app.logger = app_logger.logger
    app.settings = Settings("config.ini")
    app_logger.set_logfile("kobo-book-disc.log")

    main()
