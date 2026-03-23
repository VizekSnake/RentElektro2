import os
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "RentElektroAPI"
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URL: str
    ADMIN_EMAIL: EmailStr | None = os.environ.get("ADMIN_EMAIL")

    model_config = SettingsConfigDict(extra="ignore")


DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
SECRET_KEY = os.environ.get("SECRET_KEY")
DB_CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
database_url = DB_CONNECTION_STRING
settings = Settings(
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_DATABASE_URL=database_url
)
