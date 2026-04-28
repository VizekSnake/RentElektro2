def test_register_user(client):
    response = client.post(
        "/api/v1/users/register",
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
    response = client.get("/api/v1/users/user/1")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_update_user(client, test_user):
    response = client.patch(
        "/api/v1/users/user/1",
        json={
            "firstname": "Updated",
            "lastname": "User",
        },
    )
    assert response.status_code == 200
    assert response.json()["firstname"] == "Updated"


def test_delete_user(client, test_user):
    response = client.delete("/api/v1/users/delete/1")
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
