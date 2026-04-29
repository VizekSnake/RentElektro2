from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ENV_FILES = (
    str(BASE_DIR / "envs" / "config.dev.env"),
    str(BASE_DIR / "envs" / "postgres.dev.env"),
)


class Settings(BaseSettings):
    APP_NAME: str = "RentElektroAPI"
    API_V1_STR: str = "/api/v1"
    APP_DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30
    PASSWORD_RESET_URL_BASE: str = "http://localhost/reset-password"
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    EMAIL_DELIVERY_MODE: Literal["console", "smtp"] = "console"
    MAIL_FROM_EMAIL: EmailStr | None = None
    MAIL_FROM_NAME: str = "RentElektro"
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False
    DATABASE_URL: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_DB: str | None = None
    ADMIN_EMAIL: EmailStr | None = None
    COOKIE_SECURE: bool = False
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:8081",
        "http://localhost:8080",
        "http://localhost:8000",
    ]

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=DEFAULT_ENV_FILES,
        env_file_encoding="utf-8",
    )

    @property
    def DEBUG(self) -> bool:
        return self.APP_DEBUG

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL

        required_parts = {
            "POSTGRES_USER": self.POSTGRES_USER,
            "POSTGRES_PASSWORD": self.POSTGRES_PASSWORD,
            "POSTGRES_HOST": self.POSTGRES_HOST,
            "POSTGRES_DB": self.POSTGRES_DB,
        }
        missing = [name for name, value in required_parts.items() if not value]
        if missing:
            missing_vars = ", ".join(missing)
            raise RuntimeError(f"Missing required database environment variables: {missing_vars}")

        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        ).render_as_string(hide_password=False)


@lru_cache
def get_settings() -> Settings:
    # SECRET_KEY is intentionally required and comes from env files at runtime.
    return Settings()  # type: ignore[call-arg]
