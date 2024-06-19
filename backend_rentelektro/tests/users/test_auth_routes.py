import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from core.database import Base
from core.dependencies import get_db
from users.handlers import create_user
from users.schemas import UserCreate

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)  # Create the tables
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)  # Drop the tables after tests


@pytest.fixture(scope="function")
def test_user():
    user_data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword",
        "firstname": "Test",
        "lastname": "User",
        "phone": "1234567890",
        "company": True,
    }
    user = UserCreate(**user_data)
    with TestingSessionLocal() as db:
        created_user = create_user(db, user)
        db.commit()
        return created_user


def test_register_user(client):
    response = client.post(
        "http://0.0.0.0:8000/api/users/register",
        json={
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
            "firstname": "Test",
            "lastname": "User",
            "phone": "1234567890",
            "company": True,
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_login(client, test_user):
    response = client.post(
        "http://0.0.0.0:8000/api/users/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    Base.metadata.drop_all(engine)


def test_read_users_me(client, test_user):
    # First, login to get a token
    login_response = client.post(
        "http://0.0.0.0:8000/api/users/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "http://0.0.0.0:8000/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"



def test_read_current_user_data(client, test_user):
    # First, login to get a token
    login_response = client.post(
        "http://0.0.0.0:8000/api/users/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "http://0.0.0.0:8000/api/users/me/data",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_get_user(client, test_user):
    response = client.get("http://0.0.0.0:8000/api/users/user/1")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_update_user(client, test_user):
    response = client.patch(
        "http://0.0.0.0:8000/api/users/user/1",
        json={
            "firstname": "Updated",
            "lastname": "User",
        },
    )
    assert response.status_code == 200
    assert response.json()["firstname"] == "Updated"

def test_delete_user(client, test_user):
    response = client.delete("http://0.0.0.0:8000/api/users/delete/1")
    assert response.status_code == 204  # User not found

def test_refresh_access_token(client, test_user):
    # First, login to get a refresh token
    login_response = client.post(
        "http://0.0.0.0:8000/api/users/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "http://0.0.0.0:8000/api/users/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
