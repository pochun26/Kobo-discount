import logging
import sys


class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

    def set_logfile(self, file_name="kobo-book-disc.log"):
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
        self.logger.debug(f"log file: {file_name}")
