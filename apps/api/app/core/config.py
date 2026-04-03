from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GEO AI Visibility API"
    app_env: str = "dev"
    app_debug: bool = True
    secret_key: str = "change-this-in-production"
    access_token_expire_minutes: int = 60 * 24

    database_url: str = "postgresql+psycopg://geo:geo@localhost:5432/geo_db"
    redis_url: str = "redis://localhost:6379/0"
    broker_url: str = "redis://localhost:6379/0"
    result_backend: str = "redis://localhost:6379/1"

    admin_username: str = "admin"
    admin_password: str = "admin123"

    model_default: str = "gpt-4o"
    model_fallback: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

