"""Test fixtures need environment variables before importing the FastAPI app."""

# ruff: noqa: E402

import os
import sys
from pathlib import Path

os.environ.setdefault("AUTO_CREATE_SCHEMA", "false")
os.environ["DEBUG"] = "false"
os.environ.setdefault("SECRET_KEY", "test-secret-key-with-32-bytes-min")
os.environ.setdefault("DATABASE_URL", "sqlite://")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.main import app
from app.modules.rentals import models as rentals_models  # noqa: F401
from app.modules.reviews import models as reviews_models  # noqa: F401
from app.modules.tools import models as tools_models  # noqa: F401
from app.modules.users import models as users_models  # noqa: F401
from app.modules.users.schemas import UserCreate
from app.modules.users.service import create_user

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def test_user(db_session):
    user_data = UserCreate(
        email="testuser@example.com",
        username="testuser",
        password="testpassword",
        firstname="Test",
        lastname="User",
        phone="1234567890",
        company=True,
    )
    return create_user(db_session, user_data)


@pytest.fixture(scope="function")
def auth_client(client, test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    try:
        yield client
    finally:
        app.dependency_overrides.pop(get_current_user, None)
