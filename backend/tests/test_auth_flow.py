import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import get_session

# Create a new in-memory SQLite engine for testing
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Fixture to create and clean up database
@pytest.fixture
def session():
    # Ensure models are registered
    from app.auth.models import User  # import models so SQLModel metadata includes them
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)

# Fixture to provide a TestClient with overridden dependency
@pytest.fixture
def client(session):
    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        yield client


def test_register_login_me(client):
    # 1. Register a new user
    register_data = {"email": "test@example.com", "password": "secret"}
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 201
    payload = response.json()
    assert payload["email"] == register_data["email"]
    assert "id" in payload

    # 2. Login with that user
    login_data = {"username": register_data["email"], "password": register_data["password"]}
    response = client.post(
        "/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

    # 3. Access /me with the token
    auth_header = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["email"] == register_data["email"]


def test_duplicate_register(client):
    data = {"email": "dup@example.com", "password": "pw"}
    # first registration succeeds
    r1 = client.post("/auth/register", json=data)
    assert r1.status_code == 201
    # duplicate registration should fail
    r2 = client.post("/auth/register", json=data)
    assert r2.status_code == 400
    assert "Email already registered" in r2.json()["detail"]


def test_login_wrong_credentials(client):
    # no such user
    r1 = client.post(
        "/auth/login",
        data={"username": "nouser@example.com", "password": "pw"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert r1.status_code == 401
    # register then wrong password
    client.post("/auth/register", json={"email": "user2@example.com", "password": "rightpw"})
    r2 = client.post(
        "/auth/login",
        data={"username": "user2@example.com", "password": "wrongpw"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert r2.status_code == 401


def test_me_requires_auth(client):
    # no header
    r1 = client.get("/me")
    assert r1.status_code == 401
    # invalid token
    r2 = client.get("/me", headers={"Authorization": "Bearer invalid.token.here"})
    assert r2.status_code == 401
