import uuid
from datetime import datetime, timezone, timedelta
from http.client import responses

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import  SessionLocal
from app.models.listing import Listing
from app.models.user import User
from passlib.hash import bcrypt

client = TestClient(app)

def cleanup_test_listing(title: str):
    db = SessionLocal()
    db.query(Listing).filter(Listing.title == title).delete()
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

def get_access_token(email: str):
    response = client.post(
        "/users/login",
        json={"email": email, "password": "password123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

def test_create_listing():
    user = create_test_user()
    token = get_access_token(user.email)
    unique_title = f"Beautiful Apartment { uuid.uuid4().hex[:6]}"

    payload = {
        "title": unique_title,
        "description": "Good appart",
        "price_per_night": 99.99
    }

    response = client.post(
        "/listings/create",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()

    assert data['title'] == unique_title
    assert data['price_per_night'] == 99.99
    assert "id" in data

    cleanup_test_listing(unique_title)

def test_get_all_listings():
    user = create_test_user()
    token = get_access_token(user.email)
    unique_title = f"Beautiful Apartment { uuid.uuid4().hex[:6]}"

    payload = {
        "title": unique_title,
        "description": "Cozy loft for testing",
        "price_per_night": 120.0
    }

    create_response = client.post(
        "/listings/create",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 201

    # Now call the list endpoint
    response = client.get(
        "/listings/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(listing["title"] == unique_title for listing in data)

    cleanup_test_listing(unique_title)



