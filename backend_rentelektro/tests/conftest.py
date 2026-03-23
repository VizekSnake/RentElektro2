import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base
from core.dependencies import get_db
from core.security import get_current_user
from main import app
from users.handlers import create_user
from users.schemas import UserCreate

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
