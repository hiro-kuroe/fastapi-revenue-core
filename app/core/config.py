from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "FastAPI Revenue Core"
    ENV: str = "local"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str

    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_PRICE_ID: str

    model_config = {
        "env_file" : ".env",
        "case_sensitive" : True,
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()