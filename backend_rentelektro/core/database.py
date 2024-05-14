import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# # Construct the connection URL using environment variables
# DB_USER = os.environ.get("POSTGRES_USER")
# DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
# DB_HOST = os.environ.get("POSTGRES_HOST")
# DB_PORT = os.environ.get("POSTGRES_PORT")
# DB_NAME = os.environ.get("POSTGRES_DB")
# SECRET_KEY = os.environ.get("SECRET_KEY")
# DB_CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# SQLALCHEMY_DATABASE_URL = DB_CONNECTION_STRING
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     pool_size=3,
#     max_overflow=0,
#     pool_timeout=30,
#     pool_recycle=3600,
# )
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()

import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Construct the connection URL using environment variables
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
SECRET_KEY = os.environ.get("SECRET_KEY")
DB_CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URL = DB_CONNECTION_STRING

try:
    # Create the SQLAlchemy engine
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=3,
        max_overflow=0,
        pool_timeout=30,
        pool_recycle=3600,
    )

    # Attempt to connect to the database
    connection = engine.connect()
    print("Database connection successful.")

    # Optional: perform a test query
    try:
        result = connection.execute("SELECT 1")
        print("Test query successful, result:", result.scalar())
    except SQLAlchemyError as e:
        print("Test query failed:", e)
    finally:
        connection.close()  # Make sure to close the connection

except SQLAlchemyError as ex:
    print(f"Database connection failed: {ex}")

# Setup session and base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

