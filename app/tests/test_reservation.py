from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.listing import Listing
from passlib.hash import bcrypt
import uuid

client = TestClient(app)

def create_test_user():
    db = SessionLocal()
    hashed_password = bcrypt.hash("password123")
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    user = User(email=unique_email, hashed_password=hashed_password, first_name="John", last_name="Doe")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def create_test_listing(user):
    db = SessionLocal()
    listing = Listing(title="Cozy Loft", description="Downtown stay", price_per_night=100, host_id=user.id)
    db.add(listing)
    db.commit()
    db.refresh(listing)
    db.close()
    return listing

def get_access_token(email):
    response = client.post("/users/login", json={"email": email, "password": "password123"})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_create_reservation():
    user = create_test_user()
    token = get_access_token(user.email)
    listing = create_test_listing(user)
    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=2)

    payload = {
        "listing_id": listing.id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "total_amount": 200.0
    }

    response = client.post("/reservations/create", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["listing_id"] == listing.id
    assert data["status"] == "pending"


def test_get_my_reservations():
    user = create_test_user()
    token = get_access_token(user.email)
    listing = create_test_listing(user)
    start_date = date.today() + timedelta(days=3)
    end_date = start_date + timedelta(days=2)

    payload = {
        "listing_id": listing.id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "total_amount": 300.0
    }

    client.post("/reservations/create", json=payload, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/reservations/my", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_cancel_reservation():
    user = create_test_user()
    token = get_access_token(user.email)
    listing = create_test_listing(user)
    start_date = date.today() + timedelta(days=5)
    end_date = start_date + timedelta(days=2)

    payload = {
        "listing_id": listing.id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "total_amount": 400.0
    }

    create_response = client.post("/reservations/create", json=payload, headers={"Authorization": f"Bearer {token}"})
    reservation_id = create_response.json()["id"]

    delete_response = client.delete(f"/reservations/{reservation_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == 204
