import os

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    APP_NAME: str = "RentElektroAPI"
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URL: str
    ADMIN_EMAIL: EmailStr | None = os.environ.get("ADMIN_EMAIL")

    model_config = SettingsConfigDict(extra="ignore")


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
            port=os.environ.get("POSTGRES_PORT"),
            database=os.environ.get("POSTGRES_DB"),
        )
    )


settings = Settings(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URL=build_database_url(),
)
