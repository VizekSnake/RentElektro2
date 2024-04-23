import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_new_user():
    # Send a POST request to register a new user
    user_data = {"email": "test@example.com", "password": "password123"}
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]

def test_register_existing_user():
    # Send a POST request to register a user with an email that already exists
    user_data = {"email": "test@example.com", "password": "password123"}
    response = client.post("/register", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]