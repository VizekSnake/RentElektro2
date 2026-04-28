from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine_options = {}
if make_url(settings.SQLALCHEMY_DATABASE_URL).get_backend_name() == "postgresql":
    engine_options = {
        "pool_size": 3,
        "max_overflow": 0,
        "pool_timeout": 30,
        "pool_recycle": 3600,
    }

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
