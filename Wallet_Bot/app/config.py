import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "<YOUR_TELEGRAM_BOT_TOKEN>")
    CURRENCY_API_URL: str = os.getenv("CURRENCY_API_URL", "https://api.exchangerate-api.com/v4/latest/USD")

settings = Settings()
