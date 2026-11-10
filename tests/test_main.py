def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Crypto Tracker API is running"
    }
def test_invalid_coin(client):
    response = client.get("/coins/dogecoin")

    assert response.status_code == 404
    assert response.json()["detail"] == "Coin_id not found"
def test_history_not_found(client):
    response = client.get("/coins/dogecoin/history")

    assert response.status_code == 404
    assert "No price history found" in response.json()["detail"]
def test_change_not_found(client):
    response = client.get("/coins/dogecoin/change")

    assert response.status_code == 404
    assert response.json()["detail"] == "Fewer than 2 snapshots found."
def test_register_invalid_email(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "not-an-email",
            "password": "test123"
        }
    )

    assert response.status_code == 422

def test_register_user(client):
    response = client.post(
        "/register",
        json={
            "username": "vedika",
            "email": "vedika@example.com",
            "password": "test123"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
def test_duplicate_username(client):
    user_data = {
        "username": "vedika",
        "email": "vedika@example.com",
        "password": "test123"
    }

    first_response = client.post("/register", json=user_data)

    second_user_data = {
        "username": "vedika",
        "email": "another@example.com",
        "password": "test123"
    }

    second_response = client.post(
        "/register",
        json=second_user_data
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Username already exists"
def test_duplicate_email(client):
    first_user = {
        "username": "user1",
        "email": "same@example.com",
        "password": "test123"
    }

    second_user = {
        "username": "user2",
        "email": "same@example.com",
        "password": "test123"
    }

    first_response = client.post("/register", json=first_user)
    second_response = client.post("/register", json=second_user)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email already exists"
def test_login_wrong_password(client):
    # First, register a user
    client.post(
        "/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "correct123"
        }
    )

    # Now try logging in with the wrong password
    response = client.post(
        "/login",
        json={
            "username": "loginuser",
            "password": "wrong123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
def test_login_success(client):
    client.post(
        "/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "correct123"
        }
    )

    response = client.post(
        "/login",
        json={
            "username": "loginuser",
            "password": "correct123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
def test_me_without_token(client):
    response = client.get("/me")

    assert response.status_code == 401
def test_me_with_valid_token(client):
    client.post(
        "/register",
        json={
            "username": "tokenuser",
            "email": "tokenuser@example.com",
            "password": "test123"
        }
    )

    login_response = client.post(
        "/login",
        json={
            "username": "tokenuser",
            "password": "test123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == "tokenuser"
def get_auth_headers(client):
    client.post(
        "/register",
        json={
            "username": "watchuser",
            "email": "watchuser@example.com",
            "password": "test123"
        }
    )

    login_response = client.post(
        "/login",
        json={
            "username": "watchuser",
            "password": "test123"
        }
    )

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
def test_add_to_watchlist(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/watchlist",
        json={"coin_id": "bitcoin"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["coin_id"] == "bitcoin"
def test_view_watchlist(client):
    headers = get_auth_headers(client)

    client.post(
        "/watchlist",
        json={"coin_id": "bitcoin"},
        headers=headers
    )

    response = client.get("/watchlist", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["coin_id"] == "bitcoin"
def test_duplicate_coin(client):
    headers = get_auth_headers(client)

    client.post(
        "/watchlist",
        json={"coin_id": "bitcoin"},
        headers=headers
    )

    response = client.post(
        "/watchlist",
        json={"coin_id": "bitcoin"},
        headers=headers
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Coin already in watchlist"
def test_remove_from_watchlist(client):
    headers = get_auth_headers(client)

    client.post(
        "/watchlist",
        json={"coin_id": "bitcoin"},
        headers=headers
    )

    response = client.delete(
        "/watchlist/bitcoin",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Coin removed successfully"
def test_add_unsupported_coin(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/watchlist",
        json={"coin_id": "dogecoin"},
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported coin"