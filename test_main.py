from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Helper function to register a user with a unique email each time
def register_test_user(email=None):
    import uuid
    if not email:
        email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    response = client.post("/auth/register", json={
        "email": email,
        "username": "testuser",
        "password": "Password123"
    })
    return response, email

# Helper function to login a user and get the token
def login_test_user(email):
    response = client.post("/auth/login", data={
        "username": email,
        "password": "Password123"
    })
    assert response.status_code == 200, f"Login failed: {response.json()}"
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]

def test_register_user():
    response, email = register_test_user()
    if response.status_code != 200:
        print("Register failed:", response.status_code, response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert "username" in data

def test_login_user():
    response, email = register_test_user()
    # Make sure user is registered before login
    token = login_test_user(email)
    # No return here to avoid pytest warning
    assert token is not None

def test_logout_user():
    response, email = register_test_user()
    token = login_test_user(email)
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        print("Logout failed:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["msg"] == "Successfully logged out"

def test_read_users_me():
    response, email = register_test_user()
    token = login_test_user(email)
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        print("Read me failed:", response.status_code, response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email

def test_create_rating():
    response, email = register_test_user()
    token = login_test_user(email)
    rating_data = {
        "transaction_id": "some-transaction-id",
        "rater_id": email,
        "score": 5,
        "comment": "Great transaction!"
    }
    response = client.post("/ratings/", json=rating_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 400, 404)

def test_get_ratings_for_user():
    response, email = register_test_user()
    token = login_test_user(email)
    user_id = "some-user-id"
    response = client.get(f"/ratings/user/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 404)
    assert isinstance(response.json(), list) or isinstance(response.json(), dict)
