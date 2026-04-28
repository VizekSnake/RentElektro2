import os

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    APP_NAME: str = "RentElektroAPI"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    AUTO_CREATE_SCHEMA: bool = False
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URL: str
    ADMIN_EMAIL: EmailStr | None = os.environ.get("ADMIN_EMAIL")
    COOKIE_SECURE: bool = False
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:8081",
        "http://localhost:8080",
        "http://localhost:8000",
    ]

    model_config = SettingsConfigDict(extra="ignore")


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_optional_int_env(name: str) -> int | None:
    value = os.environ.get(name)
    if value is None or value == "":
        return None
    return int(value)


def build_database_url() -> str:
    explicit_url = os.environ.get("DATABASE_URL")
    if explicit_url:
        return explicit_url

    return str(
        URL.create(
            drivername="postgresql+psycopg2",
            username=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_HOST"),
            port=get_optional_int_env("POSTGRES_PORT"),
            database=os.environ.get("POSTGRES_DB"),
        )
    )


settings = Settings(
    SECRET_KEY=get_required_env("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URL=build_database_url(),
)
