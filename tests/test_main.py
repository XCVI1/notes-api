import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/notesdb"
)

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# helpers
def register_user(username="testuser", email="test@test.com", password="password123"):
    return client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })


def get_token(username="testuser", password="password123"):
    response = client.post("/auth/login", data={
        "username": username,
        "password": password
    })
    return response.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# health
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# auth
def test_register():
    response = register_user()
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"


def test_register_duplicate_username():
    register_user()
    response = register_user()
    assert response.status_code == 400


def test_register_duplicate_email():
    register_user()
    response = register_user(username="otheruser")
    assert response.status_code == 400


def test_login():
    register_user()
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    register_user()
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


# notes
def test_create_note():
    register_user()
    token = get_token()
    response = client.post("/notes/", json={
        "title": "Test note",
        "content": "Test content"
    }, headers=auth_headers(token))
    assert response.status_code == 201
    assert response.json()["title"] == "Test note"


def test_get_my_notes():
    register_user()
    token = get_token()
    headers = auth_headers(token)
    client.post("/notes/", json={"title": "Note 1", "content": "Content 1"}, headers=headers)
    client.post("/notes/", json={"title": "Note 2", "content": "Content 2"}, headers=headers)
    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_public_notes():
    register_user()
    token = get_token()
    client.post("/notes/", json={
        "title": "Public note",
        "content": "Content",
        "is_public": True
    }, headers=auth_headers(token))
    response = client.get("/notes/public")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_note_unauthorized():
    response = client.get("/notes/")
    assert response.status_code == 401


def test_update_note():
    register_user()
    token = get_token()
    headers = auth_headers(token)
    note = client.post("/notes/", json={
        "title": "Old title",
        "content": "Content"
    }, headers=headers).json()
    response = client.put(f"/notes/{note['id']}", json={
        "title": "New title"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_delete_note():
    register_user()
    token = get_token()
    headers = auth_headers(token)
    note = client.post("/notes/", json={
        "title": "To delete",
        "content": "Content"
    }, headers=headers).json()
    response = client.delete(f"/notes/{note['id']}", headers=headers)
    assert response.status_code == 204


def test_delete_note_other_user():
    register_user()
    register_user(username="user2", email="user2@test.com")
    token1 = get_token()
    token2 = get_token(username="user2")
    note = client.post("/notes/", json={
        "title": "Private",
        "content": "Content"
    }, headers=auth_headers(token1)).json()
    response = client.delete(f"/notes/{note['id']}", headers=auth_headers(token2))
    assert response.status_code == 403


def test_get_private_note_other_user():
    register_user()
    register_user(username="user2", email="user2@test.com")
    token1 = get_token()
    token2 = get_token(username="user2")
    note = client.post("/notes/", json={
        "title": "Private",
        "content": "Content",
        "is_public": False
    }, headers=auth_headers(token1)).json()
    response = client.get(f"/notes/{note['id']}", headers=auth_headers(token2))
    assert response.status_code == 403
