import configparser
from app import app
import os


class SettingsError(Exception):
    def __init__(self, message="Settings error"):
        self.message = message
        super().__init__(self.message)


class Settings:
    def __init__(self, config_name="config.ini") -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_name)
        app.logger.setLevel(self.config["DEFAULT"].get("log_level", "INFO").upper())
        self.max_workers = self.config["DEFAULT"].getint("max_workers")
        app.logger.debug(f"{config_name} readed")

        if os.environ.get("KOBO_SESSION") is None:
            app.logger.error("KOBO_SESSION is None")
            raise SettingsError("KOBO_SESSION is None")

        self.kobo_cookies = "KoboSession=" + os.environ.get("KOBO_SESSION")
