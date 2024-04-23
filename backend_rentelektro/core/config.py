import os
from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URL: str


class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URL: str

    # Application Settings
    APP_NAME: str = "FastAPI Application"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database Settings
    SQLALCHEMY_DATABASE_URL: str

    # Security
    ALGORITHM: str = "HS256"
    ADMIN_EMAIL: EmailStr = "karol.gaca@imagen.team"

    class Config:
        # Configuration class meta-data
        env_file = "db.envs"
        env_file_encoding = 'utf-8'


# Construct the connection URL using environment variables
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
