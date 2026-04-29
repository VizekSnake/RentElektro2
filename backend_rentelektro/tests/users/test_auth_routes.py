import re

from app.core.security import verify_password
from app.modules.users.models import (
    PasswordResetToken as PasswordResetTokenModel,
    User as UserModel,
)


def test_register_user(client):
    response = client.post(
        "/api/v1/users",
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
        "/api/v1/users/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert response.json()["authenticated"] is True
    assert "access_token" in response.cookies


def test_read_users_me(client, test_user):
    # First, login to get a token
    client.post("/api/v1/users/login", data={"username": "testuser", "password": "testpassword"})

    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_read_current_user_data(client, test_user):
    # First, login to get a token
    client.post("/api/v1/users/login", data={"username": "testuser", "password": "testpassword"})

    response = client.get("/api/v1/users/me/data")
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_get_user(client, test_user):
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_update_user(client, test_user):
    response = client.patch(
        "/api/v1/users/1",
        json={
            "firstname": "Updated",
            "lastname": "User",
        },
    )
    assert response.status_code == 200
    assert response.json()["firstname"] == "Updated"


def test_delete_user(client, test_user):
    response = client.delete("/api/v1/users/1")
    assert response.status_code == 204  # User not found


def test_refresh_access_token(client, test_user):
    # First, login to get a refresh token
    client.post(
        "/api/v1/users/token",
        data={"username": "testuser", "password": "testpassword"},
    )

    response = client.post("/api/v1/users/refresh")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def extract_reset_token(log_text: str) -> str:
    match = re.search(r"token=([A-Za-z0-9_-]+)", log_text)
    assert match is not None
    return match.group(1)


def test_request_password_reset_returns_accepted_for_known_email(
    client, db_session, test_user, caplog
):
    with caplog.at_level("INFO"):
        response = client.post(
            "/api/v1/users/password-reset/request",
            json={"email": "testuser@example.com"},
        )

    assert response.status_code == 202
    assert "link do resetu hasla" in response.json()["message"]
    assert db_session.query(PasswordResetTokenModel).count() == 1
    assert "console_email_delivery" in caplog.text


def test_request_password_reset_returns_accepted_for_unknown_email(client, db_session, caplog):
    with caplog.at_level("INFO"):
        response = client.post(
            "/api/v1/users/password-reset/request",
            json={"email": "missing@example.com"},
        )

    assert response.status_code == 202
    assert db_session.query(PasswordResetTokenModel).count() == 0
    assert "console_email_delivery" not in caplog.text


def test_confirm_password_reset_updates_password(client, db_session, test_user, caplog):
    with caplog.at_level("INFO"):
        client.post(
            "/api/v1/users/password-reset/request",
            json={"email": "testuser@example.com"},
        )

    token = extract_reset_token(caplog.text)
    response = client.post(
        "/api/v1/users/password-reset/confirm",
        json={"token": token, "new_password": "newpassword123"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Haslo zostalo zresetowane."
    assert db_session.query(PasswordResetTokenModel).count() == 0

    db_session.expire_all()
    updated_user = db_session.query(UserModel).filter(UserModel.id == test_user.id).first()
    assert updated_user is not None
    assert verify_password("newpassword123", updated_user.hashed_password)

    old_login = client.post(
        "/api/v1/users/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert old_login.status_code == 401

    new_login = client.post(
        "/api/v1/users/login",
        data={"username": "testuser", "password": "newpassword123"},
    )
    assert new_login.status_code == 200
