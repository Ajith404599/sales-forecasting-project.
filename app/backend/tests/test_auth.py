def test_login_success(client):
    response = client.post("/auth/token", data={"username": "test_admin", "password": "admin123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "test_admin"
    assert data["user"]["role"] == "admin"


def test_login_with_email(client):
    response = client.post("/auth/token", data={"username": "manager@test.com", "password": "manager123"})
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "test_manager"
    assert data["user"]["role"] == "manager"


def test_login_wrong_password(client):
    response = client.post("/auth/token", data={"username": "test_admin", "password": "wrongpassword"})
    assert response.status_code == 401
    assert "Incorrect username/email or password" in response.json()["detail"]


def test_login_unknown_user(client):
    response = client.post("/auth/token", data={"username": "nonexistent_user", "password": "any"})
    assert response.status_code == 401


def test_login_inactive_user(client):
    response = client.post("/auth/token", data={"username": "test_inactive", "password": "inactive123"})
    assert response.status_code == 403
    assert "Account is inactive" in response.json()["detail"]
