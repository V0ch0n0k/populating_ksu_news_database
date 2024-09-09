from functools import lru_cache
import os

from dotenv import load_dotenv

load_dotenv()

__all__ = ["get_settings", "clear_cache_settings"]


class Settings:

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    BASE_RESOURCE_PATH = os.getenv("BASE_RESOURCE_PATH") or "../resources"

    def get_db_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def clear_cache_settings():
    get_settings.cache_clear()
