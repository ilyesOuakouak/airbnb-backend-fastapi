import uuid
from datetime import datetime, timezone, timedelta

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import  SessionLocal
from app.models.user import User
from passlib.hash import bcrypt

client = TestClient(app)

def cleanup_test_user(email: str):
    """Utility: clean up user after test to avoid unique constraint errors."""
    db = SessionLocal()
    db.query(User).filter(User.email == email).delete()
    db.commit()
    db.close()

def create_test_user():
    db = SessionLocal()
    hashed_password = bcrypt.hash("password123")
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    test_user = User(
        email=unique_email,
        hashed_password=hashed_password,
        first_name="Test",
        last_name="User"
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()

    return test_user

def test_get_user_by_id():
    user = create_test_user()

    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email
    assert "password" not in data # password should never appear

def test_register_user():
    test_email = "test_register_user@example.com"
    cleanup_test_user(test_email)

    payload = {
        "email": test_email,
        "password": "password123",
        "first_name": "Ilyes",
        "last_name": "Ouakouak",
        "created_at": (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
    }

    response = client.post(f"/users/register", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data['email'] == test_email
    assert "id" in data
    assert isinstance(data['id'], int)

    db = SessionLocal()
    user = db.query(User).filter(User.email == test_email).first()
    assert user is not None
    assert user.first_name == "Ilyes"
    db.close()

    cleanup_test_user(test_email)