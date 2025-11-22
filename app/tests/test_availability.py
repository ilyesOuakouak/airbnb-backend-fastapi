from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.listing import Listing
from passlib.hash import bcrypt
import uuid
import pytest


client = TestClient(app)

def create_test_user():
    db = SessionLocal()
    hashed_password = bcrypt.hash("password123")
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    user = User(email=unique_email, hashed_password=hashed_password, first_name="Ilyes", last_name="Ouakouak")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def create_test_listing(user):
    db = SessionLocal()
    listing = Listing(title="Nice flat", description="Downtown", price_per_night=100, host_id=user.id)
    db.add(listing)
    db.commit()
    db.refresh(listing)
    db.close()
    return listing

def get_access_token(email):
    response = client.post("/users/login", json={"email": email, "password": "password123"})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_create_availability():
    user = create_test_user()
    token = get_access_token(user.email)
    listing = create_test_listing(user)
    test_date = date.today() + timedelta(days=1)

    payload = {
        "listing_id": listing.id,
        "date": test_date.isoformat(),
        "status": "available",
        "custom_price": 120.0,
        "checkout_only": False
    }

    response = client.post(
        "/availabilities/update",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()

    assert data["listing_id"] == listing.id
    assert data["date"].startswith(test_date.isoformat())
    assert data["status"] == "available"

@pytest.mark.skip(reason="Availability listing not implemented yet")
def test_get_availabilities():
    user = create_test_user()
    token = get_access_token(user.email)
    listing = create_test_listing(user)
    test_date = date.today() + timedelta(days=2)

    payload = {
        "listing_id": listing.id,
        "date": test_date.isoformat(),
        "status": "available",
        "custom_price": 150.0,
        "checkout_only": False
    }

    client.post("/availabilities/update", json=payload, headers={"Authorization": f"Bearer {token}"})

    response = client.get(
        f"/availabilities/{listing.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert any(a["date"].startswith(test_date.isoformat()) for a in data)